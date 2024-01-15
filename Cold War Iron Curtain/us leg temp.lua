


    Employee_Free_Choice_Act_Vote = {
        
        allowed = { tag = USA }
        ai_will_do = { factor = 10 }
        
        available = {
            NOT = { has_country_flag = law_passing }
        }
        visible = {
            NOT = { has_country_flag = law_passing }
            has_country_flag = Employee_Free_Choice_Act_Vote
        }
        cost = 50
        fire_only_once = yes
        
        complete_effect = {
            set_variable = {					
                bipartisan_value = 0.45
            }	
            set_country_flag = law_passing
            bipartisan_house_calc = yes
            
            hidden_effect = {
                senate_normal_dem_support = yes
            }
            
            effect_tooltip = {
                add_political_power = 30
                increase_union_policy = yes
                step_towards_public = yes
            } 			
        }
        days_remove = 50
        remove_effect = {
            hidden_effect = {
                if = {
                    limit = { 
                        check_variable = { supseat > 216 } 
                        check_variable = { supseat_sen > senate_passing_value } 
                    }
                    country_event = { id = us_congress.100 }
                    add_political_power = 30
                    increase_union_policy = yes
                    step_towards_public = yes
                }
                if = {
                    limit = { 
                        OR = {
                            check_variable = { supseat < 217 } 
                            check_variable = { supseat_sen < senate_failing_value  } 
                        }
                    }
                    country_event = { id = parliament.1 }
                }
                set_variable = { supseat = 0 }
                set_variable = { supseat_sen = 0 }
                
                clr_country_flag = law_passing
                clear_support_types = yes
            }
        }
    }


    senate_moderate_dem_support
    senate_progressive_dem_support
    senate_dixiecrat_dem_support
    
    senate_gop_moderate_support
    senate_gop_liberal_support
    senate_gop_conservative_support
    
    senate_gop_total_support
    
    senate_normal_dem_support