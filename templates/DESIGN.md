---
version: alpha
name: Field Notes
description: Пример DESIGN.md — спокойный «рабочий блокнот» для продуктивного приложения. Замени значения на свои.
colors:
  ink: "#1B1D1F"
  graphite: "#5E646B"
  paper: "#F6F3EE"
  surface: "#FFFFFF"
  rule: "#E3DED6"
  primary: "#C2410C"
  on-primary: "#FFFFFF"
  ok: "#2F6B3F"
  danger: "#B42318"
typography:
  display:
    fontFamily: Fraunces
    fontSize: 2.75rem
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  h2:
    fontFamily: Fraunces
    fontSize: 1.5rem
    fontWeight: 600
    lineHeight: 1.25
  body:
    fontFamily: IBM Plex Sans
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: IBM Plex Mono
    fontSize: 0.75rem
    fontWeight: 500
    letterSpacing: 0.04em
rounded:
  sm: 4px
  md: 8px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
    padding: 10px 16px
  button-primary-hover:
    backgroundColor: "#9A3412"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: 24px
  page:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
  caption:
    textColor: "{colors.graphite}"
    typography: "{typography.label}"
  divider:
    backgroundColor: "{colors.rule}"
    height: 1px
  badge-ok:
    backgroundColor: "{colors.ok}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
  badge-danger:
    backgroundColor: "{colors.danger}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
---

## Overview

Тихий рабочий инструмент, похожий на хороший бумажный блокнот: тёплая бумага, плотные чернила, один акцентный цвет. Интерфейс отступает на второй план и выпускает вперёд содержимое пользователя. Плотность — средняя: это ежедневный инструмент, а не лендинг.

## Colors

- **Ink (#1B1D1F)** — основной текст и заголовки.
- **Graphite (#5E646B)** — вторичный текст, подписи, метаданные. Не используется на цветном фоне.
- **Paper (#F6F3EE)** — фон приложения. Теплее белого, снижает утомление.
- **Surface (#FFFFFF)** — карточки и поля ввода поверх paper.
- **Rule (#E3DED6)** — разделители и границы вместо теней.
- **Primary (#C2410C)** — единственный акцент: главное действие на экране и фокус. Не более одного акцентного элемента в видимой области.
- **Ok / Danger** — только для статусов, никогда для декора.

## Typography

Fraunces (засечки, характер) — только заголовки. IBM Plex Sans — весь интерфейс и текст. IBM Plex Mono — метки, даты, числа в таблицах (табличные цифры). Масштаб ограничен четырьмя стилями из токенов; новый размер = сначала обсудить.

## Layout

Сетка 8 px. Колонка текста не шире 68 знаков. Боковая панель 264 px, основная зона — гибкая. Отступы между секциями `xl`, внутри карточек `lg`. На мобильных — одна колонка, навигация снизу.

## Elevation & Depth

Глубина передаётся границами `rule` и сменой фона paper → surface. Тени только у всплывающих слоёв (меню, диалоги): `0 8px 24px rgba(27,29,31,.12)`.

## Shapes

Небольшие радиусы: `sm` для кнопок и полей, `md` для карточек. Без «таблеток» и полностью круглых кнопок, кроме аватаров.

## Components

- **Кнопка primary** — фон primary, одна на экран. Secondary — прозрачная с границей rule. Tertiary — текстовая ссылка.
- **Карточка** — surface, граница rule, радиус md, без тени. Карточки не вкладываются друг в друга.
- **Поле ввода** — surface, граница rule, фокус — обводка primary 2 px.
- **Пустое состояние** — одна строка объяснения + одно действие. Без иллюстраций-заглушек.

## Do's and Don'ts

- Do: одна главная мысль и одно главное действие на экран.
- Do: состояния загрузки, пустые состояния и ошибки проектируются вместе с основным экраном.
- Do: контраст текста не ниже WCAG AA (4.5:1).
- Don't: градиенты, свечения, стеклянные панели.
- Don't: иконка в цветном квадрате над каждым заголовком.
- Don't: серый текст на цветном фоне.
- Don't: Inter, Roboto, системный шрифт как основной.
