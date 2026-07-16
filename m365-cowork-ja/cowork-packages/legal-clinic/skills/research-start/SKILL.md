---
name: research-start
description: >
  日本法のresearch roadmapを公式日本語原文から開始し、法令・裁判所規則・事件固有命令・裁判例・省庁guidance・JFBA rules・secondary sourceをlayer分けする。source URL、retrieval、effective status、current/future law、coverageを記録し、裁判所裁判例検索をcitator又は完全databaseと扱わない。leadであり最終authorityではない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: direct
  logical-target-id: ja-jp.cowork.legal-clinic.research-start
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Research start

canonical label: `/legal-clinic:research-start [issue]`

## Mandatory matter / source / current-law gate

1. `references/common/cowork-runtime-contract.md`と
   `references/common/source-provenance-and-review.md`を読む。
2. matter-specific researchではexact user、active non-null expiring binding、
   conflict/engagement/scope、ACLを確認する。general researchはfresh practice sessionで
   binding不在とし、matter factsを混ぜない。
3. issue、forum、jurisdiction、procedural posture、as-of dateを具体化する。
4. seed sourceはexact item/version、ACL、coverageを確認する。
5. current Japanese official text、effective date、transitionを優先し、future-lawを
   current conclusionへ使わない。
6. research connectorをlive probeし、実際に取得したsourceだけにprovenance tagを付ける。
7. exact textを開いていないquote、pinpoint、holdingを作らない。
8. outputはresearch roadmap/internal notes。client advice、filing、deadline verification
   ではない。
9. large inputはread coverageとunreadを示す。
10. Cowork内DLPがrequiredならconfidential matter sourceを投入しない。
11. `criminal | immigration | housing | benefits`はapproved source cardの更新又は作成を
    目的とするresearchに限定し、card approved前にsubstantive matter conclusionへ使わない。

Japan:
`references/common/jurisdictions/ja-jp/source-register.md`、
`references/common/jurisdictions/ja-jp/currency-watch.md`。

## Research hierarchy

1. 官報/e-Govのcurrent Japanese text、amendment、effective date。
2. current Supreme Court rule、particular court/agency order/form。
3. official judgment、court/date/case number、supporting passage。
4. ministry/regulator guidance。bindingでないことを明示。
5. JFBA/local bar professional rule。
6. commercial database/secondary source。種類を明示。

日本法令外国語訳DBはreference-only。CourtListener/Fastcase等の米国coverageを日本法の
verificationとして使わない。裁判所裁判例検索のnegative resultはabsence proofでない。
日弁連の職務基本規程、public lawyer search、業務広告規程・指針を別sourceとして扱い、
検索結果だけでauthority、専門性、availability又はengagementを証明しない。

## Workflow

### 1. Frame question

広すぎる場合はissueを分ける。requested outcome、relevant facts、forum、date、
procedure、counterargumentを含むquestionにする。

### 2. Seed material

responsible lawyer approved guide、official form、redacted precedent、matter documentを
readし、何を読んだか、何が不足かを示す。seedはcurrent lawの代替ではない。

### 3. Roadmap

各source candidate:

```yaml
authorityType: "[ASCII enum]"
title: "[title]"
issueSupported: "[issue]"
officialUrl: "https://..."
articleOrSection: "[article/section]"
effectiveFrom: "[date or unknown]"
asOf: "[date]"
retrievalStatus: retrieved | lead-only | unavailable
supportStatus: supports | partial | adverse | unclear | unread
nextCheck: "[specific verification]"
```

case lawはcourt、date、case number、procedural posture、holding/support、later treatment
checkをroadmapにする。単なるcase name listをauthorityとして扱わない。

### 4. Search terms

e-Gov、官報、裁判所、省庁、Japanese commercial database向けのJapanese queryを示す。
英語queryはcross-border又はtranslation discoveryに限定し、日本語原文へ戻る。

### 5. Existing research gap analysis

uploaded researchについてcovered、missing、stale、future/current conflict、quote/support、
adverse authority、forum mismatchを示す。source不足をmodel knowledgeでsilent補完しない。

family matterでは2026-04-01 reform、DV protection orderの地方裁判所route、
児童虐待防止法6条等をcurrent sourceから別々に調べる。民事時効では民法147～152条等の
完成猶予/更新を区別し、民事電子送達では109条の2・109条の3、time-computation、
transition fieldsを確認する。

## Output

- DRAFT/reviewer note
- precise research question
- seed documents and coverage
- primary-source roadmap
- case-law areas and database limitation
- professional/guidance/secondary layers
- current vs future law table
- search queries
- open factual/source questions
- verification plan for student and responsible lawyer

`lead-only`をcitation-readyと表示しない。verification eventはappend-only auditへ記録する。

consequential translationを作る場合、Japanese source item/version、target artifact
version/hash、responsible-lawyer legal review、competent-language reviewを別々に記録する。

## 行わないこと

- authoritative memo、client advice、case acceptance
- Westlaw syntax又はU.S. sourceを日本default
- translationをbinding Japanese textとして引用
- judgment databaseをcomplete/citatorとして扱う
- sourceなしのquote、pinpoint、good-law conclusion
- deadlineをverified/calendared
- send/post/file
