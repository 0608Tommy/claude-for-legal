---
name: vendor-ai-review
description: >
  ベンダーのAI addendum、契約、利用規約、AI条項を実務プロファイルの標準と比較する。学習利用、秘密保持、model change、知財、責任、incident、human review、監査、subprocessor、上流モデルのflow-downを確認し、修正文案とエスカレーションを提示する。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ai-governance-legal
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# ベンダーAIレビュー

旧来の参照ラベルは `/ai-governance-legal:vendor-ai-review`。Coworkではvendor名と、権限を持つ正確なSharePoint契約アイテムを会話で指定する。

## 目的

初期設定で記録した「望む標準」と、実際にvendorが提示した「契約条件」の差を確認する。DPAは個人情報を扱い、AI termsは学習、model change、output、AI固有事故等を扱うため、相互の代替ではない。

## 必須ゲート

1. **セットアップ:** SharePoint `profiles` のvendor governance、policy commitments、registry、escalationと、複合キーが一致する現在利用者の`user-profile`を読む。未設定なら実質レビューを停止し、`cold-start-interview` を案内する。別利用者のroleを流用しない。
2. **案件:** session–matter binding、client、counterparty、matter overrideを確認する。別案件の契約・playbookを読まない。
3. **管轄:** 契約準拠法、利用地域、影響を受ける人を確認し、`request > matter > practice-profile > tenant-default` で解決する。日本なら日本モジュール、EU等なら対応基礎を追加する。
4. **情報源:** 実際の契約本文、version、effective date、incorporated URLsを読む。vendor websiteの一般説明を契約条項として扱わない。読めない添付・リンクを黙って無視しない。
5. **秘匿性・宛先:** 契約のNDA、privilege、共有先、DLP、保持を確認する。内部reviewをvendorへそのまま送らない。
6. **人のレビュー:** severity、fallback、redline、risk acceptance、署名推奨は弁護士・指定approverの判断。AIは署名を承認しない。
7. **不可逆操作:** vendorへの送信、契約署名、redline確定、accepted deviation保存は明示確認後。draft作成同意を送信同意にしない。
8. **失敗:** 全文・添付・incorporated termsの不足、大規模文書の部分読取り、権限不足、write conflictならcoverageを示し停止する。ローカル保存へ切り替えない。

## 入力確認

文書種別:

- standalone AI agreement / AI addendum
- main agreementのAI provisions
- Terms of Service
- DPA + AI addendum
- Acceptable Use Policy

AUPだけなら、AUPは利用者側の禁止を示すが、vendorの学習利用・責任・変更通知を示さないと説明し、service agreement / AI addendumを求める。

## 読取り範囲

50ページ超または複数文書では、definitions、AI/data terms、confidentiality、IP、liability、indemnity、security、incident、subprocessors、term/termination、governing lawを優先し、読んだページ・文書をレビュー担当者向け注記に記録する。全体を読んでいない場合、包括的結論を出さない。

## AI stack

次の各層を特定する。

1. End-user SaaS
2. API gateway / orchestration
3. Cloud AI service
4. Model provider
5. RAG / knowledge base / vector database
6. Other subprocessors

上流vendorのterms、責任、学習利用、保持が契約へflow-downされているか確認する。top-level vendorだけをレビューして完了としない。

## Term-by-term

詳細matrixは `references/vendor-review-matrix.md`。最低限:

- Training on our data
- Confidentiality of inputs
- Model changes
- Output ownership / IP
- Liability for outputs
- Incident notification
- Human review rights
- Use restrictions
- Audit / auditability
- Subprocessors / model providers
- Data residency
- Term and termination
- Stacked-vendor accountability

各項目でvendor文言を引用し、profileの`standard / acceptable fallback / never`と比較する。playbookにpositionがなければ、人に決めてもらい、勝手に追加しない。

## Severity

- 🟢 **Aligned** — standard以上
- 🟡 **Note** — fallback内だがstandardより弱い
- 🟠 **Significant** — standard外で交渉・承認が必要
- 🔴 **Critical** — fallback外。解決または明示的escalationなしに進めない

profile定義を優先し、上流の重大度を理由なく下げない。

## AI addendum gap

DPAはあるがAI addendumがない場合、少なくとも学習利用、model change、AI output責任、AI固有incident、上流モデルを確認する。Elevated/High用途では重大gap候補とする。

AI termsが全くない場合、一般termsでAIサービスを提供している事実と、保護がない論点を明示する。vendorの評判から好条件を推測しない。

## Policy consistency

次を比較する。

- policy prohibits training vs contract permits
- human review required vs workflow/terms do not support
- approved vendor list
- disclosure obligation vs contract restrictions
- data residency / confidentiality commitments

矛盾は契約、設計、policyのどれを変えるか人に決めてもらう。

## Redline

最小限の編集を優先する。

1. word
2. phrase
3. subclause
4. sentence
5. whole clause

全面置換は、surgical editより読みにくい場合だけ行い、置換理由をtransmittalに示す。flow-downがなければ、上流model/infrastructure/subprocessorに同等以上の義務を課し、top-level vendorが責任を負う具体的条項を提案する。

## 日本向け

`references/common/jurisdictions/ja-jp/contracts-security.md` を読み、個人情報は `references/common/jurisdictions/ja-jp/privacy-data.md`、著作権は `references/common/jurisdictions/ja-jp/copyright-content.md` を追加する。

- AI事業者ガイドラインを契約義務と混同しない。
- PPCの個人情報・国外・委託/第三者提供の整理を確認する。
- output allocationと日本法上の著作物性を分ける。
- prompt injection、data exfiltration、tool misuse等のAI securityを確認する。
- 2026年改正法の施行前規定を現行契約義務として断定しない。

## Output

`references/vendor-review-output.md` を使う。必須:

- reviewer noteとread coverage
- document/version/use case/tier
- bottom line
- severity counts
- term-by-term comparison
- AI addendum status
- policy consistency
- surgical redlines
- if-they-won't-move fallback / escalation
- unverified incorporated terms

## 署名ゲート

署名可能という最終結論は出さない。非弁護士が署名判断を求める場合、vendor、use case、data use、liability、auditability、model change、accepted deviations、未読文書を1ページにまとめ、弁護士確認まで停止する。

## 保存

初稿はOneDrive。レビュー済み内部memoは`outputs`へ人の確認後に昇格する。accepted deviationをprofileへ反映する場合は別の`customize`変更として差分レビューする。

## 完了

最重要🔴/🟠、必要資料、交渉優先順位を示し、redline package、escalation memo、追加質問、renewal watchから選んでもらう。vendorへ自動送信しない。

## 本スキルが行わないこと

- DPA全体のprivacy review（旧来参照ラベル `/privacy-legal:dpa-review`）
- security postureの技術監査
- fallback外条件の受諾判断
- 契約署名・送信
- 上流terms未取得のまま完全レビューを装うこと
