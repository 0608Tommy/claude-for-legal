---
name: legal-hold
description: >
  日本案件のinternal preservation controlをissue、refresh、release、statusの会話stateで扱うPower Platform front end。証拠保全やspecific legal dutyと区別し、statusはread-only、変更はversioned record・restricted ACL・fresh approvalで行う。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Legal hold / internal preservation control

canonical label:
`/litigation-legal:legal-hold [slug] [--issue | --refresh | --release | --status]`

canonical IDと`legal-hold`用語を保持するが、日本modeでは法定義務と自動同一視しない。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読み、gateway、state、matter、
   hold/evidence ACL、auditをlive preflightする。
2. `--status`はread-only。gateway write capability、item/eTag、confirmationを要求しない。
3. issue/refresh/releaseはexact user/profile、active binding、matter access、authority、
   retention、DLPを確認。
4. Japanなら
   `references/common/jurisdictions/ja-jp/evidence-confidentiality-preservation.md`と
   `source-register.md`を読む。
5. basisを
   `internal-control | CCP-234 | court-order | sector-rule | contract |
   foreign-proceeding | other`
   から分類し、actual legal basisをcurrent official sourceで確認。
6. hold roster、custodian identity、evidence registerをrestricted ACLへ置く。
7. draft、state update、notice issue/release、system deletion suspensionを別operation。
8. AIはnotice送信、IT change、collection、releaseを実行しない。

## Required wording

internal notice:

> これはLegalが承認した内部preservation instructionです。

actual basisがない限り「法律が保存を要求する」と書かない。6か月refreshは
configurable internal policyで、statutory intervalではない。

## `--status` — read-only

slugあり: 1 matter。slugなし: authorized portfolio。

表示:

- draft/active/released
- basis typeとexact citation
- issued/last refresh/next refresh
- pseudonymous custodian count
- source systems / auto-delete status
- departed custodian/collection gap
- release blocker

state、cursor、last checkedを更新しない。0件でもwriteしない。

## `--issue`

1. trigger factsとbasisを確認。
2. scope、date range、custodian pseudonymous IDs、systems、ongoing collection、
   auto-delete suspension proposalを作る。
3. `internal-control`とformal evidence preservationを混同しない。
4. draft noticeとstate diffを表示。
5. qualified counsel、authorized issuer、IT/records owner、destinationを確認。
6. fresh approval後、`preservation-control`を`expectedAbsent: true`でconditional create。
7. notice deliveryは別operationのまま停止。

noticeはexternal custodian-facing versionとinternal scope/analysisを分ける。

## `issue-confirmed`

draft holdを`active`へ変更する別operation。

1. exact notice artifact item/version/hash。
2. custodianごとのdelivery receiptとacknowledgment status。
3. IT/records ownerごとのauto-delete suspension、collection、failure。
4. undelivered/failed recipientとremediation。
5. qualified counsel/issuerのfresh confirmation。
6. `hold-custodian` recordを1 custodian = 1 recordでcreate/update。
7. 全required delivery/IT actionを検証後だけpreservation controlを`active`へupdate。

delivery/acknowledgment/IT actionの証拠なしに`active`と表示しない。

## `--refresh`

exact current record/item/eTag/versionを読む。

- new/removed custodians
- new systems/topics/date range
- departed employee handling
- collection/integrity gaps
- active court/order/retention changes
- next internal refresh

exact diffとimpactを示し、fresh confirmation後にversioned update。past versionを
overwriteしない。refresh noticeのsendは別operation。

## `--release`

release前に:

- proceeding終了だけでなくappeal/finality/execution
- related claim / limitation
- court order / regulator / contract / foreign proceeding
- retention policy
- evidence register / shared link
- partial releaseの可否

を確認。release authorityとqualified counsel reviewがない場合block。

releaseはpreservation control stateのupdate候補を作るだけ。custodianへのrelease
notice送信、normal deletion再開、system setting変更を実行しない。

## Record

`references/common/litigation-record-schemas.md`の`Preservation control`を使う。

```yaml
mode: issue | refresh | release | status
status: draft | active | released
nextRefreshAt: "[ISO-8601 or null]"
```

source canonical fields `issued`, `issued_date`, `scope`, `custodians`,
`last_refresh`, `next_refresh`, `released`はimport compatibilityとして保持し、
Japan basis fieldsを追加する。

## Completion

mode、basis、scope/custodian counts、version、ACL、unresolved blocker、write/audit
resultを示す。

## 行わないこと

- status branchでwrite
- Rule 37(e)/Zubulakeを日本法として使用
- notice send、IT deletion suspension、collection、release
- 6か月を法定intervalと表示
- unrestricted custodian list
- local filesystem、agent、hook、subagent
