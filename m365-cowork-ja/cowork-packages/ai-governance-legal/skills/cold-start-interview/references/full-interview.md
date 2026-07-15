> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# フル設定インタビュー

## Part 0 — 利用者、practice setting、接続

### 利用者

- Lawyer / legal professional
- Non-lawyer with attorney access
- Non-lawyer without regular attorney access

非弁護士には、最終判断前の停止と弁護士用ブリーフを説明する。

### Practice setting

- Solo / small firm: escalationを「外部専門家・同僚への相談」に置換
- Midsize / large firm: approval chain
- In-house: GC/CLO、business、CISO/CPO
- Government / legal aid / clinic: supervisionと法的権限
- Other: 自由記述

### 接続

SharePoint、OneDrive、任意MCPをライブprobeする。`connected | configured-unverified | not-connected`。

## Part 1 — AI活動とシステム

会社の事業、販売先、チャネルを把握する。次を確認する。

- generative / classification / recommendation / automation
- customers / employees / applicants / no direct human impact
- build / fine-tune / third-party use
- model card / system card
- vendor owner
- consequential decisions

EUが関係する場合、システムごとにroleとtierを台帳へ登録する。

### Shadow AI

- Slack AI、Microsoft Copilot、Salesforce Einstein、Gmail、Zoom等の組込み機能
- ChatGPT、Gemini、Claude、Perplexity等の非公式利用
- CRM、HR、文書管理等に埋め込まれたAI

未評価は `[UNDOCUMENTED — NEEDS TRIAGE]` とする。

## Part 2 — 規制footprint

- customers、employees、data subjects、operationsの所在地
- cross-border reach
- AI-specific law、biometric、automated decision、sector rules
- contractual AI requirements
- regulator investigation、commitment、consent order
- government procurement certification

日本についてはAI法、AI事業者ガイドライン、個人情報、労働、著作権、消費者、競争、業法を必要に応じて分ける。

## Part 3 — Use case registryとred lines

既存registry/policy/allowlistがあれば先に読む。なければ具体例で `Approved / Conditional / Never` を聞く。

Deployer例:

- résumé screening
- performance review summary
- human-reviewed customer support draft
- expense anomaly flag
- legal first draft

Builder例:

- personalized recommendation
- lead scoring
- no-human automated decision

各例で条件、理由、必要review、disclosure、vendor、human oversightを記録する。

Red line候補を提示するだけで決めない:

- biometric
- emotion detection
- political/religious inference
- fully automated adverse decision
- children
- confidential data in unapproved tools

Governance tierと承認経路を取得する。

## Part 4 — Governance、escalation、external commitments

- team sizeと所属
- vendor relationship owner
- AI risk owner
- standard / elevated / highの承認者
- incident、regulator inquiry、employee misuse
- outside counsel / specialist consultation
- public AI principles、voluntary commitments、transparency report

## Part 5 — Seed documents

各資料の`itemId`、version、read coverage、権限を記録する。

1. AI / acceptable use policy
2. prior AIA
3. vendor AI agreement
4. system inventory
5. allowlist / blocklist

資料なしの場合、baselineとinterview positionを明確に分ける。

## Part 6 — Outputs

- reviewed shared deliverableの保存先
- personal draftの保存先
- actual AI policy item
- naming convention
- policy review cadence
- last acknowledged sweep
- retained audit fields

`policy-monitor` が読める正確なSharePoint scopeを設定する。
