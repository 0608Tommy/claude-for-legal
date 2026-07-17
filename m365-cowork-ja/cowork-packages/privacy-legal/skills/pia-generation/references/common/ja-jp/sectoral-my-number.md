> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — My Numberとsectoral overlay

**状態:** DRAFT — qualified Japanese counsel review pending

## My Number

番号法とPPC事業者編guidelineをAPPIと別に確認する。

- 利用目的は法令上認められた事務へ限定
- 特定個人情報の提供・収集・保管制限
- access、取扱担当者、区域、log、安全管理
- 委託・再委託
- 保存期間後の削除
- 漏えい等報告

公式:

- https://laws.e-gov.go.jp/law/425AC0000000027
- https://www.ppc.go.jp/legal/policy/my_number_guideline_jigyosha/

2026-07-16時点で番号法現行版は2026-06-14施行、事業者guidelineは2025-06
一部改正。漏えい等報告ruleは2025-10-01現行版を確認する。

本人確認のためにMy Number cardを使っても、裏面の個人番号を不要に取得・copyしない。

## 特定個人情報保護評価

一般民間PIAと同一ではない。国の行政機関、地方公共団体、独立行政法人等と、情報提供networkを使う一部対象者の固有制度。一般企業が給与・税事務で番号を扱うだけで必ず同評価対象になるとは書かない。

https://www.ppc.go.jp/legal/assessment/

PIA規則は2025-04-01現行版、指針は2025-07-15改正、解説は2025-10-24
改正を確認する。

## 金融

金融分野guideline、実務指針、監督法、AML/CFT、信用情報、outsourcing、cyber incident、regulator noticeを確認する。

- https://www.ppc.go.jp/personalinfo/legal/kinyubunya_GL/
- https://www.ppc.go.jp/personalinfo/legal/guidelines/

- 金融guideline（2024-03-12、2024-04-01適用）:
  https://www.ppc.go.jp/files/pdf/240312_kinyubunya_GL.pdf
- 金融Q&A（2025-10-01）:
  https://www.ppc.go.jp/files/pdf/251001_kinyukikan_QA.pdf

GLBA等の外国sector lawと日本の金融ruleを混ぜない。

## 医療・介護

PPC/MHLWの医療・介護関係事業者guidance、医療法、守秘、研究、次世代医療基盤法、倫理指針等を役割・用途から確認する。APPIの要配慮個人情報だけで分析を終えない。

source入口:
https://www.ppc.go.jp/personalinfo/legal/guidelines/

- 医療・介護guidance / Q&A（2026-04-01）:
  https://www.ppc.go.jp/files/pdf/260401_iryoukaigo_guidance.pdf
  https://www.ppc.go.jp/files/pdf/260401_iryoukaigo_guidance_QA.pdf

## 電気通信・放送・郵便

PPC/MICの分野guideline、電気通信事業法、通信の秘密、外部送信規律、事故報告等を確認する。

- https://www.ppc.go.jp/personalinfo/legal/guidelines/
- https://laws.e-gov.go.jp/law/359AC0000000086

- 電気通信guideline（2025-10-01）:
  https://www.ppc.go.jp/files/pdf/251001_telecom_GL.pdf
- 電気通信解説（2026-06-14）:
  https://www.ppc.go.jp/files/pdf/260614_telecom_GLs_description.pdf
- 放送受信者guideline / 解説:
  https://www.ppc.go.jp/files/pdf/251001_broadcast_recipient_GL.pdf
  https://www.ppc.go.jp/files/pdf/260614_broadcast_recipient_GLs_description.pdf
- 郵便guideline / 解説:
  https://www.ppc.go.jp/files/pdf/251001_postal_survice_GL.pdf
  https://www.ppc.go.jp/files/pdf/260614_postal_survice_GLs_description.pdf

## 教育・子ども

学校・教育serviceでは、APPIの民間/公的部門区分、自治体規程、学校契約、文科省security guidance、外国法FERPA/COPPA等を確認する。日本にCOPPAと同じ単一法があるとは表現しない。

## Credit / advertising / data broker

割賦販売、貸金、信用情報、広告、位置情報、data broker、platform等は適用業法・guidanceを個別に確認する。`personal data`であることだけでsector dutyを見落とさず、sector exemptionがあることだけでAPPIや他法が消えると仮定しない。

## Public sector

行政機関等にはAPPIの行政機関等の規律、local authority、information disclosure、公文書、特定個人情報保護評価、government cloud/security rulesが関係する。民間用DPA/DSAR templateをそのまま適用しない。

## Gate

sectorが不明、license status不明、複数regulator、sensitive data、statutory retention、reporting conflictがある場合、該当分野の日本法有資格者へrouteする。
