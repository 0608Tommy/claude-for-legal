> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本の法的status、改正、施行日

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

## Independent status model

canonical `lifecycleStatus`:

| status | workflow |
|---|---|
| `proposed` | consultation、bill、draft、deliberative item。current obligationにしない |
| `current` | current version。force/applicabilityは別fieldで確認 |
| `future-effective` | adopted/promulgated等だが将来施行・適用 |
| `not-adopted` | proposal/resultが不採用 |
| `withdrawn` | proposal/instrumentが撤回 |
| `superseded` | later version/instrumentに置換 |
| `repealed` | 廃止 |

日本固有の`bill-pending`, `passed-not-promulgated`,
`promulgated-not-effective`, `partially-effective`, `effective`,
`result-published`等は`processStage`へ保存する。normative force、applicability、
instrument class、jurisdiction/nexusをlifecycleへ押し込まない。

## Verification sequence

1. exact Japanese title、authority、instrument class。
2. law/bill/public-comment/SRO ID。
3. bill passage status。
4. 官報公布日、種類、号、page、signature/timestamp。
5. e-Gov `law_id`と`law_revision_id`。
6. `CurrentEnforced`, `PreviousEnforced`, `UnEnforced`。
7. 附則、施行期日、article-level commencement。
8. 適用日、経過措置、猶予、grandfathering。
9. implementing政令、省令、委員会規則、告示。
10. later amendment、repeal、future revision、conflict。

lifecycle、process stage、force、applicability、dateは別field。current instrumentでも
一部provisionのapplication dateが将来の場合がある。単一`due`へ潰さない。

## e-Gov revision behavior

Law API revision recordsはcurrent、previous、future-unenforcedを区別する。
行政手続法`405AC0000000088`のrevision endpointは、2026-07-16確認時に
2026-06-24施行のcurrent revisionと2028-12-23予定のfuture revisionを示した:

https://laws.e-gov.go.jp/api/2/law_revisions/405AC0000000088

2026-06-24 revisionのtextは次のrevision-pinned URLで固定する:

https://laws.e-gov.go.jp/api/2/law_data/405AC0000000088_20260624_508AC0000000046

future revisionをcurrent textとしてdiffしない。text取得時はrevision IDとhashを
固定し、proposal/final/historical versionをoverwriteしない。

## 官報

官報はpromulgation record。e-Gov consolidated textまたはpublic-comment resultとは
役割が異なる。官報PDFの電子署名/timestampを確認する。

官報法16条は、電子官報の全記録を含み他人の利用に供するdatabaseについて承認制を
置く。個別取得、部分dataset、内部利用を同じ制限と推測せず、予定するdatabaseの
coverage・提供先・用途を確認する。

site termsはsiteへ負荷を与えるrobot/crawler collectionを禁止するのであり、あらゆる
automation requestを一律禁止するとは記録しない。rate、coverage、terms、Art.16該当性を
確認し、未確認ならadapter/manual/licensed routeへfallbackする。

## Dates

最低限分離:

```yaml
proposalAt: null
commentOpenAt: null
commentCloseAt: null
passedAt: null
promulgatedAt: null
effectiveDates: []
applicationDates: []
transitionDates: []
internalTargetAt: null
revisitAt: null
```

raw displayed datetimeと`Asia/Tokyo` normalized ISOを保持する。date-onlyを
23:59へ推測しない。official deadlineとinternal deadlineを分ける。

## Analysis branch

- `proposed` + consultation/bill/deliberative process stage → readiness/watch
- `future-effective` → implementation gap
- `current` + binding + applies → compliance diff
- `current` + nonbinding guideline → alignment/organizational choice
- `current` + binding-on-covered-parties exchange/SRO rule → exact covered-party scope
- `not-adopted | withdrawn | superseded | repealed` → close/supersession analysis

## False statements to avoid

- press releaseがあるため施行済み
- 結果公示があるためfinal rule施行済み
- e-Gov consolidated pageがあるため全改正が現行
- 成立日が施行日
- SRO ruleが全企業へ法定適用
- ガイドライン違反が直ちにstatutory violation
- internal target missがofficial deadline miss
