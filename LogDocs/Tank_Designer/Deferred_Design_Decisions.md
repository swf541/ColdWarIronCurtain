# Deferred designer decisions and QA follow-up

Date: 2026-09-06. Owner direction: `TankQANotes.txt`; source context:
`HANDOFF_Deferred_Scope.md`. This records accepted choices and new implementation
judgment. It does not replace the frozen workbook or claim unfinished work is done.

## Accepted direction

| Area | Decision | Implementation status |
| --- | --- | --- |
| Mechanized | Build APC/IFV designer roles using the existing light/medium hull families and the 18 mechanized envelopes. Preserve non-NSB equipment support. | Conversion pending |
| Heavy Mech III | Keep the existing equipment year, 1955. Record the workbook's 1960 as a deliberate year exception; do not change its stats. | Existing year retained |
| Artillery/AA | Gate the legacy and designer paths by DLC; preserve technology-based sub-unit activation. | Target manifest frozen; delivery changes pending |
| Amphibious | Use an amphibious mobility module on eligible mechanized designs; replace NSB whole-equipment amphibious unlocks only when the replacement vehicles and marine-unit supply contract work. | Pending; legacy marine equipment still needed |
| Night/thermal vision | Author new balance values and record them as design decisions. | Pending |
| Special slots | Specialize the ten existing special slots without expanding the 15-position GUI. | First layout implemented |
| Source workbook | Keep byte-identical; use the CSV and explicit reviewed overrides for new balance. | Preserved |

## Specialized slots

The five existing mandatory slots remain turret, weapon, suspension, base armor,
and engine. The following ten optional slots have the same IDs and GUI positions
as before, but narrower category lists and descriptive English titles.

| Slot | Allowed categories | Design tradeoff |
| --- | --- | --- |
| 1, 2 | Kinetic, chemical, missile or HE ammunition | Two ammunition choices; conventional recipes retain AP and HE |
| 3 | Aiming devices | Dedicated aiming/stabilization capacity |
| 4 | Optics | Dedicated sight capacity; vision integration still to be designed |
| 5 | Ballistic/artillery computer or radar | Computing and radar compete |
| 6 | Manual loader assist, autoloader or artillery loader | One loading system |
| 7 | Passive or reactive protection | Additional armor choice |
| 8 | Passive, reactive or active protection | APS competes with another armor layer |
| 9 | Survivability, auxiliary mobility or smoke | Utility capacity |
| 10 | Secondary weapon, survivability, auxiliary mobility or smoke | Secondary weapon competes with utility capacity |

All 18 existing special-module categories remain reachable on all three hull
archetypes. Existing category count limits remain in force. No new module is
silently added to a slot, no GUI frame is resized, and no extra slot is created.
The 125 generic AI recipes and 35 explicit starting/export recipes currently
use only the ammunition slots or leave the special slots empty, so they fit.
Player designs from before this slot change may use now-ineligible placements;
use fresh campaigns for acceptance testing, as required by the branch handoff.

## QA changes implemented

1. Finland's Soviet T-55 focus now pairs NSB research with NSB enabled, and
   legacy research with NSB disabled, both for availability and rewards. A
   producer's research from the other DLC path cannot open a non-paying focus.
   The legacy focus still requires Soviet `main_battle_tanks_3` research.
   The same DLC pairing is applied to Greece and both generic supplier focuses.
   All four legacy `else_if` rewards are now siblings of their designer `if`,
   rather than nested inside it; validation checks that structural distinction.
2. USA and SOV receive an explicit 1980 tank-research package in dated history.
   It grants all 97 NSB tank/hull/module technologies dated through 1980 except
   the experimental super-heavy gun, or the corresponding legacy tank research
   when NSB is disabled. This is an authored major-producer baseline, not a
   claim that both countries historically fielded every system. It fills the
   USA's missing post-1960 progression and Soviet module gaps. Other countries
   and their OOBs are not changed by this package.
3. Four gas-turbine technologies now use 1965/1975/1985/2005, three MBT heavy-gun
   technologies use 1985/1995/2010, and the super-heavy gun uses 1955. HEAT-MP and
   HEAT-DU each use 1985/1995/2005. Research years, AI dates and named GUI rows
   now agree. These 14 technologies previously retained 1940/1942 research dates.
   Gun/ammunition dates were checked against the drawio gun page; the heavy MBT
   scratch worksheet's differing dates were not substituted for that tree.
4. Export helper internals run inside `hidden_effect`. Export variants remain
   producer-flag-guarded and name-stable, but are created as obsolete to keep
   them out of the producer's default production list. Stockpile and license
   references remain explicit. Live validation must confirm archived export
   designs remain usable through the license UI.
5. Conventional turret balance now differs from light turret balance, below.

## Conventional turret balance

Authored decision in response to QA: conventional turret gets +5% breakthrough
for an extra 0.5 IC. The light turret remains the inexpensive option. Reliability
is unchanged. This is a limited choice between cost and breakthrough, not a
complete turret/weapon-size eligibility redesign.

| Field | Frozen workbook | Revised conventional turret | Light turret |
| --- | --- | --- | --- |
| Build cost IC | 1 | 1.5 | 1 |
| Additive reliability | 0.15 | 0.15 | 0.15 |
| Breakthrough multiplier | absent | +0.05 | absent |
| Dismantle cost IC | 0.5 | 0.75 | 0.5 |

The CSV carries the revised conventional-turret row and operation metadata.
The validator checks that row against the script, the workbook against the old
values, and the revised turret against its explicit numeric contract. The only
cross-source exceptions are this turret's reviewed cost and breakthrough values.

## QA findings that are not transcription fixes

Gun-Launched ATGM III (`gl_atgm_2p`) has additive hard attack 95, soft attack 5.5
and piercing 600 in both script and workbook. Heavy ATGM values also remain
covered by the module balance report. Matching the source does not establish
that the finished vehicle is balanced; missile/gun interactions need live
calibration before we impose a new scale.

Radar II (`Radar_1`) has additive fuel use 1.2, supply-use multiplier -0.075,
air-attack multiplier +0.25 and reliability multiplier -0.05. These match the
workbook. The supplied screenshot shows supply use rounded to -0.0; that is not
a zero in the module definition. Actual application and tooltip precision need
live verification before changing the balance to address a display symptom.

## Remaining work and acceptance

The owner reports all four fresh bookmark/DLC combinations loaded, live stats
looked reasonable, and the NSB Finnish reward worked. That is acceptance evidence
for the pre-change branch. No new runtime pass is claimed for this batch.

Nationally named historical tank presets are still missing. The generic OOB
variants must be migrated together with their producer/name references; adding
T-54/T-55 display strings alone would not solve that contract. Generic bootstrap
clutter is separate from the export-only designs addressed here. The USA also
still uses its existing OOB setup; this batch fixes research, not its whole army.

Next implementation batch: calibrate complete tank recipes (including parent
and gun/ammunition behavior), establish named national presets, then build the
APC/IFV roles and their 18-envelope acceptance contract. Add amphibious modules
only together with marine equipment/sub-unit supply compatibility. Artillery/AA
gating and new night-vision/special-module balance follow in separate batches.
The owner has authorized judgment on these designs; no repeat approval of the
Section 8 choices is needed.

Recheck fresh 1949/1980 NSB and non-NSB campaigns, ahead-of-time penalties,
USA/SOV 1980 research, slot menus, conventional/light turret tradeoffs, and the
four export reward/license branches. Save/reload and the cosmetic brigade-model
fallback decision are not explicitly recorded as passed in the supplied notes.
