---
name: policy-monitor
description: >
  AIポリシーと実際の運用のずれを確認する。SharePointのレビュー済みAIA、トリアージ、ベンダーレビューを前回確認以降で比較するsweep modeと、提案中のAI実務を個別比較するdirect query modeを会話で実行する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ai-governance-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# AIポリシー監視

旧来の参照ラベルは `/ai-governance-legal:policy-monitor`。自律agent、hook、subagentは使わない。Cowork会話または別途承認されたテナントautomationから明示的に開始する。

## 目的

AIAで新しい利用が条件付き承認されても、AIポリシーが更新されなければ実務と表示がずれる。本スキルは、内部実務のdriftを検出し、現行文言、gap、修正文案を人へ提示する。外部の法改正を監視する `reg-gap-analysis` とは方向が異なる。

## 必須ゲート

1. **セットアップ:** `profiles` のAI policy commitments、use case registry、outputs scope、actual policy `itemId`、複合キーが一致する現在利用者の`user-profile`を読む。対象scopeの`policy-sweep-cursor`は`state`から別途取得する。policy原文がない場合、summaryだけで確定差分を出さず、別利用者のroleを流用しない。
2. **案件:** sweep範囲がpractice-levelか特定matterかを確認する。既定で別案件を横断しない。秘密性が異なる成果物を1つの報告へ混ぜない。
3. **管轄:** policyが対象とする法域を `request > matter > practice-profile > tenant-default` で解決する。新しい実務が別法域を追加する場合は明示する。
4. **情報源:** policy原文とレビュー済み成果物を正確な`itemId`/versionで読む。引用できない、版が不明、一部のみ取得の場合はgapを確定しない。
5. **秘匿性・宛先:** 報告は元成果物の機密性を引き継ぐ。共有先、DLP、保持を確認し、相手方・公開チャネルへ内部gapを送らない。
6. **人のレビュー:** REQUIRED / ADVISABLE、修正文案、registry entryは人が確認する。スキルがpolicyを採用・更新しない。
7. **不可逆操作:** `lastAcknowledgedSweep`、`gapsFound`、policy本文、registryは、結果の明示的acknowledgment前に更新しない。公開・配布しない。
8. **失敗:** outputs取得、policy読取り、write concurrencyに失敗したら範囲を示して停止する。ローカルcrawlやローカル保存へ切り替えない。

保存、取得コンテンツ、Cowork DLP制約の詳細は
`references/common/cowork-runtime-contract.md` を必ず読む。

## モード

旧 `--sweep` はfrontmatterから除き、会話状態として扱う。

| 状態 | トリガー | 対象 |
|---|---|---|
| `sweep` | 「sweep」「前回以降を確認」「--sweep」 | SharePoint `outputs` |
| `direct-query` | 新しいAI実務の説明 | その提案とpolicy/registry |
| `acknowledge-sweep` | 結果をレビューしたとの明示 | sweep stateだけ更新 |

モードが不明なら2択を示す。

## Sweep mode

### 範囲

対象scopeの`policy-sweep-cursor`より後のレビュー済み成果物を取得する。
cursorはpractice/matterごとに分離し、ISO-8601 timestampと同時刻の
`cursorItemId`を組にして順序を確定する。cursorがなければfirst sweepとして
全件を対象にするが、大量なら期間・種類・件数を提示して分割する。

対象:

- AIA: use case、deployment mode、conditions、affected parties、vendor、disclosure
- triage: classification、tier、conditions
- vendor review: vendor、data use、accepted deviations、AI addendum
- registry updates

draft、未レビュー、別案件の成果物をpolicy上の確定実務として扱わない。

### Gap

- **REQUIRED:** policyの明示的約束と実務が矛盾する、または外部影響のある承認済み実務が無記載で、表示が実態を誤らせる。
- **ADVISABLE:** 矛盾はないが、重要な実務をpolicyが十分説明していない。

各gapに次を付ける。

- source `itemId` / output type
- actual practice
- current policyの引用
- gap
- suggested language
- owner、timing
- registry sync

テンプレートは `references/policy-monitor-outputs.md`。

### Acknowledgment

報告提示直後にstampを更新しない。「sweep結果をレビューした」「acknowledge」と明示された後だけ、同じ報告のhash/IDとともに次を更新する。

```yaml
recordType: policy-sweep-cursor
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
cursorTimestamp: "2026-07-16T14:30:00+09:00"
cursorItemId: "[last processed output itemId]"
gapsFound: 3
acknowledgedReportItemId: "[itemId]"
acknowledgedBy: "[userObjectId]"
eTag: "[eTag]"
```

acknowledgmentが曖昧なら更新しない。

## Direct query mode

提案から次を抽出する。

- system / capability
- assistive / automated / content generation
- affected people
- vendor/model
- human review
- disclosure
- data flow
- jurisdiction

曖昧なら最も結論を左右する質問を1つずつ行う。policyとregistryを次で比較する。

| Check | Current policy / registry | Proposed practice | Verdict |
|---|---|---|---|
| Use case category | | | 🟢 / 🟡 / 🔴 |
| Scope of AI use | | | |
| Automated decisions | | | |
| Disclosure | | | |
| Vendor data use | | | |
| Human oversight | | | |

結論は `POLICY UPDATE REQUIRED / ADVISABLE / NO UPDATE NEEDED` の提案。policyに反する実務を黙って許容しない。

## 修正文案

- actual policyのvoiceを合わせる。
- model名ではなくdurableな表現を優先する。
- 守れない「常にhuman review」等を約束しない。
- position変更と単なる明確化を区別する。
- 消費者・従業員向け文言は平易にする。
- 追加先のsectionを特定する。
- substantive ruleは情報源または `[review — adapted, no direct source]` を付ける。

## 定期実行

本パッケージはagentやschedulerを作成しない。週次実行が必要なら、テナント管理者が別の承認済みPower Automate等で、最小権限、idempotency、監査、human acknowledgment gateを満たすtriggerを構成する。本スキルだけで自動更新しない。

## 保存

報告初稿はOneDrive。レビュー済み報告を`outputs`へ昇格する場合、人の確認後に条件付き書込みする。policy本文の編集は別操作として差分を示し、採用承認を要求する。

## 完了

REQUIRED / ADVISABLE件数、読んだ範囲、未取得資料、次の判断を示す。policy文案、registry entry、escalation、追加事実、次回確認から選んでもらう。

## 本スキルが行わないこと

- 法改正の自律監視
- policyの自動採用・公開
- registryの無確認更新
- Slack/email等の非構造化決定を勝手に確定実務として扱うこと
- 保存されていない成果物を読んだと仮定すること
