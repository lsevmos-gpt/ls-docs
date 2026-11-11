from datetime import date
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('legal_release',ROOT/'scripts/legal_release.py')
release=importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class LegalReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        shutil.copytree(ROOT/'legal',self.root/'legal')
        for name in ['oferta','rules','archive']:
            shutil.copytree(ROOT/'site'/name,self.root/'site'/name)
        self.day=date(2026,11,11)

    def tearDown(self):
        self.temp.cleanup()

    def test_ten_complete_calendar_days(self):
        self.assertEqual(release.effective_date(self.day),date(2026,11,22))
        self.assertEqual(release.effective_date(date(2026,12,25)),date(2027,1,5))
        self.assertEqual(release.effective_date(date(2028,2,20)),date(2028,3,2))

    def test_undated_project_is_not_deployable(self):
        release.check(self.root)
        with self.assertRaisesRegex(ValueError,'prepared'):
            release.check(self.root,True,now=self.day)

    def test_backdate_and_future_date_are_rejected(self):
        before=(self.root/'site/oferta/index.html').read_bytes()
        for candidate in [date(2026,9,28),date(2026,11,12)]:
            with self.assertRaisesRegex(ValueError,'actual Moscow date'):
                release.stamp(self.root,candidate,now=self.day)
        self.assertEqual(before,(self.root/'site/oferta/index.html').read_bytes())

    def test_publication_dates_match_all_three_rule_copies(self):
        data=release.stamp(self.root,self.day,now=self.day)
        self.assertEqual(data['effective_date'],'2026-11-22')
        self.assertEqual(release.check(self.root,True,now=self.day),{'oferta':2,'rules':1})
        offer=(self.root/'site/oferta/index.html').read_text()
        rules=(self.root/'site/rules/index.html').read_text()
        self.assertEqual(offer.count('data-publication-state="announced"'),2)
        self.assertEqual(rules.count('data-publication-state="announced"'),1)
        self.assertNotIn('data-publication-state="draft"',offer+rules)
        self.assertEqual(json.loads((self.root/'site/legal-releases/2026-11-11.json').read_text()),data)

    def test_repeated_same_day_stamp_preserves_publication(self):
        release.stamp(self.root,self.day,now=self.day)
        before=(self.root/'site/oferta/index.html').read_bytes()
        release.stamp(self.root,self.day,now=self.day)
        self.assertEqual(before,(self.root/'site/oferta/index.html').read_bytes())
        with self.assertRaisesRegex(ValueError,'already has'):
            release.stamp(self.root,date(2026,11,12),now=date(2026,11,12))

    def test_old_published_pages_are_preserved(self):
        archive=self.root/'site/archive/2026-11-11-before-6d'
        before={n:(archive/n/'index.html').read_bytes() for n in ['oferta','rules']}
        release.stamp(self.root,self.day,now=self.day)
        for name,data in before.items():
            self.assertEqual(data,(archive/name/'index.html').read_bytes())


if __name__=='__main__':
    unittest.main()
