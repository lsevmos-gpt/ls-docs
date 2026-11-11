#!/usr/bin/env python3
"""Validate the coordinated 6D amendment and date its publication explicitly."""
import argparse
from datetime import date, datetime, timedelta
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo

REVISION = '2026-11-11'
TARGETS = ('oferta', 'rules')
DOMAIN = 'https://docs.liniyasporta.ru'
NOTICE = re.compile(r'<section class="legal-revision"[^>]*>.*?</section>', re.S)


class Clauses(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = {}
        self.current = None
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'p' and attrs.get('data-legal-clause'):
            self.current = attrs['data-legal-clause']
            self.parts = []

    def handle_data(self, data):
        if self.current is not None:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'p' and self.current is not None:
            text = ' '.join(''.join(self.parts).split())
            text = re.sub(r'^\d+(?:\.\d+)*\.\s*', '', text)
            self.values.setdefault(self.current, []).append(text)
            self.current = None


def load(root):
    base = root / 'legal' / REVISION
    return json.loads((base / 'release.json').read_text()), json.loads((base / 'clauses.json').read_text())


def today():
    return datetime.now(ZoneInfo('Europe/Moscow')).date()


def effective_date(publication, minimum_days=10):
    # The ten complete calendar days after publication precede the effective date.
    return publication + timedelta(days=minimum_days + 1)


def check(root, for_deploy=False, now=None):
    meta, expected = load(root)
    totals = {}
    for kind in TARGETS:
        source = (root / 'site' / kind / 'index.html').read_text()
        parser = Clauses()
        parser.feed(source)
        count = 2 if kind == 'oferta' else 1
        for key, value in expected.items():
            wanted = 0 if key == '3.9' and kind == 'rules' else count
            values = parser.values.get(key, [])
            if len(values) != wanted or any(v != value for v in values):
                raise ValueError(f'{kind}: inconsistent clause {key}')
        if len(NOTICE.findall(source)) != count:
            raise ValueError(f'{kind}: revision notice missing')
        if '1 500' in source or '1500' in source or 'бесхозяйной вещи' in source:
            raise ValueError(f'{kind}: superseded automatic storage clause remains')
        if kind == 'oferta':
            if 'марта 2026 года' not in source or re.search(r'Приложени[еи]\s*№\s*4', source):
                raise ValueError('Original offer date or appendix references are inconsistent')
        if kind == 'rules' and 'февраля 2026 года' in source:
            raise ValueError('Separate rules still reference the wrong original date')
        archived = root / 'site' / meta['archive_base'].strip('/') / kind / 'index.html'
        if not archived.is_file():
            raise ValueError(f'{kind}: previous version archive missing')
        totals[kind] = count
        state = 'draft' if meta['status'] == 'prepared' else 'announced'
        if source.count(f'data-publication-state="{state}"') != count:
            raise ValueError(f'{kind}: notice and release state differ')

    if for_deploy:
        if meta['status'] != 'announced':
            raise ValueError('This revision is prepared, not dated for publication. Run legal_release.py stamp immediately before publishing.')
        published = date.fromisoformat(meta['publication_date'])
        active = date.fromisoformat(meta['effective_date'])
        now = now or today()
        if published > now or active != effective_date(published, meta['minimum_notice_days']):
            raise ValueError('Invalid publication or effective date')
        if published < now:
            # A later routine redeploy may preserve dates only if the first notice is already live.
            url = f'{DOMAIN}/legal-releases/{REVISION}.json'
            request = urllib.request.Request(url, headers={'Cache-Control': 'no-cache'})
            with urllib.request.urlopen(request, timeout=20) as response:
                live = json.load(response)
            if live.get('publication_date') != meta['publication_date'] or live.get('revision') != REVISION:
                raise ValueError('Cannot confirm the earlier publication date on the live site')
    return totals


def stamp(root, publication, now=None):
    meta, _ = load(root)
    if publication != (now or today()):
        raise ValueError('First publication must be dated with the actual Moscow date; backdating and future dating are rejected')
    if meta['status'] != 'prepared':
        if meta['publication_date'] == publication.isoformat():
            check(root)
            return meta
        raise ValueError('This revision already has a first-publication date; do not reset the notice period')
    check(root)
    active = effective_date(publication, meta['minimum_notice_days'])
    published_ru = publication.strftime('%d.%m.%Y')
    active_ru = active.strftime('%d.%m.%Y')
    for kind in TARGETS:
        path = root / 'site' / kind / 'index.html'
        notice = f'''<section class="legal-revision" data-legal-revision="{REVISION}" data-publication-state="announced">
<p><b>Редакция от 11 ноября 2026 года</b></p>
<p>Дата опубликования: <time datetime="{publication.isoformat()}">{published_ru}</time>. Вступает в силу: <time datetime="{active.isoformat()}">{active_ru}</time>.</p>
<p>До даты вступления в силу применяется <a href="{meta['archive_base']}/{kind}/">предыдущая редакция</a>. Новые положения не применяются задним числом; права по ранее заключённым договорам и согласованные условия оплаченных услуг сохраняются в пределах закона.</p>
</section>'''
        path.write_text(NOTICE.sub(lambda match: notice, path.read_text()))
    meta.update(status='announced', publication_date=publication.isoformat(), effective_date=active.isoformat())
    text = json.dumps(meta, ensure_ascii=False, indent=2) + '\n'
    (root / 'legal' / REVISION / 'release.json').write_text(text)
    public = root / 'site' / 'legal-releases' / f'{REVISION}.json'
    public.parent.mkdir(parents=True, exist_ok=True)
    public.write_text(text)
    (root / 'legal' / REVISION / 'NOTICE_RU.txt').write_text(
        'УВЕДОМЛЕНИЕ О НОВОЙ РЕДАКЦИИ ОФЕРТЫ И ПРАВИЛ КЛУБА\n\n'
        f'Опубликовано {published_ru}. Новая редакция вступает в силу {active_ru}.\n'
        'Уточняются проход по QR-коду и браслету в клубе на Героев Сталинграда, 6Д, '
        'временное пользование шкафчиками и ячейками, исключение для оплаченной аренды, '
        'действия при сбоях и порядок возврата забытых вещей.\n'
        f'Документы: {DOMAIN}/oferta/ и {DOMAIN}/rules/.\n'
        'До указанной даты применяется предыдущая редакция, доступная по ссылке в документах. '
        'Новая редакция не вводит автоматическую платную аренду, хранение или штрафы.\n'
    )
    check(root)
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'stamp'])
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--publication-date', type=date.fromisoformat)
    parser.add_argument('--for-deploy', action='store_true')
    args = parser.parse_args()
    try:
        if args.action == 'stamp':
            result = stamp(args.root, args.publication_date or today())
        else:
            result = check(args.root, args.for_deploy)
    except (ValueError, OSError, urllib.error.URLError) as error:
        parser.exit(1, f'Legal release check failed: {error}\n')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
