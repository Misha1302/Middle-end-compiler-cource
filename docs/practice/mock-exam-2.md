# Пробный зачёт — вариант 2

## Теория — 25 минут

1. Чем CFG отличается от dominator tree?
2. Сформулируй dominance frontier через predecessor-свидетель.
3. Почему φ edge-sensitive?
4. Когда `readonly` call нельзя считать pure?
5. Чем natural loop отличается от irreducible SCC?
6. Дай четыре проверки LICM.

## Практика — 90 минут

```text
p=input; n=input; i=0; s=0
head: if i>=n goto exit
if p goto add else skip
add: t=3*n+1; idx=4*i; v=load A[idx]; s=s+v+t; goto cont
skip: dead=i*0
cont: i=i+1; goto head
exit: print s
```

Построй blocks/CFG, Dom/idom/DF, SSA, затем выполни legal propagation/LVN/DCE и loop analysis. Для LICM и strength reduction укажи предпосылки.

<details>
<summary>Ключевые ориентиры</summary>

`i` и `s` требуют φ в header. При неизвестном `p` обе ветви достижимы. `dead` удаляется DCE. `t` loop-invariant и является кандидатом LICM при безопасной arithmetic semantics. `idx` — derived IV с step 4. Load не invariant из-за idx.

</details>
