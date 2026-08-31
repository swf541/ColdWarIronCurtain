# CWIC Localisation Style Guide

How event, focus and idea text is written in this mod. Rules here are drawn from the strongest existing content,
not invented: `VIE_events_l_english.yml`, `FRE_CEFEO_l_english.yml`, `IC_Laos_Raid_l_english.yml` and
`CWIC_Indochina_Outcomes_l_english.yml` are the working references.

Scope: `localisation/english/` only. `french/` and `japanese/` are owned by the translation team - never edit them.

---

## 1. Hard rules

These are mechanical and enforced by `tools/loc_audit.py --check`. They are correctness, not taste.

### ASCII only

The loc files are read as ANSI. Any character above U+007F renders in-game as `?`.

| Never write | Write instead |
|---|---|
| `'` `'` (U+2018/2019) | `'` |
| `"` `"` (U+201C/201D) | `\"` |
| `—` `–` (em/en dash) | ` - ` |
| `…` | `...` |
| `é ì á ü ó ç` etc. | `e i a u o c` |
| `•` | `-` |

Two characters above U+007F are functional and must be kept:

- `§` (U+00A7) opens a colour code, `§!` closes it - `§YMetropole Patience§!`.
- `£` (U+00A3) references an inline sprite - `£texticon_SIA_Separatists_1`, `£decision_SIA_Development`.

Everything else above U+007F is text, and text is what renders as `?`.

### Escape inner quotes

A bare `"` inside a value terminates the string and corrupts everything after it on that line.

```
# WRONG - breaks the key
MEO.2.d:0 "Ho added his own inscription: "Tan Tam Bao Quoc.""

# RIGHT
MEO.2.d:0 "Ho added his own inscription: \"Tan Tam Bao Quoc.\""
```

### Structure

- Paragraph breaks are `\n\n`. A single `\n` is a line break within a paragraph - use it for verse, datelines
  and readouts, not between paragraphs.
- No trailing whitespace inside the value, and no trailing whitespace after the closing quote.
- Titles carry no trailing period and never begin lowercase.
- Match the surrounding file's key numbering. Both `KEY:0 "..."` and `KEY: "..."` are in active use; do not
  convert a file from one to the other while editing it.
- Every flag, modifier and scripted effect that a player can see needs a loc key. An unlocalised one shows the
  raw key on screen.

---

## 2. News events

Reference: **`Etat_du_Vietnam.0`** (`VIE_events_l_english.yml:1255`).

A news event is a wire report. It is not addressed to the player and it does not take sides.

**Title** - `[GetNewspaperHeader]` immediately followed by a headline. Present tense, no article at the front,
no closing period.

```
Etat_du_Vietnam.0.t: "[GetNewspaperHeader]Bao-Dai Proclaims the \"Etat du Vietnam\""
```

**Body** - opens with a dateline, then three paragraphs separated by `\n\n`, ~850 characters total.

```
Saigon, [?global.date.GetDateStringNoHourLong] - Chief of State Bao-Dai has arrived in the capital to proclaim...
```

`[?global.date.GetDateStringNoHourLong]` is the house standard (78 uses against 26 for `[GetDateText]`). Use it
in new text, and migrate `[GetMonth].[GetYear]` and bare `[GetDateText]` when you touch a line for other reasons.

The three paragraphs do the same three jobs every time:

1. What happened, where, and who announced it.
2. The background a reader needs - what it took to get here, what is unresolved.
3. What it sets up next. Close on the open question, not on a verdict.

Register: reported and attributed. No second person, no "our glorious leader", no exclamation marks. Where the
mod's own factions would disagree about the facts, attribute rather than assert.

**Reply** - one short detached line. `"Interesting."` `"The world is watching."` `"Nobody won."` It is a reader
putting the paper down, not a government issuing a statement.

---

## 3. Country events

References: **`VIE_Vinh.3`**, the **`PQC_1950s.*`** block, **`laos_raid.1`**.

A country event is a briefing delivered to the player in their own chair.

**Voice** - first person plural from the firing nation. "Our government", "we", "the staff advise". Present or
recent-past tense. The nation's own bias is welcome here; this is how *they* see it.

**Title** - names the situation, not the mechanic. `"Mutiny in Tay-Ninh"`, `"The Quoc-Cong Civil War"`. Not
`"Stability Event"`, not a question unless the event genuinely poses one.

**Body** - two to four paragraphs, `\n\n` separated, ~400-1200 characters.

1. What has happened.
2. Why it matters to us specifically - our position, our exposure, who inside our government wants what.
3. The decision now in front of us, framed so both options sound defensible.

Do not restate the mechanical effects in prose. The option tooltip already shows them.

**Options** - first person, and they voice a *choice*, not a summary of effects.

```
laos_raid.1.a:0 "Press the offensive - take a capital or nothing!"
laos_raid.1.b:0 "Call off the raid and consolidate our gains"
```

Not `"Gain 25 political power"`. Not `"Option A"`. If an option is the only one, it is an acknowledgement -
`"We await their response."`, `"The Kingdom endures"`.

**Conditional variants** - when an event fires for several tags with `.t.a`/`.t.b`/`.d.a`/`.d.b`, each variant
must be written from that tag's own perspective, with its own facts and its own sympathies. See `BaoDai.16`,
where Saigon and Tokyo read the same death very differently. Do not write one text and lightly reword it.

---

## 4. Focuses, ideas and modifiers

Reference: **`FRE_CEFEO_l_english.yml`**, **`CWIC_Indochina_Outcomes_l_english.yml`**.

- A focus or idea description explains the situation and its cost, in the same national voice as a country event,
  in one to three short paragraphs.
- Put the live numbers at the end, on their own line, in colour codes:
  `\n\n§YMetropole Patience§!: §Y[?FRE.FRE_Metropole_Patience|0]§!/100 - [GetFREMetropolePatience]`
- Variable syntax is `[?SCOPE.var|fmt]`. `[TAG.?var]` is malformed and silently renders empty.
- Colour convention: `§G` good/green, `§R` bad/red, `§Y` neutral emphasis and numbers, `§!` closes. Every opened
  code must be closed.
- `"will be added"` is not a description. If there is nothing to say yet, the focus is not finished.

---

## 5. Names and terminology

Consistency across files matters more than any one romanisation. The mod's established forms:

| Use | Not |
|---|---|
| Bao-Dai, Cuong-De, Ho Chi Minh, Ngo Dinh Diem | Bảo Đại, Cường Để, Hồ Chí Minh |
| Vuong Chi Sinh, Sa Phin, Ha Giang | Vuong Chi Sình, Sa Phìn |
| Dien Bien Phu, Tay-Ninh, Phu Quoc, Haiphong | Điện Biên Phủ |
| Viet Minh (two words), Viet Quoc, VNQDD | Vietminh |
| Etat du Vietnam, Cochinchina, Annam, Tonkin | État du Viêt-Nam |
| CEFEO, the corps, the Expeditionary Corps | the French army |
| Vietnamese | Vietnamise |

Period terms are used as the period used them - "Meo" rather than Hmong, "montagnards", "the Emergency",
"communist bandits" in a Malayan government voice. That is characterisation of the speaker, not the mod's
own position, and it belongs in nation-voiced text rather than in news events.

---

## 6. Checklist before committing loc

- [ ] `python3 tools/loc_audit.py --check` passes.
- [ ] Every new key resolves - no raw keys visible in game.
- [ ] News events have `[GetNewspaperHeader]`, a dateline, three paragraphs, a one-line reply.
- [ ] Country events read from the firing nation's chair, and options are choices.
- [ ] Conditional `.t.a`/`.t.b` variants are genuinely different texts.
- [ ] No wording change smuggled into an ASCII-normalisation commit, and vice versa.
