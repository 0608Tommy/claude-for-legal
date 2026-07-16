---
name: use-case-triage
description: >
  新しいdata processing、feature、vendor利用を短時間で確認し、PROCEED、PIA REQUIRED、DPIA MANDATORY、STOPを暫定分類する。house trigger、法定assessment、policy conflict、sectoral overlay、法域別routeを分け、次のPIA等へhandoffする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: privacy-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Privacy use-case triage

旧来の参照labelは `/privacy-legal:use-case-triage [describe the data processing activity or feature]`。

classificationは暫定draft。AIはlaunch、processing、vendor、policy changeをapproveしない。

## 必須gate

1. `references/common/cowork-runtime-contract.md`を読む。local fileへ保存しない。
2. exact practice profileのPIA trigger、regulatory footprint、privacy commitments、risk postureと現在利用者の`user-profile`を読む。
3. workspaceが有効でmatter scopeを選ぶ場合はserver binding、matter
   `status: active`、scopeを確認する。workspaceが無効、またはfresh session
   でpractice-levelを明示した場合は`scopeType: practice`を許可する。
   archived/revokedでは停止する。
4. activityが曖昧なら、最も結論を左右する質問を1つずつ行う。
5. `request > matter > practice-profile > tenant-default`で法域を解決する。
6. house trigger、binding-law trigger、official guidance、internal policyを分ける。
7. current law、deadline、2026年改正statusをofficial sourceで確認する。
8. destination、confidentiality、personal-data minimizationを確認する。
9. severityはupstream floorとして下流へ渡す。
10. writeはexact ID/eTag/idempotencyとfresh confirmationを使う。

## Setup incomplete

tailored triageを停止し、`cold-start-interview`を案内する。利用者が明示的にprovisional runを求めた場合だけ:

- `[PROVISIONAL — no configured profile]`
- generic assumptionを明記
- findingごとに`[PROVISIONAL]`
- `PROCEED`を最終承認として扱わない
- personal draftのみ

## Classification

- `PROCEED` — house triggerも法定assessment triggerも見当たらず、policy conflictなし。standard safeguardsは残る。
- `PIA REQUIRED` — internal triggerまたは強いrisk indicator。法定mandatoryとは限らない。
- `DPIA MANDATORY` — current binding lawのformal assessment triggerが確認できる。
- `STOP` — policy/noticeの直接矛盾、明確な法的route欠落、禁止・never position。redesignまたはhuman decision前に進めない。

## 会話state machine

| state | action |
|---|---|
| `understand-activity` | data、subjects、purpose、new/reuse、vendor、decision |
| `resolve-jurisdiction` | affected people、entity、countries、sector |
| `house-trigger` | internal PIA trigger |
| `sector-first` | regulated data/activity |
| `mandatory-assessment` | current law trigger |
| `policy-conflict` | policy/CMP/labels/consent/sector notice |
| `classify` | 4 classificationのproposal |
| `conditions` | owner、deadline、evidence |
| `handoff` | PIA、AIA、DPA、launch review |
| `confirm-save` | personal draft / reviewed output |

## Activity facts

- exact data fields、inferred attributes
- customers、employees、applicants、children、patients等
- purpose / benefit
- new collection / reuse / combination
- vendor / model / independent training
- automated or consequential decision
- internal / customer-facing / public
- country / remote access / retention

`anonymized`、`pilot`、`vendor handles privacy`、`we already do it`を自動safe harborにしない。

## Sector-first

US:

- GLBA / Reg P
- HIPAA / HITECH
- FERPA
- COPPA
- VPPA、CPNI、DPPA、TCPA等

Japan:

- My Number
- financial
- medical / care
- telecom / communications secrecy / external transmission
- employee / applicant
- child / biometric
- public sector

日本module:
`references/common/jurisdictions/ja-jp/sectoral-my-number.md`。

## Assessment trigger

日本の民間一般PIAは一律mandatoryではない。
`references/common/jurisdictions/ja-jp/pia-assessments.md`を読む。

強いindicator:

- children
- biometric / emotion / personality
- sensitive or vulnerable people
- large-scale/systematic tracking
- employee/applicant scoring
- dataset combination / inference
- unexpected reuse
- ad-tech
- automated consequential decision
- new transfer / vendor training

current binding-law triggerがなければ`PIA REQUIRED`であり、`DPIA MANDATORY`とは書かない。

## Policy conflict

actual policy、CMP、App Store/Google label、in-product consent、sector noticeと比較する。

- new data category
- new purpose
- vendor independent use
- sale/share等
- longer retention
- new country / recipient
- rights process gap

direct conflictなら`STOP`候補。policyを変えるだけで適法になると仮定しない。

## Output

`references/triage-output.md`を使う。classification、reason、house trigger、law trigger、policy conflict、conditions、ownerを示す。

## Handoff

PIAが必要なら、利用者の同意後に`pia-generation`を同じconversationで開始できる。AI decision-makingなら `/ai-governance-legal:aia-generation [activity]`、product launchなら `/product-legal:launch-review`、vendor termsなら `/privacy-legal:dpa-review` を参照labelとして示す。

他skillを自動起動せず、人に選んでもらう。

## Batch

roadmap等はsummary tableを先に出し、non-PROCEEDだけ展開する。大量ならscope/batchを選んでもらう。

## 完了

PIA intake、additional facts、DPA review、policy change、escalationから次を選んでもらう。
