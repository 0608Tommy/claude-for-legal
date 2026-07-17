> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — APPI core

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

## 適用と用語

現行法は個人情報の保護に関する法律（平成15年法律第57号）。2026-07-16
時点のe-Gov現行版は令和8年法律第46号による2026-06-24施行版である。
施行令は平成15年政令第507号（現行版2026-05-21施行）、施行規則は平成28年
個人情報保護委員会規則第3号（令和8年PPC規則第2号による2026-06-14施行版）
を確認する。

- 法律: https://laws.e-gov.go.jp/law/415AC0000000057
- 施行令: https://laws.e-gov.go.jp/law/415CO0000000507
- 施行規則: https://laws.e-gov.go.jp/law/428M60020000003
- PPC通則guideline: https://www.ppc.go.jp/personalinfo/legal/guidelines_tsusoku/

- `個人情報`
- `個人データ`
- `保有個人データ`
- `要配慮個人情報`
- `個人識別符号`
- `仮名加工情報`
- `匿名加工情報`
- `個人関連情報`
- `個人情報取扱事業者`

同じrecordでも段階によりcategoryが変わり得る。公開情報、business contact、cookie ID、pseudonymized dataを自動的に法外としない。

## 基本check

1. 利用目的を具体的に特定したか。
2. 目的の通知・公表・明示が必要か。
3. 目的変更は合理的関連性の範囲か。
4. 不適正利用・不正取得がないか。
5. 要配慮個人情報の取得同意または例外はあるか。
6. data accuracy、利用不要後の消去努力、安全管理、従業者監督、委託先監督を満たすか。
7. 漏えい等報告・本人通知のtriggerがあるか。
8. 第三者提供、委託、事業承継、共同利用を正しく区分したか。
9. 外国にある第三者、個人関連情報、第三者提供record義務を確認したか。
10. 保有個人データの公表事項と本人請求手続があるか。

## `controller` / `processor`のfalse equivalence

APPIはGDPRと同じ法定`controller` / `processor` taxonomyを採用していない。

- APPI上の`個人情報取扱事業者`がGDPR controllerと常に同じではない。
- APPI Article 27(5)(i)の`委託`は一定範囲で第三者に該当しない扱いだが、Article 25の必要かつ適切な監督が必要。
- 受託者が独自目的で使う、範囲外再提供をする、共同で目的を決める場合、単純な`processor`または`委託`labelでは足りない。
- CCPA/CPRAの`service provider` / `contractor`も別test。

DPAでは法域ごとにrole tableを作る。

| 法域 | role / route | 事実 |
|---|---|---|
| Japan | APPI事業者、委託、第三者提供、共同利用 | purpose、指示、独自利用、再提供 |
| EU/UK | controller、joint controller、processor | purpose / means、Article 28 |
| California | business、service provider、contractor、third party | statutory contract restrictions |

## 委託と共同利用

委託なら、委託業務の範囲、取扱data、目的、security、再委託、incident、audit/assurance、return/deletion、監督方法を確認する。契約締結だけで監督完了としない。

共同利用なら、共同利用者の範囲、data項目、利用目的、管理責任者等の法定公表事項と実態を確認する。marketing partnershipを安易に共同利用へ変換しない。

## 個人関連情報

Cookie ID、広告identifier、閲覧履歴等が`個人関連情報`に当たり、提供先が個人データとして取得することが想定される場合、APPIの確認・同意関連ruleを検討する。提供元・提供先のどちらが何を知り、どのdataと結合するかをflowで確認する。

## 域外適用・public sector

日本の本人に対する商品・service提供に関連して国外事業者が個人情報を取得する場合等の域外適用を確認する。行政機関等には民間事業者と異なる章・guidelineが関係するため、民間workflowをそのまま使わない。

## 第221回国会・閣法54号（三年ごと見直し改正）

成立済みだが2026-07-16時点で公布日・法律番号未確認、未施行。統計等、16歳未満、特定生体個人情報、連絡可能個人関連情報、課徴金等を現行ruleに混ぜない。
