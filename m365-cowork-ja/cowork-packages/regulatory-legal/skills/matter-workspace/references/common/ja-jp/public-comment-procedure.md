> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本の意見公募・consultation tracking

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

## Procedure type

- `statutory-public-comment`: 行政手続法に基づく意見公募手続
- `voluntary-consultation`: 任意の意見募集
- `sro-consultation`: JPX/JSDA等
- `ministry-hearing`: hearing/meeting
- `information-request`: 情報提供依頼
- `local-procedure`: 条例等に基づくlocal procedure

同じe-Gov上に表示されてもstatutory/voluntaryを分ける。SRO/local procedureへ
行政手続法の30日原則を自動適用しない。

## Record kind

- `consultation`: proposalと意見受付があるrecord
- `exception-notice`: prior consultationを行わないexception公示
- `result-only`: result/final artifactだけを取得したrecord

`exception-notice`または`result-only`ではproposal/open/close datesをnullにできる。
prior consultationがない場合、架空の日付を補わず`exceptionBasis`とreasonを保存する。
final resultは`adopted | not-adopted | withdrawn`で記録する。

## Store verbatim

- パブリック・コメント制度 / 意見公募手続
- 行政手続法に基づく手続 / 任意の意見募集
- 命令等の案
- 案件番号
- 根拠法令条項
- 案の公示日
- 受付開始日時 / 受付締切日時
- 30日未満の場合の理由
- 意見募集要領
- 結果の公示日
- 命令等の公布日 / 対象が定められた日
- 提出意見数、考慮、修正の有無、結果・理由

statutory periodは原則30日以上だが例外・短縮がある。意見は票数でなく内容を考慮。

## Deadline rules

1. raw displayed datetimeと`Asia/Tokyo` normalized ISOを保存。
2. end-of-dayを推測しない。
3. RSS `dc:date`はfeed publication timeで、legal deadlineではない。
4. detail recordと全ての意見募集要領・draft attachmentを開く。
5. routeごとにmethod、exact destination、instruction URL+hash、deadline、
   receipt-or-postmark、verifiedAtを保存。
6. official deadlineとinternal review dateを別field。
7. T-14、T-3、T-1、immediately-before-submissionで再確認。
8. close後もresult RSSをmonitorし、result、final instrument、官報、effective dateをlink。
9. proposal/result version labelが異なっても両snapshotを保持。
10. `waived`は真正なwaiver以外`not_filing`。

email/postal routeを名称や過去案件から推測しない。verified instructionにないrouteは
`unknown`としてblockし、route-specific deadlineとreceipt/postmark ruleを他routeへ
流用しない。

## Verified fixtures

| 案件番号 | required behavior |
|---|---|
| `240000127` | 2026-07-16 00:00 open、2026-08-14 23:59 close。canonical entry `https://public-comment.e-gov.go.jp/pcm/detail?CLASSNAME=PCMMSTDETAIL&id=240000127`、instruction PDF `https://public-comment.e-gov.go.jp/pcm/download?seqNo=0000318027`、SHA-256 `e7bb3a9145c11b02f31c2b223a91d3c3b0a3f6168e060f1995fef0dcd93d5035`、POST action `https://public-comment.e-gov.go.jp/pcm/2010`、`CLASSNAME=PCMIKENINPUT`、case ID `240000127`、form routeのpostal timingはnot-applicable |
| `155260508` | 2026-07-16 00:00 open、2026-07-29 23:59 close。行政手続法40条1項shortened period。災害発生時の復旧措置を災害に備え可能な限り速やかに施行するため政令を速やかに定めるexact reasonを保持。39条4項1号にしない |
| `495260109` | 2026-07-14 10:20 open、2026-08-14 00:00 close。23:59へnormalizeしない |
| `495260046` | 2026-05-01 proposal、2026-06-01 12:00 close、result/promulgation 2026-07-15、adopted |
| `495250498` | 任意の意見募集。proposal title/versionは`6.1`、final artifactは`7.0`。両snapshotを保持 |
| `155260717` | 行政手続法39条4項8号のno-prior-consultation。2026-05-20公布、2026-07-16結果掲載は43条5項に反するapparent late result-publication/source-control failureとしてflagし、normal delayにしない |

fixture sourceは2026-07-16 09:01:03+0900生成のopen/result RSSとlinked detail。

## Decision lifecycle

```text
undecided
filing
not_filing
filed
withdrawn
result_published
final_instrument_linked
```

`filing`は内部decision。実際の提出ではない。`filed`はverified route、human-provided
submission/receipt evidence、qualified reviewがある場合だけ。結果掲載後もfinal
instrument、disposition、version relationを追跡するが、155260717のapparent
late-publicationをnormal operational lagとして一般化しない。

## Human gate

comment positionは会社のpublic record、later proceeding、trade association
coordination、admission、consistencyへ影響し得る。draft、internal decision、
submissionを別operationにする。AIは提出しない。

提出前に:

- qualified Japanese counsel review
- authorized company owner/submitter
- exact case ID、proposal/version、verified route ID
- route-specific destination、instruction URL/hash、deadline、receipt-or-postmark、
  verifiedAt
- exact artifact ID/hash
- public/confidential information check
- destination、DLP、fresh human confirmation

提出用web form、email、postal actionはhuman process。verified instructionにrouteが
なければemail/postを提案・推測しない。skillはcopy-ready draftまたはmanual checklistまで。

## Notification

assignment/reminderはrecipientとmessage全文をpreviewし、毎回explicit yes。
batch/cadenceでもauto-sendしない。deadline/citationが未確認ならmessageにも残す。
