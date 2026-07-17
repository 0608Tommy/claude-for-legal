---
name: deposition-prep
description: >
  canonical IDを保持しつつ、日本案件を米国depositionとして扱わず、内部witness interview、陳述書support、証人・当事者尋問、remote examinationの準備へrouteする。本人の記憶を作らず、exact record、論点、質問、矛盾を整理する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Witness / party examination preparation

canonical label: `/litigation-legal:deposition-prep [witness name]`

## Japan routing blocker

日本の民事訴訟では、米国型out-of-court sworn depositionを前提にしない。このcanonical
IDはmigration compatibilityのため保持するが、日本matterでは必ず次へrouteする。

```yaml
prepMode: internal-interview | witness-statement-support | witness-examination | party-examination | remote-examination
```

`FRCP 30`, `30(b)(6)`, state deposition equivalentを日本法として主張しない。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。
2. exact user/profile、active binding、matter/evidence ACL、witness accessを確認。
3. purpose、prep mode、witness role、friendly/adverse/neutral、court/dateを確認。
4. Japanなら
   `references/common/ja-jp/evidence-confidentiality-preservation.md`と
   `civil-procedure-and-digital.md`を読む。
5. current民訴法・民訴規則、case-specific orderをofficial sourceで確認。
6. exact document/transcript item/versionとcoverageを記録。
7. destination、attorney-limited/clean-team、personal data、DLPを確認。
8. quote/pinpoint/provenance ruleを適用。
9. AIはwitnessをcoachして虚偽・暗記証言を作らず、testimonyを本人として代筆しない。

## Workflow

### 1. Witness and purpose

- name / pseudonymous ID
- role、relationship、personal knowledge
- why this person matters
- fact/legal issue to establish or test
- hearing/examination type

### 2. Source set

- authored/sent/received documents
- meeting/calendar records
- prior statement/testimony
- relevant pleading/order/exhibit
- chronology events

connectorはlive probe成功後だけ使う。unread sourceをinventしない。

### 3. Japan procedure

民訴法202条は原則として申出当事者、相手方、裁判長の順で、裁判所が変更できる。
question form、document handling、remote examination、interpreter、sequestration等は
current rules/orderを確認する。

### 4. Build topics

- background / foundation
- facts supporting our theory
- facts cutting against us
- document authentication / context
- contradiction / credibility
- pivot fact
- open evidentiary or procedural issue

friendly witnessには記憶を引き出すopen prompt、adverse witnessにはlawyer review用の
controlled sequence候補を作る。courtが許すquestion formをqualified counselが確認する。

### 5. Record fidelity

prior statementをexact passageなしにquoteしない。impeachment pointのpinpointが
proposition全体を支えるか確認する。不一致は解消せず並列表示する。

## Output

```markdown
> **⚠️ レビュー担当者向け注記**
> [common block]

# Witness / party examination preparation — [name]

**Prep mode:** [enum]
**Witness posture:** friendly | adverse | neutral
**Court / date:** [...]
**Purpose:** [...]
**Applicable rules/order:** [...]

## I. Background / foundation
**Goal:** [...]
**Sources:** [...]
**Question prompts:** [...]

## II. Key factual topic
[same structure]

## III. Documents
| Exhibit candidate | Source/version | Purpose | Exact quote/pinpoint | ACL |
|---|---|---|---|---|

## IV. Contradictions / follow-up
[exact source pairs]

## V. Pivot fact
[goal、sequence、risks]

## Open legal/procedural questions
[qualified counsel review]
```

陳述書supportではquestion prompts、本人の回答、shown documents、consistency checklistを
分ける。AIが本人の声で事実を生成しない。

## Completion

mode、topics、source coverage、quote flags、rule questions、ACL、save stateを示し、
次から人に選んでもらう。

1. question outline refine
2. document/exhibit packet draft
3. contradiction source取得
4. procedural questionをcounselへescalate
5. other

## 行わないこと

- 日本にUS deposition procedureがあるとの表示
- 30(b)(6) equivalentの発明
- witness testimony/recollectionの生成
- witness examinationの実施
- sourceなしのimpeachment
- local filesystem、agent、hook、subagent
