# Эталоны и критерии проверки

Открывать после двух самостоятельных попыток или во время разбора со мной

| **Отдельный сборник** | **Для всех 20 дней** | **Версия 3.0** |
|-----------------------|----------------------|----------------|

| **Как пользоваться.** Сначала сравни не итог, а первый расходящийся шаг. Эталон может содержать один из нескольких допустимых вариантов, если условие оставляет выбор IR-контракта. |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Общие правила проверки

- Графы проверяются по вершинам, рёбрам и pred/succ symmetry, а не по расположению рисунка.

- SSA допускает разные имена, но не разные def-use/dominance/φ semantics.

- Minimal и pruned SSA могут различаться мёртвыми φ; выбранная форма должна быть названа.

- Оптимизация засчитывается только при указанной legality premise.

- При неоднозначности memory/overflow используй контракт навигатора и явно укажи допущение.

## Занятие 1. Диагностика и полный путь компиляции

### Задача A: Диагностика без подсказки

Эталонная карта: source → lexer/tokens → parser/AST → name/type/effect analysis → linear or structured IR → basic blocks/CFG → dominance/SSA/analyses → optimization passes → lowering/instruction selection → register allocation/scheduling → assembly/object file → linking → executable/shared objects → loader/runtime start. Для каждой границы должны быть названы вход, выход и одна гарантия. Для Wist2 как одного из возможных case studies допустимое сопоставление: Lexer → Parser → AST/Bytecode → AIR → optimizers → CIL compiler/interpreter. Точная граница SSA зависит от текущей архитектуры: после CFG-capable AIR и до SSA-based optimizations.

| **Проверить обязательно.** не менее 9 стадий • вход и выход каждой стадии • минимум 5 инвариантов |
|---------------------------------------------------------------------------------------------------|

### Задача B: Разбор своего проекта

Проверочная таблица выбранного проекта не имеет единственного текста; для Wist2 она, но обязана различать source binding, AST/Bytecode entity, AIR temporary и backend/runtime storage. Ошибка — объявить CIL backend частью frontend или считать interpreter стадией линковки.

| **Проверить обязательно.** таблица «классическая стадия → компонент выбранного проекта» • 2 возможные границы для SSA |
|----------------------------------------------------------------------------------------------------------|

### Задача C: Устный ответ

Четырёхминутный ответ засчитывается, если это причинная цепочка, а не перечень. Обязательны distinctions: compile vs assemble vs link vs load; why CFG/SSA; object vs executable.

| **Проверить обязательно.** связный рассказ • frontend/middle-end/backend • объектный файл, линкер, загрузчик |
|--------------------------------------------------------------------------------------------------------------|

## Занятие 2. Лидеры и базовые блоки

### Задача A: Разметка лидеров

Лидеры исходного примера: 1 (entry), 4 (инструкция после conditional branch), 6/Lneg (target), 7/Lend (target). Блоки: B0=1–3, B1=4–5, B2=6, B3=7–8. Терминаторы: conditional, goto, fall-through, return.

| **Проверить обязательно.** каждый лидер обоснован одним из правил • блоки максимальны • терминаторы последние |
|---------------------------------------------------------------------------------------------------------------|

### Задача B: Новый линейный фрагмент

Для нового фрагмента лидеры: 1, 3 (после conditional), 5/L1 (target), 7 (после conditional), 8/L2 (target). Блоки: B0=\[1,2\], B1=\[3,4\], B2=\[5,6\], B3=\[7\], B4=\[8\]. Терминаторы: B0 conditional; B1 goto; B2 conditional; B3 fall-through; B4 return.

| **Проверить обязательно.** не пропущен лидер после строки 6 • указан fall-through • каждая инструкция принадлежит одному блоку |
|--------------------------------------------------------------------------------------------------------------------------------|

### Задача C: Контрпримеры

Неверное объединение: поместить 2 и 3 в один блок после conditional — тогда управление может покинуть последовательность до выполнения 3. Неверное дробление: \[1\] и \[2\] отдельно при отсутствии метки/перехода между ними — нарушена максимальность, хотя граф остаётся семантически эквивалентным.

| **Проверить обязательно.** 2 контрпримера • назван нарушенный инвариант |
|-------------------------------------------------------------------------|

## Занятие 3. Построение CFG и проверка достижимости

### Задача A: CFG с таблицей рёбер

Для приведённого фрагмента блоки: B0=\[1,2\], B1=\[3,4\], B2=\[5,6\], B3=\[7\], B4=\[8\]. Рёбра: B0→B2 (p), B0→B1 (!p); B1→B4; B2→B4 (q), B2→B3 (!q); B3→B4. pred: B0={}, B1={B0}, B2={B0}, B3={B2}, B4={B1,B2,B3}.

| **Проверить обязательно.** все переходы отражены • fall-through подписан • pred/succ симметричны |
|--------------------------------------------------------------------------------------------------|

### Задача B: Достижимость

Блок Dead, не являющийся target и расположенный после безусловного goto, не посещается обходом от entry и поэтому unreachable. Текстовое расположение не создаёт ребро после unconditional terminator.

| **Проверить обязательно.** порядок обхода • множество visited • вывод основан на пути |
|---------------------------------------------------------------------------------------|

### Задача C: Обратное восстановление

Тот же CFG допускает разные линейные порядки блоков, если терминаторы скорректированы явными goto/fall-through. Например, B2 можно разместить перед B1; граф задаётся рёбрами, а не порядком печати.

| **Проверить обязательно.** терминатор каждого блока • минимум 2 линейных порядка |
|----------------------------------------------------------------------------------|

## Занятие 4. Доминирование: смысл и вычисление

### Задача A: Таблица итераций

Для B0→B1,B2; B1,B2→B3; B3→B4: Dom0(B0)={B0}; остальные сначала {B0,B1,B2,B3,B4}. После первого прохода: Dom(B1)={B0,B1}, Dom(B2)={B0,B2}, Dom(B3)={B0,B3}, Dom(B4)={B0,B3,B4}. Следующий проход не меняет множества.

| **Проверить обязательно.** инициализация • минимум один полный проход • явно отмечена неподвижная точка |
|---------------------------------------------------------------------------------------------------------|

### Задача B: Проверка через пути

B0 dom B4 — да, все пути начинаются в B0. B1 dom B3 — нет, путь B0→B2→B3. B3 dom B4 — да, единственный predecessor B4 — B3.

| **Проверить обязательно.** для ложного утверждения дан путь • для истинного рассмотрены все варианты |
|------------------------------------------------------------------------------------------------------|

### Задача C: Граф с циклом

После добавления B4→B3 множества остаются: Dom(B3)={B0,B3}, Dom(B4)={B0,B3,B4}. B4 не доминирует B3, потому что путь B0→B1→B3 или B0→B2→B3 достигает B3 до B4.

| **Проверить обязательно.** новая таблица • объяснение через первый вход в цикл |
|--------------------------------------------------------------------------------|

## Занятие 5. Непосредственные доминаторы, дерево и фронт доминирования

### Задача A: Построение дерева

Для простого ромба idom(B1)=B0, idom(B2)=B0, idom(B3)=B0, idom(B4)=B3. Дерево: B0 children B1,B2,B3; B3 child B4.

| **Проверить обязательно.** один idom у каждого блока кроме entry • предки дерева совпадают со строгими доминаторами |
|---------------------------------------------------------------------------------------------------------------------|

### Задача B: Фронты

Для CFG B0→B1,B2; B1,B2→B3; B3→B4,B5; B4→B3: idom(B1)=B0, idom(B2)=B0, idom(B3)=B0, idom(B4)=B3, idom(B5)=B3. Ненулевые DF: DF(B1)={B3}, DF(B2)={B3}, DF(B3)={B3} из-за back edge через B4, DF(B4)={B3}; DF(B0)=DF(B5)=∅. Формальную проверку делай по predecessor B1/B2/B4 блока B3.

| **Проверить обязательно.** указан доминируемый predecessor • проверено отсутствие строгого доминирования самой вершины |
|------------------------------------------------------------------------------------------------------------------------|

### Задача C: Подготовка к SSA

Definitions x в B1 и B2 дают φ в B3. Если definition также в B4, DF(B4) также содержит B3, но это не создаёт новый блок сверх B3; B3 как φ-definition имеет DF(B3)={B3}, closure стабильна.

| **Проверить обязательно.** рабочее множество • точки φ до неподвижной точки |
|-----------------------------------------------------------------------------|

## Занятие 6. SSA: определения значений и расстановка φ-функций

### Задача A: Разделение сущностей

Примеры сущностей: source binding y в AST scope; runtime local/storage — слот локальной переменной или адрес; AIR temporary — результат конкретной AIR instruction; SSA value y3 — результат одного definition. Нельзя объединять: разные lifetimes, identity rules и verifier contracts.

| **Проверить обязательно.** 4 сущности • разные жизненные циклы • риск смешения |
|--------------------------------------------------------------------------------|

### Задача B: Расстановка φ

Для указанного CFG φ для a требуется в B3: туда сходятся definitions B1/B4 и путь от B0/B2; B3 также может попасть в собственный DF из-за back edge, но одна φ уже вставлена. Использования в B5 получают значение, выходящее из B3. Точный ответ подтверждается таблицей DF из дня 5.

| **Проверить обязательно.** worklist • итерации DF • φ в начале блоков |
|-----------------------------------------------------------------------|

### Задача C: Проверка φ-контракта

Для каждой φ B3 predecessors={B1,B2,B4}, значит нужны три подписанных incoming values. После добавления нового predecessor B6 verifier должен отклонить φ без входа \[B6:…\]; после удаления predecessor соответствующий incoming обязан исчезнуть.

| **Проверить обязательно.** один вход на predecessor • подписанные операнды • ошибка verifier при несоответствии |
|-----------------------------------------------------------------------------------------------------------------|

## Занятие 7. SSA: переименование и проверка корректности

### Задача A: Трасса стеков

Ромб после renaming: B0 x0=input; branch. B1 y1=x0+1. B2 y2=1-x0. B3 y3=phi\[B1:y1,B2:y2\]; print y3. Стек x: push x0 в B0 и pop после всего subtree; stack y: push y1 только в B1, заполнить B3 incoming и pop; аналогично y2; в B3 сначала push y3, затем print, затем pop.

| **Проверить обязательно.** φ-def обрабатывается первым • uses читают вершину • после ветви выполнен pop |
|---------------------------------------------------------------------------------------------------------|

### Задача B: SSA цикла

Цикл: pre: i0=0; sum0=0; goto head. head: i1=phi\[pre:i0,latch:i2\]; sum1=phi\[pre:sum0,latch:sum2\]; if i1\>=n goto exit else body. body/latch: v1=load a\[i1\]; sum2=sum1+v1; i2=i1+1; goto head. exit: return sum1.

| **Проверить обязательно.** φ для i и sum • одно определение на имя • обратные входы из latch |
|----------------------------------------------------------------------------------------------|

### Задача C: Ручной verifier

Verifier table обязана показать defs x0/y1/y2/y3 и uses; x0 определён в B0 и доминирует B1/B2; y1/y2 используются на edges B1→B3/B2→B3; y3 определён в B3 и используется там после φ.

| **Проверить обязательно.** все values перечислены • φ uses проверены на ребре |
|-------------------------------------------------------------------------------|

## Занятие 8. Граф зависимостей и локальная нумерация значений

### Задача A: Граф зависимостей

Data edges: a→t1,t2; b→t1,t2; t1→t3; t2→t4; constant 2→t3,t4; t3,t4→print. CFG edges отсутствуют внутри одного блока как отдельный dependency type.

| **Проверить обязательно.** узел на каждое определение • 2 входа у бинарной операции • не смешаны control/data edges |
|---------------------------------------------------------------------------------------------------------------------|

### Задача B: Таблица LVN

Один допустимый LVN trace: VN(a)=1,VN(b)=2; a+b key add(1,2)→3; b+a canonical add(1,2)→reuse 3; a-b sub(1,2)→4; повтор a+b→3; 2\*(a+b) mul(VN2const,3)→5. Повторные results заменяются canonical representative.

| **Проверить обязательно.** канонизация только для коммутативных • копии/повторы заменены • типы учтены |
|--------------------------------------------------------------------------------------------------------|

### Задача C: Эффекты

Без effect summary unknown call может читать/писать память, поэтому второй load p нельзя заменить первым. При доказанной pure функции, не меняющей память и не бросающей наблюдаемое исключение, load equivalence всё ещё требует отсутствия иных aliasing stores и одинаковой memory version.

| **Проверить обязательно.** консервативный вариант • условия безопасного объединения |
|-------------------------------------------------------------------------------------|

## Занятие 9. Свёртка и глобальное распространение констант в SSA

### Задача A: Lattice trace

Entry executable; c0=constant(1); comparison true; executable edge только B0→B1. x1=constant(5); B1→B3 executable. Edge B2→B3 не executable, x2 не влияет на φ. x3=constant(5), y1=constant(7). После fixed point branch becomes goto B1.

| **Проверить обязательно.** unknown/constant/overdefined • учтена достижимость входов φ • показана очередь изменений |
|---------------------------------------------------------------------------------------------------------------------|

### Задача B: Циклический пример

i=phi(0,i+1): после открытия back edge второй input зависит от i и принимает отличающиеся значения, поэтому result переходит в overdefined; нулевая initial value не делает все итерации нулевыми.

| **Проверить обязательно.** обратный вход • переход к overdefined • нет ошибочного бесконечного folding |
|--------------------------------------------------------------------------------------------------------|

### Задача C: Собственный тест

Пример: branch true в B0 на B1/B2; B1 x1=3; B2 x2=4; B3 x3=phi. До edge facts inputs различны; после доказательства B2 unreachable φ имеет только x1 и становится 3.

| **Проверить обязательно.** две ветви • доказанное условие • итоговая константа |
|--------------------------------------------------------------------------------|

## Занятие 10. Удаление мёртвого и недостижимого кода

### Задача A: Классификация

Классификация по контракту: unused pure add — удалить; ordinary load — удалить только если гарантировано non-trapping/non-volatile; volatile load — нельзя; store — нельзя; pure call — можно при no-throw; unknown call — нельзя; division — только при proof nonzero и отсутствии observable trap/flags.

| **Проверить обязательно.** эффект/исключение отдельно • нет безусловочного удаления unknown call |
|--------------------------------------------------------------------------------------------------|

### Задача B: Полный цикл очистки

После branch simplification B0 goto B1. UCE удаляет B2. В B3 φ loses B2 input and becomes x1; заменить x3→x1. Fold y1=5+2→7. DCE удаляет c0/comparison/лишние copies, если они больше не нужны; финально B0 goto B1; B1 goto B3; B3 print 7.

| **Проверить обязательно.** отдельная версия после каждого pass • pred/succ обновлены • φ упрощена |
|---------------------------------------------------------------------------------------------------|

### Задача C: Mark-sweep

Mark roots: return/print/store/unknown call. Worklist идёт от их operands к defining instructions. Один use-count=0 удаляет только текущий leaf; после удаления его operands могут стать zero-use, поэтому нужен worklist/fixed point или mark-sweep.

| **Проверить обязательно.** worklist живых defs • каскадная мёртвость |
|----------------------------------------------------------------------|

## Занятие 11. Inlining: подстановка тела функции

### Задача A: Механическая подстановка

После split caller: CallPre x0=input; branch to cloned Entry. Clone has P/N blocks with fresh r1c/r2c. Both return blocks goto Cont. Cont: y0=phi\[P:r1c,N:r2c\]; z0=y0\*2. Parameters a заменены x0. CFG/dominance пересчитываются.

| **Проверить обязательно.** fresh block/value names • аргумент сопоставлен параметру • оба return сведены |
|----------------------------------------------------------------------------------------------------------|

### Задача B: Оптимизация после inline

При argument 3 condition true, N unreachable; φ collapses to r1c=4; z0=8. После UCE/DCE остаётся прямой вычислительный путь; возможно constant fold всего результата.

| **Проверить обязательно.** известное условие • удалённая ветвь • итоговое выражение |
|-------------------------------------------------------------------------------------|

### Задача C: Решение об inline

Getter — обычно выгоден; большая функция в hot loop — потенциально выгодна, но code-size/cache risk; recursive — требует depth/budget and usually limited; pure helper с constant arg — сильный кандидат из-за propagation. Это profitability judgments, не универсальные истины.

| **Проверить обязательно.** legality отдельно от profitability • кодовый размер • контекст вызова |
|--------------------------------------------------------------------------------------------------|

## Занятие 12. Комплексная работа №1

### Задача A: Часть A — графы

Один корректный CFG: B0=1–3, B1=4–6, B2=7–8, B3=9–10, B4=11–12, Bdead=13–14. Edges B0→B1/B2; B1,B2→B3; B3→B4 (false branch target Bdead never executable semantically, но CFG до propagation содержит B3→Bdead и B3→B4); Bdead terminal. Reachability до constant analysis включает Bdead структурно.

| **Проверить обязательно.** leaders обоснованы • pred/succ • таблица Dom до стабилизации • DF |
|----------------------------------------------------------------------------------------------|

### Задача B: Часть B — SSA

SSA: x0=2 in B0, x1=a+2 in B1, x2=2 in B2, x3=phi\[B1:x1,B2:x2\] in B3. t1=x1\*4, t2=x2\*4, t3=phi\[B1:t1,B2:t2\] if later use in Bdead retained; q1=x3\*4. Exact dead φ placement depends on pruned vs minimal SSA; state your convention.

| **Проверить обязательно.** подписанные φ-входы • одно определение • dominance checks |
|--------------------------------------------------------------------------------------|

### Задача C: Часть C — оптимизации

Optimization: false branch removes Bdead via UCE; t and its φ become dead and are removed. LVN can identify q1 with branch-local t values only after suitable global reasoning; local VN alone cannot cross blocks. Final print is x3\*4; when a≤0 x3=2. Rubric: graphs 25, dominance/DF 20, SSA 25, passes 25, verification 5.

| **Проверить обязательно.** не перепрыгнуты состояния • эффекты сохранены • итоговый print корректен |
|-----------------------------------------------------------------------------------------------------|

## Занятие 13. Циклы в CFG: естественные, сводимые и несводимые

### Задача A: Анатомия цикла

Diagram labels: head=header; latch source of latch→head back edge; body and latch inside; pre outside with sole edge to head; head→exit is exit edge, exit target is exit block. If multiple outside predecessors, split their edges through new preheader.

| **Проверить обязательно.** внешние predecessors перенаправлены • семантика входа сохранена |
|--------------------------------------------------------------------------------------------|

### Задача B: Natural loop

CFG A→B; B→C,D; C→E; E→B; D→X. B dominates C,E, so E→B is back edge. Start set {B,E}; add predecessors of E: C; predecessors of C: B; stop. Natural loop={B,C,E}.

| **Проверить обязательно.** доказано B dom E • worklist обратного сбора • тело цикла |
|-------------------------------------------------------------------------------------|

### Задача C: Несводимый регион

SCC with entries E→A and E→B has mutual reachability inside, but neither A nor B necessarily dominates the other and there is no single header dominating all region nodes. Это irreducible multi-entry region.

| **Проверить обязательно.** два входа • dominance-контрпример • SCC ≠ natural loop |
|-----------------------------------------------------------------------------------|

## Занятие 14. Алгоритм Хавлака и дерево циклов

### Задача A: Карточки фаз

Правильный порядок карточек: DFS → predecessor classification → reverse DFS headers → initial pool/worklist → expansion via non-back predecessors → irreducibility check → union/collapse → parent relation. В учебной разбивке последние две карточки могут быть объединены.

| **Проверить обязательно.** для каждой фазы указан вход/выход • понятна причина следующей фазы |
|-----------------------------------------------------------------------------------------------|

### Задача B: Вложенный пример

Во вложенном примере DFS должен открыть outer header, затем inner region. Reverse order сначала обработает inner_head, свернёт inner_body/inner_latch under it, затем outer_head увидит representative inner loop как часть внешнего region. Loop tree: outer loop parent inner loop.

| **Проверить обязательно.** DFS numbers • два loop descriptors • parent-child |
|------------------------------------------------------------------------------|

### Задача C: Несводимость

Для multi-entry SCC при рассмотрении одного candidate header expansion встретит representative узла, достижимого через второй внешний вход и не являющегося DFS-descendant header; именно проверка descendant/ancestry классифицирует irreducible. Конкретный node зависит от DFS ordering, что нужно показать в трассе.

| **Проверить обязательно.** конкретный non-back predecessor • проверка dominance • маркировка irreducible |
|----------------------------------------------------------------------------------------------------------|

## Занятие 15. Индуктивные переменные и strength reduction

### Задача A: Классификация

i=i+1 basic IV. j=2\*i+5 derived IV if coefficients invariant. k=k+j не basic fixed-step и не доказанная affine IV без дополнительного анализа. m=load p not IV. n=n+c basic IV if c loop-invariant and update occurs once per iteration on all back paths.

| **Проверить обязательно.** init • step invariant • зависимости |
|----------------------------------------------------------------|

### Задача B: Closed form

For i0=0, step=1: i=0,1,2,3; j=3,7,11,15; closed forms i(k)=k, j(k)=4k+3.

| **Проверить обязательно.** таблица k=0..3 • формула • согласованность |
|-----------------------------------------------------------------------|

### Задача C: Strength reduction в SSA

Strength reduced: pre j0=3. head j1=phi\[pre:j0,latch:j2\]. use a\[j1\]. latch j2=j1+4. i may be removed only if loop condition and all uses can be expressed without it, e.g. a separate trip counter or j bound preserving semantics.

| **Проверить обязательно.** правильный j_init • j_step=4 • анализ uses i |
|-------------------------------------------------------------------------|

## Занятие 16. Вынос инвариантного кода из цикла

### Задача A: Кандидаты и причины

t1=a+b invariant, pure, speculatable under mathematical arithmetic, safe. t2=t1\*4 becomes invariant after t1 and is safe. x=load arr\[i\]+t2 not invariant because address depends on i. Matrix must distinguish invariant from hoist legality.

| **Проверить обязательно.** четыре отдельных свойства • не смешана инвариантность и safety |
|-------------------------------------------------------------------------------------------|

### Задача B: Создание preheader

With outside predecessors P1,P2 to H, insert Pre: P1→Pre, P2→Pre, Pre→H. If H φ had incoming \[P1:v1,P2:v2,L:vL\], create vpre=phi\[P1:v1,P2:v2\] in Pre and replace external H inputs with \[Pre:vpre\], keeping \[L:vL\].

| **Проверить обязательно.** внешние рёбра объединены • внутренний back edge сохранён • φ корректна |
|---------------------------------------------------------------------------------------------------|

### Задача C: Опасный пример

if(flag) 10/x: before hoist division is skipped when flag false; after hoist it executes and may trap at x=0. Safe if x proven nonzero and division otherwise speculatable, or if control guarantees flag true on every loop entry/path where preheader executes.

| **Проверить обязательно.** нулевое число итераций/false flag • деление на ноль • доказанное nonzero или guaranteed execution |
|------------------------------------------------------------------------------------------------------------------------------|

## Занятие 17. Unrolling, peeling, splitting, distribution и fusion

### Задача A: Пять карточек «до/после»

Expected sketches: unroll duplicates body with adjusted IV and remainder; peeling executes first iteration separately; splitting creates ranges \[0,k),\[k,n); distribution creates two loops over same range; fusion combines adjacent same-bound loops. Each sketch must preserve order/effects.

| **Проверить обязательно.** 5 преобразований • видна новая структура итераций |
|------------------------------------------------------------------------------|

### Задача B: Dependence reasoning

For a\[i\]=...; c\[i\]=a\[i-1\], distribution order matters. If producer loop for all a runs before consumer loop for all c, dependence from iteration i-1 to i is preserved and may be legal; reversing loops is not. Boundary i=0 must be defined. This is not a blanket “cannot split”.

| **Проверить обязательно.** distance dependence • порядок итераций • вердикт с условием |
|----------------------------------------------------------------------------------------|

### Задача C: Выбор оптимизации

Fixed short trip count→unroll; special first iteration→peeling; independent statements with different vectorizability→distribution; adjacent compatible loops→fusion. Each answer must mention code size, dependence, locality or register-pressure risk.

| **Проверить обязательно.** выгода • предусловие • риск |
|--------------------------------------------------------|

## Занятие 18. Комплексная работа №2

### Задача A: Структура и SSA

Blocks: pre instructions 1–4 then goto/flow H; H test; body 6–10; latch 10–11 can be same block depending terminator; exit 12–13. Natural loop H/body/latch. SSA: i1=phi\[pre:i0,latch:i2\], s1=phi\[pre:s0,latch:s2\]; body computes s2; latch i2.

| **Проверить обязательно.** header/latch/preheader/exits • φ с подписанными входами • verifier |
|-----------------------------------------------------------------------------------------------|

### Задача B: Ациклические оптимизации

k and t have syntactically same pure expression with invariant n. GVN can replace t by k if types and arithmetic flags/overflow semantics match. DCE then removes t. Plain local VN alone cannot cross preheader/body.

| **Проверить обязательно.** эквивалентность выражений • семантические флаги • удаление мёртвого def |
|----------------------------------------------------------------------------------------------------|

### Задача C: Цикловые оптимизации

idx derived IV: idx0=3; idx1=phi\[pre:idx0,latch:idx2\]; idx2=idx1+4. Expression 4\*n+1 is invariant and already k in preheader. load A\[idx1\] changes address each iteration and cannot be LICM-hoisted. Final SSA must keep load and accumulation in loop.

| **Проверить обязательно.** basic/derived IV • preheader init • latch update • LICM legality |
|---------------------------------------------------------------------------------------------|

## Занятие 19. Пробный зачёт

### Задача A: Теоретическая часть

Theory answer is graded by definition/purpose/example/error, not verbatim wording. Minimum topics: compiler pipeline, CFG, dominance/DF, SSA construction, dependency/VN, cleanup passes, loop/LICM legality.

| **Проверить обязательно.** точное определение • назначение • мини-пример/ошибка |
|---------------------------------------------------------------------------------|

### Задача B: Практическая часть

Practical solution must include every artifact named in the local rubric. Exact optimized IR depends on stated memory/overflow assumptions; contract defaults apply. Critical expected optimizations: q equals base under matching semantics; dead=q\*0 is dead in skip branch; idx is derived IV; invariant q/base candidate; load remains variant; acc and i require φ.

| **Проверить обязательно.** все промежуточные версии • legality пояснения • итоговый verifier |
|----------------------------------------------------------------------------------------------|

### Задача C: Самопроверка и оценка

Use the local 100-point rubric. Three repair items must be concrete: e.g. “φ missing incoming from latch” → new loop SSA example; not “повторить SSA”.

| **Проверить обязательно.** балл • 3 критических пробела • план ремонта |
|------------------------------------------------------------------------|

## Занятие 20. Финальный ремонт и компактная карта зачёта

### Задача A: Ремонт пробела №1

Repair answer is individual. Valid submission names the old error, violated invariant, corrected rule, new unseen example and evidence that error did not repeat.

| **Проверить обязательно.** правило своими словами • новый пример • отсутствие старой ошибки |
|---------------------------------------------------------------------------------------------|

### Задача B: Ремонт пробела №2

Second repair follows same contract; if it is legality, include a counterexample; if algorithmic, include state trace and stop condition.

| **Проверить обязательно.** перенос на новый контекст • проверяемый артефакт |
|-----------------------------------------------------------------------------|

### Задача C: Финальный retrieval

Final retrieval should contain the exact pipeline and at least 15 precise definitions. Any answer taking \>15 seconds enters the spaced-repetition queue for the next morning.

| **Проверить обязательно.** полный pipeline • 15 определений • список задержек |
|-------------------------------------------------------------------------------|
