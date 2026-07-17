> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# `ja-JP` 日本商事契約module

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

日本に関係する商事契約reviewの追加layerであり、法的助言または承認済み見解ではない。

## 選択

`request > matter > practice-profile > tenant-default`

1. 利用者が明示した対象法域を確認する。
2. matterのgoverning law、当事者所在地、履行地、customer/worker/data subject所在地を確認する。
3. practice profile、tenant defaultを下位fallbackとして使う。
4. 値が複数、矛盾、空欄、対象者所在地と不整合なら停止する。

`Japan`, `日本`, `JP`, `ja-JP`を正規化しても、準拠法と強行適用法を同一視しない。越境案件では日本、契約準拠法、履行地、data/consumer法域を別々に示す。

## 読み分け

| 論点 | file |
|---|---|
| 契約成立、定型約款、債務不履行、解除、電子署名、準拠法 | `contract-core.md` |
| 個人情報、DPA、委託、第三者提供、国外 | `privacy-data.md` |
| 取適法、フリーランス法、委託条件、支払、更新・解除 | `entrusted-transactions.md` |
| 消費者契約、通信販売、最終確認画面、電子申込み | `consumer-electronic.md` |
| 独占禁止、優越的地位、知財・data、営業秘密 | `competition-ip.md` |
| law/guidance、URL、確認日 | `source-register.md` |

## 共通原則

1. binding law、official guidance、internal playbookを分ける。
2. B2B契約へconsumer ruleを自動適用せず、consumer transactionへB2B market practiceだけを適用しない。
3. `governing law: Japan`だけで、取適法、フリーランス法、個人情報保護法等の適用を決めない。各statuteのscopeを確認する。
4. 電子署名法第3条の推定要件と、契約成立・証拠力・権限確認を分ける。
5. 日本法上の秘密保持・文書提出を米国`ATTORNEY WORK PRODUCT`と同一視しない。
6. 2026年改正・新guidanceは公布、施行、経過措置を確認し、未施行ruleを現行義務として適用しない。
7. workflowまたはbusiness approvalは指定approverが行い得るが、日本法上の
   結論、本moduleの承認、`pending` statusの変更は日本法有資格者reviewを
   要し、指定approverで代替しない。
