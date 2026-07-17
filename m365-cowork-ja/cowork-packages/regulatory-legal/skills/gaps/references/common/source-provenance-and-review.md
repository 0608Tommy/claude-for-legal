> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 情報源、法的character、status、レビューの共通ルール

## Independent legal/source dimensions

`B/G/P/I/F/X`をmutually exclusiveなforce/statusとして保存しない。authoritative
recordは次を独立fieldで持つ。

```yaml
jurisdictions:
  - JP
nexus:
  - jurisdiction: JP
    basis: "[entity/activity/territory/venue/contract]"
    facts: []
    status: established | potential | absent | unknown
instrumentClass: statute | cabinet-order | ministerial-ordinance | commission-rule | delegated-notice | administrative-guidance | official-guideline | faq | cabinet-decision | bill | consultation | council-material | exchange-rule | sro-rule | platform-policy | internal-policy | enforcement-action | judgment | other
normativeForce: binding | nonbinding | binding-on-covered-parties | contractual | internal | unknown
lifecycleStatus: proposed | current | future-effective | not-adopted | withdrawn | superseded | repealed
applicability:
  status: applies | potentially-applies | does-not-apply | unknown
  basis: "[scope test]"
  coveredParties: []
  territorialScope: []
  conditions: []
displayTags:
  - B
  - F
  - X
```

`displayTags`は複数可のUI shorthandに限る。外国法は`[X,B]`または`[X,B,F]`に
なり得る。tagからforce、currentness、applicabilityを推測しない。internal policy
違反を違法と書かず、exchange/SRO ruleをstatuteまたはordinary platform contractと
扱わない。

proposal/current/futureは`lifecycleStatus`、territorial/party scopeは
`applicability`、法的拘束性は`normativeForce`に置く。`成立`、`公布`、`施行`等の
詳細は`processStage`、effective/application/transition dates、source revisionで
補足する。結果公示はfinal instrument、官報公布または施行を意味しない。

## Administrative guidance

```yaml
isAdministrativeGuidance: false
administrativeGuidanceBasis:
  basisType: apa-arts-32-through-36-3 | sector-statute | other | none | unknown
  statute: "[law/source or null]"
  provisions: []
  classificationReason: "[why this is or is not administrative guidance]"
```

行政手続法32条から36条の3（36条の2・36条の3を含む）の「行政指導」は法的概念である。資料名に「ガイドライン」
「指針」「手引」が含まれるだけでは`isAdministrativeGuidance: true`にしない。
generic official guideline、FAQ、supervisory materialはitemごとにinstrument class、
basis、normative forceを確認する。
sector-statute basisはexact statuteとnonempty exact provisionsを要求する。

## Findingの必須field

```yaml
jurisdictions: []
nexus: []
instrumentClass: "[canonical instrument class]"
normativeForce: binding | nonbinding | binding-on-covered-parties | contractual | internal | unknown
lifecycleStatus: proposed | current | future-effective | not-adopted | withdrawn | superseded | repealed
applicability:
  status: applies | potentially-applies | does-not-apply | unknown
  basis: "[scope test]"
  coveredParties: []
isAdministrativeGuidance: false
administrativeGuidanceBasis: {}
marketRuleContext:
  kind: exchange | non-exchange-sro | null
  issuerEntity: "[exact entity or null]"
  venue: "[exact venue or null]"
  approvalRequired: true | false | unknown | null
  approvalAuthority: "[exact authority or null]"
  approvalStatus: "[status or null]"
  approvalBasis: "[source/provisions/exact pin status or null]"
  coveredParties: []
displayTags: []
sourceSystem: "[canonical source system]"
sourceItemId: "[exact source item ID]"
sourceVersionOrRevisionId: "[exact version/revision ID]"
sourceUrl: "[official or exact source URL]"
effectiveDates:
  - "[date/provision/status]"
applicationDates:
  - "[date/scope]"
transitionDates:
  - "[date/measure]"
verificationState: verified-current | verified-future | conflicting | pending
factsNeeded:
  - "[結論を左右する事実]"
humanOwner: "[legal/compliance/policy/business/other]"
```

## 情報源順位

1. 官報、e-Gov法令、e-Gov意見公募、国会、内閣法制局、所管当局、裁判所、
   JPX/JSDA等のofficial primary source。
2. authorized SharePoint record、policy正本、利用者提供資料。
3. current legal research database。
4. 二次資料。一次資料発見のleadに限定する。

Federal RegisterはU.S. federal sourceだけに使う。EUはEUR-Lex / Official Journal、
UKはlegislation.gov.ukと所管当局、その他はjurisdiction-specific official register/
regulatorを使い、Federal Registerをglobal fallbackにしない。

施行日、改正status、deadline、threshold、designation、SRO scope、enforcement
postureに依存する場合、その会話でcurrent official sourceを確認する。
[日本法router](ja-jp/README.md)と
[source register](ja-jp/source-register.md)は検索indexであり、
個別適用判断または将来の正確性を保証しない。

## 情報不足の3値

1. sourceを取得しprovenance tag付きで進む。
2. exact text/recordまで停止する。
3. 結論には使わないが、結果を変え得る既知の改正、延期、将来revision、
   enforcement moratoriumを`[model knowledge — verify]`で示す。

利用者が示したlaw、article、case、date、deadline、threshold、jurisdictionも分析前に
確認する。原文未取得で理解が衝突すれば内容を創作せず
`[statute unretrieved — verify]`とする。

## Provenance tag

- `[primary source]`
- `[official guidance]`
- `[SRO/exchange policy — live version]`
- `[user provided]`
- 実際に応答したtool名
- `[secondary — verify against primary]`
- `[model knowledge — verify]`
- `[settled — last confirmed YYYY-MM-DD]`
- `[verify]`, `[review]`
- `[retrieved but verify support]`
- `[premise flagged — verify]`
- `[statute unretrieved — verify]`

tagはconfidenceではなく取得経路を表す。URL、law ID、`law_revision_id`、案件番号、
canonical source IDを翻訳・改変しない。CourtListenerは日本のprimary source
connectorではない。英訳は参考で、日本語本文が支配する。

## Citation・record check

- propositionを直接支えるか。
- title、instrument form、authority、delegation、scopeが一致するか。
- definition、exception、附則、経過措置、未施行revisionを落としていないか。
- guidance、SRO/platform policy、internal controlをlawとして扱っていないか。
- proposal/final/historical snapshotを上書きしていないか。
- public-comment deadlineのraw表示時刻、timezone、submission methodを保持したか。
- tool resultとmodel knowledgeが衝突した場合、両方と衝突点を示したか。

## レビュー担当者向け注記

成果物の直前に1blockだけ置く。

> **⚠️ レビュー担当者向け注記**
> - **Sources:** [取得source、未接続source]
> - **Read:** [documents/pages/records、coverage、未読]
> - **Jurisdiction / nexus / instrument / force / applicability:** [independent fields]
> - **Lifecycle / dates:** [proposed/current/future-effective等、effective/application/transition]
> - **Flagged for your judgment:** [`[review]`件数]
> - **Destination:** [保存先、viewer、秘密性]
> - **Before relying:** [有資格者が確認する1～2点]

meta-commentaryを本文へ散らさない。すべて確認済みなら1行へ短縮できる。

## 判断姿勢、role、severity

不確かな主観判断は見落としより回収可能な過剰flagを選び`[review]`を付ける。
上流severityは下流のfloor:

- 🔴 Blocking
- 🟠 High
- 🟡 Medium
- 🟢 Low

Non-lawyer利用者にはresearch notes / draftとして構成し、attorney routeを示す。
lawyer roleでもAIはmateriality、applicability、comment position、policy approval、
filing、submission、certificationを最終決定しない。

## Verification audit

法令、guidance、SRO rule、deadline、thresholdを確認したらcanonical auditへappend:

```yaml
eventType: legal-source-verified
details:
  citeOrFact: "[cite or fact]"
  jurisdictions: []
  instrumentClass: "[class]"
  normativeForce: "[force]"
  lifecycleStatus: "[status]"
  applicabilityStatus: "[status]"
  displayTags: []
  sourceSystem: "[canonical source system]"
  sourceItemId: "[exact source item ID]"
  sourceVersionOrRevisionId: "[revision/version ID]"
  sourceUrl: "[official source URL]"
  checkedAt: "[ISO-8601]"
  verdict: confirmed | corrected | could-not-verify
  correction: "[corrected value or null]"
```

監査recordを編集・削除しない。

## 次の選択肢

分析後はAIがdecisionを選ばず、自然なdraft、named ownerへのescalation、追加事実、
tracker候補、watch、その他を示す。外部send、post、publish、file、submit、state
writeは別operationである。
