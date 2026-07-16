> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Full interview sections

1turnで2～3 answerable promptsまで。回答がdocumentにある可能性が高ければ、再入力より
official link、approved file、pasteを先に求める。real client materialは収集しない。

## A. Authority and host model

- responsible lawyer name、bar association、registration verification source/date
- supervisor identity、responsible lawyerとの関係
- host model:
  `university-clinic | law-office | bar-consultation | houterasu-contracted |
  court-appointed-criminal | other`
- clinic modelに関する弁護士法72条等のqualified counsel position
- client/retainer holder、fee/legal aid/program model

## B. Conflicts, engagement, scope

- conflict owner、system、minimum names、restricted/blocked process
- information barrier owner/policy。barrierはclearance/waiverでないこと
- prospective-client confidentiality handling
- engagement decision owner、agreement/source record
- disclaimerとactual conductが矛盾した場合のimmediate lawyer escalation
- limited scope、excluded issues、termination/closure
- related matters、information barrier、waiver authority

## C. Student participation and supervision

activityごとにobserve、interview、research、internal draft、routine logistics、
substantive communication、advice、negotiate、accept/decline、sign、file、represent、
settle、closeを設定する。lawyer-only floorを明示する。

matrixはinternal policyで、legal authority又はAttorney Act 72 cureではないことを
profileへ固定する。

- review queue preference
- version-specific lawyer approval
- pedagogy default `assist | guide | teach`
- supervisor competence sign-off
- student access grant/revoke process

## D. Data, confidentiality, security

- APPI regime-specific analysis: 利用目的、要配慮個人情報、委託、第三者提供、
  外国にある第三者への提供、法令/緊急例外、本人対応
- host/業務ごとのAPPI regime:
  `private-sector-chapter4 | public-sector-chapter5 |
  article58-private-treatment | mixed | unresolved`
- clinic restricted categoriesと法定要配慮個人情報が同義でないこと
- account/tenant retention/training/subprocessor
- approved storage、foreign transfer、vendor
- identity/contact、health、immigration、criminal、child/family/DV、interpreter ACL
- My Number refusal/redaction/incident
- safe contact
- retention/deletion、internal preservation control、court order、originals、exports
- incident owner、breach route
- Cowork prompt DLP requirement

## E. Urgent and emergency route

- life/body danger、DV/stalking、自傷他害
- custody/criminal interview
- today/near hearing、appeal、limitation、eviction/execution
- responsible lawyer、backup、docket owner、public emergency route
- safe destination and delivery evidence

response time又はavailabilityを保証する設定を作らない。

## F. Practice and jurisdiction

- practice areas、forum types、jurisdictions
- typical client population、languages、accessibility
- legal aid/referral programs
- official law/rule/guidance
- court/agency forms、case-specific order practice
- civil/criminal/administrative/family/labor/immigration branch
- housing、benefits branch
- 2026-04-01 family reform、DV protection orderの地方裁判所route
- child-abuse human reporting owner/route
- current vs future law review owner
- `criminal | immigration | housing | benefits` approved source card
- consequential translationのresponsible-lawyer legal reviewerとcompetent-language
  reviewer

## G. Sources and seed documents

- handbook、clinic procedures、security/ethics policy
- approved intake form
- current official statutes/rules/forms
- redacted precedent
- retention and incident documents
- synthetic training scenarios

各itemにsource system、item ID/version、purpose、ACL、as-of、reviewerを付ける。

Houterasuは法律相談援助、代理援助、書類作成援助、国選弁護等関連業務を別source/
program fieldにする。

## H. Semester and handoff

- term ID、cohort dates
- competence sign-off
- incoming conflict clearance before access
- assignment owner
- deadline reconciliation
- client notice practice
- departing access/export revocation
- originals、retention、internal preservation control、court order、closure process

semester endをautomatic close/archive/delete triggerにしない。

## I. Integrations and automation

- SharePoint profiles/matters/outputs/state/audit
- OneDrive drafts
- case management/document system
- research connector
- Power Platform solution ID/version/owner/connection/scope
- recurrence/last successful run

declarationとlive proofを分ける。

## K. Canonical payload review

`common/clinic-state-payloads.schema.json`のnested profileとsetup-sessionへ
回答をmapする。completed sections、pending questions、sources、status、profile
item/versionをstrictに検証する。`interview-complete`をlegal review approvalと呼ばない。

## J. Final review

全回答を順番に再読し、contradiction、missing owner、unverified source、silent default、
guardrail degradationを示す。responsible lawyerとsupervisorが別々にapproveするまで
profile statusは`review-pending`。
