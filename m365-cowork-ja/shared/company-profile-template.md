> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) のcompany profileを日本語化し、SharePoint保存向けに変更した派生文書です。

# 会社・組織プロファイル

全プラグインで共有する会社・組織レベルの事実です。最初のセットアップで
SharePoint `profiles` libraryへ作成し、他のプラグインは同じ`itemId`を
参照します。案件固有情報、利用者固有role、active matterは保存しません。

```yaml
recordType: company-profile
tenantId: "[tenant id]"
organizationId: "[organization id]"
itemId: "[SharePoint item id]"
eTag: "[eTag]"
locale: ja-JP

practiceSetting: "Solo / small firm | Midsize / large firm | In-house | Government / legal aid / clinic"
name: "[会社・法律事務所・組織名]"
industry: "[事業内容または主な取扱分野]"
productsAndServices: "[製品・サービス・提供先、またはN/A]"
size: "[従業員数・弁護士数・関連人員]"

geographicAndRegulatoryFootprint:
  jurisdictions:
    - "[国・地域・州等]"
  primaryJurisdiction: "[主な法域]"
  regulators:
    - "[実際に適用される規制当局]"
  openRegulatoryMatters:
    - "[案件またはnone]"

riskPosture:
  overall: "Conservative | middle | aggressive"
  worstDay: "[重大な失敗]"
  leadershipQuestion: "[経営陣が常に尋ねる問い、またはunknown]"

keyPeople:
  headOfLegal: "[氏名・role]"
  defaultEscalation:
    - "[role or person]"
```

## 分離ルール

- 利用者role・弁護士連絡先は`user-profile`へ保存する。
- current matterはsession–matter bindingへ保存する。
- plugin playbook、review framework、house styleはplugin practice profileへ保存する。
- profile更新はexact `itemId`、current `eTag`、unique `idempotencyKey`で行う。
- 共有値へ案件秘密または別利用者の設定を混ぜない。
