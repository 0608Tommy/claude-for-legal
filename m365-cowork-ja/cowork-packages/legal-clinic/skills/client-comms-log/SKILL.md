---
name: client-comms-log
description: >
  authorized clinic matterの依頼者communicationをadd、read、summary、patternsで扱うSharePoint / Power Platform front end。safe-contact、language、interpreter、approved artifact、reviewer、delivery evidenceを最小限で記録し、過去entryを上書きせずcorrectionを追記する。append-only integrityとretentionを分け、送信又は法律助言を実行しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: power-platform
  logical-target-id: ja-jp.power.legal-clinic.client-comms-log
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Client communications log

canonical label:
`/legal-clinic:client-comms-log [matter-id] [--add | --read | --summary | --patterns]`

## Mandatory matter / privacy / write gate

1. `references/common/cowork-runtime-contract.md`を読み、exact userとnon-null、
   unexpired session–matter binding、active engagement/scope、authorized ACLを確認する。
2. bindingがない、別client/matter、expired、conflict/engagement不明なら停止する。
   switchはcurrent bindingをrevokeし、新しいCowork conversationを要求する。
3. identity、safe-contact、health、immigration、criminal、child/family/DV、
   interpreter dataはrestricted itemから必要最小限だけ読む。
4. gateway、state list、conditional create、append-only audit、retention/preservation、
   storage/flow DLPをlive preflight。失敗時はsession内formatted entry draftだけ。
5. `add`はexact previewとfresh confirmation後、`expectedAbsent: true`、
   idempotencyでcreateする。past entryをupdateしない。
6. correctionはnew entryで`correctionOfEntryId`を参照する。
7. communication recordはsend/delivery、法律助言、client understandingの証明ではない。
8. Cowork内DLPが必須ならconfidential contentを投入しない。
9. writeは`references/common/clinic-state-payloads.schema.json`の
   `trackerRecord` + `communicationPayload`へvalidateし、artifact item/version/hash、
   destination、reviewer、delivery evidenceを必須fieldとして扱う。
   outer `scopeType: matter`、`scopeId == payload.matterId`をsemantic validateし、
   duplicated tenant/practice fieldはouter値と一致させる。
10. consequential translationはresponsible-lawyer legal reviewとcompetent-language
    reviewの両方を同じartifact version/hashに要求する。

Japan:
`references/common/ja-jp/client-access-and-communications.md`。

## Mode

| mode | behavior |
|---|---|
| `add` | human-confirmed communication entryをcreate |
| `read` | authorized exact matterのrecent entries |
| `summary` | source IDs付きcondensed factual summary |
| `patterns` | unanswered、follow-up、language、安全、contact gap candidate |

defaultは`add`。modeとmatter IDを会話名から推測しない。

## `add`

minimum input:

- occurred date/time、direction、medium
- actor、client-side participantのpseudonymous ID
- language、interpreter/accessibility
- 2～4文のfactual summary
- action items、follow-up candidate
- inbound/outbound artifact item/version
- outboundならresponsible lawyer reviewer、approved version、destination
- delivery evidence又は`not-confirmed`
- translated legal/deadline/scope contentなら両review record

tone、credibility、mental state、family dynamicを根拠なく記録しない。substantive legal
analysisは`internal-memo`へ分ける。deadline、scope、legal position、bad newsを含む
outbound communicationはresponsible lawyer approvalなしに記録をrelease-readyとしない。

write sequence:

1. current safe-contact、destination、artifact hash/versionを再取得。
2. formatted entryとrestricted fieldsを表示。
3. fresh confirmation。
4. canonical key、unique idempotency、`expectedAbsent: true`でcreate。
5. returned exact item ID/eTag/versionを表示。
6. audit append。

## `read`

exact matter、authorized viewer、scope-specific cursorを使う。default 5 entries。
identity mapping又はsafe-contact restrictionを一般summaryへ展開しない。

## `summary`

last contact、entry count、open action candidates、unanswered inbound、language/
accessibility、delivery evidence gapsをsource entry IDs付きで示す。semester handoffへ
渡す場合もincoming conflict clearance後だけ。

## `patterns`

candidateとして次をsurfaceする。

- inbound後にoutbound/delivery evidenceがない
- follow-up candidate経過後にresolution entryがない
- unsafe channelとsafe-contact recordの不一致
- requested language/interpreter/accommodationの未対応
- active matterで長いcontact gap

client emotion、student fault、malpracticeを自動結論にしない。urgent safety/deadlineを
検知したらresponsible lawyerとapproved emergency/docket routeへescalate candidateを
作るが、response又はdeliveryを約束しない。

child-abuse concernを検知した場合はAI queueを通告と扱わず、responsible lawyer/
designated humanがcurrent lawと守秘を直ちに評価するhuman routeを示す。

## Artifact separation

communication trackerは`tracker-record`。内部strategyは`internal-memo`、clientへ送る
文面は`client-safe-draft`、court/agency文書は`filing-draft`。相互に自動変換しない。

## 行わないこと

- Outlook/Teams/SMS/letterのsend/post
- client advice、scope change、accept/decline、case close
- past entry overwrite/delete
- append-onlyを永久保持として扱う
- cross-matter pattern scan without explicit authority
- delivery evidenceなしに「送信済み」「連絡済み」と表示
- Power Platform flow又はscheduleがprovision済みと主張
