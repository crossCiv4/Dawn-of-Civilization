from Consts import *
from RFCUtils import *
from Events import *

def getModifier(iCivilization, iModifier):
	if iCivilization in lCivOrder:
		return tModifiers[iModifier][lCivOrder.index(iCivilization)]
	return tDefaults[iModifier]
	
def getAdjustedModifier(iPlayer, iModifier):
	if scenario() > i3000BC and dBirth[iPlayer] < dBirth[iNorse]:
		if iModifier in dLateScenarioModifiers:
			return getModifier(iPlayer, iModifier) * dLateScenarioModifiers[iModifier] / 100
	return getModifier(iPlayer, iModifier)
	
def setModifier(iPlayer, iModifier, iNewValue):
	player(iPlayer).setModifier(iModifier, iNewValue)
	
def changeModifier(iPlayer, iModifier, iChange):
	setModifier(iPlayer, iModifier, player(iPlayer).getModifier(iModifier) + iChange)
	
def adjustModifier(iPlayer, iModifier, iPercent):
	setModifier(iPlayer, iModifier, player(iPlayer).getModifier(iModifier) * iPercent / 100)
	
def adjustModifiers(iPlayer):
	for iModifier in dLateScenarioModifiers:
		adjustModifier(iPlayer, iModifier, dLateScenarioModifiers[iModifier])
		
def adjustInflationModifier(iPlayer):
	adjustModifier(iPlayer, iModifierInflationRate, dLateScenarioModifiers[iModifierInflationRate])
	
def updateModifier(iPlayer, iCivilization, iModifier):
	setModifier(iPlayer, iModifier, getModifier(iCivilization, iModifier))
	
def updateModifiers(iPlayer, iCivilization):
	for iModifier in range(iNumModifiers):
		updateModifier(iPlayer, iCivilization, iModifier)


@handler("playerCivAssigned")
def init(iPlayer, iCivilization):
	updateModifiers(iPlayer, iCivilization)
	
	if scenario() > i3000BC and dBirth[iPlayer] < dBirth[iNorse]:
		adjustModifiers(iPlayer)
	
	player(iPlayer).updateMaintenance()


@handler("BeginGameTurn")
def updateLateModifiers(iGameTurn):			
	if scenario() == i3000BC and iGameTurn == year(600):
		for iPlayer in players.major().where(lambda p: dBirth[p] < dBirth[iNorse]):
			adjustInflationModifier(iPlayer)
		

### Modifier types ###

iNumModifiers = 14
(iModifierCulture, iModifierUnitUpkeep, iModifierResearchCost, iModifierDistanceMaintenance, iModifierColonyMaintenance,
iModifierCitiesMaintenance, iModifierCivicUpkeep, iModifierHealth, iModifierUnitCost, iModifierWonderCost, 
iModifierBuildingCost, iModifierInflationRate, iModifierGreatPeopleThreshold, iModifierGrowthThreshold) = range(iNumModifiers)

### Modifiers (by civilization!) ###

# 				            EGY BAB HAR ASS CHI CHS HIT GRE NUB IND CAR PLY PER CEL ROM MAY TAM ETH TOL KUS KOR KHM MAL BYZ FRA MAA JAP VIK TUR ARA TIB MOO JAV SPA ENG HRE BUR UKR VIE SWA POL POR INC ITA MON AZT MUG THA SWE RUS OTT CON IRA NET GER AME ARG MEX COL BRA CAN     IND IND NAT BAR 

tCulture =		          (  90, 80, 80, 80, 80, 80, 80,100, 80, 80,100,100,100, 80,100,100,110, 90,100,100,100,120,130,100,160,120,110,130,120,110,120,125,120,125,130,150,120,120,100,110,110,147,140,150,135,140,125,130,130,130,150,130,135,165,150,140,130,140,140,140,140,     20, 20, 20, 30 )

tUnitUpkeep = 		      ( 135,120,200,100,125,135,110,110,130,135,115,100,100,110,100,110,100,115,110,100,100, 90,100,110,100,100,100, 90,100,120,110,110,100,110,100,100,100,100,100,100,100,100,100,100, 75, 90,110, 90, 80,100,120, 90,110, 90, 75, 80, 80, 90, 90, 80, 75,     50, 50,100,100 )
tResearchCost = 	      ( 150,140,125,120,125,120,125,150,130,130,110,200,125,150,120,125,120,120,135,110,105, 90,100,140, 90,100,110,100,120,140, 90, 90, 90, 80, 80,100, 90, 90, 90,110, 80, 85, 80, 70, 90, 80,120,100, 80, 80,120, 85,110, 80, 70, 75, 70, 90, 90, 90, 70,    125,125,125,110 )
tDistanceMaintenance = 	  ( 150,110,120,100,120,120,120,110,100,120, 60, 50, 85, 60, 70,100, 95,100,150,100,120, 80, 80,120, 90, 80, 95, 70, 60,120,120, 80, 80, 70, 70, 85, 90, 90,110, 80, 90, 80, 60, 70, 75, 70,130, 80, 90, 75,110, 80,100, 70, 80, 60, 50, 70, 70, 80, 70,    100,100,100, 20 )
tColonyMaintenance =      ( 150,150,150,150,150,150,150,150,150,100,100,100,100,100,100,150,100,150,150,150,150,150,100,150, 60,100, 80, 80,100,150,150,150,150, 55, 50, 90,150,150,150,100,100, 70,100, 80,150,100,150,150, 80,100,100,150,150, 60, 75, 90,100,100,100,100,100,    100,100,100, 20 )
tCitiesMaintenance = 	  ( 120,135,125,100,125,125,125,125,145,150,120,100, 75,120, 60,115,100,115,160,100,130,100, 90,120, 90,100,110, 75, 90,130,120, 70, 80, 50, 75, 75,100, 80,100, 70, 75, 85, 80, 80, 75, 85,110,100, 80, 60,120, 90,100, 80, 75, 70, 50, 85, 85, 80, 60,    100,100,100, 30 )
tCivicUpkeep = 		      ( 130,110,100,110,120,120,110,110,125,140, 70, 80, 70,120, 75, 80, 80, 80,100, 80, 80,100, 80,120, 80,100, 80, 80,110,110, 80, 90,100, 75, 70, 70,100, 80, 80, 80, 70, 80, 60, 60, 60, 60,100, 80, 70, 80, 90, 80, 80, 70, 60, 50, 50, 70, 70, 75, 75,    100,100,100, 70 )
tHealth = 		      	  (   1,  1,  1,  1,  1,  1,  1,  3,  2,  1,  3,  3,  3,  1,  3,  3,  2,  3,  3,  3,  3,  3,  2,  3,  2,  3,  2,  3,  2,  2,  3,  2,  3,  2,  2,  2,  3,  2,  3,  2,  2,  2,  3,  2,  3,  3,  4,  4,  2,  2,  4,  4,  3,  3,  3,  3,  3,  3,  3,  3,  3,      0,  0,  0,  0 )

tUnitCost = 		      ( 125,140,200,120,130,130,100,110,125,120, 90,100,100,100, 80,105, 85, 90,110,100, 80, 90, 90,115, 90,100, 90, 85,100,100,110,100, 90, 90,100, 90, 80, 90, 90,100, 80, 90,100,110, 80,100,100, 90, 80, 90,100, 70, 90, 90, 75, 85, 80, 85, 85, 85, 85,    300,300,150,140 )
tWonderCost = 		      (  80, 80,120, 80,120,120,100, 80, 80,100, 90,100, 85,120,100, 90,100,100,100,110,100, 90, 90,110, 70, 90,100, 90,120, 90,100, 85, 80, 90, 90,100,100, 90,100,100,100, 90, 80, 80, 90, 80, 80, 90,100,100, 90,100, 85,100, 90, 70, 70, 90, 90, 90, 80,    150,150,150,100 )
tBuildingCost = 	      ( 110,110,100,110,100,100,110,100,110,110, 90, 50,110,120, 80, 90, 70,100,120,100, 80,100, 80,110, 85, 90, 80, 90,100,100, 80, 90, 90, 90, 90, 85,100, 90, 90, 80, 80, 80, 70, 80, 80, 80, 85, 80, 80, 90, 80, 80, 80, 80, 70, 70, 70, 80, 80, 75, 80,    100,100,150,100 )
tInflationRate = 	      ( 130,130,130,125,150,150,130,150,140,140,130,130,130,140,130,125,110,130,125,120, 90,100,115,130, 90,100, 80, 70, 90,140,100, 85, 90, 90, 70, 70, 90,100, 90, 90, 70, 80, 80, 85, 90, 80,120, 75, 70, 80,100, 75, 85, 85, 70, 65, 60, 65, 65, 60, 60,     95, 95, 95, 95 )
tGreatPeopleThreshold =   ( 140,140,140,140,125,125,140,140,140,125,120,120,110,140,110,100,110,110,120,100,110, 90, 80,120, 70, 90, 90, 90, 90, 80, 85, 75, 90, 75, 75, 80, 90, 90, 90, 80, 80, 75, 70, 65, 70, 70, 75, 80, 75, 80, 80, 85, 80, 70, 65, 65, 70, 80, 80, 80, 75,    100,100,100,100 )
tGrowthThreshold = 	      ( 150,150,150,150,150,150,150,130,150,150,120,120,130,150,120,110,110,100,120,120,112, 80, 75, 90, 80,100, 90, 80, 80, 80, 80, 80, 80, 80, 70, 80, 90, 80,120, 80, 80, 80, 70, 70, 75, 70, 70, 75, 80, 80, 70, 75, 70, 75, 70, 70, 70, 70, 70, 70, 70,    125,125,125,125 )

tModifiers = (tCulture, tUnitUpkeep, tResearchCost, tDistanceMaintenance, tColonyMaintenance, tCitiesMaintenance, tCivicUpkeep, tHealth, tUnitCost, tWonderCost, tBuildingCost, tInflationRate, tGreatPeopleThreshold, tGrowthThreshold)

tDefaults = (100, 100, 100, 100, 100, 100, 100, 2, 100, 100, 100, 100, 100, 100)

dLateScenarioModifiers = {
iModifierUnitUpkeep : 90,
iModifierDistanceMaintenance : 85,
iModifierCitiesMaintenance : 80,
iModifierCivicUpkeep : 90,
iModifierInflationRate : 85,
iModifierGreatPeopleThreshold : 85,
iModifierGrowthThreshold : 80,
}