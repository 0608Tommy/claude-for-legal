# Microsoft 365成果物renderer

ローカルで再現可能なHTML、Markdown、CSV rendererと、Microsoft 365側で
実装・検証するOffice/PDF契約です。

## 実装済み

```bash
python3 scripts/render_m365_dashboard.py \
  m365-cowork-ja/artifacts/fixtures/sample-findings.json \
  m365-cowork-ja/.cache/artifact-output
```

- standalone HTML
- Markdown summary/table
- Excel-compatible CSV

外部文字列はHTML escapeし、URL schemeを制限し、CSV formula injectionを
防ぎます。

## Tenant rendererが必要

- Word `.docx`
- native Excel `.xlsx`
- PowerPoint `.pptx`
- PDF
- tracked changes、Office style fidelity

これらは対象tenantのOffice/Power Automate actionまたは承認済みrendererで
作成し、golden-file testを通るまで対応済みと表示しません。
