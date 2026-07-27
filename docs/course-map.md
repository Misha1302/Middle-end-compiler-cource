# Карта курса и зависимости

| № | Тема | Обязательный вход | Наблюдаемый результат |
|---:|---|---|---|
| 1 | [Путь через компилятор](modules/01-pipeline-and-diagnostic.md) | базовое программирование | объяснены frontend/middle-end/backend и semantic analysis |
| 2 | [Лидеры и блоки](modules/02-leaders-and-basic-blocks.md) | линейный IR | разбиение на maximal basic blocks |
| 3 | [CFG](modules/03-building-cfg.md) | блоки/terminators | edges, pred/succ, reachability |
| 4 | [Dominance](modules/04-dominators.md) | CFG | полная fixed-point trace |
| 5 | [IDom и DF](modules/05-idom-tree-and-df.md) | Dom sets | отдельные CFG/dom-tree и DF trace |
| 6 | [SSA placement](modules/06-ssa-and-phi.md) | DF, binding/storage/value | iterated-DF worklist и φ contract |
| 7 | [SSA renaming](modules/07-ssa-renaming.md) | placement/dom tree | stack trace и verifier |
| 8 | [Def-use и LVN](modules/08-dependencies-and-lvn.md) | SSA/effects | dependence graph и VN table |
| 9 | [Константы](modules/09-constants.md) | def-use | simple propagation; SCCP отделён |
| 10 | [DCE/UCE](modules/10-dce-uce-and-pass-order.md) | effects/reachability | cleanup pipeline |
| 11 | [Inlining](modules/11-inlining.md) | CFG/SSA rewrite | clone/rename/return merge |
| 12 | [Комплексная №1](modules/12-checkpoint-1.md) | 1–11 | сквозной ациклический pipeline |
| 13 | [Loop anatomy](modules/13-loop-concepts.md) | DFS/SCC, dominance | natural/reducible/irreducible examples |
| 14 | [Хавлак](modules/14-havlak-and-loop-tree.md) | DFS/SCC/loops | pool/Union-Find trace |
| 15 | [IV](modules/15-induction-variables.md) | loop SSA | recurrence и strength reduction |
| 16 | [LICM](modules/16-licm.md) | canonical loop/effects | legality matrix и preheader repair |
| 17 | [Loop transformations](modules/17-loop-transformations.md) | loop-carried dependence | before/after + legality verdict |
| 18 | [Комплексная №2](modules/18-checkpoint-2.md) | 13–17 | полный loop pipeline |
| 19 | [Пробный зачёт](modules/19-mock-exam-1.md) | весь курс | независимая оценка |
| 20 | [Финальный ремонт](modules/20-final-repair.md) | журнал ошибок | два пробела закрыты transfer-задачами |

## Маршрут без скрытых зависимостей

Перед стартом прочитай [предпосылки](prerequisites.md). Если переход к следующей строке требует понятия, которого нет в обязательном материале предыдущих строк, это дефект курса.
