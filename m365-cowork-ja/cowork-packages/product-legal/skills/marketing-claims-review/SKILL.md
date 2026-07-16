---
name: marketing-claims-review
description: >
  marketing copy、画像、disclaimer、review/testimonial、landing page、subscription final screenをcomplete consumer impressionで確認する。景品表示法、stealth、特定商取引法、消費者契約法、sector rule、platform policy、house standardを分離し、evidenceと修正文案をdraftする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: product-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Marketing claims review

正規labelは `/product-legal:marketing-claims-review [asset]`。

本skillはreview draftと修正文案を作る。claim approval、publication、posting、
campaign activationを行わない。

## Mandatory gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読む。gateway unavailable
   時はcurrent requestのasset/evidenceだけを使うread-only/manual draft mode。
2. exact user/company/product-legal practice profileのclaims posture、
   substantiation standard、comparative policy、escalationを読む。unavailable時は
   `[PROVISIONAL — profile unavailable]`。
3. matter scopeはactive/unexpired non-null binding。practice modeはfresh session
   でbinding不在。archived/revoked/expiredでは停止。
4. jurisdictionを解決し、日本があれば
   [consumer/claims module](references/common/jurisdictions/ja-jp/consumer-commerce-claims.md)
   とtriggerしたsector moduleを読む。
5. [法源rule](references/common/source-provenance-and-review.md)に従い
   `[B]/[G]/[P]/[I]/[F]/[X]`を分ける。platform policyはlive fetch。
6. rendered asset、surrounding page、locale、device、destination、advertiser/
   supplier identity、actual product/spec、evidence、purchase flowを取得する。
7. source item/version、screen timestamp、coverage、unread visualを記録する。
8. claim evidenceはpublication前に存在するかを確認。法的floorをhouse postureで
   demoteしない。
9. destination、viewer、confidentiality、DLPを確認。internal analysisと
   marketing向けclean revisionを分ける。
10. state write、publish、send、post、claim approvalは別operation。AIは実行しない。

## Scope — words onlyではない

日本のstealth marketing、overall impression、disclaimer prominence、SCTA final
screenは文字列だけでは確認できない。次を求める。

- rendered screenshot/video/story/thread
- surrounding page、preceding/following step
- desktop/mobile/app、locale
- font、placement、timing、contrast
- landing pageからpurchase/final screenまで
- image、icon、ranking、award、customer logo
- synthetic person/review/testimonial
- platform destinationとlive policy

visualを取得できない場合、`text-only partial review`と明示し、ready/publication
postureを出さない。

## Claim taxonomy — issue spotting only

- vague / subjective
- specific factual
- comparative
- implied
- absolute

`puffery`を自動safe harborにしない。audience、context、complete impression、
consumer reliance、sector claimを確認する。

## Step 1 — Extract and map

exact quote、visual implication、disclaimer、link/footnote、speaker、material
connection、destinationを一覧化する。

marketing assetが短い場合も、headlineだけでなくsurrounding contextを読む。

## Step 2 — Separate legal calls

各claim/flowについて、applicable rowだけを使う。

| Layer | Question |
|---|---|
| `[B] 景品表示法` | superiority/advantage misrepresentation、reasonable basis、complete impression |
| `[B/G] stealth designation/FAQ` | advertiser involvement、commercial nature、overall presentation |
| `[B/G] SCTA` | 通信販売広告、subscription/trial、final confirmation screen |
| `[B] Consumer Contract Act` | solicitation、misrepresentation、consumer-prejudicial term |
| `[B/G] sector advertising` | medical/health/finance/children等 |
| `[P] platform policy` | live ad/review/synthetic-content rule |
| `[I] house standard` | comparative、absolute、substantiation、brand posture |
| `[X] foreign law` | FTC/NAD/COPPA/U.S. state/EU等の独自nexus |

1つのgeneric `advertising law`へまとめない。

## Step 3 — Evidence

- evidence existed before publication
- who measured、when
- methodology、sample、representativeness
- apples-to-apples comparison
- product version、market、locale
- limitation/disclaimerがclaimを実際に限定するか
- current count/award/certification
- security/accuracy/fairness claimの具体的meaning

合理的根拠資料提出の一般的15日説明に依存する場合、current CAA sourceを確認する。

## Step 4 — Stealth / reviews / AI

- advertiser/supplier involvement
- employee/vendor/influencerへの指示、対価、content/review process
- review solicitation/moderation
- `広告`, `PR`, platform disclosureのvisibility
- synthetic person、AI-generated review、voice/image
- commercial natureが全体で明瞭か

`#ad`、platform toggle、AI labelはsafe harborではない。逆に、すべてのAI-assisted
contentへ一律の日本法label義務があるとも書かない。`material connection`は
外国法または社内taxonomyとして補助的に使えても、日本の告示上の独立要件として
扱わない。

## Step 5 — Commerce/final screen

subscription、trial、auto-renewal、in-app purchaseでは:

- total price/fees
- quantity/duration
- renewal/trial conversion
- cancellation method/deadline
- return/refund
- final confirmation screen
- button/label/correction

termsだけで確認を終えない。

## Step 6 — Claim-by-claim output

```markdown
**Claim / impression:** "[exact quote or visual implication]"
**Type:** [taxonomy]
**Audience / placement:** [context]
**Evidence:** [item/version/date | missing]
**Draft posture:** [No issue identified | Evidence needed | Reword | Remove/hold | Visual review incomplete]
**Legal character:** [B/G/P/I/F/X]
**Source/effective status:** [URL/date/current]
**Suggested revision:** "[copy-ready wording]"
**Why / facts needed / human owner:** [one or two lines]
```

short assetは実際のrevised copyを返す。300 words超はclaim-by-claim diffにする。

## Output

[claims output template](references/claims-output.md)を使う。summaryは
`No issue identified in reviewed scope | Changes required | Hold pending evidence |
Partial visual review`とし、`Ready to publish: Yes`またはapprovalを出さない。

## Sector triggers

- medical/health → PMD/Medical Care/Health Promotion/APPI
- finance/payments → registration、disclosure、risk/return/fee
- minors → age、material connection、purchase/consent、vulnerable design
- AI → no fabricated benchmark/review、human escalation、IP/privacy
- public company → selective disclosure、forecast/MNPI

specialist handoffを人に選んでもらい、自動起動しない。

## 行わないこと

- words-onlyでvisual/checkout complianceを確定
- `puffery`を自動ignore
- FTC/NADを日本のcontrolling lawとして使用
- claim substantiationを創作
- publish、post、send、approve
