---
name: renewal-tracker
description: >
  SharePointのrenewal registerで契約更新、cancel-by、send-by、notice method、business ownerを管理する。次の90日または指定window、missed deadline、reviewからのingest、承認済みconnector syncを会話状態で扱う。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: commercial-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Renewal tracker

旧来の参照label:

- `/commercial-legal:renewal-tracker`
- `--days N`
- `--horizon N`
- `--missed`

Coworkではflagを実行せず、`days`と`horizon`を同じ`windowDays`へ正規化する。本skillはSharePoint / Power Platform stateのfront endであり、scheduled watcherまたはmanaged solutionを含まない。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を必ず読む。旧`renewal-register.yaml`やlocal calendarへwriteしない。
2. **Setup/user:** practice profile、current`user-profile`、business owner/authorityを読む。別userのroleを使わない。
3. **Matter/scope:** server bindingを確認する。renewal recordの`scopeType/scopeId`が一致しない場合は表示・更新しない。practice-level searchは権限あるscopeだけ。
4. **Jurisdiction:** `request > matter > practice-profile > tenant-default`。notice mechanics、business day、consumer/取適法/Freelance等が関係すれば`ja-JP`moduleを読む。
5. **Source:** exact contract clause、current term、notice method、incorporated terms、source item/versionを確認する。metadataだけでdeadlineを確定しない。
6. **Confidentiality:** register viewer、destination、retention、legal hold、保存境界DLPを確認する。
7. **Human review:** trackerはdecision support。renew/cancel、notice送信、late cancellation交渉、term更新を決定しない。
8. **Write:** 新規ingestはcanonical composite key、`recordId`、unique
   `idempotencyKey`による条件付きcreateを使い、返された`itemId`/`eTag`を
   保存する。既存recordのupdate/roll-forward/syncは1itemずつdiffを示し、
   exact`itemId`、latest`eTag`、unique`idempotencyKey`で確認後に実行する。
   duplicateまたはstale writeは停止する。

情報源tag、dashboard、irreversible gateは
`references/common/source-provenance-and-review.md`を使う。

## 会話state

| state | intent |
|---|---|
| `upcoming` | default next 90 days |
| `window` | `windowDays = N`で今後N日 |
| `missed` | passed send-byでcancel recordなし |
| `ingest` | review handoffまたはmanual record追加 |
| `show <recordId>` | exact recordとhistory |
| `update <recordId>` | 1fieldまたはconfirmed recalculation |
| `sync` | approved live connectorからcandidateを取得 |

`--days 180`と`--horizon 180`はどちらも`window`、`windowDays: 180`。両方が異なる値で指定されたら停止して1つを選んでもらう。positive integerでなければ再入力。

## Upcoming

urgencyは`send_by_effective - today`で計算する。half-open intervalで重複させない。

- 🔴 `0 <= days < 14`
- 🟠 `14 <= days < 45`
- 🟡 `45 <= days < windowDays`

default`windowDays`は90。day 14、45、90を2bucketへ入れない。negativeは`missed`。

表示:

| Record ID | Counterparty | Send by | Cancel effective by | Renewal | Annual value | Owner | Notice method | Notes |
|---|---|---|---|---|---|---|---|---|

summary counts、total annual exposure、uncapped price、missing owner/sourceを示す。10行超ならdashboardを提案する。

## Deadline calculation

`references/renewal-records.md`のschemaと手順を使う。

1. `current_term_end`
2. `notice_period_days`
3. raw`cancel_by_calendar`
4. contract-defined business day、governing-law holiday
5. `cancel_by_effective`
6. notice methodのtransit/receipt mechanics
7. `send_by_effective`

alertは`send_by_effective`。calculationは`[model calculation — verify against the notice clause]`を保持する。契約が`received by`、time-of-day、portal-only等を指定する場合、それがgeneric bufferより優先する。

calendarを確認できない場合、US holiday等をplaceholderとして使わず、jurisdiction calendar未確認で停止するかconservative candidateを`[verify]`で示す。

## Ingest

reviewからrenewalが渡されたらcandidate recordを示す。counterparty一致だけでduplicate判定せず、source contract item ID、agreement title、termを比較する。

既存recordがある場合:

- replacement/renewed agreement
- additional agreement
- duplicate

を人に選んでもらう。

## Rolling renewal

`initial_term_end`はhistoryとして保持し、future deadlineは`current_term_end`から計算する。window通過だけでauto-renewedと断定しない。actual renewal、notice absence、contract mechanicsを確認し、新termとdatesのdiffを示してから更新する。

## Missed

`send_by_effective < today`かつ`status: active`で、cancel/non-renewal eventがないrecordを表示する。

options:

- late cancellationを交渉するdraft
- renewalを確認し次期termを登録
- convenience/causeその他のtermination rightを`review`
- business owner/attorneyへescalate

AIはlate noticeをsendしない。

## Sync

Ironclad、DocuSign等がmanifestに登録済みとは限らない。live probe、administrator approval、least privilegeが確認できる場合だけcandidateを取得する。

- source-specific、scope-specific cursor
- exact source item ID
- active/executed status
- clause textまたはread-required flag

metadataだけのcandidateは`needs-contract-read`。bulk write前に件数、scope、duplicates、missing fieldsを示し、各itemまたは明示されたbatchを確認する。

scheduled renewal-watcher flowが存在する場合、flow definition/version、last run、scope、destinationをstateから表示できる。存在しない場合「毎週通知される」と言わない。

別途導入されるflowとの互換behaviorは
`references/automation-contract.md`を読む。

## Consequential gate

renewal accept/decline、non-renewal、termination notice、countersignatureの前:

- current user role
- attorney review
- exact clause/date/method
- approver
- destination

を確認し、draft noticeまでで停止する。人の明示確認なしにsendしない。

## 完了

window、scope、read count、missing source、urgent records、saved changes、scheduled flow statusを示す。`review`、`escalation-flagger`、business owner questionsから選んでもらう。

## 行わないこと

- contractをcancel/renewする
- noticeをsendする
- decisionをbusiness ownerの代わりに行う
- global cursorで別matterへ続行する
- schedule/notificationが存在すると推測する
- local calendar/registerへ保存する
