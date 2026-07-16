---
name: dsar-response
description: >
  Data Subject Access Requestまたは日本法上の保有個人データ請求を分類し、本人確認、system別探索、例外・redaction、確認通知、本回答、監査logをdraftする。法域別deadlineを分け、回答・開示・訂正・停止・削除は人の承認後にだけ実行する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: privacy-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# DSAR response drafting

旧来の参照labelは `/privacy-legal:dsar-response [paste the request, or describe it]`。

requestには本人のPIIが含まれる。必要最小限だけ取得し、本人氏名をfilename、record ID、dashboard labelへ入れない。outward-facing letterは常にdraftで、人がreviewして送る。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を読む。local fileへ保存しない。
2. **Setup/user:** exact practice profileのsystems list、verification method、internal SLA、handlerと、現在利用者の`user-profile`を読む。別利用者のroleを流用しない。
3. **Matter:** workspaceが有効でmatter scopeを選ぶ場合はexact server bindingと
   matter `status: active`を確認する。archived/revokedではrequest dataを
   読まず拒否する。workspaceが無効、またはfresh sessionでpractice-levelを
   明示した場合は`scopeType: practice`を許可し、過去matter dataをcarryしない。
4. **Privacy:** session、connector、output storageがPII要件を満たすか確認する。ID attachment、unrelated thread等を必要なく保存しない。
5. **Jurisdiction/role:** data subject、entity、controller/processor/委託、applicable regimesを確認する。日本の権利をGDPR/CCPAと同一視しない。
6. **Deadline:** receipt起算、extension、tolling、fee、authorized agentをcurrent primary sourceで確認する。internal SLAと法定deadlineを分ける。
7. **Scope/coverage:** exact identifiers、date range、systems、vendorsを決める。partial searchをcompleteと書かない。
8. **Human judgment:** exemption、redaction、refusal、identity sufficiency、delivery、deletionは有資格者が決める。
9. **No autonomous action:** AIはsend、respond、produce、correct、restrict、deleteを行わない。
10. **Write:** create/updateを分け、exact ID/eTag/idempotencyとfresh confirmationを使う。

共通source tag、non-lawyer mode、reviewer noteは
`references/common/source-provenance-and-review.md`。

## 会話state machine

| state | action |
|---|---|
| `intake-minimize` | requestを最小限取得し、receiptを記録 |
| `classify-rights` | access / deletion / portability / correction / objection / restriction等 |
| `resolve-regimes` | Japan / GDPR / UK / California / state / sector |
| `calculate-clocks` | regime別deadline、extension、internal SLA |
| `verify-identity` | riskに比例した本人・代理人確認 |
| `locate-data` | system-by-system search plan / results |
| `assess-limits` | exemption、redaction、retention、legal hold |
| `draft-acknowledgment` | prompt acknowledgment draft |
| `draft-substantive` | production/action/refusal response draft |
| `attorney-review` | open judgmentをreview |
| `confirm-action` | human send / production / deletion等を別確認 |
| `log-result` | exact resultをstate/auditへ記録 |

## Classification

combination requestを分ける。例: access後deletionは2つのlinked right。

日本が関係する場合は
`references/common/jurisdictions/ja-jp/rights-dsar.md`を読む。

- 日本APPI: 利用目的通知、開示、第三者提供record、訂正等、利用停止等
- GDPR/UK GDPR: Articles 12–22
- California/US state: current statute/regulations
- sector: HIPAA、GLBA、FERPA、COPPA等

日本では`保有個人データ`等のscopeを確認し、GDPRの1か月やCaliforniaの45日を自動適用しない。

## Identity

logged-in session、registered email、challenge、代理権等をriskに合わせる。over-verificationで権利行使を妨げず、under-verificationで他人のdataを開示しない。

verification未完了でも、clockが自動停止すると仮定しない。applicable regimeを確認し、探索等を並行できる範囲で進める。

## Locate

practice profileのsystems listをfloorにする。

| System | Exact query / item | Queried? | Data found? | Coverage / error |
|---|---|---|---|---|

production、analytics、support、CRM、marketing、logs、backups、email/collaboration、paper、processor/vendorを案件に応じて確認する。取得不能を`none`と記録しない。

## Limits / exemptions

候補:

- other individuals
- privilege / confidentiality
- trade secret
- security
- statutory retention
- establishment / defense of claims
- litigation hold
- backup rotation
- manifestly unfounded / excessive等のregime-specific rule

各候補にbinding authority、facts、scope、redaction alternativeを付ける。`proposed — qualified review required`であり、AIがblanket exemptionを確定しない。

## Drafts

`references/response-workflow.md`の2通templateを使う。2通processは移行元のhouse processであり、全法域で一律の法定要件とは書かない。

- acknowledgment draft: receipt、understood scope、identity gap、target date、contact
- substantive draft: data/action、delivery、withheld scopeと理由、complaint/contact

本人向けletterに内部header、reviewer note、他人の情報、内部strategyを入れない。内部cover memoにreviewer noteを置く。

## Japan

日本の開示はPPC FAQ上`遅滞なく`であり固定日数ではない。利用停止・消去等は請求要件が別。2026年改正の16歳未満・特定生体個人情報ruleは未施行として分ける。

## Action gate

次を別々に確認する。

1. acknowledgment send
2. substantive response send
3. data production
4. correction
5. restriction / opt-out
6. deletion
7. processor instruction

1つのyesを他のactionへ拡張しない。AIはactionを実行しない。

## Log

`references/dsar-log-schema.md`を使う。received、verified、regimes、deadlines、systems、withheld basis、approver、sent/action resultを記録する。data minimization、retention、legal holdを守る。

## Escalate

- plaintiff、opposing counsel、journalist
- regulator copied / threatened
- prior disputed response
- broad internal communications request
- litigation hold
- child / guardian conflict
- biometric、health、financial、My Number
- multi-jurisdiction deadline conflict
- identity fraud concern

## 完了

acknowledgment、substantive response、attorney brief、missing-system plan、extension draftから人に選んでもらう。送信しない。
