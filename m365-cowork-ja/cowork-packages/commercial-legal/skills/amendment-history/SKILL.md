---
name: amendment-history
description: >
  基本契約と全変更契約を時系列で読み、変更全体のsummaryまたは指定条項のprovision traceを作る。現在の支配文言、変更元、section reference、矛盾、未読資料を示し、複数versionの契約がある場合に使用する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: commercial-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# 変更契約履歴

旧来の参照labelは `/commercial-legal:amendment-history [file(s)] --provision <clause name>`。Coworkではfile pathやflagを実行せず、権限あるSharePoint itemと会話状態を指定する。

## 必須gate

1. **保存契約:** `references/common/cowork-runtime-contract.md` を必ず読む。ローカルfile、cache、home directoryへread/writeしない。
2. **Setup:** SharePoint `profiles`の会社・実務profileと、複合keyが一致する現在利用者の`user-profile`を読む。未設定でも純粋なhistory extractionはできるが、privilege、destination、保存先、matterが不明なら保存・共有を停止する。
3. **Matter:** server-side session–matter bindingを確認する。別matterの契約を候補にせず、複数候補、権限不足、binding矛盾ならfail closed。
4. **Jurisdiction:** `request > matter > practice-profile > tenant-default`で解決する。日本が含まれる場合は`references/common/jurisdictions/ja-jp/README.md`と`references/common/jurisdictions/ja-jp/contract-core.md`を読む。ただし本skillは原則historyを整理し、法的controlを断定しない。
5. **Source:** base agreement、全amendment、addendum、assignment、order form、effective dateをexact item/versionで取得する。読めない資料を無視しない。
6. **Confidentiality:** authorized viewers、NDA、clean-team、retention、legal hold、保存境界DLPを確認する。
7. **Human review:** conflicting amendment、priority、novation、assignment、waiver、現在の支配条項は法的解釈になり得る。AIは確定せず`[review]`へ回す。
8. **Irreversible/write:** 初稿はOneDrive。新規draftはcanonical key、
   `recordId`、unique`idempotencyKey`で条件付きcreateする。既存draftの更新
   またはSharePoint `outputs`への昇格はexact`itemId`とlatest`eTag`を要求し、
   人の確認後に行う。外部送信、契約変更、signatureを行わない。

情報源tagとreviewer noteは
`references/common/source-provenance-and-review.md`を使う。

## 会話state

| state | user intent | transition |
|---|---|---|
| `collect-documents` | baseとamendmentsを指定 | `order` |
| `order` | chronological chainを確定 | `choose-mode` |
| `summary` | 全変更を時系列・net current stateで整理 | `review-output` |
| `provision-trace` | 指定条項だけを原文付きで追跡 | `review-output` |
| `review-output` | coverage、watch items、保存先を確認 | `draft` / `promote` |

`--provision <clause name>`は`provision-trace`へのreference intentとして認識する。条項名がなければ`summary`、明確な条項名があれば`provision-trace`へ進む。曖昧な場合だけ候補を示して選択してもらう。

## Document chain

chronologyは次の順で根拠を使う。

1. execution metadata
2. document header / recitalのdate
3. amendment number・title
4. 「[date]のagreementをamendする」というcross-reference

順序を推測した場合、推測したitemだけを明示する。party name、entity、assignment、effective dateが一致しない場合はwatch item。

50page超または多数文書ではdefinitions、amendment operation、changed clauses、priority、term、termination、liability、indemnity、IP、data、confidentiality、governing lawを優先し、未読範囲を記録する。

## Summary mode

各amendmentについて:

- document type、execution/effective date
- purpose（recital等から明示できる場合だけ）
- added / deleted / replaced provision
- before → afterのplain-language effect
- exact section reference

最後に`Net current state` tableとwatch itemsを作る。詳細形式は`references/amendment-workflow.md`。

## Provision trace

触れられていないamendmentは表示しない。

- original exact quote
- each changed versionの`Was` / `Now`
- practical effect
- current candidate languageとsource item/version
- conflict、section renumbering、cap carveout等

未変更なら「base agreementのoriginal languageが変更されていない」とし、「法的に必ず支配する」とは書かない。

## Output

成果物直前にreviewer noteを1block置き、read coverage、chronology confidence、missing documents、destinationを示す。internal markingはmatter・法域に合わせる。

「現在の支配条項」は、文書上のlatest candidateとして示す。conflictがあれば:

> amendment chain上は[文言]がlatest candidateです。ただし[conflict/priority issue]があるため、法的controlは有資格者確認が必要です `[review]`。

## 完了

別条項trace、full`review`、`stakeholder-summary`、追加資料取得から選んでもらう。旧来labelは`/commercial-legal:review`、`/commercial-legal:stakeholder-summary`だが、Coworkでは同じ会話で開始できる。

## 行わないこと

- conflict時の支配条項を最終判断する
- new amendmentをdraft・executeする
- playbook comparisonを暗黙に行う
- native Word tracked changesを生成したと主張する
- external send、signature、state updateを確認なしに行う
