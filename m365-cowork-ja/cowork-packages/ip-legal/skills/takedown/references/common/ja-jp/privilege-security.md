> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本の秘密性・matter security

## Legal position

- **[B] Attorney Act Art. 23:** bengoshiのprofessional secret。
- **[B] Patent Attorney Act Art. 30:** benrishiのbusiness secret。
- **[B] Civil Procedure Code Art. 197:** specified professionalsのtestimony refusal。
- **[B] Art. 220(4)(c):** unwaived professional/technical secretを含む文書の取扱い。

これらをblanket client-held U.S. attorney-client privilegeまたはwork-productと
表示しません。in-house non-lawyer analysisはlabelでprivilegedになりません。
日本のbenrishi protectionを*Queen's University*のU.S. patent-agent privilegeと
同一視しません。

truthful internal header example:

`秘密・社外秘 — 日本法上の秘匿特権の有無は文書、作成者、目的及び手続により異なる。外部共有前に日本法弁護士確認。`

## Matter controls

- private practice matter作成前にconflict search。Attorney Act Art. 25を確認。
- key:
  `tenantId + practiceId + userObjectId + sessionId + matterId`
- shared global active matterを作らない。
- SharePoint item-level ACL、separate retrieval index、clean-team membership。
- cross-matterはexplicit purpose、exact IDs、authorizationが必要。
- exact item ID、eTag、idempotency、append-only audit。
- close時に全binding revoke。
- invention-security-screened materialをunapproved/cross-border connectorへ送らない。

`clean-team` labelだけでtechnical isolation済みと表示しません。

## Cowork DLP blocker

2026-06-22時点でCowork prompt/taskのPurview DLP/data classificationは未対応です。
storage/flow DLPで代替できると表示しません。prompt-level DLPが必須のtrade secret、
unpublished invention、litigation strategyはproduction blockerです。

## Destination

counterparty、platform、public channel、customer/distributor、foreign associate、
external search serviceへの共有前に、authority、purpose、minimum necessary、
NDA、export/economic security、retention、source termsを確認します。

internal analysis、external C&D、provider notice、Customs application、board/business
summaryを別artifactとして作り、internal noteを外部版へ混ぜません。
