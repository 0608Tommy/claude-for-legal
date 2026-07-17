---
name: oss-review
description: >
  authorized dependency list、SBOM、package、outbound codeについてactual license本文、version/hash、direct/transitive、deployment、linking/API、notice/source/patent義務、licence compatibilityをreviewする。日本ではcopyright・contract・patent・trade-secret layerを分け、categoricalなAGPL/LGPL/SaaS shortcutを避ける。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# OSS review

旧来の参照label:
`/ip-legal:oss-review [manifest / SBOM | package name | repo material | paste text]`。

Coworkではauthorized SharePoint/OneDrive item、approved connector result、または
会話で提供されたmanifest/SBOM/license textを使います。local repositoryをscanしたと
表示しません。

## Mandatory gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、gateway、
   exact source/version、scope、destinationをpreflight。
2. user/practice profile、OSS owner、policy、approverを読みます。
3. matter scopeならactive/unexpired binding。practice modeはfresh session。
4. scopeを`dependency-list | single-library | outbound-code`で確認。
5. deploymentを
   `SaaS | distributed-binary | internal-only | embedded-firmware |
   customer-hosted | mobile | container`で確認。
6. actual license/header/NOTICEを読み、metadataだけで分類しません。
7. source code、customer data、credential、trade secretの外部共有をしません。
8. AIはship、publish、source release、licence purchase/acceptanceを決定・実行しません。

[日本OSS module](references/common/ja-jp/trade-secrets-oss.md)と
[source rule](references/common/source-provenance-and-review.md)を使います。

## Inventory

- package/version/source URL/hash
- actual `LICENSE`、file headers、NOTICE
- direct/transitive
- dual-license choice
- modification/fork
- static/dynamic linking、header/inline、IPC/subprocess、network API
- deployment/conveyance
- notice/source/source-offer/installation information
- patent/trademark clauses
- contributor/CLA/DCO/employee/contractor authority
- outbound licence

missing licenseは`unknown`でありpermissive defaultにしません。

## Classification enum

`Permissive | Weak copyleft | Strong copyleft | Public domain |
Non-OSI source-available | Other/custom/unknown`

examples:

- permissive: MIT、BSD-2-Clause、BSD-3-Clause、Apache-2.0、ISC、Zlib
- weak: LGPL、MPL、EPL、CDDL
- strong: GPL、AGPL、OSL、version-dependent EUPL
- source-available: SSPL、BUSL、Commons Clause、Elastic、Confluent、fair-source

`OSI approved`はpolicy classificationです。日本法上のenforceability結論では
ありません。

## Trigger analysis

actual licence version/textを優先します。

- AGPL network interactionを単にdistributionとせず、modification、combined work、
  §13、actual network use。
- pure SaaSだからMIT/BSD UI attributionがautomaticと決めない。
- dynamic LGPL linkingをautomatic low riskとせず、relink/reverse engineering、
  source、notice、modification。
- microservice/API boundaryをautomatic safe harbor/triggerにしない。
- MPLはfile scope、modified files、larger workを確認。
- embedded/firmwareはinstallation information/reproducible replacement ability。
- customer-hosted/container/mobileはcopy conveyanceとdelivery packageを確認。

## Compatibility / outbound

- chosen outbound licenceとembedded dependency
- GPL version compatibility、Apache-2.0 patent terms
- licence conflict between metadata/header/file
- recently relicensed version
- proprietary/confidential/customer code
- credential/history exposure
- project name/trademark policy

## Finding

| Package@version | Licence/source | Class | Deployment/link | Obligations | Risk | Action |
|---|---|---|---|---|---|---|

action:

`comply | replace | remove | attorney-review | seek-commercial-licence |
verify-license | block-release`

strong copyleft、unknown、conflict、source-available business restrictionはhuman legal
review前にship/releaseしません。

## Output

- reviewer note
- scope/deployment/source coverage
- classification counts
- top blockers
- package findings
- obligation checklist
- outbound compatibility
- Japanese law/guidance distinction
- named approver/options

10 package超なら[dashboard](references/common/dashboard-template.md)を提案しますが
自動生成しません。

## Other jurisdictions

[U.S./global layer](references/common/original-ip-logic.md)とlicence governing lawを
separate sectionで示します。日本でのcopyright/contract analysisとFSF/OSI policyを
混同しません。

## 行わないこと

- unknownをpermissiveと分類
- categorical AGPL/LGPL/API conclusion
- actual licenceを読まずにship approval
- code/repositoryをpublicにする
- source disclosure、NOTICE distribution、commercial licence購入を実行
- local filesystem、agent、hook、subagentを使う
