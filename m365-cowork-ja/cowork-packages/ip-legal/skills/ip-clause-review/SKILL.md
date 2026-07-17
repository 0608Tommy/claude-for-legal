---
name: ip-clause-review
description: >
  employment、consulting、SOW、vendor、licence、collaboration等の知財条項をreviewし、日本の権利帰属・JPO recordal、Copyright Articles 27/28、moral rights、employee inventions、co-ownership、trade secret、OSS/AI、competitionを確認して最小granularityの修正文案を作る。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# IP clause review

旧来の参照label:
`/ip-legal:ip-clause-review [file path | Drive link | paste text]`。

Coworkではauthorized SharePoint/OneDrive itemまたは会話で提供されたtextを使い、
local pathを読みません。

## Mandatory gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、gateway、
   exact source item/version、scope、destinationをpreflight。
2. practice/user profile、approver、jurisdictions、house IP position、OSS policyを読む。
3. matter scopeならactive/unexpired binding。practice modeはfresh session。
4. agreement type、company sideを
   `granting | receiving | both`でdocumentごとに確定。
5. main agreement、SOW、order、annex、incorporated URLを読み、coverageを記録。
6. governing lawだけでなくcreator、right、registration、performance territoryを確認。
7. 日本なら[契約・ownership module](references/common/ja-jp/contracts-ownership.md)。
8. internal memoとcounterparty redline draftを分離。AIは送信、署名、recordal、
   filingを実行しません。

## Orient

| Question | Value |
|---|---|
| Agreement type | employment / consulting / SOW / vendor / in-license / out-license / collaboration / settlement / acquisition / other |
| Side | granting / receiving / both |
| Counterparty | entity/type/sophistication |
| Consideration | salary / fee / royalty / equity / other |
| Governing law / right jurisdictions | [...] |
| Source coverage | [...] |

## Assignment gap first

employment/consulting/SOW等では最初に:

- present/future assignment languageとactual effect
- scope of work product/invention/design/data
- pre-existing/background IP schedule
- further assurances
- recordal cooperation
- employee-invention benefit/process
- copyright Arts. 27/28
- moral-rights non-exercise
- contractor ownership
- AI-use/human authorship/inventorship disclosure

U.S. `hereby assigns`または`work made for hire`を日本でuniversal solutionとして
扱いません。registered industrial rightのtransfer effect/recordalを別に確認します。

## Clause review

- ownership / assignment
- background/foreground IP
- improvements/derivatives
- licence: exclusivity、territory、field、sublicence、term、termination
- statutory exclusive vs contract-exclusive ordinary licence
- co-ownership
- warranties / authority / non-infringement
- indemnity: scope、cap、procedure、exclusion
- trademark quality/use control
- confidentiality/trade secret
- OSS/source/NOTICE/patent clauses
- AI training/output/data/code/inventorship
- competition: grant-back、non-assert、exclusive dealing、territory/customer、tying

## Japanese formalities

- patent/trademark/design transfer and JPO registration
- Patent Act Art. 99 ordinary licence
- patent co-owner practice/share transfer/licence
- copyright co-owner exercise
- Copyright Arts. 27/28 presumption
- copyright transfer registration/opposability
- moral rights non-transferability
- corporate authorship Art. 15 conditions
- Patent Act Art. 35 and Design Act Art. 15
- Trademark Act Art. 53 quality/confusion risk

source、actual contract intent、recordal statusを確認し、法律とinternal playbookを
分けます。

## Finding

```markdown
### [Section]: [Clause]
**Source quote:** [...]
**What it does:** [...]
**Layer:** [B] / [G] / [I] / contract
**Risk:** 🔴 Blocking | 🟠 High | 🟡 Medium | 🟢 Low
**Why:** [...]
**Smallest redline:**
> [...]
**Fallback/approver:** [...]
**Open judgment:** [review]
```

## Cross-clause consistency

- grant vs ownership
- background licence sufficiency
- warranty vs indemnity
- termination vs surviving licence
- SOW vs MSA
- confidentiality vs residuals/AI use
- OSS representation vs delivery/source obligation
- co-ownership vs enforcement/recordal

## Redline granularity

word → phrase → subclause → sentence → whole clauseの順。whole replacementは必要性を
説明します。native Word tracked changesを生成・適用したとは表示せず、deletion/
insertion/clean textを示します。

## Output

- reviewer note
- bottom line/issues/approver
- assignment gap
- clauses by severity
- cross-clause consistency
- Japanese formalities/recordal
- consolidated redline draft
- external transmittal draft（別artifact）

## Other jurisdictions

[U.S./global layer](references/common/original-ip-logic.md)を別sectionで適用し、
work-for-hire、moral rights、recordal、competitionをjurisdiction別に示します。

## 行わないこと

- title/ownership/perfectionをcontract wordingだけで確定
- signature-ready、recorded、effectiveと未検証で表示
- counterpartyへsend
- JPO/copyright registrationをsubmit
- local filesystem、agent、hook、subagentを使う
