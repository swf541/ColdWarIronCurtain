# -*- coding: utf-8 -*-
# Target share of world production, 1950. Blended across the sub-commodities each
# mod category represents. Anchors: US steel 47%, US oil ~50%, USSR steel 14%,
# USSR coal 18%, SAF gold 48%, Canada nickel ~85%, Congo uranium dominant.
TARGETS = {
 # Petrochemicals = oil + coal + gas, weighted by energy content (oil x1.4 tce)
 'oil':{'USA':0.400,'SOV':0.135,'ENG':0.100,'WGR':0.050,'VEN':0.050,'POL':0.036,
        'DDR':0.032,'FRA':0.024,'PER':0.021,'PRC':0.020,'JAP':0.018,'SAU':0.017,
        'RAJ':0.015,'KUW':0.011,'CAN':0.010,'AST':0.008,'IRQ':0.008,'CZE':0.008},
 # Construction Metals = steel, copper, lead, tungsten, molybdenum, manganese
 'steel':{'USA':0.420,'SOV':0.145,'ENG':0.080,'WGR':0.060,'FRA':0.045,'JAP':0.025,
          'CAN':0.022,'BEL':0.020,'CZE':0.016,'POL':0.013,'ITA':0.013,'CHL':0.012,
          'RAJ':0.010,'SWE':0.009,'AST':0.008,'BRA':0.008,'DOC':0.008},
 # Light Metals = bauxite, chromite, nickel, zinc, tin, silver, magnesium
 'aluminium':{'USA':0.280,'CAN':0.180,'SOV':0.110,'TUR':0.050,'SAF':0.048,'MLA':0.045,
              'FRA':0.032,'AST':0.030,'MEX':0.025,'BOL':0.022,'INO':0.020,'NOR':0.018,
              'RHO':0.016,'ITA':0.014,'PHI':0.012},
 # Rare Earths = gold, palladium, REE, lithium
 'tungsten':{'SAF':0.440,'CAN':0.150,'SOV':0.150,'USA':0.090,'AST':0.035,'GHA':0.030,
             'RHO':0.020,'PHI':0.012,'MEX':0.012,'BRA':0.010,'COL':0.008},
 # Nuclear Materials = uranium, thorium
 'chromium':{'DOC':0.420,'CAN':0.170,'SOV':0.145,'USA':0.110,'CZE':0.040,'DDR':0.035,
             'SAF':0.020,'AST':0.008,'POR':0.007},
}
