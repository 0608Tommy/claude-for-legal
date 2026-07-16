> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本のリーガルクリニック法務router

**状態:** DRAFT — qualified Japanese counsel and clinic supervisor review pending
**checked through:** 2026-07-16 JST

## 適用順序

1. requestに明示された法域、forum、事件種別。
2. exact matter profile、engagement scope、事件固有命令。
3. clinic practice profileと責任弁護士が承認したguide。
4. tenant default。

矛盾又は不明があれば停止し、責任弁護士へrouteする。日本法frameworkがないpractice
areaへ米国法を自動適用しない。

## Module

- [一次資料台帳](source-register.md)
- [clinic、資格、利益相反、守秘](clinic-law-and-supervision.md)
- [依頼者dataと安全](privacy-client-data.md)
- [手続、digitalization、期限](procedure-deadlines.md)
- [legal aid、能力、accessibility、通信](client-access-and-communications.md)
- [currency watch](currency-watch.md)

## Hard boundaries

- 全国一律のstudent-practice licence又は`Certified Legal Intern` statusがあると
  表示しない。
- faculty supervisorと日本の有資格弁護士を同一視しない。
- 弁護士法72条について「無償又は教育目的だから常に適法」としない。
- clinic intake又はmatter recordが受任、代理、法律相談、裁判所提出権限を生むと
  表示しない。ただしdisclaimerだけで実際のconductによるengagement/scope成立可能性を
  否定しない。
- information barrierをconflict clearance又はwaiverと扱わない。
- student participation matrixを法的権限又は弁護士法72条riskの治癒と扱わない。
- 米国のattorney-client privilege、FRCP work product、limitation、service、
  certificate of service、court formを日本へ置換適用しない。
- civil、criminal、administrative、family、labor、immigrationのforumと期限を混同
  しない。
- `criminal | immigration | housing | benefits`はapproved current source cardなしに
  substantive advice、eligibility、deadline、formを生成しない。
- legal holdをFRCP 37(e)又は日本法上の一般的同等制度と扱わない。
- consequential translationはresponsible-lawyer legal reviewとcompetent-language
  reviewの両方を要求する。
- 公式日本語原文、施行日、経過措置、事件固有命令をその会話で再確認する。

## Output status

すべての法律分析、期限、文書は責任弁護士・監督者review用draftである。内部memo、
client-safe draft、tracker、filing draftを分け、AIはsend/post/file/sign/calendar/
accept/decline/settle/closeを実行しない。
