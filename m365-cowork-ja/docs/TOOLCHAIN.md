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
package上限を検証し、skills-only ZIPを再現可能に生成します。検証済みの正本は
`m365-cowork-ja/dist/<plugin>/<plugin>-ja.zip` へfleet単位で原子的に
公開されます。その公開hashを再検証した後、正本とSHA-256、サイズ、全バイト、
正規化ZIP contractが一致する候補12件をすべて完成させてから、各候補を
`m365-cowork-ja/cowork-packages/<plugin>/build/<plugin>-ja.zip` へ
原子的にrenameします。

package-local `build/` はgit管理外のconvenience mirrorです。fleet build成功後
のmirrorだけを検証済みとして扱います。手動の `atk package` 出力、過去のZIP、
途中終了後の一部更新を信頼せず、次を再実行して正本とmirrorを修復します。

```bash
bash scripts/test-m365-cowork-fleet.sh
```

WSLのCLIには `realpath` のPOSIX絶対パスを渡します。Windowsのupload画面では
同じパスを `wslpath -w` で変換し、その出力をそのまま選択します。

```bash
REPO="$(git rev-parse --show-toplevel)"
PLUGIN=ai-governance-legal
ZIP="$(
  realpath "$REPO/m365-cowork-ja/dist/$PLUGIN/$PLUGIN-ja.zip"
)"
printf 'WSL: %s\nWindows: %s\n' "$ZIP" "$(wslpath -w "$ZIP")"
```

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
