---
name: use-case-triage
description: >
  提案されたAI利用を実務プロファイルのuse case registry、red lines、governance tierと照合し、APPROVED、CONDITIONAL、NOT APPROVEDの暫定分類、必要条件、承認経路、AIA・privacy・product reviewへの引継ぎを示す。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ai-governance-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# ユースケース・トリアージ

旧来の参照ラベルは `/ai-governance-legal:use-case-triage`。Coworkでは利用内容または複数のbacklogを会話で提示する。移行元の正規token `batch` は、複数件モードを選ぶ会話上の意図として扱う。

## 目的

「AIをこれに使ってよいか」という提案を、組織が既に決めたregistryとred linesから素早く分類する。トリアージはgatewayであり、詳細AIAまたは最終承認の代替ではない。

## 必須ゲート

1. **セットアップ:** SharePoint `profiles` のpractice profile、registry、red lines、tier、approval pathと、複合キーが一致する現在利用者の`user-profile`を読む。未設定・placeholderなら実質分類を停止し、`cold-start-interview` を案内する。別利用者のroleまたはgeneric defaultで承認しない。
2. **案件:** session–matter bindingを確認し、必要なmatter contextとoverrideだけを読む。未選択、矛盾、別案件しかない場合は停止する。
3. **管轄:** 影響を受ける人と所在地を確認し、`request > matter > practice-profile > tenant-default` で解決する。全適用法域を確認し、最も都合のよい法域を選ばない。曖昧なら分類を保留する。
4. **情報源:** 規制を理由に使う場合、現行一次資料を取得し、出所タグを付ける。条文・日付・thresholdを補作しない。
5. **秘匿性・宛先:** 結果の保存先、閲覧者、privilege/confidentiality、DLP、保持を確認する。広いchannelへ内部理由を送らない。
6. **人のレビュー:** APPROVED、NOT APPROVED、red-line exception、High tierは人の判断。AIは導入を許可・禁止しない。
7. **不可逆操作:** 本番導入、registry更新、businessへのhard no送付、外部送信は明示確認後。非弁護士には弁護士確認用briefを先に作る。
8. **失敗:** registry、policy、法域、vendor、human oversight等の重要情報が不足、または書込み競合なら停止する。ローカル保存へフォールバックしない。

## 状態

`understand` → `registry-match` → `red-line-check` → `jurisdiction-check` → `classify` → `human-gate` → `conditions` → `handoff` → `registry-proposal`

## 1. 利用内容を理解する

曖昧なら次を1つずつ確認する。

- AIは生成、score、classification、recommendation、actionのどれを行うか。
- employees、customers、applicants、third partiesの誰に影響するか。
- 人は出力前に実質レビューできるか。
- vendor / tool / modelは何か。
- internal-onlyかexternalか。
- personal/confidential dataを扱うか。
- どの法域の人が影響を受けるか。

「AIで採用を改善」等の抽象表現のまま分類しない。

## 2. Registry match

- **Direct match:** 登録済みの分類と条件を適用する。
- **Near match:** 類似項目を示し、差異が結論を変えないか確認する。
- **No match:** `CONDITIONAL` pending AIAを既定にし、preliminary riskと必要事実を示す。

registryは権限ある最新versionを使う。過去の会話記憶を優先しない。

## 3. Red line

一部でもred line候補に触れる場合、先に示す。

> この利用は `[red line]` に触れる可能性があります。実務プロファイル上はautomatic stopです。例外を適用するかはトリアージではなく、人の法務判断です。

red lineを弱めてConditionalにしない。例外を求める場合は、理由、代替設計、承認者を明確にしてエスカレーションする。

## 4. 法域

実務プロファイルの全regimeと、今回の対象者・導入地域から追加で見つかるregimeを確認する。複数法域では、各法域の結果を分け、厳しい条件を全体の最低条件とする。

EU/米国の基礎は `references/common/original-jurisdiction-logic.md`。日本は `references/common/ja-jp/README.md`。

例:

- EU employment high-risk候補
- NYC LL 144のbias audit候補
- 日本の公正採用、個人情報、労働法レビュー

pinpoint citationは一次資料なしに確定しない。

## 5. Classification

正規値:

- `APPROVED`
- `CONDITIONAL`
- `NOT APPROVED`

分類基準、conditions、tierはpractice profileから取る。定義されていない論点は利用者にpositionを確認し、勝手にplaybookを作らない。

### 人のゲート

- `APPROVED`: 本番利用を許可する結果になるため、指定approverの明示確認が必要。
- `NOT APPROVED`: business askを止めるため、同様に指定approverの確認が必要。
- `CONDITIONAL`: 条件案として提示できるが、条件充足の認定は人が行う。

非弁護士には、use case、registry mapping、red line、リスク、質問を1ページにまとめ、弁護士確認までhard yes/noを確定しない。

## 6. Output

`references/triage-output.md` を使う。必須要素:

- use case
- proposed classification
- registry match
- reasoning
- red lines
- jurisdiction notes
- governance tierとapproval path
- Conditionalの場合のowner付き条件
- human review status
- information sources

## 7. 引継ぎ

- ConditionalまたはHigh: `aia-generation`（旧来参照ラベル `/ai-governance-legal:aia-generation`）
- personal data: PIA/DPIA（`/privacy-legal:pia-generation`）
- new vendor: `vendor-ai-review`（`/ai-governance-legal:vendor-ai-review`）
- product feature: product counsel launch review（`/product-legal:launch-review`）
- 未登録system: `ai-inventory`（`/ai-governance-legal:ai-inventory`）

Coworkでは別コマンドを実行させず、この会話で次のworkflowへ進むか確認する。

## 8. Registry proposal

未登録またはnear matchの差異が重要なら、次を提案する。

| Use case | Approved | Conditions / Requirements | Never — reason |
|---|---|---|---|

人の確認後、SharePoint practice profileまたは専用`state` recordを正確な`itemId`、最新`eTag`、一意な`idempotencyKey`で更新する。提案だけで保存しない。

## Batch

複数件は先にsummaryを出す。

| # | Use case | Proposed classification | Key condition / blocker |
|---|---|---|---|

APPROVED以外を個別展開する。10件超ならdashboardを提案するが、依頼なしに作らない。件数が大きい場合はbatch範囲と未処理件数を明示する。

## Edge cases

- **Already live:** retroactive triageと明示し、既存registry、未実施AIA、実際の条件充足を確認する。
- **Internal only:** employee screening/monitoring等は低リスクとは限らない。
- **Vendor says safe:** vendor説明は独立評価の代替ではない。
- **Pilot:** real data・real peopleを扱うpilotは免除されない。
- **Human in the loop:** rubber-stampなら実効的監督と扱わない。

## 完了

最も重要な未解決事実を1つ示し、AIA、条件文案、escalation、追加質問、watch-and-waitから選んでもらう。AIが選択を代行しない。
