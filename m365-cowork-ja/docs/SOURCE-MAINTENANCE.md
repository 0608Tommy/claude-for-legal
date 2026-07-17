> **変更通知:** ルート`CLAUDE.md`の保守規約を日本語化し、Microsoft 365 targetの規則を追加した派生文書です。

# Sourceと日本語targetの保守

このrepositoryは、12個の第一者legal plugin、1個のvendor plugin、5個の
managed-agent cookbookを含みます。既存Claude treeは正本であり、日本語
Microsoft 365 targetは`m365-cowork-ja/`に並列追加します。

## Source layout

```text
.claude-plugin/marketplace.json
<plugin>/.claude-plugin/plugin.json
<plugin>/.mcp.json
<plugin>/CLAUDE.md
<plugin>/README.md
<plugin>/skills/<name>/SKILL.md
<plugin>/agents/<name>.md
managed-agent-cookbooks/<name>/
scripts/
references/
```

## Source validation

```bash
claude plugin validate .claude-plugin/marketplace.json
for d in */; do
  [ -f "$d/.claude-plugin/plugin.json" ] && claude plugin validate "$d"
done
claude plugin validate external_plugins/cocounsel-legal
python3 scripts/lint-tool-scope.py
```

Marketplaceは重複、description、source path、hidden Unicode、name regexを
満たします。curated display orderは既知の例外なので、追加時に勝手に全体を
並べ替えません。

## Source conventions

- first-party `marketplace.json`と`plugin.json`のname/description/authorを揃える。
- prose内のskill名は実在するcanonical directory名を使う。
- plugin `CLAUDE.md`はpractice-profile templateであり、project contextではない。
- `external_plugins/`はvendor-maintainedで、許可なく原文を変更しない。
- JSONは2-space、textはfinal newline、trailing whitespaceなし。
- hook欠落やpluginごとの`.gitignore`差異を無断で統一しない。

## Cookbooks

orchestratorはlocal read/routingだけを持ち、MCP/writeは特定leafへ限定します。
READMEのsecurity表、YAML comments、実際のtool scopeを一致させます。

## Microsoft 365 target

- `shared/migration-map.json`で全artifactの処置を管理する。
- `shared/package-catalog.json`でapp ID・日本語表示名を固定する。
- manifestは1.28 skills-onlyを既定とする。
- internal helperはcallerへflattenし、登録skillとして露出しない。
- mandatory safety gateをoptional referenceだけへ移さない。
- referenceはskill root内に閉じ、20 companions以下にする。
- skill配下の全fileは、filenameを除くskill root相対の親directory数を最大3に
  する。root直下は0、`references/file`は1、
  `references/common/ja-jp/file`は3で有効、
  `references/common/jurisdictions/ja-jp/file`は4で無効とする。
- package rootの英語`LICENSE`と`NOTICE`を正式な正本として保持し、
  skills-only ZIPのroot memberからは除外する。
- 各skill rootの必須配布fileを`SKILL.md`、`LICENSE.txt`、
  `NOTICE.txt`とする。後二者はconverter互換の意図的なcopyで、package
  rootの正本とbyte-for-byteで一致させる。extensionlessまたは別拡張子の
  skill-level legal fileは許可しない。
- source-derived fileへApache変更通知を付ける。
- connector、Power Platform solution、Cowork app ZIPを分離する。
- CoCounselは書面承認までblockする。
- 日本法moduleはqualified reviewer承認までproductionへ含めない。
