> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本雇用法 — 施行・改正watch

**基準日:** 2026-07-16 JST
**状態:** DRAFT — qualified Japanese counsel review pending

official Japanese textを優先し、英訳の遅れを考慮します。runtimeの`asOfDate`を明示し、
将来施行は施行確認前にcurrent dutyへ昇格しません。

| 日付 | 2026-07-16時点 | 影響 |
|---|---|---|
| 2024-04-01 | effective | 労働条件・募集情報の追加明示、裁量労働手続、時間外上限の適用拡大 |
| 2024-11-01 | effective | Freelance Act、freelancer労災特別加入 |
| 2025-04-01 | effective | 育児・介護休業改正第1段階、雇用保険育児給付 |
| 2025-10-01 | effective | 3歳から就学前の柔軟な働き方、意向聴取・配慮 |
| 2026-04-01 | effective | 常時雇用101人以上の女性活躍情報公表拡大、労安衛等の段階施行 |
| 2026-07-01 | effective | 民間障害者法定雇用率2.7%、原則37.5人以上 |
| 2026-10-01 | future | customer harassment・求職者sexual harassment措置、短時間社会保険の月額賃金要件撤廃 |
| 2026-12-01 | future | 2025公益通報者保護法改正 |
| 2027-04-01 | future | 育成就労制度 |
| 2027-10-01 | future | 短時間社会保険の企業規模要件36人以上へ |
| 2028-10-01 | future | 雇用保険週所定労働時間10時間へ |

## 2026-10-01 gate

`asOfDate < 2026-10-01`なら、customer harassment、求職者sexual harassmentの
新措置と社会保険月額賃金要件撤廃を「準備事項」とし、現行義務として適用しません。
`asOfDate >= 2026-10-01`でもofficial commencement/current textを再取得してから
適用します。

## 2026-12-01 gate

`asOfDate < 2026-12-01`なら2025公益通報法改正をfuture readinessとします。
`asOfDate >= 2026-12-01`でも施行済みconsolidated text、guidance、transitionを
確認してから調査・通報workflowへ適用します。

## 毎回refreshする項目

- 都道府県別・産業別最低賃金
- article 36 agreement、特別条項、上限・適用除外/猶予
- working-time system、裁量労働、高度professionalの手続
- childcare/family-care leave、個別周知、意向確認、意向聴取、配慮
- disability employment rateと算定
- social/labor insuranceの加入要件・料率
- harassment/whistleblower guidance
- dispatch licence、worker supply、EOR structure
- visa/status、foreign-worker notification
- dismissal、nonrenewal、RIF、restrictive covenantのcurrent case law
- APPI/PPC guidance、monitoring、foreign transfer

ストレスcheckの50人未満拡大等、政令施行日依存の項目はofficial commencement確認前に
有効化しません。
