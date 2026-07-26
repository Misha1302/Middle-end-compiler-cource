# Middle-end Compiler Course

Этот курс учит не запоминать названия проходов, а **доказывать корректность анализов и преобразований через инварианты**.

К концу курса вы сможете:

- строить basic blocks и CFG;
- вычислять dominators, IDom, dominator tree и dominance frontier;
- расставлять φ-функции и выполнять SSA-renaming;
- рассуждать о def-use зависимостях, LVN, constant propagation, DCE/UCE и inlining;
- находить natural loops и различать reducible/irreducible CFG;
- анализировать legality LICM, strength reduction и основных loop transformations;
- объяснять, какие анализы инвалидируются после изменения CFG или SSA.

## Начало

- [Как проходить курс](getting-started.md)
- [Карта из 20 занятий](course-map.md)
- [Единый контракт учебного IR](ir-contract.md)
- [Занятие 1](modules/01-pipeline-and-diagnostic.md)

## Печатные материалы

В каталоге `printable/` находятся обязательный маршрут, карточки и словарь. Основной, обновляемый источник курса — Markdown в `docs/`.
