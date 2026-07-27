# Занятие 15. Индуктивные переменные и strength reduction

> Предсказуемые recurrence вместо повторного дорогого выражения

[← Карта курса](../course-map.md) · [Предыдущее занятие](../modules/14-havlak-and-loop-tree.md) · [Следующее занятие](../modules/16-licm.md)

## Результат занятия

Ты распознаёшь basic/derived IV, выводишь первые значения и выполняешь strength reduction.

**Перед началом:** SSA loop, header, latch и preheader.

## Зачем это вообще нужно

Некоторые значения меняются по простой формуле каждую итерацию. Это позволяет заменить повторное умножение постоянным сложением.

## Термины до заданий

| Термин | Простое объяснение | Точная опора |
|---|---|---|
| **basic IV** | базовая индуктивная переменная | `i_next=i+step`, где init/step loop-invariant |
| **derived IV** | линейная функция basic IV | `j=a*i+b` при invariant a,b |
| **recurrence** | правило перехода к следующему значению | описывает init и update |
| **closed form** | формула значения на итерации k | например `i(k)=init+k*step` |
| **strength reduction** | замена дорогой операции дешёвым обновлением | создаёт собственную recurrence для derived IV |

Сначала прочитай готовые объяснения. Затем закрой таблицу и сформулируй каждый термин своими словами. Пустая формулировка ученика — это проверка после обучения, а не замена обучения.

## Первая модель

`i(k)=i0+k`; `j(k)=4*i(k)+3`; следовательно `j(k+1)=j(k)+4`.

## Разобранный пример: состояние за состоянием

| k | i(k) | j(k)=4i+3 | recurrence j |
|---|---:|---:|---:|
| 0 | 0 | 3 | init 3 |
| 1 | 1 | 7 | 3+4 |
| 2 | 2 | 11 | 7+4 |
| 3 | 3 | 15 | 11+4 |

SSA после strength reduction добавляет `j0=3` в preheader, φ для j в header и `j2=j1+4` в latch.

## Формальное правило

Basic IV имеет invariant init и step. Derived `a*i+b` получает step `a*step_i`. Преобразование обязано сохранить base case, один inductive step и overflow semantics.

## Типичные ошибки

- Называть любую меняющуюся переменную IV.
- Не проверять invariant step.
- Вычислять неверный initial value derived IV.
- Игнорировать overflow/тип.

## Задача A — по образцу

Классифицируй `i=i+1`, `j=2*i+5`, `k=k+j`, `m=load p`, `n=n+c` с явными предпосылками.

<details>
<summary>Проверка задачи A — открывать после попытки</summary>

`i` basic IV. `j` derived от i. `k` не доказана affine IV без дополнительного анализа j/recurrence. `m` не IV. `n` basic только если c loop-invariant и update выполняется на каждом latch-пути.

</details>

## Задача B — перенос на новый пример

Для init `i0=2`, step `3`, `j=5*i-1` найди closed forms и strength-reduced update.

<details>
<summary>Проверка задачи B — открывать после попытки</summary>

`i(k)=2+3k`; `j(0)=9`; `j(k)=9+15k`; update `j_next=j+15`.

</details>

## Проверка на выходе

**Что делает IV базовой?**  


**Как найти step derived IV?**  


**Что проверять после strength reduction?**  


<details>
<summary>Короткие ответы</summary>

**Что делает IV базовой?**  
Invariant init и регулярное обновление на invariant step.

**Как найти step derived IV?**  
Умножить коэффициент при basic IV на её step.

**Что проверять после strength reduction?**  
Initial value, один inductive step, uses и точную числовую семантику.

</details>

## Профессиональная граница

Scalar Evolution обобщает recurrence далеко за линейные IV. Для курса достаточно affine случаев с явными предпосылками.
