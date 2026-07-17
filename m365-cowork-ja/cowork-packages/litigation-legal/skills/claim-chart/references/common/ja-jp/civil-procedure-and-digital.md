> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本の民事手続、digitalization、保全、執行、労働審判

## Source layer

- 民事訴訟法: `binding-law`
- 民事訴訟規則: `binding-rule`
- 裁判所のmodel/form/部運用: 原則`official-guidance`
- 事件固有の命令・期日指定: その事件で優先するsource

最高裁判所規則の根拠は憲法77条。裁判所のweb説明を米国型local ruleと呼ばない。

## Matter fields

```yaml
proceedingType: pre_suit | ordinary_civil | provisional_remedy | mediation | labor_tribunal | patent_infringement | JPO_trial | appeal | execution | other
court: "[court]"
division: "[division or null]"
caseNumber:
  era: "[era]"
  year: "[year]"
  caseSymbol: "[symbol]"
  serial: "[serial]"
mintsCaseId: "[ID or null]"
recordRegime: legacy_case_paper | legacy_case_repealed_mints_transition | new_case_mints_new_regime | other_procedure_partial
```

## 民事訴訟digitalization

2026-05-21にordinary civil litigationのnew regimeが施行。原則として同日以降
commenced actionへ適用し、2026-05-20以前commenced actionはlegacyとして扱う。
mintsはcurrent systemであり、旧mints rulesの廃止とsystem廃止を混同しない。

retained litigation agent（民訴法54条1項但書の特別許可代理人、国指定代理人、
地方公共団体委任職員等を除く）は132条の11の電子提出義務を確認する。oral filing
や帰責不能system failure exception、electronic-service notice提出も確認する。

phase:

- 2023-02-20: 氏名・住所等の秘匿制度
- 2023-03-01: 両当事者のweb/telephoneによる弁論準備・和解期日
- 2024-03-01: web口頭弁論
- 2026-05-21: online filing/service、electronic record、ordinary civil phase

2026年1月～5月20日commenced caseもlegacy。new ordinary civil、旧事件、
旧mints transition、別手続を`recordRegime`で区別する。

民事執行、倒産、労働審判、非訟、家事・人事はordinary civilのfull online/
electronic-record rollout外で、原則2028年6月までの別rollout。ただし2026-05-21
改正で一部execution/provisional-remedy hearingのweb参加やelectronic title関連
措置が始まったため、procedure feature matrixを確認しbinary excludedとしない。

electronic evidenceのfile type、size、署名、提出方法はcurrent court細則と
case-specific directionを確認する。Word/Office文書をそのまま受理すると約束しない。

## Current deadline controls

### Electronic service

民訴法109条の2のprescribed electronic-service noticeが前提。mandatory electronic
filerは132条の11(2) noticeも確認する。109条の3ではaccess、download/record、
notification後1週間のうちstatutory earliest eventで効力発生する。
electronic filingは132条の10(3)によりcourt fileへrecordされた時点を確認する。

記録:

```yaml
notificationSentAt: "[ISO-8601]"
viewedAt: "[ISO-8601 or null]"
downloadedOrRecordedAt: "[ISO-8601 or null]"
effectiveServiceAt: "[earliest valid timestamp]"
sourceItemId: "[mints/court notice item]"
```

### Appeal

民訴法285条: electronic judgmentまたは254条2項electronic recordのserviceから
2週間の不変期間。legacy transition、起算点、service effect、休日、追完、
上訴種類を確認し、candidateを自動calendar登録しない。

### Period rules

- 民訴法95条: Civil Code period ruleを取り込み、末日が土曜、日曜、祝日、
  1月2～3日、12月29～31日等の場合を確認
- 96条: 不変期間以外の伸縮に加え、遠隔地居住者の不変期間付加
- 97条: missed invariable periodのみ。原因消滅後1週間、国外partyは2か月、
  court-system failureを含むcurrent text

answer deadlineは裁判所指定。米国の21日をdefaultにしない。

## 法定審理期間訴訟手続

民訴法381条の2以下の別procedureとして扱う。consumer-contract actionと
individual-labor civil actionは除外。両partyのrequest/consent、court decision後
2週間以内のfirst date、原則5か月以内のsubmission close、6か月以内のtrial/
evidence、1か月以内のjudgmentを確認する。dismissal以外のjudgmentには通常appeal
ではなく同courtへの2週間不変期間のobjection routeを確認する。

## Court document / pleading types

日本向けdraft:

- 訴状
- 答弁書
- 準備書面
- 証拠説明書
- 陳述書
- 控訴状・控訴理由書
- 上告状・上告理由書
- 各種申立書

statute/article、court/date/case number、甲/乙号証、actual form、mints requirementを
使う。Bluebook、US local rule、Rule 11 certificationをdefaultにしない。

民訴法2条の信義誠実、157条の時機に後れた攻撃防御方法はそれぞれの要件で扱い、
「日本版Rule 11」と表現しない。

## Civil provisional remedies

民事保全法:

- 13条: 被保全権利・権利関係と保全の必要性を明らかにし、疎明
- 20条: monetary claimについてexecutionが不能または著しく困難となるおそれ
- 23条: disputed subject matter保全、または重大損害・急迫危険回避の暫定地位

証拠保全とは別。担保、管轄、緊急性、送達、執行、保全異議等は事件固有に確認する。
AIは申立て、担保提供、執行を自動実行しない。

民事保全法43条によりcreditorへのorder service後2週間を経過すると原則執行
できない期限と、debtorへのservice前執行可能性を確認する。

## Civil execution

民事執行法22条等の債務名義にはprovisionally enforceable judgment等も含む。
25条・29条、送達、執行文、対象財産、2026-05-21後のrecord certificate/event
identification regimeを確認する。
財産開示・第三者情報取得は執行段階の制度であり、pretrial discoveryではない。

matter closeは判決言渡しだけでなく、確定、appeal、settlement、execution、
preservation/retention dispositionを分ける。

## Labor tribunal

労働審判法15条2項: 特別の事情を除き3回以内の期日で審理を終結。労働審判規則
13条は原則として申立てから40日以内に第1回期日を指定し、14条は答弁書期限を
労働審判官が定める。27条はやむを得ない事由を除き第2回期日終了までに主張・
証拠書類提出を終える。

労働審判法21条: 審判書送達または告知から2週間の不変期間内に異議申立て。
適法な異議で審判は失効し、22条によりoriginal petition時にaction filedとみなす。
異議がなければ裁判上の和解と同一の効力。26条のrecord access restrictionも確認。

「3回以内」はordinary civilのhearing limitではない。労働審判は非公開で、
ordinary civil digitalizationと同じmints coverageを仮定しない。

## Court record/database limitation

裁判所裁判例検索はすべての判決等を掲載していないselected database。negative
searchは事件・判断不存在を証明しない。ordinary recordのinspection、copy/certified
copy、nonpublic hearing/settlement portion、CPC 92 restrictionを区別する。
2026-07-16確認でofficial public bulk docket/APIは特定できなかったとだけ記録する。

docket statusはmints notice、court document、OC、manual checkを優先する。
