---
name: customize
description: >
  商事契約実務profileの1項目を、全初期設定をやり直さず安全に変更する。会社情報、法域、risk posture、approver、sales/purchasing playbook、NDA・SaaS position、house style、review preference、matter、connectionを調整する場合に使用する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: commercial-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Profile調整

旧来の参照labelは`/commercial-legal:customize [section]`。Coworkでは自然言語で変更を指定し、1変更ずつ確認する。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を必ず読む。local configを編集しない。
2. **Setup/user:** exact company/practice profileと現在利用者の`user-profile`を読む。存在しない、`setupStatus`未完了、required position欠落なら`cold-start-interview`へ案内する。
3. **Scope:** company、user、practice、matter、stateのどこへ属する変更か判定する。user roleをshared practiceへ、matter secretをcompanyへ書かない。
4. **Side:** playbook変更は`sales | purchasing`を明示し、反対側を変更しない。
5. **Jurisdiction/source:** law、effective date、thresholdを変更する場合、primary source確認ができるまで確定しない。日本は`ja-JP`moduleの`pending`を維持する。
6. **Confidentiality:** destination、authorized viewers、retention、legal hold、保存境界DLPを確認する。
7. **Human review:** legal position、NDA GREEN criteria、never、automatic escalation、risk acceptance、approval thresholdの緩和はqualified reviewer確認なしに`approved`へしない。
8. **Per-change write:** current value、proposed value、downstream impact、exact destinationを示し、各変更ごとに確認する。exact`itemId`、latest`eTag`、unique`idempotencyKey`で1回だけ条件付き更新する。

profile構造は`references/profile-schema.md`、情報源ruleは
`references/common/source-provenance-and-review.md`。

## 変更map

- **Company:** name、entity、industry、business、practice setting
- **Jurisdictions:** operating、governing、consumer/data/worker footprint
- **Risk posture**
- **People:** approver、attorney contact、authority
- **Playbook sales**
- **Playbook purchasing**
- **NDA triage**
- **SaaS / AI/ML rights**
- **Escalation**
- **Review preferences:** `confirmRouting`
- **House style**
- **Workflow:** matter、renewal、proposal
- **Integrations**

現在値を1行で添える。何を変更したいか既に明確なら全mapを表示せず、その項目へ進む。

## 会話state

`select-scope` → `show-current` → `collect-new` → `check-consistency` → `explain-impact` → `confirm-one-change` → `conditional-write` → `audit` → `next-or-done`

複数変更依頼は順番を決めるが、batch approvalにまとめない。各diffを個別承認する。

## Impact例

- liability fallbackを12か月→6か月: future`review`のdeviation thresholdが変わる。past memoは自動変更しない。
- approver変更: future escalation routeが変わる。既存draft/sent recordは自動付替えしない。
- `confirmRouting: false`: routing confirmationを省略できるが、memoにrouting decisionを残す。
- `ja-JP`追加: 日本法draftを追加適用するが、qualified review完了にはならない。
- renewal horizon変更: display defaultが変わる。既存deadline calculationは再計算・確認なしに書き換えない。

## Consistency

次をflagする。

- `activeSide: sales`なのにpurchasing positionを変更
- aggressive postureと全件GC approval
- NDA GREEN criteriaが未review
- auto-renewalを許容するのにrenewal state/ownerなし
- matter isolation onでcross-matter default allow
- AI training禁止とSaaS fallback unrestricted
- Japan in scopeで`ja-JP`なし

AIがどちらを優先するか決めず、人に選んでもらう。

## Guardrail

次をdisableしない。

- `[review]`, provenance, `[verify]`
- matter isolation、destination check
- human approval、per-change confirmation
- exact item ID、ETag、idempotency
- audit append
- non-lawyer consequential-action gate
- Cowork DLP production blocker

削除依頼は、必要なら`Not configured`、deprecated、disabled-with-reasonとして影響を示す。history/auditを削除しない。

## Integration change

connection statusはlive probeに基づく。Ironclad、DocuSign、iManage、
TopCounsel、Definely、Slack、Google Drive等の候補名があるだけで
`connected`にしない。runtimeでpackage外のdraft metadataへ依存せず、
credentialやsecretをprofileへ保存しない。

## 完了

updated item ID、field、old/new、review status、未解決矛盾を示す。

> 変更は次回の出力から反映されます。既存memo、renewal、proposal、sent escalationは自動更新していません。

追加変更があれば同じstate machineを最初から1件ずつ実行する。
