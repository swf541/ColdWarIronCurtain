# Sphere of Influence — Content-Creator API

Everything a focus/event/decision author needs to hook into the sphere system.
Nothing here requires touching the core files.

---

## 1. Modifiers (grant via ideas, focuses, dynamic modifiers)

These are **custom modifiers** — use them in any `modifier = { }` block on an idea,
dynamic modifier, focus reward (as an idea), etc.

| Modifier | Effect |
|---|---|
| `influence_slots` | +N countries you can influence at once (base is 2). |
| `influence_gain_flat` | +N flat weekly influence gain per active target (base is 4). |
| `foreign_influence_modifier` | % multiplier on the influence YOU project (e.g. `0.25` = +25% faster). |
| `foreign_influence_defense_modifier` | % resistance to being influenced BY others (e.g. `0.25` = incoming influence −25%). |
| `sphere_strategic_value` | How badly AI Great Powers want to influence this country. AI ranks targets by `num_of_factories + sphere_strategic_value`, so put it on a nation's starting spirit to make it a Cold War prize (oil, chokepoints, big economies). Copy the `sph_strategic_value_template` idea. |

Weekly gain per target = `(4 + influence_gain_flat) x (1 + foreign_influence_modifier) x (1 - target's foreign_influence_defense_modifier)`.

```
# Example: a focus reward idea that makes you influence faster
my_diplomacy_corps = {
    allowed = { always = no }
    removal_cost = -1
    modifier = {
        influence_slots = 1
        foreign_influence_modifier = 0.20
    }
}
```

---

## 2. Triggers (check in `available`, `bypass`, `visible`, event `trigger`, AI)

Direct checks (no scripted trigger needed):

```
check_variable = { Sphere_Leader = USA.id }     # target is in USA's sphere
has_country_flag = sph_econ_accord_USA          # target has an econ accord with USA
has_country_flag = sph_mil_accord_USA           # target has a mil accord with USA
has_idea = sphere_member_trade                  # target is a sphere member
is_in_array = { sph_members = FROM }            # (leader scope) FROM is my member
```

Scripted triggers (see `common/scripted_triggers/CWIC_sphere_triggers.txt`):

| Trigger | Scope | Meaning |
|---|---|---|
| `is_sphere_capable` | any | can this country run the influence game |
| `sph_is_sphered` | target | is in some sphere |
| `sph_is_free` | target | is in no sphere |
| `sph_root_is_my_leader` | target | ROOT is my sphere leader |
| `sph_from_is_my_leader` | target | FROM is my sphere leader |
| `sph_from_is_my_member` | leader | FROM is one of my members |
| `sph_has_members` | leader | I lead at least one member |
| `sph_root_is_influencing_me` | target | ROOT is actively influencing me |

**Influence-level check** (needs a two-step because triggers can't loop):
```
# in an effect block first (ROOT = the leader whose influence you want)
SPA = { sph_ce_store_influence = yes }
# then, wherever you can check variables on SPA:
check_variable = { SPA.sph_query_influence > 50 }
```

---

## 3. Effects (call in `completion_reward`, event `immediate/option`, decisions)

**Convention:** call inside the TARGET country's scope; ROOT is the LEADER/influencer.
(Inside `SPA = { ... }` within a USA focus, ROOT is still USA.)

| Effect | Params | Result |
|---|---|---|
| `sph_ce_give_influence` | `temp sph_ce_amount` | add (or, if negative, remove) influence over the target |
| `sph_ce_set_influence` | `temp sph_ce_amount` | set the leader's influence over the target to an exact 0–100 |
| `sph_ce_force_econ_accord` | — | sign the Economic Accord immediately (skips the influence cost) |
| `sph_ce_force_mil_accord` | — | sign the Military Accord immediately (requires the econ accord) |
| `sph_ce_force_sphere` | — | put the target straight into ROOT's sphere |
| `sph_ce_free_sphere` | — | remove the target from whatever sphere it's in |
| `sph_ce_store_influence` | — | write `sph_query_influence` (0–100) and `sph_query_stage` (0/1/2) on the target |
| `sph_ce_seek_influence` | — | make ROOT start actively influencing the target (ongoing; ignores slot limits) |
| `sph_ce_stop_seeking` | — | make ROOT stop influencing the target |

```
# USA focus: "Contain the South" — start courting Brazil and Argentina
completion_reward = {
    BRA = { sph_ce_seek_influence = yes }
    ARG = { sph_ce_seek_influence = yes }
}
```

**AI targeting:** AI Great Powers score each candidate as
`num_of_factories + sphere_strategic_value + 40 (borders the GP or a member) + 30 (shares the GP's government)`,
then court the most valuable uncontested one. Use `sphere_strategic_value` to bias them.

```
# USA focus: "The Marshall Plan" — hand France a big influence head start
completion_reward = {
    set_temp_variable = { sph_ce_amount = 60 }
    FRA = { sph_ce_give_influence = yes }
}

# USA focus: "Rio Pact" — bring Brazil straight into the sphere
completion_reward = {
    BRA = { sph_ce_force_sphere = yes }
}

# Event: a coup frees a country from its sphere
immediate = {
    ROOT = { sph_ce_free_sphere = yes }
}
```

**Also available (lower-level, temp `sph_from` = leader id, target scope):**
`sph_add_influence` (temp `sph_amount`), `sph_sign_econ_accord`, `sph_sign_mil_accord`,
`sph_lower_accord`, `sph_add_to_sphere`, `sph_remove_from_sphere`, `sph_discredit`.
Capability: `sph_grant_capability` / `sph_revoke_capability` (leader scope) to make a
country able / unable to run spheres at all.

---

## 4. Display (use in your own tooltips / GUI text)

| Get function | Scope | Shows |
|---|---|---|
| `[GetSphereName]` | target | e.g. "American Sphere of Influence" / "Not Part of Any Sphere" |
| `[GetSphLeaderNameWithFlag]` | target | the sphere leader's name + flag, or "None" |
| `[GetSphStageName]` | target | the viewing player's accord stage with this country |
| `[GetSphMyInfluenceText]` | target | `sph_query_influence`/100 (run `sph_ce_store_influence` first) |

---

## 5. Data model (if you need to read the raw arrays)

- **Target country:** `sph_gp_ids[]` (leader ids) · `sph_gp_score[]` (0–100) ·
  `sph_gp_stage[]` (0 none / 1 econ / 2 mil) · `Sphere_Leader` (leader id, 0 = none)
- **Leader country:** `sph_active_ids[]` (who I'm influencing) · `sph_members[]` ·
  `sph_slots` · `sphere_tag_list[]` (canonical membership list)

Same index across `sph_gp_ids`/`sph_gp_score`/`sph_gp_stage`. To find a leader's row on
a target, use `sph_get_pair_index` (temp `sph_from` = leader id) → temp `sph_idx` (or −1).

---

## 6. Ideological compatibility (2026-09-06)

Accords are refused across the Iron Curtain. The policy is two lists in
`common/scripted_triggers/CWIC_sphere_triggers.txt` — `sph_bloc_left`
(communism, maoism, trotskyism, socialist) and `sph_bloc_west` (democratic,
liberal, centrist, conservative). Everyone else — nationalists, monarchies,
islamists, non-aligned — can deal with either side, because Washington armed
the Shah and Moscow armed Nasser.

| Trigger | Scope | Meaning |
|---|---|---|
| `sph_bloc_left` / `sph_bloc_west` | any | which side of the curtain |
| `sph_curtain_blocked_root` | target, ROOT = power | accords barred (use in GUI/diplomatic actions) |
| `sph_curtain_blocked_from` | target, temp `sph_from` | same test inside effects |
| `sph_can_econ_accord_root` | target | economic accord legal |
| `sph_can_mil_accord_root` | target | military accord legal (also requires they answer to no rival) |

**Exception flag:** `sph_ignore_ideology` on *either* country lifts the bar.
That is the Tito / Nasser / Ceausescu hatch — set it from your focus or event.

```
# Yugoslavia can deal with both sides
YUG = { set_country_flag = sph_ignore_ideology }
```

## 7. Telling the great powers something is happening

`sph_find_patrons` — **target scope**, temp `sph_min` = the influence a power
needs to be told. Fills global event targets `sph_patron_1..3` (and
`sph_patron_subject` = the country itself) plus temp `sph_patron_count`.

Use it for elections, coups, regime change, succession — any moment the
patrons would want a say. You write the event; this finds who has earned one.

```
# A colonel's coup is brewing in Iran — anyone holding 50+ influence gets a say
IRN = {
    set_temp_variable = { sph_min = 50 }
    sph_find_patrons = yes
    if = {
        limit = { check_variable = { sph_patron_count > 0 } }
        event_target:sph_patron_1 = { country_event = my_coup.1 }
    }
    if = {
        limit = { check_variable = { sph_patron_count > 1 } }
        event_target:sph_patron_2 = { country_event = my_coup.1 }
    }
}
```

`cwic_sphere.5` is a working template for the receiving event — copy it. Its
first option spends 25 influence, so intervening costs the standing you built.

**Automatic notifications** already fire on their own: `sph_notify_rivals`
runs whenever an accord is signed or lost, a country is sphered, or one is
torn out of a sphere. Every power holding more than 25 influence there is
told (`cwic_sphere.2`), the country itself is told when it joins a sphere
(`cwic_sphere.3`), and sphere members are told when their patron's embargo is
forced on them (`cwic_sphere.4`). `global.sph_news_kind` carries what
happened; `[GetSphNewsLine]` renders it.

