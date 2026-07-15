> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) のcontributor guideを日本語化し、Microsoft 365 target向け検証を追加した派生文書です。

# コントリビューション

## 最初のPull Request

最初のPRではCLA Assistantの案内に従い、原文
[`CLA.md`](../../CLA.md) を読み、指定された文言で同意します。日本語参考訳は
[`CLA.ja.md`](CLA.ja.md) ですが、英語原文が正式です。

## 設計原則

`SKILL.md` 自体が正しい挙動を持ち、共通guardrailは安全網として働く構造に
します。guardrailが偶然発火した場合だけ正解になるskillは不十分です。

- doctrine、計算、例外、decline gateをskill本体へ置く。
- 数値、日付、期限の直後にprovenance/verify tagを置く。
- refusalを逃げ道ではなくdefault-onのhard gateとして書く。
- parent gateを広く書き、例外をsub-bulletで限定する。
- irreversible action、matter isolation、source verificationをcompanion
  fileだけに置かない。

## Microsoft 365 target

- source pluginを変更せず、`m365-cowork-ja/cowork-packages/<plugin>`へ追加する。
- strict frontmatterは`name`, `description`, `license`, `metadata`,
  `compatibility`だけを使う。
- skill ID、path、enum、URL、citationを翻訳しない。
- shared referenceをskill rootの外へ参照しない。
- source-derived MarkdownへApache変更通知を付ける。
- 各skillに英語`LICENSE`と`NOTICE`を同梱する。
- connectorとPower Platform solutionをCowork ZIPへ混在させない。
- Cowork DLPが対応済みと表示しない。
- 日本法moduleをqualified reviewerの記録なしに`approved`へ変更しない。

## 検証

```bash
claude plugin validate .claude-plugin/marketplace.json
python3 scripts/lint-tool-scope.py
bash scripts/test-cookbooks.sh

bash scripts/test-m365-cowork-inventory.sh
bash scripts/test-m365-apache-notices.sh
bash scripts/test-m365-cowork-target.sh
bash scripts/build-m365-cowork-packages.sh
```

Python変更はsuppressionsなしでstrict gateを通します。JSONは2-space indent、
全text fileはfinal newline、trailing whitespaceなしとします。
