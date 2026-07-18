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
- skill `name`は1--64 charactersの
  `^[a-z0-9]+(?:-[a-z0-9]+)*$`とし、folder名と完全一致させる。
- `SKILL.md` frontmatterはsafe YAMLとしてparseし、malformed YAML、duplicate
  key、mapping以外のroot、string以外の`name`/`description`を拒否する。
  block scalarと許可済みfieldは保持する。
- `description`は1--1,024 charactersとする。外部URLまたはmarketplace表現と
  purchase/subscribe CTAが同時にある場合だけconservative lintで拒否する。
  このlintは意味論の完全証明ではないため、公開時のhuman reviewを必須とする。
- 1 packageの宣言skillは20件以下とし、source validatorだけでなくstandalone
  ZIP normalizerでも同じ上限を強制する。
- internal helperはcallerへflattenし、登録skillとして露出しない。
- mandatory safety gateをoptional referenceだけへ移さない。
- referenceはskill root内に閉じる。
- manifestの`agentSkills[].folder`はraw値を`./`込みで256文字以下にし、
  manifest宣言とsourceの`skills/<skill>/`集合を完全一致させる。
- `SKILL.md`以外の全fileをcompanionとして数える。`LICENSE.txt`と
  `NOTICE.txt`も含め、1 skillあたり20 files以下、各5,242,880
  uncompressed bytes以下、合計10,485,760 uncompressed bytes以下にする。
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
- connector数10件のcontract parityだけをlocalで確認する。transport、auth、
  runtime availability、tenant registrationの受入は従来どおりdelegated/
  blockedであり、offline validatorが完了扱いにしない。
- color iconは192x192のopaque 8-bit RGBまたはopaque 8-bit RGBAを許可する。
  outline iconは32x32 RGBA、transparent background、visible pure-white
  pixelを必須とする。
- CoCounselは書面承認までblockする。
- 日本法moduleはqualified reviewer承認までproductionへ含めない。

### 公式ruleとrepository hardening

公式根拠はMicrosoft Learnの
[`Build plugins for Copilot Cowork`](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-plugin-development)
（git commit
`ccf9e7d4473352536ff966995ed7cf305ff40292`、`ms.date`
2026-06-29、page updated 2026-07-07、確認日2026-07-19）です。
companion count、file/total size、relative path、traversal・backslash・NUL・
hidden segment・Windows reserved nameの禁止、安全な文字、folder長、
15秒download timeout、skill name/description、公開descriptionのmarketplace
CTA注意を公式ruleとして記録します。

Microsoft Learnの`5 MB`と`10 MB`は、このrepositoryでは再現可能な境界値として
それぞれ5 MiB（5,242,880 bytes）と10 MiB（10,485,760 bytes）に固定します。
15秒はCowork runtimeが全companionをdownloadするtimeoutであり、source/ZIPの
static validatorはnetwork時間を計測・強制しません。

明示ASCII segment `[A-Za-z0-9._! -]+`、Unicodeと`@`の拒否、末尾dot/spaceの
拒否、extension付きでもcase-insensitiveにWindows reserved basenameを拒否
（`CON.txt`、`com1.md`は無効、`COM10`は有効）、case-insensitive collision
拒否はcross-platform展開を安定させるconservative Windows hardeningです。
最大depth 3、lowercase extension allowlist、skill-level legal filename規約も
Microsoft universal allowlistではなくrepository/fleet互換ruleです。

icon根拠はMicrosoft Learnの
[`root.icons object`](https://learn.microsoft.com/en-us/microsoft-365/extensibility/schema/root-icons?view=m365-app-1.28)
（git commit `6b6977d3ecac88e4bb94edb4693b7c8d42362aec`）と
[`Design App Icon for Teams Store`](https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/design/design-teams-app-icon-store-appbar)
（git commit `17e3ba5912e75ce4fd10a82b77be0c07a5d08d8f`、確認日
2026-07-19）です。前者はoutlineだけをtransparent PNGと明記し、colorを
full-color PNGとします。後者はcolored/white/full-flat-color backgroundを
例示するため、opaque color PNGを受け入れます。noninterlaced 8-bitとcolor type
2/6限定はparserのattack surfaceを狭めるrepository fleet security profileであり、
Microsoftの全PNGに対する普遍的制約とは主張しません。
