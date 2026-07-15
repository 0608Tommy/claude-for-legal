---
name: aia-generation
description: >
  AI影響評価（AIA）を作成する。構造化インテーク、法域別の規制分類、ポリシー整合性、具体的リスクと対策、導入条件、プライバシー・ベンダーレビューへの引継ぎを、実務プロファイルのhouse styleで文書化する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ai-governance-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# AI影響評価

旧来の参照ラベルは `/ai-governance-legal:aia-generation`。Coworkでは対象システムまたはトリアージ結果を会話で指定する。

## 目的

AIAはフォームではなく、設計・導入判断の記録である。AIが何をし、どう出力し、誤った場合に誰が害を受け、人がどこで介入でき、導入してよい条件は何かを文書化する。個人データの適法性を扱うPIA/DPIA、基本権影響評価（FRIA）、formal conformity assessmentの代替ではない。

## 必須ゲート

1. **セットアップ:** SharePoint `profiles` の会社・実務プロファイルと、複合キーが一致する現在利用者の`user-profile`を読み、AIA trigger、house style、sign-off、AI policy commitmentsを確認する。不足なら substantive analysisを停止し、`cold-start-interview` を案内する。別利用者のroleを流用しない。
2. **案件:** session–matter bindingと正確な案件資料を確認する。案件が必要なのに未選択、複数候補、他案件しか見つからない場合は停止する。
3. **管轄:** `request > matter > practice-profile > tenant-default` で解決する。影響を受ける人や導入地域がプロファイル外なら再導出する。曖昧なら結論を出さない。`ja-JP` なら日本法モジュールを追加する。
4. **情報源:** 法令、施行日、tier、閾値、義務は現行の一次資料を確認する。取得できない条文を補作しない。出所タグと `[verify]` / `[review]` を残す。
5. **秘匿性・宛先:** 成果物の保存先、閲覧者、privilege/confidentiality、DLP、保持を確認する。外部向け版は内部版と分ける。
6. **人のレビュー:** リスク分類、残余リスク、導入条件、最終勧告は有資格者・指定承認者のレビュー対象。AIは承認しない。
7. **不可逆操作:** `Status: APPROVED`、本番導入、共有成果物への昇格、外部送信は明示確認なしに行わない。非弁護士利用者には弁護士確認用ブリーフを先に作る。
8. **失敗:** 資料を読めない、全体の一部しか読めない、書込み競合、コネクタ不通なら範囲と失敗を示し、推測で埋めない。ローカル保存へ切り替えない。

詳細は `references/common/cowork-runtime-contract.md` と `references/common/source-provenance-and-review.md`。

## ワークフロー

状態は次の順に進める。

`scope` → `need-check` → `risk-track` → `intake` → `jurisdiction-analysis` → `policy-diff` → `draft` → `human-review` → `save-draft`

途中の必須情報が欠けたら前の状態へ戻る。利用者が「承認して」と言っても `human-review` を飛ばさない。

## 1. Scope

- 評価対象のシステム、feature、vendor、version
- 提案、pilot、production、scaledのどの段階か
- 既存の `ai-inventory` レコードと過去評価
- 対象案件、利用者、影響を受ける人、導入地域
- 依頼された成果物と保存先

## 2. AIAが必要か

実務プロファイルのtriggerに加え、次のいずれかなら原則評価する。

- 人に影響する判断を行う・実質的に左右する
- 個人データを扱う
- 顧客・応募者・従業員・第三者に接する
- 第三者モデルを使う
- Elevated / High tier
- 新しい法域、データ、目的、モデル、重大変更

不要なら、理由、前提、再評価トリガーを1段落で記録する。評価不要という判断自体を人が確認する。

## 3. Risk track

house styleの基準に従い `Fast track` または `Full assessment` を選ぶ。基準がなければFullを既定にし、後でプロファイルへ追加する候補を示す。雇用、信用、医療、公共サービス、生体、未成年者、完全自動判断、重大な外部影響はFast trackにしない。

## 4. Intake

必須質問は `references/intake-and-regulatory-analysis.md` を使い、フォームを一括で投げず会話で取得する。少なくとも次を確定する。

- 何を入力し、何を出力し、どの行動につながるか
- assistive / augmentative / automated
- 誰が影響を受け、現実的な最悪被害は何か
- personal data、学習、RAG、保存、国外処理
- 人による変更権限、異議、訂正、停止
- accuracy、bias、security、testing
- owner、scale、stage、過去の異議・事故

「human in the loop」との説明は、実際の変更率・時間・権限が確認できなければ `Nominally (rubber-stamp risk)` とする。

## 5. 法域別分析

各法域を分けて調査する。

- 適用範囲、役割、tier
- 禁止候補
- 透明性、記録、人の監督、テスト、登録、事故報告
- provider/builderとdeployer/userの義務差
- FRIA等の別成果物
- 施行・経過措置
- sector law、契約、外部コミットメント

EUロジックは `references/common/original-jurisdiction-logic.md`、日本は `references/common/jurisdictions/ja-jp/README.md` から関連ファイルを読む。

実務プロファイルのfootprintが古く、今回の対象者・判断類型を含まない場合、現在の事業地域と事実から再導出し、プロファイル更新候補を示す。`AI role: Both` 相当なら法域ごとにproviderとdeployerの義務を別列にする。

## 6. Policy diff

AI policy commitments、use case registry、red lines、vendor positionsと比較する。

| 項目 | 現在の約束 | 設計・運用 | 結果 |
|---|---|---|---|
| 利用カテゴリ | [profile] | [system] | 🟢 / 🟡 / 🟠 / 🔴 |
| 人による監督 | | | |
| 開示 | | | |
| vendor/data use | | | |
| approved tools | | | |

矛盾を「両方要確認」のまま放置しない。設計変更、ポリシー変更、停止のどれを誰が判断するかを条件にする。

## 7. リスク品質

2～5件の具体的なリスクを優先する。

- 悪い例: 「hallucination」
- 良い例: 「顧客向け回答に存在しない返金条件を生成し、送信前レビューがないため誤表示になる」

- 悪い例: 「bias」
- 良い例: 「過去採用データの偏りを学習したscoreが、特定集団を低く評価し、人がscore根拠を見ず除外する」

各リスクにlikelihood、impact、control、owner、status、residual riskを付ける。上流の重大度を理由なく下げない。

## 8. 成果物

house styleがあれば優先する。なければ `references/default-aia-template.md` を使う。必須要素:

- レビュー担当者向け注記
- 内部法務レビュー用の適切な機密表示
- Executive summaryとoverall risk
- システム、対象者、データ、監督、accuracy/bias/security
- 法域別分類と情報源
- policy consistency
- risks and mitigations
- `APPROVED / APPROVED WITH CONDITIONS / CHANGES REQUIRED / NOT APPROVED` の**提案**
- conditions、owner、deadline
- PIA、vendor review、FRIA等の引継ぎ
- cite check、未確認事項

非弁護士向けでは、不確かな日付・閾値を本文で断定せず、「弁護士に確認する事項」へ集約する。

## 9. 人によるレビューと保存

初稿はOneDriveに個人ドラフトとして保存する。SharePoint `outputs` へ昇格する前に、指定承認者、秘匿性、共有先、保持、DLPを確認する。`itemId`、`eTag`、`idempotencyKey` を使い、監査イベントを追記する。

`Status: APPROVED` にするには、承認者の明示確認とレビュー記録が必要。非弁護士が承認を求める場合は、システム、分類、主要リスク、残余リスク、未解決点を1ページにまとめ、弁護士レビューまでDRAFTのまま停止する。

## 引継ぎ

- 個人データ: PIA/DPIAを並行（旧来参照ラベル `/privacy-legal:pia-generation`）
- 新規vendor: `vendor-ai-review`（`/ai-governance-legal:vendor-ai-review`）
- 新規法規制: `reg-gap-analysis`（`/ai-governance-legal:reg-gap-analysis`）
- 未登録システム: `ai-inventory`（`/ai-governance-legal:ai-inventory`）
- 新規product feature: product counsel review（`/product-legal:launch-review`）

Coworkでは別コマンドを実行させず、「この会話で次の評価へ進むか」を確認する。

## 終了

「チェックリストにないが確認したい1点」を必要に応じて示し、次の選択肢を出す: 条件文案、エスカレーション、追加質問、監視・再評価、その他。AIが最終決定を選ばない。

## 移行上の修正

移行元の `aia-generation` は20,000文字を超えていた。必須ゲートと中核フローを本書に残し、詳細インテークと標準テンプレートを2つのcompanion fileへ分離したため、strict character limitに対応する。
