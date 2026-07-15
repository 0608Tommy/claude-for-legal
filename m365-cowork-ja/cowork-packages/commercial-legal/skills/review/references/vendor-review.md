> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Vendor / services agreement review

## Purpose

teamのactual playbookと契約を比較し、deviation、risk、business impact、smallest redline、approval routeを1passで示す。`market standard`ではなくprofileのstandard/fallback/neverを使う。

## Orient

| Question | Required answer |
|---|---|
| Agreement | MSA / services / SOW / license / other |
| Our side | Customer / Vendor |
| Counterparty | identity、negotiating leverage |
| Value | ACV / TCV / unknown |
| Term | initial、renewal |
| DPA | attached / URL / missing |
| Order form | attached / separate / missing |
| SLA | attached / referenced / missing |

value不明でapproval mathをしない。

## Incorporated terms

DPA、privacy policy、AUP、service terms、security terms、SLAがURL incorporationされる場合:

- exact URL
- accessed version/date
- unilateral update
- priority
- archive/evidence

を確認する。`missing`と`incorporated but unread`を分ける。DPA unreadならdata analysisはpartial。

## Deal-breaker

`oneThing`を先にcheckする。

```markdown
## ⛔ DEAL-BREAKER PRESENT

**Section [X]** contains [issue].
Playbook: [exact never/deal-breaker].

- Push back: [specific language]
- Escalate: [named approver]
- Alternative/walk: [realistic option]
```

detail reviewを続けるかは利用者のscopeに従う。

## Core categories

- definitions/scope/order of precedence
- obligations/acceptance/change control
- fees/tax/invoice/late fee
- warranties
- limitation of liability
- indemnification
- confidentiality
- data protection/security/incident
- IP/background/foreground/license
- insurance
- audit/records
- term/renewal/termination
- transition/data return
- assignment/change of control
- force majeure
- publicity
- governing law/forum/arbitration
- notices
- compliance with law
- missing provisions

## Finding format

```markdown
### [Finding ID] — §[X]: [Issue]

**Playbook**
> "[exact current position]"

**Contract**
> "[full relevant conditional text]"

**Gap:** [category]
**Legal risk:** [scale]
**Business friction:** [scale]
**Why it matters:** [...]

**Smallest proposed change**
- Delete: "[text]"
- Insert: "[text]"
- Result: "[clean resulting sentence]"

**Fallback / escalation:** [...]
**Jurisdiction:** [law/guidance/playbook distinction]
```

## Liability cap

必ず4次元:

1. directとindirect/consequential
2. exact cap base
3. above/below cap carveouts
4. playbook per dimension

aggregate/per-event、order form、fees paid/payable、lookback、claims aggregationも確認する。capがnominalかmeaningfulかをvendor riskに照らして説明する。

## Indemnity

- trigger: claim/loss/breach
- covered parties
- IP/data/confidentiality
- defense/control/counsel
- consent to settlement
- exclusions
- cap interaction
- sole/exclusive remedy

indemnity directionはsales/purchasingで反転し得る。

## DPA/security

main terms、DPA、security exhibit、privacy policyのpriorityを確認する。日本は`common/jurisdictions/ja-jp/privacy-data.md`、取引scopeは`common/jurisdictions/ja-jp/entrusted-transactions.md`を読む。security certificationだけでactual controlを保証しない。

## Japanese transaction screen

- 取適法/Freelance Act scope
- required written/electronic terms
- payment/acceptance/change process
- consumer/特商法 scope
- competition/優越的地位
- electronic signature authority/evidence

法律、guidance、playbookを別列にする。

## Favorable and missing

**Better than standard:** negotiation trade-baitとして示す。

**Missing:** assignment、insurance、audit、security、force majeure、notice等。playbookに不要ならautomatic findingにしない。

## Redline granularity

word → phrase → subclause → sentence → whole clause。whole replacementはsurgical editより明確な場合だけで、理由をtransmittalに示す。

native tracked changesを主張しない。

## Escalation

value、🔴、automatic triggerをmatrixへ当て、全approverを列挙する。business sign-offをlegal approvalへ混ぜない。

## Connector

live、approved connectorがあればprior agreement、workflow、signature statusをread candidateとして使える。record作成、memo attach、envelope generate/sendは別confirmation。manifest未登録なら利用不可と扱う。

## Consequential gate

non-lawyerがredline送付・署名を求めた場合、counterparty、value、findings、proposed language、fallback、open documentsを1page briefにし、attorney reviewまで停止する。

## Close

redline draft、escalation、facts、renewal、summaryから選択。AIはdecisionを選ばない。
