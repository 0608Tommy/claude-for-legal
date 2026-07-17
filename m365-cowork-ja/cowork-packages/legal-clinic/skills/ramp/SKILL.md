---
name: ramp
description: >
  日本のリーガルクリニック学生向けsemester onboarding。責任弁護士、全国一律の学生代理資格がないこと、student participation matrix、conflict-first、守秘/APPI/My Number、forum triage、safe contact、current source、mints、期限verification、access revocationをsynthetic exerciseで学び、responsible lawyerのcompetence sign-off前にreal client accessを与えない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: direct
  logical-target-id: ja-jp.cowork.legal-clinic.ramp
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Ramp

canonical label: `/legal-clinic:ramp [--card]`

## Mandatory training / no-client-access gate

1. `references/common/cowork-runtime-contract.md`を読み、exact student user profile、
   approved clinic profile、responsible lawyer、supervisor、term IDを確認する。
2. profileがdraft/pending/blocked、responsible lawyer未確認、student participation
   matrixなしではgeneral synthetic orientationだけ。
3. onboardingは資格、代理権、受任権限、court filing authorityを与えない。
4. 全国一律のstudent-practice status又は`Certified Legal Intern`があると教えない。
5. exerciseはsynthetic dataだけ。real client identity/contact/health/immigration/
   criminal/child dataをtrainingへ使わない。
6. competence sign-off、conflict clearance、assignment、least-privilege access、
   fresh-session binding前にreal matterへaccessしない。
7. Cowork内DLPがrequiredならreal client useをblockedとして説明する。
8. AIはstudentをcertifyせず、responsible lawyerがsign-offする。
9. student participation matrixはinternal policyで、legal authority又はAttorney Act
   72 cureではないと教える。
10. information barrierはconflict clearance/waiverでなく、disclaimerはactual conductに
    よるengagement/scope成立可能性を排除しないと教える。

Japan:
`references/common/ja-jp/clinic-law-and-supervision.md`、
`references/common/ja-jp/privacy-client-data.md`。

## Walkthrough

### 1. Clinic and roles

- clinic scope、host model、responsible lawyer、supervisor
- engagement/scopeとcase acceptance
- student participation matrix
- software review preferenceとmandatory lawyer gate
- where profiles/matters/outputs/state/audit live

studentはobserve/interview/research/draft等のapproved範囲だけで補助する。

### 2. Ethics / data / safety

- conflict names before substantive facts
- confidentialityと日本のprivilege caveat
- student、AI/cloud、vendorが弁護士と同じ保護を自動的に得ないこと
- APPI、My Number refusal、approved AI uses
- identity mapping、safe contact、health、immigration、criminal、child data ACL
- language、interpreter、capacity、reasonable accommodation
- incident、DV/stalking、自傷他害、custody、urgent deadline route

emergency routeはresponse guaranteeではない。

### 3. Forum and source

- civil、criminal、administrative、family、labor、immigrationのtriage
- housing、benefitsのapproved source-card restriction
- 官報/e-Gov/裁判所/省庁/JFBA等のsource hierarchy
- Japanese official textとtranslation limit
- current vs future law
- judgment database incompleteness
- mints、electronic service、legacy/new/other procedure
- deadline candidateとdual verification
- 民法の完成猶予/更新、civil electronic-service/time/transition
- 2026-04-01 family reform、DV district-court route、child-abuse human reporting
- Houterasuのconsultation/representation advancement/document preparation
  advancement/appointed criminal counselの分離

### 4. Skill practice

synthetic matterで:

1. conflict-first intake
2. internal memo scaffold
3. official-source research roadmap
4. client-safe appointment draft
5. deadline candidate handoff
6. supervisor review submission
7. semester handoff/access revocation discussion

各exerciseで「AIがしたこと」「studentが分析すること」「responsible lawyerが決めること」
を分ける。

### 5. Verification habits

- every output is DRAFT
- exact matter binding and fresh-session switch
- every fact/source/deadline/version
- no quote without exact passage
- no internal memo in client/filing artifact
- no send/post/file/sign/calendar/accept/decline/settle/close
- urgent route without response promise
- consequential translation requires both legal and language review

## `--card`

1ページ相当のreference:

- ASCII skill IDsと用途
- responsible lawyer/supervisor contact route
- allowed/prohibited student activities
- conflict-first、safe-contact、restricted data
- source hierarchy/current-vs-future
- deadline candidate rule
- artifact separation
- emergency and incident route

cardはtraining artifactで、matter/client dataを含めない。

## Competence sign-off

completion candidate:

```yaml
studentObjectId: "[object ID]"
termId: "[ASCII term ID]"
modulesCompleted: []
syntheticExercisesCompleted: []
openQuestions: []
signedOffByResponsibleLawyer: "[object ID or null]"
signedOffAt: "[ISO-8601 or null]"
realMatterAccessEligible: false
```

sign-offとaccess grantは別operation。AI又はskill completionで
`realMatterAccessEligible: true`にしない。

## 行わないこと

- substantive Japanese law course又はprofessional qualification
- real client dataでsimulation
- student certification、assignment、access grant
- U.S. clinic examples/rulesを日本defaultとして教える
- handbook/profile未確認でclinic policyを創作
