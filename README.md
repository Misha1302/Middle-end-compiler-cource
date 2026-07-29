# Анализ и оптимизация программ в компиляторе

Самостоятельный русскоязычный курс о средней части компилятора (*middle-end*): от базовых блоков и CFG до SSA, ациклических оптимизаций и преобразований циклов.

## Что внутри

- 20 занятий по схеме «проблема → определения → модель → пошаговый разбор → правило → практика»;
- единый контракт учебного IR v1: нормализованные терминаторы, `i32`, память, эффекты и ошибки;
- словарь из 100 терминов с простыми и точными объяснениями;
- отдельные разделы с необходимыми предварительными понятиями: семантический анализ, DFS и SCC, каноническая форма цикла и межитерационные зависимости;
- полные эталоны комплексных работ с CFG, Dom, `idom`, DF и SSA;
- учебный инструмент на Python, который показывает не только итог анализа, но и промежуточные состояния;
- машинно проверяемые семантические эталоны ключевых графов.

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
python scripts/validate_content_contracts.py
python scripts/validate_golden_examples.py
python -m unittest discover -s tests -v
mkdocs build --strict
```

`validate_course.py` проверяет структуру, ссылки и редакторские ограничения. `validate_content_contracts.py` защищает исправленные содержательные контракты от регрессии. `validate_golden_examples.py` независимо пересчитывает достижимость, Dom, `idom` и DF для ключевых учебных графов.

Код опубликован под MIT, учебные материалы — под CC BY 4.0.
