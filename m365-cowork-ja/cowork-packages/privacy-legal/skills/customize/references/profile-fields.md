> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Privacy profile fields

| Section | Scope | Examples | Downstream |
|---|---|---|---|
| Company | company profile | name、industry、practice setting | all legal packages |
| Jurisdictions | practice profile | ja-JP、EU、US states | all privacy skills |
| Risk posture | practice profile | conservative/middle/aggressive | triage、PIA、DPA |
| People | practice/user | DPO、GC、attorney contact | escalation / non-lawyer gate |
| DPA processor | practice profile | audit、incident、subprocessor、transfer、deletion、liability | dpa-review |
| DPA controller | practice profile | required security、notice、audit、deletion | dpa-review |
| Policy | practice profile | data、purpose、recipient、retention、rights | PIA、triage、monitor |
| Surfaces | practice profile | CMP、labels、employee/sector notice | policy-monitor |
| PIA | practice profile | trigger、format、depth、sign-off | pia-generation |
| DSAR | practice profile | systems、identity、SLA、delivery | dsar-response |
| Matter | matter record | override、jurisdiction、viewers | matter-bound skills |
| Integration | practice/user | connected status、scope | retrieval only |

## Non-deletable safety fields

- isolation and binding
- source/currency verification
- human approval gates
- DLP blocker
- immutable audit
- retention/legal hold
- Japan review status

`Not configured`、`inactive`、`superseded`等でhistoryを保持する。
