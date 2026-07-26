# Пробный зачёт — вариант 2

Незнакомый IR для проверки переноса после разбора первого варианта

| **Дополнительный вариант** | **Дополнительный вариант** | **Версия 3.0** |
|----------------------------|-------------------------|----------------|

| **Условия.** 150 минут. Без учебника и эталонов. После завершения разрешён разбор со мной. Контракт IR — из навигатора. |
|-------------------------------------------------------------------------------------------------------------------------|

## Теоретическая часть — 30 баллов

1.  Дай определение dominance frontier и объясни его связь с φ placement.

2.  Опиши renaming SSA, включая порядок φ, uses, definitions, successor inputs и pop.

3.  Чем data dependence отличается от control dependence и memory dependence?

4.  Почему branch simplification обычно выполняется до UCE и DCE?

5.  Назови условия безопасного LICM для арифметики, load и потенциально бросающей операции.

6.  Чем natural loop отличается от irreducible SCC?

## Практическая часть — 60 баллов

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>1: n = input()<br />
2: flag = input()<br />
3: i = 0<br />
4: sum = 0<br />
5: factor = 3 * n + 2<br />
Lh:<br />
6: if i &gt;= n goto Lexit<br />
7: repeated = 3 * n + 2<br />
8: if flag goto Lload else Lskip<br />
Lload:<br />
9: idx = 3 * i + 1<br />
10: value = load A[idx]<br />
11: sum = sum + value + repeated<br />
12: goto Lcont<br />
Lskip:<br />
13: unused = repeated - repeated<br />
Lcont:<br />
14: i = i + 1<br />
15: goto Lh<br />
Lexit:<br />
16: print sum<br />
17: return</th>
</tr>
</thead>
<tbody>
</tbody>
</table>

7.  Разбей linear IR на basic blocks и построй CFG с pred/succ/reachability.

8.  Вычисли Dom, idom, dominator tree и нужные DF.

9.  Построй SSA для \`i\`, \`sum\` и значений, которым требуется φ; проверь verifier invariants.

10. Выполни value numbering/constant simplification, UCE и DCE в обоснованном порядке.

11. Найди loop, basic/derived IV; выполни strength reduction для \`idx\`.

12. Определи, можно ли заменить \`repeated\` на \`factor\` и что можно вынести из loop.

13. Покажи финальный IR и список сделанных предположений.

## Рубрика — 100 баллов

| **Область**                 | **Баллы** | **Критерий**                                                  |
|-----------------------------|-----------|---------------------------------------------------------------|
| Разбиение и CFG             | 15        | blocks максимальны; pred/succ симметричны; reachability верна |
| Dominance/idom/DF           | 15        | таблицы и formal checks без пропусков                         |
| SSA construction            | 20        | φ placement, renaming, edge uses и verifier                   |
| Ациклические passes         | 20        | строгий порядок, legality и промежуточные IR                  |
| Loop analysis/optimizations | 20        | loop anatomy, IV, LICM/transform preconditions                |
| Финальная проверка          | 10        | effects, φ, CFG, dominance и объяснение ошибок                |

| **Порог.** 70 — минимально уверенная готовность; 85 — хорошая; 95 — устойчивое решение с полной проверкой legality. |
|---------------------------------------------------------------------------------------------------------------------|

## Краткий эталон для проверки после выполнения

- factor и repeated эквивалентны только при совпадающих типах/overflow semantics и invariant n.

- unused = repeated - repeated является чистым нулём и удаляется, если результат не используется.

- i и sum требуют loop-header φ; idx=3\*i+1 — derived IV, strength-reduced increment равен 3.

- load A\[idx\] остаётся внутри loop; arithmetic invariant expressions могут быть в preheader.

- Ветвление по invariant flag может открыть loop unswitching, но оно не входит в обязательный список — не применяй без запроса.
