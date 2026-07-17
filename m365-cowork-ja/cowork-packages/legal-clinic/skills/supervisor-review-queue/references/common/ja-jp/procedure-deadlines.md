> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — forum triage、手続、digitalization、deadline

**状態:** DRAFT — qualified Japanese counsel and clinic supervisor review pending

## Forum triage

| forumType | minimum urgency facts |
|---|---|
| `civil` | claim/respondent、court paper、service、hearing、preservation、limitation |
| `family` | existing order、child/safety、hearing、service、confidentiality |
| `labor` | termination/discipline/wage、labor tribunal/court、union、deadline |
| `criminal` | suspect/defendant/victim、custody、interview/hearing、appointed counsel |
| `administrative` | agency、disposition、notice/knowledge date、review/litigation route |
| `immigration` | agency/forum、status、custody、notice、hearing、remedy、deadline |
| `housing` | tenure、notice、court/agency、service、eviction/execution、safety |
| `benefits` | program、decision、notice、review/appeal route、payment/health urgency |
| `transactional` | party、scope、document、counterparty deadline、regulatory filing |

civil legal-aid flowをcriminalへ流用せず、ordinary civilのdigitalizationをfamily、
execution、insolvency、labor tribunal等へ一律適用しない。

`criminal | immigration | housing | benefits`はresponsible-lawyer-approved source cardが
currentかつmatter/forum一致の場合だけsubstantive rule、deadline、eligibility、formを
使う。cardがなければminimum fact/document capture、安全・緊急route、specialist referral
だけに限定する。

## Civil digitalization

research recordではordinary civil litigationのfull digitalizationが2026-05-21に
施行された。new/legacy case、mints transition、別手続のfeature matrixをcurrent
court sourceと事件固有命令で確認する。

民事電子送達は少なくとも次を別fieldで取得する。

```yaml
mode: paper | electronic | court-order | not-applicable | unknown
noticeRequired: true | false | null
noticeIssuedAt: "[timestamp or null]"
accessedAt: "[timestamp or null]"
recordedToUserFileAt: "[timestamp or null]"
oneWeekAfterNoticeAt: "[timestamp or null]"
excludedInabilityPeriods: []
effectiveServiceEvent: paper-service | access | record-to-user-file | one-week-after-notice | court-order | not-determined
effectiveServiceAt: "[timestamp or null]"
sourceItemId: "[exact item or null]"
sourceVersion: "[exact version or null]"
```

民事訴訟法109条の2・109条の3のcurrent text、prescribed notice、事件recordを確認し、
閲覧、user fileへの記録、通知発出日から1週間経過のうち最も早い時を記録する。
受送達者の責めに帰せない事由で閲覧又は記録できない期間は1週間へ算入しないため、
excluded periodとsourceを別記する。曖昧な「notice後一定期間」で済ませず、
studentがdocumentを開いた時だけをtriggerとしない。mints account
又はlawyer credentialのaccessは代理権を生まず、credentialをstudentと共有しない。

transition fields:

```yaml
proceedingCommencedAt: "[timestamp or null]"
reformEffectiveAt: "2026-05-21T00:00:00+09:00"
recordRegime: pre-2026-05-21-legacy | post-2026-05-21-new-ordinary-civil | transitional-mints | procedure-specific | unknown
applicabilitySourceItemId: "[source]"
caseSpecificDirectionItemId: "[source or null]"
```

ordinary civil以外又は開始日不明ではnew regimeを推定しない。

## Deadline rule card

州別plausibility bandを使わず、責任弁護士が承認したeffective-dated rule cardを使う。

```yaml
ruleCardId: "[ID]"
forumType: "[ASCII enum]"
proceedingAndRemedy: "[scope]"
triggerEvent: "[event]"
triggerEvidence: "[required evidence]"
startDayRule: "[rule]"
holidayRule: "[rule/source]"
filingMethodAndCutoff: "[method/cutoff]"
deadlineClass: statutory-invariable | statutory-extendable | court-set | contractual | limitation | internal
authorityUrl: "https://..."
articleOrOrder: "[article/rule/order]"
effectiveFrom: "[YYYY-MM-DD]"
transitionalRule: "[rule or none]"
verifiedAt: "[YYYY-MM-DD]"
verifiedByLawyer: "[object ID]"
```

rule cardがない、不鮮明、stale、事件に適用不明ならdateを推測せずurgent calculation taskを
作る。AI ledgerをsole calendarにしない。

time-computation payloadはperiod value/unit、start event、初日算入/不算入、timezone、
last-day rule、holiday/court-closure source、filing method/cutoff、calculation stepsを
必須にする。月・年による期間、court-set period、invariable period、追完、遠隔地等を
単一の「日数加算」に潰さない。

適用regimeを先に記録する。

- 民法138～143条: general period rules。ただし法令、裁判上の命令、法律行為の
  special ruleを優先。
- 民事訴訟法95条: 民事訴訟の期間計算と同条固有の末日調整。
- 刑事訴訟法55条: 刑事の時間/日月年、初日、暦、末日、時効期間のproviso。
  schema enumは`criminal-procedure-code-55`。
- 行政機関の休日に関する法律1～2条: 対象となる国の行政庁への法定申請等と
  proviso/special rule。
- special statute、court/agency order、contract。

`cpc95Applies`を明示し、民事訴訟法95条の土日祝等extensionを行政不服、行政庁届出、
契約、benefits、immigration、private deadlineへ自動適用しない。行政機関休日法も
地方公共団体、裁判所、private counterparty又は時をもって定める期間へ自動適用しない。
applicability sourceがない場合はcandidate dateを確定しない。

刑事の期間計算には`criminal-procedure-code-55`とapplicable criminal special provision/
court orderを使う。民事訴訟法95条又は民法138～143条を刑事へ代用せず、刑事訴訟法
55条ただし書の時効期間、刑事上訴等のspecific triggerを別途確認する。

このregimeでは`civilElectronicService`を`not-applicable`とし、notice/access/
user-file record/one-week/deemed-service/outage/source metadataを全てnull又はemptyにする。
transitionは`procedure-specific`、ordinary-civil reform dateはnull。
`post-2026-05-21-new-ordinary-civil`を刑事recordへ使わない。

## Limitation completion postponement / renewal

「tolling」へ一括翻訳せず、民法147～152条等のcurrent textに従い:

- 裁判上の請求等
- 強制執行等
- 仮差押え・仮処分
- 催告
- 協議を行う旨の合意
- 権利の承認

について`完成猶予`と`更新`、発生時点、終了後の扱い、相対効、再催告/再合意等を
区別する。deadline recordには`completionPostponementGround`と`renewalGround`を別々に
記録し、両方を同時に推定しない。approved source cardと責任弁護士verificationなしに
limitation dateを出さない。

民法153条の当事者・承継人間の効力範囲も確認し、別partyへ自動波及させない。

## Current examples — defaultsではない

次はofficial sourceを再確認するためのissue-spotting例であり、matterへ自動適用しない。

- 民事控訴: 民事訴訟法285条の2週間の不変期間。送達、electronic record、起算、
  休日、追完、経過措置を確認。
- 刑事控訴: 刑事訴訟法373条の14日。事件固有手続を確認。
- 行政不服審査: 行政不服審査法18条の期間とspecial statuteを確認。
- 取消訴訟: 行政事件訴訟法14条の期間、処分、知った日、正当理由を確認。
- 民事訴訟法95条: 期間末日、休日等をcurrent textで確認。

answer、appeal、service、limitation、administrative filingについて米国defaultを使わない。

## Family reform / DV

父母の離婚後等の子の養育に関する2026-04-01施行改正は、事件・行為の日付、経過措置、
parental authority、子の利益、DV/虐待facts、existing orderをcurrent official sourceで
確認する。共同親権又は単独親権をAIがdefaultにしない。

DV防止法上の保護命令は地方裁判所routeをcurrent law/court guidanceで確認し、
family courtへ自動routingしない。申立先、対象、命令種類、期間、e-filing availability、
安全計画をcase-specificに確認する。差し迫る危険ではdocument workflowよりhuman
emergency routingを優先する。

民事訴訟法55条は民事の訴訟代理権範囲・特別委任事項だけに使い、刑事の期間計算へ
使わない。student participation matrix、mints access又はsystem permissionを
訴訟代理権へ置換しない。

## Candidate lifecycle

`candidate` → lawyer verification → docket owner verification → `verified`であり、
calendar entryではない。trigger、effective service、authority、calculation、
holiday、case orderのいずれかが不明なら`candidateDate: null`。

`complete`は実際のfile/submit/service evidenceを人が確認した後、
`close`はdeadlineが適用されなくなった理由と責任弁護士approval後に行う。
old recordをdeleteせず`rejected | superseded | completed | closed`としてversionを残す。

## Court/agency artifact

訴状、答弁書、準備書面、申立書、陳述書、審査請求書等はforum-specific current form、
事件固有命令、責任弁護士precedentを使う。criminal又はadministrative filingをcivil
templateから生成しない。service/certificateを自動追加せず、sign/fileを実行しない。

internal preservation instructionを`legal hold`又はFRCP相当の法的制度と断定しない。
裁判所命令、民事訴訟法上の証拠保全その他のexact legal basisがある場合だけ別sourceに
記録する。

## Urgent deadline routing

today/near-term hearing、custody、eviction/execution、appeal、limitation、agency filing、
protective relief等を検知したらstandard queueを止め、responsible lawyerとapproved
docket/emergency routeへ即時escalation candidateを作る。response timeを約束せず、
delivery成功を確認できなければ未達として表示する。
