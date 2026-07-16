> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Interview branches

## `initial`

orientation → gateway status → role → quick/full。

## `quick`

role、practice、team、tooling、recommendation/update preference、restrictive default、
DLP blockerを取得する。tenant policyはdraft。

## `full`

quick項目にsource/publisher、deployment context、license、connector/tool、
freshness、reviewer、group、retention/DLP/audit、starter packを追加する。

## `resume`

exact setup session ID/eTagを読み、answered fieldを再質問しない。pending questionだけ。
gatewayがなければprevious conversationを保存済みと推測しない。

## `redo`

current profile/policyをreadし、sectionごとの差分を作る。user/practice recordと
tenant policy requestを別operationにする。

## `check-integrations`

live probeだけ。接続状態以外を変更しない。

## Pacing

- 1 turn 2～3prompt
- typed answerが必要なら待つ
- skipは明示的`[PENDING]`
- write前にopen item一覧
- pause/saveの成否をreturned evidenceで表示
