# Binh-Xuyen Revolt Unification - COMPLETE

Status: **done**. Both of Diem's premiership routes now fight the same war on
the CCC tag. This document is a record of the finished mechanic, not a task
list.

---

## The problem this solved

The Binh-Xuyen existed twice, in two unrelated implementations:

- **Bao-Dai / Diem route** modelled them abstractly - the Battle of Saigon and
  the Hoang-Dieu Campaign were events that only moved VIE country variables
  (`Binh_Xuyen_Annihilation`, `Binh_Xuyen_Loyalty`, `VIE_Warlord_Status_2`) and
  flags. No country spawned, no war was fought.
- **Cuong-De route** (`VIE_NH_Diem_Destroy_Org_Crime`) spawned a real
  belligerent on the CCC tag and declared war - but wrote none of the sect
  variables, and nothing ever resolved the war. After winning it the sect GUI,
  the referendum score, the Geneva branch and the sitrep loc all still reported
  the Binh-Xuyen as intact.

Resolution: **one** CCC-based mechanic, with the war authoritative and the
existing variable/flag layer driven from it, so every pre-existing reader keeps
working untouched.

---

## The mechanic as built

```
phase 1  spawn, Cholon contested     VIE_spawn_binh_xuyen_revolt[_full]
   |                                 (Diem.2.a / VIE_NH_Diem_Destroy_Org_Crime)
   v     VIE retakes Cholon 13709
phase 2  Rung-Sac pocket             VIE_binh_xuyen_retreat_to_rung_sac
   |                                 (Diem.42, via the daily watcher)
   v     CCC beaten
end      revolt resolved             VIE_finish_the_binh_xuyen
                                     (on_capitulation / on_annex, or Diem.40.a)
```

### State

| Flag | Scope | Meaning |
| --- | --- | --- |
| `CCC_Binh_Xuyen_Revolt` | CCC | this revolt, as distinct from the 1949 Cochinchina state and from `CCC_Phuong_Mutiny` |
| `VIE_Binh_Xuyen_Rung_Sac` | VIE | phase 2 active (pre-existing, 5 readers) |
| `VIE_Hoang_Dieu_Complete` | VIE | revolt resolved (pre-existing; repurposed, it had one tooltip reader) |
| `crushed_binh_xuyen` | VIE | set by `VIE_dismantle_binh_xuyen` at the end, as before |

### Effects - `common/scripted_effects/Vietnam_effects.txt`

All under one header block, next to the older Binh-Xuyen effects.

- **`VIE_binh_xuyen_revolt_shell`** - shared setup, no territory or OOB. Flags
  CCC, sets the cosmetic tag and politics, moves Le-Van-Vien and gives him the
  leader role (both guarded on `has_character`), strips the three
  `CCC_cochinchina_*` dynamic modifiers, sets `VIE_Warlord_Status_2 = 2`.
- **`VIE_spawn_binh_xuyen_revolt`** - Diem route. Transfers 1754 Phuoc Tuy,
  takes control of 13709 Cholon, `load_oob = CCC_Binh_Xuyen_Cholon`, declares
  war.
- **`VIE_spawn_binh_xuyen_revolt_full`** - Cuong-De route. Same, plus control of
  13707 Rung-Sac and the original full `CCC_Binh_Xuyen` order of battle.
- **`VIE_binh_xuyen_retreat_to_rung_sac`** - wraps the pre-existing
  `VIE_binh_xuyen_driven_from_saigon` (Warlord_Status 2, annihilation 100 -> 30,
  loyalty +20, Rung-Sac flag) and adds the territorial half: control of 13707
  and `load_oob = CCC_Binh_Xuyen_RungSac`.
- **`VIE_binh_xuyen_revolt_watcher`** - on `on_daily_VIE`. Fires `Diem.42` six
  hours after CCC stops controlling 13709. Serves both routes.
- **`VIE_finish_the_binh_xuyen`** - body unchanged (zero annihilation, clear
  Rung-Sac, set `VIE_Hoang_Dieu_Complete`, `VIE_dismantle_binh_xuyen`). Now also
  winds up the shell: leader role removed, nationality returned to VIE, revolt
  flag cleared, CCC annexed. Guarded on `country_exists` so it cannot recurse
  with the `on_annex` hook.

### Why Phuoc Tuy is transferred on both routes

A country that owns no state does not exist and cannot be declared war on.
State 1754 is the owned rump that makes CCC a legal belligerent; Cholon (13709,
inside VIE-owned Gia Dinh 286) is held by *control* only and is the prize of
phase 1. This is why the "Cholon first" design still starts with a state
transfer.

### Resolution hook - `common/on_actions/VIE_on_actions.txt`

Blocks in **both** `on_capitulation` and `on_annex`, beside the existing
`CCC_Phuong_Mutiny` precedent, gated on `CCC_Binh_Xuyen_Revolt` + `FROM = VIE` +
VIE not already holding `VIE_Hoang_Dieu_Complete`. CCC is not in
`ic_failsafe_active_trigger`'s tag list, so the explicit `annex_country` inside
the finish effect is what keeps a vanilla peace conference from opening.

### CCC tag hygiene

`history/countries/CCC - Cochinchina.txt` boots the 1949 colonial state. The
revolt shell therefore removes the three `CCC_cochinchina_*` dynamic modifiers,
and `common/national_focus/CCC_50s.txt` now carries a `factor = 0` modifier on
`has_country_flag = CCC_Binh_Xuyen_Revolt` so the revolt does not inherit the
Cochinchina focus tree.

`common/ai_strategy/CCC_Binh_Xuyen.txt` is new: theatre demand on 1754 and 286,
careful front control, and `conquer`/`invade` VIE at -1000 so the revolt
garrisons instead of marching on Saigon.

### Order of battle

`history/units/CCC_Binh_Xuyen.txt` is unchanged and still serves the Cuong-De
route. Two new files, each redeclaring the templates it uses (`create_unit`
fails with "Malformed token" if the owner never loaded the template):

| File | Deployment |
| --- | --- |
| `CCC_Binh_Xuyen_Cholon.txt` | 3 divisions at 13709 Cholon, 1 at 13705 Phuoc Tuy |
| `CCC_Binh_Xuyen_RungSac.txt` | 2 divisions at 13707 Rung-Sac |

Adjacency was verified against `map/provinces.bmp` / `map/definition.csv`:
13705 borders 13707, so the pocket stays supply-connected.

### Events

- **`Diem.2.a`** now calls `VIE_spawn_binh_xuyen_revolt` instead of resolving
  the fight abstractly. `Diem.2.b` (negotiate) is untouched and still leaves no
  pocket.
- **`Diem.42`** is new - the Rung-Sac withdrawal. Loc at
  `VIE_events_l_english.yml`. Note `Diem.4` was already taken.
- **`Diem.40.a`** unchanged; it is now the scripted way to end the pocket war,
  and annexes CCC through the extended finish effect.
- **`CuongDe_NgoDinh.20`** had full loc but an empty payload. It now carries the
  crackdown's cost (PP -50, stability -0.05, war support +0.10, influence +15),
  matching `Diem.2.a`.

---

## Deliberate deviations from the original plan

1. **Hoang-Dieu `available` was left alone.** The plan called for a "CCC no
   longer controls 13707" progress gate. CCC capitulates the moment its last
   ground falls, so that gate would only open after the war had already
   resolved, making the focus unreachable. The focus instead remains the
   scripted conclusion of the pocket war.
2. **Bug fixed in passing:** the Hoang-Dieu bypass ("Battle of Saigon done, no
   Rung-Sac flag, past 1955.09.01") would have skipped the focus for any player
   still fighting phase 1 in September. `NOT = { has_war_with = CCC }` was added
   to that AND.

Also cleaned up: the duplicate empty `completion_reward = { }` blocks on
`VIE_NH_Diem_Destroy_Org_Crime` and `VIE_NH_Diem_Disarm_Religious_Private_Armies`.
Harmless only because the first block was empty - a duplicate
`completion_reward` silently drops the earlier one.

---

## Files changed

```
M  common/national_focus/CCC_50s.txt                  # tree gated off the revolt flag
M  common/national_focus/VIE_50s_Bao_Dai.txt          # Hoang-Dieu bypass fix
M  common/national_focus/VIE_50s_CuongDe.txt          # calls the shared effect, dup cleanup
M  common/on_actions/VIE_on_actions.txt               # daily watcher + capitulation/annex hooks
M  common/scripted_effects/IC_Geneva_Test_Effects.txt # test_vie_binh_xuyen_* harness
M  common/scripted_effects/Vietnam_effects.txt        # the mechanic
M  events/VIE_Events.txt                              # Diem.2.a, Diem.42, CuongDe_NgoDinh.20
M  localisation/english/VIE_events_l_english.yml      # Diem.42
M  localisation/english/VIE_misc_l_english.yml        # VIE_binh_xuyen_revolt_tt
A  common/ai_strategy/CCC_Binh_Xuyen.txt
A  history/units/CCC_Binh_Xuyen_Cholon.txt
A  history/units/CCC_Binh_Xuyen_RungSac.txt
```

Earlier in the same work: `CCC_Binh_Xuyen` cosmetic tag added to
`common/countries/cosmetic.txt` with loc in
`Indochina_minorities_misc_l_english.yml`, the OOB fixed and expanded, and the
dead `history/units/Cao_Dai_Militias.txt` deleted.

---

## Not yet verified in-game

Braces balance, loc BOMs are intact and no BOM was introduced into any script
file. The phase transitions and the CCC shell reset still need a run.

Console harness: `e test_vie_binh_xuyen_spawn`, `e test_vie_binh_xuyen_rungsac`,
`e test_vie_binh_xuyen_resolve`.

1. Diem route: Battle of Saigon -> `Diem.2.a`. CCC should appear as "Binh-Xuyen"
   (grey, correct flag, no Cochinchina focus tree), at war, divisions in Cholon.
2. Take Cholon. `Diem.42` fires once; CCC holds 1754 + 13707; annihilation 30;
   Hoang-Dieu available from 1955.09.01.
3. Clear the pocket. Expect `crushed_binh_xuyen`, `VIE_Warlord_Status_2 = 3`,
   annihilation 0, no peace conference, sect GUI and `GetVIESitrepBinhXuyen`
   both reading "crushed", referendum score +30.
4. Re-run with `Diem.2.b`: no war, no CCC, Hoang-Dieu bypasses via
   `VIE_Diem_No_Rung_Sac_Pocket_tt`.
5. Cuong-De regression: `VIE_NH_Diem_Destroy_Org_Crime` spawns as before plus
   the new variable wiring, and winning now sets `crushed_binh_xuyen`.
6. `error.log` clean of new entries.
