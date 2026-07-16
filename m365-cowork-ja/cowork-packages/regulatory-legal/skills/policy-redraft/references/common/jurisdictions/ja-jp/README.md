> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# `ja-JP` 規制対応法務module

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

本moduleは日本に関係する規制監視、policy diff、gap/comment tracking、policy
redraftへ追加するjurisdiction adapterであり、U.S. workflowの単純翻訳ではない。

## 選択条件

`request > matter > practice-profile > tenant-default`

最終的に日本が含まれる場合、本moduleを適用する。`Japan`, `日本`, `JP`,
`ja-JP`が矛盾する、entity/affected activity所在地が不明、または外国法も適用し得る
場合は、対象ごとに法域を分ける。

## Independent classification

各itemはjurisdiction/nexus、instrumentClass、normativeForce、lifecycleStatus、
applicabilityを独立して保存する。`displayTags: [B,G,P,I,F,X]`は複数可の表示用で、
force/statusを決めない。外国法もbindingかつfuture-effectiveになり得る。

## Lifecycle

canonical:
`proposed | current | future-effective | not-adopted | withdrawn |
superseded | repealed`。

法律案、成立、公布、段階施行等の詳細は`processStage`とdate fieldsへ保存する。

authoritative sequenceは法律案、成立、官報公布、施行。titleまたはpress releaseだけで
binding/effectiveと推測しない。`告示`は法的委任によりbindingの場合があり、
`ガイドライン`と同じclassにしない。

`isAdministrativeGuidance`とbasisを必ず分ける。行政手続法32条から36条の3
（36条の2・36条の3を含む）の行政指導と、
名称だけがguideline/指針のgeneric official documentを同一視しない。

## 読み分け

| 論点 | 読むファイル |
|---|---|
| lifecycle、附則、改正、経過措置 | [legal-status-and-effective-dates.md](legal-status-and-effective-dates.md) |
| 意見公募、任意募集、deadline、結果 | [public-comment-procedure.md](public-comment-procedure.md) |
| FSA、JPX、JFTC、PPC、MHLW、METI、MIC等 | [regulator-source-pack.md](regulator-source-pack.md) |
| official URL、role、確認日 | [source-register.md](source-register.md) |
| stale/future/change watch | [currency-watch.md](currency-watch.md) |

## Mandatory Japan preflight

1. activity/entity/affected personのJapan nexus。
2. authority、instrumentClass、delegation、normativeForce。
3. lifecycleStatus、processStage、applicability。
4. e-Gov `law_id`、`law_revision_id`、Japanese text。
5. 官報reference、electronic signature/timestamp、permitted access method。
6. 附則、article-level commencement、application date、transition。
7. implementing order、ordinance、commission rule、notice。
8. later amendment、repeal、future-unenforced revision。
9. exchange/SRO ruleのexact issuer、venue、approval、covered party。
10. national sourceでprefecture/municipalityをcoverageしたと表示しない。
11. deadlineはraw datetime、`Asia/Tokyo`、submission method。
12. primary-source conflict、missing attachment、source terms。

## False equivalence

- Federal Registerは官報そのものではない。e-Gov法令・意見公募とも別。
- NPRMと命令等の案は近似であり同一制度ではない。
- ANPR/RFIにuniversalな日本法categoryはない。
- 案件番号はRegulations.gov型docketではない。
- 結果公示は公布または施行ではない。
- `成立`は`公布`または`施行`ではない。
- public commentは投票ではない。
- 英訳は参考。日本語本文が法的に支配する。

## Gate

sourceを取得できない、lifecycle/applicabilityが未確認、分類fieldが衝突、
qualified Japanese counsel reviewがない場合は`pending`または`[review]`。
house materialityはscreeningを調整できるがbinding obligation、covered-party
exchange/SRO requirement、official deadlineを下げない。
