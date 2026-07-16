---
name: status
description: >
  clinic matterの同じfactsからclient、internal、court、agency向けstatusを別artifactとして作る。plain-language-letters helperのsubstantive intentを統合し、client-safe draft、internal memo、tracker、filing draftを分離する。deadline candidate、source provenance、日本の守秘 caveat、responsible lawyer reviewを明示し、送信・提出・case closeを行わない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: direct
  logical-target-id: ja-jp.cowork.legal-clinic.status
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Status

canonical label: `/legal-clinic:status [client | internal | court | agency]`

`plain-language-letters` helperのsubstantive branchを本skillへflattenしている。routine
appointment/document-requestは`client-letter`へrouteする。

## Mandatory audience / artifact / review gate

1. `references/common/cowork-runtime-contract.md`を読み、exact user、active non-null
   expiring matter binding、conflict/engagement/scope、responsible lawyer、ACLを確認する。
2. audienceとdestinationを`client | internal | court | agency`で確定し、ambiguousなら
   external artifactを作らない。
3. exact facts/source item versions、communication records、deadline recordsを読む。
4. deadlineは`candidate | verified`を表示し、candidateをcalendar fact又はclient promiseに
   しない。
5. client、court、agency向けはexact artifact version/hashへのresponsible lawyer review
   必須。internalもstudent assessmentとlawyer judgmentを分ける。
6. 日本の守秘・提出拒絶等を米国型privilege/work productと同一視しない。
7. identity、safe contact、health、immigration、criminal、child/family/DV、
   interpreter dataをaudienceに必要な最小限へsanitizationする。
8. draft、approval、output promotion、send/post/file/service/calendar/closeは別operation。
9. Cowork内DLPが必須ならconfidential matterを投入しない。
10. `criminal | immigration | housing | benefits`はapproved current source cardなしに
    substantive status、eligibility、deadline、formを生成せず、safety/emergency/
    specialist routingだけ。
11. consequential translationはresponsible-lawyer legal reviewとcompetent-language
    reviewの両方を同じartifact version/hashに要求する。

## Audience

### `client`

`client-safe-draft`:

- what happened、exact verified date/source
- what happens next
- what client needs to do
- candidate vs verified deadline
- safe contact、language/interpreter/accessibility
- scopeとresponsible lawyer

internal legal analysis、weakness、credibility、conflict、accepted risk、守秘評価を除く。
bad news、scope change、legal advice、settlement、case closingはresponsible lawyerが
content/communication planを決める。

### `internal`

`internal-memo`:

- procedural/agency posture
- actions since last review with exact evidence
- verified/candidate deadlines
- evidence/document gaps
- student assessment clearly labelled
- questions/decisions for responsible lawyer
- conflict/engagement/scope、privacy、retention/preservation

student assessmentをAIのconclusionとして埋めない。

### `court`

`filing-draft`。current Japanese form、case-specific order、court、case number、
submission regime、signature/representation authorityを確認する。日本で不要な米国型
caption、certificate of service、`court-ready` labelをdefaultにしない。fileしない。

### `agency`

courtと別artifact。agency、disposition、remedy、statutory form、submission method、
deadline、attachments、representative authorityを確認する。civil court templateを
流用しない。

## Source and review note

各artifactにsource items/versions、read coverage、authority layer/effective date、
deadline status、unresolved `[review]`、destination/ACL、DRAFT legal review statusを
1blockで示す。外部版へinternal noteを残さない。

## Plain Japanese / translation

client artifactはやさしい日本語を参考に、短文、明確なaction、必要な法律用語の説明を
使う。英語grade-levelを機械適用しない。重要なtranslated statusはlegal reviewと
competent-language reviewの両方がapprovedになるまで外部利用しない。

## Consequential action

send/file前に人がfinal version/hash、responsible lawyer approval、destination、
safe-contact、attachments、deadline/source、retention/DLPを再確認する。本skillは
Outlook、Teams、mints、agency portalを操作せず、communication logへ自動追加しない。

## 行わないこと

- audience間のautomatic copy
- client advice、settlement、scope、case closeの決定
- candidate deadlineを確定日又はresponse promiseとして表示
- internal privilege/conflict assessmentをexternal artifactへ含める
- U.S. certificate/service/filing practiceの日本移植
- send/post/file/sign/serve/calendar/accept/decline/close
