> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本法router

**状態:** DRAFT — qualified Japanese counsel review pending
**一次資料確認日:** 2026-07-16 JST

法域解決は`request > matter > practice-profile > tenant-default`です。日本で就労する
人、日本の事業場、日本entity/EOR/派遣、日本の労働条件・社会保険・work statusが
関係するとき本moduleを使います。勤務地、事業場、entity、employee status、
as-of dateが不明なら結論前に確認します。

## Authority

- `[B]` binding law/rule/case
- `[SG]` statutory guidance
- `[G]` administrative guidance/model
- `[I]` internal control

## Module

- `source-register.md` — official authority
- `hiring-work-rules.md` — 採用、雇用契約、就業規則、差別・harassment
- `wage-worker-status.md` — 労働者性、派遣/請負、賃金、労働時間、OSH
- `leave-harassment.md` — 育児介護、母性、年休、配慮、harassment
- `termination-investigations.md` — 解雇、雇止め、RIF、discipline、通報・調査
- `international-insurance.md` — 社会保険、労組、高齢者、EOR、移民
- `privacy-privilege.md` — APPI、monitoring、restricted matter、confidentiality

## Japan-specific exclusions

日本outputへ米国固有の雇用随意、連邦exemption/leave、older-worker release、
mass-layoff notice、health continuation、corporate interview warning、union interview
right、公務員供述免責をdefaultとして入れません。日本法に同名・同機能の制度があると
推測せず、適用法、work rules、CBA、internal policyを別々に確認します。

## Current-law gate

`currency-watch.md`に従い、次を早期適用しません。

- 2026-10-01 customer harassment・求職者sexual harassment措置
- 2026-10-01 short-time social-insurance月額賃金criterion撤廃
- 2026-10-01 part-time/fixed-term・dispatch subordinate-law/guidance改正
- 2026-10-01 OSH personal-exposure measurement phase
- 2026-12-01 Whistleblower Protection Act改正

minimum wage、social insurance、disability rate、leave、article 36、dispatch、
visa、case lawはruntimeにrefreshします。
