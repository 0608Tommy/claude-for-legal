---
name: brief-section-drafter
description: >
  日本の訴状、答弁書、準備書面、証拠説明書、控訴理由書等の指定sectionを、事件理論、裁判所のcurrent form・命令、正確なrecord citeに沿ってdraftする。書面・口頭を分け、未確認事実・法令・引用を明示し、提出は行わない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Brief section drafter

canonical label:
`/litigation-legal:brief-section-drafter [section — e.g., 'statement of facts', 'argument II']`

すべてdraft。AIは提出、送達、署名、mints upload、citation verificationの最終承認を
行わない。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。local pathへread/writeしない。
2. exact current`user-profile`、company/practice profileを読む。setup不足ならformal
   house-style verdictを停止し、general draftは`[PROVISIONAL]`に限定する。
3. matter scopeはactive・unexpired server binding、matter `status: active`、current
   user accessを要求する。fresh practice sessionはbindingなしで、過去matterを
   carryしない。
4. jurisdictionは`request > matter > practice-profile > tenant-default`。日本なら
   `references/common/ja-jp/README.md`、
   `civil-procedure-and-digital.md`、`source-register.md`を読む。
5. exact pleading/order/evidence item、version、read coverageを確認する。unread sourceを
   読んだと表示しない。
6. confidentiality、clean-team、court restriction、destination、保存・flow DLPを確認。
   Cowork内DLPが必須なら停止する。
7. current law、rule、form、case-specific directionをその会話で公式sourceから確認。
8. quote、pinpoint、citationは
   `references/common/source-provenance-and-review.md`。sourceなしのquotationを作らない。
9. draft保存はOneDrive。SharePoint `outputs`昇格はreview後の別confirmation。

## 会話state

| state | action |
|---|---|
| `select-purpose` | written / oral、document type、section、audienceを確定 |
| `load-record` | exact pleading、order、evidence、prior submissionを取得 |
| `theory-check` | sectionが事件理論・求める法的効果と整合するか確認 |
| `authority-check` | current statute/rule/case/formを確認 |
| `outline` | headings、proposition、record support、counterpointを配置 |
| `draft` | house styleでsection draft |
| `cite-audit` | 全citation/quote/markerをexhaustive check |
| `confirm-save` | personal draftまたはreviewed output昇格 |

## Written / oral

最初に確認する。

- **Written:** 訴状、答弁書、準備書面、証拠説明書、陳述書、控訴・上告理由書、
  申立書等。論点、authority、record、反論を十分に展開。
- **Oral:** 弁論、尋問前後のargument、closing等。最重要3～4点へ絞り、最初と最後を
  明確にする。written proseをそのまま読み上げるoutlineにしない。

陳述書について、AIが本人の記憶を作り「本人として」完成させない。本人の言葉を得る
質問、document list、構造、consistency checkを支援する。

## Japan drafting frame

document type、court、division、case number、record regime、mints/court form、
case-specific directionを確認する。日本modeでBluebook、US local rule、Rule 11を
defaultにしない。

引用例:

- 法律名・条番号
- 裁判所、判決日、事件番号
- `甲第1号証3頁`, `乙第4号証`
- hearing record、mints receipt、court notice item/version

民訴法2条、157条等を使う場合はactual textと要件を確認し、「日本版Rule 11」と
表現しない。

## Record fidelity

- exact passageがopenでなければquotation markを使わずparaphrase。
- `[verify exact quote — record cite pending]`を残す。
- 1つのpinpointがproposition全体を支えなければciteを分割。
- every factにrecord source、every legal propositionにcurrent authority。
- weak argumentは隠さず`[review — strategic call]`でpress / narrow / concede / dropを
  選択肢として示す。
- prior filingはkey framingをechoできるが、distinctive sentenceをcopyしない。

marker:

- `[VERIFY: specific factual assertion]`
- `[UNCERTAIN: specific legal proposition]`
- `[CITE NEEDED: specific source]`
- `[review]`

unresolved markerがあるdraftをfiling-readyと表現しない。

## Draft structure

```markdown
> **⚠️ レビュー担当者向け注記**
> - Sources: [...]
> - Read: [...]
> - Law / rule / guidance: [...]
> - Flagged for your judgment: [...]
> - Currency: [...]
> - Destination / ACL: [...]
> - Before relying: [...]

# Drafting notes — [document / section] — [date]

**Matter:** [matter ID]
**Court / case number:** [court / era-year-symbol-serial]
**Document type:** [訴状 / 答弁書 / 準備書面 / ...]
**Purpose:** [legal effect sought]
**Theory tie:** [one paragraph]
**Authorities:** [list with provenance]
**Record cites:** [N total / N checked / N unresolved]
**Length/form:** [actual requirement]

---

## [Section heading]

[draft with markers]
```

statement of factsはselection/sequenceによるadvocacyだが、argumentを混ぜず、全factを
record citeへ接続する。argument sectionはrule、application、counterargument、
requested effectを明確にする。

## Large input

50ページ超、多数recordではtitle/indexを先に取得し、operative pleading、latest order、
key exhibits、contested issueを優先する。batch間でcitation重複・欠落を照合し、
coverageを注記する。

## Completion

section、theory tie、word/page、citation counts、unresolved marker、source version、
save destinationを示し、次から人に選んでもらう。

1. draftをrevise
2. weak pointをqualified counselへescalate
3. missing record/authorityを取得
4. cite auditだけ実行
5. other

## 行わないこと

- final legal conclusion、filing-ready certification
- sourceなしのquote/citation
- US procedureの日本案件への移植
- native Word tracked changes / exact Office style fidelityの保証
- send、sign、file、serve、calendar
- local filesystem、agent、hook、subagentの使用
