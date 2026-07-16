---
name: reg-gap-analysis
description: >
  新法、改正、規則、official guidanceを現行privacy policy・運用・DPA・本人請求processと比較する。適用範囲、成立・公布・施行status、binding law・guidance・internal policyを分け、gapとowner付き是正計画をdraftする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: privacy-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Regulation-to-policy gap analysis

旧来の参照labelは `/privacy-legal:reg-gap-analysis [regulation name, or paste reg text/summary]`。

本skillは指摘されたchangeを分析する。自律的monitor、agent、hook、schedulerではない。

## 必須gate

1. `references/common/cowork-runtime-contract.md`を読む。local fileへ保存しない。
2. exact practice profileのregulatory footprint、privacy commitments、systems、DPA/PIA processと現在利用者の`user-profile`を読む。
3. workspaceが有効でmatter scopeを選ぶ場合はserver bindingとmatter
   `status: active`を確認する。workspaceが無効、またはfresh sessionで
   practice-levelを明示した場合は`scopeType: practice`を許可する。
   archived/revokedでは停止し、過去matter contextをcarryしない。
4. source text、version、issuing authority、statusを取得する。summaryだけで条文を創作しない。
5. `proposed | introduced | enacted | promulgated | effective | enforced`を分ける。
6. binding law、official guidance、internal policyを分ける。
7. current primary sourceを取得し、施行日、transition、threshold、scope、exceptionを確認する。
8. partial source・translationならcoverageを示す。
9. remediation、risk acceptance、policy adoptionはhuman decision。
10. writeはcreate/updateを分け、exact ID/eTag/idempotencyとconfirmationを使う。

source tagとcurrent-law ruleは
`references/common/source-provenance-and-review.md`。

## 会話state machine

| state | action |
|---|---|
| `collect-authority` | exact law/guidance/sourceを取得 |
| `status-check` | proposal→enforcementのstatusを確認 |
| `scope` | jurisdiction、threshold、sector、entity、data |
| `extract-requirements` | discrete requirementとcitation |
| `load-current-state` | policy、process、systems、DPA、PIA |
| `diff` | none / partial / full gap |
| `prioritize` | deadline、impact、effort、dependency |
| `remediation` | owner、due、evidence、approver |
| `review-save` | draft保存・reviewed output昇格 |

## Source status

日本2026年APPI改正のmodel:

- 国会成立: yes, 2026-07-10
- 公布の閣議決定: yes, 2026-07-14
- 公布年月日・法律番号: 2026-07-16時点で公式議案欄は空欄
- 施行: 未確認

結論は`成立済み・公布確認待ち・未施行`。改正をcurrent compliance gapとして断定せず、future-readiness planと現行法gapを分ける。

日本module:
`references/common/jurisdictions/ja-jp/source-register.md`。

## Scope

- data subjects / customers / employees / applicants
- revenue / volume / entity threshold
- sector / license / exemption
- controller / processor / 委託等のrole
- effective / enforcement / transition
- territorial / extraterritorial reach

適用しない場合も、理由とsourceを短いrecordに残す。

## Requirement extraction

| # | Requirement | Layer | Citation | Effective | Applicability |
|---|---|---|---|---|---|

category:

- Notice / transparency
- Rights / request
- Security / breach
- Vendor / DPA
- Consent / opt-out
- Governance / assessment / records
- Children / biometric / workplace
- Cross-border
- Sectoral

guidanceのrecommendationをlaw columnへ入れない。

## Current state

exact profile summaryだけでなく、可能ならactual policy、CMP、App Store/Google label、in-product notice、sector notice、DSAR process、DPA template、recent PIAを読む。version不明ならgapを確定しない。

## Diff

各requirementについて:

- regulation says
- current practice
- gap: `None | Partial | Full | Unknown`
- remediation type
- deadline
- evidence
- legal risk / operational risk
- owner / approver

unknownをnoneへ丸めない。recoverable errorとして`[review]`。

## Prioritize

1. effective/enforced deadline
2. penalty / individual harm / regulator attention
3. dependencyとlead time
4. cheap high-impact changes
5. already compliant controls

法定deadlineとinternal targetを分ける。

## Output

`references/gap-output.md`を使う。`no gaps`でも証跡としてdraftを残せるが、reviewed output昇格は人が確認する。

## Integration

- PIAで見つけたpolicy gapを入力にできる。
- policy-monitorは内部drift、本skillは外部rule change。
- regulatory feedの自律監視は別の承認済みtenant automationが必要。

## Large source

law package、consultation paper、guidelineが大きい場合、definitions、scope、duties、exceptions、effective/transition、enforcementを先に読み、coverageを記録する。summaryをfull legal reviewと書かない。

## 完了

policy draft、process change、DPA template change、product backlog、outside counsel question、watch itemから人に選んでもらう。
