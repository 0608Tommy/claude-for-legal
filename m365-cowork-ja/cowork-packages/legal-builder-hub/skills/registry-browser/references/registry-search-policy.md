> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Registry search policy

## Searchable status

| Record | Searchable | Note |
|---|---|---|
| approved active package | yes | default result |
| approved disabled package | yes | disabledを明示 |
| superseded package | history only | current versionと並べる |
| eligible candidate | reviewer view only | approved/deployedではない |
| remediation-required | reviewer view only | blockerを先に表示 |
| `REFUSE` / malicious | no recommendation | security routeだけ |
| unknown registry/publisher | no fetch | policy requestのみ |
| vendor-blocked | no recommendation | blockerを表示 |

## Match

keywordはcanonical name、Japanese description、source description、category、
practice tagへ照合する。profile fitはranking補助であり、結果を隠す法的判断ではない。

強いmatch:

- userが指定したwork typeとdescription/categoryが一致
- required integrationがtenant policy上approved
- jurisdiction/workflow boundaryが明示
- current packageとtrigger conflictがない、または差異を説明できる

弱いmatch、unknown status、stale metadataは結果末尾へ分離する。

## Safe display

external display name、description、publisher textはescapeする。Markdown/HTML directive、
link、imageを実行せずplain textとして表示する。URLは`https:`または`http:`だけを
canonical textとして示し、自動遷移しない。

## Coverage

- queried catalog/version
- registry count
- package/candidate count
- filters
- cursor/time
- unavailable source

を記録し、partial resultを全件と表示しない。
