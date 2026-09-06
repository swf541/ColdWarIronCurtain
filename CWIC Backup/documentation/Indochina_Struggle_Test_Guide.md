# Indochina Struggle Test Effects Guide

## Quick Start

Use these commands in the game console (press `~` to open console):

```
e <effect_name>
```

Example: `e test_indochina_reset`

## Test Effect Categories

### Setup & Reset
- `test_indochina_reset` - Reset everything to initial state
- `test_indochina_setup_initial` - Setup with balanced initial scores

### Phase Manipulation
- `test_indochina_set_phase_high_intensity` - Set to Phase 3
- `test_indochina_set_phase_medium_intensity` - Set to Phase 4
- `test_indochina_set_phase_low_intensity` - Set to Phase 5 (starting)
- `test_indochina_set_phase_high_tension` - Set to Phase 6
- `test_indochina_set_phase_medium_tension` - Set to Phase 7
- `test_indochina_set_phase_low_tension` - Set to Phase 8 (Geneva trigger)
- `test_indochina_set_phase_never_ending` - Set to Phase 9
- `test_indochina_set_phase_failed_state` - Set to Phase 10
- `test_indochina_set_phase_geneva` - Set to Phase 11 (Geneva active)
- `test_indochina_force_escalation` - Add 500 escalation points (triggers on daily tick)
- `test_indochina_force_deescalation` - Add 500 de-escalation points (triggers on daily tick)
- `test_indochina_manual_escalate` - Manually escalate phase (no daily tick needed)
- `test_indochina_manual_deescalate` - Manually de-escalate phase (no daily tick needed)

### Score Manipulation
- `test_indochina_set_communist_high` - Set Communist score to 2000
- `test_indochina_set_communist_low` - Set Communist score to 100
- `test_indochina_set_profrance_high` - Set Pro-France score to 2000
- `test_indochina_set_proindependence_high` - Set Pro-Independence score to 2000
- `test_indochina_set_proethnic_high` - Set Pro-Ethnic score to 2000
- `test_indochina_set_kuomintang_high` - Set Kuomintang score to 2000
- `test_indochina_add_communist_points` - Add 100 to Communist score
- `test_indochina_add_profrance_points` - Add 100 to Pro-France score
- `test_indochina_add_proindependence_points` - Add 100 to Pro-Independence score
- `test_indochina_add_proethnic_points` - Add 100 to Pro-Ethnic score
- `test_indochina_recalculate_anti_communist` - Recalculate total anti-communist score

### Ending Tests
- `test_indochina_trigger_communist_victory` - Test Communist Victory ending
- `test_indochina_trigger_southern_victory` - Test Southern Victory ending
- `test_indochina_unlock_southern_victory` - Test Southern Victory ending availability (checks conditions)
- `test_indochina_setup_southern_victory` - Setup Southern Victory conditions (scores and relations)
- `test_indochina_trigger_southern_victory` - Directly trigger Southern Victory ending (for testing effect)
- `test_indochina_unlock_federal_vietnam` - Test Federal Vietnam ending availability (checks conditions)
- `test_indochina_setup_federal_vietnam` - Setup Federal Vietnam conditions (scores)
- `test_indochina_trigger_federal_vietnam` - Directly trigger Federal Vietnam ending (for testing effect)
- `test_indochina_unlock_balkanized_vietnam` - Test Balkanized Vietnam ending availability (checks conditions)
- `test_indochina_setup_balkanized_vietnam` - Setup Balkanized Vietnam conditions (scores)
- `test_indochina_trigger_balkanized_vietnam` - Directly trigger Balkanized Vietnam ending (for testing effect)
- `test_indochina_unlock_kuomintang_victory` - Test Kuomintang Victory ending availability (checks conditions)
- `test_indochina_setup_kuomintang_victory` - Setup Kuomintang Victory conditions (scores)
- `test_indochina_trigger_kuomintang_victory` - Directly trigger Kuomintang Victory ending (for testing effect)
- `test_indochina_unlock_geneva` - Test Geneva Conference ending availability (checks conditions)
- `test_indochina_force_unlock_geneva` - Force unlock Geneva Conference (bypasses conditions)
- `test_indochina_unlock_never_ending` - Test Never Ending Conflict ending availability (checks conditions)
- `test_indochina_unlock_never_ending_phase` - Test Never Ending Conflict via Phase 9
- `test_indochina_force_unlock_never_ending` - Force unlock Never Ending Conflict (bypasses conditions)
- `test_indochina_trigger_never_ending` - Directly trigger Never Ending Conflict ending (for testing effect)
- `test_indochina_unlock_failed_state` - Test Failed State ending availability (checks conditions)
- `test_indochina_unlock_failed_state_phase` - Test Failed State via Phase 10
- `test_indochina_force_unlock_failed_state` - Force unlock Failed State (bypasses conditions)
- `test_indochina_trigger_failed_state` - Directly trigger Failed State ending (for testing effect)
- `test_indochina_unlock_dan_quoc_peace` - Test Dan Quoc Peace ending availability (checks conditions)
- `test_indochina_setup_dan_quoc_peace` - Setup Dan Quoc Peace conditions (scores and flag)
- `test_indochina_trigger_dan_quoc_peace` - Directly trigger Dan Quoc Peace ending (for testing effect)
- `test_indochina_unlock_american_north_vietnam` - Test American-North Vietnam ending availability (checks conditions)
- `test_indochina_setup_american_north_vietnam` - Setup American-North Vietnam conditions (focus and scores)
- `test_indochina_trigger_american_north_vietnam` - Directly trigger American-North Vietnam ending (bypasses event chain, for testing effect only)
- `test_indochina_full_american_north_vietnam_setup` - Complete setup with all conditions (Ho Chi Minh, opinions, scores, focus)
- `test_indochina_full_american_north_vietnam_ending` - End-to-end test (setup + auto-trigger)
- `test_indochina_trigger_reunification_chain` - Manually trigger first reunification event
- `test_indochina_advance_reunification_chain` - Check status of reunification event chain
- `test_indochina_verify_ending_available` - Verify ending is available after reunification completes

### GUI Tests
- `test_indochina_show_gui` - Show main struggle GUI
- `test_indochina_hide_gui` - Hide main struggle GUI
- `test_indochina_show_intro` - Show introduction popup
- `test_indochina_show_phase_prompt` - Show phase change prompt
- `test_indochina_show_ending_popup` - Show ending popup
- `test_indochina_show_phase_list` - Show phase list GUI

### Comprehensive Scenarios
- `test_indochina_scenario_communist_win` - Full Communist victory scenario
- `test_indochina_scenario_geneva` - Geneva Conference scenario
- `test_indochina_scenario_never_ending_date` - Never Ending Conflict via date condition
- `test_indochina_scenario_never_ending_phase` - Never Ending Conflict via Phase 9
- `test_indochina_scenario_failed_state_phase` - Failed State via Phase 10
- `test_indochina_scenario_failed_state_collapse` - Failed State via score collapse
- `test_indochina_scenario_dan_quoc_peace` - Dan Quoc Peace (Diem-Ho Reunification)
- `test_indochina_scenario_american_north_vietnam` - American-North Vietnam Diplomatic (A Gift From Truman)
- `test_indochina_scenario_southern_victory` - Southern Victory (A Quoc-gia Vietnam)
- `test_indochina_scenario_federal_vietnam` - Federal Vietnam
- `test_indochina_scenario_balkanized_vietnam` - Balkanized Vietnam (An Overgrown Garden)
- `test_indochina_scenario_kuomintang_victory` - Kuomintang Victory (White Star Over Vietnam)
- `test_indochina_scenario_failed_state_collapse` - Failed State via score collapse
- `test_indochina_scenario_escalation` - Escalation path scenario (manual, no loop)
- `test_indochina_scenario_deescalation` - De-escalation path scenario (manual, no loop)
- `test_indochina_scenario_escalation_with_points` - Escalation with points (triggers on daily tick)
- `test_indochina_scenario_deescalation_with_points` - De-escalation with points (triggers on daily tick)
- `test_indochina_scenario_all_endings` - All endings available (GUI testing)

### Debug/Info
- `test_indochina_debug_state` - Display current struggle state in log
- `test_indochina_debug_all_triggers` - Test all ending triggers and log results

### Southern Victory Focus Chain Testing
- `test_indochina_test_southern_victory_chain` - Full chain: setup → bypass focus → revolt event
- `test_indochina_setup_southern_victory_full_chain` - Setup conditions for full chain testing
- `test_indochina_bypass_liberator_focus` - Bypass VIE_BaoDai_Liberator_of_Vietnam and fire revolt event

## Common Test Workflows

### Test Phase Transitions
```
# Manual transition (recommended - no loop)
e test_indochina_reset
e test_indochina_set_phase_low_intensity
e test_indochina_manual_escalate
e test_indochina_debug_state

# Or use points (will trigger on daily tick, may cause loops)
e test_indochina_reset
e test_indochina_set_phase_low_intensity
e test_indochina_force_escalation
# Wait for daily tick
e test_indochina_debug_state
```

### Test Ending Conditions
```
e test_indochina_reset
e test_indochina_set_phase_medium_intensity
e test_indochina_set_communist_high
e test_indochina_recalculate_anti_communist
e test_indochina_trigger_communist_victory
```

### Test Geneva Conference
```
# Unlock Geneva (makes focuses/decisions available)
# NOTE: Geneva becomes available when at Phase 8 (Low Tension) AND de-escalation points > 500
# This represents trying to de-escalate from Phase 8 but can't go further, so Geneva becomes an option
# Phase stays at 8 (Low Tension) - Phase 11 is only set when the ending is triggered via GUI
e test_indochina_reset
e test_indochina_set_phase_low_tension
e test_indochina_unlock_geneva
e test_indochina_debug_state
# Then check GUI - Geneva ending should be available to click
# When you click it, phase will change to 11

# Or force unlock (bypasses conditions)
e test_indochina_reset
e test_indochina_force_unlock_geneva
e test_indochina_debug_state
# Then check GUI - Geneva ending should be available to click

# Directly trigger the ending (for testing the effect itself)
# This will set phase to 11 and fire the ending event
# NOTE: This bypasses the GUI - use for testing ending effects only
e test_indochina_reset
e test_indochina_trigger_geneva
```

### Test Never Ending Conflict
```
# Test via date condition (requires date > 1957.1.1)
e test_indochina_reset
e test_indochina_set_phase_medium_intensity
e test_indochina_unlock_never_ending
e test_indochina_debug_state
# Then check GUI - Never Ending Conflict ending should be available to click

# Test via Phase 9 (direct)
e test_indochina_reset
e test_indochina_unlock_never_ending_phase
e test_indochina_debug_state
# Then check GUI - Never Ending Conflict ending should be available to click

# Or force unlock (bypasses conditions)
e test_indochina_reset
e test_indochina_force_unlock_never_ending
e test_indochina_debug_state
# Then check GUI - Never Ending Conflict ending should be available to click

# Direct trigger (for testing ending effect)
e test_indochina_reset
e test_indochina_trigger_never_ending
```

### Test Failed State
```
# Test via score collapse condition (requires date > 1955.1.1 and all scores < 500)
e test_indochina_reset
e test_indochina_set_phase_medium_intensity
e test_indochina_unlock_failed_state
e test_indochina_debug_state
# Then check GUI - Failed State ending should be available to click

# Test via Phase 10 (direct)
e test_indochina_reset
e test_indochina_unlock_failed_state_phase
e test_indochina_debug_state
# Then check GUI - Failed State ending should be available to click

# Or force unlock (bypasses conditions)
e test_indochina_reset
e test_indochina_force_unlock_failed_state
e test_indochina_debug_state
# Then check GUI - Failed State ending should be available to click

# Direct trigger (for testing ending effect)
e test_indochina_reset
e test_indochina_trigger_failed_state
```

### Test Dan Quoc Peace
```
# Test Dan Quoc Peace ending availability
e test_indochina_reset
e test_indochina_unlock_dan_quoc_peace
e test_indochina_debug_state
# Note: Requires Ngo Dinh Diem in power in VIE and Ho Chi Minh in power in VIN
# Note: Requires dan_quoc_peace flag to be set (normally via focus/event) *Currently not available, set via set_global_flag in console
# Then check GUI - Dan Quoc Peace ending should be available to click

# Setup conditions (scores and flag)
e test_indochina_reset
e test_indochina_setup_dan_quoc_peace
e test_indochina_debug_state
# Note: Still need to ensure leaders are in power
# Note: If White Star Over Vietnam shows as active, ensure you're playing as VIE or VIN (not PQC)
# Note: The test setup now explicitly sets Kuomintang score to 0 to prevent accidental triggers

# Direct trigger (for testing ending effect)
e test_indochina_reset
e test_indochina_trigger_dan_quoc_peace
```

### Test American-North Vietnam Diplomatic (Full Event Chain)
```
# COMPLETE END-TO-END TEST (Recommended)
# This sets up all conditions and triggers the full reunification event chain
e test_indochina_reset
e test_indochina_full_american_north_vietnam_ending
# This will:
# - Complete USA focus USA_50s_Reestablish_Deer_Team
# - Set up all required scores (Communist > 2x Anti-Communist, > 500)
# - Ensure Ho Chi Minh is in power in VIN
# - Set positive opinions between USA and VIN
# - Ensure VIN favors USA over SOV
# - Ensure USA and VIN are not at war
# The reunification event chain should trigger automatically via on_daily_FRA
# After all events complete, the ending will be available in GUI

# STEP-BY-STEP TESTING
# Step 1: Full setup (sets up all conditions)
e test_indochina_reset
e test_indochina_full_american_north_vietnam_setup
e test_indochina_debug_state
# Wait for daily tick - event chain should trigger automatically
# If it doesn't, proceed to Step 2

# Step 2: Manually trigger first reunification event (if needed)
e test_indochina_trigger_reunification_chain
# This fires USA_VIN_Reunification.1 for USA
# Events will chain: .2 (VIN) → .3 (USA) → .4 (VIE) → .5/.6 (VIN) → .7 (USA) → .8 (VIN)

# Step 3: Check chain progress
e test_indochina_advance_reunification_chain
# Shows status of the event chain

# Step 4: Verify ending is available after reunification completes
e test_indochina_verify_ending_available
# Opens GUI and verifies ending is available
# Ending should be clickable in GUI after USA_VIN_Reunification.8 completes

# QUICK AVAILABILITY TEST (Old method - doesn't test event chain)
e test_indochina_reset
e test_indochina_unlock_american_north_vietnam
e test_indochina_debug_state
# Note: This only checks if conditions are met, doesn't set up full chain
# Note: Ending will be LOCKED until reunification event chain completes

# DIRECT TRIGGER (Bypasses event chain - for testing ending effect only)
e test_indochina_reset
e test_indochina_trigger_american_north_vietnam
# WARNING: This bypasses the event chain and directly triggers the ending
# Use only to test the ending effect itself, not the full process
```

### Test Southern Victory
```
# Test Southern Victory ending availability
e test_indochina_reset
e test_indochina_unlock_southern_victory
e test_indochina_debug_state
# Note: Requires VIE with anti-communist government
# Note: Requires high tension between VIE and VIN (war or opinions < -50)
# Note: Requires phase 3, 4, 6, or 7 (high tension/intensity)
# Then check GUI - Southern Victory ending should be available to click

# Setup conditions (scores and relations)
e test_indochina_reset
e test_indochina_setup_southern_victory
e test_indochina_debug_state
# Note: Still need to ensure VIE has anti-communist government

# Direct trigger (for testing ending effect)
e test_indochina_reset
e test_indochina_trigger_southern_victory
```

### Test Southern Victory Focus Chain (Hoang Lien Son Revolt)
```
# Full chain test: Focus bypass → Revolt event → Focus unlock → Crackdown
e test_indochina_reset
e test_indochina_test_southern_victory_chain
# This sets up conditions, bypasses VIE_BaoDai_Liberator_of_Vietnam, and fires revolt event
# VIE_Why_Revolting focus should now be unlocked
# Complete the focus to trigger crackdown event (BaoDai.14)

# Test focus bypass (simulates ending becoming available)
e test_indochina_reset
e test_indochina_setup_southern_victory_full_chain
e test_indochina_bypass_liberator_focus
# Bypasses VIE_BaoDai_Liberator_of_Vietnam and fires revolt event immediately
# In normal gameplay, revolt event fires 14 days after bypass
```

### Test Federal Vietnam
```
# Test Federal Vietnam ending availability
e test_indochina_reset
e test_indochina_unlock_federal_vietnam
e test_indochina_debug_state
# Note: Requires playing as FRA
# Then check GUI - Federal Vietnam ending should be available to click

# Setup conditions (scores)
e test_indochina_reset
e test_indochina_setup_federal_vietnam
e test_indochina_debug_state
# Note: Still need to ensure you're playing as FRA

# Direct trigger (for testing ending effect)
e test_indochina_reset
e test_indochina_trigger_federal_vietnam
```

### Test Balkanized Vietnam
```
# Test Balkanized Vietnam ending availability
e test_indochina_reset
e test_indochina_unlock_balkanized_vietnam
e test_indochina_debug_state
# Note: Requires playing as FUL, FRA, or CCC
# Then check GUI - Balkanized Vietnam ending should be available to click

# Setup conditions (scores)
e test_indochina_reset
e test_indochina_setup_balkanized_vietnam
e test_indochina_debug_state
# Note: Still need to ensure you're playing as FUL, FRA, or CCC

# Direct trigger (for testing ending effect)
e test_indochina_reset
e test_indochina_trigger_balkanized_vietnam
```

### Test Kuomintang Victory
```
# Test Kuomintang Victory ending availability
e test_indochina_reset
e test_indochina_unlock_kuomintang_victory
e test_indochina_debug_state
# Note: Requires playing as PQC
# Note: Requires PQC to own Saigon (286) and/or Hanoi (1760)
# Then check GUI - Kuomintang Victory ending should be available to click

# Setup conditions (scores)
e test_indochina_reset
e test_indochina_setup_kuomintang_victory
e test_indochina_debug_state
# Note: Still need to ensure you're playing as PQC and PQC owns the states

# Direct trigger (for testing ending effect)
e test_indochina_reset
e test_indochina_trigger_kuomintang_victory
```

### Test GUI Elements
```
e test_indochina_reset
e test_indochina_setup_initial
e test_indochina_show_gui
e test_indochina_show_intro
```

### Quick State Check
```
e test_indochina_debug_state
e test_indochina_debug_all_triggers
```

## Tips

1. **Always reset first**: Use `test_indochina_reset` before starting a new test scenario
2. **Check state frequently**: Use `test_indochina_debug_state` to see current values
3. **Test triggers**: Use `test_indochina_debug_all_triggers` to see which endings are available
4. **Combine effects**: You can chain multiple effects in one command: `e test_indochina_reset; e test_indochina_set_phase_low_tension`
5. **Check logs**: Open the game log to see detailed output from debug effects
6. **Avoid phase loops**: Use `test_indochina_manual_escalate`/`deescalate` instead of `force_escalation`/`deescalation` to avoid daily tick loops
7. **Geneva testing**: If `test_indochina_trigger_geneva` doesn't work, use `test_indochina_force_geneva` to bypass conditions
8. **Southern Victory chain**: Use `test_indochina_test_southern_victory_chain` for quick testing of the full focus bypass → revolt → crackdown chain
10. **State ownership**: Ensure VIE owns state 1761 (Hoang Lien Son) before testing revolt events - the setup effects handle this automatically

## Phase Reference

- **Phase 3**: High Intensity
- **Phase 4**: Medium Intensity  
- **Phase 5**: Low Intensity (Starting Phase)
- **Phase 6**: High Tension
- **Phase 7**: Medium Tension
- **Phase 8**: Low Tension (Geneva trigger)
- **Phase 9**: Never Ending Conflict
- **Phase 10**: Failed State
- **Phase 11**: Conference in Geneva

## Score Thresholds for Endings

- **Minimum score**: 1000 points required for most endings
- **Ratio requirement**: Most endings require 2x the score of competing factions
- **Total Anti-Communist**: Sum of ProFrance + ProIndependence + ProEthnic

## Notes

- All test effects are prefixed with `test_indochina_` for easy identification
- Effects that modify scores will also update related variables when appropriate
- Some effects include logging to help track what's happening
- GUI effects only show/hide elements - they don't test functionality
- Ending test effects will check conditions and trigger if met, or log if not

