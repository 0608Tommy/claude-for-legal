---
name: escalation-flagger
description: >
  契約論点、金額、automatic trigger、business decisionを実務プロファイルの承認matrixへ当て、具体的なapproverと判断依頼draftを示す。承認者を知りたい、GC等へescalateしたい、権限超過をrouteしたい場合に使用する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: commercial-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# エスカレーション整理

旧来の参照labelは`/commercial-legal:escalation-flagger`。本skillは承認せず、送信せず、誰に何を判断してもらうかをdraftする。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を必ず読む。ローカルpathを使わない。
2. **Setup/user:** exact`commercial-practice-profile`と、`tenantId + practiceId + userObjectId`が一致する`user-profile`を読む。承認matrix、利用者権限、attorney contactが不明ならrouteを確定しない。
3. **Matter:** server-side binding、client、counterparty、matter override、deadlineを確認する。別matterのapprovalやdeal valueを使わない。
4. **Side:** `sales | purchasing`を契約ごとに決め、該当playbookだけを読む。
5. **Jurisdiction/source:** `request > matter > practice-profile > tenant-default`で解決し、contract quote、playbook version、deal valueのprovenanceを記録する。日本なら関連`ja-JP`moduleを読む。
6. **Confidentiality/destination:** draftの宛先がprivilege/confidentiality circle内か、channel、attachments、authorized viewersを確認する。
7. **Human review:** AIはapproval、risk acceptance、walk/accept判断を行わない。recommendationは選択肢のdraft。
8. **Write/send:** messageを自動sendしない。新規escalation draftはcanonical
   key、`recordId`、unique`idempotencyKey`で条件付きcreateし、返された
   `itemId`/`eTag`を保存する。既存record updateだけexact`itemId`とlatest
   `eTag`を要求する。いずれも人の確認が必要。

情報源とseverityは
`references/common/source-provenance-and-review.md`を使う。

## 会話state

`intake` → `characterize` → `match-matrix` → `draft-ask` → `confirm-record` → `done`

| state | action |
|---|---|
| `intake` | issue、contract、value、deadline、reviewer authorityを取得 |
| `characterize` | `dollar-threshold | term-deviation | automatic-trigger | business-decision`へ整理 |
| `match-matrix` | named person/role、channel、required co-approversを決定 |
| `draft-ask` | decision-ready messageを作る |
| `confirm-record` | 保存するexact state差分を示し、人が確認 |

## Characterize

- **Dollar threshold:** contract valueが利用者権限を超える
- **Term deviation:** standard/fallback外
- **Automatic trigger:** `never`、deal-breaker、unlimited liability、IP assignment等
- **Business decision:** legal approvalではなくbusiness owner/CFO等のcommercial choice

termが明確にfallback内なら、escalation不要と説明する。ambiguous、novel、ぎりぎりの場合はrecoverable errorとしてescalateし、何が不明かを明示する。

deal valueがMSAにない場合、order form value、thresholdのabove/below、conservative higher routeのいずれかを人に選んでもらう。推測でroutingしない。

## Matrix match

1. automatic triggerか
2. value thresholdを超えるか
3. fallback外か
4. legalではなくbusiness decisionか
5. 複数approverが必要か

「legal leadership」ではなくprofileのperson/roleを示す。matrixに空白がある場合:

> 承認matrixは[situation]を扱っていません。暫定的に[GC/owner]へroutingの所有者を確認してください `[review]`。

## Draft

`references/escalation-workflow.md`のformatを使う。approverがmessageだけで判断できるよう、exact quote、playbook position、options、recommendation、deadline、full memo linkを含める。

recommendationは理由付きで1案を示せるが、approverが決定する。walk optionを現実的な選択肢でない場合もmechanicalに入れず、deal contextに合わせる。

## Record

保存する場合:

```yaml
recordType: escalation
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[practiceId or matterId]"
recordId: "esc:[sourceReviewItemId]:[sourceReviewVersion]:[approverObjectId]"
contractItemId: "[exact itemId]"
findingIds:
  - "[finding id]"
approverObjectId: "[immutable user/group id]"
approverDisplay: "[name or role]"
channel: "[draft destination]"
status: draft
decisionBy: "[ISO date or null]"
sourceReviewItemId: "[itemId or null]"
sourceReviewVersion: "[version or artifact hash]"
```

`status: sent | approved | rejected`へAIが自動変更しない。Power Platform flowのresultがある場合もexact event IDを読み、人が見える形で表示する。

## 完了

draftと、未確認value、missing approver、deadline、保存状態を示す。「送信しますか」と自動actionへ進まず、copy-ready draft、修正、保存、終了を選んでもらう。

## 行わないこと

- issueをapproveする
- messageをsendする
- signature、redline送付、renew/cancelを実行する
- profileにないapproverを創作する
- uncertain termをsilentにlower severityへ変える
