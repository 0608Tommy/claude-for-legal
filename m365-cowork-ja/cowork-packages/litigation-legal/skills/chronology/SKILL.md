---
name: chronology
description: >
  指定matterまたは文書群から、event date、作成・送受信・提出・送達・知得・時効関連日を区別した日本語chronologyを作成・version更新する。sourceをde-duplicateし、甲乙号証等へpin citeし、秘密性確認済みの範囲だけを扱う。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Chronology

canonical label:
`/litigation-legal:chronology [slug] [--format=working|sof|witness-[name]]`

grammar compatibility:

- `--matter`
- `--documents`
- `--include-flagged`

`--include-flagged`は秘密性・提出制限を理解した明示acknowledgment後だけ。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。local folderを使わない。
2. exact user/profile、active binding、matter access、confidentiality/clean-team ACLを確認。
3. practice-level documents modeはfresh session・bindingなしで、pre-matter researchとして
   分離する。
4. sourceがdisclosure/production/court order/clean-teamから得られた場合、actual use
   restriction、protective order、court direction、purposeを確認する。
5. privilege/secrecy postureを人が選ぶまでextractしない。
6. 日本なら`references/common/ja-jp/evidence-confidentiality-preservation.md`
   と`civil-procedure-and-digital.md`を読む。
7. exact source item/version、language、translation、coverage、unreadを記録する。
8. quote/citation、artifact safetyは
   `references/common/source-provenance-and-review.md`とruntime contract。
9. draftとstate/version writeを分離し、gateway unavailableならread-only resultだけ。

## Privilege / confidentiality acknowledgment

次から選ぶ。

```yaml
confidentialityPosture: cleared | mixed | abort
```

- `cleared`: authorized reviewerが利用目的とsource restrictionを確認済み。
- `mixed`: entryごとに
  `clear | confidential | withholding-review | clean-team`を付け、external variantから
  flagged entryを除外。
- `abort`: source screening後に再開。

`--include-flagged`では、含めるcategory、audience、purpose、approverをoutput headerと
auditへ残す。

## Mode

- `--matter`: active matterのtheory、pivot fact、authorized sourceから作る。
- `--documents`: exact ad-hoc setから作り、matter factを補完しない。
- `--format=working`: complete internal chronology。
- `--format=sof`: external advocacy候補。flagged sourceを既定で除外。
- `--format=witness-[name]`: named personがsender/recipient/attendee/subjectのevent。

## Extraction fields

```yaml
eventId: "[stable ID]"
event_date: "[date or range]"
document_created_at: "[timestamp or null]"
sent_at: "[timestamp or null]"
received_at: "[timestamp or null]"
filed_at: "[timestamp or null]"
effective_service_at: "[timestamp or null]"
knowledge_or_accrual_date: "[date or null]"
limitation_event: "[event/basis or null]"
calendar_system: Gregorian | Japanese-era
event: "[fact]"
legal_significance: "[separate analysis]"
significance: key | relevant | background
confidentiality: clear | confidential | withholding-review | clean-team
sources: []
```

dateが矛盾する場合、1つに決めず両sourceと不一致を記録する。document date、
filing date、effective service、knowledge/accrualを混ぜない。

## Workflow

1. exact matter/theory/side、date range、purposeを確認。
2. source inventoryを作る。SharePoint matter item、mints/court document、email/export、
   eDiscovery等。connectorはlive probe成功後だけconnected。
3. sourceごとにmetadata、language、translation review、restrictionを記録。
4. dated eventを抽出。sourceにないeventをinventしない。
5. same eventをde-duplicateし、複数sourceへmerge。
6. factとlegal significanceを分離。
7. side/theoryに対するsignificanceを`key | relevant | background`でfirst-pass tag。
   borderlineは`[review]`。
8. limitation/deadlineはcurrent official sourceとtriggerを別recordで計算し、timeline
   factへsilentに埋め込まない。
9. prior versionがあればstable IDでdiffし、new/changed/removedを示す。removedは理由。
10. draft表示後、exact source/versionとsave destinationを確認。

## Output

```markdown
> **⚠️ レビュー担当者向け注記**
> [common block]

# Chronology — [matter / document set]

**Mode:** matter | documents
**Format:** working | sof | witness-[name]
**Built:** [ISO-8601]
**Version:** [N]
**Sources:** [N]
**Entries:** [N]
**Confidentiality posture:** cleared | mixed
**Included flagged categories:** [none/list]

| Event date | Created / sent / received | Filed / effective service | Event | Significance | ACL | Sources |
|---|---|---|---|---|---|---|
| [date] | [timestamps] | [timestamps] | [fact] | key/relevant/background | [class] | [甲第1号証3頁; item/version] |

## Key events
[fact、source、theory tieを分ける]

## Contradictions
[conflicting dates/facts]

## Gaps
[missing period、custodian、system、unread item]

## Limitation / deadline candidates
[separate candidate IDs; auto calendarなし]

## Version diff
[new/changed/removed]
```

Markdown/CSVはsafe renderingする。XLSXはapproved tenant rendererがある場合だけで、
native Office featureを保証しない。

## Completion

entry counts、key/relevant/background、flagged、unread、date conflicts、version、
save stateを示し、次から選んでもらう。

1. SoF skeleton draft
2. witness-specific view
3. missing source acquisition
4. deadline verification
5. other

## 行わないこと

- contradictionの解消、privilege/withholding final call
- source外eventの生成
- US discovery frameworkの日本への適用
- automatic calendar、filing、production、sharing
- local filesystem、agent、hook、subagent
