---
name: pia-generation
description: >
  新機能・製品・処理活動について、house styleと法域別assessment triggerを分けてPrivacy Impact Assessmentをdraftする。data flow、権利、policy整合性、具体的risk、mitigation、owner、条件、residual riskを整理し、承認は人に残す。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: privacy-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# PIA generation

旧来の参照labelは `/privacy-legal:pia-generation [feature name or description]`。

PIAはconversation with the product/teamを記録するdraftである。AIはprocessingをapproveせず、regulatorへ提出せず、launchを承認しない。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を読む。local outputを作らない。
2. **Setup/user:** exact practice profileのPIA trigger、format、depth、sign-off、privacy commitmentsと現在利用者の`user-profile`を読む。
3. **Matter:** workspaceが有効でmatter scopeを選ぶ場合はserver binding、
   matter `status: active`、scope、confidentialityを確認する。
   archived/revokedでは停止する。workspaceが無効、またはfresh sessionで
   practice-levelを明示した場合は`scopeType: practice`を許可する。
4. **Jurisdiction:** `request > matter > practice-profile > tenant-default`。data subjects、entity、processing、vendor、countriesを確認する。
5. **Trigger separation:** binding-law assessment、official guidance、internal house trigger、foreign-law triggerを分ける。
6. **Current law:**法定trigger、lawful route、rights、transfer、sectorをprimary sourceで確認する。2026年日本改正を現行法として使わない。
7. **Prior context:** 同scopeのtriage、prior PIA、DPA reviewを読む。上流severityをfloorとする。
8. **Coverage:** PRD、data flow、security、vendor、policy等の読取り範囲を記録する。missing factを想像しない。
9. **Human judgment:** residual risk、recommendation、conditions、sign-offは人が決める。
10. **Write:** personal draft→reviewed output昇格を分け、exact ID/eTag/idempotencyとfresh confirmationを使う。

## 会話state machine

| state | action |
|---|---|
| `check-trigger` | house / binding / foreign / sector triggerを分離 |
| `collect-context` | prior triage、PIA、DPA、policy、PRD |
| `intake-what-why` | activity、purpose、data、subjects |
| `map-flow` | collection、storage、access、sharing、country、retention |
| `classify-law` | role、legal route、rights、assessment duty |
| `assess-risk` | peopleへのspecific harmとcontrol |
| `policy-diff` | policy、CMP、labels、consent、sector notice |
| `draft-pia` | house formatまたはfallback template |
| `conditions` | owner、deadline、evidence |
| `human-signoff` | proposed recommendationをreview |
| `confirm-save` | personal draft / reviewed output |

## Trigger

日本が関係する場合は
`references/common/jurisdictions/ja-jp/pia-assessments.md`を読む。

- 民間一般の日本PIA: 一律の法定義務ではなくPPCが促進する自主的取組
- My Number: 対象主体には特定個人情報保護評価という固有制度
- GDPR/UK GDPR: Article 35
- US state / sector: current statute
- internal trigger: company policy

`PIA REQUIRED — internal policy`と`DPIA MANDATORY — [law]`を明確に分ける。

強いindicator:

- children、biometric、health、financial、location、communications
- employee/applicant scoring・monitoring
- systematic tracking、ad-tech
- automated consequential decision
- dataset combination・inference
- vendor independent training
- new cross-border route
- unexpected reuse
- policy conflict

indicatorだけで日本法上mandatoryと断定しない。

## Prior context

同scopeのprior outputを引用する。

- prior triageのclassification・conditions
- prior PIAのcarried / revised conclusion
- vendor DPA findings

新事実なしにseverityを下げない。prior outputがない場合はcold startと記録する。

## Intake

`references/pia-template.md`の質問を1回に2～3個ずつ行う。PRD等に既にある事実を再入力させず、exact item/versionを読む。

## 法域別legal route

GDPRの`Consent / Contract / Legitimate Interest`表を日本に機械適用しない。日本は利用目的、取得、目的外利用、要配慮、第三者提供、委託、共同利用、外国提供等を確認する。US state、sectorも別欄にする。

## Risks

genericな`data breach`や`non-compliance`ではなく設計に結び付ける。

悪い例: `位置情報漏えい`

良い例: `support roleが監査logなしに過去30日の位置履歴を閲覧でき、内部者が本人に気付かれず追跡できる`

2～5個のmaterial riskを優先する。likelihood、impact、affected people、mitigation、owner、evidence、residual riskを示す。

## Policy diff

website policyに加え、CMP/cookie banner、App Store privacy label、Google Data Safety、in-product consent、GLBA/HIPAA/FERPA/COPPA等のsector noticeを確認する。

日本のtrackingは
`references/common/jurisdictions/ja-jp/tracking-telecom.md`。

direct conflictはlaunch conditionまたはSTOP候補。policyを変えるかdesignを変えるかは人が選ぶ。

## Output

`references/pia-template.md`を使い、house formatが設定されていればsection orderとtoneを優先する。

recommendationは次のhuman proposal:

- `APPROVED`
- `APPROVED WITH CONDITIONS`
- `CHANGES REQUIRED`
- `NOT APPROVED`

AIがstatusを`APPROVED`へ更新しない。

## Japan current-law note

2026年改正は成立済み・公布確認待ち・未施行。16歳未満、特定生体個人情報等はfuture-readiness欄に分ける。現行APPI、PPC guideline、sector ruleを基礎にする。

## Large input

PRDが大きい場合、data inventory、architecture、vendor、security、retention、notice、rightsを優先し、読んだpages/itemsと未読を記録する。複数featureを1つのPIAへ混ぜず、batch/scopeを人に選んでもらう。

## Human gate

sign-off、regulator consultation/submission、launch approval、policy publicationは別確認。Non-lawyerにはregime、trigger、risks、residual risk、open facts、3つの質問をbriefにする。

## 完了

conditions draft、product questions、DPA redline、policy update、escalationから次を人に選んでもらう。
