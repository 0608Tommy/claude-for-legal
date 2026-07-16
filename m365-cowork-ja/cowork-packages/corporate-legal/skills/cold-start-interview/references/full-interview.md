> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のcorporate/M&A setup向けに変更した派生ファイルです。

# Full interview

1 turnに2～3 answerable prompt。documentがあるfieldはexact itemを先に求める。

## 1. User / practice / security

- role、attorney contact/supervision
- practice setting、organization、team
- escalation/approval authority
- SharePoint/OneDrive/gateway live status
- connector live status
- retention、legal hold、DLP
- matter workspace/clean-team

## 2. Japan entity/governance

- entity form: KK/GK/other
- legal name、registered head office、corporate number
- organ design
- articles/board regulation/committee charter items
- public-notice method
- share-certificate/restricted-share
- Art. 370 authorization
- current directors/auditors/committees
- electronic minutes/signature policy

## 3. M&A

- buy-side/sell-side/both
- transaction structures used
- deal cadence/lead/outside counsel
- request list/category
- PA/internal materiality
- VDR
- issues memo format/severity/audience
- Luminance/Kira trust and transfer policy
- closing/integration owner/cadence

## 4. Board / consent

- formal role、meeting cadence、portal
- minutes depth/turnaround/approval
- precedent source/version
- consent use/limits
- Art. 319/370/372/committee practice
- recital/resolution/authorization language
- e-signature/evidence/retention
- annual governance cycle

## 5. Public company

- listed status、exchange/market、EDINET code
- fiscal year/reporting calendar
- annual/half-year securities report
- internal-control report/confirmation
- extraordinary report
- TDnet decision/fact disclosure
- governance report
- insider list/pre-clearance/trading window
- Art. 163 officer/major shareholder report
- Arts. 166/167
- large holding
- tender offer process
- disclosure committee/approver

Form 4、accelerated filer、10-Qを日本fieldへ流用しない。

## 6. Entity management

- entity list/org chart
- corporate number/entity form/ownership
- organ/officer term
- event-driven registry owner
- annual meeting/accounts/public notice
- tax/social/labour owner
- licence list/renewal
- seal/electronic certificate
- beneficial-owner list evidence
- dormant entities
- intercompany agreement

## 7. Outputs

- internal marking
- external/corporate record separation
- house memo/schedule/table format
- dashboard preference
- source/currency standard
- human approval for send/sign/file/close

## Seed extraction

fieldごとに:

```yaml
value: "[value]"
sourceType: document | interview | default
sourceItemId: "[itemId or null]"
sourceVersion: "[version or null]"
sourceLocation: "[location or null]"
reviewStatus: confirmed | pending | default-human-review
```

documentなしをdocument-derivedと表示しない。
