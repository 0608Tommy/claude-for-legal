---
name: claim-chart
description: >
  日本の特許侵害・無効または民事請求・抗弁について、claim・要件事実を証拠へ要素別にmappingし、gapを優先表示する。dependent claimを実row化し、除外claimを開示し、全cellをexact sourceへpin citeする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Claim chart

canonical label:
`/litigation-legal:claim-chart [--patent | --civil] [--infringement | --invalidity | --review] [--claim <n>] [--count <name>] [--target <slug>]`

grammar compatibility: `--include-dependents`。

chartはdraftであり、contention、brief、expert opinion、merits conclusionではない。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。
2. exact user/profile、active matter/binding、conflicts/access、source/evidence ACLを確認。
3. disclosed/produced/clean-team sourceのuse restrictionとpurposeを確認。
4. mode、side、forum、phase、claim/count、target、existing chartを確定。
5. 日本なら
   `references/common/ja-jp/patent-and-claim-charts.md`、
   `evidence-confidentiality-preservation.md`、`source-register.md`を読む。
6. controlling textとauthorityをその会話でofficial sourceから確認。templateをlawと
   扱わない。
7. exact source item/version、read coverage、translation statusを記録。
8. quote/pinpoint/provenanceとsafe cell renderingを適用。
9. draft保存、state create/update、external service/fileを分離する。

## Mode

### `--patent`

sub-mode:

- `--infringement`
- `--invalidity`
- `--review`

必要情報: patent number、controlling Japanese claim text、asserted claims、target、
specification、drawings、prosecution history、court/JPO proceeding、existing
construction。

日本modeのsections:

1. `_claim-text-ja`
2. `_translations`
3. `_construction`
4. `_literal-mapping`
5. `_equivalents`
6. `_indirect-infringement`
7. `_invalidity`
8. `_specific-manner`
9. `_evidence-acquisition`
10. `_damages`
11. `_confidentiality`
12. `_proceeding-stage`

特許法68、70、100～105条の4、29、29条の2、36、123条等をactual issueに応じて
確認する。独立Markman、US PLR、§101/102/103/112を日本modeに使わない。

### `--civil`

必要情報: actual pleaded claim/defence、legal effect、side、forum、pleading、
authority、evidence corpus。

row:

```yaml
claim_or_defence: "[claim/defence]"
legal_effect_sought: "[effect]"
statutory_and_case_authority: []
essential_facts: "[要件事実 / 主要事実]"
burden_of_allegation_and_proof: "[burden]"
pleading_location: "[source]"
admitted_or_denied: admitted | denied | unknown | partial
supporting_evidence: []
contrary_evidence: []
evidence_acquisition_route: "[route]"
limitation_and_accrual: "[analysis]"
source_state: supported | partial | disputed | gap | needs-discovery
normalized_state_jp: supported | partial | disputed | gap | needs-evidence
strength: strong | moderate | weak | none
```

米国pattern jury instruction、Twombly/Iqbal、MSJ、RFA/interrogatoryを使わない。

## Claim parse / dependent claims

1. controlling claim/countをverbatimでparse。
2. stable row IDを付ける。
3. userにparseを示し、mapping前に確認。
4. asserted dependent claimは`--include-dependents`で追加limitationをactual row化。
5. runから除外したasserted dependent claimを番号と理由付きで必ず開示。
6. silent dropは禁止。

## Mapping

各row:

- exact element / essential fact
- target feature / pleaded fact
- supporting evidenceとcontrary evidence
- exact quote、page/paragraph/line、item/version
- assumed construction / legal formulation
- patent: separate `mapping`, `state`, `confidence`
- civil: raw `source_state`, normalized `normalized_state_jp`, `strength`
- open question / evidence acquisition route
- verified checkboxは人だけが更新

source mapping enumは
`references/common/original-litigation-logic.md`に従い、import時にrenameしない。
日本modeのnew rowは適切なJapan fieldも保持する。

thin evidenceは`needs-evidence`または`gap`。類似product、一般経験、model knowledgeで
埋めない。

## Output

```markdown
> **⚠️ レビュー担当者向け注記**
> [common block]

# Claim / element chart — [subject]

**Mode:** patent | civil
**Sub-mode:** infringement | invalidity | review | N/A
**Forum / phase:** [...]
**Claims / counts:** [...]
**Targets:** [...]
**Controlling sources:** [...]
**Dependent claims omitted:** [none/list + reason]

| Row | Element / 要件事実 | Supporting evidence | Contrary evidence | Mapping | State | Confidence / strength | Open question | Verified |
|---|---|---|---|---|---|---|---|---|

## Gap / needs-evidence list
[priority output]

## Construction / formulation assumptions
[assumption and fail condition]

## What cuts which way
[strongest / weakest without conclusion]

## Conclusion line
This skill does not conclude. [mapped/supported], [gap/needs-evidence], [disputed].
```

MarkdownとCSVを作れる。CSVはvalue fileとsource companionを分け、formula injectionを
neutralize。XLSXはapproved tenant rendererとgolden-file reviewがある場合だけで、
native comment、hidden source column、format fidelityを保証しない。

state writeは`claim-chart` recordのconditional create/updateでversion管理し、
past versionを削除しない。

## Completion

claims/counts、target、row counts by state、gap list、omitted dependent claims、
unread source、version、save stateを示し、次から選んでもらう。

1. missing evidence plan
2. construction/formulation questionをcounselへescalate
3. chronology/witness prep handoff
4. version comparison
5. other

## 行わないこと

- infringement/non-infringement/liability/non-liabilityの結論
- controlling element/claim constructionの最終決定
- expert analysisの代替
- sourceなしのmapping
- serve/file/sign
- local filesystem、agent、hook、subagent
