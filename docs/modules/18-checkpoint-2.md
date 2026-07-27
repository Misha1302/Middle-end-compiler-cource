# Занятие 18. Комплексная работа №2

> SSA loop, IV, LICM и strength reduction с единым контрактом

[← Карта курса](../course-map.md) · [Предыдущее занятие](../modules/17-loop-transformations.md) · [Следующее занятие](../modules/19-mock-exam-1.md)

## Результат занятия

Ты проводишь полный loop pipeline и явно доказываешь legality каждого преобразования.

**Перед началом:** занятия 13–17.

## Зачем это вообще нужно

Loop passes зависят от корректных CFG/SSA и memory assumptions. Эта работа проверяет цепочку, а не отдельные определения.

## Термины до заданий

| Термин | Простое объяснение | Точная опора |
|---|---|---|
| **loop SSA** | SSA с φ для значений, переходящих между итерациями | initial input из preheader и updated input из latch |
| **legality** | доказательство сохранения поведения | предусловия transformation выполнены |
| **profitability** | ожидаемая практическая польза | не входит в доказательство корректности |
| **analysis invalidation** | старый результат анализа больше не соответствует IR | CFG rewrite обычно инвалидирует Dom/DF/loop info |
| **final verifier** | последняя механическая проверка | CFG, φ, dominance, defs, effects и use validity |

Сначала прочитай готовые объяснения. Затем закрой таблицу и сформулируй каждый термин своими словами. Пустая формулировка ученика — это проверка после обучения, а не замена обучения.

## Первая модель

`CFG/loop structure → SSA verifier → IV → invariant candidates → legality matrix → transformations → invalidated analyses → final verifier`

## Разобранный пример: состояние за состоянием

В контрольном режиме первые 120 минут работа выполняется без подсказок. Правило «запросить помощь через 10–15 минут» для этого занятия не действует; разбор начинается только после сохранения самостоятельной попытки.

## Формальное правило

Каждый pass получает проверенный IR, выдаёт новую версию, перечисляет сохранённые/инвалидированные analyses и проходит соответствующий verifier.

## Типичные ошибки

- Использовать общий шаблон помощи внутри контрольной части.
- Выполнить LICM до доказательства preheader/speculation.
- Strength-reduce expression без base case.
- Не пересчитать loop info после CFG rewrite.

## Задача A — по образцу

Для IR:

```text
n=input; i=0; s=0; k=4*n+1
head: if i>=n goto exit
t=4*n+1
idx=4*i+3
v=load A[idx]
s=s+v+t
i=i+1
goto head
exit: print s
```

Построй CFG, Dom/idom/DF, natural loop и SSA для `i,s`.

<details>
<summary>Проверка задачи A — открывать после попытки</summary>

Header содержит φ `i1=φ(pre:i0,latch:i2)` и `s1=φ(pre:s0,latch:s2)`. Latch обновляет i, body обновляет s. Natural loop включает header/body/latch, preheader с initial values снаружи.

</details>

## Задача B — перенос на новый пример

Докажи или отвергни: заменить `t` на `k`, вынести load, выполнить strength reduction `idx`, затем перечисли invalidated analyses.

<details>
<summary>Проверка задачи B — открывать после попытки</summary>

`t` и `k` эквивалентны при одинаковых типах/overflow flags; `t` можно заменить, затем удалить. Load нельзя вынести без invariant address и alias proof, а `idx` variant. Strength reduction: init 3, step 4. CFG неизменен для этих rewrites, но def-use/value facts меняются; создание preheader или CFG rewrite инвалидирует Dom/DF/loop info.

</details>

## Проверка на выходе

**Почему контрольная часть без помощи?**  


**Что invalidates Dom?**  


**Что проверяет final verifier?**  


<details>
<summary>Короткие ответы</summary>

**Почему контрольная часть без помощи?**  
Она измеряет самостоятельное воспроизведение; помощь переносится в последующий разбор.

**Что invalidates Dom?**  
Изменение CFG edges/blocks, способное изменить множество путей.

**Что проверяет final verifier?**  
Структуру CFG, φ-predecessor contract, unique defs, dominance uses и допустимость эффектов/operands.

</details>

## Профессиональная граница

Профильный компилятор хранит analysis preservation декларативно. В учебной работе достаточно явного ledger после каждого pass.
