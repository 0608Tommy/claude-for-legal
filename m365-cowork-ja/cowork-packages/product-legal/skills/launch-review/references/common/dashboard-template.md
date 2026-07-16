> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# ダッシュボード標準

価値は装飾ではなく、短時間で全体像を理解できることにあります。

## 構造

1. **Title / metadata:** 対象、作成日時、scope、source version。
2. **Summary stats:** 例
   `40件: 🔴 3 blocking · 🟠 8 high · 🟡 15 medium · 🟢 14 low`。
3. **レビュー担当者向け注記:** source、coverage、authority class、currency、
   destination、before relying。
4. **Chart:** risk、right type、jurisdiction、deadline timelineから1～2個。
5. **Table:** sort/filter可能にし、asset/finding、owner、due、source、statusを保持。
6. **Decision tree:** draft、escalate、追加事実、watch、その他。

## Microsoft 365成果物

- **HTML:** 単一file、inline CSS、外部CDN/font/frameworkなし。SharePointまたは
  OneDriveへ保存し、static tableでも読めるようにする。
- **Excel/CSV:** source、state、owner、date、verification列を保持し、
  formula injectionを防止する。
- **PowerPoint:** summary statsと1～2 chartだけ。
- **Markdown/PDF:** 同じsummaryとsourceを保持する。

native Office fidelity、macro、interactive HTML動作は、target tenantで
golden-file testを通った範囲だけを対応済みと表示します。

## 未信頼input

- `&`, `<`, `>`, `"`, `'`をHTML entityへescape。
- DOM textは`textContent`、未信頼値を`innerHTML`へ渡さない。
- URL schemeは`http:`, `https:`, `mailto:`のみ。
- CSV/Excelで`=`, `+`, `-`, `@`, tab、CR、LFから始まる外部値をneutralize。

dashboardは依頼または提案への同意後だけ作り、自動生成しません。
