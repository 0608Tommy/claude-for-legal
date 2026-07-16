> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 移行元Employment Legal behavior

## Source identity

- plugin ID: `employment-legal`
- source version: `1.0.2`
- source skills: 20
- registered target skills: 18
- source MCP names/URLs:
  - `Slack` — `https://mcp.slack.com/mcp`
  - `Google Drive` — `https://drivemcp.googleapis.com/mcp/v1`

canonical skill IDs、slash labels、flags、JSON/YAML/frontmatter keys、enum、URL、
tool/product name、placeholder構造を翻訳・改名しません。

## 20→18 disposition

`internal-investigation`は登録せず、次の5 callerへcompileします。

- `investigation-open`
- `investigation-add`
- `investigation-query`
- `investigation-memo`
- `investigation-summary`

carryover: privilege/confidentiality formation、restricted matter isolation、
audience stripping、open/add/query/memo/summaryのfive-mode state、source coverage、
needle-finding、entry ID citation、memo update。

`international-expansion`は登録せず、`expansion-kickoff`と`expansion-update`の
skill-local referenceへcompileします。

carryover: EOR versus entity framing、dependency tracker、tax/finance/HR/
outside-counsel routing、country briefing、persistent state。

source `leave-tracker` skillとagentはtarget `leave-tracker`へmergeし、current-law
check、decision-point alerts、clean-leave summary、actual schedule、coverageを
保持します。scheduleは別のapproved Power Platform solutionがある場合だけ表示します。

## Preserved workflow

- cold-start: quick/full、resume、redo、redo-section、check-integrations、
  jurisdiction footprint、seed documents、escalation、live connector probe。
- customize: current→proposed→impact→confirm、one change。
- hiring: work location、classification、covenant、background、offer content、
  consequential gate。
- termination: high-risk scan、documentation、jurisdiction、severance/release、
  escalation、human decision。
- policy/handbook: core draft、jurisdiction delta、cross-reference、promise impact、
  publish gate。
- wage/hour: jurisdiction first、current source、calculation inputs、close-call flag。
- classification: prospective-only gate、purpose-specific tests、factor table、
  gap analysis、remediation route。
- investigation: source checklist、all-document disposition、surface ratio、
  conflicts/gaps、credibility、audience-specific summary。
- expansion: single-block intake、structure framing、cross-functional questions、
  dependency update。
- matter: `new | list | switch | close | none`。

## Japanese route

`ja-JP`では米国固有の`at-will`, `FLSA`, `FMLA`, `OWBPA`, `WARN`, `COBRA`,
`Upjohn`, `Weingarten`, `Garrity`をdefaultとして適用しません。日本の労働条件、
解雇、労働時間、休業、労働者性、通報、調査、社会保険、派遣・供給、移民へ
routeします。他法域のmatterは、その法域のcurrent primary sourceとqualified
counselへrouteし、日本法をgeneric global defaultにしません。

## Consequential boundaries

sourceの「draft、flag、gate」の役割を保持し、AIがoffer送信、採用、discipline、
termination、leave/accommodation、payroll/benefit、investigation finding、
external response、filingを決定・実行しません。
