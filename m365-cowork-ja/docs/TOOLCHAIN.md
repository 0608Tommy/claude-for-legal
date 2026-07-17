> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) の検証・配布方式をMicrosoft 365向けに変更した派生文書です。

# 固定ツールチェーン

基準日は2026-07-17です。機械可読な正本は
`../shared/toolchain-lock.json` です。

| 用途 | 固定値 |
|---|---|
| Unified App Manifest | 1.28 |
| M365 Agents Toolkit CLI | `@microsoft/m365agentstoolkit-cli@1.1.12` |
| Agent Skills reference validator | `skills-ref==0.1.1` |
| Power Platform CLI | `Microsoft.PowerApps.CLI.Tool@2.9.3` |
| Power Platform runtime | .NET 10 |

## ローカルのみで行う検証

```bash
atk validate \
  --manifest-file m365-cowork-ja/cowork-packages/<plugin>/manifest.json \
  --interactive false \
  --telemetry false

m365-cowork-ja/.cache/skills-ref-venv/bin/python \
  -m skills_ref.cli validate \
  m365-cowork-ja/cowork-packages/<plugin>/skills/<skill>
```

`scripts/build-m365-cowork-packages.sh` はmanifest、skill、Apache通知、
package上限を検証し、skills-only ZIPを再現可能に生成します。

## 公式converter

Microsoftの `Convert-ClaudePluginToMOS3.ps1` はversion/checksumが公開されて
いないため、scaffoldとしてのみ使用します。現在のscriptはplaceholder
icons/OAuth、`devPreview`、未正規化SKILL.mdを生成し得るため、そのまま
配布しません。

## Power Platform

Power Automate / Copilot StudioはCowork app ZIPと分離したmanaged solution
として扱います。`pac solution check` はsolutionをPower Apps Checkerへ
送信する外部開示操作です。test environment、connection reference、
environment variable、最小権限identityを準備してから実行します。
