> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 従業員・応募者、子ども、生体情報

**状態:** DRAFT — qualified Japanese counsel review pending

## 従業員・応募者

従業員・応募者dataにもAPPIを適用する。雇用関係があることだけで自由利用・包括同意が認められるとは扱わない。

確認:

- 利用目的と職務上の必要性
- health、disability、思想信条等の要配慮性
- 採用時に適性・能力と無関係な情報を取得していないか
- monitoringの必要性、比例性、透明性、より侵襲性の低い代替
- performance、discipline、terminationへの利用
- vendor / AI scoring、bias、訂正・human review
- retention、退職・不採用後の削除
- works rules、labor agreement、consultation、sector rule

厚労省:

- https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/koyou/newpage_56780.html
- https://kouseisaiyou.mhlw.go.jp/consider.html
- https://laws.e-gov.go.jp/law/322AC0000000141
- https://www.mhlw.go.jp/web/t_doc?dataId=00005680&dataType=0&pageNo=1
- https://www.mhlw.go.jp/content/001170632.pdf

職業安定法（昭和22年法律第141号）5条の5は求人者・募集者等にも適用される。
平成11年労働省告示第141号の指針は同法48条に基づく指針である。一方、
公正採用選考web資料全体は独立した差別禁止法ではない。従業員健康情報は
2023-10-27付留意事項も確認する。

## 子ども — 現行

現行APPIにGDPR Article 8やCOPPAと同じ一般年齢thresholdを自動挿入しない。PPC FAQは、同意の結果を判断できる能力をdata・serviceの性質から確認し、一般に12～15歳以下では法定代理人同意が必要となる場面を示す。

https://www.ppc.go.jp/all_faq_index/faq1-q1-62/

child-friendly notice、data minimization、parent/guardian authority、本人利益とのconflict、age assurance、marketing、location、school data、retentionを確認する。COPPA、FERPA、state law等が別途適用される場合は並行適用する。

## 子ども — 2026改正

成立した改正には16歳未満の法定代理人への通知等が含まれるが、2026-07-16時点で公布日・法律番号・施行を確認できない。現行の一律`under 16` ruleとして使わない。

## 生体情報 — 現行

身体特徴そのものが常に個人識別符号となるのではなく、施行令1条1号・
施行規則2条の要件を満たす電子計算機用の変換符号が該当する。raw画像等は
別途、識別可能性により個人情報となり得る。生体情報それ自体が常に
`要配慮個人情報`とは限らず、健康・障害等を推定・含有する場合は別途
要配慮性を確認する。

- 施行令: https://laws.e-gov.go.jp/law/415CO0000000507
- 施行規則: https://laws.e-gov.go.jp/law/428M60020000003
- PPC camera resources: https://www.ppc.go.jp/news/camera_related/
- 顔識別機能付きcamera guide: https://www.ppc.go.jp/files/pdf/kaoshikibetsu_camera_system.pdf

確認:

- raw image / template / score / inferred attribute
- identification / verification / categorization
- 利用目的、必要性、代替
- spoofing、false match、差別・exclusion
- 保存、暗号化、revocation可能性
- vendor独自利用、model training
- 第三者提供、越境
- 本人説明、訂正・停止route

## 生体情報 — 2026改正

改正には`特定生体個人情報`について違法取扱い等がなくても利用停止等を請求可能とする内容が含まれるが未施行。current lawとfuture readinessを別sectionにする。

## Triage floor

children、biometric identification、emotion/personality inference、employee/applicant scoring、continuous monitoringは最低でもPIA REQUIREDまたは`[review]`。法定DPIAとinternal PIAを区別する。
