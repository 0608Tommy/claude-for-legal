---
name: review-proposals
description: >
  SharePoint stateのpending playbook proposalを1件ずつ読み、Accept、Reject、Edit、Deferを会話で処理する。deviation pattern、現行・提案文言、supporting dealsを確認し、各変更を別々に承認してpractice profileへ条件付き反映する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: commercial-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Playbook proposal review

旧来の参照labelは`/commercial-legal:review-proposals`。移行元`playbook-monitor` agentのreview/approval部分を、SharePoint / Power Platform stateのCowork front endへ移す。agent、hook、autonomous monitorは本packageに含まない。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を必ず読む。移行元のproposal fileやmonitor logへwriteしない。
2. **Setup/user:** exact practice profile、現在利用者の`user-profile`、approval authorityを読む。別userのdecisionを流用しない。
3. **Matter/scope:** proposalとsupporting deviationの`scopeType/scopeId`を確認する。matter proposalをpracticeへ昇格する場合は別reviewが必要。
4. **Side:** proposalの`sales | purchasing`を確認し、反対側のplaybookへapplyしない。
5. **Source:** proposal generation、deviation item IDs、date、one-off exclusion、current profile versionを読む。missing supporting dataを推測しない。
6. **Jurisdiction:** legal positionに関係する変更は`request > matter > practice-profile > tenant-default`で該当moduleを読み、primary sourceを確認する。
7. **Human review:** playbook変更はlegal/practice judgment。AIがAcceptを選ばない。NDA GREEN、never、automatic escalation等の変更はqualified reviewerが必要。
8. **Per-change write:** proposalごと、fieldごとにexact diffを示し、Accept/Edit後にもう一度`Confirm? yes/no`を得る。exact`itemId`、latest`eTag`、unique`idempotencyKey`でconditional writeする。

provenance、severity、irreversible actionは
`references/common/source-provenance-and-review.md`を使う。

## 会話state

| state | action |
|---|---|
| `list` | pending/deferred proposal一覧 |
| `review-next` | 1件をfull display |
| `accept` | proposed diffを提示 |
| `reject` | reasonを記録、profile変更なし |
| `edit` | user wordingを取得しdiff提示 |
| `defer` | exact dateまたはapproved monitor run IDを記録 |
| `confirm-change` | 1変更だけconditional write |
| `generate-draft` | exact deviation stateからon-demand draftを作る |
| `summary` | accepted/rejected/edited/deferred結果 |

利用者がoptionを選ぶまで次proposalへ進まない。batch Acceptをしない。

## No proposal

scope内に`status: pending`、または`status: deferred`かつ
`deferUntil <= today` / `deferAfterRunId`で指定したrun ledger recordの
`status: completed`を満たすrecordがなければ:

`deferAfterRunId`は「現在のlatest run」と比較しない。指定runが完了した時点で
proposalを`pending`へ条件付きtransitionし、後続runがあっても消えないように
する。

> Pending proposalはありません。Playbookが最新という意味ではなく、review対象recordがない状態です。

scheduled flowのlast runがなければ、その事実も示す。

`deal-debrief`と`playbook-monitor`の互換state・trigger・one-off ruleは
`references/automation-contract.md`を読む。

## Proposal content

各proposalに:

1. pattern、count、period、common basis
2. current exact playbook language
3. proposed exact language
4. supporting deal/deviation IDs
5. `Revise | Clarify | Flag for discussion`
6. side、scope、generatedAt、profile version
7. excluded one-offs

default pattern settingは`patternThreshold: 5`, `lookbackMonths: 12`だが、profile値を優先する。

directionally inconsistentなdeviationは`Clarify`候補。one-off`excludeFromPatterns: true`をcountしない。

## `generate-draft`

Power Platform flowがなくても、利用者の明示依頼でexact deviation recordsからread-only計算できる。

- lookback内
- scope/side/clause一致
- one-off除外
- direction group
- threshold

threshold未達ならproposalを作らない。生成draftは`status: draft`であり、保存も別確認。notificationを自動sendしない。

## Review

1件ずつ`references/proposal-records.md`のformatで提示する。

### Accept

current profileを再取得し、proposal作成時versionからのdriftを確認する。driftがあればstale proposalとして停止し、rebase draftを作る。

```diff
- [current text]
+ [proposed text]
```

downstream effectを説明し、`Confirm? yes/no`後にのみwrite。

### Edit

user wordingをverbatim candidateとして保持し、consistency、side、jurisdiction、guardrailを確認する。exact diffを再提示し、confirmation後にwrite。

### Reject

profileを変更しない。reason、rejection date、pattern snapshotを記録する。同じsnapshotを次cycleで再提出しない。rejection後のnew deviationsでpatternが変わった場合は新proposalにできる。

### Defer

profileを変更しない。`deferUntil`または`nextCycle`を記録する。

## Apply transaction

profile updateとproposal status updateを可能ならtransactional flowで行う。atomicでない場合:

1. profile conditional write
2. success確認
3. proposal status conditional write
4. partial successをauditし、推測でretryしない

同じidempotency keyでduplicate changeを作らない。old proposalをdeleteせず`resolved | superseded | archived`にする。

## Completion

accepted、edited、rejected、deferred、stale、failedを件数とexact IDsで示す。profile updated timestamp、pending qualified review、次のmonitor statusを示す。

## 行わないこと

- playbookを自動変更する
- per-change confirmationをbatch化する
- one-offをpatternに入れる
- rejected proposalを同じdataで再提出する
- Power Platform flow、notification、scheduleがあると推測する
- audit/proposal historyをdeleteする
