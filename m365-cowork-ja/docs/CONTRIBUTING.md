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
- manifestのraw `agentSkills[].folder`は`./`込み256文字以下とし、宣言skillと
  source directoryを完全一致させる。
- `SKILL.md`以外（`LICENSE.txt`と`NOTICE.txt`を含む）はすべてcompanionとして
  数え、1 skillあたり20 files、各5,242,880 bytes、合計10,485,760 bytesを
  超えない。
- companion pathの各segmentはASCII `[A-Za-z0-9._! -]+`だけを使う。
  hidden segment、backslash/control、末尾dot/space、Windows reserved
  basename、case-insensitive collisionを含めない。`COM10`はreservedではない。
- source-derived MarkdownへApache変更通知を付ける。
- package rootの英語`LICENSE`と`NOTICE`を正式な正本として必須にし、
  skills-only ZIPのroot memberには含めない。
- 各skill rootの必須配布fileを`SKILL.md`、`LICENSE.txt`、
  `NOTICE.txt`とする。後二者はconverter互換の意図的なcopyで、package
  rootの正本とbyte-for-byteで一致させる。extensionlessまたは別拡張子の
  skill-level legal fileは同梱しない。
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

Microsoft Learnのsize表記は、このrepositoryではbinary MiBのexact byte境界
（5 MiB / 10 MiB）として検証します。15秒companion download timeoutは
runtime-only情報であり、local static testがnetwork timeoutを模擬するものでは
ありません。公式ruleと追加のWindows hardeningの区別は
[`SOURCE-MAINTENANCE.md`](SOURCE-MAINTENANCE.md)を参照してください。
