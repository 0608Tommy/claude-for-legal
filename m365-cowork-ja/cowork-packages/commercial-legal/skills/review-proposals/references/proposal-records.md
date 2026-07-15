> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Proposal and deviation records

## Deviation

```yaml
recordType: deviation
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[id]"
recordId: "dev:[dealId]:[clause]:[sourceVersion]"
dealId: "[source ID or stable generated ID]"
contractItemId: "[exact itemId]"
sourceVersion: "[contract/version or signed artifact hash]"
side: sales | purchasing
counterparty: "[name]"
agreementType: MSA | NDA | SOW | SaaS | Other
dateSigned: "[ISO date]"
excludeFromPatterns: false
dealContext: "[notes]"
clause: limitation_of_liability
standardPosition: "[text]"
signedPosition: "[text]"
direction: "[normalized direction]"
severity: minor | moderate | critical
basis: counterparty_leverage | commercial_priority | timeline_pressure | strategic_relationship | negotiation_stalemate | legal_judgment | other | not_provided
context: "[text]"
```

duplicateはimmutable `recordId`と`dealId + clause + sourceVersion`で確認する。

## Proposal

```yaml
recordType: playbook-proposal
proposalId: "[immutable id]"
recordId: "[same immutable proposalId]"
tenantId: "[tenant id]"
practiceId: "[practice id]"
scopeType: practice | matter
scopeId: "[id]"
side: sales | purchasing
clause: limitation_of_liability
status: draft | pending | accepted | edited | rejected | deferred | superseded | archived
pattern:
  count: 6
  lookbackMonths: 12
  direction: "accepted cap above 12 months"
  commonBasis: counterparty_leverage
currentLanguage: "[exact text]"
proposedLanguage: "[exact text]"
recommendation: Revise | Clarify | Flag for discussion
supportingDeviationIds:
  - "[id]"
excludedDeviationIds:
  - "[one-off id]"
profileItemId: "[itemId]"
profileETagAtGeneration: "[eTag]"
generatedAt: "[ISO datetime]"
generatedBy: PowerAutomate | Cowork-on-demand | manual
rejectedAt: "[ISO datetime or null]"
deferUntil: "[ISO date or null]"
deferAfterRunId: "[approved monitor run ID or null]"
```

## Display

```markdown
Proposal [N] of [total]: [Clause]

**Pattern:** [what, count, period]
**Most common basis:** [basis]
**Scope / side:** [scope, sales/purchasing]

**Current**
> "[text]"

**Proposed**
> "[text]"

**Supporting records**
- [counterparty, date, deviation ID]

**Recommendation:** [Revise | Clarify | Flag for discussion] — [reason]

Choose: Accept / Reject / Edit / Defer
```
