# Курс по средней части компилятора

Самостоятельный русскоязычный курс по средней части компилятора: от базовых блоков и CFG до SSA, ациклических оптимизаций и преобразований циклов.

## Что внутри

- 20 занятий по схеме «проблема → определения → модель → полная трасса → правило → практика»;
- словарь из 100 терминов с простыми и точными объяснениями;
- отдельные разделы с необходимыми предварительными понятиями: семантический анализ, DFS и SCC, каноническая форма цикла и межитерационные зависимости;
- ответы рядом с задачами и банк новых задач для проверки переноса навыка;
- учебный инструмент на Python, который показывает не только итог анализа, но и промежуточные состояния.

## Сайт

https://misha1302.github.io/Middle-end-compiler-cource/

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m pip install -r requirements-docs.txt
mkdocs serve
```

## Учебный анализатор

```bash
course-cfg dominators examples/diamond.json --trace
course-cfg natural-loop examples/loop.json --header B1 --latch B3 --trace
```

Старый вызов `course-cfg examples/diamond.json` сохранён как сокращение для команды `summary`.

## Проверка

```bash
python scripts/validate_course.py
python -m unittest discover -s tests -v
mkdocs build --strict
```

Код опубликован под MIT, учебные материалы — под CC BY 4.0.
