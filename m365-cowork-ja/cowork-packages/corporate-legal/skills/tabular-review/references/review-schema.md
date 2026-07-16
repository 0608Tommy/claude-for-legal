> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 tabular review向けに変更した派生ファイルです。

# Review schema

```yaml
schema:
  name: "M&A Diligence — Project [Code]"
  created: "[ISO date]"
  transactionStructure: "[canonical value]"
  sourceScope:
    sourceSystem: "[system]"
    folderOrQueryId: "[ID]"
    sourceVersion: "[version]"
  columns:
    - id: counterparty
      label: "Counterparty"
      type: verbatim
      prompt: "契約当事者名を原文どおり取得する。"
    - id: effective_date
      label: "Effective Date"
      type: date
      prompt: "契約のeffective dateはいつか。"
    - id: change_of_control
      label: "Change of Control"
      type: classify
      options:
        - silent
        - consent_required
        - consent_not_unreasonably_withheld
        - automatic_termination
        - notice_only
        - counterparty_right_to_terminate
      prompt: "targetのchange of controlを扱うか。triggerとeffectは何か。"
```

## Stable schema rule

- `id`、`type`、`options`はrun中にsilentに変えない。
- changeはnew schema versionとしてsampleし直す。
- user-facing `label`は日本語化できるが、canonical ID/optionは保持する。
- source scope、transaction structure、schema versionをoutputへ埋め込む。
- `free`はdriftしやすいため必要最小限。

## Cell contract

```yaml
value: "[typed value or null]"
state: answered | not_present | unclear | needs_review
quote: "[exact text or null]"
location: "[specific location or null]"
sourceVersion: "[version]"
notes: "[reason or null]"
verified: ""
```
