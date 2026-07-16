---
name: matter-update
description: >
  filing、effective service、order、hearing、evidence、settlement、preservation、judgment、finality、appeal、execution等のeventをappend-onlyで追加し、必要なmatter fieldをexact diffでversion更新するPower Platform front end。past eventを編集しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Matter update

canonical label:
`/litigation-legal:matter-update [slug] [brief event description]`

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読み、gateway、binding、ACL、
   append/create/update/auditをpreflight。
2. exact active matter、latest item/eTag/version、current user authorityを確認。
3. exact source item/version、event timestamp、service evidenceを確認。
4. Japanならcivil procedure、evidence、demand、currency modulesをissueに応じて読む。
5. deadline effectはofficial sourceとcase orderから別candidateとして作る。
6. settlement acceptance、preservation release、calendar、external sendは別operation。
7. past eventをeditしない。correctionはnew event。
8. gateway unavailableならproposed event/diffだけ。

## Event type

source compatibility:

```yaml
sourceEventType: Procedural | Discovery | Substantive | Strategy | Risk re-assessment | Stakeholder | Administrative
```

Japan detail:

```yaml
eventTypeJP: filing | effective-service | order | hearing | evidence | settlement | preservation | judgment | finality | appeal | execution | other
```

日本modeでは`Discovery` tokenをimport compatibilityに限定し、一般的US discovery stageと
して使わない。

## Capture

- event date/timeとrecorded time
- one-paragraph factual summary
- exact source item/version/hash
- legal significance（factと分離）
- filed/service/hearing/order/finality/execution effect
- field changes candidate
- materiality check
- deadline candidate create/update
- ACL/clean-team/hold impact

materiality re-checkを必須にするevent:

- merits/substantive ruling or key evidence
- settlement offer/acceptance
- risk reassessment
- regulator/enforcement
- provisional remedy / judgment / appeal / execution

`no-change`もexplicitに記録。

## Settlement / consequential gate

offer made/receivedのlogはできる。acceptance、agreement execution、release、payment、
withdrawal、filingはfresh qualified counsel approvalと別operation。AIはstateに
acceptedと書き込む前にapproval recordを要求する。

## Write sequence

1. `matter-event`をappend-only conditional create。
2. matter field changesがあればcurrent matterを再読取り。
3. exact diff、downstream deadline/ACL/materiality impactを表示。
4. event createとmatter updateを別confirmationにできるよう分離。
5. exact item/eTag/idempotencyでconditional update、version increment。
6. deadline candidateも別create/update。
7. partial successをitemごとにauditし、推測で継続しない。

## Output

```markdown
## [eventAt] — [eventTypeJP]: [short title]

**Facts:** [...]
**Legal significance:** [...] `[review]`
**Source:** [item/version]
**Field changes:** [old → new]
**Materiality check:** no-change | changed
**Deadline candidates:** [IDs / none]
**ACL/preservation impact:** [...]
```

## Completion

event ID、matter changes、deadline candidates、new eTag/version、partial failures、
audit IDsを示す。

## 行わないこと

- past event edit
- settlement acceptance/file/calendar/hold release
- scalar `next_deadline`だけのsilent update
- US discovery stageの日本への移植
- local filesystem、agent、hook、subagent
