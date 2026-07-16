> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 移行元legal-clinic workflowの正規token

本書はsource compatibilityのtoken台帳である。日本法layerは米国法を移植せず、ID、
mode、field、enum、pedagogy、handoff shapeを保持する。

## 登録IDとcanonical label

| ID | canonical label / mode |
|---|---|
| `build-guide` | `/legal-clinic:build-guide [practice-area]` |
| `client-comms-log` | `/legal-clinic:client-comms-log [matter-id] [--add | --read | --summary | --patterns]` |
| `client-intake` | `/legal-clinic:client-intake [practice-area]` |
| `client-letter` | `/legal-clinic:client-letter [appointment | doc-request | update]` |
| `cold-start-interview` | `/legal-clinic:cold-start-interview [--quick | --full | --redo | --redo <section> | --check-integrations]` |
| `customize` | `/legal-clinic:customize [section or change]` |
| `deadlines` | `/legal-clinic:deadlines [--add | --report | --update <id> | --complete <id> | --close <id> | --horizon=N]` |
| `draft` | `/legal-clinic:draft [document-type]` |
| `memo` | `/legal-clinic:memo [issue]` |
| `ramp` | `/legal-clinic:ramp [--card]` |
| `research-start` | `/legal-clinic:research-start [issue]` |
| `semester-handoff` | `/legal-clinic:semester-handoff [--semester=term] [--case=matter-id]` |
| `status` | `/legal-clinic:status [client | internal | court | agency]` |
| `supervisor-review-queue` | `/legal-clinic:supervisor-review-queue [--approve ID | --return ID note | --edit ID]` |

Coworkではslash commandを要求せず、会話stateとして解釈する。

## Internal helper flattening

- `form-generation`は`draft`へcompileする。旧utteranceはaliasとして受け付けるが、
  別skillを登録しない。
- `plain-language-letters`はintent routerである。appointment、document request等の
  routine intentは`client-letter`、期限・scope・法的position・bad news等の
  substantive intentは`status client`へrouteする。
- helperのmissing-fact、plain-language、supervision、no-send/no-file rulesをcallerへ
  直接残す。

## Source modes preserved

```yaml
pedagogyMode: assist | guide | teach
conflictStatus: pending | clear | restricted | blocked
engagementStatus: pending | active | limited | declined | closed
triage: urgent | time-sensitive | standard | may-be-out-of-scope
communicationMode: add | read | summary | patterns
deadlineMode: add | report | update | complete | close
reviewStatus: pending | approved | edited-approved | returned | superseded
handoffStatus: draft | lawyer-reviewed | access-pending | released | superseded
statusAudience: client | internal | court | agency
```

sourceの`formal review queue | configurable flags | lighter-touch`はsoftware workflow
preferenceとして保持できるが、日本向けのsubstantive lawyer review gateを無効化しない。
information barrierはsource compatibility上のrestricted controlであり、
`conflictStatus: clear`又はwaiverへ変換しない。

## Source behavior preserved

- every output is draft; student analysisとlawyer reviewを分ける。
- intakeはcase acceptanceを決定しない。
- conflictをAIが解決しない。
- disclaimerだけでnon-engagementを保証しない。実際のconductとscopeを責任弁護士が確認。
- deadline handoffは`client-intake`から`deadlines`へ必須。
- missing factsをguessせずspecific promptにする。
- research roadmapはleadでありauthorityではない。
- communication、deadline、review、handoff historyはappend-only correction。
- deadline、client communication、court/agency documentをsupervisorへrouteする。
- pedagogy `assist | guide | teach`をpractice-area guideから適用する。
- semester handoffはcase closeを実行しない。
- queueはauto-approveしない。
- student participation matrixはinternal policyであり、legal authority又は
  Attorney Act 72 cureではない。

## 日本向けに強化する順序

1. conflict pre-screenをsubstantive factsより前に行う。
2. responsible Japanese lawyer、supervisor、student roleを分ける。
3. engagementとscopeをconflict clearanceから分ける。
4. identity、safe contact、health、immigration、criminal、child dataをrestrictedにする。
5. civil、criminal、administrative、family等をforum-specificにrouteする。
6. current official sourceとfuture-lawを分ける。
7. deadlineをcandidateとしてdual verificationする。
8. external artifactはversion-specific lawyer approvalを必須にする。
9. client/matter/sessionをserver bindingで分離する。
10. destination、retention、internal preservation control、court order、DLPを各operationで確認する。
11. `criminal | immigration | housing | benefits`はapproved source cardがない限り
    safety/urgency/referralだけ。
12. consequential translationはresponsible-lawyer legal reviewとcompetent-language
    reviewの両方。

## 日本へ移植しないUS default

ABA Formal Opinion 512、Model Rules、米国student-practice rule、`Certified Legal
Intern`、FRCP 26(b)(3) work product、Westlaw/CourtListener中心の日本法調査、州別
plausibility bands、米国のlimitation/service/filing/certificate-of-service、
immigration/eviction/FDCPA formを日本法として使わない。

IRACはpedagogy scaffoldとして利用できるが、日本法の必須形式とは表現しない。
日本の裁判所・行政庁文書はcurrent official form、事件固有命令、責任弁護士precedent
から作り、`court-ready`ではなく`court-or-agency draft`とする。

`legal hold`はinternal preservation controlとして扱い、FRCP 37(e)又は日本法上の
一般的同等制度と表示しない。法的保全根拠がある場合は別source fieldへ記録する。
