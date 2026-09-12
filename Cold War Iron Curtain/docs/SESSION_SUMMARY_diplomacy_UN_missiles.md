# CWIC — Diplomacy, UN & Missiles: what changed

A working session's worth of changes across the diplomatic layer, the UN, the
proxy-war system and a new missile designer. Written for someone who did not
watch it happen.

---

## 1. The influence system is gone, and nothing replaced it

Influence was removed. A second currency (**Diplomatic Power**) was built to
replace it, then deleted too — the conclusion was that a new mana bar is the
wrong answer when Political Power already exists and already has nothing to
compete for it.

**Everything foreign-policy now costs Political Power**, through the engine's
own `cost` field on diplomatic actions:

| Action | PP |
|---|---|
| Recall Volunteers | 0 |
| Revoke Military Cooperation | 0 |
| Lift Embargo | 25 |
| Military Cooperation Accord | 50 |
| Withdraw Guarantee | 50 |
| Impose Embargo | 75 |
| **Guarantee Independence** | 100 |
| **Secure Their Bloc** (UN) | 100 |

Vanilla anchors for comparison: guarantee 15, embargo 100, and a permanent
member burns 250 PP to veto a UN resolution.

Also deleted: `influence_scripted_diplomatic_actions.txt`, 785 lines of which
10 of 11 actions were `visible = { always = no }` — dead since influence went,
still parsed every launch. The one live action (a sphere leader clearing a
client's debt) survives as `CWIC_sphere_debt_action.txt`.

**Alignment and spheres were deliberately left alone.** They are content's to
set, and nothing the player does moves a country between blocs.

---

## 2. The diplomacy panel is much shorter

Removed outright: guarantee independence (replaced by ours), licensed
production, market access, expeditionary forces (all three), naval blockade,
and the six separate vanilla access requests.

**Military Cooperation Accord** replaces those six with one signature —
transit, ports and airfields together, because nobody in this era signed for
one and refused the others.

**Guarantee Independence** is ours now, and it is a different promise from
vanilla's. It does **not** drag you into their war. What it does:

- writes the volunteer licence, so you *and every member of your faction* can
  send volunteers there
- opens lend-lease to them
- tells your AI allies to actually *want* to go

That last point mattered more than expected — see §6.

Faction leaders only, since it speaks for a whole bloc.

**Embargo** is one button now. "Embargo" and "Impose Naval Blockade" were the
same engine mechanic under two names the whole time.

**Lend-lease** is free for everyone — the old gate was "same sphere", which
since the influence removal meant `0 = 0` and therefore let every unsphered
pair through while blocking every sphered one. Exactly backwards.

---

## 3. The UN stopped being a vending machine

The 17 player-proposable resolutions are **deleted**, along with the resolution
dropdown, the target and state pickers and the submit button. `UN_Tab.txt` went
1,526 → ~1,070 lines, the GUI 1,094 → 872.

The reasoning: any number of buttons on a vending machine is the wrong number,
because the interesting question — *should this be on the table at all?* — was
never asked. Resolutions now only **arrive**, through the weekly check that
already existed and was only ever watching the calendar.

What the player does instead:

- **votes**, and decides whether to burn the veto
- **buys blocs**

**Voting blocs are authored.** Nothing computes them from ideology or spheres.
A bloc exists because a content file said so and changes because an event,
decision or focus said so. Starting set: Arab League (EGY), Latin America
(BRA — twenty votes, and the reason the US could carry the General Assembly at
will), South Asia (RAJ), Nordic (SWE). No African bloc and no Non-Aligned
Movement, because in 1949 neither exists yet — those are content's to create as
they form.

```
EGY = { cwic_make_bloc_leader = yes }
set_temp_variable = { cwic_new_bloc = EGY.id }
SYR = { cwic_join_bloc = yes }
```

**Bloc cohesion now actually drives votes.** The AI's vote weighting was reading
`influence_array` for ±200 — an array nothing has written since influence was
removed. So 400 points of bloc behaviour had silently stopped existing and every
country was voting as an individual. That now reads `Sphere_Leader`.

---

## 4. Proxy wars

The system watches every war and, when one bloc sends volunteers, gives the
other bloc an event demanding withdrawal. Refusing licenses the rival to arm
the other side.

It had **never run once**. The monthly sweep was hooked to `on_monthly`, which
is not a real on_action — only the per-country `on_monthly_<TAG>` form exists.
It also only ever saw wars declared *after* the game started, so every war
already running at the bookmark was invisible to it.

Both fixed, plus: the licence used to point at the theatre country itself —
licensing you to arm the side your rival was already propping up.

---

## 5. Missiles

A **missile designer**, built on the air designer. This took four attempts and
the reason is worth recording: the designer needs **both** a `type` it supports
**and** a registered blueprint, and CWIC ships all eight
`plane_blueprints_*.gui` as zero-byte files, which had deleted the blueprint
layer entirely. `missile` is not a designer-supported type — vanilla's own
`guided_missile_equipment` has no module slots and never opens a designer
either. So the missile is a strategic bomber to the engine and a missile to the
player: one-use, no crew, missile modules and art.

Four new techs in the existing rocket folder, each gated on By Blood Alone via
`allow_branch` (that is the DLC that adds the air designer — without it the
techs would unlock an airframe nobody could configure). Three new modules; the
airframe's slots already accept vanilla's bombs, jets, rocket engines and radar,
so it is additive to what players already research.

**Not yet wired to anything.** The intended three uses — tactical nukes,
pre-war strategic strikes, space launches — all ride the raid mechanic. See §8.

---

## 6. Bugs found in code that predates this session

Worth knowing about independently of anything above:

- **Infamy can only ever rise.** `subtract_from_variable = { badboy = -0.25 }`
  is a double negative. Every country's infamy has been climbing forever, and
  the clamp runs *before* the monthly additions so the 0–100 cap never applies.
- **Air volunteers were capped near zero.** The define was written as
  `AIR_VOLUNTEER_PLANES_LIMIT`; the real name is `..._RATIO`. A misspelled
  define is silently ignored, so it never applied. Now 0.75 (vanilla 0.2) and
  airbase capacity 1.0 (vanilla 0.1).
- **310 localisation keys are missing.** CWIC's `diplomacy_l_english.yml`
  fully replaces vanilla's and dropped 310 keys on the way, including both air
  volunteer strings and all four embargo relation descriptions — which is why
  the embargo appeared to do nothing, and why tooltips printed their own key
  names. The 23 relation strings are restored; the other ~285 are not.
- **13 localisation lines were missing the space before the quote**
  (`team_weapons_2:0"Team Weapons II"`). That is a hard parse error that kills
  the **rest of the file** — one was at line 13 of `ROC_l_english_.yml`, so
  nearly that whole file was dead. All fixed.
- `UN_Peacekeepers_Enabled` is set by three resolutions and read nowhere.
  Peacekeepers do nothing.
- Two fired UN resolution events (`.31`, `.32`) do not exist.
- The expanded 10-seat Security Council GUI is gated on a flag nothing sets.

---

## 7. Lessons that cost time, recorded so they do not cost it again

- **`ROOT = { ... }` does not execute** inside a scripted diplomatic action's
  `complete_effect`. The whole block is skipped silently. ROOT works as a
  *target*, not as a scope.
- **Effects reject event targets.** `give_guarantee`, `send_embargo`,
  `recall_volunteers_from` and friends document THIS/ROOT/PREV/FROM only.
  Passing `event_target:x` is a silent no-op — the action fires, variables
  update, and nothing happens.
- **Permission is not desire.** Opening a gate for the AI does nothing unless
  something also tells it to want the thing. Volunteers needed
  `send_volunteers_desire`; diplomatic actions need `ai_desire`.
- **A misspelled `is_diplomatic_action_valid_` token fails silently.** The game
  does log it — `lexer.cpp: Tried to get dynamic token that does not exist` —
  which is how six wrong guesses were caught.
- **`set_temp_variable` does not cross a scope change.**

---

## 8. Open decisions

1. **UN votes should run continuously.** Right now resolutions only arrive from
   four historical checks, all date-gated before 1950 — so after January 1950
   the UN never convenes and buying blocs buys nothing. The intent is a
   permanently running vote, mostly historical, with content able to supersede
   it, and votes awarding Cold War victory points.
2. **Missile uses.** Tactical nukes, pre-war strategic strikes and space
   launches all ride the raid mechanic. Raids *can* consume equipment
   (`essential_equipment`) and vanilla's `nuclear_missile_strike` is an exact
   template. The catch: **a raid can never target a country** — only a province,
   state or building. Space launches will target a launch-site province.
3. **Should the designer replace the existing missile equipment?** CWIC already
   has `icbm/irbm/srbm/slbm_equipment` with air units and nuclear raids wired to
   them. The designer currently sits alongside rather than folding into them.
4. **Map mode button icons** for the three new map modes (embargo, UN vote, UN
   blocs) need real art.
