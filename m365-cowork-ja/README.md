# Microsoft 365 Copilot Cowork 日本語版

このディレクトリは、既存の Claude Code / Claude Cowork 向けプラグインを
変更せずに維持しながら、Microsoft 365 Copilot Cowork 向けの日本語版を
構築するための並列ターゲットです。

## 成果物

- `cowork-packages/`: プラグインごとの Microsoft 365 app package source
- `power-platform-solutions/`: Power Automate / Copilot Studio solution source
- `shared/`: 移植契約、翻訳規約、法域・保存・レビュー基準
- `dist/`: 生成済み ZIP（Git 管理対象外）

Cowork app package と Power Platform solution は別々にビルド・配布します。
Power Automate や Copilot Studio の定義を Cowork app ZIP に入れても実行
されないため、単一 ZIP の機能としては扱いません。

## 移植原則

1. 既存の英語版を正本として保持する。
2. skill、plugin、connector の識別子、パス、列挙値、URL、引用を維持する。
3. 表示名、説明、手順、警告、例、成果物テンプレートを日本語化する。
4. 原法域の忠実な日本語版と日本法版を別のレビュー状態で管理する。
5. 未レビューの日本法モジュールを production package に含めない。
6. SharePoint Lists を構造化状態、document library を共有文書、
   OneDrive を個人下書きの既定保存先とする。
7. Microsoft 365 Copilot Cowork で直接表現できない agent、hook、
   schedule、ローカルファイル操作を、対応済みと偽らない。

## 現在の基準

`shared/target-contract.json` が、実装時に適用する strict host 制約と
Microsoft 公式制約の共通基準です。

```bash
python3 scripts/build_m365_cowork_inventory.py
bash scripts/test-m365-cowork-inventory.sh
bash scripts/build-m365-cowork-packages.sh
```

生成された `shared/source-inventory.json` は、全 source artifact の
移植台帳を作成するための機械可読な基礎データです。人が確認した最終的な
処置、call graph、mode変換、agent対応は `shared/migration-map.json` を
正本とします。
