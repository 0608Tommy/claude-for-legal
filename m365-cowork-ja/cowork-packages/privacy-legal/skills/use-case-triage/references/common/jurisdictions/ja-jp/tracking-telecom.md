> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本 — Cookie、外部送信、通信の秘密

**状態:** DRAFT — qualified Japanese counsel review pending

## 一律ruleを作らない

日本で全Cookieに一律opt-in consentが必要とも、Cookieなら規制外とも書かない。少なくとも次を別々に確認する。

1. APPI上の個人情報・個人データ
2. `個人関連情報`と提供先での個人データ化
3. 電気通信事業法の外部送信規律
4. 電気通信事業者に関係する通信の秘密・sector guideline
5. 表示、consent representation、consumer protection
6. GDPR/ePrivacy、US state等の外国法

## APPI

Cookie ID、広告ID、閲覧履歴、device情報が個人を識別できる、または他情報と容易照合できる場合のcategoryを確認する。提供先が個人データとして取得することが想定される`個人関連情報`の提供では、本人同意取得の確認等を検討する。

first party / third partyというbrowser用語だけでAPPI結論を出さず、誰が受け取り、何と結合し、何に使うかを見る。

- PPC FAQ Q8-1: https://www.ppc.go.jp/all_faq_index/faq1-q8-1/
- PPC FAQ Q8-3: https://www.ppc.go.jp/all_faq_index/faq1-q8-3/

## 外部送信規律

電気通信事業法27条の12は、原則として送信情報、送信先等を通知し、または
利用者が容易に知り得る状態に置くことを要求する。例外は、役務提供に必要な
情報、提供者が送信した識別符号を同じ提供者へ返送する場合、利用者が同意
した情報、法定要件を満たすopt-out措置の対象情報である。単なるgeneric
`公表`を独立routeとして扱わない。

外部送信規律を導入した令和4年法律第70号は2023-06-16施行。2026-07-16
時点の電気通信事業法現行版は2026-05-27、施行規則（昭和60年郵政省令
第25号）は2026-06-30現行版を確認する。

公式:

- https://www.soumu.go.jp/main_sosiki/joho_tsusin/d_syohi/gaibusoushin_kiritsu.html
- https://www.soumu.go.jp/main_sosiki/joho_tsusin/d_syohi/gaibusoushin_kiritsu_00001.html
- https://www.soumu.go.jp/main_sosiki/joho_tsusin/d_syohi/gaibusoushin_kiritsu_00002.html

すべてのwebsite/appが同じ範囲で対象とは限らない。service category、
電気通信事業該当性、送信program、必要情報、identifier、同意、opt-out等の
要件を確認する。

## 通信の秘密

電気通信事業法:
https://laws.e-gov.go.jp/law/359AC0000000086

通信内容、通信当事者、日時、場所等が通信の秘密の対象となるか、service providerの立場、同意、正当業務行為等を日本のtelecom専門家と確認する。一般APPI同意が通信の秘密に関する有効同意を常に満たすとは仮定しない。

## Policy / CMP diff

policy-monitorでは次を比較する。

- privacy policyのdata category / purpose / recipient
- CMP category、default、consent log
- tag manager / SDK / pixelの実際の送信
- App Store / Google Data Safety
- opt-out停止範囲
- cross-border recipient
- retention

bannerが表示されるだけで裏側のtagが停止していると仮定しない。technical inventoryとnetwork evidenceを確認する。

## Output

法律上のminimum、official guidance、internal preferenceを分ける。`consent required`、`notice sufficient`、`out of scope`のいずれも適用事実とcurrent sourceなしに断定しない。
