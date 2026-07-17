---
name: ai-inventory
description: >
  AIシステム単位でEU AI Act上の役割、リスク区分、EUとの接点、所有者、状態、見直し期限を管理する。会社全体に単一の役割を割り当てず、台帳の一覧、追加、編集、分類、詳細表示を会話で進めたい場合に使用する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ai-governance-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# AIシステム台帳

旧来の参照ラベルは `/ai-governance-legal:ai-inventory`。Coworkではコマンドを実行せず、「台帳を一覧」「システムを追加」「`sys-001` を分類」のように会話でモードを選ぶ。

## 目的

EU AI Act上の役割とtierは**会社単位ではなくAIシステム単位**で評価する。同じ組織が、あるシステムでは `provider`、別のシステムでは `deployer`、さらに別のシステムでは `importer` になり得る。台帳は判断根拠を残すが、義務を固定表から自動生成しない。

## 必須ゲート

1. **セットアップ:** SharePoint `profiles` の会社プロファイル、`ai-governance-legal` 実務プロファイル、複合キーが一致する現在利用者の`user-profile`を読む。未作成、`[PLACEHOLDER]`、必須項目欠落なら、一覧表示以外の実質処理を停止し、`cold-start-interview` を案内する。別利用者のroleを流用しない。
2. **案件:** サーバー側のsession–matter bindingを確認する。複数候補、矛盾、権限不足なら停止する。既定で案件横断参照をしない。
3. **管轄:** `request > matter > practice-profile > tenant-default` で解決する。曖昧なら分類を停止する。`ja-JP` が含まれる場合は `references/common/ja-jp/README.md` と関連モジュールを追加で読む。
4. **情報源:** 現行のEU AI Act原文を取得できない場合、条文・Annex・施行日を確定せず `[verify against current AI Act text]` を残す。出所タグは実際の取得結果に従う。
5. **秘匿性・宛先:** 表示・保存前に閲覧者、保存先、DLP、保持、案件分離を確認する。米国法上のwork-product保護を他法域に断定しない。
6. **人のレビュー:** `prohibited`、`high_risk`、役割変更、義務判断は人のレビュー対象。台帳登録は法的結論または導入承認ではない。
7. **不可逆操作:** 追加・編集・分類結果の保存前に差分と保存先を確認する。削除は行わず、廃止は `status: deprecated` とする。
8. **Create / update:** `add`はcanonical key、`recordId`、
   `expectedAbsent: true`、一意な`idempotencyKey`でconditional createし、
   createへ架空の`itemId` / `eTag`を要求しない。`edit` / `classify`はexact
   `itemId`、latest`eTag`、一意な`idempotencyKey`でconditional updateし、
   updateへ`expectedAbsent`を含めない。stale、duplicate、partial successでは
   上書きせず停止し、ローカルファイルへフォールバックしない。

詳細な保存契約は `references/common/cowork-runtime-contract.md`、出所ルールは `references/common/source-provenance-and-review.md` を参照する。

## 会話モード

旧 `argument-hint` はfrontmatterから削除した。次の状態を本文で明示的に選ぶ。

| 状態 | 利用者の意図 | 次の状態 |
|---|---|---|
| `list` | 一覧、件数、期限切れを見たい | `done` または対象選択 |
| `add` | 新しいAIシステムを登録したい | `collect-required` → `classify-or-save` |
| `edit <id>` | 既存レコードの1項目を変更したい | `show-current` → `confirm-write` |
| `classify <id>` | 役割とtierを評価したい | `role` → `tier` → `confirm-write` |
| `show <id>` | 全項目と履歴を見たい | `done` |

意図が不明なら、この5つを提示して1つ選んでもらう。一度に複数の書込みを暗黙に行わない。

## 状態レコード

SharePoint `state` リストに1システム1レコードで保存する。列名またはJSON値は次の正規値を保持する。

```yaml
recordType: ai-system
tenantId: "[tenant id]"
practiceId: "[practice id]"
pluginId: ai-governance-legal
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
id: sys-001
name: "Resume screening tool"
owner: "HR / Jamie"
description: "Filters inbound CVs against job criteria"
status: in_production
eu_nexus: true
role: deployer
role_basis: "We license from VendorX and deploy internally [verify against current AI Act text]"
tier: high_risk
tier_basis: "Annex III(4)(a) — employment, recruitment selection [verify against current AI Act text]"
obligations_assessed: false
obligations_note: "Assessment required; no table-derived conclusion"
next_review: "2026-08-01"
review_trigger: "on substantial modification or annually"
created: "2026-05-11"
updated: "2026-05-11"
```

正規enum:

- `status`: `planned | in_development | in_production | deprecated`
- `role`: `provider | deployer | importer | distributor | authorized_rep | product_manufacturer`
- `tier`: `prohibited | high_risk | limited | minimal | gpai | gpai_systemic`

日本向け追加分類が必要な場合は、EU値を上書きせず `japan_role`、`japan_risk_notes` 等の別フィールドを使う。

## 書込み契約

`add`と既存recordの変更を同じrequest shapeにしない。

| Operation | Required concurrency fields | Forbidden |
|---|---|---|
| create (`add`) | canonical key、`recordId`、`expectedAbsent: true`、unique `idempotencyKey` | pre-existing `itemId` / `eTag` |
| update (`edit`, `classify`, `deprecated`) | exact `itemId`、latest `eTag`、unique `idempotencyKey` | `expectedAbsent` |

create成功後にresponseのexact `itemId` / `eTag`を保持する。どちらも保存先、
保持、DLP、閲覧者、権限、差分を人が確認した後の1回の条件付きoperationであり、
台帳登録、分類、廃止、承認、外部送信を自動実行しない。

## `list`

正確な案件・実務スコープ内のレコードだけを取得し、次の表を出す。

| ID | Name | Owner | Status | EU nexus | Role | Tier | Next review |
|---|---|---|---|---|---|---|---|

表の下にtier別件数と「30日以内にレビュー予定のN件」を示す。10行を超える場合は、tier、status、EU nexus、ownerで絞れるダッシュボードを提案するが、依頼なしに作らない。

## `add`

次を1項目ずつ、または構造化された貼付けから取得する。

1. `name`
2. `owner`
3. `description` — 何をし、どのデータを使うか
4. `status`
5. `eu_nexus` — EU/EEAでの導入・提供、またはEU/EEAの人への影響
6. 今すぐ分類するか、未分類で保存するか

`sys-NNN` は同一スコープ内の最大番号の次を割り当て、完全なcanonical keyと
`expectedAbsent: true`で競合しないconditional createを行う。成功responseの
`itemId` / `eTag`を保持する。必須値のないレコードを完成扱いにせず、timeoutや
duplicate時に別IDで再createしない。

## `edit <id>`

現在値、exact `itemId`、latest `eTag`、更新履歴を示し、変更する1項目、
新しい値、下流影響を確認する。role/tierを直接書き換える依頼では、分類根拠も
同時に更新する。`id`、`created`、監査履歴は変更せず、update requestへ
`expectedAbsent`を含めない。

## `classify <id>`

詳細手順は `references/classification-and-record.md` を読む。

1. EUとの接点を再確認する。
2. システムについて組織が何をするかを確認し、`role` と `role_basis` を提案する。
3. Article 5 → Annex III → GPAI → limited → minimalの順で検討する。
4. `substantial modification`、目的変更、fine-tuning、rebrandingがあればprovider化の可能性を `[review]` とする。
5. 結果と根拠、exact diffを見せ、人が確認してからexact `itemId` / latest
   `eTag`でconditional updateする。

分類を説明なしに自動確定しない。条文対応が未検証ならタグを外さない。

## `show <id>`

全フィールド、最終検証日、根拠、未完了事項、次回レビュー、監査イベントへの参照を表示する。別案件のレコードは候補にも出さない。

## 義務の扱い

「このシステムの義務は何か」と聞かれた場合、role × tier表から断定しない。現行法を取得し、システムの役割、tier、導入日、法域、業種を会話で分析し、正式記録が必要なら `aia-generation` へ引き継ぐ。旧来の正規参照ラベルは `/ai-governance-legal:aia-generation` だが、Coworkでは同じ会話で開始できる。

## 完了

書込み後は、保存先、`itemId`、更新したフィールド、未検証事項、次回レビューを短く示す。義務評価またはAIAを続けるかを提案するが、利用者の代わりに承認しない。

## 移行上の修正

- `argument-hint` を削除し、`list | add | edit <id> | classify <id> | show <id>` を会話状態として本文へ移したため、報告済みfrontmatterエラーを解消している。
- ローカルの `ai-systems.yaml` 書込みをSharePoint `state` レコードへ置換した。
