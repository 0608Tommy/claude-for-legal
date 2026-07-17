> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) の導入手順をMicrosoft 365 Copilot Cowork向けに変更した派生文書です。

# クイックスタート

## 前提

- Microsoft 365 Copilotライセンス
- Coworkの有効化とusage-based billing
- custom appを許可するテナントポリシー
- Microsoft 365 / Copilot管理者
- Node.jsとnpm

法務機密を扱う場合、先に
[`PRIVACY.md`](PRIVACY.md) と
[`SECURITY.md`](SECURITY.md) を確認してください。2026-07-16時点でCoworkの
DLPとdata classificationは未対応です。Cowork内DLPが必須なら導入を停止
します。

## ローカル検証・ビルド

```bash
npm install --global @microsoft/m365agentstoolkit-cli@1.1.12

python3 -m venv m365-cowork-ja/.cache/skills-ref-venv
m365-cowork-ja/.cache/skills-ref-venv/bin/python \
  -m pip install "skills-ref==0.1.1"

bash scripts/test-m365-cowork-fleet.sh
```

配布用の正本は
`m365-cowork-ja/dist/<plugin>/<plugin>-ja.zip` です。fleet全体のビルドが
成功した後だけ、同一バイトの検証済みconvenience mirrorが
`m365-cowork-ja/cowork-packages/<plugin>/build/<plugin>-ja.zip` に
原子的に置き換わります。`build/` はgit管理外であり、正本ではありません。
手動の `atk package` が同じ場所へ出力したZIPは検証済みとはみなしません。

WSL上のCLIにはWSLの絶対パス、Windowsのfile pickerには `wslpath` が返す
Windowsパスをそのまま使います。手作業で相互変換しません。

```bash
REPO="$(git rev-parse --show-toplevel)"
PLUGIN=ai-governance-legal
CANONICAL_ZIP="$(
  realpath "$REPO/m365-cowork-ja/dist/$PLUGIN/$PLUGIN-ja.zip"
)"
MIRROR_ZIP="$(
  realpath \
    "$REPO/m365-cowork-ja/cowork-packages/$PLUGIN/build/$PLUGIN-ja.zip"
)"

printf 'WSL canonical: %s\n' "$CANONICAL_ZIP"
printf 'Windows canonical: %s\n' "$(wslpath -w "$CANONICAL_ZIP")"
printf 'WSL validated mirror: %s\n' "$MIRROR_ZIP"
printf 'Windows validated mirror: %s\n' "$(wslpath -w "$MIRROR_ZIP")"
```

Windows側では通常
`\\wsl.localhost\<distribution>\home\...\m365-cowork-ja\dist\...zip`
形式になります。表示された正確な値を使用してください。

## 個人サイドロード

開発・検証テナントでのみ行います。

```bash
atk auth login
atk install \
  --file-path "$CANONICAL_ZIP" \
  --scope Personal
```

新しいCowork会話を開始し、日本語のpositive/negative trigger、保存先、
権限、案件分離、成果物を確認します。

## 管理者配布

1. Microsoft 365 admin centerの **Manage apps** でcustom appをuploadする。
2. **Agents → Tools** で対象pluginを選ぶ。
3. pilot user/groupへ限定して配布する。
4. 利用者ごとの接続同意、保持、audit、eDiscovery、sensitivity labelを確認する。
5. tenant acceptanceが完了するまで全社配布しない。

## 外部へ送信する検証

次の操作はZIPまたはsolutionをMicrosoftのvalidation serviceへ送信します。
組織の承認なしに実行しません。

```bash
atk validate \
  --package-file m365-cowork-ja/dist/<plugin>/<plugin>-ja.zip \
  --validate-method validation-rules \
  --interactive false \
  --telemetry false
```
