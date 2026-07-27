# Банк задач на перенос

Эти задачи используются после исправления ошибки. Они не повторяют worked examples дословно.

## Блоки и CFG

1. Разбей `if p goto L1; x=1; goto L2; L1: x=2; L2: return x` на блоки и построй pred/succ.
2. Добавь недостижимый блок после `return` и докажи недостижимость обходом.

## Dominance и DF

1. Граф `A→B,C; B→D; C→D; D→E,F; E→D`: вычисли Dom/idom/DF.
2. Построй контрпуть к утверждению `B dom D`.

## SSA

1. Переведи в SSA ромб с двумя определениями `x` и use после join.
2. Переведи loop со счётчиком и accumulator, запиши stack trace только для accumulator.

## Оптимизации

1. Выполни propagation/cleanup для branch с известным false.
2. Классифицируй операции для DCE при разных effect contracts.
3. Выполни LVN через unknown call и объясни, какие memory facts потеряны.

## Циклы

1. Собери natural loop для двух latch blocks.
2. Найди SCC с двумя входами и докажи irreducibility.
3. Для `i+=2`, `j=3*i+1` выполни strength reduction.
4. Проверь LICM для invariant load при наличии store через возможно aliasing pointer.
5. Дай legality verdict для distribution с dependence distance 1.

## Стоп-правило

Пробел считается закрытым после двух новых задач подряд без исходной ошибки и с объяснением соответствующего инварианта.
