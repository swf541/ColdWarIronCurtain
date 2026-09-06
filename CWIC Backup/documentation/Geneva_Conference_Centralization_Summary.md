# Geneva Conference Centralization - Summary

## Overview
The Geneva Conference system has been centralized to eliminate duplicate logic and provide a single source of truth for when and how Geneva Conference is triggered.

## Centralized Components

### 1. Centralized Triggers (`common/scripted_triggers/IC_struggle_triggers.txt`)

**`indochina_struggle_ending_geneva_trigger`**
- **Purpose**: Determines when Geneva Conference ending should be available
- **Conditions**:
  - Struggle hasn't ended yet (`NOT has_global_flag = Indochina_War_Over`)
  - AND either:
    - Phase = 8 (Low Tension) AND date > 1953.1.1, OR
    - Date > 1954.7.1 AND phase < 9

**`geneva_conference_available_trigger`**
- **Purpose**: Checks if Geneva Conference has already been triggered
- **Condition**: `has_global_flag = Geneva_Conference`

**`geneva_conference_should_be_available_trigger`**
- **Purpose**: Checks if Geneva Conference should be available (before triggering)
- **Conditions**: 
  - `indochina_struggle_ending_geneva_trigger = yes`
  - AND `NOT has_global_flag = Geneva_Conference`

### 2. Centralized Effect (`common/scripted_effects/CWIC_Struggle_Effects.txt`)

**`indochina_struggle_trigger_geneva_conference`**
- **Purpose**: Single effect that triggers Geneva Conference
- **Actions**:
  - Sets `Geneva_Conference` global flag
  - Sets phase to 11 (Geneva Conference phase)
  - Fires `Geneva_conference.1` news event
  - Auto-completes relevant focus trees:
    - `VIN_The_Geneva_Peace_Conference`
    - `FRA_Geneva_Peace_Conference`
    - `USA_50s_The_Geneva_Conferece`
    - `GC_Geneva_Peace_Conference` (for all involved nations)

## Updated Files

### Focus Trees
1. **`VIN_50s.txt`** - `VIN_The_Geneva_Peace_Conference`
   - Now uses `geneva_conference_should_be_available_trigger` for availability
   - Calls `indochina_struggle_trigger_geneva_conference` on completion

2. **`FRA_1950s.txt`** - `FRA_Geneva_Peace_Conference`
   - Now uses `geneva_conference_should_be_available_trigger` for availability
   - Auto-bypasses if `geneva_conference_available_trigger` is true
   - Calls `indochina_struggle_trigger_geneva_conference` on completion

3. **`USA_FP_50s.txt`** - `USA_50s_The_Geneva_Conferece`
   - Now uses `geneva_conference_should_be_available_trigger` for availability
   - Auto-bypasses if `geneva_conference_available_trigger` is true
   - Calls `indochina_struggle_trigger_geneva_conference` on completion

4. **`Geneva_Conference.txt`** - `GC_Geneva_Peace_Conference` (shared focus)
   - Now uses `geneva_conference_available_trigger` instead of direct flag check

5. **`VIE_50s_Bao_Dai.txt`** - `VIE_Accept_Geneva_Conference`
   - Now uses `geneva_conference_available_trigger` instead of direct flag check

6. **`VIE_50s_Military_CD.txt`** - Focus requiring Geneva
   - Now uses `geneva_conference_available_trigger` instead of direct flag check

7. **`VIE_50s_Military.txt`** - Focus requiring Geneva
   - Now uses `geneva_conference_available_trigger` instead of direct flag check

### Decisions
1. **`FRA.txt`** - `The_Geneva_Accords`
   - Now uses `geneva_conference_should_be_available_trigger` for availability
   - Calls `indochina_struggle_trigger_geneva_conference` on completion
   - Still handles historical state transfers and peace treaties (kept separate from centralized effect)

### On Actions
1. **`CWIC_Struggle_on_actions.txt`** - `on_daily_FRA`
   - Added automatic Geneva Conference triggering when phase reaches 8 (Low Tension)
   - Added automatic Never Ending Conflict ending when phase reaches 9
   - Added automatic Failed State ending when phase reaches 10

## Benefits

1. **Single Source of Truth**: All Geneva Conference logic is centralized in triggers and effects
2. **No Duplication**: Eliminates multiple implementations doing the same thing
3. **Consistency**: All focus trees and decisions use the same triggers
4. **Automatic Integration**: Phase system automatically triggers Geneva when conditions are met
5. **Easier Maintenance**: Changes to Geneva logic only need to be made in one place

## How It Works

1. **Triggering Geneva Conference**:
   - Can be triggered via:
     - Focus tree completion (VIN, FRA, USA)
     - Decision (`The_Geneva_Accords`)
     - Automatic phase transition (when phase reaches 8)
   
2. **All triggers call** `indochina_struggle_trigger_geneva_conference` which:
   - Sets the global flag
   - Updates phase
   - Fires events
   - Auto-completes relevant focus trees

3. **Availability checks**:
   - Focus trees use `geneva_conference_should_be_available_trigger` to check if they should be available
   - Focus trees use `geneva_conference_available_trigger` to auto-bypass if already triggered

## Notes

- The historical Geneva Accords decision (`The_Geneva_Accords`) still contains state transfer and peace treaty logic - this is intentional as it's specific to the historical outcome
- The centralized effect handles the flag, phase, events, and focus completion
- All focus trees that depend on Geneva Conference being triggered now use the centralized trigger

