# Middle-end Compiler Course

Практический русскоязычный курс по устройству **middle-end компилятора**: от базовых блоков и CFG до SSA, ациклических оптимизаций и преобразований циклов.

## Что внутри

- 20 последовательных занятий с причинной моделью, разобранным примером и задачами A/B/C;
- единый контракт учебного IR;
- комплексные работы и два варианта пробного зачёта;
- эталоны, критерии проверки, словарь и карточки;
- небольшой Python-инструментарий для экспериментов с CFG, dominators, IDom, DF и natural loops;

## Быстрый старт

1. Откройте [онлайн-версию курса](https://misha1302.github.io/Middle-end-compiler-cource/) или [страницу курса в репозитории](docs/index.md).
2. Прочитайте [правила прохождения](docs/getting-started.md).
3. Зафиксируйте [контракт учебного IR](docs/ir-contract.md).
4. Начните с [занятия 1](docs/modules/01-pipeline-and-diagnostic.md).

Локальный сайт:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements-docs.txt
mkdocs serve
```

Инструмент для анализа CFG:

```bash
python -m middle_end_course.cli examples/diamond.json
```

Для запуска без установки пакета:

```bash
PYTHONPATH=src python -m middle_end_course.cli examples/diamond.json
```

Проверка репозитория:

```bash
python scripts/validate_course.py
python -m unittest discover -s tests -v
```

## Границы

Это курс по **middle-end**, а не полный курс по разработке компилятора с нуля. Lexer, parser, type checker, instruction selection и register allocation обозначены в общей архитектуре, но не являются основными темами. Раздел про Хавлака пока использует учебную схему и явно помечен как такой.

## Правовой статус

Код опубликован под MIT, а учебные материалы — под CC BY 4.0. Подробности — в [LICENSE](LICENSE) и [NOTICE.md](NOTICE.md).
