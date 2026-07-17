---
name: matter-briefing
description: >
  1件のmatterについて、手続類型、裁判所・事件番号、mints・送達、複数deadline、証拠、秘密保持、保全、控訴確定、執行、最近のeventをread-onlyでbriefingする。stalenessと再評価質問を示すがstateを変更しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Matter briefing

canonical label: `/litigation-legal:matter-briefing [slug]`

本skillはread-only。matter/event/deadlineを更新しない。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。
2. exact user/profile、active unexpired binding、matter `status: active`、ACLを確認。
3. exact matter、event、deadline、preservation、evidence state versionを読む。
4. Japanなら
   `references/common/ja-jp/civil-procedure-and-digital.md`、
   `evidence-confidentiality-preservation.md`、`currency-watch.md`を読む。
5. current deadlineはauthority/trigger/service/calculation/verificationを確認し、
   candidateを確定日と表現しない。
6. clean-team/hold/evidence restricted factsはauthorized audienceだけ。
7. coverage/failure/source versionをreviewer noteへ記録。
8. Cowork DLP mandatoryならconfidential briefingを停止。

## Read

- source compatibility matter fields
- Japan procedure fields
- latest 3～5 event records
- all active deadline candidates
- evidence register summary
- confidentiality/court order
- preservation status
- provisional remedy / appeal / execution
- outside counsel and internal owner
- conflicts/access status

## Output

```markdown
> **⚠️ レビュー担当者向け注記**
> [common block]

# [Matter] — briefing as of [timestamp]

**Matter ID:** [...]
**Proceeding:** [proceedingType]
**Court / case number:** [...]
**Record regime / mints:** [...]
**Status / stage:** [...]
**Risk / materiality:** [...]
**Last updated:** [...] [STALE if >30d]
**Conflicts / access:** [...]

## One-paragraph posture
[our/their position、pivot、current procedural posture]

## Recent changes
[latest events with source item/version]

## Deadlines and hearings
| Candidate | Class | Trigger/service | Authority | Date | Verification |
|---|---|---|---|---|---|

## Evidence / confidentiality
[register coverage、orders、withholding review、gaps]

## Preservation
[internal control / formal evidence preservation / specific duty]

## Provisional remedy / appeal / execution
[actual status]

## Risk and materiality re-check
[questions, not decisions]

## Open questions for the conversation
[purpose-tailored]
```

`calendar_entry_id: null`のcandidateはcalendar済みと書かない。public judgment searchの
quiet resultをquiet docketと解釈しない。

## Completion

staleness、deadline verification gaps、evidence coverage、preservation、appeal/
execution、restricted omissionsを示し、次から人に選んでもらう。

1. matter update draft
2. counsel status request draft
3. missing source/deadline verification
4. escalation brief
5. other

## 行わないこと

- outcome prediction / strategy decision
- state update
- calendar entry
- unauthorized restricted fact disclosure
- local filesystem、agent、hook、subagent
