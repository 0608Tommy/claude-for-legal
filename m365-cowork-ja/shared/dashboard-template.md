> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) のdashboard templateを日本語化し、Microsoft 365成果物向けに変更した派生文書です。

# ダッシュボード標準

価値は装飾ではなく、短時間で全体像を理解できることです。

## 構造

1. **タイトルとmetadata:** 対象、作成日時、範囲を1行で示す。
2. **summary stats:** 重要な件数を先頭に置く。
   `40件: 🔴 3 blocking · 🟠 8 high · 🟡 15 medium · 🟢 14 low`
3. **レビュー担当者向け注記:** 情報源、読取範囲、判断事項、currency、
   宛先、依拠前の作業を1ブロックにする。
4. **chart:** 1～2個まで。risk distribution、category、timelineから選ぶ。
5. **table:** sort/filter可能にし、重要列を画面内に収める。
6. **decision tree:** draft、escalate、追加事実、watch、その他を示す。

## Microsoft 365成果物

- **HTML:** 単一ファイル、inline CSS、外部CDN・font・frameworkなし。
  SharePoint/OneDriveへ保存し、Coworkでファイルリンクを返す。inline
  JavaScriptが表示環境で許可されると仮定せず、静的表でも読めるようにする。
- **Excel:** 会議・共有・フィルタ用途。formula injectionを防止し、
  source、status、owner、date等の列を保持する。
- **PowerPoint:** 経営向けにsummary statsと1～2 chartだけを使用する。
- **Markdown/PDF:** HTMLを開けない利用者向けに同じsummaryを保持する。

tracked changes、特定のWord style、macro、interactive HTMLの動作は、対象
テナントでgolden-file testを通った範囲だけを対応済みと表示する。

## 未信頼入力

- `&`, `<`, `>`, `"`, `'` をHTML entityへescapeする。
- DOMへ入れる文字列は`textContent`を使い、未信頼値を`innerHTML`へ渡さない。
- 未信頼値をscriptへ補間しない。
- URL schemeは`http:`, `https:`, `mailto:`だけを許可する。
- Excel/CSVで`=`, `+`, `-`, `@`から始まる外部値を式として実行させない。

## 表示規則

- severityはred / orange / yellow / green、neutralはgray、statusはblue。
- animation、外部依存、複雑なlayoutを使わない。
- summary、reviewer note、chart、table、decision treeの順序を全pluginで揃える。
