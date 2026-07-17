---
name: build-guide
description: >
  日本のリーガルクリニック責任弁護士・監督者がpractice-area guideを作成し、相談質問、pedagogy mode、固定lawyer gate、cross-skill check、公式source、data restrictionを設定するadmin skill。assist/guide/teachで教育方法を調整しても、資格・利益相反・受任・期限・外部送信・提出gateを弱めない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: admin
  logical-target-id: ja-jp.admin.legal-clinic.build-guide
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Build guide

canonical label: `/legal-clinic:build-guide [practice-area]`

## Mandatory admin / lawyer gate

1. `references/common/cowork-runtime-contract.md`を読み、exact current user、
   clinic profile、responsible lawyer、supervisor、gateway、profiles/audit listをlive
   preflightする。失敗時はguide draftだけで、保存済みと表示しない。
2. callerはauthenticated supervisorであり、legal/professional gateの変更は
   responsible Japanese lawyerも承認する。student又は一般staffは閲覧・提案だけ。
3. conflict、engagement、scope、student participation、privacy、retention、
   emergency、substantive external review、filing gateはnon-configurable floor。
   barrierはclearanceでなく、student matrixはinternal policy/非権限、disclaimerは
   actual conductを支配しない。
4. practice area、forum、jurisdictionをexact profileで確認し、米国templateを日本へ
   silent移植しない。
5. current official source、future-law、clinic policy、pedagogyを別layerにする。
6. proposed guideはOneDrive admin draft、approved guideはSharePoint `profiles`の
   `practice-guide` record。create/update、approval、publishは別operation。
7. exact item ID、latest ETag、version、idempotency、diff、fresh confirmation、
   append-only auditを使う。
8. Cowork内DLPが必要ならclient-derived exampleを投入せず、synthetic exampleだけ。

Japan layer:
`references/common/ja-jp/clinic-law-and-supervision.md`。

## 会話state

`select-area` → `intake` → `pedagogy` → `review-gates` →
`cross-skill` → `sources-and-forms` → `data-controls` → `review-draft` →
`confirm-write` → `conditional-write` → `audit`

既存guideがある場合は`revise | start-fresh-draft | show-current`を選ぶ。approved versionを
overwriteせずnew versionにする。

## Guide content

### 1. Intake

- conflict pre-screenで必要なnames/aliases/related parties
- conflict clear後に聞くpractice-specific questions
- civil/criminal/administrative/family/labor等のforum route
- urgent danger、custody、hearing、limitation、filing trigger
- safe contact、language、interpreter、capacity/accommodation
- good-fit / refer-out candidate
- Houterasu:
  `consultation-aid | representation-advancement |
  document-preparation-advancement | appointed-criminal-counsel`
- `criminal | immigration | housing | benefits` approved source-card requirement
- family reform、DV district-court route、child-abuse human reporting route

`good-fit`はAIによる受任判断ではない。出力は
`受任判断未了 — responsible lawyer decision required`。

### 2. Pedagogy

ASCII enum:

- `guide`: structure、question、checklistを示し、学生がsubstanceを作る。
- `assist`: AIがreview用draftを作り、学生が検証・修正する。
- `teach`: 学生が先に作り、AIはSocratic feedbackを行う。

defaultとartifact別overrideを記録する。

```yaml
pedagogyModeDefault: guide
pedagogyModeClientLetter: guide
pedagogyModeMemo: guide
pedagogyModeDraft: guide
```

modeはlegal authorityを変えない。`assist`でもAI又はstudentがadvice、sign、file、
accept/decline、settle、closeを行わない。

### 3. Fixed review gates

常にresponsible lawyer:

- substantive client communication、bad news、scope、deadline、strategy
- conflict waiver、受任/辞任、capacity/guardian判断
- settlement、court/agency draft、signature、filing
- case close、retention/destruction、preservation release

routine appointment logistics等はresponsible lawyerがlocked template、safe-contact、
permitted student activityを明示した場合だけtemplate-level approvalを設定できる。

### 4. Cross-skill checks

skill ID、利用場面、input restriction、reviewer、output artifact、禁止operationを記録する。
他pluginを呼ぶ場合もclient/matter binding、ACL、severity floor、responsible lawyer gateを
引き継ぐ。外国法skillの結論を日本法へ流用しない。

### 5. Official sources / forms

法令、裁判所規則、official form、agency material、JFBA/local bar rule、clinic
precedentを分類し、official URL、effective date、checked date、reviewerを記録する。
criminal又はadministrative formをcivil templateから作らない。
日弁連の職務基本規程、public lawyer search、業務広告規程・指針を別sourceとして扱う。

### 6. Data and safety

identity、safe contact、health、immigration、criminal、child/family/DV、interpreter、
My Numberのcollection/ACL、retention、internal preservation control、court order、
destinationを指定する。client-derived
teaching exampleはde-identificationとresponsible lawyer approvalが必要。

APPIをgeneric GDPR lawful-basis fieldへ短縮せず、利用目的、要配慮、委託、第三者提供、
外国にある第三者への提供、例外、本人対応、My Numberを分ける。consequential
translationはresponsible-lawyer legal reviewとcompetent-language reviewを両方固定する。

## Guide schema

```yaml
practiceAreaId: "[ASCII kebab-case]"
displayNameJa: "[Japanese]"
forumTypes: []
intakeQuestionsAfterConflictClearance: []
redFlags: []
fitCriteriaCandidates: []
referOutCandidates: []
pedagogyModes: {}
fixedLawyerGates: []
routineTemplateExceptions: []
crossSkillChecks: []
officialSources: []
approvedForms: []
restrictedDataRules: []
urgentRoutingId: "[ID]"
approvedBySupervisor: "[object ID]"
approvedByResponsibleLawyer: "[object ID]"
version: 1
```

## Completion

draft/approved version、exact item ID/eTag、approvers、unresolved source/data issuesを
表示する。test runはsynthetic matterだけで行い、real client workを自動開始しない。

## 行わないこと

- studentによるguardrail変更
- lighter-touchをsubstantive lawyer review免除として実装
- 受任、conflict clearance、deadline ruleをAI決定
- client dataをtraining exampleへ自動転用
- source不明の日本法・formをapprovedとして保存
- flow、guide publish、external sendが完了したと未検証で主張
