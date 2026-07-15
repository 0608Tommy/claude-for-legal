# Connector compatibility layer

Source `.mcp.json`の52宣言・20 unique connectorを、Microsoft 365 Copilot
Cowork向けに評価する台帳です。初回packageはskills-onlyであり、manifestへ
`agentConnectors`を登録しません。

## Target条件

- public HTTPS Streamable HTTP
- TLS 1.2以上、JSON-RPC 2.0
- `initialize`, `notifications/initialized`, `tools/list`, `tools/call`
- 30秒以内のtool call
- long-running jobはstart/status/result
- `readOnlyHint`, `destructiveHint`, `title`
- OAuthPluginVaultとMicrosoft Token Store
- per-user authorization
- write/destructive actionのfresh confirmation

source URLが`/sse`で終わるconnectorはそのまま登録せず、Streamable HTTP
adapterを要求します。URLだけから現行transport/auth/tool safetyを推測しません。

## Microsoft 365置換

- Slack用途 → Teams / Outlook / approved notification flow
- Google Drive用途 → SharePoint / OneDrive
- generic state → SharePoint Lists / Dataverse

置換は名称の単純変更ではありません。read/write scope、identity、retention、
matter isolation、external sharing、auditを用途ごとに確認します。

## 実装状態

`compatibility-matrix.json`はdispositionを確定していますが、実際の
OAuthPluginVault registration、vendor consent、tool discovery、annotations、
timeout、data egress、tenant ingestionは未実施です。test tenantで成功するまで
`connected`または`compatible`と表示しません。
