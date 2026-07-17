> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 社会保険、労組、高齢者、国際雇用

**状態:** DRAFT — qualified Japanese counsel review pending

## Social/labor insurance [B]

health insurance、employees' pension、employment insurance、workers'
compensationを別々に確認します。ordinary three-quarter test、short-time worker
criteria、employer size、scheduled hours、monthly wage、expected duration、student
status、entity/establishmentをcurrent official sourceで確認します。

2026-07-16時点のshort-time social-insurance routeでは、同一法人番号の各
事業所を通じた厚生年金被保険者数等で51人以上の企業規模、
週20時間以上、月額賃金88,000円以上、2か月超の雇用見込み、非学生等のcriteriaと
ordinary three-quarter testを確認します。個別caseではofficial current textを
再取得します。

2026-10-01前はshort-time social-insuranceの月額賃金criterion撤廃をfutureとして
扱います。enterprise thresholdは2027-10-01に36人以上、2029-10-01に21人以上、
2032-10-01に11人以上、2035-10-01に全企業へ段階拡大予定です。根拠は
令和7年法律第74号（2025-06-20公布）を確認します。2028-10-01のemployment-
insurance週10時間threshold（令和6年法律第26号）も早期適用しません。
rate、standard monthly remuneration、bonus、benefit amountをhardcodeしません。

payroll withholding、resident tax、corporate/permanent-establishment taxはtax
owner/counselへrouteします。AIはenrollment、payroll、benefit applicationを実行しません。

## Unions・CBA [B]

Labor Union Act、applicable CBA、union shop、collective bargaining、consultation、
unfair labor practiceを確認します。investigation、discipline、RIF、work-rule change、
working time、transfer等にCBA procedureがある場合、internal workflowより優先する
可能性をflagします。米国固有のunion interview defaultを移植しません。

## Older workers・employment measures [B]

age 65までのemployment-security measuresとage 70までのendeavor obligationを
区別します。2025-04-01以降、continued-employment optionは原則希望者全員を
対象とし、旧経過措置のselection criteriaを使いません。retirement age、
independently valid termination grounds、social insurance、benefit、mass
separation/reemployment-planを確認します。

## International employment [B/G]

Act on General Rules for Application of Laws Article 12では、外国法選択がある
場合にworkerが最密接関係地法の特定の強行規定を適用する意思を表示する仕組み
等を確認し、「全mandatory protectionが自動適用」と単純化しません。habitual
workplaceはconnectionの推定要素です。勤務地、
habitual place、temporary assignment、secondment、entity、payroll、CBA、tax、
social insurance、APPI foreign transferを確認します。

## Immigration・foreign workers [B/G]

`出入国管理及び難民認定法（昭和26年政令第319号）`に基づくstatus of
residence、authorized activity、sponsoring entity、work location、
change/renewal、foreign-worker hire/separation notificationをcurrent ISA/MHLW
sourceで確認します。MHLW foreign-worker notificationとISAのstatus-specific
affiliation/contract notificationを分けます。令和6年法律第60号による
2027-04-01予定の育成就労regimeを施行前に適用しません。

## EOR/entity gate

cost/timeline比較の前に:

1. providerがgenuine employerか。
2. daily instructionを誰が行うか。
3. dispatch、placement、outsourcing、prohibited worker supplyのどれか。
4. work rules、36 agreement、payroll、insurance、OSH、discipline、dismissalのowner。
5. licence、visa sponsorship、foreign-worker notice。
6. APPI/HRIS transfer。

legal feasibilityが不明ならEORを推奨しません。outside employment counselとtax
counselを必須routeとします。
