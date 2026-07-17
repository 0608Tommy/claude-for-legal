> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# `ja-JP` 日本プライバシー法モジュール

**状態:** DRAFT — qualified Japanese counsel review pending

**一次資料確認日:** 2026-07-16

本moduleは日本が関係するprivacy analysisの追加layerであり、法的助言または承認済み見解ではない。

## 選択

`request > matter > practice-profile > tenant-default`

日本のdata subjects、従業員、応募者、顧客、事業所、vendor処理、保存・提供、通信service、My Number等が関係する場合、日本を含める。`Japan`, `日本`, `JP`, `ja-JP`の意味が矛盾し、対象者所在地やdata flowと合わない場合は停止する。

本moduleはglobal / GDPR / US logicを削除しない。法域ごとに結論、deadline、role、right、transfer routeを分ける。

## 読み分け

| 論点 | file |
|---|---|
| APPIの適用、利用目的、取得、第三者提供、委託、共同利用 | `appi-core.md` |
| 開示、訂正、利用停止等の本人請求 | `rights-dsar.md` |
| 漏えい等報告、本人通知、安全管理 | `breach-security.md` |
| 外国提供、DPA、controller/processorの非同一性 | `cross-border-dpa.md` |
| Cookie、個人関連情報、外部送信規律、通信の秘密 | `tracking-telecom.md` |
| 従業員・応募者、子ども、生体情報 | `workplace-children-biometrics.md` |
| My Number、金融、医療、電気通信その他sector | `sectoral-my-number.md` |
| PIA / DPIA / 特定個人情報保護評価 | `pia-assessments.md` |
| 公式URL、status、確認日 | `source-register.md` |

## 共通原則

1. Binding law、official guidance、internal policyを分ける。
2. APPIにはGDPRと同じ`controller` / `processor`法定区分がない。契約上のlabelを自動変換しない。
3. 日本の本人請求をGDPR/CCPAの`DSAR`と同一視せず、`保有個人データ`、請求要件、拒否根拠、期限を確認する。
4. 民間一般のPIAは一律の法定義務ではない。house trigger、外国法上のDPIA、My Number固有評価を分ける。
5. Cookie全般に一律consentが必要とも、不要とも書かない。APPI、電気通信事業法、通信の秘密、表示・consumer law、適用serviceを分ける。
6. 日本法上の秘密保持・文書提出を米国`ATTORNEY WORK PRODUCT`と同一視しない。
7. 日本法有資格者のreview記録がない限り`pending`から変更しない。

## 2026年改正status

- 2026-07-10: 国会成立。
- 2026-07-14: 内閣が公布を決定。
- 2026-07-16: 参議院議案ページの公布年月日・法律番号は空欄で、施行未確認。

したがって **成立済み・公布確認待ち・未施行**。改正内容を現行法として使わない。
