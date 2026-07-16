---
name: clearance
description: >
  proposed trademarkのfirst-pass clearanceを行う。日本ではexact文字、かな読み、漢字の観念、ローマ字・翻字、J-PlatPat、Nice class、類似群コード、未登録市場使用、商標法・不正競争防止法・Hyozanを分離してflagし、clearという結論を出さない。
license: Apache-2.0
metadata:
  locale: ja-JP
  source-plugin: ip-legal
  migration-target: direct
  legal-review: pending
compatibility: Microsoft 365 Copilot Cowork; SharePoint/OneDrive storage contract required
---

> **変更通知:** `anthropics/claude-for-legal` (source revision `5ceb305b30b4c82653c9b6642499c12e946ec319`) を日本語化し、Microsoft 365 Copilot Cowork向けに変更した派生ファイルです。


# Trademark clearance

旧来の参照label:
`/ip-legal:clearance [describe the proposed mark, goods/services, and jurisdictions]`。

## Loudest guardrail

> **これはfirst passでありclearance opinionではありません。**
> searchでobvious conflictが見つからないことは、markがclearであることを意味しません。
> adoption、filing、investment前に、日本の弁護士・弁理士または該当法域の
> trademark counselがfull searchと判断を行います。

## Mandatory gate

1. [保存契約](references/common/cowork-runtime-contract.md)を読み、gateway、
   exact profile/user/matter scope、destinationをpreflight。失敗時はread-only。
2. practice mix、registered/enforcement jurisdictions、brand owner、watch、
   approver、search sourceを読みます。未設定ならsetupへ案内。
3. matter scopeならactive/unexpired bindingを要求。practice modeはfresh session。
4. jurisdictionを`request > matter > practice-profile > tenant-default`で解決。
5. 日本なら[商標module](references/common/jurisdictions/ja-jp/trademark-clearance.md)と
   [official source register](references/common/jurisdictions/ja-jp/source-register.md)。
6. connector/resultはlive retrieval時だけsource名を付けます。searchなしなら
   searchなしと明記します。
7. internal memoだけを作り、filing、adoption、opposition、consent agreementを
   自動実行しません。

## Intake

1回のbatchで確認:

- exact mark、word/device/composite/3D/sound、stylization
- kana reading、alternative reading、kanji meaning
- romaji、translation、transliteration、script variation
- actual goods/services、users、channels
- Nice classes（不明ならcandidateを示し人が確認）
- similar-group codes（既知なら）
- use、filing、enforcement jurisdictions
- taglines、family marks、logo/trade dress
- proposed owner/licensee

## Japanese search

record:

- source、query、date、coverage、unread/failed
- J-PlatPat exact、partial、phonetic、owner
- same/adjacent類似群コード、cross-class code
- pending、registered、defensive mark、relevant dead record
- Madrid designation affecting Japan
- trade name、domain、app store、marketplace、social、well-known use
- translation、transliteration、phonetic twins、adjacent word families

official-register hitsとmarket evidenceを別tableにします。dead markはautomatic barでは
ありませんが、fame、predecessor、market evidenceとして記録できます。

searchできない場合:

> **商標database searchは実行していません。** このfirst passはJ-PlatPat、
> Madrid、trade name、domain、app store、marketplace、未登録使用を確認していません。
> intrinsic issueと利用者が示したmarkだけを整理しています。adoption/filing前に
> full professional searchが必要です。

## Japanese analysis

- Trademark Act Arts. 3, 4, 8, 19–20, 26, 32, 50 **[B]**
- UCPA well-known/famous indication、product configuration **[B]**
- JPO Guidelines、Similar Goods/Services、類似群コード、Nice 13-2026 **[G]**
- *Hyozan* overall appearance、sound、concept、actual trading circumstances **[C]**

registrability:

- distinctiveness/generic/descriptive/geographic/deceptive/quality/source
- prohibited/public-interest marks
- earlier mark、well-known/famous indication
- prior use、non-use、limitation
- consent制度（2024-04-01）。written consentだけで足りずJPOのno-confusion判断
- quality control/licence risk

Nice classまたは類似群コード一致をconfusion conclusionにしません。
`du Pont`, `Polaroid`, `Sleekcraft`, Lanham Act, TDRAを日本testとして使いません。

## Other jurisdictions

[U.S./global layer](references/common/original-ip-logic.md)を別に適用し、US、EU、UK、
Madrid/national routeを混ぜません。cross-borderの場合はjurisdiction別sectionを作ります。

## Output

```markdown
# Trademark Clearance — First Pass (NOT AN OPINION)

**Proposed mark:** [...]
**Goods/services:** [...]
**Jurisdictions:** [...]
**Search date/sources:** [...]

## Intrinsic / registrability flags
| Issue | Class | Direction | Source |

## Official-register hits
| Mark | Reading | Owner | Goods/services | Class/code | Status | Source |

## Market/common-use evidence
| Sign | Use/channel | Territory/date | Source | Note |

## Similarity flags
| Appearance | Sound | Concept | Trading circumstances | Direction |

## Scope gaps
## Recommended next steps
```

結論は次のいずれかに限定:

- potential conflicts found; counsel assessment required
- no conflict found in sources actually searched; full clearance required
- factors mixed; counsel judgment required
- no database search; no availability conclusion

10 hit超なら[dashboard標準](references/common/dashboard-template.md)を提案しますが
自動生成しません。

## Completion

full search、mark redesign、goods/services refinement、consent/non-use research、
named counsel escalationから人に選んでもらいます。portfolio追加またはfilingを
自動開始しません。

## 行わないこと

- markがclear/available/non-infringingと結論する
- searchしていないregistryを検索済みと表示
- applicationをfileする
- consentでArt. 4 issueが必ず解消すると表示
- U.S. confusion factorを日本へ移植
- local filesystem、agent、hook、subagentを使う
