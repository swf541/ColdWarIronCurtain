# Diplomacy gating in CWIC — how it actually works

Why the diplomacy list looks the way it does, why some buttons are greyed, and
where volunteer permissions come from.

---

## 1. Two separate systems, two separate files

HOI4 gates each diplomatic action twice, and the two are easy to confuse.

| | Availability | Visibility |
|---|---|---|
| **Naming** | `DIPLOMACY_<ACTION>_ENABLE_TRIGGER` | `is_diplomatic_action_valid_<action>` |
| **File** | `common/scripted_triggers/diplomacy_scripted_triggers.txt` | `common/scripted_triggers/00_diplo_action_valid_triggers.txt` |
| **Effect when false** | button visible but **greyed**, with your tooltip explaining why | button **not shown at all** |
| **Action name case** | UPPERCASE (`SEND_VOLUNTEERS`) | lowercase (`send_volunteers`) |

Use availability when the player should see the thing exists and learn why they
cannot do it. Use visibility to delete an action from the mod entirely.

**Both hooks are optional.** If nobody defines one, the game just doesn't call
it and uses its own logic. So "not found in vanilla" does NOT mean the hook does
not exist — it means vanilla had no use for it. There are ~44 known availability
hooks; vanilla defines 24.

## 2. Scopes inside these triggers

```
ROOT  = the country doing the action   (the sender)
FROM  = the country it is done to      (the target)
```

Both sides are available, which is what makes per-pair rules possible:
"USA may send volunteers to VIN but not to CUB" is expressible.

## 3. The replacement hazard

A mod file at the same path **replaces vanilla's entirely** — it does not merge.
Our `diplomacy_scripted_triggers.txt` is 9.7 KB against vanilla's 43.9 KB, so
every vanilla rule we did not copy across simply stopped existing.

Two had been lost this way and are now restored: the Philippines/USA permanent
naval base rule and the Iraq/England Anglo-Iraqi treaty rule, both of which
govern revoking offered docking and air base rights.

**When touching this file, diff against vanilla first.**

## 4. What CWIC currently blocks

Deliberate design decisions, not bugs:

| Action | State |
|---|---|
| Guarantee independence | **blocked** (`always = no`, tooltip `RULE_GUARANTEE_BLOCKED_TT`) |
| Release nation | **blocked** |
| Revoke guarantee | allowed |
| Vanilla embargo | **hidden** — replaced by our own `opt_embargo_action` |
| Military / docking / air base access (ask + offer) | **hidden**, all six — replaced by `opt_military_cooperation_action` |
| Licensed production | greyed out unless **both sides are human** |
| Boost party popularity, stage coup | **hidden** (La Résistance operations replace them) |

## 5. Volunteers — the one that matters

`DIPLOMACY_SEND_VOLUNTEERS_ENABLE_TRIGGER` decides, for each sender/target pair,
whether the Send Volunteers button is usable. A country may send volunteers to a
target if **any** of:

1. **Same sphere** — `ROOT.Sphere_Leader = FROM.Sphere_Leader`
2. **Sphere leader, target in our faction** — we lead a sphere and they are a
   faction ally
3. **Explicit licence** — `ROOT.Volunteer_Allowance^FROM > 0`

The third is the interesting one. `Volunteer_Allowance` is an array on the
sender, indexed by target tag. Any positive value is a licence for that pair.

```
# In a focus: lets the USSR send volunteers to North Korea
set_variable = { Volunteer_Allowance^KPA = 1 }
```

Written in **33 places across 22 focus trees** — Korea, the Chinese and Greek
civil wars, Malaya, Vietnam, Singapore. It used to be that **nothing ever cleared it** — a licence granted in 1950 still
stood in 1989. `cwic_proxy_close` now wipes the USA/SOV entry when the war that
justified it ends, *unless* the patron holds a standing Defence Commitment, which
is a licence somebody paid for and which is revoked by its own action.

Also note the volunteer floor is lowered mod-wide:

```
vanilla:  VOLUNTEERS_DIVISIONS_REQUIRED = 30
CWIC:     VOLUNTEERS_DIVISIONS_REQUIRED = 1
```

So the army-size barrier is effectively gone; this trigger is the real gate.

### Fixed just now

The licence check read `= 1` exactly, but seven grants use `5`, `10` or `20` —
including the Soviet Korean War branch and the Chinese and Greek civil war
branches. Those grants did nothing. Changed to `> 0`, which repairs all seven
without touching the focus files. The larger numbers still read as though
someone meant "how many divisions" — they do not do that, they are just truthy.

## 5b. Everything costs Political Power

There is no second currency. Diplomatic Power was built and then removed: PP is
the one pool, and foreign policy competes with construction, advisors and laws
for it. Scripted diplomatic actions express this through the engine's own
`cost` field, which greys the button out and writes the price into the tooltip
by itself — so **never** hand-roll a `custom_trigger_tooltip` for a PP cost.

| Action | PP | Why |
|---|---|---|
| Recall Volunteers | 0 | de-escalation is never gated |
| Revoke Military Cooperation | 0 | walking away from a base is free |
| Lift Embargo | 25 | vanilla revoke is 0; a token price stops yo-yoing |
| Military Cooperation Accord | 50 | transit + ports + airfields in one signature |
| Revoke Defence Commitment | 50 | breaking your word costs something |
| Embargo | 75 | vanilla is 100, ours also cancels trade |
| Defence Commitment | 100 | the guarantee **and** the volunteer licence |

Vanilla anchors for comparison: `GUARANTEE_COST = 15`, `EMBARGO_COST = 100`.

`custom_cost_trigger` / `custom_cost_text` — the money-cost path — works on
**decisions only**, not on diplomatic actions. A diplomatic action that must
cost something other than PP or CP has to be `cost = 0` plus a
`custom_trigger_tooltip` in `selectable` and the spend in `complete_effect`.

## 6. Known quirks

- `DIPLOMACY_GUARANTEE_ENABLE_TRIGGER_OVERRIDES_GAME` (line 32) is missing the
  `_TRIGGER` suffix, so the game never calls it. Harmless today, because the
  main guarantee trigger blocks guarantees anyway — but it is dead code that
  looks live. Renaming it is a **design decision** about whether cross-ideology
  guarantees should exist, not a typo fix.
- Rule 1 (same sphere) now depends on `Sphere_Leader`, which since the influence
  system was removed is **flavour set by content**, not maintained by any system.
  It still works, but only for countries whose content actually sets it.

## 7. Adding a new gate

```
DIPLOMACY_<ACTION>_ENABLE_TRIGGER = {
    if = {
        limit = { tag = USA  FROM = { tag = CUB } }
        custom_trigger_tooltip = {
            tooltip = MY_REASON_TT
            always = no
        }
    }
}
```

Wrap conditions in `if = { limit = ... }` so the tooltip only appears for the
pair it concerns, rather than on every country pair in the game.
