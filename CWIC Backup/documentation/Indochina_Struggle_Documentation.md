# Indochina Struggle GUI System

## Overview

The Indochina Struggle GUI is the core mechanic for the First Indochina War. It uses a
phase system (3-8 active, 9-11 endings) and five faction scores to determine outcomes.
All major decisions, focus trees, and events feed into this GUI system.

## Design Philosophy

**GUI-Centric Design:**
- Decisions and focus trees act as triggers/precursors, not automatic resolvers
- All state transfers, peace treaties, and major changes happen in GUI ending effects
- Player selects endings through GUI, maintaining agency

**Integration Pattern:**
- Decisions: Unlock GUI options, set flags, award scores
- Focus Trees: Award scores, unlock GUI options, set flags
- Events: Award scores, modify phase points, provide narrative
- GUI Endings: Handle all state changes, peace treaties, annexations

---

## The scoring charter

The authoritative copy of this table is the header block above the helper section in
`common/scripted_effects/CWIC_Struggle_Effects.txt`. Keep the two in step.

**Two currencies, orthogonal.**
- *Faction score* = a camp's claim to decide the postwar settlement. Stored on FRA.
- *A / B points* = how hot the war is. Global. A phase flips at > 499.

A battlefield win can raise both; a negotiated win raises score and lowers heat.

### Faction score tiers

| Tier | Value | Used for |
|---|---|---|
| T1 | 3 | raid `limited_success` |
| T2 | 6 | raid `success`, minor event option |
| T3 | 15 | raid `critical_success`, ordinary focus |
| T4 | 50 | named operation, campaign phase, diplomacy decision |
| T5 | 100 | Vinh Yen, Na San, Hoa Binh, Northwest, RC4, Laos raid victory |
| T6 | 200 | Dien Bien Phu, fall of a capital, Castor failure |
| T7 | 350 | ending unlock, unification, Geneva accession |

### Phase point tiers

| Tier | Value |
|---|---|
| P1 | 5 |
| P2 | 10 |
| P3 | 25 |
| P4 | 50 |
| P5 | 100 |
| P6 | 175 |

### Symmetry rule

A contested outcome pays the winner T*n*, the loser -T*n*/2, and the opposing faction
+T*n*/2. **No outcome pays both sides positively for the same result.**

### Repeatable score income

Raids and Struggle Diplomacy decisions award their listed score directly. The former
monthly cap was removed because it silently discarded otherwise successful outcomes,
required five persistent faction counters plus reset plumbing, and did not reliably
enforce its nominal ceiling (an award could overshoot it). Raid availability, cost,
duration, and outcome odds remain the visible limits on repeatable score income.

One-shot content - focuses, named operations, and battle outcomes - continues to use the
`indochina_struggle_grant_*` helpers so its intent remains distinct from repeatable
content, although both now write score directly.

### Score target

A faction committed to its historical path lands **1200-1500 by mid-1954**; a
present-but-passive faction lands **300-500**. Removing the repeatable cap increases the
upper bound for unusually raid-heavy play, so these targets should be rechecked in the
next full AI balance run. The ending thresholds remain (`> 1000`, `> 499`).

---

## Core Components

### Faction Arrays (Stored on FRA)
- Communist: VIN, NLF, MEO
- Pro-France: FRA, CAM, LOS, RCG, SEN, TOG, CMR, TUN, MOR, FRE, AND, SAR
- Pro-Independence: VIE, CCC
- Pro-Ethnic: NUN, FUL, TAI, TAM, THO
- Kuomintang: PQC, added by `PRC_Lose_CCW` / `ROC_lose_CCW` when the Chinese Civil War
  resolves. MEO can move itself into this array (or into Pro-Ethnic) from `MEO_50s`.
- Interlopers: USA, SOV, PRC, CHI, SIA, KOR, KPA, HUM

### Score Variables (Stored on FRA)
- `StruggleInvolvedNationsIndochinaCommunistScore`
- `StruggleInvolvedNationsIndochinaProFranceScore`
- `StruggleInvolvedNationsIndochinaProIndependenceScore`
- `StruggleInvolvedNationsIndochinaProEthnicScore`
- `StruggleInvolvedNationsIndochinaKuomintangScore`
- `StruggleInvolvedNationsIndochinaTotalAntiCommunistScore`

**The anti-communist total is derived**, not accumulated:
`indochina_struggle_recalculate_total_anti_communist_score` rewrites it every day from
`on_daily_FRA` as ProFrance + ProIndependence + ProEthnic. **Never add to it directly** -
the write is erased within a day. Kuomintang is deliberately outside the sum, so KMT
points neither help nor hinder the anti-communist ratio gates.

### Helper effects

All in `common/scripted_effects/CWIC_Struggle_Effects.txt`.

| Helper | Caller sets | Behaviour |
|---|---|---|
| `indochina_struggle_award_<faction>` | `temp.ic_award` | repeatable score award |
| `indochina_struggle_grant_<faction>` | `temp.ic_award` | uncapped one-shot grant |
| `indochina_raid_award_actor` | `temp.ic_award` | dispatches on `actor_country`'s faction array |
| `indochina_raid_award_victim` | `temp.ic_award` | dispatches on `victim_country`'s faction array |
| `indochina_raid_penalise_victim` | `temp.ic_award` | subtracts from the victim's faction |
| `indochina_raid_escalate` / `_deescalate` | `temp.ic_phase` | A / B points |
| `indochina_struggle_escalate` / `_deescalate` | `temp.indochina_phase_amount` | A / B points; the older spelling, used outside the raid file |
| `indochina_struggle_add_<faction>_military_points` | - | T3 score + P4 to A |
| `indochina_struggle_add_<faction>_diplomatic_points` | - | T3 score + P4 to B |

`<faction>` is one of `communist`, `pro_france`, `pro_independence`, `pro_ethnic`,
`kuomintang`. All five exist for every helper family.

### Phase System

**Active Phases (3-8):**
- Phase 3: High Intensity
- Phase 4: Medium Intensity (campaign start)
- Phase 5: Low Intensity
- Phase 6: High Tension
- Phase 7: Medium Tension
- Phase 8: Low Tension (max de-escalation)

**Ending Phases (9-11):** 9 Never Ending Conflict, 10 Failed State, 11 Geneva Conference.
Phase 100 = struggle over (cleanup).

**Phase Variables:** `global.Indochina_War_Active_Phase`,
`global.Indochina_War_Next_Phase_A_Points`, `global.Indochina_War_Next_Phase_B_Points`.

**Transition Rules:**
- 500-point threshold; the flip zeroes **both** pools
- Escalation is checked before de-escalation, so it wins a same-day tie
- Transitions only while phase < 8; `indochina_struggle_clamp_scores` pins A at 499 in phase 3
- Ending phases are set when endings trigger via the GUI

---

## Ending Conditions

Shorthand: `C` Communist, `PF` Pro-France, `PI` Pro-Independence, `PE` Pro-Ethnic,
`KMT` Kuomintang, `AC` = PF + PI + PE.

**The settlement window** (`indochina_settlement_window_trigger`): tension phase 6-8 and
after 1953.1.1. The three negotiated endings - Federal, Balkanized, Dan Quoc - require it.
Without it a France that banked points through the 1951-52 defensive battles could impose
a federal settlement in 1952, while the war was still at High Intensity. The military
endings (Communist, Southern, Kuomintang) are decided on the map and are not gated by it.
The failsafe mirrors carry the date floor but not the phase gate, so a genuinely stuck war
can still be routed out of a hot phase.

### 1. Communist Victory (VIN)
`C > 2*AC` and `C > 1000`. Map bypass: at war with VIE and owns Saigon (286), or VIE
capitulated / gone.
Effect: VIN annexes VIE/NLF, transfers all Vietnam states, capital to Hanoi (1760).

### 2. Southern Victory (VIE)
Non-communist government, high tension with VIN (war or mutual opinion < -50), **any
active phase**, `AC > 2*C`, `PI > PF`, `PI > PE`, `PI > 1000`. Map bypasses: owns Hanoi
(1760) while at war, or VIN annexed and VIE holds both capitals.
Effect: VIE annexes VIN/NLF, capital to Saigon (286), cores Hanoi.

### 3. Federal Vietnam (FRA)
**Settlement window**, `AC > 2*C`, `PF > PI`, **`PE > 250`**, `PF > 1000`, `PF > PE`.
The ethnic clause is an absolute floor - the Crown Domains still exist as a political
fact - rather than a race against Saigon. Tying it to Pro-Independence made it
unreachable when that score was starved and unreachable again once it earned properly.

### 4. Balkanized Vietnam (FUL / FRA / CCC)
**Settlement window**, `(PE+PF) > 1000`, `> 2*PI`, `> 2*C`, and **`PE*2 >= PF`**.
Federal keeps `PF > PE`, so 3 and 4 overlap in the band `PE < PF <= 2*PE`. That overlap
is deliberate: with a respectable but not dominant ethnic score the player gets a real
choice between the two, and the daily availability ladder's fixed order (federal before
balkanized) only decides which the popup surfaces first.

### 5. Dan Quoc Peace (VIN / VIE)
**Settlement window**, `dan_quoc_peace` flag, Diem ruling VIE, Ho ruling VIN, `PI > PF`,
`PI > 499`.
Also reachable outright via the `diem_ho_chi_minh_reunified` flag.

### 6. American-North Vietnam Diplomatic (USA / VIN)
Ho ruling VIN, not at war with USA, positive mutual opinion, VIN favours USA over SOV,
`USA_50s_Reestablish_Deer_Team` complete, `C > 2*AC`, `C > 499`.

### 7. Kuomintang Victory (PQC)
PQC exists and VIE has warred it. Owns both Saigon and Hanoi, **or** owns one plus
**`KMT > 500`** and `KMT` greater than every other faction score.

### 8. Geneva Conference (any)
`Geneva_Conference_Preparations` and `Geneva_Conference_Negotiations_Complete`. The
conference itself becomes available at phase 8 with B > 499, via the FRA decision, the
FRE focus, the Pro-Independence proposal decision, or the panic-collapse path.
Effect: partition at the negotiated line, Laos and Cambodia independent.

### 9. Never Ending Conflict (any)
Phase 9, or after 1957.1.1 in any active phase with the failed-state test not passing.

### 10. Failed State (any)
Phase 10, or after 1955.1.1 with **all five** faction scores below 500.

### The unfinished-arc guard

`vin_campaign_finish` white-peaces FRE, TAI and TAM at the end of every VIN campaign, so
the cooldown between campaigns is a genuine no-war state **by design**. The failsafe's
no-war watchdog read that lull as the end of the war and terminated the struggle in June
1952, in a run where VIE had also annexed NLF.

Two guards now stand between a lull and the terminator:

- `ic_failsafe_no_theatre_war_trigger` tests whether VIN, NLF, LAO, MEO, PQC or FRE is at
  war *at all*. Those tags exist only for this theatre, so any war they are in is this
  war. The old form enumerated belligerent pairs and went blind the moment one of the
  named pairs stopped existing.
- `ic_failsafe_theatre_unfinished_trigger` holds while the scripted arc still has content
  in front of it: before 1954.7.21 always, while a conference is sitting, or before
  1955.1.1 while VIN still has a campaign to run (`VIN_Campaign_Cooldown_Tay_Bac` /
  `_Hoa_Binh` / `_Dien_Bien`) or the Laos raid is live. The no-war watchdog will not route
  while it holds, the router will not enter its mutating preflight without a genuinely
  decisive condition, and postflight cannot dissolve CEFEO merely because a normal
  campaign cooldown currently satisfies `ic_failsafe_no_theatre_war_trigger`.
  `indochina_failsafe_force_cleanup_if_needed` will not terminate while the guard holds.
  The 1955 ceiling stops a permanently passive Hanoi from holding the theatre open.

### Failsafe mirrors

`common/scripted_triggers/IC_Failsafe_triggers.txt` carries a score-mirror copy of each
ending trigger (`ic_ending_federal_ok` etc.) reading `global.ic_score_*` instead of the
FRA variables, so the contingency layer still works once France is gone. **Every
threshold change above must be made in both files in the same commit.**

---

## Where score comes from

| Source | Owner | Notes |
|---|---|---|
| `common/raids/Indochina_Raids.txt` | all five | 73 raids, T1/T2/T3 by outcome level, dispatched through `indochina_raid_award_actor`. Capped. |
| Struggle Diplomacy decisions (`common/decisions/Indochina_War.txt`) | all five | 3 de-escalation + 1 escalation per faction. 25 PP, 70-day re-enable, 45-day per-faction lock. Capped. |
| `events/FRE_Events.txt` | ProFrance / Communist | 6 preparation missions (T3), 5 named operations (T4), 5 set-piece battles (T5 aggressive / T4 cautious), the DBP arc (T6). |
| `common/national_focus/FRE_50s_Indochina.txt` | ProFrance / ProEthnic | includes `FRE_Proclaim_Victory_in_Indochina` (T7) and its mirror `FRE_The_Fall_of_Saigon` (-T7), plus `FRE_Montagnard_Loyalty` (T5 ethnic). |
| `common/national_focus/VIN_50s.txt` + `VIN_Campaign_Effects.txt` | Communist | the campaign milestones: border campaign, Northwest, Hoa Binh (T5 each), Dien Bien Phu (T6). |
| `common/scripted_effects/IC_Laos_Raid_Effects.txt` | Communist / ProFrance | attacker victory T5, stalemate T4, total failure pays France T4. |
| `common/national_focus/VIE_50s_*.txt` | ProIndependence / ProEthnic | National Army (T5); the traditional-tactics and Territoire Autonome branches pay ethnic. |
| `common/national_focus/{FUL,NUN,MEO,PQC,CCC}_*.txt` | ProEthnic / KMT / Communist | 69 wired focuses. These trees awarded nothing before. |
| VIE State Integration Panel (`Vietnam_effects.txt`) | ProIndependence / ProEthnic | integrating a state pays ProIndependence T3 and costs ProEthnic 8; opening diplomacy pays ProEthnic T3. |
| `USA_FP_50s.txt`, `America_1950s_Expansion.txt` | Communist / ProInd / ProFrance | via the `USA_indochina_add_*_score` helpers. |
| `Indochina_Border_War.*` (`events/Indochina_War_Rework.txt`) | all five | flat T4 per border-war resolution. |

### The communist victory unlock

`indochina_struggle_auto_trigger_communist_victory_preparation` fires once from
`on_daily_FRA` when VIE capitulates/vanishes or VIN takes Saigon while at war. It pays
T7 + P6 as an ending *unlock*, not as the war's reward - the war itself is earned through
the campaign milestones above.

### Time-Based Drift (on_monthly_FRA)

- 1950-52: +25 A/month while phase > 3
- 1953: +20 B/month
- 1954: +30 B/month
- 1955: +25 B/month

The de-escalation drips are gated on `NOT has_global_flag Indochina_War_Escalated` (a war
at full intensity does not cool itself) and run in every active phase including Low
Tension, so progress toward the Geneva threshold does not stall at maximum de-escalation.

---

## Focus Tree Bypass System

Focuses automatically bypass when their ending becomes available:
- `VIN_Total_Victory` - Communist Victory
- `VIE_BaoDai_Liberator_of_Vietnam` - Southern Victory
- `VIN_Accept_French_Three_Vietnam_Federal_Scheme` - Federal Vietnam
- `VIN_A_Failed_State` - Failed State
- `VIE_Accept_Geneva_Conference` - Geneva Conference

Bypass triggers check if the ending trigger is met OR the war is over.

## Indochina_Wrapup_Timer (AI-only auto-resolution)

Activated from `ic_pulse` only when `indochina_struggle_all_participants_ai_trigger`
passes: France and every Indochina participant is AI controlled. A human playing any
participant keeps full control; interloper players still shape the outcome through scores.

Historical window 1954.5.20-1954.7.10, with the 60-day timeout landing ~21 July 1954. A
post-1957.1.1 window catches AI-only stalemates. On timeout it runs the first *earned*
decisive ending, defaulting to the historical Geneva partition.

## Save-load guard

The struggle `on_startup` block is guarded by `indochina_struggle_initialized`; without it
every reload reset the phase/scores and duplicated the GUI arrays.

---

## Testing

`common/scripted_effects/IC_Struggle_Test_Effects.txt`:
- `e test_ic_score_report` - dumps all five scores, the derived total, the phase, and both
  point pools to `game.log`
- `e d_ic_reset`, `e test_indochina_set_<faction>_high`, `e test_indochina_set_phase_*`,
  `e test_indochina_trigger_<ending>` - the pre-existing harness

Verification passes worth repeating after any change to the ladder:
1. Brace balance and on-tier values across `Indochina_Raids.txt`
2. `python3 tools/loc_audit.py --check`
3. A full AI run from 1949, reading `test_ic_score_report` at 1954.7

## File Locations

- Scripted GUI: `common/scripted_guis/CWIC_Struggle.txt`
- On Actions: `common/on_actions/CWIC_Struggle_on_actions.txt`
- Scripted Effects: `common/scripted_effects/CWIC_Struggle_Effects.txt`
- Scripted Triggers: `common/scripted_triggers/IC_struggle_triggers.txt`
- Failsafe: `common/scripted_effects/IC_Failsafe_Effects.txt`,
  `common/scripted_triggers/IC_Failsafe_triggers.txt`,
  `common/on_actions/IC_Failsafe_on_actions.txt`
- Test Effects: `common/scripted_effects/IC_Struggle_Test_Effects.txt`
- Decisions: `common/decisions/Indochina_War.txt`, `common/decisions/FRA.txt`
- Raids: `common/raids/Indochina_Raids.txt`
- Events: `events/FRE_Events.txt`, `events/Indochina_War_Rework.txt`, `events/VIE_Events.txt`
- Focus Trees: `common/national_focus/VIN_50s.txt`, `VIE_50s_Bao_Dai.txt`,
  `FRE_50s_Indochina.txt`, `FUL_50s.txt`, `NUN_50s.txt`, `MEO_50s.txt`,
  `PQC_1950s.txt`, `CCC_50s.txt`
