---
name: memo
description: >
  clinic studentの法的分析を支える内部memo scaffold。日本向けに結論、issues、applicable authority、facts/evidence、application、counterarguments、procedure/deadlines、open questionsを構造化し、IRACはpedagogyとしてのみ利用する。受任判断、client advice、外部文書を作らず、source provenanceとstudent analysis blockを残す。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: direct
  logical-target-id: ja-jp.cowork.legal-clinic.memo
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Memo

canonical label: `/legal-clinic:memo [issue]`

## Mandatory internal-only / pedagogy gate

1. `references/common/cowork-runtime-contract.md`と
   `references/common/source-provenance-and-review.md`を読む。
2. exact user、active non-null expiring matter binding、conflict/engagement/scope、
   responsible lawyer、authorized internal ACLを確認する。
3. memoは`internal-memo`。client、opposing party、court、agencyへ配布しない。
4. 日本の守秘・提出拒絶等を米国型privilege/work productと同一視せず、headerで
   保護が生じると表示しない。
5. current official Japanese sourceとfuture-lawを分け、citation、quote、deadline、
   user premiseを検証する。source unavailableならgapを残す。
6. `Take/Decline`又は受任recommendationをAIが決めない。
7. application、professional judgment、conclusionはstudentとresponsible lawyerの仕事。
8. destination、retention、internal preservation control、court order、DLPを確認する。
9. `criminal | immigration | housing | benefits`はapproved current source cardなしに
   substantive rule/applicationを生成せず、facts、urgency、research/referral gapsだけ。
10. student、AI/cloud又はinternal headerが日本の弁護士と同じ守秘/拒絶保護を自動的に
    得るとは表示しない。

## Pedagogy

- `guide`: issue/source/fact structureを作り、studentがrule/application/conclusionを書く。
- `assist`: frameworkとsource-backed propositionを作れるが、student analysisとfinal
  conclusionを明示してreviewさせる。
- `teach`: studentが先にissue/rule/applicationを作り、AIはquestionとfeedbackだけ。

IRACを使う場合も日本法のrequired formatとは呼ばない。

## Workflow

### 1. Frame issues

抽象labelでなく、facts、forum、remedy、procedural postureを含むquestionにする。
cross-area、conflict、scope、capacity、deadline、evidence gapもissue候補として示す。

### 2. Source map

1. official Japanese law/rule
2. case-specific order/document
3. professional rule/guidance
4. responsible lawyer approved source
5. secondary lead

各propositionにauthority type、official URL、effective/as-of date、retrieval、supportを
付ける。裁判所裁判例検索のnegative resultをcase absenceとしない。

### 3. Scaffold

```text
Conclusion candidate — student/lawyer to complete
Issues
Applicable authority and source status
Facts and evidence with exact cites
Application — STUDENT ANALYSIS
Counterarguments / adverse facts
Procedure and deadline candidates
Open factual, legal, strategic questions
```

source未取得は`[RESEARCH NEEDED]`、fact欠落は`[FACT NEEDED]`、subjective callは
`[review]`。AIがconfidenceだけでtagを外さない。

### 4. Strengths / weaknesses

fact/sourceに結び付けてcandidateとして示す。client credibility、capacity、criminal
exposure、immigration risk等を根拠なく結論にしない。上流severityをsilentに下げない。

### 5. Deadline and procedure

deadlineはexact deadline record IDを参照し、`candidate | verified`を明示する。
candidate dateをcalendar factにしない。urgent candidateはresponsible lawyer/docket routeへ
escalateするが、response又はreliefを約束しない。

## Output

1. reviewer note
2. internal confidentiality caveat
3. scope / forum / responsible lawyer
4. issue questions
5. source-backed scaffold
6. student analysis/conclusion blocks
7. unresolved facts/sources
8. deadline candidates
9. next options

client-safe explanation又はfiling draftが必要なら別artifactを別skillで作り、新しい
sanitization/reviewを行う。

translated legal conclusion又はdeadlineを外部artifactへ移す場合、responsible-lawyer
legal reviewとcompetent-language reviewの両方を要求する。

## 行わないこと

- client advice、受任/decline、strategy、settlementの決定
- unverified citation又はquoteの創作
- IRACを日本の法的要件として表示
- internal memoをclient/court/agencyへ自動転用
- send/post/file/calendar/close
