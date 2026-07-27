# Middle-end Compiler Course

Самостоятельный русскоязычный курс по middle-end компилятора: от basic blocks и CFG до SSA, ациклических и цикловых оптимизаций.

## Что внутри

- 20 занятий в порядке «проблема → определения → модель → полная трасса → правило → практика»;
- 100 терминов с готовым простым и точным объяснением;
- явные prerequisite bridges по semantic analysis, DFS/SCC, canonical loops и loop-carried dependences;
- локальные ответы к задачам и банк transfer-задач;
- Python-инструмент, который показывает финальные анализы и промежуточные состояния.

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

Старый вызов `course-cfg examples/diamond.json` сохранён как сокращение для `summary`.

## Проверка

```bash
python scripts/validate_course.py
python -m unittest discover -s tests -v
mkdocs build --strict
```

Код опубликован под MIT, учебные материалы — под CC BY 4.0.
