> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本規制対応 currency watch

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

本書は検索checklistであり、個別案件への適用または将来の正確性を保証しない。
status、revision、deadline、source termsに依存する場合、その会話でofficial sourceを
再取得する。

## Current observations

- 電子官報は2025-04-01開始。PDFの電子署名/timestampと利用規約を確認する。
- 官報site termsは負荷を与えるrobot/crawler collectionを制限する。全automationを
  blanket禁止とせず、官報法16条のall-records/third-party database approvalも別確認。
- e-Gov Law APIはcurrent/previous/future-unenforced revisionを分ける。
- 行政手続法revision endpointは2026-06-24 currentと2028-12-23 future revisionを
  2026-07-16確認時に表示した。
- Ministry of Justice等の英訳は参考で、日本語textが法的に支配する。
- MIC RSSと衆議院議案pageはShift_JIS。
- MHLW law databaseはmonthly updateで、「登載準備中」がある。
- JFTC/METI/MAFF automated retrievalはadapter-required/manual。
- 国家サイバー統括室はhttps://www.cyber.go.jp/。NISCはhistorical alias。
- national sourcesはlocal ordinance/gazette/consultationをcoverageしない。

## Recheck trigger

- 施行日または適用日が近い。
- passed/promulgated/effectiveの境界。
- future `law_revision_id`がcurrentへ変わった。
- public-comment route別instruction URL/hash、deadline、receipt-or-postmark、verifiedAt。
- result publication、final instrument、官報relation。
- SRO rule、membership、listing、designated status。
- regulator enforcement posture。
- source page/format/encoding/terms変更。
- last checkedから90日超。

## Per-item currency fields

```yaml
checkedThrough: "2026-07-16"
retrievedAt: "[ISO-8601]"
sourceSystem: "[canonical source system]"
sourceItemId: "[exact source item ID]"
sourceVersionOrRevisionId: "[revision/version ID]"
lifecycleStatus: proposed | current | future-effective | not-adopted | withdrawn | superseded | repealed
verificationState: verified-current | verified-future | conflicting | pending
nextRecheckAt: "[ISO-8601]"
recheckTrigger: "[event]"
```

90日超更新されていない場合、本書をcurrent statusのsourceとして使わず、検索対象の
一覧としてのみ使う。更新時はsource、version、変更内容をcanonical auditへappend。
