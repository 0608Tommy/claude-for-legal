> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) のMCP connector説明をMicrosoft 365 Copilot Cowork向けに変更した派生文書です。

# Connector方針

初回リリースは **skills-only** です。source `.mcp.json` は互換性台帳へ
取り込みますが、`agentConnectors` をmanifestへ自動登録しません。

## 必須条件

- 公開到達可能なHTTPS Streamable HTTP
- TLS 1.2以上、JSON-RPC 2.0
- `initialize`, `notifications/initialized`, `tools/list`, `tools/call`
- 原則30秒以内のtool call
- 長時間処理はstart/status/resultへ分割
- `readOnlyHint`, `destructiveHint`, `title`
- OAuthPluginVaultとMicrosoft Token Store
- Microsoft指定redirect URI
- 利用者ごとの認証
- write/destructive toolの明示確認

stdioとSSE-only connectorはそのまま登録しません。adapterが必要です。

## 現在の保留理由

Unified App Manifest 1.28、1.29、Cowork exampleの間で
`mcpToolDescription`、API key、DCR等の記述に差異があります。1.29へ黙って
上げず、1.28でのATK検証とtest-tenant ingestionが成功したconnectorだけを
追加します。

## Microsoft 365置換

Slack / Google Drive前提は用途ごとにTeams、Outlook、SharePoint、
OneDriveの承認済みactionまたはremote adapterへ置換します。source名を
単純置換せず、read/write、scope、保持、外部共有、matter isolationを確認
します。

CoCounselは `../shared/vendor-clearance.json` の条件が満たされるまで
登録・配布しません。
