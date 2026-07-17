---
name: review
description: >
  契約のtitle、exhibit、schedule、order formを先に読み、NDA、vendor/services、SaaS overlay、combined reviewへrouteする。売り手側・買い手側playbookとの差、修正文案、renewal handoff、named approverを単一memoで示す。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: commercial-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Commercial contract review

旧来の参照labelは`/commercial-legal:review [file path | Drive link | CLM ID | paste text]`。

移行元のhidden helper:

- `vendor-agreement-review`
- `nda-review`
- `saas-msa-review`

は登録せず、本skillと`references/vendor-review.md`、`references/nda-review.md`、`references/saas-overlay.md`へ統合する。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を必ず読む。local file path、home directory、cacheへread/writeしない。
2. **Setup/user:** exact company/practice profileと、`tenantId + practiceId + userObjectId`が一致する`user-profile`を読む。該当side playbookが未設定・未reviewならformal playbook verdict、NDA GREEN、signature-readyを出さず、`cold-start-interview`へ案内する。
3. **Matter:** matter bindingがある場合はbinding statusとmatter
   `status: active`、client、counterparty、matter overrideを確認する。
   revoked bindingまたはarchived matterでは実質レビューを停止する。
   matter workspaceが無効、またはfresh sessionで明示的にpractice-levelを
   選んだ場合は`scopeType: practice`でreviewできるが、過去matterのcontract、
   quote、draft、renewal、precedentをcarryしない。
4. **Side:** 契約ごとに`sales | purchasing`を確定し、該当sideだけを適用する。reseller、partnership、revenue share等で曖昧なら質問する。
5. **Jurisdiction:** `request > matter > practice-profile > tenant-default`。governing law、party、performance、consumer/data/worker locationを確認し、日本なら`references/common/ja-jp/README.md`と該当moduleを読む。
6. **Source:** exact contract item/version、全exhibit、incorporated URL、order form、DPA、SLAを読む。missingとunreadを分け、partial readでcomprehensive conclusionを出さない。
7. **Confidentiality/destination:** NDA、privilege、clean-team、authorized viewers、retention、legal hold、保存境界DLPを確認する。internal reviewをcounterpartyへそのまま出さない。
8. **Human review/irreversible:** severity、fallback、redline、risk acceptance、
   signature、renew/cancelは人の判断。AIはsend、sign、approve、state updateを
   自動実行しない。新規review/deviation draftはcanonical key、`recordId`、
   unique`idempotencyKey`で条件付きcreateする。既存record updateはexact
   `itemId`とlatest`eTag`を要求し、いずれも別confirmationを必要とする。

情報源、reviewer note、dual severity、decision treeは
`references/common/source-provenance-and-review.md`。

## Setup incomplete

正式reviewは停止し、quick/full setupを案内する。利用者が明示的にgeneral issue spottingを求めた場合だけ、playbook comparisonではない`[PROVISIONAL — no configured playbook]`のresearch notesを作れる。その場合:

- GREEN、signature-ready、approval不要を出さない
- generic market positionをteam positionと書かない
- findingごとに`[PROVISIONAL]`
- 保存する場合もdraftのみ

## 会話state machine

| state | action |
|---|---|
| `collect-source` | exact items/attachmentsを取得 |
| `read-structure` | main titleと全attachment titleを先に抽出 |
| `route-nda` | NDA triage |
| `route-vendor` | vendor/services review |
| `route-saas-overlay` | vendor review + SaaS overlay |
| `route-combined` | 複数document/skillを単一memoへ |
| `routing-confirmation` | `confirmRouting: true`なら確認 |
| `review` | applicable reference workflowを実行 |
| `escalation-check` | named approverを整理 |
| `handoff-review` | renewal、summary、deviation draft候補 |
| `confirm-save` | draft保存またはshared output昇格 |

body keywordだけでrouteしない。titleが`Agreement`等で曖昧なら最初の2pageとtable of contentsを読み、解決できないときだけ質問する。

## Routing

`references/review-routing-and-output.md`のtableを使う。

典型:

- standalone NDA → `route-nda`
- MSA/SOW/services → `route-vendor`
- SaaS/subscription/order form/SLA → `route-saas-overlay`
- MSA + DPA + order form + SLA → `route-combined`

`confirmRouting: true`またはfield欠落時:

```text
この契約を次としてreviewします: [type(s)]
- [title] → [workflow]
- [exhibit] → [workflow]
このroutingでよいですか。
```

confirmation後に進む。`false`ならmemo先頭にrouting decisionを記録する。

## Read coverage

50page超、多数attachment、URL termsがある場合:

- definitions
- scope/obligations
- fees/order form
- term/renewal/termination
- liability/indemnity
- IP/data/confidentiality
- security/SLA
- governing law/dispute

を優先し、read/unreadをreviewer noteへ記録する。全文未読なら「full review」と表記しない。

## Deal-breaker

該当sideの`oneThing`を先に確認する。存在すればtopへ⛔を置き、specific responseを示す。利用者がcomplete reviewを求めている場合は「解決までmoot」と明示して残りも続ける。

## Dollar value

MSAにvalueがなくorder formが別なら、approval thresholdを計算する前に:

1. exact ACV/TCVを取得
2. threshold以上/未満だけ利用者が確認
3. conservative higher approverへroute

のいずれかを選ぶ。silent assumptionをしない。

## Review application

- vendor/services: `references/vendor-review.md`
- NDA: `references/nda-review.md`
- SaaS: vendor workflow全部 + `references/saas-overlay.md`
- output/routing: `references/review-routing-and-output.md`

checklistはfloorであり、依頼に関連する追加issueを無視しない。依頼が標準memoと異なる場合、求められたartifactを直接作りつつ共通guardrailを適用する。

## Finding

各deviation:

- playbook exact position
- contract full relevant quote、section、item/version
- `Missing | Weaker than standard | Weaker than fallback | Non-standard structure | Unacceptable`
- legal risk
- business friction
- why it matters
- smallest workable redline language
- fallback / named approver
- jurisdiction note

playbookにpositionがなければ、market defaultを保存せず`[review]`としてpositionを決めてもらう。

## Japanese module

日本が含まれる場合、issueに応じて:

- `references/common/ja-jp/contract-core.md`
- `references/common/ja-jp/privacy-data.md`
- `references/common/ja-jp/entrusted-transactions.md`
- `references/common/ja-jp/consumer-electronic.md`
- `references/common/ja-jp/competition-ip.md`

を読む。binding law、official guidance、internal playbookを別欄にする。日本法有資格者review statusは`pending`。

## Handoff

review完了後、候補を提示するが自動writeしない。

- `escalation-flagger`: authority超過findingごとのdraft
- `renewal-tracker`: exact renewal candidate
- `stakeholder-summary`: internal/sanitized summary
- deviation record: accepted positionを人が確認した場合だけ
- privacy DPA review: 旧参照label`/privacy-legal:dpa-review`

multiple approverを1件に潰さず、全targetをreconcileする。
deviation handoffと別途導入される`deal-debrief`互換flowは
`references/automation-contract.md`を読む。

## Signature/redline gate

相手方へのredline、signature envelope、countersignature、risk acceptance前に、current user role、attorney review、approver、destination、final item/versionを確認する。

native Word tracked changesを生成・適用したとは主張しない。提供できるのは:

- clause-by-clause change table
- deletion/insertion text
- clean replacement language
- comment-ready rationale

相手方への送信は人が文書へ適用・確認後に別操作として行う。

## Completion

bottom line、issue counts、deal-breaker、approval route、missing documents、renewal candidate、save stateを示し、redline draft、escalation、facts、tracker、summaryから選んでもらう。

## 行わないこと

- hidden helperを別skillとしてinvoke/登録する
- signature、send、approve、renew/cancelを自動実行する
- unread DPA/URL termsを不存在として扱う
- unsupported native tracked changesを約束する
- local filesystem、agent、hook、subagentを使う
