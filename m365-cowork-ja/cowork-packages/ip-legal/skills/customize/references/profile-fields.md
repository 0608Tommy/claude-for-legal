> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Customizable profile fields

| Scope | Examples | Downstream |
|---|---|---|
| company | name、industry、practice setting、operation jurisdictions | all skills |
| user | canonical role、Japanese professional role、attorney route | header、approval |
| practice | active IP areas、jurisdictions、outside counsel | routing |
| enforcement | posture、approvers、automatic escalation | C&D/takedown/triage |
| trademark | watch、owner、search source | clearance/portfolio |
| patent | strategy、invention intake、employee rule、secrecy owner | invention/FTO |
| copyright | platform route、approver | takedown |
| trade-secret | classification、control owner | triage |
| OSS | accepted/review/blocked licences、release process | OSS review |
| transaction | assignment/licence/recordal positions | clause review |
| portfolio | source、owner、verifier、window、alert candidate | portfolio |
| matter | enabled、cross-matter default、clean-team | all substantive skills |
| integration | live status、scope、fallback | source coverage |
| production | Cowork DLP requirement、blocker | production gate |

legal-review status enum:
`pending | in-review | approved | blocked`

connection status enum:
`connected | configured-unverified | not-connected`

fieldを削除せず、`not-configured | deprecated | disabled-with-reason`等のstatusと
historyを保持します。
