> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 訴訟紛争法務 — Microsoft 365 Copilot Cowork 日本語パッケージ

日本の民事訴訟、労働審判、民事保全・執行、証拠・秘密性、催告・和解、
特許・民事主張表、案件・期限・外部弁護士管理を扱うskills-onlyパッケージです。

> **重要:** すべての分析、書面、通知案、主張表、時系列、status、deadlineは
> 有資格者レビュー用のドラフトです。AIは送信、提出、calendar登録、証拠提出、
> settlement受諾、preservation instructionの発出・解除、matter closeを自動実行
> しません。日本法モジュールは
> **DRAFT / qualified Japanese counsel review pending** です。
>
> **Cowork DLP blocker:** Microsoftの2026-06-22付Purview対応表ではCoworkの
> DLPとdata classificationは未対応です。SharePoint、OneDrive、Power Platform、
> connector等の保存・flow境界へDLPを適用しても、Cowork内prompt/taskがDLPで
> 保護されるとは表示しません。Cowork内DLPが必須なら機密資料を投入せず、本番導入を
> 停止します。
>
> **State prerequisite:** tenant-approved state gateway、SharePoint
> list/library、item-level ACL、append-only audit、Power Platform solutionは
> 本ZIPに含みません。live preflight成功まではread-only/manual draft modeです。

## 登録スキル — exactly 19

| ID | 移行区分 | 主な用途 |
|---|---|---|
| `brief-section-drafter` | direct | 訴状、答弁書、準備書面等のsection draft |
| `chronology` | direct | 事実、送達、提出、時効関連日付の時系列化 |
| `claim-chart` | direct | 日本特許claim chart / 民事要件事実chart |
| `demand-draft` | direct | 催告・契約通知・権利主張・和解通信のdraft |
| `demand-intake` | direct | demand前の法的性質、時効、通知、delivery intake |
| `demand-received` | direct | inbound demandの事実・期限・選択肢triage |
| `deposition-prep` | direct | 日本案件では証人・当事者尋問、陳述書、interview準備 |
| `matter-briefing` | direct | 1案件の手続・証拠・期限・執行status briefing |
| `privilege-log-review` | direct | 秘密性・提出拒絶根拠review |
| `subpoena-triage` | direct | 裁判所命令、照会、嘱託、当局要請の分類 |
| `legal-hold` | Power Platform front end | 内部preservation controlのissue/refresh/release/status |
| `matter-close` | Power Platform front end | 終局、確定、和解、控訴、執行を確認してarchive |
| `matter-intake` | Power Platform front end | 日本の事件番号、mints、送達、複数deadline等を登録 |
| `matter-update` | Power Platform front end | filing/service/order/hearing/finality/execution event追加 |
| `matter-workspace` | Power Platform front end | new/list/switch/close/noneとrestricted isolation |
| `oc-status` | Power Platform front end | 外部弁護士status request draft |
| `portfolio-status` | Power Platform front end | 複数案件・複数期限・staleness・hold status rollup |
| `cold-start-interview` | admin | 日本の手続、mints、証拠、時効、秘密性を含む設定 |
| `customize` | admin | profile/source/state設定を1変更ずつ安全に更新 |

登録集合は
`brief-section-drafter`, `chronology`, `claim-chart`, `demand-draft`,
`demand-intake`, `demand-received`, `deposition-prep`, `matter-briefing`,
`privilege-log-review`, `subpoena-triage`, `legal-hold`, `matter-close`,
`matter-intake`, `matter-update`, `matter-workspace`, `oc-status`,
`portfolio-status`, `cold-start-interview`, `customize`です。

## Coworkでの使い方

slash commandの実行は不要です。「この準備書面の第2節をdraft」「甲第1号証から
chronologyを作る」「この文書提出命令をtriage」「案件を切り替える」のように
依頼します。移行元の`/litigation-legal:...`、flags、state、keys、enumsは
正規参照labelとして保持し、Coworkでは会話stateへ変換します。

特に次を誤移植しません。

- 日本の証人・当事者尋問を米国のdepositionや`Rule 30`として扱わない。
- 日本の照会・嘱託・文書提出命令を`Rule 45` subpoenaとして扱わない。
- demand/和解通信へ`FRE 408`の自動的な排除・秘密性を約束しない。
- 内部preservation instructionを`Rule 37(e)`型の法定legal holdと断定しない。
- 弁護士法23条、民訴法197条・220条の保護を一般的な米国型privilege /
  work productと同一視しない。
- 裁判所裁判例検索を公開docketやPACER相当と扱わない。

## 保存、binding、restricted ACL

[Cowork実行・保存契約](references/cowork-runtime-contract.md)に従い、local
filesystemへ保存しません。

| 情報 | Microsoft 365保存先 |
|---|---|
| 会社・実務・利用者profile | SharePoint `profiles` document library |
| matter、evidence、hold、clean-team資料 | SharePoint `matters` document library、item-level ACL |
| review済み共有成果物 | SharePoint `outputs` document library |
| matter/event/deadline/preservation/setup/binding | SharePoint `state` list |
| 個人draft | OneDrive |
| verification/approval/write/flow/error | 追記専用SharePoint `audit` list |

state keyは
`tenantId + practiceId + scopeType + scopeId + recordType + recordId`、
binding keyは
`tenantId + practiceId + userObjectId + sessionId`です。bindingは非nullの
`matterId`と`expiresAt`を持ちます。practice-levelはfresh sessionにbindingが
存在しない状態で表し、`matterId: null`のactive bindingを作りません。
switch/noneは新しいsessionを要求し、closeは対象matterの全bindingをrevokeします。

`standard | heightened | restricted | clean-team`を分け、hold roster、evidence
register、trade secret、個人情報、社内調査、弁護士限定資料は必要最小限のgroupへ
限定します。central portfolio indexへ実質証拠や秘密情報を複製しません。

## 日本法レイヤー

- [日本法router](references/jurisdictions/ja-jp/README.md)
- [民事手続・digitalization](references/jurisdictions/ja-jp/civil-procedure-and-digital.md)
- [証拠・秘密性・preservation](references/jurisdictions/ja-jp/evidence-confidentiality-preservation.md)
- [催告・時効・和解](references/jurisdictions/ja-jp/demands-limitation-settlement.md)
- [特許・民事claim chart](references/jurisdictions/ja-jp/patent-and-claim-charts.md)
- [一次資料台帳](references/jurisdictions/ja-jp/source-register.md)
- [currency watch](references/jurisdictions/ja-jp/currency-watch.md)

2026-07-16 JST時点のe-Gov、裁判所、法務省等の公式情報を基礎にしています。
控訴の2週間の不変期間、電子送達の効力発生、労働審判の3回以内・異議2週間、
催告の6か月の完成猶予等は、起算点、経過措置、事件固有命令、休日規則を含めて
その会話で一次資料を再確認します。答弁期限は裁判所指定であり、米国の21日を
defaultにしません。

## Docket automation境界

[Power Platform互換contract](references/power-platform-automation-contracts.md)は、
`docket-reader`、`candidate-deadline-mapper`、`matter-tracker-writer`、
`approved-delivery`を別identity/connectionに分離します。candidate deadlineは
自動calendar entryになりません。弁護士とdocket ownerの二重確認後も、calendar
writeは別operation・別approvalです。本packageはagent、hook、subagent、
scheduled flow、managed solutionを含みません。

## Connectorとpackage境界

外部MCP候補は`connectors.draft.json`に隔離し、`manifest.json`へ登録せず、生成
ZIPへ含めません。宣言だけで`connected`と扱わず、管理者同意、per-user consent、
最小権限、保持、保存・flow DLP、live probeが必要です。

## 本番前blocker

strict validator、skills-ref 0.1.1、Microsoft 365 Agents Toolkit 1.1.12、
tenant smoke test、SharePoint concurrency/isolation/ACL test、Power Platform
solution test、移行元法域review、日本法有資格者reviewが必要です。
