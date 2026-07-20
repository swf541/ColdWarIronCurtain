# Victoria 2-Style Sphere of Influence Rework — Implementation Plan

Replaces the current normalized influence-pie system (`00_influence_scripted_effects.txt`)
with a Vic2-style Great Power influence game: influence points accrue per target from your
power projection split by priority, opinion climbs in stages, and at the top you sphere the
country for economic integration.

Status: DRAFT for review. Nothing implemented yet.

---

## 1. Design summary (the loop)

1. **Sphere-capable** countries (GPs) can influence any **non-sphere-capable** country.
   Capability is a flag granted/removed by events & decisions — losing it makes you a normal
   spherable target.
2. Each GP has a monthly **Influence Power** (IP) pool derived from its power projection
   (reuses the current FPP inputs: factories, GDP, subjects).
3. For each target the GP picks a **priority: None / Low / Normal / High** (Vic2-style
   buttons on the target's panel). None = no IP spent on them.
4. **Monthly tick**: your IP is split across your prioritized targets by weight
   (Low 1 / Normal 2 / High 4), modified by your `foreign_influence_modifier`, the target's
   `foreign_influence_defense_modifier` and situational factors. Each pair has a plain
   **0–100 influence score** (NOT zero-sum between GPs — each GP has its own track on the
   target, exactly like Vic2).
5. At **100 influence** on a target: influencing that target pauses; the **Increase Opinion**
   action unlocks. Using it spends the 100 points (score resets to 0) and raises the opinion
   stage by one.
6. **Opinion stages** (per GP-target pair): `0 Hated, 1 Disliked, 2 Neutral, 3 Liked, 4 Loved`
   (+ the implicit 6th state: **Sphered**). Each stage applies a real `opinion_modifier` so AI
   diplomacy follows along.
7. At **Loved + 100 influence**: the **Add to Sphere** action unlocks. Sphering spends the
   points and binds the country:
   * **Market access**: mutual trade bonuses between leader and member (see §6).
   * **Embargo sync**: when the leader embargoes a country, all sphere members automatically
     embargo it too (and un-embargo when the leader stops).

---

## 2. Data model

All persistent state lives in variables/flags (no new engine features needed).

**On every country (potential target):**
| Var | Meaning |
|---|---|
| `sph_gp_ids` (array) | country ids of GPs with an influence track here |
| `sph_gp_score` (array) | matching influence score 0–100 |
| `sph_gp_stage` (array) | matching opinion stage 0–4 |
| `sph_leader` (var) | id of sphere leader (0/unset = not sphered) |
| flag `sphere_capable` | this country is a GP (cannot be targeted) |

**On every GP (influencer):**
| Var | Meaning |
|---|---|
| `sph_target_ids` (array) | targets with a set priority |
| `sph_target_prio` (array) | 1 = Low, 2 = Normal, 4 = High |
| `sph_influence_power` (var) | monthly IP pool (recomputed monthly) |
| `sph_members` (array) | ids of sphered members |
| `sph_embargoes` (array) | ids the leader is embargoing (for sync) |

**Selected-country UI context vars** (temp): current viewer's score/stage/prio on the
selected nation, for the GUI properties.

### Influence Power formula (monthly)
```
IP = clamp( base 2
     + num_of_factories / 150
     + grossdomesticproduct_fake / X        # tuned so USA/SOV ≈ 10–14, mid GPs ≈ 5–8
     + subjects' GDP sum / Y ,  2 .. 15 )
```
Reuses the inputs of `monthly_power_projection_gain`; the old `foreignPowerProjection`
variable is retired (or kept updated for backward references only).

### Monthly gain per target
```
share   = prio_weight / sum(prio_weights of all my active targets)
gain    = IP * share
gain   *= (1 + my modifier@foreign_influence_modifier)
gain   *= (1 - target modifier@foreign_influence_defense_modifier)
gain   *= 1.25 if neighbor / same continent
gain    = 0 if at war with target, target at war with my sphere, or target sphered by me
score   = clamp(score + gain, 0, 100)
```
Existing act/idea content (Mutual Security, CIA Act, McCarran, media laws, Peace Corps,
Boland/Clark repeals…) keeps working unchanged because it feeds these two modifiers.

---

## 3. New files

| File | Contents |
|---|---|
| `common/scripted_effects/CWIC_sphere_core_effects.txt` | `sph_init_country`, `sph_monthly_tick` (IP calc + allocation loop), `sph_add_influence` (pair mutator, used by all content), `sph_set_priority_low/normal/high/none`, `sph_increase_opinion`, `sph_decrease_opinion` (for events), `sph_add_to_sphere`, `sph_remove_from_sphere`, `sph_grant_capability`, `sph_revoke_capability`, `sph_embargo_sync`, cleanup helpers (annex/civil-war) |
| `common/scripted_triggers/CWIC_sphere_triggers.txt` | `is_sphere_capable`, `sph_can_target`, `sph_can_increase_opinion`, `sph_can_sphere`, `sph_is_in_my_sphere`, `sph_same_sphere` |
| `common/on_actions/CWIC_sphere_on_actions.txt` | `on_startup` → migration + init; `on_monthly` → `sph_monthly_tick` (GPs only) + `sph_embargo_sync`; `on_annex` / `on_capitulation` / `on_civil_war_end` → cleanup pairs; `on_declare_war` → zero hostile tracks |
| `common/scripted_guis/CWIC_sphere_gui.txt` | Selected-country influence panel (priority buttons, progress bar, opinion stage, action buttons) + GP overview window (list of my targets & allocation) |
| `interface/CWIC_sphere_gui.gui` | The window layouts (follow the existing `show_influence_pie_chart` selected-country pattern) |
| `interface/CWIC_sphere_gui.gfx` | Button/stage icons (Low/Normal/High toggles, 5 opinion stage pips, sphere crest) — placeholder sprites from existing assets first |
| `common/opinion_modifiers/CWIC_sphere_opinions.txt` | `sph_stage_hated` (−60) … `sph_stage_loved` (+60), `sph_sphere_member` (+100 leader↔member) |
| `common/ideas/CWIC_sphere_ideas.txt` | `sphere_member_trade` idea (member: trade/market bonuses, see §6), `sphere_leader_market` dynamic-modifier idea reading `sph_members^num` |
| `localisation/english/CWIC_sphere_l_english.yml` | All UI strings, tooltips, stage names |
| `docs/SPHERE_INFLUENCE_REWORK_PLAN.md` | this file |

## 4. Modified files

| File | Change |
|---|---|
| `common/scripted_effects/00_influence_scripted_effects.txt` | Gut to a **compatibility shim**: `change_influence_percentage` → translates `percent_change/tag_index/influence_target` into `sph_add_influence` on the new score (so ~60 existing content files — UAR, IMF, Yugoslavia, dozens of focuses, investment slots — keep functioning without edits). `spread_influence`, boost/decrease effects likewise shimmed. Sorting/pie/`calculate_influence_percentage` deleted. |
| `common/scripted_diplomatic_actions/influence_scripted_diplomatic_actions.txt` | Remove `opt_influence_action` / `opt_stop_influence_action` (replaced by priorities). Keep trade agreement / subsidies / debt / defense pact actions (they become influence sources via `sph_add_influence`). Rewrite `opt_add_to_sphere` / `opt_remove_from_sphere` on the new triggers. |
| `common/on_actions/influence_on_actions.txt` | Delete the daily influencing tick (superseded). |
| `common/decisions/IC_Influence.txt` | Keep the `Invest_in_X` decisions; their `short/medium/long_length_investment_influence_boost` reroute to `sph_add_influence` (investments become a way to speed a track). Delete `target_influencer_0..6` (replaced by phase-2 Discredit action). |
| `common/scripted_guis/influence_scripted_gui.txt` + pie chart .gui | Replace ideology pie with the new panel (or keep pie as read-only flavor initially). |
| `history/countries/*` | **No edits.** Startup migration (§7) converts the old arrays in memory. |
| `common/scripted_localisation/influence_scripted_localisation.txt` | Replace tokens with stage/priority text tokens. |

## 5. GUI spec (Vic2 feel, HOI4 idioms)

**A. Target panel** (`selected_country_context`, like the existing pie chart button+window):
* Header: "Influence — [Country]"
* My score: progress bar 0–100 + numeric.
* Opinion stage: name + colored pip row (Hated red → Loved green; Sphered = gold crest).
* Priority buttons: `[None][Low][Normal][High]` — radio-style toggles writing
  `sph_set_priority_*`; visible only to sphere-capable viewers on valid targets.
* Action buttons: `Increase Opinion` (enabled at score 100), `Add to Sphere` (enabled at
  Loved + 100), `Remove from Sphere` (leader only).
* Rivals readout: list other GPs' score/stage on this target (top 3-4 by score).

**B. GP overview window** (topbar button, own-country):
* IP this month, number of targets, table: target flag | priority | score | stage.
* Warning row when total weights dilute gains below a useful threshold.

**AI**: no GUI — a monthly AI block in `sph_monthly_tick` assigns priorities:
High on same-continent / resource-rich / already-Liked targets it can flip, Normal on
strategic neighbors, None when hopeless (rival at Loved, or at war). Budget: AI caps active
targets so its IP isn't diluted below ~1.5 pts/target/month.

## 6. Sphere effects (concrete)

* **Member gets** `sphere_member_trade` idea: `global_trade_bonus_adjustment` +X,
  `extra_trade_to_overlord_factor`-style access, small `consumer_goods_export_rate` bonus —
  exact modifiers picked from the wired set in `influence_modifier_definitions.txt`.
* **Leader gets** a dynamic modifier scaling with member count (small
  `office_park_income_bonus` / trade bonus per member — big-market flavor).
* `sphere_tag_list` (already consumed by USA content/investment lists) is **kept as the
  canonical output array** — `sph_add_to_sphere/remove` maintain it, so downstream systems
  keep working untouched.
* **Embargo sync** (`sph_embargo_sync`, monthly + on-action): diff the leader's embargo list
  against `sph_embargoes`; for each new entry force members to embargo the same tag, for each
  removed entry lift it. Uses the mod's embargo mechanism (verify exact effect names during
  implementation — vanilla BBA embargo vs. any CWIC trade-system hook).

## 7. Migration of existing state & content

At `on_startup` (once, global-flag guarded), for every country with old `influence_array`:
* Old value ≥ 100 → score 100, stage Liked; ≥ 50 → score = value clamped, stage Neutral;
  < 50 → score = value, stage Neutral.
* `influenced_by`/`sphere_tag_list` relations upgraded: existing sphere members → Sphered
  under their leader.
* Old arrays cleared afterward. History files never touched (471 of them).

Sphere capability needs **no seeding** — it's derived from the existing `sphere_tag_list`
ownership (see §10.4), which history/on_startup/focus content already grants.

## 8. What dies

* The normalized 100% pie & `domestic_influence_amount` (concept removed).
* `sort_influence`, `delete_influencer_check`, `check_uar_influence` (with its `_val` bug),
  the no-op `recalculate_influence`, index-4 displacement bug — all gone with the pie.
* Daily 50 PP + 1 FPP influencing tick.
* `target_influencer_X` counter-decisions (phase 2 replaces with Discredit).

## 9. Phases

1. **Core** (no GUI): data model, monthly tick, priorities via temporary debug decisions,
   compat shim, migration, sphere add/remove + `sphere_tag_list` continuity. Testable via
   console/observer.  **[DONE 2026-07-19]**
2. **GUI**: target panel (score bar, opinion stage, priority buttons, action buttons) via
   `CWIC_sphere_gui.txt` + `interface/CWIC_sphere_gui.gui`/`.gfx`, daily display refresh, stage/
   priority scripted-loc. **[DONE 2026-07-19 — layout needs an in-game visual tuning pass]**
3. **Sphere economics**: member/leader ideas, embargo sync.
4. **AI** priorities + tuning pass (IP scale, gain rates — target: Neutral→Sphered on a
   focused High target ≈ 3–5 game-years).
5. **Phase 2 (later, optional)**: Discredit/Expel-style hostile actions, war-driven sphere
   collapse events. (Note: pulling countries out of rival spheres via Loved+100 is now IN
   scope for phase 1 core — see §10.3.)

## 10. Design decisions (LOCKED 2026-07-19)

1. **Independent tracks.** Each GP has its own 0–100 score per target — no zero-sum pie.
   Rivalry expresses through opinion stages, sphere contests, and later hostile actions.
2. **No decay.** Scores are permanent progress; setting priority to None just stops gains.
3. **Spheres contestable from day one.** Rivals can build tracks on sphered countries.
   A rival reaching **Loved + 100** on a sphered target may spend the points to **pull it
   out of the sphere** (target becomes unsphered; scores persist). Sphering it themselves
   then requires banking another 100.
4. **Sphere capability = owning a `sphere_tag_list`** — this already exists in the mod:
   USA & SOV get theirs (with members) in `on_startup.txt`; BEL, CHI, ENG, FRA, HOL, PAK,
   RAJ, SAF, SIA, VND, YUG, BOP, CSK via history files; various focuses grant lists to
   NIC, KEN, NGA, BCP, COG targets etc. The rework keeps this exact marker:
   `is_sphere_capable = has_variable sphere_tag_list`. `sph_grant_capability` creates the
   array; `sph_revoke_capability` dissolves it (members released, leader becomes targetable).
   No new flag needed — all existing grants keep working.
5. **Stages**: Hated, Disliked, Neutral, Liked, Loved + Sphered as the sixth state.
