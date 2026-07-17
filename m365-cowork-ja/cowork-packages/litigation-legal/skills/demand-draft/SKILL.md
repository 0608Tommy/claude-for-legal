---
name: demand-draft
description: >
  completed intakeから日本の催告、契約通知、権利主張、和解通信等をdraftする。時効・通知・delivery、admission、秘密性、事実精度をgateし、FRE 408を日本法として使わず、versioned draftとreview checklistだけを作る。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: litigation-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# Demand draft

canonical label:
`/litigation-legal:demand-draft [slug] [--skip-gate] [--version=N]`

related real state: `resume-strategic`。

すべてdraft。AIはsend、郵便発送、service、署名、settlement、calendar、matter/hold
state変更を実行しない。

## Mandatory gate

1. `references/common/cowork-runtime-contract.md`を読む。
2. exact intake item/versionを取得。欠落なら停止。
3. `strategic_block: skipped | partial`なら
   `resume-strategic | proceed-flagged`を選ばせる。`resume-strategic`はintakeの
   未回答stateへ遷移する。
4. exact user/profile、matter binding/access、destination、external/internal versionを
   確認する。
5. Japanなら
   `references/common/ja-jp/demands-limitation-settlement.md`と
   `source-register.md`を読む。
6. current statute、contract notice clause、limitation、delivery requirementを
   official source/exact contractで確認。
7. confidentiality、admission、preservation、clean-team、DLPを確認。
8. quote/citation/provenanceはcommon rule。unverified citeをinventしない。
9. save/create/update/sendを別operationにする。

## Flags

- `--skip-gate`: gateを実行済みとするdocumented recordがある場合だけ。skip reason、
  approver、record IDをdraft metadataに残す。blank bypassは禁止。
- `--version=N`: requested version。existing sent/final versionをoverwriteしない。

## Japan pre-draft checklist

userが各itemへengageするまでdraftしない。

```text
PRE-DRAFT CHECKLIST — [demand ID]

1. Governing law / forum / notice clause
   exact source and version:

2. Legal character
   rights assertion / contractual cure notice / statutory notice /
   Civil Code 150 demand / settlement communication / other

3. Limitation / accrual / transition
   claim, accrual, knowledge, period, 2020 transition, candidate date:

4. Delivery
   content-certified mail / delivery certificate / contract method / email /
   other; what each proves:

5. Factual accuracy / quote
   unresolved [VERIFY] / exact quote:

6. Admission / escalation language
   facts or liability inadvertently conceded:

7. Confidentiality / settlement use
   actual agreement/order/basis; no automatic FRE 408 effect in Japan:

8. Preservation request
   nonbinding unless order or specific law; exact basis:

9. Tone / signer / destination
   measured / assertive / aggressive; final reviewer:
```

Civil Code 150 demandは6か月完成猶予と再催告制限を正確に扱う。Civil Code 151 agreement
はactual written/electronic agreementとstatutory limitsを確認する。

## Drafting rules

- external letterにinternal privilege/strategy headerを付けない。
- specific fact、date、amount、obligationをsourceへ接続。
- exact quoteがなければquotation markを使わない。
- law/citation不足は`[CITE NEEDED: ...]`。
- fact不足は`[VERIFY: ...]`。
- weak claimはreviewer packetで`[review — strategic call]`。
- preservation requestを法的義務と断定しない。
- `without prejudice`等のlabelだけでinadmissibility/confidentialityを約束しない。
- consequence languageはactual available remedyとapproved toneに限定。
- internal reviewer noteとexternal bodyを別artifactにする。

## Soft structures

### Payment

relationship、obligation/source、default、specific amount、deadline/basis、payment
method、rights reservation、signature。

### Breach / cure

agreement、specific obligation、breach facts、contractual cure、consequence、
rights reservation。

### Cease and desist

right/source、specific act、demand、deadline/basis、available relief、
evidence/preservation requestのlegal status。

### Employment separation

agreement/statute、specific conduct、requested action、relationship/settlement option、
employment specialist review。

### Preservation

dispute context、categories、custodians、date range、nonbinding statusまたはactual
order/law、acknowledgment request。Rule 37(e) sanctionsを日本法として書かない。

## Output

1. in-chat plain-text review
2. OneDrive versioned personal draft
3. internal pre-send checklist
4. approved tenant rendererがある場合だけ`.docx` candidate

`.docx`生成、letterhead/style fidelity、native tracked changesを保証しない。

metadata:

```yaml
demandId: "[ID]"
intakeItemId: "[item ID]"
intakeVersion: "[version]"
draftVersion: "[N]"
legalCharacterJP: "[value]"
gateStatus: completed | documented-skip
gateRecordId: "[ID or null]"
unresolvedMarkers: []
destination: "[external audience]"
status: draft
```

internal checklist:

- final reviewer
- exact final item/version/hash
- all `[VERIFY]`, `[CITE NEEDED]`, `[review]`
- limitation/notice/delivery recheck
- content-certified mail / delivery proof instruction
- internal/external separation
- signer authority
- send is separate operation

## Completion

version、legal character、gate status、markers、source coverage、save destinationを示し、
次から人に選んでもらう。

1. revise
2. qualified counselへescalate
3. missing fact/source取得
4. approved final versionのsend preparation draft
5. other

## 行わないこと

- send/serve/sign/calendar
- FRE 408の日本への移植
- citation/limitationの創作
- preservation義務の過大表示
- automatic matter create/hold issue
- local filesystem、agent、hook、subagent
