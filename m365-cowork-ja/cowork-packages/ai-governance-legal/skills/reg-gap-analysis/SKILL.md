---
name: reg-gap-analysis
description: >
  新しいAI法令、規則、ガイダンスを現在のAIガバナンスと比較する。適用範囲、役割、施行時期、要件を一次資料から確認し、gap、優先順位、owner、期限、受容リスクを含む是正計画を作成する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ai-governance-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# 規制ギャップ分析

旧来の参照ラベルは `/ai-governance-legal:reg-gap-analysis`。法令名、公式URL、添付資料、または規制変更の説明を会話で指定する。

## 目的

新しい規制の全文を要約するのではなく、現在のuse case registry、AI policy commitments、vendor positions、AIA practiceとの**差分**を出し、何をいつまでに直すかを示す。適用外なら理由を1行で示して終了する。

## 必須ゲート

1. **セットアップ:** SharePoint `profiles` のregulatory footprint、registry、policy、vendor governance、AIA house styleと、複合キーが一致する現在利用者の`user-profile`を読む。不足なら実質分析を停止する。別利用者のroleを流用しない。
2. **案件:** 特定システム・案件のgapか、practice-wide gapかを確認する。別案件資料を暗黙に集約しない。
3. **管轄:** `request > matter > practice-profile > tenant-default` で解決する。規制の地理的適用、対象者、域外適用、sector、threshold、roleを先に確認する。曖昧ならdiffへ進まない。
4. **情報源:** 現行の公式原文、附則、改正、delegated/implementing acts、公式guidanceを取得する。日付・条文・penaltyをモデル知識で埋めない。
5. **秘匿性・宛先:** current-state資料、compliance gap、accepted riskは機密性が高い。保存先、閲覧者、DLP、保持を確認する。
6. **人のレビュー:** 適用、曖昧な解釈、risk acceptance、priority、外部専門家の必要性は人が決める。日本法モジュールは有資格者レビュー前はdraft。
7. **不可逆操作:** policy変更、system停止、regulator filing、vendor notice、risk acceptanceを自動実行しない。是正計画のdraftまで。
8. **失敗:** 原文未取得、版不明、read coverage不足、write conflictなら停止し、何が不足するかを示す。ローカル保存へ切り替えない。

## 状態

`identify-source` → `scope` → `research-current-text` → `extract-requirements` → `diff` → `prioritize` → `remediation-plan` → `human-review` → `save-draft`

## 1. Sourceとcurrency

- regulation / guidanceの正式名称
- issuing authority
- official URL / document ID / version
- enacted / proposed / effective / phased / repealed
- last checked date
- amendment、litigation、delay、moratorium

二次資料しかない場合、一次資料を取得するまで結論を確定しない。ただし変更可能性は `[verify]` として示す。

## 2. Scope

- 対象法域と域外適用
- provider/builder、deployer/user、importer、distributor等
- sector carve-out
- revenue、user count、headcount、compute、system category等のthreshold
- affected people
- effective/enforcement dates

明らかに適用外なら:

> 適用外と考えられます。理由: [official-source-supported reason]。前提が変わる場合の再確認trigger: [trigger]。

## 3. Requirements

| # | Requirement | Citation | Category | Live date |
|---|---|---|---|---|

Categories:

- Transparency
- Impact assessment
- Human oversight
- Accuracy / testing
- Governance / record-keeping
- Vendor flow-down
- Prohibited practices
- Rights / appeal
- Security / incident
- Registration / filing

法令義務、公式guidance、自主的best practiceを分ける。

## 4. Diff

各要件について:

```markdown
### [Requirement #N]: [name]

**Regulation says:** [quote/paraphrase + source]
**Current state:** [profile/policy/registry/output item]
**Gap:** [None | Partial | Full]
**Missing:** [specific]
**Effort:** [Policy | Process | Product | Assessment | Vendor | Filing]
**Risk:** [penalty/enforcement/reputation, sourced]
```

「documentation不足」ではなく、「System Xにhuman overrideの記録がない」のように具体化する。

## 5. Priority

1. enforceable deadlineとpenalty
2. prohibited practice
3. effort-to-impact
4. 複数use caseへの波及
5. external commitments / customer contracts

正規重大度は🔴 Blocking / 🟠 High / 🟡 Medium / 🟢 Low。上流AIA等のseverityを理由なく下げない。

## 6. Remediation

`references/gap-analysis-output.md` を使い、次を分ける。

- Must-do before enforcement
- Should-do
- Already compliant
- Accepted gaps

accepted riskには、理由、承認者、期限、再検討triggerを必須とする。AIがrisk acceptanceを設定しない。

## 法域別

### EU

`references/common/original-jurisdiction-logic.md` を使い、role、tier、prohibition、GPAI、FRIA、phase-in、implementing actsを現行Official Journalで確認する。

### 日本

`references/common/ja-jp/README.md` から関連moduleを読む。

- AI法をEU型tier規制と同一視しない。
- AI事業者ガイドラインと法的義務を区別する。
- PPC、文化庁、消費者庁、厚労省、デジタル庁、sector regulatorの原文を確認する。
- 2026年個人情報保護法改正は公布・施行を確認するまで現行義務としてdiffしない。

## 非弁護士向け

不確かな日付、threshold、phase-inを本文で断定せず、次へ集約する。

**弁護士に確認する事項:**

- 述べた内容
- 不確かな点
- gapに与える影響

## 保存

初稿はOneDrive、レビュー済み分析はSharePoint `outputs`へ人の確認後に昇格する。tracker状態の更新は正確な`itemId`、最新`eTag`、一意な`idempotencyKey`で行い、auditへ追記する。

gapがゼロでも記録する。確認した範囲と日付が将来のbaselineになる。

## 完了

最重要gap、期限、未確認事項、必要な外部専門家を示し、policy修正文案、owner向けtask、escalation、追加事実、watch-and-waitから選んでもらう。

## 本スキルが行わないこと

- ambiguous textの権威的解釈
- 自律的な規制監視
- 修正の実装
- filing、registration、通知
- sector specialistの代替
