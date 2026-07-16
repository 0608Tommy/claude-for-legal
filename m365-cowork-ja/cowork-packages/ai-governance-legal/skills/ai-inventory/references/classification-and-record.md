> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# AI台帳 — 分類詳細

## Role

質問: **この組織は、このシステムについて何をしているか。**

- `provider`: 開発し、または開発させ、自己の名称・商標でEU市場に提供または利用開始する。
- `deployer`: 個人的・非職業的利用を除き、自己の権限の下で利用する。
- `importer`: EU域外提供者のAIシステムをEUへ導入する。
- `distributor`: `provider` / `importer` 以外でEU市場に提供する。
- `authorized_rep`: EU域外提供者を代理するEU域内の者。
- `product_manufacturer`: AIシステムを自己の製品へ組み込み、自己の名称・商標で提供する。

複数roleがあり得る場合、単一値に押し込まず関係ごとに記録するか `[review]` とする。実質的変更、目的変更、rebranding、fine-tuningはArticle 25等の現行原文を確認する。

## Tier

### A. Article 5候補

次は条文要約であり原文ではない。

- 行動を実質的に歪めるサブリミナル・欺瞞的手法
- 年齢、障害、社会経済状況等の脆弱性の悪用
- 公的機関のsocial scoring
- 一定のリアルタイム遠隔生体識別
- センシティブ属性を推論する生体分類
- 職場・教育での感情認識
- インターネット/CCTVからの顔画像の無差別収集
- 性格特性のみに基づくpredictive policing

候補があれば `prohibited` を提案し、利用停止・法務レビューへ回す。例外をモデル知識で適用しない。

### B. Annex III候補

1. 生体識別・分類
2. 重要インフラ
3. 教育・職業訓練
4. 雇用、労働者管理、自営業へのアクセス
5. 重要な民間・公共サービス
6. 法執行
7. 移民、庇護、国境管理
8. 司法運営と民主的過程

該当箇所と例外をOfficial Journalで確認し、`high_risk` と `tier_basis` を提示する。

### C. GPAI

- `gpai`: 広範なデータで大規模に学習され、一般性を持ち、多様なタスクを遂行できるモデル。
- `gpai_systemic`: 現行のcompute閾値またはCommission指定を一次資料で確認する。

### D. Limited / minimal

自然人と対話するchatbot、deepfake、一定の感情認識・生体分類等の透明性義務を確認する。その他を `minimal` とする前に、sector lawと他法域を確認する。

## 推奨事項

分類後に次を提示する。

1. 現行法に基づく義務分析
2. `aia-generation` による正式な影響評価
3. `next_review` と `review_trigger`

## 更新監査

shared append-only audit envelopeで記録する。system、change、source、
classification固有fieldは`details`へ入れ、top-levelへ追加しない。

<!-- inventory-audit-event-example -->
```yaml
tenantId: tenant-1
practiceId: ai-governance
matterId: matter-1
eventType: ai-inventory-classified
correlationId: corr-ai-classify-0001
idempotencyKey: ai-classify-0001
actorObjectId: user-1
timestamp: "2026-07-16T11:00:00+09:00"
outcome: succeeded
itemIds:
  - ai-system-item-1
details:
  pluginId: ai-governance-legal
  operation: classify
  systemId: sys-001
  changedFields:
    - role
    - role_basis
    - tier
    - tier_basis
  sourceSystem: sharepoint-state
  sourceItemId: ai-system-item-1
  sourceVersionOrRevisionId: '"12"'
  eTagBefore: '"11"'
  eTagAfter: '"12"'
  reviewedByObjectId: user-1
  sourceTags:
    - statute-regulator-site
```
