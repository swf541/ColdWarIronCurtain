# Diplomatic Power (DP) — content designer API

One national currency for everything outside our borders. Political Power for
foreign affairs. It accrues monthly and **content spends it** — decisions,
diplomatic actions, events. There is deliberately no system behind it: no score
per country, no slots, no accord ladder, no AI manager.

Spheres, pacts, alignments and blocs are **flavour you write**, not mechanics
the engine enforces.

---

## 1. The variable

`diplomatic_power` — a plain country variable, 0 to 500.
`dp_income` — what was earned last month (for tooltips).

Check it like any variable:

```
check_variable = { diplomatic_power > 99 }
```

## 2. Spending it

**On a decision** — use the engine's custom cost so the player sees the price
on the button (this is the same pattern CAM.txt already uses for money):

```
USA_back_the_colonels = {
    icon = generic_political_actions
    visible = { ... }
    custom_cost_trigger = { check_variable = { diplomatic_power > 149 } }
    custom_cost_text = dp_cost_150
    complete_effect = {
        set_temp_variable = { dp_cost = 150 }
        dp_spend = yes
        GRE = { country_event = my_coup.1 }
    }
}
```

**Anywhere else** (events, focuses, diplomatic actions):

```
set_temp_variable = { dp_cost = 75 }
dp_spend = yes
```

## 3. Granting it

```
set_temp_variable = { dp_amount = 50 }
dp_gain = yes
```

## 4. Modifiers you can hand out

Both are already registered and already granted by existing content:

| Modifier | Effect |
|---|---|
| `foreign_influence_modifier` | percentage on monthly income (`0.25` = +25%) |
| `influence_gain_flat` | flat points per month |

## 5. Income

```
3  + factories/20  + subjects*2  + nukes*0.5,  then modifiers.  Cap 500.
```

Rough targets: superpower 15-25/month, middle power 5-8, minor 3-4.
Tune in `cwic_dp_monthly` — it is the only place income is decided.

## 6. Suggested price bands

Not enforced anywhere. Keep them roughly consistent across the mod:

| Band | Cost | Examples |
|---|---|---|
| Small | 25-50 | propaganda, a trade deal, a state visit |
| Medium | 75-150 | arms transfer, basing rights, swing an election |
| Large | 200-300 | back a coup, bring a country into your bloc |
| Huge | 400+ | pull a country out of a rival's bloc |

A superpower earning ~20/month can afford a coup roughly once a year, or several
small moves. That is the intended pace — spending should hurt.

## 7. Spheres are now yours

The old sphere machinery is gone, but the variables 41 content files already use
are untouched and still mean exactly what they meant:

```
set_variable = { Sphere_Leader = USA.id }        # who they follow
add_to_array = { sphere_tag_list = GRE.id }      # USA's member list
set_country_flag = Is_In_Sphere
```

Nothing enforces them any more. If you want joining a sphere to require an
election, a coup and a trade pact, write those three decisions and set the
variable at the end. If you want it to cost 300 Diplomatic Power, charge it.

## 8. Colour

Everything DP-facing is **light green** — `§G` in localisation. Costs, gains,
the topbar number and any tooltip that mentions it. The display name lives only
in `dp_name` / `dp_name_short`, so switching between "Diplomatic Power" and
"Diplomatic Projection" is a two-line edit in
`localisation/english/CWIC_diplomatic_power_l_english.yml`.
