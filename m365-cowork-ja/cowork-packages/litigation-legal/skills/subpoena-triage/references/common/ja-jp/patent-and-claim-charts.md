> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本の特許claim chartと民事要件事実chart

chartはdraftであり、filed contention、鑑定、法律意見、裁判所判断ではない。

## Patent mode

主要source:

- 特許法68条、70条: 特許権、技術的範囲
- 100～103条: 差止め、間接侵害、損害、過失推定
- 104条の2: 具体的態様の明示義務
- 104条の3: 無効の抗弁
- 105条: 書類・電磁的記録提出
- 105条の2～105条の2の10: 査証
- 105条の3: 相当な損害額認定
- 105条の4: 秘密保持命令
- 29条、29条の2、36条、123条: 新規性、進歩性、記載要件、無効審判

required sheets/sections:

1. `_claim-text-ja`: final correction/trial、invalidation status、abandonmentを反映した
   controlling registered Japanese claims。official file/register/gazetteで確認
2. `_translations`: noncontrolling translation
3. `_construction`: 特許法70条、明細書、図面、出願経過、当事者主張
4. `_literal-mapping`
5. `_equivalents`: Ball Spline five-factor analysis
6. `_indirect-infringement`: 101条
7. `_invalidity`: 29, 29-2, 36, 104-3, 123条
8. `_specific-manner`: 104条の2
9. `_evidence-acquisition`: 105条、105条の2以下
10. `_damages`: 102～103条
11. `_confidentiality`: 105条の4
12. `_proceeding-stage`: infringement phase / damages phase / JPO parallel

独立Markman手続を前提にしない。constructionは`proposed | tentative | adopted`で
version管理し、裁判所の整理・判断が変わればnew version。

均等論は1998-02-24最高裁、平成6年(オ)1083号Ball Splineを起点にするが、
current precedent、prosecution history、factsをqualified counselが確認する。
2017-03-24 Maxacalcitrol decisionのfifth conditionも確認する。
JPO審査基準は`official-guidance`で、裁判所のclaim constructionを拘束すると書かない。
特許法70条3項によりabstractをtechnical scope決定へ用いない。
J-PlatPatはerror/omission/status lagの可能性があるためofficial register/certified
copyと照合する。

米国のPLR、§101/102/103/112、Federal Circuit、clear-and-convincing、Markmanを
日本modeへ移植しない。

## Civil mode

日本のcivil chart fields:

```yaml
claim_or_defence: "[claim/defence]"
legal_effect_sought: "[effect]"
statutory_and_case_authority: []
essential_facts: "[要件事実 / 主要事実]"
burden_of_allegation_and_proof: "[burden]"
pleading_location: "[item/page]"
admitted_or_denied: admitted | denied | unknown | partial
supporting_evidence: []
contrary_evidence: []
evidence_acquisition_route: "[route]"
limitation_and_accrual: "[analysis]"
source_state: supported | partial | disputed | gap | needs-discovery
normalized_state_jp: supported | partial | disputed | gap | needs-evidence
strength: strong | moderate | weak | none
```

民法415条、703条、709条、715条等は例示。actual claimの要件、抗弁、主張立証責任、
判例、特別法をcurrent sourceで確認する。司法研修所資料はtraining guidanceであり
binding lawではない。

米国pattern jury instruction、Twombly/Iqbal、12(b)(6)、MSJ、directed verdict、
RFA/interrogatoryを日本modeに使わない。

## Chart discipline

- claim/要件をverbatimで固定し、row IDをversion間で安定。
- dependent claimを`--include-dependents`で実row化。
- 除外したasserted dependent claimを明示。
- each cellにexact item/version、page/paragraph/line、quote provenance。
- gapを推測で埋めない。
- external cellのformula/HTML/Markdown injectionをneutralize。
- Markdown/CSVはoffline。XLSXはapproved tenant rendererとgolden-file reviewがある
  場合だけ。native Excel comment、hidden column、Office fidelityを保証しない。
- chartのserve/fileはAIが行わない。
