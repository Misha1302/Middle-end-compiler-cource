# Статус курса

## Подтверждённая область

Версия 2 является самостоятельным курсом по middle-end foundations. Все 20 занятий проходят структурный педагогический validator: определения до задач, полная трасса, формальное правило, типичные ошибки, две задачи и локальные ответы.

## Реализованный учебный инструмент

Python-пакет содержит immutable CFG model и отдельные анализы dominators, IDom, DF и natural loop. Dominators и natural loop возвращают промежуточные состояния; CLI имеет human/JSON режимы.

## Явные границы

- Хавлак дан как проверяемая учебная трасса фаз; production implementation остаётся отдельной лабораторной.
- SCCP объяснён как расширение; обязательная часть занятия 9 использует simple propagation.
- MemorySSA, advanced alias analysis, register allocation и backend не входят в основной scope.

## Следующая версия

Отдельные лабораторные реализации: SSA construction/verifier, pass manager с invalidation, loop canonicalization/LCSSA и точный вариант Хавлака.
