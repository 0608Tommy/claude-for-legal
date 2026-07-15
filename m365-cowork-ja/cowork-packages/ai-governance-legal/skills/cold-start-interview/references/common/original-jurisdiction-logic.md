> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 移行元の法域ロジック — 日本語基礎レイヤー

本書は移行元の米国・EU中心の判断枠組みを忠実に日本語化した基礎レイヤーです。日本法モジュールに置き換えるものではありません。

## 法域認識

1. 実務プロファイルの法域、案件の準拠法、当事者所在地、販売・導入地域、影響を受ける人の所在地を確認する。
2. 非米国法域が関係する場合、米国法のテストを黙って適用しない。
3. 対応する枠組みがなければ、適用可能な公式基準を検索する、現地有資格者へ回す、または米国枠組みを構造だけに使い、各結論を `[US framework — verify against [jurisdiction] law]` とする。
4. 異なる法域では別々に結論を示す。最も緩い法域を選ばない。

## 管轄解決

Cowork版では次の優先順位を使う。

`request > matter > practice-profile > tenant-default`

上位の明示指定が下位と矛盾するときは、上位指定を採用する前に、案件の事実や影響対象との整合性を確認する。複数候補、空欄、無効な値、越境影響の見落としがある場合は停止する。

## EU AI Act — システム単位の役割

会社全体に1つの役割を割り当てない。同じ組織がSystem Aでは `provider`、System Bでは `deployer`、System Cでは `importer` になり得る。

- `provider`: 自ら開発し、または開発させ、自己の名称・商標で市場提供または利用開始する者
- `deployer`: 個人的・非職業的利用を除き、自己の権限の下で利用する者
- `importer`: EU域外の提供者のシステムをEU市場に導入する者
- `distributor`: `provider` または `importer` 以外でEU市場に提供する者
- `authorized_rep`: EU域外提供者の委任を受けるEU域内の者
- `product_manufacturer`: 自己の製品にAIシステムを組み込み、自己の名称・商標で提供する者

意図された目的の変更、自己データによる大幅なfine-tuning、rebranding等の `substantial modification` があれば、`deployer` から `provider` への役割変化を検討する `[verify against current AI Act text]`。

## EU AI Act — リスク区分

確認順:

1. Article 5の禁止行為
2. Annex IIIのhigh-risk領域
3. `gpai` / `gpai_systemic`
4. 透明性義務を伴うlimited risk
5. minimal risk

移行元が示す禁止行為の要約には、行動を実質的に歪めるサブリミナル・欺瞞的手法、脆弱性の悪用、公的機関のsocial scoring、一定のリアルタイム遠隔生体識別、センシティブ属性を推論する生体分類、職場・教育での感情認識、顔画像データベースの無差別収集、性格特性のみに基づくpredictive policingが含まれる。これは条文の代替ではなく、毎回Official Journalで確認する。

Annex IIIの要約領域:

1. 生体識別・分類
2. 重要インフラ
3. 教育・職業訓練
4. 雇用、労働者管理、自営業へのアクセス
5. 重要な民間・公共サービス
6. 法執行
7. 移民、庇護、国境管理
8. 司法運営と民主的過程

`gpai_systemic` のcompute閾値、条文番号、附属書の細目、施行段階は変動し得るため、一次資料確認なしに固定しない。

## FRIA、AIA、PIA

- AIAはAI設計・導入の責任ある判断記録。
- PIA / DPIAは個人データ処理の適法性とリスクを扱う。
- FRIAが別途要求される場合、AIAで代替したと扱わない。
- formal conformity assessmentが必要な場合、内部AIAをその代替と主張しない。

## 米国法上の秘匿性表示

`ATTORNEY WORK PRODUCT` は米国の doctrine（例: FRCP 26(b)(3)）であり、表示だけで保護は生じない。

- EU: 一般的なwork-product保護はなく、LPPの範囲は異なる。
- UK: litigation privilegeには通常、合理的に予見された訴訟等の要件がある。
- その他の法域: 保護の範囲は異なり、内部AIA、DPIA、launch reviewが当然に秘匿されるとは限らない。

日本向け成果物では米国法上の保護を断定せず、秘密保持、依頼関係、作成目的、共有範囲を有資格者が確認する。

## 米国の変動領域

移行元 `currency-watch.md` は2026-05-10確認であり、90日を超えた場合は最新情報源としてではなく検索チェックリストとしてのみ使う。特に次を毎回確認する。

- Colorado AI Actの施行日・改正
- Texas TRAIGA
- NYC Local Law 144
- Illinois AIPAおよび雇用分野のAI改正
- その他州法の成立・延期・執行
- EU AI Actのimplementing acts、delegated acts、harmonised standards
- 米国連邦機関の執行方針・Executive Orders

## 情報源が不足する場合

次の3択とする。

1. 追加情報源を取得し、出所タグを付けて進む。
2. 原文が得られるまで停止する。
3. 結論には使わないが、結果を変え得る既知の疑義を `[model knowledge — verify]` として示す。

既知の施行延期、訴訟、失効、改正提案を黙って無視しない。
