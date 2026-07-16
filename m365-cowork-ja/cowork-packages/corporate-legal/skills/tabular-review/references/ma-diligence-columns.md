> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、日本のM&A diligence columnを追加した派生ファイルです。

# M&A diligence — standard column set

`--template ma-diligence`のstarting point。PA、request list、structure、sectorが
支配する。

```yaml
schema:
  name: "M&A Diligence — Standard"
  columns:
    - id: counterparty
      label: "Counterparty"
      type: verbatim
      prompt: "target以外のcontracting party名を原文どおり取得する。"

    - id: agreement_type
      label: "Agreement Type"
      type: classify
      options: [msa, purchase_order, license_in, license_out, lease, services, supply, distribution, nda, joint_venture, loan, guaranty, employment, other]
      prompt: "agreement typeは何か。"

    - id: effective_date
      label: "Effective Date"
      type: date
      prompt: "effective dateはいつか。"

    - id: term
      label: "Term"
      type: duration
      prompt: "initial/current termは何か。"

    - id: auto_renewal
      label: "Auto-Renewal"
      type: classify
      options: [none, annual, fixed_period, evergreen]
      prompt: "auto-renewalとcycleは何か。"

    - id: termination_for_convenience
      label: "Termination for Convenience"
      type: classify
      options: [none, either_party, target_only, counterparty_only]
      prompt: "without-cause terminationは誰にあるか。"

    - id: termination_notice
      label: "Termination Notice Period"
      type: duration
      prompt: "termination notice periodは何か。"

    - id: change_of_control
      label: "Change of Control"
      type: classify
      options: [silent, consent_required, consent_not_unreasonably_withheld, automatic_termination, notice_only, counterparty_right_to_terminate]
      prompt: "CoC trigger/effectは何か。"

    - id: claim_assignment
      label: "Claim Assignment"
      type: classify
      options: [silent, restricted, consent_required, notice_required, freely_assignable]
      prompt: "claim assignmentをどう扱うか。"

    - id: obligation_transfer
      label: "Obligation Transfer"
      type: classify
      options: [silent, restricted, consent_required, assumption_required]
      prompt: "obligation/debt transferをどう扱うか。"

    - id: contractual_position
      label: "Contractual Position"
      type: classify
      options: [silent, consent_required, novation_required, successor_permitted]
      prompt: "entire contractual positionの移転はどう扱うか。"

    - id: transaction_succession
      label: "Transaction Succession"
      type: classify
      options: [share_sale_no_party_change, business_transfer_individual_transfer, merger_universal_succession, company_split_special_succession, unknown]
      prompt: "deal structure上の承継mechanismは何か。"

`needs_review`はclassify valueに入れない。不明・矛盾・判断保留はcell
`state: needs_review`かつ`value: null`で表す。

    - id: exclusivity
      label: "Exclusivity / Non-Compete"
      type: classify
      options: [none, exclusive_supplier, exclusive_customer, non_compete, non_solicit, territory_restriction, most_favored_nation]
      prompt: "competition restrictionは何か。"

    - id: liability_cap
      label: "Liability Cap"
      type: currency
      prompt: "liability cap amount/multiplierは何か。"

    - id: indemnification
      label: "Indemnification"
      type: classify
      options: [none, mutual, target_indemnifies, counterparty_indemnifies, ip_only, third_party_claims_only]
      prompt: "indemnity direction/scopeは何か。"

    - id: governing_law
      label: "Governing Law"
      type: verbatim
      prompt: "governing lawを原文どおり取得する。"

    - id: licence_treatment
      label: "Licence / Permit Treatment"
      type: classify
      options: [not_applicable, transferable, prior_consent, post_notice, reapplication, non_transferable, unknown]
      prompt: "licence/permitのtransfer/control-change treatmentは何か。"

    - id: personal_data
      label: "Personal Data / Security"
      type: classify
      options: [none, personal_data, sensitive_data, my_number, cross_border, security_obligation]
      prompt: "personal data/security/foreign transfer issueはあるか。"

    - id: notices
      label: "Notice Requirements"
      type: verbatim
      prompt: "targetへのnotice method/address/deadlineを原文どおり取得する。"
```

## Common additions

- listed/public target: EDINET、TDnet、insider、tender offer、large holding
- foreign investor: FEFTA facts
- overlap/market: JFTC turnover/voting/market
- labour-heavy: transfer consent/objection、union、benefits
- IP-heavy: title、employee invention、moral rights、OSS、recordal
- regulated: licence、foreign ownership、prior consent、economic security

fast passでもcounterparty、effective_date、term、change_of_control、
contractual_position、licence_treatmentを優先し、internal fast passをlegal
clearanceと表示しない。
