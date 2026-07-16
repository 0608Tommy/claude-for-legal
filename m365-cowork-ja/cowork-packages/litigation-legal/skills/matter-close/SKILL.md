---
name: matter-close
description: >
  settlement、判決、取下げ、請求放棄・認諾、控訴、確定、執行、preservation dispositionを確認してmatterをarchiveするPower Platform front end。source outcome tokenを保持し、matterをfenceしてactive session bindingだけをrevokeし、deleteしない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Matter close

canonical label: `/litigation-legal:matter-close [slug]`

closeはdeleteでなくarchive。`matter-workspace close`と同じarchive semanticsを使い、
folder moveをしない。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読み、gateway、matter/state/audit、
   atomic matter fence、all-binding query、conditional revokeをlive preflight。
2. exact user/profile、target matter、latest item/eTag/version、authorityを確認。
3. exact matter preconditionとcurrent `bindingGeneration`を確認し、new binding createを
   fenceできないgatewayではcloseを開始しない。
4. Japanなら
   `references/common/jurisdictions/ja-jp/civil-procedure-and-digital.md`、
   `demands-limitation-settlement.md`、`evidence-confidentiality-preservation.md`を読む。
5. settlement、judgment、appeal/finality、execution、related matter、preservation/
   retentionをexact sourceで確認。
6. close reason、date、approver、downstream effect、ACLを示す。
7. fresh confirmation後だけconditional updates。
8. AIはsettlement acceptance、appeal waiver、execution、preservation release、
   deleteを実行しない。

## Outcome

source compatibility:

```yaml
outcome: settled | dismissed | judgment-for-us | judgment-against-us | withdrawn | consolidated | other
```

Japan detail:

```yaml
outcomeDetailJP: private-settlement | court-settlement | judgment-rendered | judgment-final | withdrawal | abandonment-or-acceptance | appeal-pending | execution-complete | consolidated | other
```

`dismissed with/without prejudice`を日本の手続へ翻訳適用しない。importされた
`dismissed`はraw source tokenとして保持し、actual Japan dispositionを別fieldで確認。

## Close checklist

- exact final/settlement/order item/version
- private settlementかcourt settlementか
- judgment rendered / served / appeal period / finality
- 労働審判異議、appeal、related proceeding
- payment/structural obligation、execution status
- costs/fees/reserve/materiality
- open deadline candidate
- evidence/record retention
- preservation control: continue / partial release / release approved / unresolved
- shared links、outside counsel、internal owner
- lessons（user-provided。AIがinventしない）

preservation releaseは`legal-hold --release`の別operation。close confirmationをrelease
approvalに拡張しない。

`appeal-pending`、open deadline、execution未了、preservation `continue` /
`partial-release` / `unresolved`のいずれかがある場合、matterをarchiveしない。
live workとresidual preservation scope、exact deadline/evidence/preservation
referenceをauthorized successor active matterへ
移管し、人が移管を確認した場合だけ元matter closeを再評価する。archived matterで
通常のappeal updateまたはhold refreshを続ける設計にしない。

## Update sequence

1. exact diffを表示。
2. fresh approval。
3. 最初のatomic conditional operationでmatterを`close-pending`等のnon-active
   stateへtransitionし、`bindingGeneration`を増やしてnew binding createをfence。
4. fence成功後、target matterの全bindingをexact query。
5. activeだけをrevocation対象とし、already-revokedはsatisfiedとして再更新しない。
6. active bindingだけをexact item/eTagで`revoked`へconditional updateし、each
   resultをcanonical auditへappend。
7. 全bindingを再照合し、zero activeを確認。
8. zero active確認後だけpost-fence matterを`status: archived`へconditional
   finalizeし、close fieldsをversion追加。
9. fence前にcommitしたcreateはstep 4で捕捉され、fence後のcreateはexact matter
   precondition/generationで失敗。
10. revocation/finalize failureはfenced stateを維持し、block eventとsubstantive
    access拒否。close summaryはreview済みoutput候補。retention deleteはscope外。

## Record

`references/common/litigation-record-schemas.md`のCloseを使う。

```yaml
status: archived
bindingGeneration: "[fenced generation]"
resolutionAt: "[ISO-8601]"
finalityAt: "[ISO-8601 or null]"
preservationDisposition: continue | partial-release | release-approved | unresolved
```

source `status: closed`, `closed`, `outcome`, `final_cost`, `last_updated`は互換fieldとして
保持できるが、canonical target statusは`archived`。

## Completion

matter ID、outcome/detail、finality、appeal/execution、preservation disposition、
revoked binding count、failures、new eTag/version、audit IDsを示す。

## 行わないこと

- delete
- settlement/appeal/preservation releaseの自動決定
- current bindingだけのrevoke
- archive-first / revoke-every close
- same-session substantive continuation
- US dismissal semanticsの移植
- local filesystem、agent、hook、subagent
