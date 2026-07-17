> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 休業・休暇、合理的配慮、harassment

**状態:** DRAFT — qualified Japanese counsel review pending

## Separate tracks

leave caseを次のtrackへ分けます。

1. **Job protection:** maternity、childcare、family care、annual leave、injury、
   pregnancy/leave disadvantage、dismissal restriction。
2. **Employer procedure:** individual notice、intention confirmation/hearing、
   accommodation、document、work-rule/CBA procedure。
3. **Insurance benefit:** employment insurance、health insurance。
4. **Annual-leave accounting:** grant date、days/hours、five-day employer duty。
5. **Disability/health accommodation:** employment-specific reasonable
   accommodation、work limitation、OSH。

employer-paid leave、insurance benefit、company sick leave、annual leaveを混同しません。
日本には一般的な法定employer-paid sick leaveがあると推測しません。

## Case fields

- pseudonymous employee ID、establishment、prefecture
- leave/measure type
- child DOB/age、covered family member category
- eligibility、labor-management exclusion agreement
- requested/approved periods、intermittent unit
- actual normal schedule
- individual notice、intention confirmation、intention hearing、accommodation dates
- overtime/night-work restriction、short hours、flexible measure
- employer procedure、insurance application、return/work restriction
- current authority/effective date

medical diagnosisやfamily detailは必要最小限にし、restricted matterへ分離します。

## Current regime [B/SG]

Childcare and Family Care Leave Act/Regulationsの2025-04-01、2025-10-01 changesを
current textで確認します。maternity、annual leave、OSH、Equal Opportunity Act、
disability accommodation、insurance benefitsも該当事実ごとに確認します。

- 2025-04-01: 子の看護等休暇は小学3年生修了まで、school closure・入学/卒業
  行事等を追加、6か月継続雇用除外を撤廃。所定外労働免除は未就学児へ拡大。
  介護の個別周知・意向確認、早期情報提供、雇用環境整備も確認する。
- 2025-10-01: 3歳～就学前について5つの柔軟措置から2つ以上を導入し、個別
  周知・意向確認、意向聴取・配慮を別々に確認する。
- 2025-04-01の出生後休業支援・育児時短就業給付はemployment-insurance
  benefitであり、employer-paid leaveではない。
- 2026-04-01: 治療と仕事の両立支援は努力義務で、新しい法定paid sick leave
  entitlementではない。
- 2026-04-01: 常時雇用101人以上の企業は男女間賃金差異と女性管理職比率の
  両方の公表義務を確認する。

numeric deadline、entitlement、eligibility、exclusion、form、benefit amountを
hardcodeせず、official sourceとemployeeのactual scheduleから算定します。

## Alerts [I]

alert windowは法定期間ではなくprofileのinternal controlです。未設定なら勝手に
3/7/30日等を入れず、人に設定を求めます。各alertに:

- controlling source/effective date
- clock owner
- calculation inputs
- decision required by whom
- missing facts
- job-protection/accommodation/insurance distinction

を付けます。clean caseは1行summaryです。

## Harassment・future gate

相談窓口、迅速な事実確認、complainant/respondent measures、privacy、
non-retaliation、recurrence preventionを確認します。2026-10-01前はcustomer
harassmentと求職者sexual harassmentの新措置をfuture readinessとして扱います。

## No automated decision

AIはleave eligibility/approval/denial、medical sufficiency、accommodation、
return-to-work、payroll、benefit、discipline、terminationを決めません。approved
Power Platform automationもcandidate alertまでです。
