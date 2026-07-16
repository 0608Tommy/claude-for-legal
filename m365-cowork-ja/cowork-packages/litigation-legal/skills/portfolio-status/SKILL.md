---
name: portfolio-status
description: >
  authorized litigation portfolioをread-onlyでroll upし、risk、手続類型、複数deadline candidate、mints/service、staleness、conflicts、preservation、appeal・execution、OC gapを表示する。candidate deadlineをcalendar entryにせず、restricted matterの存在を漏らさない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Portfolio status

canonical label:
`/litigation-legal:portfolio-status [--all | --risk=high | --stale]`

additional source filters:

- `--risk=critical|high|medium|low`
- `--type=employment`
- `--owner=[name]`

本skillはread-only。state、cursor、deadline、matterを更新しない。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。
2. exact user/profileとauthorized practice scopeを確認。
3. matter listはACL-filtered query。unauthorized restricted/clean-team matterの存在も
   漏らさない。
4. exact state version/cursorでmatter、deadline、preservationを読むがcursor更新しない。
5. Japanならcivil procedure、evidence、currency、source registerを読む。
6. candidate deadlineをverified/calendar済みと表示しない。
7. public judgment databaseのquiet resultをquiet docketと解釈しない。
8. 10件超ならdashboardを提案するが自動生成しない。
9. Cowork DLP mandatoryならconfidential portfolio outputを停止。

## Rollup

- active/archived counts
- risk distribution
- proceeding type / court / record regime
- deadlines by 14/30/60 days:
  statutory invariable / extendable / court set / contractual / limitation / internal
- unverified trigger/service/authority
- next hearing
- stale >30 days
- conflicts pending/not-run/override
- high/critical without OC
- materiality/reserve staleness
- preservation:
  none / assessment / active internal control / formal evidence preservation /
  specific order / refresh due / release unresolved
- confidentiality/clean-team ACL anomaly
- appeal/finality/execution
- missing required fields

source `stage` valuesはimport compatibilityで表示できるが、日本のordinary civilを
US pleadings/discovery/MSJ/trial stageだけで分類しない。

## Output

```markdown
> **⚠️ レビュー担当者向け注記**
> [common block]

# Portfolio status — [timestamp]

**Authorized active matters:** [N]
**Deadline candidates inside 14 days:** [N]
**Unverified service/authority:** [N]
**Stale matters:** [N]

## By risk / procedure
[tables]

## Deadline candidates
| Matter | Class | Trigger/service | Authority | Candidate | Lawyer | Docket owner | Calendar |
|---|---|---|---|---|---|---|---|

## Preservation / confidentiality
[counts and authorized flags]

## Appeal / finality / execution
[table]

## Anomalies
[overdue candidate、stale、conflicts、OC、missing field、ACL]
```

`calendar_entry_id: null`なら`not calendared`。lawyer/docket owner verificationが両方
あっても、calendar writeはseparate approved operation。

## Docket automation

`references/common/power-platform-automation-contracts.md`を読む。reader、deadline
mapper、tracker writer、deliveryを分離し、flow/version/last runが確認できない場合は
scheduled monitoringが動くと表示しない。

## Completion

counts、highest priority candidate、verification gap、stale/restricted omission、
automation statusを示し、次から人に選んでもらう。

1. matter briefing
2. deadline verification packet
3. OC status draft
4. authorized dashboard
5. other

## 行わないこと

- state/cursor/calendar update
- unauthorized matter existence disclosure
- US discovery/hold stageの日本への移植
- outcome prediction
- scheduled flowの存在を推測
- local filesystem、agent、hook、subagent
