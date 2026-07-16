---
name: client-intake
description: >
  日本のリーガルクリニック向けconflict-first相談受付。最小限の氏名pre-screenとlawyer clearance後に、identity/scope、safe contact、capacity、civil・criminal・administrative等のforum、urgent danger/deadline、legal-aid routeを整理し、受任判断未了の内部summaryとdeadline candidate handoffを作る。受任、代理、法律助言を決定しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: direct
  logical-target-id: ja-jp.cowork.legal-clinic.client-intake
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Client intake

canonical label: `/legal-clinic:client-intake [practice-area]`

## Mandatory conflict-first / no-engagement gate

1. `references/common/cowork-runtime-contract.md`を読む。intake record又は会話開始だけで
   弁護士・依頼者関係、受任、代理、法律相談を宣言しない。ただしdisclaimerは決定的で
   なく、actual advice/undertaking/representation/reliance等が生じたら直ちに責任弁護士へ
   engagement/scope評価をrouteする。
2. substantive facts前にprospect scopeでprospective client、adverse parties、
   aliases、旧姓、関連法人・人物・matterの最小限pre-screenを行う。
3. conflict statusは`pending | clear | restricted | blocked`。責任弁護士又はapproved
   conflicts ownerが`clear/restricted`を記録するまで詳細facts/documentを収集しない。
   information barrier又はrestricted ACLだけでclearance/waiverとしない。
4. My Numberをconflict identifier又はmatter IDに使わない。
5. conflict clear後もengagement、client identity、scope、responsible lawyerを別に確認。
6. identity/contact、safe-contact、health/capacity、immigration、criminal、
   child/family/DV、interpreter dataをrestricted ACLへ分離する。
7. urgent danger、custody、today/near deadline、eviction/execution等は通常intakeを止め、
   approved emergency/docket routeへ人が連絡する選択肢を示す。responseを約束しない。
8. legal authorityを引用する場合、official sourceをlive preflightし、current/future
   lawを分ける。connector declarationだけをverifiedとしない。
9. outputはinternal intake summary。`Take/Decline`を出さず
   `受任判断未了 — responsible lawyer decision required`。
10. deadline issueは`deadlines`へ必須handoffするが、未確認日はcalendar factにしない。
11. `criminal | immigration | housing | benefits`はapproved current source cardなしに
    substantive issue、eligibility、deadline、formを生成せず、minimum facts、
    safety/emergency、specialist referralだけ。

Japan:
`references/common/jurisdictions/ja-jp/clinic-law-and-supervision.md`、
`references/common/jurisdictions/ja-jp/privacy-client-data.md`、
`references/common/jurisdictions/ja-jp/procedure-deadlines.md`。

## Workflow

### State 1 — conflict pre-screen

相談内容を詳しく聞く前にnames/variantsだけを取得し、exact prospect recordを照合する。
unauthorized matchの内容又は存在を開示しない。`restricted`は責任弁護士の指示した
information barrier内で続行し得るが、barrierはconflict clearance又はwaiverではない。

### State 2 — identity / engagement / scope

- 誰がclient又はprospective clientか
- host modelとresponsible lawyer
- requested helpとexcluded issues
- current engagement status
- disclaimerとactual conductの一致。conductが先行した場合はimmediate lawyer review
- consent/disclosure/data handling status
- Houterasu program route:
  `consultation-aid | representation-advancement |
  document-preparation-advancement | appointed-criminal-counsel | other`

clinic eligibilityをHouterasu eligibilityと同一視せず、consultation、費用立替、
court appointmentを混同しない。

### State 3 — capacity / safe contact / accessibility

- age、client wishes、guardian/support person、authority evidence、possible conflict
- preferred language、interpreter、reasonable accommodation
- safe channel/time/address、voicemail/mail、third-party contact

AIはcapacity、guardian authority、safe-contact waiverを決定しない。

児童虐待が疑われる場合は通常queueだけに残さず、児童虐待防止法6条等と守秘の関係を
responsible lawyer/designated humanが直ちに確認し、prompt human notificationを行う
routeを示す。route candidateは`189`。AI/cloud入力又はqueue登録を通告と扱わず、
AIは通告しない。

### State 4 — forum-specific intake

| forumType | minimum questions |
|---|---|
| `civil` / `labor` | claim、respondent、papers、service、hearing、preservation、limitation |
| `family` | existing order、2026-04-01 reform transition、parental authority、child interests、DV/abuse、安全 |
| `criminal` | suspect/defendant/victim、custody、interview/hearing、counsel、immediate escalation |
| `administrative` | agency、disposition、notice/knowledge date、review/litigation route、special deadline |
| `immigration` | status、agency/forum、custody、notice/hearing、safe contact、qualified specialist route |
| `housing` | tenure、notice、service、court/agency、eviction/execution、安全 |
| `benefits` | program、decision notice、review/appeal、payment/health urgency |
| `transactional` | parties、scope、document、counterparty deadline、regulatory filing |

practice-area guideがある場合、そのquestions/red flagsをfloorとして追加する。米国clinic
template又はformを日本へ自動適用しない。

DV protection orderはapproved source cardで地方裁判所routeを確認し、family courtへ
自動routingしない。相談route candidateは`DV相談ナビ #8008`だが、safe device/channel、
call history、相手方monitoringを先に確認する。

### State 5 — issue spotting / triage

```yaml
triage: urgent | time-sensitive | standard | may-be-out-of-scope
```

legal issueはhypothesisとしてprovenance tagを付ける。cross-area issue、conflict、
scope、safety、capacity、language、document gapを`[review]`で責任弁護士へ示す。

### State 6 — mandatory deadline handoff

各triggerを別candidateとして出す。matter作成前はwriteせずhandoff draft、matter作成後は
`references/common/clinic-state-payloads.schema.json#/$defs/deadlinePayload`へ完全に
mapする。partial ad-hoc payloadをstateへwriteしない。

documentに明記されたhearing dateもexact source/versionを記録し、人が確認する。
computed date、limitation、service-based dateは責任弁護士とdocket ownerのverification前に
calendar factと表示しない。

## Output

`internal-memo`として次を作る。

1. reviewer noteとDRAFT status
2. client situation in their words
3. conflict status、engagement/scope status
4. forum/issue hypothesesとsource provenance
5. key facts/source/document gaps
6. safe contact、language/accessibilityのrestricted references
7. triageとurgent route
8. deadline handoff blocks
9. specific verification questions
10. `受任判断未了 — responsible lawyer decision required`

substantive intake completion後もmatter create、binding create、client communicationは別
operationである。

## 行わないこと

- conflict clearance、受任、decline、scope、legal aid eligibilityの決定
- intake中の法律助言
- client/matter switchをsame sessionで実行
- sensitive dataをgeneral profile又はauditへ複製
- deadline計算をverified calendar factとして登録
- emergency response又はlawyer callbackを保証
- court/agency filing又はexternal send
