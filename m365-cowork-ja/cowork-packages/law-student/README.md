> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 法学学習支援 — Microsoft 365 Copilot Cowork 日本語パッケージ

法科大学院・法曹コース、司法試験・司法試験予備試験、司法修習、一般の法学学習と、
明示的に選択した米国JD/bar prep等を分離して支援するskills-onlyパッケージです。

> **学習用:** 出力は `STUDY NOTES — NOT LEGAL ADVICE` です。法的助言、提出物、
> 公式解答、公式採点、合否判定、履修登録、提出、LMS操作、外部投稿、scheduled
> tutoringを提供しません。実在する依頼者・事件・修習記録は入力しません。
>
> **日本法レビュー:** 日本法・日本の法曹養成・試験内容は、2026-07-16 JSTまでに
> 確認した公的資料を基礎にした **DRAFT / qualified review pending** です。
>
> **Cowork DLP blocker:** 2026-07-16時点でCowork内prompt/taskのDLPとdata
> classificationを利用できるとは扱いません。Cowork内DLPが必須なら機密資料を
> 投入せず、本番利用を停止します。
>
> **State prerequisite:** tenant-approved gateway、SharePoint
> list/library、ACL、conditional write、append-only audit、Power Platform
> solutionは本ZIPに含みません。live preflightに失敗した場合はread-only/manual
> draftだけで、profile、進捗、deck、学習計画を保存済みとは表示しません。

## 登録skill — exactly 13

| ID | 移行区分 | 日本語での用途 |
|---|---|---|
| `bar-prep-questions` | direct | 司法試験・予備試験または選択した米国barの演習 |
| `case-brief` | direct | 判例・裁判例の読解scaffold |
| `cold-call-prep` | direct | 授業準備。指定教材に基づく質問演習 |
| `cold-start-interview` | admin | 法体系、学習段階、科目、試験、出典、AI policyの初期設定 |
| `customize` | admin | profileの1変更ずつの安全な更新 |
| `exam-forecast` | direct | 予測ではなく過去問分析・学習配分 |
| `flashcards` | Power Platform front end | version付きcardの生成・演習・進捗候補 |
| `irac-practice` | direct | IRACまたは日本語答案scaffoldへの形成的フィードバック |
| `legal-writing` | direct | レポート・答案・起案の構造フィードバック。書き直さない |
| `outline-builder` | direct | 自分で作るoutlineの構造化・不足確認 |
| `session` | direct | fixed-count演習。必要ならaudited state更新へhandoff |
| `socratic-drill` | direct | 一問ずつのソクラテス式演習 |
| `study-plan` | Power Platform front end | 生活制約と公式日程に基づく学習計画 |

deployed skill IDと旧来のlabel `/law-student:<skill-id>`、`--mbe`、
`--essay`、`--flashcards`、`--tanto`、`--ronbun`、`--koutou`、
`--kian`等はASCIIのまま保持します。Coworkではflagを会話stateへ変換します。

## 日本の学習route

日本語UIだから日本法とは推測しません。`ui_locale`と`study_legal_system`を別々に
解決し、次を区別します。

1. 制度上の法曹コース（`legal-profession-course`）
2. genericな学部法学（`undergraduate-law`）
3. 法科大学院の`mishu-3-year`・`kishu-2-year`
4. 司法試験予備試験の短答・論文・口述
5. 司法試験の短答・論文
6. 司法修習の導入・分野別・選択型・集合・司法修習生考試
7. 一般の日本法・比較法学習
8. 米国JD/LLM、UBE、NextGen、state-specific等の明示的な別route

`1L/2L/3L`、MBE、MEE、Bluebook、Barbri等を日本の制度へ置き換えません。
日本の法科大学院や試験を米国用語の同義語として表示しません。

`bar_or_exam.exam_format`はofficial source/version付きobjectとして保存し、
`customize`、`study-plan`、`session`で同じversionを確認します。司法試験は
短答・論文、予備試験は短答→論文→口述のprerequisiteを分けます。

## 2026年の公的資料

[公的source・2026試験](references/official-sources-and-2026-exams.md)を参照します。
司法試験・予備試験では`exam-cutoff`、`currently-effective`、
`future-enacted`、`historical`、`pending-proposal`を分けます。2026年試験用の
`exam-cutoff`は原則2026-01-01です。
`future-enacted`は公布済み・未施行だけです。cutoff後に施行され現在有効な法は
`currently-effective`かつ`excluded-post-cutoff`で、試験基準法へ含めません。

2026-07-16時点で司法試験は実施中です。2026-07-21の公式問題公開までは、
漏えい、受験者の記憶、試験委員情報、topic speculationを使わず、2025年以前の
公式公開資料だけで演習・分析します。法務省は出題趣旨や採点実感を公開しますが、
「公式模範答案」とは表示しません。

## 学習・academic integrity

- 学校・授業・試験のAI policy、honor code、assignment permissionをexact
  source/version付きで確認します。
- graded workで許可が不明なら、答案の内容生成・解答提示を停止します。
- `case-brief`、`outline-builder`、`legal-writing`、`irac-practice`は学生の
  読解・執筆を置き換えません。
- Socratic drillは一問ずつ提示し、学生の試行前に解答を開示しません。
- 実在する判例、法令、条文、判旨、出題趣旨、採点実感、引用を創作しません。
- 商用casebook・予備校教材は、利用者が権限を持つ範囲を超えて複製しません。

## 保存・Power Platform境界

[Cowork実行・保存契約](references/cowork-runtime-contract.md)に従います。

| 情報 | Microsoft 365保存先 |
|---|---|
| learner/profile、course、exam mode、source pointers | SharePoint `profiles` |
| approved syllabus、rubric、AI policy、教材pointer | SharePoint `matters`相当のauthorized study library |
| review済み共有study artifact | SharePoint `outputs` |
| setup、plan、session、deck metadata、progress、verification | SharePoint `state` |
| 個人draft、outline、feedback | OneDrive |
| read、verification、confirmation、write、failure | append-only SharePoint `audit` |

`flashcards`、`study-plan`、`cold-start-interview`、`customize`は、別途導入された
audited gateway/Power Platform flowのfront endです。本packageだけではwrite、
schedule、reminder、LMS連携は動きません。`session`の結果も、保存前に人が確認し、
audited `study-plan` state handoffを使います。

stateはshared schemaどおり
`tenantId + practiceId + scopeType + scopeId + recordType + recordId`です。
個人progressは`scopeType: user`、session result/setupは`scopeType: session`。
study固有metadataは`payload`、auditでは`details`へ入れます。
[schema-valid state fixtures](references/state-fixtures.md)をpackage-localに含めます。

## Helper・agent・hookの境界

law-studentの移行mapにはinternal helper skillはありません。`session --flashcards`
はcanonical `flashcards --session <n>`への明示的handoffを作り、動的に実行したとは
表示しません。question routingはskill-local contractへcompileします。source
pluginにはagentがなく、`hooks/hooks.json`は空です。このため
agent、scheduler、hook automationは本packageへ移しておらず、失われた自動behaviorも
ありません。Cowork skillがagent、hook、scheduled tutoringとして常時動くとは
表示しません。

司法試験合格だけで弁護士とは表示しません。在学中受験資格合格者の法科大学院修了、
司法修習生採用、修習、司法修習生考試、弁護士資格、所属弁護士会経由の日弁連
弁護士名簿登録を別段階として扱います。

## Connector境界

sourceのSlack、Google Drive、CourtListener、Descrybe候補は
`connectors.draft.json`へ隔離し、`manifest.json`や生成ZIPへ登録しません。
live probe、管理者同意、per-user consent、最小権限、保持、保存・flow DLPが必要です。
CourtListenerは米国裁判例向けで、日本のauthorityを検証しません。日本法はe-Gov、
法務省、文部科学省、裁判所等の公的sourceを優先します。

## 本番前gate

- target validator
- `skills-ref==0.1.1`の全13 skill検証
- Microsoft 365 Agents Toolkit `1.1.12` manifest/package検証
- tenant smoke test
- SharePoint scope、ACL、ETag、idempotency、audit test
- Power Platform solution/connection test
- 原法域の教育workflow review
- 日本法・日本の法曹養成に詳しい有資格者review
