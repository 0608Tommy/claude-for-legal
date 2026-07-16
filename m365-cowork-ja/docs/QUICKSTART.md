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

生成物は `m365-cowork-ja/dist/<plugin>/<plugin>-ja.zip` に保存されます。

## 個人サイドロード

開発・検証テナントでのみ行います。

```bash
atk auth login
atk install \
  --file-path m365-cowork-ja/dist/<plugin>/<plugin>-ja.zip \
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
