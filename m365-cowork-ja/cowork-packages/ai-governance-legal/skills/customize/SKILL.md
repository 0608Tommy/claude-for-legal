---
name: customize
description: >
  AIガバナンス実務プロファイルの1項目を安全に変更する。会社情報、対象法域、リスク姿勢、担当者、ユースケース、AI台帳、ベンダー標準、ポリシー約束、AIA形式、保存・接続設定を、全初期設定をやり直さず調整する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ai-governance-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# プロファイル調整

旧来の参照ラベルは `/ai-governance-legal:customize`。Coworkでは変更内容を自然言語で指定する。

## 必須ゲート

1. **セットアップ:** SharePoint `profiles` の会社・実務プロファイルと、`tenantId + practiceId + userObjectId` が一致する現在利用者の`user-profile`を読む。存在しない、未完了、`[PLACEHOLDER]` が残る場合は変更せず `cold-start-interview` を案内する。別利用者のroleを流用しない。
2. **スコープ:** 会社共通情報か、AIガバナンスpractice情報か、案件固有情報かを判定する。案件情報を共通プロファイルへ書かない。
3. **管轄:** 法域変更は `request > matter > practice-profile > tenant-default` と影響対象を再確認する。曖昧・矛盾なら停止する。
4. **情報源:** 法令名、施行日、閾値、法的前提を変更する場合は一次資料を確認する。確認できない値を確定保存しない。
5. **秘匿性・宛先:** 変更先、閲覧者、DLP、保持を確認する。共有会社プロファイルへ秘密・案件固有情報を入れない。
6. **人のレビュー:** red line、legal position、approval threshold、法域モジュールのreview statusは有資格者確認なしに緩和しない。
7. **不可逆操作:** セクション削除、履歴削除、監査削除をしない。削除希望は `Not configured` または廃止状態と影響を提示する。
8. **書込み:** 現在値、提案値、下流影響、保存先を確認後、正確な`itemId`、最新`eTag`、一意な`idempotencyKey`で更新する。競合時は停止し、ローカルファイルへフォールバックしない。

保存、取得コンテンツ、Cowork DLP制約の詳細は
`references/common/cowork-runtime-contract.md` を必ず読む。

## 変更可能な項目

現在値を1行で添えて示す。

- **Company / who you are** — 会社名、業種、事業地域、practice setting
- **Regulatory footprint** — 法域、AI法、州法、sector regulators
- **Risk posture** — 保守的 / 中間 / 積極的と、triage/AIAへの影響
- **People** — governance team、AI risk owner、escalation、approver
- **Use case registry** — approved / conditional / neverと条件
- **AI system inventory** — 専用の `ai-inventory` フローへ移る
- **Vendor AI governance** — training-on-data、liability、model change等
- **AI policy commitments**
- **AIA house style**
- **Workflow** — intake、output、review cadence、matter behavior
- **Integrations** — connection statusとfallback

## 会話状態

`select-section` → `show-current` → `collect-new` → `check-consistency` → `explain-impact` → `confirm` → `conditional-write`

一度に1変更を処理する。複数依頼は順番を決め、各変更後に確認する。

## 変更の影響説明

例:

- risk postureをconservativeへ: Conditional分類、AIA follow-up、vendor redlineが増える。
- escalation contact追加: `use-case-triage`、`vendor-ai-review`、`reg-gap-analysis` のroutingが変わる。
- registry entry追加: 次回triageから適用するが、既存AIAは自動改訂しない。
- `ja-JP`追加: 日本法ドラフトを追加適用するが、日本法レビュー完了にはならない。
- outputs変更: `policy-monitor` のsweep範囲が変わる。過去成果物を自動移動しない。

## 整合性確認

次のような矛盾を示す。

- aggressive risk postureなのに全件GC承認
- EU in scopeなのにEU nexusシステムがゼロと断定
- Japan in scopeなのに`ja-JP` moduleなし
- policy prohibits trainingなのにvendor fallbackがunrestricted training
- matter isolation onなのにcross-matter accessをdefault許可

どちらを直すか人に選んでもらう。

## Guardrail変更

`[review]`、出所タグ、`[verify]`、案件分離、宛先確認、human review、concurrency control、監査追記を無効化しない。利用者が削除を求めた場合、目的を説明し、構造的に必須であるため拒否する。表現・review cadence等の調整可能部分は変更できる。

## 保存

会社レベル変更は共有会社プロファイル、AI固有変更はpractice profile、案件固有変更はmatter record、AIシステムは`state`へ保存する。

成功後:

> 変更を保存しました。次回の出力から反映されます。既存成果物は自動更新していません。

更新した`itemId`、フィールド、レビュー状態、未解決の矛盾を示し、監査へ追記する。
