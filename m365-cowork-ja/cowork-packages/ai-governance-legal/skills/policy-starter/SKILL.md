---
name: policy-starter
description: >
  公開された公式ガイダンス、モデルポリシー、実務プロファイルを根拠に、AI利用ポリシーの採用前ドラフトを作成する。対象者、適用範囲、必要セクションを先に選び、各判断点をreview対象として残す。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ai-governance-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# AI利用ポリシー初稿

旧来の参照ラベルは `/ai-governance-legal:policy-starter`。Coworkでは「会社全体のAIポリシー初稿」「既存ポリシーを2026年の変更に合わせたい」等の会話から開始する。移行元のscope hintである `firm-wide`、`legal team only`、`update existing` も会話上の意図として認識する。

## 目的

公開資料から根拠をたどれる**初稿**を作り、GC、弁護士、経営会議、IT、HR等が決めるべき選択肢を可視化する。完成・採用・配布されたpolicyを装わない。

## 必須ゲート

1. **セットアップ:** SharePoint `profiles` の会社・実務プロファイル、registry、red lines、vendor positions、governance teamと、複合キーが一致する現在利用者の`user-profile`を読む。未設定ならdraftingを停止し、`cold-start-interview` を案内する。別利用者のroleを流用しない。
2. **案件:** policyが会社全体、legal team、特定matter/clientのどれかを確認する。案件固有の秘密を全社policyへ入れない。
3. **管轄:** `request > matter > practice-profile > tenant-default` で法域を解決し、対象者・導入地域に合う公式資料を選ぶ。曖昧ならscopeを確定しない。`ja-JP`なら日本法モジュールとsource registerを使う。
4. **情報源:** substantive ruleごとに公式原文、公式guidance、公開model policy等のURLと取得日を記録する。web検索不能または原文未取得ならその旨を示し、発明しない。
5. **秘匿性・宛先:** audience、保存先、配布範囲、DLP、保持を確認する。内部legal draftとstaff-facing policyを分ける。
6. **人のレビュー:** threshold、named tool、approval path、disclosure、discipline、exceptionは `[review]`。AIはhard callを選ばない。
7. **不可逆操作:** policy採用、公開、全社配布、既存policy置換は明示的な人の承認なしに行わない。ドラフト作成同意を配布同意と扱わない。
8. **失敗:** policy原文、source、保存先、権限、versionを取得できない場合は範囲を示して停止する。ローカルファイルへ保存しない。

## Scope interview

先に必要sectionを選ぶ。全部を自動生成しない。

1. **Scope** — 対象者、対象AI、対象データ
2. **Permitted and prohibited uses**
3. **Approval and review**
4. **Disclosure**
5. **Data handling**
6. **Training and certification**
7. **Incidents and reporting**
8. **Enforcement**
9. **Review cadence and ownership**
10. **Glossary**

初回の推奨候補は1, 2, 3, 4, 5, 9だが、利用者が選ぶ。

次に確認する。

- Audience: all staff / legal only / attorneys and staff / client-facing version
- Deployment context: law firm / in-house legal / company-wide / clinic / government
- New policyかexisting policy updateか
- Desired tone、length、effective date target
- Approvers

1回に2～3個の回答可能な質問にする。

## 情報源選択

実務プロファイルの法域から導出する。

- US: ABA Formal Opinion 512、state bar guidance、ILTA、CLOC、公式法令、公開peer policies
- UK: SRA、Law Society、ICO、Bar Council
- EU: EU AI Act、EDPB、各DPA
- Australia: Law Council、OAIC、Australian AI Ethics Framework
- Singapore: PDPC Model AI Governance Framework、MinLaw、MAS
- Canada: law societies、OPC、TBS Directive
- Japan: `references/common/ja-jp/source-register.md`、AI法、AI事業者ガイドライン、PPC、文化庁、消費者庁、厚労省、デジタル庁等

複数法域では相違を示す。二次資料は一次資料探索に使い、ruleとしてそのまま採用しない。

## Drafting state

`scope` → `source-research` → `source-table` → `draft-selected-sections` → `open-questions` → `adoption-checklist` → `human-review` → `save-draft`

source tableがないままdraftへ進まない。

## Draft header

必ず冒頭に次の趣旨を置く。

```text
DRAFT FOR INTERNAL LEGAL REVIEW — NOT FOR DISTRIBUTION
Prepared for: [firm / company]
Date: [date]
Prepared by: ai-governance-legal policy-starter skill
Not for adoption, distribution, posting, or reliance until reviewed, adapted, and approved by [approver].
```

非弁護士向けには、弁護士連絡先へ持参するための初稿であり、そのまま採用できないことを追加する。

日本語版の本文表示は次を併記できる。

`内部法務レビュー用ドラフト — 配布禁止 — 有資格者と指定承認者の確認前に採用・依拠しないこと`

## Source table

| Source | URL | Accessed | What the draft used |
|---|---|---|---|

公式資料かmodel policyかを区別する。引用または適応したruleにinline sourceを付ける。取得していない資料を「確認済み」としない。

## 各section

選択されたsectionだけを書く。

- scope sentence
- substantive rules
- choice pointに `[review]`
- source attribution
- section末尾に2～3件のopen questions

例:

> 機密情報を入力できるAIは、組織が承認し、契約上の学習利用・保持・アクセス条件を確認したサービスに限る `[review — approved tools and data classes]`。

特定vendor、懲戒内容、数値threshold、例外をAIが決めない。

詳細構造は `references/policy-draft-structure.md`。

## 日本向け注意

- AI法とAI事業者ガイドラインの位置付けを区別する。
- 個人情報の入力、学習、第三者提供、国外処理をPPC資料と整合させる。
- 採用・人事AIは公正な採用選考、個人情報、労働法の専門レビューへ回す。
- 生成物・学習データは文化庁資料と著作権法を確認する。
- 2026年個人情報保護法改正は公布・施行確認前に現行ruleとして書かない。
- `ATTORNEY WORK PRODUCT` を日本法上の保護として断定しない。

## Adoption checklist

実務プロファイルの承認者から作る。

- [ ] Legal / GC review
- [ ] IT / security review
- [ ] Privacy review
- [ ] HR review（該当section）
- [ ] Executive / board approval（必要性を確認）
- [ ] Training materials
- [ ] Announcement
- [ ] Effective date `[review]`
- [ ] Review cadence
- [ ] Registry / practice profileへの反映
- [ ] Japanese qualified counsel review（`ja-JP`の場合）

## 保存

初稿はOneDriveへ保存する。SharePoint `outputs` または正式policy libraryへの昇格は、レビュー記録、承認、宛先、DLP、保持、versionを確認した別操作とする。既存policyを上書きせず、新versionとして差分を保つ。

## 完了

レビュー担当者向け注記、source table、`[review]` 件数、open questions、adoption checklistを示す。次は、flagsの解決、stakeholder summary、training draft、vendor sweep、regulatory gap checkから選んでもらう。

## 禁止事項

- scope interviewなしの全section生成
- 出所のないsubstantive rule
- 完成品に見える表示
- 利用者が選んでいないsectionの追加
- 特定vendorやdisciplineの決定
- legal sufficiencyの保証
- 自動採用・公開
