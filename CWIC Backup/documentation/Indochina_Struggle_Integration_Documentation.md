# Indochina Struggle Mechanic Integration - Implementation Philosophy

## Overview

This document outlines the comprehensive integration of focuses, events, and decisions with the Indochina Struggle mechanic. The goal is to create a dynamic, interconnected system where player choices in focus trees, diplomatic decisions, and narrative events directly influence the course of the First Indochina War through the Struggle GUI system.

## Design Philosophy

### Core Principles

1. **Narrative Coherence**: Every action that logically should affect the Indochina conflict does so through the Struggle mechanic. Military buildups, diplomatic overtures, economic aid, and political decisions all have measurable impacts.

2. **Player Agency**: Players should feel that their choices matter. Taking a focus that increases military support for France should be reflected in the Struggle scores, making the player's strategic decisions visible and impactful.

3. **Balanced Progression**: The point system is designed to prevent any single action from being overpowered while ensuring that cumulative choices create meaningful shifts in the conflict's trajectory.

4. **Historical Authenticity**: Point values reflect the relative importance of actions. Major diplomatic breakthroughs (like Geneva Conference preparations) have larger impacts than minor economic aid packages.

5. **Systemic Integration**: All major game systems (focus trees, events, decisions) feed into the Struggle mechanic, creating a unified experience where the GUI reflects the cumulative state of all player and AI actions.

## Point Balance System

### Escalation/De-escalation Points (`global.Indochina_War_Next_Phase_A/B_Points`)

These points determine phase transitions (3-8) in the Struggle system. They represent the intensity of the conflict.

**Tier 1 - Minor Actions (25-50 points)**
- Low-level diplomatic decisions
- Small-scale military reorganizations
- Minor economic aid packages
- Individual unit deployments
- Small border skirmishes

**Tier 2 - Moderate Actions (75-150 points)**
- Medium-scale military buildups
- Significant diplomatic initiatives
- Economic aid programs
- Political reforms affecting the war
- Regional military operations

**Tier 3 - Major Actions (200-500 points)**
- Large-scale military interventions
- Major diplomatic conferences
- Comprehensive economic aid programs
- Strategic military reorganizations
- Decisive political changes

### Faction Score Points (Stored on FRA)

These scores determine which faction wins the Struggle and influence ending outcomes.

**Tier 1 - Minor Actions (25-50 points)**
- Small diplomatic gestures
- Minor military support
- Limited economic aid
- Individual political decisions

**Tier 2 - Moderate Actions (75-150 points)**
- Significant military support
- Major diplomatic initiatives
- Substantial economic aid
- Political reforms
- Regional military victories

**Tier 3 - Major Actions (200-500 points)**
- Large-scale military interventions
- Comprehensive aid programs
- Major diplomatic breakthroughs
- Strategic victories
- Decisive political changes

## Implementation Categories

### 1. Military Focuses

**Pattern**: Military focuses that increase capabilities, deploy forces, or reorganize military structures should:
- Add escalation points (increasing conflict intensity)
- Add faction scores to the relevant side
- Scale based on the scope of the military action

**Examples**:
- Small military reorganization: +25 escalation, +25 faction score
- Medium military buildup: +75 escalation, +75 faction score
- Large-scale intervention: +200 escalation, +200 faction score

### 2. Diplomatic Focuses

**Pattern**: Diplomatic focuses that improve relations, provide aid, or change diplomatic posture should:
- Add de-escalation points (reducing conflict intensity) for peaceful diplomacy
- Add escalation points for confrontational diplomacy
- Add faction scores based on which side benefits
- Scale based on the importance of the diplomatic action

**Examples**:
- Minor diplomatic gesture: +25 de-escalation, +25 faction score
- Major diplomatic initiative: +150 de-escalation, +150 faction score
- Confrontational diplomacy: +75 escalation, +75 opposing faction score

### 3. Economic Focuses

**Pattern**: Economic focuses that provide aid, investment, or economic support should:
- Add de-escalation points (economic stability reduces conflict)
- Add faction scores to the recipient
- Scale based on the amount of aid/investment

**Examples**:
- Small economic aid: +25 de-escalation, +25 faction score
- Medium economic program: +75 de-escalation, +75 faction score
- Large-scale reconstruction: +200 de-escalation, +200 faction score

### 4. Political Focuses

**Pattern**: Political focuses that change government, implement reforms, or shift ideology should:
- Add escalation or de-escalation points based on whether the change increases or decreases conflict
- Add faction scores based on which faction benefits
- Scale based on the significance of the political change

**Examples**:
- Minor political reform: +25 points (direction depends on reform)
- Major political change: +150 points
- Revolutionary change: +300 points

### 5. Events

**Pattern**: Events should follow similar scaling but often have narrative context that determines point values. Random events may have variable outcomes.

**Examples**:
- Minor event outcome: +25-50 points
- Moderate event outcome: +75-150 points
- Major event outcome: +200-500 points

### 6. Decisions

**Pattern**: Decisions are typically repeatable or have lower individual impact but can be taken multiple times. They should have smaller point values but can accumulate.

**Examples**:
- Repeatable decision: +25-50 points per use
- One-time decision: +75-150 points
- Major decision: +200-300 points

## Country-Specific Implementation Guidelines

### VIE (South Vietnam)

**Faction**: Pro-Independence
**Focus Areas**:
- Military focuses → +Pro-Independence score, +escalation
- Diplomatic focuses with USA/France → +Pro-Independence score, +de-escalation
- Economic focuses → +Pro-Independence score, +de-escalation
- Political focuses → Variable based on direction

### VIN (North Vietnam)

**Faction**: Communist
**Focus Areas**:
- Military focuses → +Communist score, +escalation
- Diplomatic focuses with PRC/SOV → +Communist score, +de-escalation (if peaceful)
- Economic focuses → +Communist score, +de-escalation
- Political focuses → Variable based on direction

### FRA (France)

**Faction**: Pro-France
**Focus Areas**:
- Indochina-specific military focuses → +Pro-France score, +escalation
- Diplomatic focuses → Variable
- Economic focuses related to Indochina → +Pro-France score, +de-escalation
- Withdrawal/negotiation focuses → +de-escalation, -Pro-France score

### USA

**Faction**: Interloper (affects all factions)
**Focus Areas**:
- Military aid focuses → +Pro-France/Pro-Independence score, +escalation
- Diplomatic focuses → Variable based on direction
- Economic aid focuses → +recipient faction score, +de-escalation
- Intervention focuses → +escalation, +relevant faction score

## Implementation Notes

1. **Always Recalculate Total Anti-Communist Score**: After modifying Pro-France, Pro-Independence, or Pro-Ethnic scores, call `indochina_struggle_recalculate_total_anti_communist_score = yes`

2. **Use Tooltips**: Always include appropriate tooltips for point additions:
   - `tooltip = Add_to_Escalation_Phase_TT`
   - `tooltip = Add_to_De_Escalation_Phase_TT`
   - `tooltip = Add_to_Communist_Victory_Points_TT`
   - `tooltip = Add_to_French_Victory_Points_TT`
   - `tooltip = Add_to_Independent_Victory_Points_TT`
   - `tooltip = Add_to_Ethnic_Victory_Points_TT`
   - `tooltip = Add_to_Kuomintang_Victory_Points_TT`

3. **Conditional Logic**: Only add points if the Indochina War is still active:
   ```
   if = {
       limit = {
           NOT = { has_global_flag = Indochina_War_Over }
       }
       # Add points here
   }
   ```

4. **Scale Appropriately**: Consider the relative importance of actions. A focus that takes 70 days and represents a major strategic shift should have more impact than a 7-day focus that's a minor adjustment.

5. **Balance Escalation vs De-escalation**: Military actions generally escalate, diplomatic/economic actions generally de-escalate, but context matters. A diplomatic ultimatum might escalate, while economic aid might de-escalate.

## Examples of Implementation

### Example 1: Military Focus (VIE)
```
completion_reward = {
    if = {
        limit = {
            NOT = { has_global_flag = Indochina_War_Over }
        }
        add_to_variable = {
            global.Indochina_War_Next_Phase_A_Points = 75
            tooltip = Add_to_Escalation_Phase_TT
        }
        FRA = {
            add_to_variable = {
                StruggleInvolvedNationsIndochinaProIndependenceScore = 75
                tooltip = Add_to_Independent_Victory_Points_TT
            }
            indochina_struggle_recalculate_total_anti_communist_score = yes
        }
    }
}
```

### Example 2: Diplomatic Focus (USA)
```
completion_reward = {
    if = {
        limit = {
            NOT = { has_global_flag = Indochina_War_Over }
            country_exists = VIE
        }
        add_to_variable = {
            global.Indochina_War_Next_Phase_B_Points = 150
            tooltip = Add_to_De_Escalation_Phase_TT
        }
        FRA = {
            add_to_variable = {
                StruggleInvolvedNationsIndochinaProIndependenceScore = 150
                tooltip = Add_to_Independent_Victory_Points_TT
            }
            indochina_struggle_recalculate_total_anti_communist_score = yes
        }
    }
}
```

### Example 3: Economic Focus (FRA)
```
completion_reward = {
    if = {
        limit = {
            NOT = { has_global_flag = Indochina_War_Over }
        }
        add_to_variable = {
            global.Indochina_War_Next_Phase_B_Points = 100
            tooltip = Add_to_De_Escalation_Phase_TT
        }
        FRA = {
            add_to_variable = {
                StruggleInvolvedNationsIndochinaProFranceScore = 100
                tooltip = Add_to_French_Victory_Points_TT
            }
            indochina_struggle_recalculate_total_anti_communist_score = yes
        }
    }
}
```

## Implementation Summary

### Completed Integrations

#### Scripted Effects (CWIC_Struggle_Effects.txt)
- Created helper scripted effects for common integration patterns:
  - `indochina_struggle_add_communist_military_points`
  - `indochina_struggle_add_communist_diplomatic_points`
  - `indochina_struggle_add_pro_independence_military_points`
  - `indochina_struggle_add_pro_independence_diplomatic_points`
  - `indochina_struggle_add_pro_france_military_points`
  - `indochina_struggle_add_pro_france_diplomatic_points`

#### VIN Focuses (VIN_50s.txt)
- **VIN_Nam_Bo_Khang_Chien**: +75 escalation, +75 Communist score (military focus)
- **VIN_Raise_the_Smuggling_Fleet**: +50 escalation, +50 Communist score (logistics focus)
- **VIN_Empower_the_Democratic_Front**: +75 escalation, +75 Communist score (political/military focus)
- **VIN_Victory_in_the_South**: +200 escalation, +200 Communist score (major victory focus)

#### VIE Focuses (VIE_50s_Military.txt)
- **VIE_Amalgamatize_VeBinh_Paramilitaries**: +75 escalation, +75 Pro-Independence score (military buildup)

#### FRA Focuses (FRA_1950s.txt)
- **FRA_First_Indochina_War**: +100 escalation, +100 Pro-France score (war commitment focus)
- **FRA_Retreat_From_Indochina**: +300 de-escalation, -200 Pro-France score (withdrawal focus)

#### Events
- Border war events already have comprehensive integration (Indochina_War_Rework.txt)
- Geneva Conference events already integrated (Geneva_Conference_Invitations.txt)

### Implementation Pattern

All focuses follow this pattern:
1. Check if war is still active: `NOT = { has_global_flag = Indochina_War_Over }`
2. Add escalation/de-escalation points with appropriate tooltip
3. Add faction score points with appropriate tooltip
4. Recalculate total anti-communist score if modifying Pro-France, Pro-Independence, or Pro-Ethnic scores

### Point Values Used

**Tier 1 (Minor Actions)**: 25-50 points
- Small military reorganizations
- Minor diplomatic gestures
- Low-level decisions

**Tier 2 (Moderate Actions)**: 75-150 points
- Medium military buildups
- Significant diplomatic initiatives
- Standard focus completions

**Tier 3 (Major Actions)**: 200-500 points
- Large-scale military interventions
- Major diplomatic breakthroughs
- Strategic victories/withdrawals

### Expansion Opportunities

The following areas can be expanded with similar integration:

1. **Additional VIN Focuses**: 
   - Diplomatic focuses (Bamboo Diplomacy, International Ties)
   - Economic focuses
   - Political focuses

2. **Additional VIE Focuses**:
   - All military focuses in VIE_50s_Military.txt
   - Diplomatic focuses in VIE_50s_Diplo.txt
   - Economic focuses in VIE_50s_Economy.txt

3. **Additional FRA Focuses**:
   - All Indochina-related focuses in FRA_1950s.txt
   - Military reinforcement focuses
   - Diplomatic negotiation focuses

4. **USA Focuses**:
   - All Indochina-related focuses in USA_FP_50s.txt
   - CIA intervention focuses in USA_CIA_50s.txt

5. **Events**:
   - VIE_Events.txt
   - North_Vietnam_Flavor.txt
   - Indochina_Flavor_Events.txt
   - France.txt (Indochina-related events)

6. **Decisions**:
   - Additional decisions in Indochina_War.txt
   - Country-specific Indochina decisions

## Conclusion

This integration system ensures that the Indochina Struggle mechanic is not an isolated minigame but rather the central reflection of all player and AI actions related to the conflict. Every meaningful choice feeds into the system, creating a dynamic, responsive experience where the Struggle GUI accurately represents the cumulative state of the war.

The implementation provided here establishes the foundation and pattern for comprehensive integration. The helper scripted effects make it easy to add more integrations following the established balance system. All focuses, events, and decisions that logically affect the Indochina conflict should follow this pattern to create a fully integrated experience.

