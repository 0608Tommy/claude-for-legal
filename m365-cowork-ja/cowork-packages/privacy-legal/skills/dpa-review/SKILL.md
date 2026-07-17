---
name: dpa-review
description: >
  Data Processing Agreementをcontroller側・processor側の方向、実務playbook、現行privacy law、sectoral rule、越境routeに照らしてreviewする。term別gap、最小granularityの修正文案、policy整合性、fallback、named approverをdraftする。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: privacy-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# DPA review

旧来の参照labelは `/privacy-legal:dpa-review [file | Drive link | paste text]`。

すべてのmemo、redline、counterparty messageはdraftであり、人がreviewして送る。AIは署名、countersign、送信、承認を行わない。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md`を読む。local path、home directory、cacheへread/writeしない。
2. **Setup/user:** exact company/practice profileと、`tenantId + practiceId + userObjectId`が一致する`user-profile`を読む。DPA playbookが未設定・未reviewならformal playbook verdictを停止し、`cold-start-interview`へ案内する。
3. **Matter:** workspaceが有効でmatter scopeを選ぶ場合はserver-side bindingと
   matter `status: active`、client、counterparty、overrideを確認する。
   archived matterまたはrevoked bindingでは実質reviewを拒否する。workspaceが
   無効、またはfresh sessionでpractice-levelを明示した場合は
   `scopeType: practice`を許可し、過去matter contextをcarryしない。
4. **Direction:** `we are processor | we are controller | other/mixed`を事実から確定する。曖昧なら質問する。誤るとrecommendationが逆転する。
5. **Jurisdiction:** `request > matter > practice-profile > tenant-default`。party、data subjects、processing、storage、remote access、governing lawを確認する。
6. **Source:** exact DPA item/version、MSA、security annex、SCC/transfer annex、subprocessor list、incorporated URLを読む。partial readをfull reviewと書かない。
7. **Current law:** deadline、transfer mechanism、adequacy、sectoral rule、2026年改正statusをcurrent primary sourceで確認する。authorityを創作しない。
8. **Confidentiality/destination:** internal memoとexternal redlineを分け、閲覧者、NDA、privilege、retention、保存・flow DLPを確認する。
9. **Human/irreversible:** risk acceptance、fallback外position、署名、redline送付は人の判断。draft作成同意をsend同意に拡張しない。
10. **Write:** create/updateを分ける。updateはexact`itemId`、latest`eTag`、unique`idempotencyKey`と別confirmationが必要。

情報源、reviewer note、severity、non-lawyer modeは
`references/common/source-provenance-and-review.md`。

## Setup incomplete

正式playbook比較は停止する。利用者が明示的にgeneral issue spottingを求めた場合だけ、`[PROVISIONAL — no configured DPA playbook]`のresearch notesを作れる。

- signature-ready、acceptable、GREENを出さない
- generic market positionをteam standardと書かない
- findingごとに`[PROVISIONAL]`
- 保存はpersonal draftのみ

## 会話state machine

| state | action |
|---|---|
| `collect-source` | exact DPAと関連文書を取得 |
| `determine-direction` | processor / controller / mixedを確認 |
| `resolve-scope` | matter、法域、data、sector、value/criticality |
| `prior-context` | prior triage、PIA、DPA reviewを同scopeで確認 |
| `sector-check` | finance、health、education、children、telecom、My Number等 |
| `term-review` | core termsをplaybook・binding lawと比較 |
| `policy-check` | privacy policy / notice / PIAとの整合 |
| `transfer-check` | corridorごとのrouteとcurrent mechanism |
| `draft-redlines` | 最小granularityの修正文案 |
| `escalation` | fallbackとnamed approver |
| `confirm-save` | personal draftまたはreviewed output昇格 |

## Directionと法域用語

GDPRの`controller` / `processor`、Californiaの`business` / `service provider` / `contractor`、日本APPIの`個人情報取扱事業者` / `委託`を同一視しない。

日本が関係する場合は
`references/common/ja-jp/cross-border-dpa.md`と
`references/common/ja-jp/appi-core.md`を読む。

contract labelより次を優先する。

- 誰がpurposeとessential meansを決めるか
- documented instructionsの範囲
- vendorの独自利用、service improvement、training
- 再提供・再委託
- 法令上独自に負う義務

## Prior context

同じscopeの`use-case-triage`、`pia-generation`、prior DPA reviewを読む。上流severityはfloor。下げる場合は新事実と理由を明記する。別matterのprecedentを既定で読まない。

## Term review

`references/clause-workflow.md`を使い、少なくとも次を確認する。

- roles / instructions / purpose
- data・subjects・duration
- security annex
- subprocessor
- incident / breach
- audit / assurance
- rights・regulator assistance
- international transfer
- return / deletion / backup
- independent use / AI training
- liability / MSA conflict

playbook standard、fallback、neverとbinding-law floorを分ける。playbook deviationを違法と書かない。

## Sector overlay

dataがNPI、PHI、education record、children data、communications、My Number、biometric等を含むか先に確認する。state-law exemptionは別sector lawが消えることを意味しない。日本は
`references/common/ja-jp/sectoral-my-number.md`。

## Transfer

origin/destinationごとに、applicable regime、adequacy、consent、SCC/IDTA、APPI Article 28、Supplementary Rules、TIA、onward transferを確認する。mechanism欠落が違法となる場合は🔴候補だが、current sourceと事実を確認する。

## Redline

最小editを優先する。

1. word
2. phrase
3. subclause
4. sentence
5. whole clause

wholesale replacementが必要なら理由をtransmittal draftへ書く。Word native tracked changesを生成・適用したと主張せず、削除・挿入・置換後文案を示す。

## Output

`references/dpa-output.md`を使う。

- directionと法域
- bottom line
- issue count
- term-by-term deviation
- policy consistency
- consolidated draft redlines
- fallback / escalation
- read coverageとunread attachments

counterparty向け文案は内部memoと別版にし、human send approvalを明記する。

## Large input

50ページ超または多数annexでは、titleとattachment一覧を先に取得し、roles、definitions、instructions、security、incident、subprocessor、transfer、deletion、liabilityを優先する。unreadを`Read:`へ記録し、batch間の重複・欠落を照合する。

## Non-lawyer signing gate

Non-lawyerには、counterparty、direction、deviations、resolved/open fallback、transfer、sectoral issue、3つの質問を1-page briefにする。attorney reviewなしにsign/countersignへ進まない。AIはroleにかかわらず署名を実行しない。

## 完了

1. draft redline
2. named approverへのescalation draft
3. missing facts
4. watch/track
5. other

から人に選んでもらう。自動送信しない。
