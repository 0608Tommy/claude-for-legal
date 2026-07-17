> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — Public-company disclosure、MNPI、秘密性

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16 JST

## Listed/reporting company preflight

次をsecurities/IR ownerへrouteする。

- material launch、strategic product change
- launch delay/failure、forecast/revenue effect
- cyber incident、safety issue、recall
- regulatory action、licence issue、investigation
- major partnership/vendor dependency
- acquisition/disposition、capital allocation
- selectively shared material information

金商法・開示府令等の[B]、金商法27条の36と重要情報公表府令によるFair
Disclosure Ruleの[B/G]、JPX上場規程等の`[P: exchange-rule]`、JPX guideの[G]を
分ける。EDINETは提出systemでありauthorityではない。companyのdisclosure
committee、insider list、trading blackout、`MNPI` label、IR processは[I]。

閣法57号は2026-07-15に成立したが、2026-07-16時点で公布・法律番号を確認できない。
非財務情報の報告・保証等を[F]として追跡し、current disclosure dutyへ先行適用
しない。

## Review questions

- issuer/listing/reporting status
- materiality under exact facts
- board/committee decision or occurrence
- forecast impact
- disclosure category、timing、responsible owner
- selective disclosure、analyst/customer/partner communication
- 金商法上の重要事実、Fair Disclosure Ruleの重要情報、JPXの会社情報
- insider information、社内MNPI label、access list、need-to-know
- draft preservation、version、translation

Form 8-Kのfour-business-day ruleを日本のdeadlineとして使わない。U.S. issuer
nexusがある場合だけ[X]として並行適用する。

`MNPI`自体を日本法上の統一要件として使わない。日本法の結論は、該当する重要事実、
Fair Disclosure Ruleの重要情報、JPX rule、社内controlをそれぞれ確認して示す。

## Matter and DLP

未公表launch、forecast、incident、regulatory contactはrestricted/MNPIになり得る。
viewer、clean-team、need-to-know、retention、legal hold、SharePoint item-level ACL、
storage/flow DLPを確認する。Cowork prompt DLPがmandatoryならproduction利用を停止
する。

## Japanese confidentiality / privilege

弁護士法23条はlawyerのprofessional secrecyを定めるが、米国のclient-owned
blanket attorney-client privilegeまたはFRCP work productと同一ではない。
document、author、purpose、holder、recipient、procedureを確認する。

JFTCの2020-12-25施行の限定的な取扱いは、不当な取引制限の疑いに関する行政調査で
提出を命じられた一定の物件についての判別・取扱手続であり、一般民事、刑事、行政、
社内文書すべてのprivilegeへ拡張しない。

official source:
https://www.jftc.go.jp/en/policy_enforcement/210413.html

Fair Disclosure Rule sources:

- https://laws.e-gov.go.jp/law/323AC0000000025
- https://laws.e-gov.go.jp/law/429M60000002054
- https://www.fsa.go.jp/common/law/kaiji/20180206-2.pdf

内部分析、board/IR draft、PM action-only draft、public disclosureを別artifactに
する。外部版から内部legal theory、accepted risk、reviewer identity、privilege
assertionを除く。

## Gate

materialityをAIが最終決定せず、securities/IR/legal owner、exact source、current
JPX上場規程・guide/FSA version、decision/occurrence date、distribution listを
記録する。delivery、EDINET/TDnet filing、public announcementをskillが実行したと
表示しない。
