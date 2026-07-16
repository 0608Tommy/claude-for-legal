---
name: deal-team-summary
description: >
  diligence findings、schedule、closing candidateを、board/exec、deal lead、working teamのaudience別に集約し、severity floor、coverage、変化、Japan regulatory screen、decision itemsを保ったbriefをdraftする。自動配布・Teams投稿は行わない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: corporate-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Deal team summary

旧来の参照labelは`/corporate-legal:deal-team-summary`。

## 目的

大量findingを「何がmaterialか、前回から何が変わったか、誰のdecisionが必要か」
へ圧縮する。summaryはsource findingを置き換えず、exact sourceへ戻れるようにする。

## 必須gate

1. `references/common/cowork-runtime-contract.md`を読み、current user、scope、
   expiring binding、matter status、authorized viewerを確認する。
2. transaction structureを
   `share sale | business transfer | merger | company split | share exchange |
   share transfer | share delivery | other`
   から確認する。
3. exact source finding IDs/version、coverage、unread/missing、last brief versionを
   読む。summaryやmemoryだけから再要約しない。
4. upstream severityをfloorとして保持する。下げる場合、old/new、reason、
   reviewerを明記する。
5. audienceとdestinationを確認する。board/exec、deal lead、working teamで
   privilege/MNPI/clean-team detailを分ける。
6. 日本案件は
   `references/common/jurisdictions/ja-jp/ma-regulatory.md`と
   `references/common/jurisdictions/ja-jp/diligence-overlays.md`を読み、
   Companies Act、FIEA/TDnet、JFTC、FEFTA、labour、APPI、IP、licenceを
   applicableな範囲で示す。
7. law、listing、guidance、PA、internal thresholdを混同しない。
8. external/business-facing版からinternal legal analysis、accepted risk、
   privilege note、clean-team restricted factsを除く。
9. AIはsend/postしない。OneDrive draftとSharePoint outputs昇格を分ける。
10. Cowork内DLP必須ならproduction useを停止する。

provenanceとreviewer noteは
`references/common/source-provenance-and-review.md`を使う。

## 会話state

| state | action |
|---|---|
| `select-audience` | `board-exec | deal-lead | working-team`を選ぶ |
| `baseline` | first briefとしてcurrent stateを集約 |
| `delta` | last exact brief以降のnew/resolved/severity/status change |
| `decision-brief` | approver、deadline、optionsに絞る |
| `sanitized-external` | privilege/clean-team/MNPIを除いた別draft |

意図不明ならaudienceを確認する。

## Audience

| Audience | 含める | 省く |
|---|---|---|
| `board-exec` | top 3–5 material issues、deal impact、regulatory blockers、decisions | green detail、process、restricted detail |
| `deal-lead` | all blocking/high、progress、consents/filings、gaps、next 72 hours | low detail |
| `working-team` | full issue/status/source、owner、dependency | 権限外matter以外は省かない |

board/exec audienceでもmaterial uncertaintyを消さず、簡潔に`[review]`を残す。

## Delta

- new findings
- severity increase/decrease
- resolved/clarified
- coverage change
- new/missing documents
- JFTC/FEFTA/FIEA/licence screen change
- consent/approval/filing status
- critical path movement

`still N high`だけでなく、movementと原因を先に示す。

## Japan regulatory strip

applicableなものを別行で示す。

| Screen | Status | Deadline/wait | Evidence | Owner |
|---|---|---|---|---|
| Companies Act approvals | | | | |
| FIEA / EDINET | | | | |
| JPX / TDnet | | | | |
| JFTC | | | | |
| FEFTA | | | | |
| Labour / APPI / licence | | | | |

`not applicable`はfactsとsourceがある場合だけ。未確認は`unknown`。

## Output

`references/summary-output.md`のformatを使う。

mandatory:

- date、deal、transaction structure、audience
- source versionsとcoverage
- summary stats
- material findings
- regulatory/approval strip
- decisions needed、decision owner、due
- delta
- gaps
- next human choice

10行超のfinding/statusなら
`references/common/dashboard-template.md`に従うdashboardを提案するが、自動生成
しない。

## Handoff

pre-closing actionが見つかった場合、`closing-checklist`へcandidateを作る。
summaryから機械的にstate updateせず、source findingとdedupeを人がreviewする。

## 行わないこと

- materiality/severityをsilentに再決定
- incomplete coverageをcompleteと表示
- privilege/clean-team情報をbroader audienceへ移す
- board、Teams、emailへ自動送信
- regulatory clearanceまたはready-to-closeをcertify
