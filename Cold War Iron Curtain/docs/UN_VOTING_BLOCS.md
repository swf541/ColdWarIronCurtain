# UN Voting Blocs — content designer guide

Countries vote in blocs at the UN. The player lobbies a **bloc leader**, not
fifty individual countries: one purchase, one bloc.

Blocs are **authored**. Nothing computes them from ideology, faction or sphere.
A bloc exists because a content file said so, and it changes because an event,
decision or focus said so. They are a separate axis from factions and spheres
on purpose — Egypt can lead the Arab bloc while sitting in nobody's sphere.

## API

All of these live in `common/scripted_effects/CWIC_un_blocs.txt`.

```
EGY = { cwic_make_bloc_leader = yes }     # EGY now leads a bloc
EGY = { cwic_clear_bloc_leader = yes }    # EGY stops; its members are released

set_temp_variable = { cwic_new_bloc = EGY.id }
SYR = { cwic_join_bloc = yes }            # SYR follows EGY at the UN

SYR = { cwic_leave_bloc = yes }           # SYR votes for itself again
```

## Triggers

```
has_country_flag = cwic_bloc_leader            # leads a bloc
check_variable = { cwic_bloc_leader_of = X }   # follows X
has_variable = un_pledged_to                   # has been lobbied by someone
```

## Starting blocs, 1949

Set once at `on_startup`, deliberately sparse — these are the groupings that
actually voted together at the outset.

| Bloc | Leader | Members |
|---|---|---|
| Arab League | EGY | SYR IRQ SAU LEB YEM JOR |
| Latin America | BRA | ARG CHL COL PER VEN MEX CUB URG BOL ECU PAR GUA HON NIC COS PAN DOM HAI ELS |
| South Asia | RAJ | PAK CEY BRM |
| Nordic | SWE | NOR DEN FIN ICE |

Africa is absent because most of it is still colonial in 1949, and the
Non-Aligned Movement is six years from Bandung. Both are content's to create as
they form — that is the point of authoring rather than computing.

## How a bloc actually votes

`cwic_un_apply_pledges` (in `CWIC_un_pledges.txt`) runs from each of the four
vote buttons. A country follows the player if **either**:

- it is the bloc leader the player lobbied, **or**
- its `cwic_bloc_leader_of` points at a leader the player lobbied

A patron's veto reads as a NO to everyone following them. Nobody follows a
patron into condemning themselves — the resolution's own target is excluded.

Pledges last 730 days, tracked by the `un_pledged` country flag.
`UN_RESET_VOTE_STATE` clears the variable once the flag lapses.

## Why it is applied at vote time, not at tally time

The AI tallies when the resolution **starts** — `UN_START_SCRIPTED_RESOLUTION`
runs `UN_ai_vote_sorting` over every member in one pass. The player votes during
the ten days that follow. So a pledge term inside `un_ai_vote_weights` could
never see the player's vote flag; it had already been read, and every bought
vote was silently ignored. Pledges are applied from the vote buttons instead.
