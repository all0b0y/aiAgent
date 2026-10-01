---
name: your-skill-name
description: <What it does, verbs first>. Use when <concrete situations and words the user says>; not for <nearest neighbour skill/case>.
---

<!--
Шаблон скилла (формат Agent Skills, agentskills.io).
- name: a-z, 0-9, дефисы; совпадает с именем папки.
- description: ≤1024 символов; ведущее слово в начале; одна ветка — один триггер.
- Тело: шаги с проверяемыми критериями сверху, справка ниже, ветвящееся — в references/.
- Детерминированная работа — в scripts/. Тело держи < 500 строк.
- Удали этот комментарий.
-->

# <Название>

<Одна строка: какой результат даёт скилл и почему процесс важен.>

## Steps

1. <Действие.>
   Done when: <проверяемое условие — агент может отличить «сделано» от «не сделано»>.
2. <Действие. Детерминированное — через скрипт:>
   `python ${CLAUDE_SKILL_DIR}/scripts/<script>.py <args>`
   Done when: <…>.
3. <Действие с ветвлением:> if <условие>, read `references/<topic>.md` first.
   Done when: <…>.
4. <Финальная проверка и отчёт: что сделано, как проверено, что осталось.>

## Rules

- <Правило в позитивной форме + почему.>
- <Жёсткое ограничение, которое нельзя сформулировать позитивно, + что делать вместо.>

## References

- `references/<topic>.md` — <когда читать>.
- `assets/<template>.md` — <для чего>.
