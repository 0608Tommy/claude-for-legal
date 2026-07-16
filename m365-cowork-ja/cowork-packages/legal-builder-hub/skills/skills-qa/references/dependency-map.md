> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Dependency map

## Upstream

- company/practice/user/matter profile
- prior skill output
- source document/database
- connector/MCP/API
- tool permission
- law/guidance/reference

## Downstream

- draft/output
- profile/state/catalog/queue
- notification/destination
- file/assignment/flow
- another skill/agent

## Automatic trigger

- hook event
- scheduled agent/flow
- ambient recommendation
- external webhook

## Breakage

各dependencyについて:

- unavailable時のfallback
- incorrect inputのrecipient
- cross-tenant/practice/matter risk
- irreversible/consequential action
- audit/rollback

## Coverage

missing command/agent/hook/manifest/connector/script/referenceを列挙する。SKILL.mdだけから
「none」と推測しない。
