> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — legal aid、意思決定支援、accessibility、依頼者communication

**状態:** DRAFT — qualified Japanese counsel and clinic supervisor review pending

## Clinic eligibility vs legal aid

clinicの対象基準とHouterasu等の制度要件を分ける。少なくとも:

- `consultation-aid`: 法律相談援助
- `representation-advancement`: 代理援助の費用立替
- `document-preparation-advancement`: 書類作成援助の費用立替
- `appointed-criminal-counsel`: 裁判所の選任と法テラスの国選弁護等関連業務

を別program recordにする。相談援助を受任・代理援助と扱わず、費用立替をgrant又は
clinic eligibilityと扱わず、国選弁護を民事扶助へroutingしない。means、matter type、
forum、merits、client responsibility、scopeをactual program sourceで確認する。

AIはeligibility、受任、referral acceptanceを決めず、route candidateと不足factsを
責任弁護士へ示す。

## Capacity / supported decision-making

年齢、成年後見等のtype、代理権資料、利益相反、本人意思、communication needを
確認する。guardian又はsupport personの存在だけで本人の意思を無視しない。AIは
capacity又は代表権を決定しない。

子ども又は未成年者を含むmatterではclient identity、法定代理、利益相反、情報共有、
安全、school/contact detailをrestrictedにし、責任弁護士がscopeを判断する。

2026-04-01 family reformが関係する場合、事件/行為日、existing order、parental
authority、子の利益、DV/虐待facts、経過措置をapproved current source cardで確認する。
AIはjoint/sole parental authority、capacity、best interestsを決めない。

児童虐待が疑われる場合、児童虐待防止法6条等のcurrent textと守秘との関係を
responsible lawyer又はdesignated humanが直ちに評価し、Art.6の`速やかに`を踏まえて
**prompt human notification**を行う。
AI/cloudへの入力又はqueue登録は通告ではなく、AIは通告したと表示しない。
human route candidateは児童相談所虐待対応ダイヤル`189`。誰が、どのsafe device/
channelから、何を伝えるかを人が決め、差し迫る危険では110/119も検討する。

## Accessibility / language

- preferred language、読み書き、通訳、手話、読み上げ、移動・時間上の配慮
- interpreter identity、independence、confidentiality、qualification
- document format、font、plain explanation、理解確認
- communication assistanceとlegal authorityの区別

「6th-grade reading level」を日本語へ機械的に移植せず、文化庁のやさしい日本語等を
参考に、必要な法律用語は省略せず短く説明する。

権利、義務、deadline、scope、advice、同意、court/agency content等のconsequential
translationは、同じartifact version/hashについてresponsible-lawyer legal reviewと
competent-language reviewの**両方**を要求する。AI translation、bilingual student、
client family memberだけをapprovalにしない。

## Client-facing draft

依頼者向けartifactは次を明確にする。

- 何が起きたか
- 次に何が起きるか
- 依頼者がすること
- deadlineがcandidateかverifiedか
- 安全な連絡方法
- clinicのscopeと責任弁護士

内部分析、credibility assessment、conflict detail、accepted risk、守秘評価を除く。
学生のroleは`法科大学院生（実習生）`等の正確な表示とし、弁護士又は認定代理人と
誤認させない。

## Routine vs substantive

責任弁護士が固定文面を承認した予約、場所、持参物等のpure logisticsだけをroutineと
し得る。deadline、scope、法的position、strategy、bad news、adverse ruling、
settlement、case closingはsubstantiveで、責任弁護士のitem-by-item reviewを要求する。

draftとsend/postは別operation。safe-contact、destination、approved version、
reviewer、delivery evidenceを確認する。

## Emergency routing

生命・身体の危険、DV/stalking、自傷他害、身柄拘束、直近の裁判/行政期限等では、
通常のclient communication templateを使わずapproved emergency routeを示す。
AIは緊急サービスではなく、clinic又は弁護士のresponseを保証しない。必要に応じて
警察110、消防・救急119等へ本人又は人間の支援者が連絡する選択肢を示せるが、
個別状況における通報をAIが決定・実行しない。

DV防止法上の保護命令はcurrent source cardで地方裁判所routeを確認し、家庭裁判所へ
自動routingしない。`criminal | immigration | housing | benefits`はapproved source
cardがない限り、minimum facts、安全・緊急routing、specialist referralだけに限定する。

DV相談route candidateは`DV相談ナビ #8008`。call log、shared phone、caller ID、
browsing/communication history、相手方のmonitoring、利用可能端末、受付時間を
safe-contact recordで確認し、安全でない端末からの発信を自動提案しない。

## Communication log

必要最小限の事実、language、interpreter/accessibility、action item、follow-up candidate、
approved artifact、reviewer、delivery evidenceを記録する。tone、mental state、
family dynamicを推測又は不用意にlabelしない。correction entryを追加し、過去entryを
書き換えない。append-only integrityとretention/deletionを分ける。
