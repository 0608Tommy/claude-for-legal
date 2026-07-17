---
name: cease-desist
description: >
  知的財産のcease-and-desistを送るための外部文案または受領letterのtriageを作る。日本法では権利・standing・recordal、第三者警告risk、Civil Code Article 150、JPO・Customs・platform routeを確認し、承認前のdraftだけを提供する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Cease and desist

正規label/flags:

- `/ip-legal:cease-desist --send`
- `/ip-legal:cease-desist --receive`

Coworkではflagをconversation stateへ変換します。flagなしなら送付案か受領triageかを
1回だけ確認します。

## 目的

`send`は権利、行為、関係、目的、counterparty diligence、承認を踏まえた外部letter
draftです。`receive`はincoming assertionを権利別に検証し、options memoを作ります。
どちらもlegal opinionではありません。

## Mandatory assertion / security gate

1. [実行・保存契約](references/common/cowork-runtime-contract.md)を読み、
   gateway、scope、ACL、destination、create/update、auditをpreflightします。
   失敗時はsession内read-only draftだけです。
2. exact `user-profile`、`ip-practice-profile`、enforcement posture、approver、
   outside counselを読みます。未設定なら`cold-start-interview`へ案内します。
3. matter scopeならactive/unexpired binding、matter `status: active`、権限を確認。
   fresh practice modeでは過去matterをcarryしません。
4. `request > matter > practice-profile > tenant-default`で法域を解決します。
   日本なら[日本法router](references/common/ja-jp/README.md)と
   [権利行使・Customs](references/common/ja-jp/enforcement-customs.md)。
5. right、registration/status、owner、recordal/chain、territory、standing、
   accused conduct、evidenceをofficial sourceで確認します。
6. external letterとinternal analysisを別artifactにします。日本の秘密性は
   [privilege/security](references/common/ja-jp/privilege-security.md)。
7. counterparty、customer/distributor、partner、press、forum、insurance、
   indemnitor、Customs/platform routeを確認します。
8. draft approvalはsend approvalではありません。AIは送信、service、filing、
   takedown、Customs applicationを実行しません。
9. Cowork内DLP必須なら機密matterを投入せずproductionを停止します。

source tag、reviewer note、severityは
[共通rule](references/common/source-provenance-and-review.md)を使います。

## Conversation state

| state | action |
|---|---|
| `select-mode` | `send`または`receive`を確認 |
| `collect-right` | right、owner、registration/chain、territory |
| `collect-conduct` | who/what/where/when/evidence |
| `relationship` | competitor、partner、former licensee、customer等 |
| `counterparty-diligence` | entity、resources、portfolio、litigation、counsel、relationship |
| `legal-check` | applicable Japaneseまたはoriginal-jurisdiction layer |
| `options` | demand/response options、tradeoff、approver |
| `draft` | internal memoとexternal letter draft |
| `gate` | source、merit、proportionality、approval、destination |
| `confirm-save` | OneDrive draftまたはreviewed output昇格 |

## Send

### Right

- **Trademark:** JPO status、registration/designated goods、owner、licence、
  prior-use/non-use/limitation、UCPA indication。
- **Patent/utility model/design:** current claim/drawing、owner/recordal、annuity、
  correction/invalidation。pending patentはPatent Act Art. 65 warning/compensationと
  post-grant enforcementを分けます。
- **Copyright:** authorship、chain、exclusive authority、protected expression。
  Japanese registrationを必須としません。
- **Trade secret:** secrecy management、usefulness、non-publicity、acquisition/use/
  disclosure act。

### Conduct and evidence

entity、accused product/mark/work、URL/channel/import、first observed date、
dated capture、sample、receipt、source/version/hash、confusion/business harmを具体化します。
薄いrecordを形容詞で補いません。

### Relationship and objective

relationshipを確認し、目的を選びます。

- stop / design-around
- account / information preservation
- inventory recall/destruction candidate
- compensation/licence/coexistence
- domain/account transfer candidate
- written undertaking
- platform route / Customs route

法令上・契約上・事実上の根拠がないremedyを要求しません。

### Counterparty diligence

draft前に次を1blockで示し、人にcalculusを確認してもらいます。

- exact legal entity、group/alias
- size/resources
- adjacent IP portfolio
- reported disputes/filings
- known counsel
- forum/provisional-relief posture
- customer、partner、investor、supplier relationship
- automatic escalation

critical factが確認できなければ停止または`[verify]`で限定します。

### Japanese checks

- Civil Code Art. 150の6-month completion postponementを確認し、repeated demandが
  limitationを再startすると表示しません。
- customer/distributorへのunsupported warningがUCPA false-fact riskを生じるか。
- pending patent warning、non-use cancellation、invalidity、Art. 104-3。
- Japanese content-certified mail/proof of deliveryはdispatch/content evidenceであり
  meritsの証明ではない。
- physical importはCustoms、online contentはprovider/court routeを並行検討。
- Lanham Act、Rule 11、FRE 408、U.S. statutory damages/fee shifting/DJ boilerplateを
  日本letterへ移植しません。

### Draft structure

1. date/sender/recipient
2. subject
3. right and verified status
4. specific conduct/evidence
5. applicable legal basis with provenance
6. proportionate requests
7. response date and method
8. preservation request where appropriate
9. reservation/non-waiver language suitable for the jurisdiction
10. authorized signer block

external letterにはinternal confidentiality/strategy blockを入れません。

## Receive

extract:

- sender、signer、counsel、delivery/date
- asserted right、registration/claim/work、jurisdiction
- alleged conduct/evidence
- legal theory、demand、stated deadline、threat

verify:

- right/status/standing/recordal/chain
- scope、similarity/claim/expression/trade-secret elements
- limitation、non-use、invalidity、licence、prior use、exhaustion
- sender deadlineが法的にbindingか
- insurer/indemnitor/contractual notice

options:

1. narrow compliance/design-around
2. coexistence/licence/negotiation
3. reasoned rejection
4. preserve/no immediate response
5. trademark non-use/invalidation
6. patent/design invalidationまたはArt. 104-3 defense
7. declaratory/provisional-relief strategy with Japanese counsel

2026-05-21以降の日本民事手続では`mints`、electronic service、evidence formatを
current court guidanceで確認します。

## Other jurisdictions

[移行元U.S./global layer](references/common/original-ip-logic.md)を別に適用します。
U.S. C&DのLanham/Copyright/DMCA/Rule 11/DJ analysisを日本結論と混ぜません。

## Output and loud gate

internal memo:

- reviewer note
- mode、right、jurisdiction、source/coverage
- diligence
- factors/defenses
- options/recommendation candidate `[review]`
- approver、automatic escalation、destination

external draftの直前に確認します。

> **このdraftは送信物ではありません。**
> 権利、standing、record、claim、evidence、法域、demandのproportionality、
> counterparty diligence、named approver、authorized signer、destinationを
> 有資格者が確認するまで送信しないでください。

保存はOneDrive draftが既定です。SharePoint `outputs`昇格と外部sendは別operation。

## 行わないこと

- C&D、soft letter、responseをsendする
- platform/Customs/courtへsubmitする
- infringement/non-infringementを結論する
- unverified registration、claim、statute、caseを補完する
- same approvalでdraft/save/sendをまとめる
- local file、agent、hook、subagentを使う
