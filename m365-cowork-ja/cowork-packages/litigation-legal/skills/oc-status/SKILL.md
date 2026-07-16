---
name: oc-status
description: >
  active matterごとに、mints、effective service、court-set deadline、争点・証拠整理、文書命令、証人・号証、保全・執行、時効、settlement authority、budgetを尋ねる外部弁護士status email draftを作るPower Platform front end。送信しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: power-platform
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Outside counsel status draft

canonical label:
`/litigation-legal:oc-status [--all | --slug=foo | --no-gmail]`

`--no-gmail`はsource compatibilityとして保持する。本skills-only packageはGmail/
Outlook draft creationやsendを提供せず、safe email text draftだけを作る。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。
2. exact user/profile、authorized matter scope、outside counsel recipient、engagement、
   destination/privilege circleを確認。
3. each matterのlatest state/event/deadline versionを読む。
4. Japanならcivil procedure、evidence、demand/currency modulesを読む。
5. deadline candidateをcalendar済み・verifiedと誤表示しない。
6. clean-team/restricted/hold/evidence detailをneed-to-knowに削る。
7. gateway unavailableならread-only draft。state/cursor updateを主張しない。
8. AIはemail send、Outlook/Gmail draft creation、Teams postを行わない。

## Filter

default:

- active matter
- outside counsel firm/leadあり
- last update >10日、またはactive candidate/hearing within 21 days

flags:

- `--all`
- `--slug=[slug]`
- `--no-gmail`

recipient email欠落でもtext draftは作れるが、宛先未確認をflagする。

## Per-matter questions

- court、division、case number
- mints filing、notification、effective service timestamp
- next court-set submission/hearing、legal/order basis
- issue/evidence organization stage
- outstanding document order/evidence request
- witness/party examination、陳述書、exhibit work
- provisional remedy / execution
- limitation/tolling/completion postponement
- settlement authority、confidentiality basis
- budget、next phase、variance
- decisions/facts needed from client

blanket`Privileged / work product` labelを自動付与せず、actual relationshipと日本の
protectionを確認する。内部tracking headerとoutgoing email bodyを分ける。

## Draft

```markdown
> **⚠️ レビュー担当者向け注記**
> [common block]

# OC status request draft — [matter]

**To:** [verified recipient]
**Subject:** [house convention]
**Source state version:** [...]

---

[lead name]

[one-line opener]

1. 手続・mints・送達
2. 裁判所指定期限・次回期日
3. 争点・証拠・文書命令
4. 証人・号証・保全/執行
5. 時効・和解・意思決定
6. budget / next phase

[signoff]
```

external bodyの後にinternal send checklistを別blockで置き、copy前にstripする。

## State / automation

draft saveは`oc-status-draft` conditional create。scheduled behaviorは
`references/common/power-platform-automation-contracts.md`のapproved flow
version/owner/last runが確認できる場合だけ表示する。本skillはrecurrenceを作らない。

## Completion

processed/skipped matters、recipient gaps、deadline verification gaps、draft IDs、
save/audit resultを示す。

## 行わないこと

- email/draft/send/Teams postの自動実行
- blanket privilege claim
- deadline calendar
- restricted detailの過剰共有
- history rewrite
- local filesystem、agent、hook、subagent
