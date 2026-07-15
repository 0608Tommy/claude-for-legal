> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# AIAインテークと規制分析

## システム

- plain languageで何をするか
- model / vendor / version
- off-the-shelf、fine-tuned、自社開発
- assistive、augmentative、automated
- output: text / score / classification / recommendation / action

## 影響を受ける人

- employees / applicants / customers / children / patients / third parties
- false positive / false negative / hallucinationの被害
- vulnerable groups
- 規模、頻度、期間

## データ

- 具体的な入力項目
- personal data / sensitive data / confidential data / copyrighted content
- training、fine-tuning、RAG、logging
- vendorへの送信、保存国、retention
- source provenanceと削除

## 判断と監督

- outputが自動で行動につながるか
- reviewerの権限、時間、情報、変更率
- appeal / correction / human fallback
- named owner
- kill switchとrollback

## 精度・公平性・安全

- test set、error rate、drift
- demographic / subgroup testing
- security testing、prompt injection、data leakage
- incident history
- monitoring thresholdとreassessment trigger

## 導入段階

- proposed: design review
- pilot: design review + scale gate
- production: retrospective harm check + go-forward review
- scaled: 上記 + remediation plan

## 法域再導出

プロファイル作成後に、新しい地域、対象者、判断類型が追加された場合:

1. 会社の事業地域を読む。
2. 影響を受ける人の所在地を特定する。
3. AIの判断分野を特定する。
4. 現行法を一次資料から検索する。
5. 追加法域をAIAに含め、プロファイル更新候補を示す。

## 法域ごとの記録

```markdown
### [Regime]

**Applicability:** [applies / does not apply / uncertain]
**Role:** [provider / deployer / other]
**Classification:** [regime-specific]
**Prohibited practice:** [none identified / candidate]
**Obligations:** [primary-source-supported list]
**FRIA or separate assessment:** [yes / no / uncertain]
**Effective date:** [confirmed date / confirm with counsel]
**Open interpretation:** [review]
```

`AI role: Both`:

| Obligation | As provider | As deployer |
|---|---|---|
| [citation] | [applies / exception] | [applies / exception] |
