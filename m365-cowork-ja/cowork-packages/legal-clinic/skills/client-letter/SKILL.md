---
name: client-letter
description: >
  予約確認、資料依頼、短いprocedural update等のroutineな依頼者向け文書を、safe-contact、やさしい日本語、language/accessibility、正確な学生role、responsible lawyer reviewに従って作る。plain-language-letters helperのroutine intentを統合し、deadline・scope・法的position・bad news等のsubstantive intentはstatusへrouteする。送信しない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: legal-clinic
  migration-target: direct
  logical-target-id: ja-jp.cowork.legal-clinic.client-letter
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Client letter

canonical label:
`/legal-clinic:client-letter [appointment | doc-request | update]`

`plain-language-letters` helperのroutine branchを本skillへflattenしている。

## Mandatory scope / safe-contact / review gate

1. `references/common/cowork-runtime-contract.md`を読み、exact current user、active
   non-null expiring matter binding、conflict/engagement/scope、authorized ACLを確認する。
2. 別client/matterへsame-session switchしない。
3. intentを`routine | substantive`へ分類する。
   - `routine`: 予約、場所、持参物、受領確認等のpure logistics。
   - `substantive`: deadline、scope、legal position、strategy、bad news、adverse ruling、
     settlement、case closing。`status client`へrouteする。
4. routineでもresponsible lawyerが承認したlocked template、student participation、
   safe-contact、destinationを確認する。substantiveはitem-by-item lawyer review。
5. identity、contact、language、interpreter、health、immigration、criminal、
   child/family/DV dataを必要最小限にする。
6. student sign-offは`法科大学院生（実習生）`等の正確なroleとresponsible lawyerを
   示し、弁護士又は認定代理人と誤認させない。
7. review labelはartifact metadata又はletter外に置き、client copyへ残さない。
8. draft、approval、SharePoint output promotion、send、communication logは別operation。
   本skillはsend/postしない。
9. Cowork内DLPが必須ならconfidential client contentを投入しない。
10. `criminal | immigration | housing | benefits`に関係するsubstantive contentは本skillへ
    押し込まず、approved source cardと`status`/responsible lawyerへrouteする。
11. consequential translationはresponsible-lawyer legal reviewとcompetent-language
    reviewの両方を同じartifact version/hashに要求する。

Japan:
`references/common/ja-jp/client-access-and-communications.md`。

## Pedagogy

practice-area guideの`assist | guide | teach`を適用する。

- `guide`: structureとrequired elementsを示し、studentがdraftする。
- `assist`: review用draftを作り、studentがfacts/languageを検証する。
- `teach`: student draftへfeedbackし、最初から完成文を出さない。

modeにかかわらずlawyer gateとno-sendは変わらない。

## Letter type

### `appointment`

- date/time/timezone
- physical/phone/video location
- participant role
- safe contact/reschedule method
- accessibility/interpreter arrangement
- approved clinic contact

### `doc-request`

- requested documentをplain Japaneseで説明
- purposeを必要な範囲で説明
- safe submission method
- requested dateがlegal deadlineかinternal targetかを区別
- My Number card等の不要なidentifierを送らない注意

### `update`

「受領した」「提出draftを責任弁護士がreview中」「裁判所通知を受けた」等、verified
eventだけを短く示す。filed/sent/deliveredはexact evidenceがある場合だけ。
deadline、legal effect、next stepのadviceが必要なら`status client`へrouteする。

## Draft format

client-safe artifactには:

- 宛名
- 目的を最初の1～2文
- what happened / what is needed / by when
- candidate dateかverified dateか
- client action
- safe contact
- studentの正確なroleとresponsible lawyer/clinic

内部review artifactには別途:

- source item/version
- safe-contact check
- language/interpreter/accessibility
- reviewer、artifact hash/version
- unresolved `[VERIFY]` / `[review]`

内部notesをclient-safe draftへ埋め込まない。

## Plain Japanese

短文、active voice、必要な法律用語の短い説明、明確な日付・actionを使う。
英語のgrade-level数値を日本語品質保証として使わない。権利、期限、scope、advice等を
含むtranslationは、legal reviewとlanguage reviewのどちらか一方だけでは外部利用しない。

## Consequential action

send前に人がexact final version、destination、safe-contact、review approval、
attachments、retention/DLPを再確認する。本skillはOutlook、Teams、SMS、郵便を実行せず、
communication logへ自動記録しない。

## 行わないこと

- legal advice、bad news、scope又はdeadline analysisをroutine templateへ押し込む
- `Certified Legal Intern`又は弁護士statusの表示
- source evidenceなしの「filed」「sent」「delivered」
- internal memo、conflict、privilege評価のclient copyへの流用
- send/post/file/sign/accept/decline/settle/close
