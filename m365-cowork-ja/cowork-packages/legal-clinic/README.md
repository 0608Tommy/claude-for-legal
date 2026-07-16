> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# リーガルクリニック — Microsoft 365 Copilot Cowork 日本語パッケージ

日本の大学・法科大学院・弁護士会・法律事務所等が運営するリーガルクリニック向けの
skills-onlyパッケージです。相談受付、利益相反pre-screen、期限候補、調査roadmap、
内部memo、依頼者向けdraft、監督review、学期引継ぎを支援します。

> **重要:** 本packageは弁護士・依頼者関係を成立させず、受任、代理、法律相談、
> 和解、署名、裁判所・行政庁への提出を行いません。学生は日本の弁護士資格を持つ
> 責任弁護士の明示した範囲で補助します。すべての法律判断と外部向け成果物は
> 責任弁護士とclinic supervisorの確認前提です。
>
> 日本法moduleは **DRAFT / qualified Japanese counsel and clinic supervisor
> review pending** です。2026-07-16 JST時点の公式一次資料を基礎にしていますが、
> source/effective dateを各matterで再確認します。
>
> **State prerequisite:** tenant-approved state gateway、SharePoint
> list/library、item-level ACL、append-only audit、Power Platform solutionは本ZIPに
> 含みません。live preflight失敗時はread-only/manual draft modeだけです。
>
> **Cowork DLP blocker:** 2026-07-16時点のMicrosoft公式情報に従い、Cowork内prompt
> 自体へDLP/data classificationが適用されるとは表示しません。保存・flow境界のDLPで
> 足りない場合、機密資料を投入せずproductionを停止します。

## 登録スキル — exactly 14

| ID | 移行区分 | 主な用途 |
|---|---|---|
| `build-guide` | admin | practice-area guideとpedagogy設定 |
| `client-comms-log` | Power Platform front end | 通信記録のadd/read/summary/patterns |
| `client-intake` | direct | conflict-first相談受付とdeadline handoff |
| `client-letter` | direct | 予約・資料依頼等の依頼者向けdraft |
| `cold-start-interview` | admin | clinic、責任弁護士、data、supervisionの初期設定 |
| `customize` | admin | profileを1変更ずつ安全に更新 |
| `deadlines` | Power Platform front end | deadline candidateのadd/report/update/complete/close |
| `draft` | direct | 日本の裁判所・行政庁・依頼者向け文書の初稿 |
| `memo` | direct | 学生分析用の内部memo scaffold |
| `ramp` | direct | 学生のsemester onboardingと模擬演習 |
| `research-start` | direct | 日本法一次資料から始めるresearch roadmap |
| `semester-handoff` | Power Platform front end | conflict-gated学期引継ぎ |
| `status` | direct | client/internal/court/agency別status draft |
| `supervisor-review-queue` | Power Platform front end | version-specific lawyer review queue |

内部helperは登録しません。`form-generation`は`draft`へcompileし、
`plain-language-letters`はroutine intentを`client-letter`、substantive intentを
`status`へrouteします。

## Canonical label

Coworkではslash commandを要求しませんが、移行互換のcanonical labelは
`/legal-clinic:<skill-id>`です。logical targetはdirectが
`ja-jp.cowork.legal-clinic.<skill-id>`、stateful front endが
`ja-jp.power.legal-clinic.<skill-id>`、adminが
`ja-jp.admin.legal-clinic.<skill-id>`です。ID、state、field、enumはASCIIを正本に
し、日本語は表示labelとして使います。

## 保存、matter binding、restricted ACL

[Cowork実行・保存契約](references/cowork-runtime-contract.md)に従います。

| 情報 | Microsoft 365保存先 |
|---|---|
| clinic/practice/user profile、guide | SharePoint `profiles` library |
| conflict pre-screen、prospect、matter、source | SharePoint `matters` library |
| review済み共有成果物 | SharePoint `outputs` library |
| deadline、communication、review、handoff、setup、binding | SharePoint `state` list |
| 個人draft | OneDrive |
| verification、approval、write、flow、error | 追記専用SharePoint `audit` list |

active binding keyは
`tenantId + practiceId + userObjectId + sessionId`で、非nullの`matterId`と
`expiresAt`を必須にします。practice modeはfresh sessionにbindingが存在しない状態
です。client/matter switchはcurrent bindingをrevokeして同じ会話を停止し、新しい
Cowork conversationを要求します。会話名、過去memory、display nameからmatterを
推測しません。

`deadlines`と`supervisor-review-queue`はscopeを分離します。matter modeはexact
1件のactive bindingを要求します。portfolio modeはfresh unbound session、explicit
portfolio authority、pseudonymous minimum metadataだけです。portfolioから1件を開く
場合はcurrent conversationを停止し、新しいbound conversationを開始します。

archive/closeはmatter status transitionと対象generationの全active binding revokeを
gatewayのall-or-none transactionで実行できる場合だけ許可し、1件でも失敗すれば
transitionをblockします。reactivateはbinding generationを増やし、fresh conversation/
fresh bindingを要求します。

identity mapping、safe contact、health/disability、immigration、criminal、child/
family/DV、interpreter、My Numberは分離itemと最小権限ACLを使います。central indexへ
実名や実質factsを複製しません。

## 日本法と監督境界

- [日本法router](references/jurisdictions/ja-jp/README.md)
- [一次資料台帳](references/jurisdictions/ja-jp/source-register.md)
- [clinic、資格、利益相反、守秘](references/jurisdictions/ja-jp/clinic-law-and-supervision.md)
- [依頼者dataと安全](references/jurisdictions/ja-jp/privacy-client-data.md)
- [手続、digitalization、期限](references/jurisdictions/ja-jp/procedure-deadlines.md)
- [legal aid、能力、accessibility、通信](references/jurisdictions/ja-jp/client-access-and-communications.md)
- [currency watch](references/jurisdictions/ja-jp/currency-watch.md)

米国のstudent-practice rule、`Certified Legal Intern`、ABA rules、FRCP work
product、州別時効・送達・提出practiceを日本へ移植しません。日本に全国一律の
学生代理資格があるとは扱わず、責任弁護士が承認したstudent participation matrixを
使います。matrixはinternal policyで、法的権限又は弁護士法72条riskの治癒では
ありません。弁護士法72条について「無償だから常に適法」と断定しません。

information barrierはconflict clearance/waiverではありません。disclaimerだけで
engagement不存在を保証せず、実際のadvice・undertaking・representation等がscopeを
成立又は拡大し得るため、責任弁護士がconductを確認します。

Houterasuは法律相談援助、代理援助、書類作成援助、国選弁護等関連業務を分けます。
student、AI、cloud、vendorは弁護士と同じ守秘・手続保護を自動的に受けるとは
表示しません。

## Artifact separation

内部memo、依頼者向けsanitized draft、deadline/communication tracker、裁判所・行政庁
向けdraftは別artifact、別ACL、別review statusです。内部分析や秘密性判断をclient
draft又はfiling draftへ自動流用しません。AIはsend、post、file、sign、accept、
decline、settle、calendar、approve、release、closeを自動実行しません。

## Automation compatibility

[Power Platform compatibility contract](references/power-platform-automation-contracts.md)
は`client-comms-log`、`deadlines`、`semester-handoff`、
`supervisor-review-queue`等のfront endを定義します。source pluginにはagent又は
managed-agent cookbookがないため、存在を捏造しません。本packageはflow、solution、
connection、scheduleを含まず、solution ID/version/owner/scope/live runをstateで
確認できる場合だけautomation availableと表示します。

deadlineは常にcandidateです。責任弁護士とdocket ownerがtrigger、送達、条文、
計算、休日、事件固有命令を確認しても、calendar writeは別operation・別approvalです。

canonical machine contractは
`references/clinic-state-payloads.schema.json`、fixtureは
`references/clinic-state-payload-examples.json`、bypass fixtureは
`references/clinic-state-payload-negative-examples.json`、cross-array semantic
validatorは`references/validate_clinic_state_payloads.py`です。profile、setup、binding、
archive/close、communication、deadline、review、handoffをstrictに検証し、state
recordは`tracker-record`へ標準化します。

`criminal | immigration | housing | benefits`はapproved source cardなしにsubstantive
rule、eligibility、deadline、formを生成しません。2026-04-01 family reform、DV
protection orderの地方裁判所route、児童虐待のhuman reporting、民法の完成猶予/更新、
民事電子送達/time computation/transitionをcurrent official sourceで確認します。

権利・期限・scope・advice・court/agency content等のconsequential translationは、
responsible-lawyer legal reviewとcompetent-language reviewの両方が必要です。

## 本番前blocker

- strict target validator
- skills-ref 0.1.1
- Microsoft 365 Agents Toolkit 1.1.12
- tenant smoke test
- SharePoint concurrency、matter isolation、restricted ACL test
- Power Platform solution test
- 移行元法域review
- qualified Japanese counselとresponsible clinic supervisorのreview

上記が完了するまでstatusはDRAFTです。
