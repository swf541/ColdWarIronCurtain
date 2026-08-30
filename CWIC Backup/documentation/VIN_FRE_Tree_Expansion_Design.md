# VIN / FRE First Indochina War Focus Tree Expansion — Final Design Specification

Status: **FINAL TECHNICAL PASS v4, reviewed — implementation in progress.** Reviewed against the earlier planning drafts: the primary campaign / response package split, the FRE offensive-initiator vs defensive-holdout modes, and the reuse of the existing Struggle score instead of a new shared war-momentum resource all resolve open questions from the prior draft cleanly and are retained as-is. One design principle from the earlier draft (Section 1, principle 7) and two flags for afushin to sanity-check before implementation (Section 15) were added back in.

This document combines the historical/content plan with the current repository's technical constraints. It supersedes the earlier draft's secondhand assumptions about the VIN campaign and FRE operation systems. Exact Paradox script syntax, balance values outside the three existing VIN campaigns, and map province lists for new operations remain implementation-stage work.

**Game start date: late May 1949.** Events before that date are background and localization, not buildable operational focuses. Both trees begin in a war already in progress.

## 1. Scope and Design Goals

The rework covers:

- VIN's northern operational spine from the 1949-50 border fighting through Dien Bien Phu.
- FRE's command, defensive, offensive, pacification, and terminal branches for the same war.
- Outcome-driven cross-tree reactions.
- Replacement of Indochina's campaign-gated movement adjacencies with province-triggered overextension penalties.
- Repair and better integration of VIN's existing army-buildup and Southern Viet Minh branches.

It does **not** replace the existing Indochina Struggle score/phase system, Geneva Conference backend, VIN campaign-supply system, FRE War Credits/Metropole Patience systems, or the existing USA Operation Vulture focus. Those systems should be reused and extended.

The core principles are:

1. **Outcomes drive reactions.** A launched operation, a clean victory, a costly victory, and a failure are different facts and must not share one generic completion flag.
2. **Operations are real map commitments.** Named operations resolve from named geographic objectives and time limits, not arbitrary border-war results or mission-success arithmetic.
3. **One primary campaign owns peace.** Supporting operations and defensive reactions may run during it, but only the primary campaign resolver may transfer territory or white-peace the belligerents.
4. **Movement is discouraged, not prohibited.** Players may leave the historical operational area, but doing so produces escalating overextension penalties.
5. **The historical spine is the default, not an unavoidable rail.** Date failsafes and bypasses prevent a dead opponent or unusual AI path from locking either tree.
6. **Player knowledge should matter.** Historical mistakes remain the AI default, while informed players may choose a safer or more expensive alternative.
7. **Some of those "mistakes" should be live decisions, not just alt-history branches.** Carried over from the earlier draft: several currently-existing free-firing FRE events grant flat, disconnected bonuses/penalties instead of representing an actual historical decision point (dig in vs abandon a border post, commit reserves vs hold them, etc). Where one of these maps to a real historical call that turned out badly (Lorraine's overextended supply line, De Lattre overcommitting at Hoa Binh's tail end), rewrite it as a real choice inside the campaign/response-package framework rather than a standalone flat modifier. AI takes the historical option by default; a player who's run the tree before can knowingly pick differently. This doesn't need new mechanics, it needs the existing free-firing events threaded into the outcome-branch system in Section 7 instead of living outside it.

## 2. Current Backend Baseline

### 2.1 VIN campaigns

VIN already has a useful campaign wrapper in `VIN_Campaign_Effects.txt`. It is not a special engine-level limited war: it declares a normal `annex_everything` war, then imposes a scripted objective, clock, outcome, territorial settlement, and white peace.

The working pieces to retain are:

- campaign IDs and Campaign Supply;
- the guaranteed `on_daily_VIN` objective tick;
- clean, ground-out, abandoned, and failed outcome classes;
- control-based objectives rather than ownership checks;
- full-state transfer only after the scripted result;
- the 90-day inter-campaign cooldown;
- the FRA-hosted 300-day safety mission;
- campaign cleanup through one common finish effect.

The existing focuses in the root `common/national_focus/VIN_50s.txt` already call these effects for Northwest, Hoa Binh, and Dien Bien Phu. The 1949 Thap Van Dai Son and 1950 Cao-Bac focuses currently grant rewards and set cooldowns but do not run map campaigns; the rework may promote them into the same campaign framework.

### 2.2 FRE operations

FRE's present named-operation wrapper is scaffolding, not the target design. It:

- uses focus completion to activate a narrative event and selectable mission;
- selects preferred target **states**, but falls back to any adjacent VIN state;
- starts a one-province border war with `change_state_after_war = no`;
- treats winning that border war anywhere as success;
- resolves a stalled operation from commitment tier plus commander/GCMA/VNA values after 90 days.

The reusable parts are War Credits, commitment tiers, commander bonuses, GCMA, VNA coordination, Metropole Patience, spawned columns, cooldown gates, and the centralized finish concept. Generic target fallback and arithmetic-only outcomes must be replaced.

**Current implementation warning (2026-08-13):** this is still live, broken production content for `FRE_Operation_Hirondelle`, `FRE_Operation_Mouette`, and `FRE_Operation_Brochet`, not merely a historical description of code that has already been superseded. Each focus still opens a narrative event and selectable mission, then calls generic operation ID `2`, `3`, or `4`; `fre_operation_launch` attempts the obsolete one-province `start_border_war`, including its arbitrary adjacent-VIN fallback. These operations are not functional/accepted parts of the rework and must not be credited by campaign playtests. Their generic active, timer, result, cooldown, and cleanup state all remain in scope for the eventual conversion.

The neighboring `FRE_Prepare_for_the_Battle_of_Na_San`, `FRE_Prepare_for_the_Battle_of_Vinh_Yen`, and `FRE_Prepare_for_the_Battle_of_Mao_Khe` chains are a separate legacy problem: they do not launch that border war, but they still resolve selectable preparation missions from inventory/commander arithmetic and schedule disconnected battle events rather than reading live map outcomes. They, and any similar preparation focuses found during the audit, remain unconverted and unvalidated. This entry documents the debt only; it does not authorize treating focus completion as success or adding a quick border-war workaround.

### 2.3 Existing shared systems

Do not create a second war-momentum resource. The Indochina Struggle already records Communist, Pro-France, Pro-Independence, Pro-Ethnic, and Kuomintang scores on FRA scope and tracks escalation/de-escalation through `global.Indochina_War_Active_Phase` plus phase-point variables. Campaign outcomes should pay into that ledger through shared tiered effects.

Geneva is a shared backend process, not a single shared focus. FRE, VIN, the great powers, and the conference GUI already enter it through common flags/triggers. The rework should feed military outcomes into the existing Geneva recorder and leverage systems rather than create a parallel ending.

## 3. Unified Campaign Architecture

### 3.1 One primary campaign, optional response packages

Only one **primary theatre campaign** may be active at once. It owns:

- the war declaration, if one is required;
- the campaign ID and initiator;
- objective and operational-envelope data;
- clean and final deadlines;
- territorial transfer;
- outcome scoring;
- final white peace and cleanup.

A response such as Lorraine during the Northwest Campaign, Condor during Dien Bien Phu, or an FRE defensive commitment is a **response package attached to the primary campaign**. It may have its own subobjective and timer, alter supply, deadlines, units, or scoring, and record its own result. It must not independently white-peace the same war or transfer the primary objective.

This prevents two concurrent resolvers from ending each other's operation and leaving flags, missions, or national spirits stranded.

### 3.2 Required campaign lifecycle

Every primary campaign follows:

`available -> launched -> commitment selected -> active -> resolving -> finished`

Use distinct flags/variables for:

- launch or preparation;
- active campaign state;
- clean success;
- costly success;
- failure;
- voluntary/peace abort;
- theatre-superseded result;
- cooldown.

Cross-tree focuses read result flags, not merely `has_completed_focus` or a generic launched flag. Result flags are permanent historical facts; active and cooldown flags are transient state.

### 3.3 Daily resolution priority

The daily tick must evaluate an active primary campaign in this order:

1. If the objective is met, resolve clean or costly success according to the inclusive time boundary.
2. If the theatre has ended (`Indochina_War_Over`, Geneva concluded, or the active phase has left the live-war window), resolve as theatre-superseded and clean up without adding a fresh campaign victory.
3. If the final deadline has passed, resolve failure.
4. If all relevant campaign wars have been absent for more than the declaration grace period, resolve aborted.

The existing 14-day grace period is retained so a declaration has time to register. If a target tag disappears, objective control decides the result: VIN/FRE receives victory if it actually holds the objective; otherwise the campaign aborts.

### 3.4 Cleanup invariant

Every exit—including watchdogs, scripted peace, tag disappearance, Geneva, and CEFEO dissolution—must call the primary campaign's common finish effect. No event may merely clear an active flag.

The finish effect must:

- clear all active/resolving/response flags;
- set the correct outcome and cooldown flags;
- end only the wars opened or adopted by the campaign;
- remove campaign, defensive, AI-support, and overextension spirits;
- remove campaign missions and timers from every host scope;
- clear objective and siege modifiers;
- remove or stand down temporary formations;
- reset campaign, siege, hold-duration, and overextension variables;
- recalculate the shared Struggle ledger where needed.

The current `vin_campaign_watchdog` violates this rule: it assumes a border war and directly fires an old stand-down event after 150 days. It must be replaced later with a safety call into the same resolver. The 300-day FRA-hosted timer may remain as the ultimate backstop, but it must also use the common resolver.

## 4. Fixed VIN Victory and Termination Conditions

The following are final design decisions for the three already implemented VIN campaigns.

| Campaign | Primary victory condition | Clean success | Costly success | Failure |
|---|---|---:|---:|---:|
| Northwest / Tay Bac | VIN simultaneously controls provinces `10075`, `12075`, `13775`, `16526`, and `16527` | Objective by day 120 inclusive | Days 121-210 inclusive | Objective absent after day 210 |
| Hoa Binh | VIN controls province `10129`, the sole province of state `1766` | Objective by day 120 inclusive | Days 121-210 inclusive | Objective absent after day 210 |
| Dien Bien Phu | VIN controls camp province `4529`; the rest of state `671` is not the objective | Objective by day 150 inclusive | Days 151-260 inclusive | Objective absent after day 260 |

Success transfers ownership only during resolution:

- Northwest transfers state `1761` (Hoang Lien Son).
- Hoa Binh transfers state `1766`.
- Dien Bien Phu transfers state `671` (Tay Bac Bo).

The current `< 120` / `< 150` checks make the exact deadline day a costly result despite localization saying “within.” Implementation must use the inclusive boundaries above.

### 4.1 Northwest operational area

Victory remains the five-province strategic corridor, not full control of state `1761`. The normal operational envelope may include reachable Hoang Lien Son provinces:

`10075`, `12075`, `13773`, `13774`, `13775`, `16526`, `16527`.

Province `12319` remains outside the envelope because it is approached through MEO-held Ha Giang and is intentionally unnecessary to the corridor objective.

### 4.2 Hoa Binh operational area

The enemy-ground objective/envelope is province `10129`, with VIN's own direct approach provinces treated as home/rear-area ground. Moving into Hoang Lien Son, Tay Bac Bo, or the Red River Delta during this campaign is off-plan and may trigger overextension.

Historically this should become a two-stage campaign:

1. FRE initiates the seizure of Hoa Binh.
2. If FRE establishes the salient, the same primary campaign transitions to VIN's counteroffensive/CEFEO holdout phase.

Salan's Operation Amarante choice is a voluntary withdrawal result within phase two, not a second independent peace-owning campaign. Holding the salient is the costly player alternative.

### 4.3 Dien Bien Phu operational area and siege

The normal VIN envelope includes the reachable Hoang Lien Son corridor and all provinces of state `671`. Only `4529` grants victory.

The existing siege begins if VIN controls **any one** non-camp province in state `671`, which will be too permissive after movement restrictions are removed. The rework should require a meaningful investment condition—at minimum an eastern/northern approach plus one valley/ring province—before siege days accrue.

Fort degradation may retain the present fourteen-day steps and AI assistance, but AI assistance cannot bypass the primary objective. It may advance the siege or force an AI-held camp to fall only after the investment and supply conditions have genuinely been met.

## 5. Province-Triggered Overextension

The new system replaces campaign-gated land adjacencies. It does not change victory conditions.

### 5.1 Trigger model

Each active campaign supplies two province sets:

- its objective set;
- its wider permitted operational envelope.

At a throttled daily or weekly pulse, each principal side checks whether it controls enemy ground outside its active envelope. Home territory, allied starting territory, and rear-area transit ground must never trigger the penalty merely because it is controlled normally.

Recommended tiers:

- **In envelope:** no overextension penalty.
- **One operational band beyond the envelope:** ordinary overextension.
- **Deep/off-theatre penetration:** severe overextension.

The first implementation may use one tier if province-band maintenance is too expensive, but the trigger/data model should not prevent adding the severe tier later.

### 5.2 Behavioral requirements

- Apply the penalty to VIN/FRE, not as a blanket state penalty affecting both sides.
- FRE's crown-domain troops must follow the FRE-side result through a shared alignment trigger.
- Re-evaluate promptly when control changes; remove the spirit as soon as no forbidden enemy province is controlled.
- A campaign result must remove all overextension spirits even if the checker has not run again.
- Straying does not auto-fail an operation. It makes the ahistorical offensive increasingly difficult while the original objective and clock continue to decide the result.
- Province lists must live in shared scripted triggers/effects or arrays, not be duplicated between focus availability, victory, localization, AI, and overextension code.

### 5.3 Adjacency retirement

Remove only the artificial campaign movement limiters after the replacement triggers have passed map tests. Straits, canals, Laos-war boundaries, and unrelated special adjacencies are outside this work. The implementation audit must map every retired `INDOCHINESE_WAR_*` rule to either a normal map connection or a retained geopolitical restriction before deleting it.

## 6. FRE Operation and Defensive-Holdout Design

### 6.1 Offensive-initiator mode

FRE operations such as the opening seizure of Hoa Binh, an independent Lorraine divergence, and Castor may create a primary campaign when none exists. Their focuses should call the operation setup effect directly on completion. A narrative/commitment event may still open immediately, but the extra selectable-mission layer should be removed.

Success must be defined by an exact province objective, a hold duration where appropriate, and a deadline. Commitment tier and existing CEFEO systems should influence forces, supply, deadline flexibility, and available decisions—not substitute for controlling the objective.

Castor specifically succeeds by establishing and holding the airhead at province `4529`, not by winning a border war elsewhere in state `671` or `1761`.

### 6.2 Defensive-holdout mode

When VIN owns the primary campaign, FRE does not launch a second limited war. The relevant FRE focus unlocks a response package that can:

- select withdrawal, standard defense, or maximum commitment;
- deploy relief/garrison formations;
- fortify the named objective;
- change the attacker's clean/final deadline within bounded limits;
- impose or mitigate supply/overextension effects;
- record a defensive result when the primary campaign resolves.

This mode is appropriate for Nghia Lo/Na San, the later Hoa Binh phase, and Dien Bien Phu.

### 6.3 Existing operation targets to preserve conceptually

The current target-state choices remain useful historical routing hints, but later map design must replace them with exact province envelopes:

| Operation | Existing target geography | Reworked role |
|---|---|---|
| Lorraine | Ha Giang / Cao Bang | Northwest response package historically; optional independent deep raid on divergence |
| Hirondelle | Lang Son | Short raid/interdiction operation with a raid objective, not territorial annexation |
| Mouette | Thanh Hoa | Spoiling/pacification operation with temporary control or disruption objective |
| Brochet | Thanh Hoa / Hoa Binh | Pacification/clearing operation; exact historical province set required |
| Castor | Tay Bac Bo / Hoang Lien Son | Primary campaign to establish the `4529` airhead |

Camargue, Pollux, Atlante, and the other operations in the master list require new operation records rather than being squeezed into one of these IDs.

## 7. Cross-Tree Reactivity Contract

Use four levels of coupling:

1. **Hard response:** an explicit causal reaction, such as Northwest launching Lorraine. Unlock on the relevant `active` or `launched` fact, with a date/war-state fallback so the tree cannot deadlock.
2. **Outcome branch:** different effects or follow-up focuses for clean success, costly success, failure, or withdrawal.
3. **Soft callback:** Na San's result modifies Castor/hedgehog choices but is not required for the tree to continue.
4. **Localization-only callback:** descriptions acknowledge earlier events without changing mechanics.

Focus completion must never masquerade as battlefield victory. Use a consistent namespace, for example conceptually:

- `VIN_Campaign_Northwest_Active`
- `VIN_Campaign_Northwest_Result_Clean`
- `VIN_Campaign_Northwest_Result_Costly`
- `VIN_Campaign_Northwest_Result_Failure`
- `VIN_Campaign_Northwest_Result_Aborted`

Exact final names should follow existing project casing and avoid unnecessary migration of flags already consumed elsewhere.

All operation focuses need the same live-war window used by VIN campaigns: not `Indochina_War_Over`, not Geneva-concluded, and active phase below 9. A focus already in progress may finish, but its completion effect must refuse to launch a new campaign after the theatre closes.

## 8. Historical Operational Spine

The historical order and intended mechanical relationship are:

| Period | Primary action | Required reaction or consequence |
|---|---|---|
| 1949-50 | PRC victory opens VIN's supply corridor; Thap Van Dai Son / Cao-Bac / RC4 | Rebuild both sides' border campaign using the primary campaign framework |
| Jan 1951 | VIN general counteroffensive at Vinh Yen | FRE defensive package under De Lattre |
| Mar 1951 | Dong Trieu / Mao Khe | Follow-up fight affected by Vinh Yen result |
| May-Jun 1951 | Day River battles | Multi-objective defensive sequence; do not flatten into Vinh Yen |
| Oct 1951 | First Nghia Lo | FRE raid/offensive distinct from the 1952 battle |
| Nov 1951-Feb 1952 | FRE takes Hoa Binh; VIN counterattacks | Two-stage campaign; Amarante withdrawal or costly hold |
| Oct-Dec 1952 | VIN takes the Northwest corridor / second Nghia Lo | Lorraine response package; withdrawal toward Na San |
| Nov-Dec 1952 | Na San | FRE holdout; its result becomes a soft doctrinal input to Castor |
| Apr 1953 | VIN Upper Laos offensive | Existing Laos raid/alt outcomes remain the base; add downstream wiring |
| Mid-1953 | Hirondelle, Camargue, Mouette, Brochet, Pollux | FRE pacification/interdiction sub-branch with distinct objectives |
| Nov 1953 | Castor establishes Dien Bien Phu | FRE primary airhead campaign; success schedules the siege setup |
| Late 1953 | VIN moves on Lai Chau | Confirms or accelerates FRE's valley commitment |
| Mar-May 1954 | VIN besieges Dien Bien Phu | FRE holdout plus optional Vulture and Condor response packages |
| 1954 | Atlante in central Vietnam | Genuine strategic branch: central buildup versus northern reinforcement |
| Jul 1954 | Geneva | Existing shared conference/settlement backend consumes accumulated outcomes |

Pre-1949 events remain background. Operation focuses should normally cost the equivalent of 5-14 days; political, command, logistical, and army-reform focuses retain longer pacing. Date gates are guardrails, while causal result flags do the real sequencing.

## 9. Supporting Tree Rework

### 9.1 VIN army and command branches

Retain the existing focus set from `VIN_Issue_Ao` through `VIN_Plan_Large`, including `VIN_Mimic_French` versus `VIN_Maintain_Domestic_Weapon_Programs` and the `VIN_Implement_Vo` command branch. Convert flat bonuses into campaign inputs where appropriate:

- Campaign Supply generation or commitment prices;
- available commitment tiers;
- artillery/logistics formations;
- siege speed or consolidation time;
- overextension mitigation;
- AI strategy and historical option weights.

No focus should grant an automatic campaign win.

### 9.2 Southern Viet Minh branch

Preserve the existing Nguyen Binh event/focus structure. `VIN_Nguyen_Binh_Ambush` is intentionally unavailable and is force-completed by the dated `ic_pulse` event chain; its death/survival result is likewise force-completed. The rework task is therefore an audit of date, state-control, leader, and terminal focus gates—not a blanket conversion to northern campaign flags.

`VIN_Bac_Tien` currently waits for the Geneva-available trigger, while `VIN_Victory_in_the_South` waits for the communist-victory ending trigger. Test those intended mutually exclusive endings after northern outcome wiring changes. Use explicit northern result callbacks only where they create an actual southern consequence.

### 9.3 Named figures

Nguyen Binh remains the pattern for character-driven forks. Add a Charles Chanson/Sa Dec chain only after confirming character IDs, event ownership, and downstream Cochinchina consumers. Other figures should use the same event-result-to-focus pattern rather than inventing a new subsystem.

## 10. Alt-History Branches Retained for Content Design

### VIN

- Full commitment to Luang Prabang, with severe corridor-overextension risk.
- “South before North,” strengthening the Southern Viet Minh/Cochinchina struggle at the expense of Tonkin campaign capacity.
- Soviet patronage over primary Chinese patronage, changing equipment, doctrine, and diplomatic leverage.
- Negotiation from strength before Dien Bien Phu, producing an earlier and weaker Geneva-equivalent position.

### FRE

- Hold Hoa Binh instead of Amarante.
- Convert Lorraine from diversion into a sustained rear-area offensive.
- Reject Dien Bien Phu and expand a network of smaller hedgehogs.
- Vulture follow-up content around the already implemented USA focus.
- Condor arriving in time as a response package, not an automatic French victory.
- Prioritize Atlante over northern reinforcement.
- Build the Royal Lao and Cambodian armies instead of concentrating on the Vietnamese National Army.
- Charles Chanson survives Sa Dec, altering later pacification options.

These branches must change later choices, resource allocation, or settlement leverage; they are not renamed versions of the historical operation.

## 11. Geneva and Theatre-End Integration

- Continue writing Dien Bien Phu results into the existing Geneva outcome recorder.
- Campaign rewards use the existing Struggle score and phase effects; no direct ad hoc setting of a final Geneva outcome except through the established recorder.
- `FRE_Proclaim_Victory_in_Indochina`, `FRE_The_Geneva_Accords`, and `FRE_The_Fall_of_Saigon` remain score-and-ground-gated finales.
- The final campaign result must be committed before a same-day Geneva route reads it.
- Once Geneva concludes or `Indochina_War_Over` is set, every live campaign/operation is superseded and cleaned up, all launch focuses are bypassed or unavailable, and CEFEO wind-down may proceed.

## 12. Implementation Order

1. Audit the Indochina province graph and classify every existing campaign adjacency as remove, retain, or unrelated.
2. Harden the VIN state machine: inclusive deadlines, theatre-superseded outcome, unified cleanup, and corrected watchdog.
3. Add shared campaign objective/envelope data and province-triggered overextension checks.
4. Convert the three existing VIN campaigns without changing their fixed objectives.
5. Build the unified primary-campaign/response-package interface.
6. Rebuild FRE's five current operations on that interface; remove generic border-war fallback and selectable-mission indirection.
7. Add the earlier VIN/FRE battles and later new operations in historical order.
8. Wire result-driven focus reactions and AI plans.
9. Audit Southern Viet Minh and character event gates.
10. Run Geneva, dissolution, save/load, tag-disappearance, and ahistorical-path regression tests.
11. Only after tests pass, retire the obsolete movement adjacency rules and legacy outcome events.

## 13. Acceptance Criteria

The rework is not complete until all of the following pass for both human and AI participants:

- Every primary campaign produces exactly one terminal result.
- Exact clean/final boundary days resolve as documented.
- Capturing non-objective ground never grants victory.
- Capturing an objective after taking a deep ahistorical route still grants the correct timed result while overextension applies.
- White peace, Geneva, target annexation, CEFEO dissolution, and the safety timer leave no active flags, missions, temporary units, siege variables, or national spirits.
- A response package cannot independently terminate its parent campaign.
- FRE operations cannot fall back to an unrelated VIN border.
- The other tree reacts to launch/result flags without deadlocking if the expected opponent or prerequisite battle no longer exists.
- Overextension never fires from a side's ordinary home/allied territory and clears after withdrawal.
- Dien Bien Phu cannot be won by controlling state `671` while province `4529` remains in enemy hands.
- Castor cannot succeed without establishing the `4529` airhead.
- Geneva and all three FRE finale regions remain mutually exhaustive after the new score awards.
- Save/load during every campaign phase produces the same eventual result as uninterrupted play.

## 14. Implementation Source Map

The later implementation should begin from these current files rather than recreating their responsibilities elsewhere:

- `common/national_focus/VIN_50s.txt` — VIN focus entry points and the Southern Viet Minh branch.
- `common/national_focus/FRE_50s_Indochina.txt` — FRE operational, support, and finale focus layout.
- `common/scripted_triggers/VIN_indochina_campaign_triggers.txt` — current VIN gates and geographic objectives.
- `common/scripted_effects/VIN_Campaign_Effects.txt` — VIN commitment, daily resolution, transfers, siege, and cleanup.
- `common/scripted_triggers/FRE_operation_triggers.txt` and `common/scripted_effects/FRE_Operation_Effects.txt` — reusable FRE gates/resources plus the border-war logic to replace.
- `common/decisions/Indochina_War.txt` and `common/decisions/FRE.txt` — campaign safety timers and the selectable-operation missions to retire.
- `common/on_actions/CWIC_Struggle_on_actions.txt` and `common/on_actions/FRE_CEFEO_on_actions.txt` — guaranteed VIN daily and FRE weekly pulses.
- `common/ideas/VIN.txt`, `common/ideas/FRE_CEFEO.txt`, and `common/dynamic_modifiers/0_dynamic_modifiers.txt` — present campaign, overextension, objective, siege, and guerrilla modifiers.
- `map/adjacency_rules.txt` and `map/adjacencies.csv` — movement limiters to audit only after the replacement is working.
- `common/scripted_triggers/IC_struggle_triggers.txt`, `common/scripted_effects/CWIC_Geneva_Conference_Effects.txt`, and `common/scripted_triggers/FRE_Indochina_ending_triggers.txt` — shared Struggle/Geneva/finale interfaces.
- `events/VIN_Campaign_Events.txt`, `events/FRE_Operation_Events.txt`, `events/FRE_Events.txt`, and `events/SWF_Indochina_War_events.txt` — current result presentation and legacy outcome paths requiring consolidation.

## 15. Remaining Content Decisions

These require designer/map-owner judgment rather than backend invention:

- Exact province objectives and operational envelopes for every new battle beyond Northwest, Hoa Binh, and Dien Bien Phu.
- Balance values for ordinary/severe overextension and whether the first release needs both tiers.
- Hold durations for FRE airheads, fortified positions, and clearing operations.
- Which named engagements deserve independent primary campaigns versus response packages or event phases.
- Final focus names/layout and which existing placeholder nodes should be renamed, moved, or retained.
- VIN internal political/command factions used to frame the alt-history branches.
- **Worth confirming before implementation starts:** Section 9.2's diagnosis of the Southern Viet Minh branch is a real correction to how this was described earlier in planning — it says `VIN_Nguyen_Binh_Ambush` is intentionally unavailable and force-completed by a dated `ic_pulse` chain, not a broken reactive trigger. That changes the task from "fix the trigger wiring" to "audit date/state/leader/terminal gates," which is a smaller and different job than originally scoped. Worth a quick sanity check against actual in-game behavior before treating it as settled, since it reverses an earlier assumption.
- **Province and state IDs throughout Section 4** (`10075`, `12075`, `13775`, `16526`, `16527`, `10129`, `4529`, states `671`/`1766`/`1761`, etc) read as pulled directly from the repo, but this review had no access to the actual map/state files to cross-check them. Worth a quick verification pass against the live province map before they get locked into acceptance criteria, since several of those criteria (Section 13) hard-depend on exact IDs being correct.

## 16. Reference Checklist

Master operational checklist: Route Coloniale 4, Vinh Yen, Mao Khe, Day River, first Nghia Lo, Hoa Binh, second Nghia Lo, Lorraine, Na San, Bretagne, Adolphe, Upper Laos/Muong Khoua, Lower Laos and northeast Cambodia, Hirondelle, Camargue, Brochet, Mouette, Castor, Pollux, Atlante, Dak Doa, Dien Bien Phu, Vulture, Condor, Mang Yang Pass, and Chu Dreh Pass.

Existing tree landmarks:

- FRE: RC4/Revers Report/De Lattre/Vinh Yen; Na San/Lorraine/Mao Khe; Hirondelle/American financing/Brochet; Mouette/Castor; Final Push; mutually exclusive Victory/Geneva/Defeat finales.
- VIN northern: `VIN_Plan_Large`; `VIN_Thap_Van_Dai` and `VIN_Operation_Cao-Bac`; `VIN_Northwest` and `VIN_Liberate_Duyen`; `VIN_Prepare_Dien`.
- VIN army/command: `VIN_Issue_Ao`, `VIN_Chin_Tranh`, `VIN_Mass_Defectors`, `VIN_Sign_Sac_17`, `VIN_Implement_Vo`, and `VIN_Plan_Large`.
- VIN southern: `VIN_Nam_Bo_Khang_Chien`, the Nguyen Binh ambush/result fork, ideological leadership branches, and `VIN_Bac_Tien` / `VIN_Victory_in_the_South`.

## 17. Implementation Ledger

### Committed response checkpoint

- Patch set: Northwest/Operation Lorraine response content, the post-Dien Bien Phu southern-war response, the accepted campaign-front containment/local-supply follow-up, and the two-stage Hoa Binh/Operation Amarante response.
- Status: recorded by this checkpoint; targeted static verification passed. Campaign-front containment, repaired southern supply, MEO self-defense, Northwest balance, the Hoa Binh lifecycle, and Lorraine's historical response path have engine acceptance. The Amarante payoff/clarity follow-up still awaits its two choice-specific human CEFEO checks. The ordinary post-Dien Bien Phu route through NLF destruction and the existing peace gate now has engine acceptance.
- Base checkpoint: the checked-in VIN lifecycle, THO/Cao-Bac, adjacency, overextension, state-policy, theatre-AI, and local-supply patch described below and in `HANDOFF.md`.

### Working Dien Bien Phu response patch

- Status: code-complete on 2026-08-11; targeted static verification passed. A full historical-path engine run completed successfully on 2026-08-12. Alternate posture and forced-terminal coverage remains available through the supplied diagnostics.
- Scope: one defensive-response package attached to live VIN campaign ID `3`, with standard hold, maximum reinforcement, Operation Condor, and Operation Vulture postures. The parent campaign still exclusively owns the exact camp objective, permanent battlefield/Geneva recorder, transfer, peace, and common cleanup.
- The production fire site for the old delayed `FRE_DBP.1-.8` arithmetic result chain is retired. The legacy definitions remain gated for old saves and console compatibility; `FRE_DBP.10` is retained as the limited American-response event and now feeds the live package.

### Working exact-province Operation Castor patch

- Status: code-complete on 2026-08-11; targeted static verification passed. The combined historical-path engine run completed successfully on 2026-08-12; alternate commitment, broken-streak, deadline, and supersession terminals were not individually reported.
- Scope: the Castor focus now opens an immediate full/limited airborne commitment and a visible thirty-day establishment clock. Success requires French-aligned control of province `4529` for fourteen consecutive daily checks; broken control resets the streak. The focus and launch effects recheck the live theatre, Tai Federation, Viet Minh, and landing-ground gates before committing resources.
- Castor is preparatory. It establishes and fortifies the camp, deploys a commitment-scaled GONO garrison, and records one of success, failure, or theatre-superseded. It does not transfer territory, make peace, resolve VIN campaign ID `3`, or write the Dien Bien Phu/Geneva battlefield recorder.
- Generic operation ID `5`, the arbitrary adjacent-state fallback, the generic border war, arithmetic threshold result, generic outcome dispatch, and 150-day watchdog consumer are retired for Castor. IDs `1`-`4` remain for the still-unconverted operation wrapper.

### Working Operation Pollux patch

- Status: code-complete on 2026-08-12; targeted static verification passed. Engine acceptance is pending. Pollux is a preparatory evacuation attached to an established Dien Bien Phu camp, not a primary campaign or a restored generic border war.
- Scope: evacuate Lai Chau toward the camp before VIN campaign ID `3` begins. The exact overland corridor is Lai Chau province `13765`, the Route Pavie approach at province `13762`, and the Dien Bien Phu camp at province `4529`.
- The commitment choice distinguishes the historical split evacuation (regular battalions by air and exposed Tai partisan columns overland), an escorted Route Pavie withdrawal, and an expanded airlift. Historical AI accepts the split evacuation and its column-loss result; an informed player may spend more to preserve the formation.
- The escorted withdrawal must keep all three exact corridor provinces under French-aligned control for seven consecutive daily checks inside a twenty-one-day window. The expanded airlift needs seven consecutive days of French-aligned camp control and ignores the land corridor. Broken control resets the relevant streak.
- Permanent results are force preserved, column lost, or theatre-superseded. A preserved force adds one Pollux survivor group to the existing GONO camp formation and supplies it; the historical column-loss result preserves only the regular stores flown out under Operation Leda. Pollux owns no state or province transfer, peace, VIN campaign result, Dien Bien Phu/Geneva recorder, or primary-campaign cleanup.
- If campaign ID `3` begins before Pollux resolves, Pollux records the result earned by its current posture and map state only where its seven-day requirement has already been met; otherwise it closes as superseded without delaying or altering the primary campaign. Theatre ending, CEFEO dissolution, mission timeout, weekly orphan handling, and console diagnostics use the same dedicated finish/cleanup path.
- Static verification: `git diff --check`, raw Clausewitz brace balance across all changed/new gameplay `.txt`, and `python3 tools/loc_audit.py --check` pass. New Pollux effects, triggers, events, AI strategies, focus, mission, and English localization keys are unique. Pixel-map adjacency confirms the exact `13765 -> 13762 -> 4529` corridor. Targeted source checks confirm three commitment choices, objective-first seventh-day handling, exclusive permanent results, parent-campaign handoff, complete orphan/dissolution/theatre cleanup, and no territory, peace, generic-operation, primary-campaign, or Geneva mutation.

### Working Operation Atlante patch

- Status: code-complete on 2026-08-12 and merged into the Pollux external-playtest batch at the user's direction. Targeted static verification passes; engine acceptance is pending.
- Scope: a ten-day focus after Pollux opens a central-Vietnam strategic choice. The full CEFEO plan, a Vietnamese-led limited plan, and cancellation in favor of a northern reserve are mutually exclusive. Atlante is a named operational package, not a Pollux extension or a restored generic border war.
- The map abstraction is the existing NLF-owned state `1287`, representing the Interzone V base. Its adjacent exact objectives are provinces `4255` and `1300`. A full commitment must keep both under French-aligned control for fourteen consecutive daily checks inside a ninety-day window; the Vietnamese-led plan must keep province `4255` under State of Vietnam control for the same streak. Broken control resets the count.
- A full commitment spends 100 War Credits, 4,500 manpower, and 7 Metropole Patience, supplies the Vietnamese National Army, and directs both allied AIs toward state `1287`. It permanently records that the expeditionary reserve went south. When VIN campaign ID `3` opens, that choice removes maximum reinforcement and Operation Condor from the CEFEO response menu while retaining the scheduled defense and Operation Vulture.
- The Vietnamese-led plan spends 40 War Credits and 2 Patience, supplies Saigon, directs the Vietnamese National Army toward the coastal objective, and preserves the complete Dien Bien Phu response menu. Canceling Atlante spends 40 War Credits, 2,500 manpower, and 3 Patience to bank a northern reserve. At campaign ID `3` launch, that reserve supplies the existing camp garrison and delays scripted fort degradation by ten active-siege days without moving the fixed day-`150` or day-`260` deadlines.
- Permanent results are full central success, Vietnamese foothold, stalled offensive, northern priority, or theatre-superseded. Atlante transfers no state or province, declares or ends no war, writes no primary campaign/Geneva record, and cannot resolve Dien Bien Phu. Daily and timer-backstop resolution, weekly orphan handling, theatre/dissolution cleanup, exact objective AI, centralized localization, and console diagnostics are wired.
- Static verification: `git diff --check`, raw Clausewitz brace balance across all changed/new gameplay `.txt`, and `python3 tools/loc_audit.py --check` pass. New Atlante effects, triggers, events, focus/mission entries, AI strategies, diagnostics, and English localization keys are unique. Pixel-map verification confirms provinces `4255` and `1300` share a land boundary inside state `1287`. Targeted checks confirm three funded commitments plus the unfunded fallback, objective-first fourteenth-day handling, exclusive results, the pre-response northern handoff, complete orphan/dissolution/theatre cleanup, and ownership/peace/campaign/Geneva neutrality.

### Completed behavior

- `FRE_Operation_Lorraine` is no longer a selectable mission or standalone generic border war. It prepares a response package attached to VIN's live Northwest/Tay Bac primary campaign; the date fallback lets the FRE tree progress if Hanoi never launches that campaign, and a prepared plan is offered automatically if it launches later.
- Lorraine offers three live choices: the historical deep Clear River thrust, a shorter raid-and-withdraw option, or withholding the mobile groups for Na San. The deep thrust spends War Credits and Metropole Patience, disrupts VIN Campaign Supply and campaign time, applies bounded supply penalties, and uses a named Dong Bac Bo rear-area objective rather than an unrelated-border fallback. The shorter raid causes a smaller immediate disruption without opening a second front. The Na San choice supplies TAI and grants a campaign-only defensive spirit.
- The response records exactly one permanent result: strategic success, limited tactical raid, failure, forces withheld, or theatre-superseded. Its result combines the deep thrust's own seven-day rear-area hold with the parent Northwest result. It cannot transfer territory, make peace, or terminate the primary campaign.
- The VIN resolver commits Lorraine's response result before common Northwest cleanup. Normal resolution, direct cleanup, CEFEO dissolution, and theatre supersession remove all Lorraine/VIN/TAI response spirits and active posture flags. The legacy Lorraine operation watchdog and credit-reserve reader no longer consume the response package.
- FRE and VIN receive cross-tree Lorraine conclusion events. The AI receives narrowly scoped Dong Bac Bo raid/counter-raid orders only for the deep posture; the existing Northwest objective and reserve orders remain in force.
- Hoa Binh is now explicitly two-stage inside the existing map abstraction. TAM's control of state `1766` is the completed French seizure/established salient; VIN campaign ID `2` begins Giap's counteroffensive and immediately attaches the CEFEO phase-two response to that same parent campaign.
- The old `FRE_Battles.5` no longer free-fires 200-245 days after Mao Khe for flat ledger changes. It is raised once by the live Hoa Binh campaign and offers the historical Operation Amarante plan or a funded hold-the-salient alternative. Historical-focus AI is forced onto Amarante; nonhistorical AI uses an 80/20 withdrawal/hold split when the hold is affordable.
- Amarante spends 30 War Credits and commits 1,500 manpower to schedule the fighting withdrawal for campaign day `105`. If it executes while Hoa Binh remains French-held, the result returns that manpower, 2,000 infantry equipment, 250 support equipment, and 100 artillery equipment; grants 75 War Credits; adds 25 de-escalation points; preserves a `+10` Na San preparation callback; and directly waives the parent clean-result `-12` Metropole Patience shock. It never changes the clean Viet Minh battlefield/Struggle result, transfers Hoa Binh, or makes peace itself: the parent resolver remains the sole owner of transfer, TAM annexation, rewards, peace, and cleanup.
- Holding Hoa Binh requires 80 War Credits and commits 4,000 manpower up front, supplies TAM, and replaces the phase-one salient modifier with a bounded defender-only state-`1766` holdout modifier plus state-focused AI demand. A true hold is now only parent outcome `4`, meaning the salient survived the final day-`210` deadline; an absent-war abort is inconclusive and cannot collect the victory package. A successful hold adds 100 War Credits, 10 Patience, 3% War Support, and a 25-point two-sided Struggle swing in addition to the normal parent failure reward. A committed hold that loses adds a further 3,000 manpower, 1,500 infantry equipment, 150 support equipment, 75 artillery equipment, 75 War Credits, 8 Patience, and 4% War Support loss, plus 50 escalation and a 25-point two-sided Struggle swing toward the communists.
- Hoa Binh records one response result before common cleanup: orderly withdrawal, held, lost, inconclusive, or superseded. CEFEO dissolution, orphan checks, and every parent-campaign exit clear its temporary state modifiers, posture flags, and withdrawal request without granting the response ownership of the war.
- Mixed player/AI engine runs confirm consistent Hoa Binh passes and clean response/resolution behavior. The follow-up now presents the asymmetric contract explicitly: Amarante concedes Hoa Binh on day `105`, preserves the field force, offsets the French Patience loss, and continues the wider war; holding retains the objective, risks the force to day `210`, pays a larger success reward, and suffers an additional result-dependent loss package if broken. Neither route changes primary-campaign ownership.
- The scoped player-facing English audit replaced raw country-tag prose and exposed implementation language in the reworked campaign, Lorraine, southern-war, and legacy named-operation tooltips. Internal keys/scopes and variable expressions remain unchanged.
- A recorded communist capture of Dien Bien Phu now raises one VIN briefing even when the NLF is already defeated or absent. The visible strategy is a focus fork after `VIN_Prepare_Dien`, gated by the recorded fall, an idle VIN campaign system, and the absence of an announced, active, or concluded Geneva conference.
- The 14-day historical focus `VIN_Push_for_Negotiations` grants 25 Communist leverage, adds 150 de-escalation points, starts `Indochina_Geneva_Pursuit`, and owns a renamed queue latch. Its immediate and daily checks retain `geneva_conference_vietnam_at_peace_trigger`; only a divisionless NLF paper war may be repaired, and only after VIN is at peace. The existing delegation and `VIN_The_Geneva_Peace_Conference` systems remain authoritative.
- The mutually exclusive 34-day `VIN_Carry_the_Revolution_South` costs no political power or Campaign Supply. It reuses the old funded-NLF posture and exact support package when NLF exists, adds 25 Communist Struggle score and 50 escalation points, clears VIN-owned pursuit/queue state, and suppresses the panic-collapse Geneva route without disabling deliberate French, American, or other conference entry points.
- The escalation continuation consists of a 56-day mobilization and a 14-day general offensive. Mobilization grants a 180-day +10% planning speed, +5% organization, -5% supply consumption, and +2% reinforce-rate spirit plus VIE-front AI and northern reserve buffers. The terminal directly declares one `annex_everything` war on VIE if no war already exists; it never sets the 1960s `Vietnam_War` flag, explicitly calls FRE/FRA, or changes NLF independence/ownership.
- Save compatibility maps the old talks posture into the focus-owned queue, maps funded-NLF into the escalation posture, and clears a legacy autonomous queue without touching an externally owned Geneva pursuit. Diagnostics and AFK telemetry report strategy exclusivity, queue ownership, the peace gate, panic suppression, NLF independence, preparation cleanup, and the guarded invasion.
- Castor now spends its manpower, transports, War Credits, and Patience at the airborne commitment event rather than at a later generic-operation prompt. Full and limited drops create different garrison tiers; a successful fourteen-day establishment returns a bounded part of the commitment, while a failed thirty-day effort applies posture-scaled losses. A lost landing ground before the drop and an unfunded plan receive distinct non-deployment conclusions.
- The camp fortification helper now sets the intended bunker and anti-air levels instead of repeatedly stacking construction. The siege state modifier is added only when VIN campaign ID `3` is actually live, so Castor can establish the pre-siege position without starting the siege months early.
- Castor's daily pulse, visible timer backstop, weekly orphan check, CEFEO dissolution, Struggle ending, and fallback dispatcher all share the dedicated result/cleanup state. If VIN campaign ID `3` begins before establishment completes, a handoff closes Castor as superseded while preserving its already-deployed garrison for the parent siege. Console helpers start, advance, fail, inspect, and reset the airhead lifecycle without routing through the generic operation wrapper.
- Live Dien Bien Phu campaign ID `3` now raises one CEFEO defensive choice. Standard hold commits manpower and accepts the scheduled airlift; maximum reinforcement spends War Credits, manpower, and Metropole Patience to strengthen the camp and delay siege degradation by fourteen active-siege days without changing the fixed campaign deadlines.
- Operation Condor becomes a map result rather than an advance bonus. It arms only after the Viet Minh satisfy the existing approach-plus-ring investment prerequisite, then requires French-aligned control of the camp, one northern/eastern approach, and one ring position for seven consecutive daily ticks. Opening the corridor relieves fourteen siege days and records force preservation, but the best response payoff still requires the camp to survive the parent day-`260` deadline.
- The Vulture posture spends War Credits and Patience to ask Washington for limited air support through the retained `FRE_DBP.10` event. Approval supplies the defenders, adds a bounded state modifier, and relieves ten siege days; refusal grants no battlefield aid. Completing `USA_50s_Operation_Vulture` during the campaign feeds the same support hook and retains its existing direct-intervention wars and diplomatic costs.
- Every posture pays its best reward only from parent outcome `4`, records a fall only from the parent's clean/costly camp capture, and treats an absent-war abort as inconclusive. Maximum commitment, failed Condor, and the Vulture route have distinct loss packages and conclusion prose; supersession is rewardless.
- The response resolves before `vin_dbp_record_outcome`, owns no state transfer, annexation, province-control mutation, white peace, campaign resolver call, or Geneva announcement, and is removed by parent cleanup, weekly orphan handling, CEFEO dissolution, or theatre supersession. State-scoped posture modifiers and CEFEO/TAI AI plans are limited to Tay Bac Bo.
- New `test_fre_dbp_response_status`, `test_fre_dbp_response_daily_check`, and `test_fre_dbp_response_reset` effects report and reset the response without changing the parent campaign, map, or Geneva recorder.
- Design review completed and canonical document selected.
- Existing VIN campaign wrapper, CEFEO custody, THO autonomy-zone chain, map ownership, startup OOB, focus, failsafe, Struggle, GCMA, and dissolution integration audited before edits.
- The common resolver now classifies clean, costly, aborted, failure, and superseded outcomes in the contractual order; clean/final deadline days are inclusive, the 300-day backstop checks the live objective and theatre first, and elapsed days survive cleanup for delayed localization.
- Every resolved primary campaign records one permanent result flag. Supersession performs cleanup without territorial transfer, Struggle movement, War Credits, Metropole Patience, or Dien Bien Phu/Geneva battlefield recording.
- The legacy VIN campaign watchdog now calls the common resolver instead of treating the absence of a border war as failure. Ending cleanup supersedes any live campaign before the theatre is dismantled.
- THO now begins alive as a neutral, French-aligned territorial council in Cao Bang and Lang Son, under FRE crown-domain custody with the existing non-Together-for-Victory puppet fallback. It begins with two small territorial battalions; VIN begins in Dong Bac Bo.
- The three early VIN economic focuses and the Hanoi asset-relocation focus now select a VIN-owned Cao Bang or Dong Bac Bo scope and never construct in or strip THO-owned territory.
- `VIN_Operation_Cao-Bac` now launches campaign ID 4 against THO. Its objective is simultaneous control of every province in Cao Bang and Lang Son; successful resolution transfers both states, removes THO without transferring its units, and unlocks air-base raids. Abort, failure, and supersession leave or restore surviving THO to French command.
- Existing CEFEO access, GCMA, Struggle, ending failsafe, dissolution handback, and postwar communist THO restoration paths remain connected. A surviving colonial THO blocks the communist re-release; a previously annexed THO can still be restored under VIN with Chu Van Tan.
- VIN and FRE AI strategies now recognize the Cao-Bac front, including targeted CEFEO defense of the two THO states while the campaign is active.
- Reusable console effects cover startup, status, deadline boundaries, abort, supersession, cleanup, result invariants, and save/load checkpoints.
- Fifty-seven northern/campaign adjacency assignments are now unrestricted land connections. Thirty-five Laos-war and theatre-divider assignments remain gated, including the two Dien Bien-to-Laos crossings; the four internal Dien Bien camp approaches are unrestricted.
- Shared geography triggers now distinguish each VIN operational envelope, previously captured VIN home territory, starting bridgeheads, the Northwest outlier, and French-aligned penetration into VIN rear areas. A daily one-tier overextension penalty applies and clears from VIN or the entire FRE/VIE/crown-domain side as control changes; Nghe-Tinh is now correctly included as VIN rear ground.
- Campaign cleanup removes overextension and campaign-command spirits before any target annexation, during normal finish, during Struggle ending cleanup, and from FRE during CEFEO dissolution.
- The Dien Bien siege now requires an eastern/northern approach plus a separate valley-ring province before siege days accrue. AI assistance can finish an established siege but cannot invent the investment.
- The first balance pass removes the blanket French combat penalty, reduces VIN campaign mobilization to a moderate logistics benefit, reduces the objective-state defense penalty from 80% to 25%, removes the generic VIN AI push into the FRE delta, and adds targeted CEFEO defense for Tay Bac, Hoa Binh, and Dien Bien Phu.
- Campaign state policy is now explicit and self-healing. Cao-Bac opens only `1280`/`1768`; Northwest opens `1761`; Hoa Binh opens `1761`/`1766`; Dien Bien opens `1761`/`671`. The nine northern states damaged by the old broad cleanup are rebuilt before the operation is applied each day, while the full Indochina `unplanned_offensive` baseline is rebuilt at launch and resolution.
- Temporary planned offensives no longer clear `VIN_unplanned_offensive_flag`. Cleanup restores the baseline after clean, costly, aborted, failed, or superseded resolution; theatre-ending cleanup still removes it normally.
- Hoa Binh now treats Hoang Lien Son as a contested approach as well as Hoa Binh itself. Tay Bac Bo remains protected during Hoa Binh and becomes planned only for Dien Bien Phu.
- VIN-controlled Thanh Hoa, Nghe-Tinh, and Quang Binh receive a campaign-only local-supply modifier representing dispersed caches and porter relays. The first implementation failed to attach in engine; the repaired helper evaluates control from state scope, applies an explicit indefinite modifier, forces its refresh, and raises its bounded local supply from `0.25` to `0.50`.
- VIN's broad tag-front wartime strategy now aborts while a named campaign is active. Campaign strategies retain reserves across Dong Bac Bo and all three southern-base states, apply strong negative requests to VIE/NUN and non-objective FRE/crown-domain fronts, and reduce the stacked global `ignore_army_incompetence` value from `300` to `50`.
- FRE, VIE, THO, TAI, TAM, and NUN now suppress requests into VIN's rear areas and receive state-scoped rather than tag-wide campaign plans. Those plans may counterattack within their assigned state; they do not authorize general pursuit. Deep Lorraine remains the only scripted Dong Bac Bo offensive exception.
- MEO has a self-defense-only Ha Giang plan with no corresponding VIN deployment request. Its own divisions are ordered to remain in state `1767`, avoid allied-border diversion, and satisfy local front demand. TAI still begins with a fourth battalion at Dien Bien Phu.
- VIE's historical NUN event may still update NUN's nationalist identity, politics, and leadership, but its autonomy transfer has been removed. NUN therefore remains under CEFEO custody and in the northern war instead of silently becoming a VIE subject.
- New diagnostics report current planned/protected states, missing rear-area supply, and post-campaign restoration failures.

### Deferred work

- Human CEFEO engine acceptance of the revised Hoa Binh contract: one Amarante execution and one day-210 hold/lost-salient wager test.
- A severe/deep overextension tier; the first replacement patch intentionally ships one tier on geography helpers that can support a second.
- Alternate-terminal and balance coverage for the new Dien Bien Phu response package plus exact-province Castor; their full historical path has engine acceptance. Remaining FRE operations and supporting narrative content remain deferred.
- A post-failure recovery route from an unsuccessful Northwest campaign into Dien Bien Phu. The present focus still requires ownership of `1761`; this patch repairs the false failures caused by lost modifiers/supply but does not turn a genuine Northwest defeat into a free valley campaign.
- Extended engine coverage of the implemented northern/southern French Indochina command interface, especially old-save migration, intentional defection exits, and CEFEO dissolution ordering. Core faction membership and separate-war behavior passed the initial playtest on 2026-08-13.
- Deletion of the now-unassigned legacy northern adjacency-rule definitions after the unrestricted connections pass an engine map test. Their CSV assignments are already retired, so they no longer affect movement.
- Named colonial THO leadership research; the restoration patch uses a generic territorial council.

### French Indochina command implementation

- French Indochina is implemented as a fixed CEFEO-led faction rather than the old VIE-led State of Vietnam faction. Its members are CEFEO, State of Vietnam, Cochinchina, the Montagnard crown domain, Tai Federation, Nung territory, Muong Federation, and Tho territory. France remains outside both the faction and the CEFEO subject chain.
- The faction owns a hidden no-call rule and a hidden no-leadership-change rule. This makes it a coordination/access wrapper instead of a war-merger: CEFEO enters attacks on its northern crown-domain subjects, VIE and its southern subjects fight the southern Viet Minh, and neither command can summon the other through ordinary faction diplomacy.
- Hanoi's Viet Minh faction contains NLF at startup, restoring the original diplomatic relationship after engine feedback rejected the temporary separation model. `VIN_NLF_Coordination_Channel` and `NLF_Hanoi_Coordination` remain the scripted political/logistical interface. Membership must not make VIE and VIN direct belligerents.
- The four northern crown domains remain CEFEO subjects with `autonomy_crown_domain`; Cochinchina and FUL remain VIE subjects. Crown domains may join their CEFEO overlord's closed faction, while the faction call rule prevents their membership from broadening a war.
- VIE's Pau and Matignon focuses no longer touch Nung custody or display fictitious autonomy changes. Live pro-French VIE coup routes retain their political-status spirits without becoming direct French subjects. The French communist-collapse event likewise keeps CEFEO independent and preserves VIE's southern custody chain.
- The VIE Nung settlement decision cannot run while CEFEO custody/the war remains live. The historical `NUN_Unification.2.a` political/leadership result still owns no autonomy transfer. Nung communist and independence routes, FUL independence, CCC rupture, and the existing FUL-to-France branch now leave/remove the appropriate command identity explicitly.
- CEFEO dissolution dismantles French Indochina before crown-domain handback and before FRE annexation, preventing unintended faction succession. General Struggle cleanup also removes the new command identity as a final leak guard.
- The French-command initializer remains one-shot so save reloads do not undo intentional local defections. It retires the old Saigon faction; a narrow startup sync outside that one-shot block restores NLF to VIN only during the live Indochina theatre when both coordination flags still exist, repairing saves made by the temporary separation model. Intentional later generic VIE factions remain untouched.
- The French Indochina and Viet Minh faction templates both use the hidden no-call rule. `French_Indochina_Faction`, `State_of_Vietnam_Faction`, and `Viet_Minh_Faction` give AI `-1000` ally-get/call/join desire and allow call refusal, matching the existing State of Vietnam protectorate safeguard. The 1953 Laos raid applies the same isolation policy to the Kingdom of Laos before its declarations rather than after them.
- `test_indochina_command_status` checks faction leadership/membership, northern and southern custody, VIE-VIN non-belligerence, VIN-NLF membership, the VIE-NLF base war, and NLF-CEFEO leakage. `test_indochina_command_repair` rebuilds only an early setup damaged for testing or loaded from a legacy save.

### Dien Bien Phu defensive-response implementation

- The first implementation is complete. It preserves the existing siege investment, exact camp objective, day-`150` clean boundary, day-`260` final boundary, and Geneva recorder while replacing the production use of the delayed arithmetic-only final-assault chain.
- The same working patch now includes exact-province Castor so one external save can test airhead establishment and the later defense in sequence.
- Historical-path engine acceptance is complete. Remaining branch coverage should use the diagnostics for Castor's alternate commitment, broken-streak reset, deadline failure, and supersession; the alternate defensive postures; parent failure/hold and clean/costly camp fall; absent-war abort and supersession; Condor's investment-and-seven-day corridor gate; and limited/direct Vulture outcomes.
- Do not tune the accepted VIN objective or primary lifecycle from a response-package result alone. Tune posture costs, state modifiers, relief days, and AI demand first.

### Changed systems

- French Indochina faction template/rules, faction-status UI, CEFEO startup/dissolution, VIE/VIN/NLF histories, VIE diplomacy/events/decisions, Nung and FUL exit paths, centralized faction/VIE localization, and command diagnostics.
- FRE Northwest focus behavior, Lorraine response effects/triggers/events, response ideas, targeted AI, legacy-operation mission/watchdog isolation, and CEFEO cleanup.
- Exact-province Castor focus/event/effect/mission behavior, its state modifier and GONO tiers, generic-operation ID-`5` retirement, fallback integration, cleanup, localization, and diagnostics.
- FRE Hoa Binh response effects/events, the repurposed Meat Grinder choice, Operation Amarante's parent-resolver request, defender-only state modifiers/AI, conclusion events, localization, cleanup, and diagnostics.
- VIN Northwest launch/resolution callbacks, post-Dien Bien Phu southern-war triggers/effects/events/decisions, NLF support spirit, Geneva-pursuit integration, and diagnostics.
- Canonical design documentation and implementation ledger.
- VIN campaign scripted triggers, effects, clock/backstop decisions, result events, scripted localization, result localization, and failsafe coverage.
- VIN northern focus behavior, early economic state targeting, and Hanoi asset relocation.
- THO/VIN country history, Cao Bang/Lang Son ownership, THO and VIN starting OOBs, and colonial/communist THO lifecycle helpers.
- Indochina Struggle ending cleanup and VIN/FRE theatre AI strategies.
- FRE, Viet Bac, and VIN campaign test effects.
- Indochina adjacency assignments, VIN/FRE campaign and overextension ideas, contested-objective balance, CEFEO dissolution cleanup, and route/overextension test diagnostics.
- Campaign state-modifier lifecycle, Thanh Hoa/Nghe-Tinh/Quang Binh local supply, VIN/FRE/VIE/crown-domain/MEO theatre AI, the TAI starting OOB, and the NUN unification event's custody-preserving behavior.

### Verification

- 2026-08-13 faction-isolation follow-up: `git diff --check`, Clausewitz structure checks for the touched gameplay files, and `python3 tools/loc_audit.py --check` pass. Targeted source checks confirm NLF is added by VIN history and restored for live-theatre saves initialized by the separation model; both local faction templates own the hidden no-call rule; all three faction identities carry `-1000` AI ally-get/call/join desire and call-refusal permission; and the Kingdom of Laos receives its matching safeguard before the event's declarations. The user's initial engine playtest confirmed that the faction rework functions correctly; longer-run migration, defection, dissolution, and Laos edge branches remain useful coverage.
- 2026-08-12 initial French Indochina command static verification (partly superseded): the original checks passed, including the now-rejected NLF-separation invariant. The CEFEO leadership/custody/dissolution findings remain valid, but the 2026-08-13 faction-isolation follow-up replaces its NLF membership and call-policy conclusions.
- 2026-08-12 combined engine acceptance: a full player/AI run completed without a reported lifecycle regression. Player-controlled Operation Lorraine reached its proper terminal, defended the intended state, and produced the proper response outcome. Historical AI followed the historical campaign outcome through Dien Bien Phu. After the NLF was destroyed, the ordinary Hanoi/Saigon peace gate passed and the Geneva Conference convened in the historical post-Dien Bien Phu sequence. This accepts Lorraine's historical response path, the combined patch's historical campaign path, and the dead-NLF automatic-Geneva terminal; unreported alternate posture/forced-terminal branches remain diagnostic coverage rather than blockers to the checkpoint.
- 2026-08-11 exact-province Castor static verification: `git diff --check`, raw Clausewitz brace balance across every changed/new gameplay `.txt`, and `python3 tools/loc_audit.py --check` pass. The new Castor effects and state modifier are unique; no generic operation ID `5` or current-operation-`5` consumer remains; the dedicated effect contains no ownership transfer, province-controller mutation, peace, annexation, primary-campaign resolution, or Geneva-result mutation. Targeted checks confirm exact province `4529`, fourteen consecutive hold days, the thirty-day visible timer/backstop, full/limited/up-front costs, objective-first daily resolution, one-of-three permanent results, generic watchdog isolation, weekly/dissolution/theatre cleanup, and a fallback wait only while Castor is unresolved. The combined historical-path run was accepted on 2026-08-12.
- 2026-08-11 Dien Bien Phu response static verification: `git diff --check`, raw Clausewitz brace balance, and `python3 tools/loc_audit.py --check` pass. New response effects, triggers, events, modifiers, AI strategies, and English localization keys are unique in their namespaces. Targeted source checks confirm four live postures, Condor's prior-investment plus seven-day exact-province requirement, both limited and direct Vulture hooks, parent-before-recorder result ordering, fixed day-`150`/`260` deadlines, result-gated payouts, and response ownership neutrality. Parent finish, weekly orphan handling, CEFEO dissolution, and theatre supersession all reach response cleanup. The combined historical-path run was accepted on 2026-08-12.

- Historical baseline, superseded by the focus fork: the 2026-08-11 autonomous post-DBP closure repair passed static verification and its ordinary destroyed-NLF route received engine acceptance on 2026-08-12. Preserve that result only as regression evidence for the shared Vietnamese peace gate and conference backend; the new focus-owned queue and escalation branch require their own checkpoint coverage.
- 2026-08-10 Hoa Binh response static verification: `git diff --check` passed; all edited/new gameplay files have balanced raw braces; new effects, events, AI strategies, state modifiers, and English localization keys are unique; the two legacy delayed `FRE_Battles.5` calls are absent; the sole remaining call is owned by the live response; Amarante contains no transfer, peace, annexation, or direct resolver call; objective capture and theatre supersession precede its request in the primary classifier; and normal finish plus CEFEO dissolution clear the package.
- 2026-08-10 Hoa Binh payoff/clarity follow-up static verification: `git diff --check` and targeted raw-brace checks pass; the three new result-payoff effects and four new/changed response localization keys are unique; a successful hold requires parent outcome `4`; the committed-hold loss package is gated by the hold posture; Amarante still owns no transfer, annexation, peace, or campaign resolution; its permanent withdrawal result alone suppresses the Hoa Binh clean-result Patience loss; the Na San callback appears once in the preparation mission; and the scoped localization audit finds no raw `VIN`/`FRE`/`VIE`/`NUN`/`TAI`/`TAM`/`THO`/`MEO`/`NLF` prose, province/state IDs, border-war language, or primary-resolver language in the audited values. Engine acceptance is pending.
- 2026-08-10 Hoa Binh engine acceptance: repeated mixed player/AI runs produced more consistent passes for both CEFEO and the Viet Minh, with no reported response, campaign-resolution, or cleanup failure. Acceptance exposed one UX/balance failure: a player who held Hoa Binh through day `105` received too little benefit from Amarante and could reasonably interpret the scripted withdrawal as losing a war they had been winning.
- 2026-08-10 external campaign-front acceptance: repeated Northwest runs confirmed the repaired southern supply modifier appears and works, MEO defends or recovers Ha Giang, historical AI can follow the intended campaign result, and a capable player-led side can still dominate. The containment/local-supply follow-up is accepted for continuing content work.

- 2026-08-10 campaign-containment/supply follow-up: `git diff --check` passed; raw Clausewitz braces balance across every modified/new gameplay `.txt`; all new AI/helper definitions are unique; VIN has one reduced campaign-wide `ignore_army_incompetence` strategy and no Ha Giang unit request; FRE has no remaining tag-wide VIN campaign front; the supply helper covers `1762`/`1763`/`838`; VIE participates in rear-area overextension application/cleanup; and no adjacency file changed. Engine acceptance remains pending.
- 2026-08-09 Northwest/Lorraine and post-DBP southern follow-up static verification: `git diff --check` passed; raw Clausewitz braces balance in every modified/new gameplay `.txt` file; all new English localization keys are unique; Lorraine has no selectable-mission or focus call into legacy operation ID 1; response result/cleanup hooks, southern response exclusivity, and Geneva peace-gate preservation passed targeted source invariants. Engine acceptance remains pending.
- `git diff --check`: passed.
- Raw Clausewitz brace balance: passed for all 21 changed/new `.txt` gameplay files.
- Targeted static invariants: passed for starting ownership/capitals, two-unit THO OOB, the single TAM declaration path, Cao-Bac active/cooldown/deadline wiring, five exclusive Cao-Bac result names, focus launch behavior, and localization key presence.
- The repository's broad style checker reports pre-existing space-indentation findings in these legacy files; inspection of added diff lines found no new four-space indentation.
- In-game verification for the lifecycle/THO patch: a full human VIN game completed on 2026-08-08. Campaign lifecycle and THO restoration otherwise behaved smoothly.
- Adjacency/overextension patch static verification: `git diff --check` passed; every modified/untracked gameplay `.txt` file has balanced raw Clausewitz braces; every operative adjacency row retains ten fields; exactly 57 campaign routes are unrestricted, 35 Laos/divider routes remain assigned, and no retired northern rule name remains assigned in the CSV.
- New overextension idea/localization uniqueness and update/cleanup call sites passed targeted checks. Engine route access and balance remain pending.
- 2026-08-09 follow-up static verification: `git diff --check` passed; every modified/untracked gameplay `.txt` file has balanced raw braces; the obsolete broad-clear effect and all tag-wide TAI conquer orders are absent; the new modifier/localization/test effects are unique; TAI has exactly four starting battalions; and NUN's historical event contains no autonomy transfer to VIE.

### 2026-08-08 playtest findings

- Artificial campaign adjacency rules blocked valid routes into THO and Dien Bien Phu objectives. Both campaigns became mechanically unwinnable without console intervention because divisions could not enter required provinces.
- Human VIN was too strong in direct fighting and could push CEFEO and its crown domains with little difficulty. The next balance pass must remove the always-on French combat penalty, reduce VIN's broad campaign buffs and the objective-state defense debuff, and replace hard movement fences with conditional overextension pressure.
- Adjacency access and combat balance are failures for the current acceptance run; campaign resolution, results, ownership transitions, and surrounding Patch 1-2 integration passed the reported full-game smoke test.

### 2026-08-09 playtest findings

- Campaign launch removed `unplanned_offensive` not only from the named operation but also from Dong Bac Bo, Thanh Hoa, Hanoi/Tonkin, Hoa Binh, and the Tai exterior. It also cleared `VIN_unplanned_offensive_flag`, so campaign cleanup had no persistent marker from which to rebuild the original front. Later campaigns therefore inherited the damage.
- Cao-Bac was mechanically correct but too easy for a human (roughly two weeks). The AI did the opposite of the intended operation: while the subject war exposed the wider CEFEO front, tag-wide concentration let it occupy most of TAI and penetrate Hanoi/Tonkin before completing the THO objective.
- Hoa Binh needs Hoang Lien Son (`1761`) inside the planned/contested approach, while Tay Bac Bo (`671`) remains an unplanned exterior position. The latter should be strongly defended but not permanently impossible once a later campaign explicitly selects it.
- VIN's Thanh Hoa and southern forces collapse when cut off from the Dong Bac capital by French-held Tonkin. The fix should model dispersed local supply rather than create a railway or supply path through hostile territory.
- Northwest exposed the same modifier and supply failures: VIN could wander through TAI yet lose Hoa Binh and the southern base, fail the Hoang Lien objective, and deadlock the Dien Bien focus gate.
- NUN's 1950 VIE puppet decision can override its CEFEO crown-domain custody and remove it from northern wars. This belongs to the northern/southern command-interface repair, but the immediate wartime override must be prevented.

### 2026-08-09 follow-up playtest findings

- The revised first three campaigns completed smoothly in a human VIN run. The adjacency retirement restored practical access to the objectives; no console movement was required.
- VIN had difficulty holding its positions during Dien Bien Phu, but still captured TAI and the valley within the campaign deadline. This is useful defensive pressure rather than the earlier hard movement failure; further tuning should wait for an AI sample and comparative loss/time data.
- Dien Bien Phu did not immediately produce Geneva because the NLF was still alive and VIE remained at war. This is the intended result of `geneva_conference_vietnam_at_peace_trigger`, not a campaign-result regression. Once both Vietnamese conference parties are at peace, the existing daily Geneva path can consume the recorded DBP outcome.
- NUN's autonomy transfer to VIE was removed from `NUN_Unification.2.a`. The event can still update its politics and leadership, but NUN remains under CEFEO custody as intended for the current command model.

### 2026-08-10 playtest findings

- Historical AI completed the entire campaign sequence and reached the historical Geneva outcome, confirming the objective/resolver spine is robust without restored northern adjacency gates.
- That success concealed excessive general-war movement. During Cao-Bac VIN overran THO but fought deeply through TAI/FRE before recovering two CEFEO-held objective provinces; during Hoa Binh CEFEO penetrated VIN rear areas while the southern base collapsed; during Northwest TAI and MEO were overrun and Hoa Binh changed hands. The next correction must shape front assignment rather than strengthen the already severe `unplanned_offensive` penalty.
- Dispersed Base-Area Supply did not appear beside `unplanned_offensive` in its intended states and provided no observed benefit. Nghe-Tinh, which contains two significant starting VIN formations, was also absent from the original two-state implementation.
- MEO repeatedly left its one-state territory insufficiently defended and capitulated. The chosen fix is MEO self-defense only; VIN is not asked to station forces in Ha Giang.
- A human FRE player defeated the Northwest campaign on its clock while penetrating VIN's interior and taking its northern capital, although encircled Hoa Binh resisted. This establishes that a French campaign victory is achievable and that complete VIN capitulation is not the correct balance target.
- Two AI games have produced VIN Northwest success. Dien Bien Phu remains unchanged pending a larger sample; no adjacency restoration or new combat-stat wall is justified by the current evidence.
- After the containment repair, multiple additional Northwest runs confirmed working southern supply, MEO self-defense/recovery, intended historical-AI results, and player freedom to outperform the script. This closes the containment/local-supply acceptance item.

### 2026-08-10 Hoa Binh response playtest findings

- Mixed player/AI control now produces consistent Hoa Binh passes for both CEFEO and the Viet Minh. The two-stage response, state modifiers, campaign result, and cleanup are mechanically accepted.
- Operation Amarante is not yet a worthwhile player choice. A CEFEO player can control and successfully defend Hoa Binh for the full 105-day withdrawal period, then automatically concede it while receiving too little force-preservation or future-operation value in return.
- A player unfamiliar with the First Indochina War can interpret that outcome as an unexplained loss of the wider war rather than a deliberate withdrawal from one costly salient. The selection tooltip must state the concession, timing, preserved force, continued wider war, and downstream benefit before selection.
- Holding must be framed as the opposite wager: retain Hoa Binh and gain a meaningful result if the Viet Minh offensive expires, but suffer materially worse result-dependent consequences if the position falls. Move appropriate rewards and penalties from selection time to response resolution.
- Player-facing prose should never show raw tags such as VIN, FRE, VIE, NUN, TAI, TAM, THO, or MEO when an in-world name is available. This does not prohibit tag-based localization keys, scope syntax, or variable expressions which the engine resolves before display.
- All localization `.yml` files are required to use UTF-8 with BOM (`EF BB BF`). Plain UTF-8 localization may not appear in game even when its YAML and keys pass the localization audit. Preserve the BOM on edits, add it to every newly created localization file, and verify the first three bytes as part of static handoff checks. The user repaired the files affected by the recent non-BOM edits.

### Known issues

- **2026-08-13 resolved faction-propagation finding:** the first CEFEO-faction run pulled the State of Vietnam and other uninvolved French Indochina/Viet Minh faction members into VIN's scripted campaigns and the 1953 Pathet Lao invasion. VIE later left through campaign white peace, but its temporary participation was still incorrect. The follow-up restored NLF to VIN's faction and added hidden no-call rules, call-refusal permission, `-1000` AI get/call/join desire, and pre-declaration Laos isolation. The user's initial replay confirmed the corrected faction rework functions properly; retain the diagnostics for longer-run and alternate-branch coverage.
- **Resolved in the 2026-08-17 renovation batch:** Hirondelle, Mouette, Brochet, and the Na San/Vinh Yen/Mao Khe preparation paths no longer use the broken generic launcher or legacy delayed arithmetic. See the implementation checkpoint below. The first full VIN run found three follow-up integration defects; their armistice, THO deployment, and objective-clarity repairs are code-complete but await focused engine acceptance.
- The Lorraine rear-depot objective uses the six provinces of state `881` (Dong Bac Bo) as the map's abstraction of the Clear River/Phu Doan rear area. The 2026-08-12 player run confirmed that the intended state can be defended, Lorraine terminates properly, and its response outcome records correctly. Alternate controller/focus-order branches remain useful diagnostic coverage.
- The retired post-DBP decisions and autonomous Geneva bridge have been superseded by the focus-owned strategy fork. Negotiations retain the existing Vietnamese peace predicate and the narrow divisionless-NLF armistice; escalation proceeds through mobilization to a direct VIN-VIE war while leaving the NLF independent.
- This repository environment still cannot run HOI4 directly; all engine findings come from the user's external playtests.
- Hoa Binh's mechanics are accepted and the payoff/contract follow-up is code-complete, but its new result values still need one human CEFEO run per choice. Do not reopen the accepted campaign lifecycle unless those runs demonstrate an engine failure.
- The scoped rework-localization audit is complete. Continue to keep raw tags and implementation terms out of player-facing values while leaving internal keys, scopes, and hidden variable syntax untouched.
- The first overextension release has one tier. Values and province bands are intentionally exposed in shared triggers/ideas for tuning after the next human and AI tests.
- Legacy `SWF_Indochina_War` border-war result events remain for debug/backward compatibility, but the production campaign watchdog no longer calls them. Consolidating or retiring those inert narrative paths belongs with the later unified campaign-ownership work.
- The legacy `FRE_DBP.1-.8` arithmetic siege definitions also remain for old saves and console compatibility, but their Castor-success production fire site is retired and each is gated out once the live response is active or resolved. Engine testing should confirm no delayed pre-patch event copy survives those guards.
- Castor's visible mission is a thirty-day timer while the scripted counter owns the exact fourteen-day streak. Engine testing must confirm that the mission removes cleanly on scripted success and that its final-day backstop credits a valid thirteenth-recorded-day-plus-current-control edge before failing the operation.

### Exact next resume point

- Re-run Cao-Bac and one restored limited battle first. Confirm THO keeps one battalion in each home state through declaration; confirm the exact province highlight, temporary VP label, and 0/5 hold count; and confirm finish removes both the temporary marker and every French-aligned campaign war without affecting Laos. Use `test_vin_campaign_armistice_cleanup` if a participant remains.
- Continue that save through the remaining limited battles and Geneva if the focused replay passes. No vanilla peace conference may appear from a completed set-piece campaign.
- Confirm Brochet/Na San alter both Castor's displayed threshold and debit, Final Push reads actual Mouette/Atlante results, and theatre closure bypasses the consolidation node. Exercise one abort on each side, one supersession, and `test_fre_limited_operation_status`; use `test_fre_limited_operation_supersede` for deterministic cleanup coverage.
- Fold the pending Pollux/Atlante acceptance into that natural run. Keep their existing alternate-route diagnostics and `test_indochina_command_status` available for opportunistic branch coverage. Use `test_indochina_command_repair` only for a deliberately damaged or legacy setup.
- If available, load one pre-renovation save with a launched old operation or preparation mission to verify the one-time migration. After acceptance, the next unimplemented named operation remains Dak Doa.
## 2026-08-17 FRE operations/preparation implementation checkpoint

The previously documented legacy warning is now addressed in the working tree. Hirondelle, Brochet, and Mouette use an exact-objective limited-operation lifecycle with daily control checks, bounded deadlines, terminal result flags, owned-war cleanup, and no territorial transfer. Their historical map contracts are Lang Son/Loc Binh (`9948`, `13761`), Hung Yen (`13755`), and Phu Nho Quan (`11909`).

The old Na San, Vinh Yen, and Mao Khe preparation arithmetic is no longer on the production path. VIN now owns limited primary campaigns for Vinh Yen (`12075`), Mao Khe (`13772`), the multi-objective Day River line (`1185`, `13753`, `13755`), and Na San (`13757`); FRE owns preparation posture and result callbacks. Each offensive requires five consecutive days on its objective and terminates through the common result enum without transferring state ownership.

The implementation also corrects initial control of Vinh Yen province `12075`, makes early results feed the following battle, carries Amarante and Lorraine into Na San, carries Na San/Brochet into Castor, activates Hirondelle's paratrooper-raid unlock, and replaces Final Push's unconditional struggle award with Mouette/Atlante result consolidation. Brochet/Na San change both Castor eligibility and the charged price. Scoped AI orders terminate with their owning package, crossing VIN campaigns supersede limited operations, Final Push has a theatre-closure bypass, and France carries the operation clock so VIN's disappearance cannot strand cleanup. A migration retires active legacy missions and prevents queued legacy outcomes from double-paying.

Static acceptance on 2026-08-17: `git diff --check`, raw Clausewitz brace balance over the 25 changed/new gameplay `.txt` files, the 22-file SEA localization audit, all edited localization BOM checks, targeted event/symbol/localization uniqueness and reference checks, both edited focus-tree cycle checks, exact-objective/owned-peace assertions, the single-carrier assertion, and legacy-result guard checks pass. A fresh 1949-1956 engine playtest remains required before this checkpoint is engine-accepted.

## 2026-08-17 VIN playtest integration repairs

A player-led VIN run reached 1956 and established that the expanded content order and operational pacing flow well. It also exposed three concrete defects in the restored content: THO's two battalions left Cao Bang/Lang Son when Cao-Bac opened; the Vinh Yen-era limited battles did not explain their exact province contracts; and a campaign armistice could white-peace the nominal target while leaving VIN at war with FRE. Continuing that orphaned war allowed an ordinary capitulation and vanilla peace conference, bypassing the intended campaign/Geneva lifecycle.

The armistice contract is now war-wide rather than nominal-target-only. Every primary campaign finish arms `VIN_Limited_Campaign_Armistice_Pending`, directly attempts white peace with FRE, France, TAI, TAM, THO, VIE, and NUN, and retries the same sweep from `on_daily_VIN` until no listed participant remains at war with VIN. Laos tags are not included, preserving unrelated Laos raid/invasion ownership. Limited-campaign declaration also records ownership even when subject/faction propagation made the target technically at war before the declaration branch evaluated. `test_vin_campaign_armistice_cleanup` exercises the production repair and reports whether another daily retry is required.

The first replay of the renovated 1953 CEFEO operations exposed a lifecycle collision in that retry: Hirondelle/Mouette/Brochet could create their fresh limited war while the prior VIN armistice flag still survived, after which the VIN daily tick immediately white-peaced the new operation. The ownership boundary is now explicit. `fre_operation_launch` clears a stale VIN campaign retry before declaring; the retry effect yields whenever `FRE_Limited_Operation_Active` is set; and `FRE_limited_operation_window_trigger` requires FRE and VIN to be at peace so an operation cannot piggyback a residual campaign war. Operation finish remains the sole owner of its deliberate white peace.

THO's two historical starting units remain at Cao Bang and Lang Son, but their defensive strategy now activates before war. It gives both home states maximum front request and theatre demand, suppresses allied/rear fronts and garrison diversion, and uses `dont_defend_ally_borders = 1000`. A separate startup inconsistency was corrected by moving VIN's second militia from TAI-controlled Vinh Yen to the VIN-controlled Hoang Lien Son approach.

Each restored limited battle now states its exact contract in the focus completion tooltip and in a persistent decision card: Vinh Yen and Mao Khe each require one named province; Day River requires Ninh Binh, Phat Diem, and the central line simultaneously; Na San requires the named camp rather than Dien Bien Phu or Son La. The card highlights the exact objective province or provinces, the map provinces have English names, and both the card and campaign clock show the live consecutive-hold count. The shared clock hides the hold line for older campaigns which do not use it.

The follow-up uses the decision system's exact `highlight_provinces` list inside each card instead of highlighting the containing state. Because all six objective provinces begin with zero victory-point value, localization alone cannot render their map labels. `vin_limited_campaign_add_objective_vps` therefore adds a reversible one-point marker only to the current objective set; one flag per campaign makes the effect idempotent, and the guaranteed daily tick repairs active saves made before this visibility layer. Common campaign finish calls `vin_limited_campaign_remove_objective_vps`, subtracting only markers whose ownership flag proves this lifecycle added them. The affected provinces are Vinh Yen `12075`, Mao Khe `13772`, Day River `1185`/`13753`/`13755`, and Na San `13757`.

Static acceptance for this follow-up: `git diff --check`, changed/new gameplay Clausewitz brace balance, the 22-file SEA localization audit, edited localization BOM checks, and 26 exact-objective visibility invariants pass. Focused engine acceptance remains required for THO's declaration-day deployment, exact province highlighting, temporary VP-label appearance/removal, five-day counter display, full French-aligned campaign teardown, survival and ordinary cleanup of the 1953 CEFEO limited-operation wars, and preservation of unrelated Laos wars.

## 2026-08-19 unattended acceptance telemetry

The remaining engine pass can now run unattended under `human_ai`. A passive,
always-on observer writes structured `IC_AFK|` records to `game.log`; it never
selects an option, changes an outcome, transfers territory, makes peace, or
repairs a failed invariant. A declaration-end call captures THO's Cao Bang and
Lang Son battalions before AI movement, while merged startup, daily-France, and
pre-peace-conference hooks observe the rest of the production lifecycle.

The record covers every VIN campaign launch/result, restored objective-marker
activation and cleanup, the retrying French-aligned armistice, the three exact
CEFEO limited operations and their owned-war cleanup, Castor's Brochet/Na San
price callbacks, Pollux and Atlante posture/results, an overlapping Atlante and
Dien Bien Phu launch, Final Push consolidation/bypass, Geneva/theatre closure,
and any premature vanilla peace conference involving an Indochina theatre tag.
It emits a heartbeat every 180 days. Exact province-highlight rendering remains
the one GUI-only observation; the underlying temporary VP-marker lifecycle is
logged automatically.

Static verification on 2026-08-19: scoped `git diff --check`, raw Clausewitz
brace balance for the two new gameplay files and the VIN callsite, effect/call
reference checks, and `python3 tools/loc_audit.py --check` pass. The repository-
wide diff check still reports a pre-existing indentation warning in the separate
dirty VIE/Diem worktree. Engine acceptance remains pending the unattended run
and post-run review of `game.log` plus `error.log`. Run instructions and filters
are in `CWIC Backup/documentation/Indochina_AFK_Playtest.md`.

### 2026-08-19 unattended engine result

The first `human_ai` run reached the end of VIE's 1956 content and produced the
historical scripted Geneva outcome naturally on 1954-05-30. No premature
Indochina peace conference was logged. Every completed VIN campaign armistice
reported zero remaining French-aligned wars; all four restored objective-marker
lifecycles activated and removed their markers; Hirondelle, Mouette, and Brochet
launched isolated wars and reported complete cleanup; Castor established the
airhead; and historical Pollux selected the split withdrawal and recorded its
column-loss result. The Brochet-clean and Na-San-failure callbacks correctly
netted Castor back to its base 100/60 prices.

Two integration items remain open. Both THO battalions were absent from their
home states at the exact Cao-Bac declaration snapshot, so the deployment repair
does not have engine acceptance. Atlante and Final Push never entered the logged
sequence before the historical Geneva closure, so this run supplies no engine
coverage for either package.

The run is a balance failure despite reaching the correct historical ending.
VIN won Cao-Bac on day 11, Vinh Yen on day 8, Hoa Binh on day 3, Northwest on
day 38, Na San on day 10, and Dien Bien Phu on day 10; only Mao Khe became costly
and Day River failed. Hirondelle and Mouette never held an objective for one day
and failed on their deadlines. During the repeated scripted wars, the other
CEFEO crown domains lost their armies and collapsed, leaving FRE effectively
confined to Saigon by the post-1952 sequence.

The next balance design pass should therefore audit and likely remove or sharply
reduce the stacked `VIN_Indochina_AI_Support`, `VIN_Campaign_AI_Support`, and
per-campaign AI resource injections before strengthening CEFEO globally. The
preferred containment direction is a two-tier operational-envelope contract:
AI must remain strictly inside each named operation/campaign envelope, while a
player may exceed it knowingly and receive a severe national/state overextension
package. A launch briefing for both sides should state the exact objectives and
the penalty contract. This is a recorded design direction only; it was not
implemented in this checkpoint.

The telemetry itself had one startup-only invalid-scope error because
`on_startup` has no country ROOT. The daily France carrier recovered and logged
the complete run. The startup hook now explicitly scopes initialization to FRA;
no production campaign logic changed as part of that correction.

### 2026-08-19 VIN/CEFEO balance and containment implementation

The first unattended run's balance correction is now implemented. VIN's two
hidden AI combat packages are no longer granted and are actively removed from
old saves. `vin_ai_prepare_campaign` no longer tops Campaign Supply to maximum
or grants 25,000 manpower, 3,000 rifles, 400 artillery, and 50 command power at
every launch. The retained idea definitions exist only so stale save state can
be cleaned safely.

Campaign participation is now objective-owned. CEFEO joins VIN's war alongside
only the crown domain which owns that campaign target: TAI for Northwest, Dien
Bien Phu, Vinh Yen, and Na San; TAM for Hoa Binh; THO for Cao-Bac; and no crown
domain for Mao Khe or Day River. Hirondelle, Mouette, and Brochet are FRE-VIN
operations and do not call TAI, TAM, NUN, or THO. Their finish path likewise no
longer white-peaces independent crown-domain wars it did not create.

All eight VIN campaigns now enforce exact operational envelopes. Vinh Yen, Mao
Khe, Day River, and Na San exempt only their named objective provinces within
the containing state. FRE's three limited operations apply the same rule to
CEFEO, while VIN is confined to its own territory during Hirondelle/Mouette and
to Brochet's single objective when attacking. Leaving the envelope applies a
single severe national penalty: -60% attack, -35% defense, -45% organization,
-35% speed, -50% planning speed, +90% supply consumption, +75% out-of-supply
penalty, -15% reinforce rate, and +35% attrition. It clears automatically on
withdrawal or operation cleanup. French-aligned campaign overextension is now
evaluated per command, preventing one CEFEO advance from debuffing unrelated
crown domains.

The AI retains positive requests only for the active objective state and gains
strong negative requests for unrelated fronts plus allied-border suppression.
The commitment events tell players that the named objectives are the contract,
that the AI follows it, and that a player may deliberately exceed it at severe
cost. AFK telemetry now records removed-buff checks, exact participant checks,
penalty application/clear transitions, and 180-day division health for CEFEO,
VIN, TAI, TAM, NUN, and THO.

Engine acceptance is pending a fresh 1949-to-Geneva `human_ai` run. Compare
campaign completion days and CEFEO operation hold days against the prior sample,
and use the `FORCE_HEALTH` series to determine whether the crown domains retain
armies through 1952-54. Any `VIN_hidden_AI_buffs_removed` or participant-envelope
`FAIL` is a code regression rather than a balance result.

## 2026-08-19 second unattended-run corrections

The follow-up run exposed three systemic defects despite again reaching the
historical outcome. The Pathet Lao clocks were declared with an impossible
`allowed` condition, AI raids reserved nearly CEFEO's entire field army, and VIN
received 500 duplicate Communist points from focus completion on top of live
campaign results.

Both Laos timers are now FRA-owned and activatable. Cleanup removes every hidden
and visible mission, a 90-day initial and 45-day last-chance daily backstop makes
the lifecycle self-terminating, and CEFEO limited operations cannot launch while
the raid is active. The shared raid AI predicate now suppresses new ambient raids
for VIN and FRE while preserving human access to all raid controls.

The five duplicate VIN focus awards are removed. VIN campaign outcomes are now
roughly quarter-strength, CEFEO limited-operation and response outcomes are
scaled into the same range, and Laos results move the score by 25-50 rather than
three-digit amounts. Escalation-phase arithmetic is intentionally unchanged.
VIN's Geneva seed now converts battlefield score at 1/50 and Communist leverage
at one quarter; PRC/SOV use one fifth. VIN's major focus and post-DBP leverage
awards are also reduced. The target for a complete VIN victory is a Communist
lead of roughly 100-200 points and a Hanoi delegate weight comparable in scale
to Saigon and France rather than the observed ~700.

AFK telemetry now logs six-month Struggle scores, all Geneva leverage pools,
VIN/VIE/FRA weights, Pathet Lao launch/result/duration, stuck-clock failures, and
any illegal CEFEO-operation overlap. Engine acceptance requires another fresh
1949-to-Geneva `human_ai` run.

## 2026-08-21 AFK defect-repair checkpoint

The follow-up log audit queue is code-complete and statically accepted. The
undefined `vin_ai_prepare_campaign` launch call is gone. An active Laos raid is
now rechecked inside `fre_operation_commit`, before any resource debit or
operation activation, and resolves the pending package as superseded. This is
the authoritative guard that focus availability alone could not provide.

THO placement telemetry established the real failure mode: both battalions load
in their historical states, but the Lang Son battalion leaves during peacetime
by June 1949. Because a front strategy cannot guarantee peacetime stationing,
Cao-Bac declaration now re-forms the two AI-only territorial battalions at Cao
Bang and Lang Son if either post is empty. This happens before war declaration
and validation, preserves exactly two battalions, and does not alter objectives,
deadlines, ownership, or campaign rewards. NUN has separate immediate-postwar
and later terminal existence/capitulation/state-ownership records to trace its
previously unexplained post-Geneva disappearance.

Balance values remain frozen pending evidence. The passive FRA daily carrier now
records every Struggle component delta, while the suspected one-time `+350`
Communist victory-preparation award emits a source-specific record. The next log
can therefore confirm or eliminate that award as the late-war overshoot source
without guessing from six-month snapshots.

The scoped runtime cleanup moves Tran Quoc Buu's retirement into NLF scope,
uses the valid generic VIN cleanup ideas, promotes Lo Van Hac through character
roles that already exist, seeds Pathet Lao's required truck variant before its
field-force OOB loads, and replaces the missing Laos demobilization icon with an
existing Laos-war asset. The Lo Van Hac role expiry and `war_industrialist`
trait remain declared on all three relevant ideology roles.

Static verification: repository and scoped `git diff --check`, raw Clausewitz
brace balance across all 17 changed gameplay `.txt` files, targeted lifecycle
and symbol assertions, and the 22-file SEA localization audit pass. External
engine acceptance remains the next step; no deferred operation, including Dak
Doa, should be started until the new baseline logs confirm these repairs.
## 2026-08-22 implementation checkpoint: Dak Doa and Northwest recovery

Implementation has begun. The contract is frozen as follows: Dak Doa is an
NLF-scoped, ownership-neutral seven-day province campaign whose cleanup can
white-peace only an NLF-FUL war it created; its CEFEO response is parent-resolved
before common cleanup. Northwest recovery is VIN campaign ID `9`, permanently
attempted at launch, always costly on success, and leaves campaign ID `1`'s
permanent result untouched. `VIN_Prepare_Dien` continues to require ownership of
state `1761`.

The historical AI defaults to the isolated-post defense represented by the
February 1954 siege; GM 100 remains the expensive counterfactual commitment.
Operational context: https://mcoecbamcoepwprd01.blob.core.usgovcloudapi.net/library/ABOLC_BA_2018/Research_Modules_B/Groupemont_Mobile_100/LaBatailled%27Ankh%C3%A9_ENG_translation.pdf

Code-complete checkpoint: Dak Doa, its CEFEO response, Northwest recovery ID
`9`, shared response validation/logging, scoped console diagnostics, English
localization, AI priorities, and the unified checkpoint playtest are present.
Static acceptance covers diff whitespace, raw braces, localization audit/BOM,
new symbol uniqueness/references, VIN focus acyclicity, permanent-result
exclusivity, ownership/peace mutation guards, and pixel-map adjacency
`1328 <-> 10180/16442/4363`. Unified engine acceptance remains pending.

Engine follow-up: the first alternate run exposed that TAI could receive the
campaign-owned white peace while FRE, pulled into that same recovery war, did
not. Campaign `9` now records a pre-launch war snapshot for the relevant
French-aligned tags. Resolution settles only opponents absent from that
snapshot, retries while a generated opponent remains, and records cleanup
complete only after all such participants are at peace. This preserves an
unrelated pre-existing VIN war while preventing the observed perpetual FRE war.
The Northwest recovery checkpoint must be rerun before engine acceptance.

## 2026-08-23 historical-AI playtest review

The 23 August logs supersede the prior baseline for current runtime behavior.
They do not accept the current battlefield AI or balance. Lifecycle telemetry
recorded no `IC_AFK|FAIL`: both THO declaration posts, participant isolation,
temporary objective markers, campaign armistices, CEFEO operation cleanup, and
Final Push consolidation behaved correctly. The result sequence was Cao-Bac
clean day `51`, Vinh Yen clean day `8`, Mao Khe failure day `36`, Day River
costly day `38`, Hoa Binh clean day `66`, Northwest clean day `102`, Na San
clean day `11`, and Dien Bien Phu clean day `30`. Hirondelle and Mouette failed,
Brochet succeeded, Castor established, Pollux was superseded by campaign `3`,
and Atlante was later superseded.

Two engine errors outrank balance interpretation. The recovery focus uses the
unsupported trigger `political_power > 49`, and the engine rejects
`defender_modifier` in all rework-local state dynamic modifiers. Until the
second issue is replaced by a supported defender-only application contract,
the intended contested-objective, holdout, Castor, Dak Doa, and Dien Bien Phu
packages cannot be treated as functioning balance inputs. The recovery console
inspection also needs to expose its cleanup-complete flag.

The same scoped error review found that `SWF_VIN.17` is deliberately fired in
both VIN and NLF scope but currently gives both options a VIN-only trigger. NLF
therefore receives no valid option. Restore a non-conflicting NLF
acknowledgement or stop sending that player-choice event to NLF. Missing Siam
focus completions in `Indochina_Flavor_Events.txt` are real adjacent regional
errors, but they are not a cause of the northern battlefield behavior and are a
lower priority than the rework-local failures.

The user's map observations establish a systemic objective-allocation problem:
Vinh Yen and Na San were not defended; VIN would not press favorable attacks at
Mao Khe and Day River; raid outposts drew CEFEO/TAI toward Lai Chau/`12319`
during Northwest; MEO did not visibly remain in Ha Giang; VIN entered Dien Bien
Phu before its named campaign; and the Laos AI left Luang Prabang open while
stacking province `13738`. Repair this through exact objective demand, local
minimum presence, raid-versus-campaign priority, and bounded reserve behavior
before applying global combat bonuses.

Operation-specific conclusions are now frozen for the next pass. Brochet's
observed behavior is acceptable. Hirondelle should become an ownership-neutral
airborne cache-destruction/interdiction raid rather than a conventional limited
war. Mouette needs exact southern-Tonkin/Red-River-Delta sweep objectives and
must keep both sides from abandoning the live operation for unrelated fronts.
Lorraine needs visible posture/result reporting. Castor and Pollux must occur
early enough to create a real preparation window; after the rejected defensive
modifier contract is repaired, the DBP garrison/output and siege duration may
be strengthened. Campaign `3` also needs a bounded Hanoi/Tonkin reserve so the
camp objective does not coexist with unopposed CEFEO penetration elsewhere.

The post-DBP focus fork is not yet authoritative. Dien Bien Phu fell on 16 March
1954, the VIN briefing appeared on 17 March, and scripted Geneva concluded on
31 May without evidence that `VIN_Push_for_Negotiations` completed. Shared
French or other pursuit owners can still bypass the visible Hanoi choice. Add
source-specific pursuit/announcement telemetry and a narrow post-communist-DBP
choice/grace latch while preserving the existing Vietnamese peace gate and
legitimate conference routes outside that causal path.

The outcome GUI must now display the full campaign ledger. "The Wars Behind the
Table" currently covers only the southern Viet Minh, Pathet Lao, Dien Bien Phu,
sects, highlands, and the Laos raid. Add the permanent result and actual
Struggle/leverage contribution for every VIN campaign, CEFEO operation, and
attached response package so raw outcomes are visible without observing each
battle live.

The score telemetry rules out the suspected single `+350` award in this run.
The Communist margin reached the desired band at `+184` in May 1953, then rose
through repeated ambient `+25`/`+50` awards to `+364` in October and `+429` in
April 1954. Trace those recurring sources before retuning outcome values. The
southern force comparison is independently unacceptable: VIE grew from `34` to
`38` divisions while NLF remained at `5` and disappeared by late April 1954.
Reduce VIE's effective wartime build/limit advantage and/or provide bounded NLF
sustainment without merging the southern and northern wars.

Revised implementation order: fix engine-rejected syntax, the NLF event with no
valid option, and recovery telemetry; make the post-DBP choice authoritative and log Geneva ownership;
expand the outcome GUI; repair objective allocation and raid interaction;
rework Hirondelle/Mouette; accelerate and then rebalance Castor/Pollux/DBP;
rebalance NLF/VIE and recurring score awards; then perform targeted checkpoint
coverage followed by a unified run. Dak Doa and Northwest recovery remain
code-complete but unaccepted because this natural run reached Geneva before Dak
Doa and did not exercise campaign `9`.

## 2026-08-23 corrective-pass implementation ledger

The corrective pass following the 23 August historical-AI review is implemented
but not yet engine-accepted. It repairs the rejected script contracts, makes
VIN's post-Dien Bien Phu strategy choice authoritative over shared Geneva entry,
adds observer-only CEFEO intelligence and a full campaign/operation outcome
journal, tightens objective AI allocation, converts Hirondelle into a
non-territorial cache raid, bounds Mouette to southern Tonkin, accelerates
Castor/Pollux, strengthens the supported Dien Bien Phu holdout modifiers, and
adds bounded NLF reconstitution. Brochet is intentionally retained unchanged.

This pass also establishes the presentation contract for future polish: VIN is
briefed only on visible French action and uncertain intent; commitment tiers and
resolver arithmetic stay concealed. A later dedicated prose pass may update the
remaining legacy raw keys and omniscient/future-tense writing, but new operation
briefings already use present-tense, fog-of-war language.

The score trace did not identify a repeated `+350` or duplicate campaign result.
The observed `+25`/`+50` deltas correspond to ordinary focus-ledger awards, so
the implementation does not apply a global score nerf without a comparative
run. The expanded GUI exposes exact standings and leverage for that test.

Engine acceptance is intentionally pending. The next sequence is a targeted
smoke pass for parser/event/mission/Geneva and operation contracts, followed by
the unified historical-AI run already requested in this specification.

## 2026-08-29 combined engine-acceptance protocol

Limited tester availability combines the targeted smoke pass and historical-AI
run into one fresh 1949-to-Geneva game. The authoritative procedure and
checkoff are in `CWIC Backup/documentation/Indochina_AFK_Playtest.md`. Parser,
telemetry, stuck-lifecycle, premature peace-conference, and post-Dien Bien Phu
choice-bypass defects are early-stop regressions. AI allocation, pacing,
force-health, and score problems are recorded and carried through the complete
run so the next fix pass has comparable evidence. Engine acceptance remains
pending review of both preserved logs and the completed checkoff.
