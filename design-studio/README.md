# Liniya Sporta Design Studio · v1.0

Единая система для разработки дизайнерских материалов спортивного клуба «Линия спорта». Создана 23.10.2026 как расширение действующего стандарта Visual System v1.7 — НЕ новый брендбук и НЕ замена MASTER.

## Что включено
- 1 управляющий skill: ls-design-studio.
- 8 специализированных skills: ls-typography, ls-interior, ls-signage, ls-pictograms, ls-print, ls-brand, ls-design-critic, ls-digital-display.
- 5 Codex subagents: ls_creative_director, ls_typographer, ls_interior_designer, ls_signage_designer, ls_design_critic.
- Правила AGENTS.md, установка для Windows/macOS/Linux, инструкция проекта ChatGPT, контрольный список.

## Установка в Codex
Если работаете непосредственно в клонированном ls-docs, Codex автоматически читает корневой AGENTS.md, skills из .agents/skills и проектных агентов .codex/agents.

Если хотите пользоваться специалистами ВО ВСЕХ репозиториях, клонируйте ls-docs и запустите:
- Windows PowerShell: powershell -ExecutionPolicy Bypass -File .\design-studio\install.ps1
- macOS/Linux: bash ./design-studio/install.sh

Скрипты устанавливают пользовательские skills в ~/.agents/skills и субагентов в ~/.codex/agents, а также добавляют бренд-ограниченный блок в ~/.codex/AGENTS.md без удаления остального. При совпадении имён сохраняют резервные копии. После установки перезапустите Codex. Проверка: /skills, затем запрос «Разработай квадратный знак для скалодрома Линии спорта, используй ls-design-studio и ls-design-critic».

Наличие этих файлов в GitHub НЕ означает, что навыки автоматически доступны из любого другого уже открытого репозитория, пока пользовательская установка не выполнена.

## ChatGPT
Для ChatGPT на вебе: откройте проект по дизайну «Линии спорта» и добавьте содержание design-studio/chatgpt-project-instructions.md в настройки Project instructions. Настоящие пользовательские навыки могут быть добавлены через поддерживаемую систему Skills/Plugin Creator, если она доступна в вашем аккаунте. GitHub-интеграция и память сами по себе НЕ устанавливают кастомный плагин во все чаты.

Текущий файл — готовый источник для создания такого навыка. Запрос в ChatGPT: «Используй правила Liniya Sporta Design Studio из GitHub ls-docs и действующий Visual System из подключённого Google Drive».

## Цепочка принятия решения
BRIEF → SOURCE PREFLIGHT → CONCEPTS → SPECIALIST → MOCKUP → INDEPENDENT CRITIQUE → FIX → PRODUCTION QA → READY.

Не запускать всех специалистов механически; по каждой задаче выбираются релевантные. Ревью обязательно.

## Источники
Первоисточник: Google Drive / Линия спорта / 00_ФИРМЕННЫЙ_СТИЛЬ_MASTER / 00_CURRENT_VISUAL_GUIDE.txt. Текущий указатель по состоянию на 23.10.2026: Visual System v1.7, AI Execution Rules v1.7, Quality Gates v1.7 и шесть оригинальных логотипов MASTER от 16.10.2026. Названия и версии здесь справочные, проверяйте обновления.

## Статусы
- READY — исходники и файл реально проверены, критических ошибок нет.
- DRAFT — результат существует, но не прошёл все проверки / требуется согласование.
- BLOCKED — нет необходимых источников или существуют критические ошибки.

## Изменения
v1.0 — первичная структура, типографика, интерьеры, графическая навигация, пиктограммы, производство, ревью; правила безопасности и разделение клуб/фитнес.
