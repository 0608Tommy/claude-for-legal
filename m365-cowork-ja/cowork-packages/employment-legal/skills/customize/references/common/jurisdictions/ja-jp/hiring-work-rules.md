> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 採用、雇用契約、就業規則

**状態:** DRAFT — qualified Japanese counsel review pending

## 採用・労働条件 [B/G]

勤務地と事業場、雇用主entity、職務内容と変更範囲、就業場所と変更範囲を確認します。
`労働条件通知書 / 雇用契約書`では少なくとも次をreviewします。

- 無期/有期、期間、更新基準、更新上限、試用
- 無期転換・雇止めに関する現行明示
- 労働時間制、始終業、休憩、休日、時間外、36協定
- 賃金、締切/支払、控除、賞与/退職金の根拠
- 退職、解雇、discipline、休業、休暇
- applicable work rules、CBA、労使協定

募集広告と内定後の条件が異なる場合、変更経緯・明示・同意を確認します。職業安定法
上の正確な募集情報と現行明示項目をofficial sourceで確認します。

## Contract type

日本matterでは`exempt/non-exempt`ではなく、次を事実で分類します。

- indefinite / fixed-term
- full-time / part-time
- direct employee / dispatched worker / genuine outsourcing
- managerial-supervisory candidate under LSA Article 41
- discretionary-work / highly skilled system candidate

labelやsalaryだけで法的statusを確定しません。

## Equal opportunity・harassment・accommodation

性別、妊娠・出産、育児介護休業、年齢、障害、組合活動、通報等の個別法を特定します。
MHLWの公正採用資料全体を単一のstatutory protected-class listへ変換しません。
障害者雇用の差別禁止・合理的配慮はemployment-specific lawを適用します。

2026-10-01前はcustomer harassment・求職者sexual harassmentの新措置をfuture
readinessとし、施行済みと書きません。施行後もofficial current textを確認します。

2026-10-01施行予定のpart-time/fixed-term・dispatch省令/guideline改正は、
採用時にArt. 14(2)説明を求め得る旨を明示する等の変更であり、説明請求権を
新設した、または同一賃金を一律義務化したと誤記しません。

2026-07-01以降の民間法定雇用率は2.7%、原則37.5人以上のemployerがquota対象。
国・地方公共団体3.0%、都道府県教育委員会2.9%を区別し、quota thresholdと
個別の差別禁止・合理的配慮義務を混同しません。

## Background check・employee data

APPIの利用目的、適正取得、要配慮個人情報、本人同意が必要な場面、vendor委託、
foreign transfer、retention、securityを確認します。職務関連性・必要性、公正採用
guidanceも確認します。米国固有のnotice packageを日本defaultにしません。

## Restrictive covenant・IP

退職後non-compete等はCivil Code Article 90とcurrent case lawを基に、会社の利益、
職務・地位、期間、地域、対象業務、代償、退職経緯、employee burdenを分析します。
米国州別ban/threshold tableを使いません。employee inventionはPatent Act Article 35、
社内規程、相当の利益、assignmentを確認します。

## Work rules [B/G]

documentが`就業規則`またはその変更かを先に判定します。常時10人以上の事業場では、
mandatory terms、majority union/representativeの意見聴取・書面添付、労働基準監督署
への届出、周知を確認します。意見は自動的なconsentではありません。

不利益変更はLabor Contract Act Article 10の合理性と周知を検討します。36協定、
育児介護等の労使協定、CBAを就業規則と混同しません。MHLW modelは[G] drafting aid
でsafe harborではありません。

## Output gate

candidate/employee向けartifactから内部review noteを除きます。AIはoffer送信、採用、
background vendor order、visa申請、保険加入、work-rule filingを実行しません。
