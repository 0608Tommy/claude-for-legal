---
name: draft
description: >
  日本のclinic matterについて、責任弁護士が承認したcurrent form・事件固有命令・precedentからclient、court、agency向けの未送信・未提出draftを作る。form-generation helperをlegacy utterance aliasとして統合し、pedagogy mode、missing facts、source/effective date、artifact separation、version-specific lawyer reviewを強制する。署名・送信・提出しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: direct
  logical-target-id: ja-jp.cowork.legal-clinic.draft
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Draft

canonical label: `/legal-clinic:draft [document-type]`

legacy `form-generation` utteranceは本skillへrouteする。別skillを登録しない。

## Mandatory matter / source / filing gate

1. `references/common/cowork-runtime-contract.md`を読み、exact user、active non-null
   expiring matter binding、conflict/engagement/scope、responsible lawyer、authorized ACLを
   確認する。
2. 別client/matterはfresh sessionでswitchする。過去matterのfacts、quote、draft、
   cursorをcarryしない。
3. document audienceを`internal | client | court | agency`、forumを
   `civil | criminal | administrative | family | labor | other`で確定する。
4. responsible lawyerが承認したcurrent official form、事件固有order、clinic
   precedentを優先する。criminal/administrative documentをcivil templateから作らない。
5. legal assertion、deadline、service、filing method、formatはcurrent official source、
   effective date、transitionを確認する。取得不能ならflag又は停止。
6. missing factをguessせず`[FACT NEEDED: ...]`。subjective judgmentは`[review]`。
7. identity、contact、health、immigration、criminal、child/family/DV、My Numberを
   mask/minimizeし、必要なrestricted referenceだけを使う。
8. draft、responsible lawyer review、SharePoint output promotion、signature、send、
   filing、serviceは別operation。本skillは外部actionを行わない。
9. filing/client artifactはexact version/hashにlawyer approvalが必要。
10. Cowork内DLPが必須ならconfidential matterを投入しない。
11. `criminal | immigration | housing | benefits`はapproved current source cardなしに
    substantive draft、eligibility、deadline、formを生成せず、issue/safety/referral
    checklistだけ。
12. consequential translationはresponsible-lawyer legal reviewとcompetent-language
    reviewの両方を同じartifact version/hashに要求する。

Japan:
`references/common/ja-jp/procedure-deadlines.md`、
`references/common/ja-jp/clinic-law-and-supervision.md`。

## Pedagogy mode

practice-area guideの`assist | guide | teach`。

- `guide`: structure、required facts、source checklistを示し、studentがsubstanceを作る。
- `assist`: review用draftを作り、studentがfacts、law、strategy、formatを検証する。
- `teach`: student draftへSocratic feedbackし、初回から完成文を出さない。

modeはlawyer gate、no-file、no-sendを変えない。

## Workflow

### 1. Document fit

document titleだけでなく目的、forum、audience、procedural posture、requested relief、
deadline、responsible lawyer、approved formを確認する。approved templateがない場合、
generic structureとして重くflagし、official form又はlawyer precedentを求める。

日本向け例:

- internal case note、research memo
- client letter / explanation draft
- 訴状、答弁書、準備書面、申立書、陳述書
- 審査請求書等のagency draft

`court-ready`と呼ばず`court-or-agency draft`。

### 2. Fact/source matrix

| required item | status | exact source |
|---|---|---|
| fact | verified / missing / disputed | item/version/page |
| authority | current / future / unavailable | official URL/effective date |
| procedural requirement | confirmed / review | order/rule/form |
| deadline | candidate / verified | deadline record ID |

exact passageを開いていないquoteを作らない。document、client、courtの言葉をparaphrase
する場合はsource cite pendingを示す。

### 3. Draft

OneDrive current-user draftとして生成し、次をmetadataへ置く。

- artifact type、matter ID、audience、forum
- source item IDs/versions、coverage
- DRAFT status
- unresolved facts/source/judgments
- destination/ACL
- required reviewer

AI review labelや`[VERIFY]`はinternal working copyに残す。外部版はlawyer review後、
unresolved flagsを解消し、内部analysisをstripした別artifactとして作る。

### 4. Japan-specific checks

- Japanese original、current law/rule/form
- party/client nameと事件番号のexact source
- mints/filing regime、legacy/transition
- signature/representation authority
- service/delivery requirement
- privacy、address secrecy、child/DV restriction
- 2026-04-01 family reform transition、DV protection orderの地方裁判所route
- child-abuse concernのhuman reporting route
- attachments/exhibits/originals
- deadline candidate vs verified

米国certificate of service、Bluebook、FRCP/ABA ruleをdefaultにしない。

### 5. Review package

responsible lawyerへ:

1. clean draft
2. separate reviewer note
3. fact/source matrix
4. unresolved `[review]`/`[VERIFY]`
5. exact artifact hash/version
6. destinationとrequested action

を渡す。approval後もsend/fileは別operation。

## Artifact separation

- student/legal analysis: `internal-memo`
- external client wording: `client-safe-draft`
- deadlines/status table: `tracker-record`
- court/agency wording: `filing-draft`

internal memoをclient又はfiling artifactへ直接copyしない。sanitizationとnew reviewを行う。

internal preservation instructionをFRCP型legal hold又は日本法上の一般的同等制度として
draftしない。法的根拠がある場合はexact statute/order/sourceを別に示す。

## 行わないこと

- final legal opinion又はcase strategyの決定
- missing fact/sourceの創作
- U.S. form、service、limitation、student-practice ruleの日本移植
- My Number又は不要なsensitive identifierの投入
- sign/send/post/file/serve/calendar/accept/decline/settle/close
- Word native tracked changes又はofficial form fidelityの未検証保証
