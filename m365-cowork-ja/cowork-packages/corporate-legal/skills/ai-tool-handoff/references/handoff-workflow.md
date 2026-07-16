> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365のexternal-tool handoff向けに変更した派生ファイルです。

# AI tool handoff output

## Transfer review

```markdown
## Transfer review — [Matter / category]

**Candidate tool:** [Luminance / Kira / other]
**Documents:** [N] exact items, [versions]
**Purpose:** [extraction targets]
**Decision candidate:** [approved / approved-with-conditions / blocked / unknown]

### Conditions
- [authorization]
- [data minimization / redaction]
- [no-training / location / retention / deletion]
- [clean-team / MNPI / My Number / trade secret]
- [human approver and expiry]
```

## Load request draft

```markdown
## [Tool] Load Request — [Deal code] — [Category]

**Batch ID:** [ID]
**Source items:** [exact IDs/versions]
**Workspace:** [approved workspace]
**Extraction targets:** [canonical IDs]
**Materiality:** [internal threshold]
**Exclude:** [data/classes]
**Return:** `{value, state, quote, location, sourceVersion}`
**Deletion evidence due:** [date]
```

## QA summary

| Clause type | Tool flagged | QA sample | Quote mismatch | Accepted after judgment | Material |
|---|---:|---:|---:|---:|---:|
| Change of control | | | | | |
| Assignment | | | | | |

show:

- trust level
- model/version
- sample method/size
- false positive/negative known limits
- widened review trigger
- deletion evidence
- `[review]` items

## Handoff

closing candidateはsource fieldsを保持する。

```yaml
item: "[action]"
category: "[Third-party consents | Corporate approval | Regulatory filing | Registry | Labour | Licence | Closing deliverable | Tax/Social Insurance]"
source: "[source item/version + location]"
blocking: true
severity: "[🔴 | 🟠 | 🟡 | 🟢]"
counterparty: "[name or N/A]"
conditions: "[condition or N/A]"
notice_deadline: "[date/period or unknown]"
approval_body: "[body or N/A]"
approval_threshold: "[threshold or unknown]"
statutory_or_charter_source: "[source or N/A]"
estimated_time_to_complete: "[estimate or unknown]"
must_occur_before: "[signing | closing | post-closing | unknown]"
legal_basis: "[authority or contract, or unknown]"
source_version: "[source version]"
effective_date: "[date or null]"
evidence_required: "[evidence or unknown]"
filing_system: "[system or null]"
waiting_period_end: "[date or null]"
waivable: false | true | unknown
```

AIはhandoffをstateへ自動保存せず、人がsource、severity、dedupe、scopeをreviewする。
