> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。

# 日本の催告、通知、時効、和解通信

## Demand legal-character gate

draft前に次を区別する。

```yaml
legalCharacterJP: rights-assertion | contractual-cure-notice | statutory-notice | Civil-Code-150-demand | settlement-communication | other
```

確認:

1. governing law、forum、契約上のnotice clause
2. exact claim、accrual、knowledge、時効期間、2020年改正の経過措置
3. 民法150条の催告か、151条の協議合意か
4. 内容証明、配達証明、契約指定deliveryが必要か
5. admission、事実精度、tone、threat/escalation
6. confidentialityの法的・契約・court basis
7. preservation requestが命令・具体的法令なしには相手を当然に拘束しないこと

## Limitation baseline

民法:

- 150条: 催告から6か月を経過するまで時効完成を猶予。同期間中の再度の催告は
  追加の完成猶予効を持たない。
- 151条: 権利について協議を行う旨の書面・電磁的記録による合意。期間・再合意の
  completion postponementは、agreementから1年、1年未満の合意期間満了、または
  continuation refusalを書面通知してから6か月のうち最も早い時まで。renewalは
  original completion dateから5年上限。150条periodと重ねてstackしない。
- 166条: claimについて権利行使可能を知った時から5年、権利行使可能時から10年。
- 167条: claim以外のproperty rightは原則20年。ownershipを除く。
- 724条、724条の2: 不法行為、生命・身体の主観期間等。
- 695～696条: 和解。

claimごとのspecial statute、contract、transition、accrual、knowledge、interruption/
completion postponementを確認する。単にdemandを再送して6か月をrefreshできると
書かない。

life/body damageは167条のobjective 20年、tortの724条はknowledgeから3年・
actから20年、724条の2はlife/bodyのsubjective periodを5年とするcurrent textを
確認する。2020-04-01前に生じたclaim等のtransitionをclaim-specificに確認する。

deadline recordは`stated`, `contractual`, `statutory`, `court`, `internal`を分ける。
相手方のstated dateは、契約、法律、裁判手続等のbasisがない限りそれだけで拘束的と
断定しない。

## Settlement communication

日本に一般的なFRE 408型の法定排除はない。民訴法247条はoral argumentと
admitted evidenceの自由評価を扱い、独立admissibility ruleと表現しない。
communicationの利用可能性はcase-sensitive。

- `without prejudice`表示だけでinadmissibilityを約束しない。
- `settlement`表示だけでconfidentialityを約束しない。
- admission、権利留保、契約上の秘密保持、別途confidentiality agreementを確認。
- 裁判上の和解調書のaccess/effectと、私的交渉全体のprivilegeを混同しない。
- court settlement/relinquishment/admissionは民訴法267条のelectronic record、
  final-judgment effect、mandatory serviceをcurrent textで確認。

FRE 408は米国forumが実際に適用されるbranchでだけ使う。

## Delivery proof

- 内容証明: 差出日・内容の証明。内容の真実や到達を証明するものではない。
- 配達証明: 配達事実を示すが、actual recipient identityまで証明するとは限らない。
- email、courier、contract portal: 契約条項とactual delivery logを確認。

AIは郵便発送、email送信、service、calendar登録を実行しない。draftとdelivery
instructionを分離する。

## Demand output

external letterに内部秘密性analysis、privilege header、weakness、approval routeを
入れない。internal reviewer packetに次を残す。

- legal character
- limitation/accrual analysis
- exact sources and unresolved markers
- delivery method and proof
- admission/confidentiality risks
- qualified counsel review
- final source item/version/hash

すべてdraft。sendはfresh approvalとexact final version確認後の別operation。
