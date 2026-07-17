> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — 個人情報、DPA、data clause

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

## 現行法

個人情報保護法とPPC規則・guidelineをcurrent baselineとする。

- law: https://laws.e-gov.go.jp/law/415AC0000000057
- PPC: https://www.ppc.go.jp/personalinfo/legal/

e-Govで2026-07-16に確認した主要条文:

- 第17条: 利用目的の特定
- 第18条: 利用目的による制限
- 第20条: 適正な取得
- 第23条: 安全管理措置
- 第25条: 委託先の監督
- 第26条: 漏えい等の報告等
- 第27条: 第三者提供の制限
- 第28条: 外国にある第三者への提供の制限

条文番号だけで結論を出さず、個人情報、個人data、保有個人data、個人関連情報、要配慮個人情報、仮名・匿名加工情報等の分類を確認する。

## 契約review

| 項目 | 確認 |
|---|---|
| role | 自社・相手方が取得主体、委託元/委託先、第三者、共同利用者のどれか |
| purpose | 契約目的、service improvement、analytics、AI training、marketing |
| instructions | documented instruction、目的外利用、human access |
| security | access、encryption、logging、incident、evidence |
| subprocessor | list、change、flow-down、objection |
| foreign | country、storage/processing、情報提供、継続的措置 |
| incident | definition、notice timing、PPC/本人対応、cooperation |
| rights | access/correction/stop等へのsupport |
| retention | term、termination、backup、deletion certificate |
| audit | report、certification、questionnaire、onsite/remote right |

DPA、documented instructions、subprocessor list/change objection、audit right、
deletion certificate、固定時間のvendor noticeはcontract risk controlであり、
APPIが一律に要求するGDPR型条項ではない。binding baselineは第25条の必要かつ
適切な委託先監督とPPC guidelineであり、各controlを
`binding law | official guidance | playbook`に分類する。

DPAがあることだけでmain agreementのdata-use grantを無効と扱わない。main terms、DPA、privacy policy、AI addendum、admin setting、subprocessor termsのpriorityを確認する。

## 委託と第三者提供

「委託」とlabelされているだけで法的分類を確定しない。受託者自身の目的利用、service improvement、cross-customer analytics、AI training、広告利用、independent controlがあれば第三者提供その他の整理が必要となり得る。

上流model/cloud providerへのflow-down、audit evidence、incident cooperationを確認する。

## 2026 amendment

2026-04-07法案提出、2026-05-26衆議院可決、2026-07-10参議院可決・成立、
2026-07-14内閣が公布を決定。2026-07-16時点で参議院の公布年月日・法律番号
欄は空欄であり、公布そのもの、法律番号、施行政令は未確認である。

主要規定は公布日から2年以内の政令指定日に施行予定である。したがって、
統計等、16歳未満、特定生体個人情報、連絡可能個人関連情報、課徴金等の
改正内容を現行permissionまたはobligationとして適用しない。成果物では
`成立・公布決定済み／公布・施行確認待ち [verify]`とする。

## Gate

data category、purpose、vendor learning、processing country、subprocessor、retention、incident termのいずれかが不明なら「個人情報なし」「DPAでcover」と仮定しない。原資料を指定し、署名推奨を保留する。
