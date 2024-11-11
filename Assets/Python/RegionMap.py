from Core import *
from Files import FileMap
from Events import handler

iNumReligionMapTypes = 5
(iNone, iMinority, iPeriphery, iHistorical, iCore) = range(iNumReligionMapTypes)

def getSpreadFactor(iReligion, plot):
	iRegion = plot.getRegionID()
	if iRegion < 0: 
		return -1
	
	return next((iFactor for iFactor, lRegions in tSpreadFactors[iReligion].items() if iRegion in lRegions), iNone)
	
def updateRegionMap():
	for (x, y), iRegion in FileMap.read("Regions.csv"):
		plot(x, y).setRegionID(iRegion)

	map.recalculateAreas()
			
def updateReligionSpread(iReligion):
	for plot in plots.all():
		plot.setSpreadFactor(iReligion, getSpreadFactor(iReligion, plot))

def init():
	updateRegionMap()
	for iReligion in range(iNumReligions):
		updateReligionSpread(iReligion)
				

# TODO: revisit
tSpreadFactors = (
# Judaism
{
	iMinority :	[rBritain, rFrance, rIberia, rItaly, rLowerGermany, rCentralEurope, rBalkans, rGreece, rPoland, rRuthenia, rLevant, rMesopotamia, rAnatolia, rCaucasus, rArabia, rEgypt, rMaghreb, rPersia, rEthiopia, rAtlanticSeaboard, rMidwest, rCalifornia, rOntario, rQuebec, rMaritimes]
},
# Orthodoxy
{
	iCore :			[rRuthenia, rEthiopia, rGreece, rCaucasus],
	iHistorical : 	[rBalkans, rAnatolia, rLevant, rMesopotamia, rEgypt, rNubia, rEuropeanArctic, rUrals, rSiberia],
	iPeriphery : 	[rMaghreb, rItaly, rPonticSteppe, rCrimea, rAmericanArctic, rCentralAsianSteppe],
	iMinority :		[rBaltics, rPoland, rPersia, rKhorasan, rTransoxiana, rTarimBasin, rNorthChina],
},
# Catholicism
{
	iCore :			[rFrance, rCentralEurope, rPoland, rIreland, rItaly, rIberia],
	iHistorical :	[rBritain, rLowerGermany, rQuebec, rMaritimes, rAtlanticSeaboard, rCaribbean, rAridoamerica, rMesoamerica, rCentralAmerica, rNewGranada, rAndes, rAmazonia, rBrazil, rSouthernCone, rCape, rPhilippines],
	iPeriphery :	[rBalkans, rGreece, rAmericanArctic, rOntario, rMidwest, rDeepSouth, rGreatPlains, rCalifornia, rAustralia, rOceania, rGuinea, rCongo, rSwahiliCoast, rMadagascar],
	iMinority: [rNorway, rDenmark, rSweden],
},
# Protestantism
{
	iCore :			[rBritain, rLowerGermany, rDenmark, rNorway, rSweden, rAtlanticSeaboard, rMidwest, rOntario, rGreatPlains, rDeepSouth, rMaritimes],
	iHistorical :	[rCalifornia, rCascadia, rAmericanArctic, rAustralia],
	iPeriphery :	[rFrance, rOceania, rCape, rZambezi],
	iMinority : 	[rPoland, rCentralEurope, rBrazil, rKorea]
},
# Islam
{
	iCore : 		[rArabia, rMesopotamia, rEgypt, rLevant],
	iHistorical : 	[rPersia, rKhorasan, rSindh, rPunjab, rTransoxiana, rMaghreb, rIndonesia, rSahel, rSahara, rHornOfAfrica, rHinduKush],
	iPeriphery : 	[rNubia, rIberia, rAnatolia, rBalkans, rHindustan, rRajputana, rBengal, rDeccan, rPonticSteppe, rCrimea, rCentralAsianSteppe, rSwahiliCoast, rCaucasus],
	iMinority : 	[rUrals, rSiberia, rTarimBasin, rMongolia],
},
# Hinduism
{
	iCore : 		[rHindustan, rRajputana, rDeccan, rBengal, rDravida],
	iHistorical : 	[rPunjab, rSindh, rIndochina, rIndonesia, rPhilippines],
},
# Buddhism
{
	iCore : 		[rHindustan, rRajputana, rBengal, rTibet, rIndochina],
	iHistorical : 	[rDeccan, rDravida, rPunjab, rSindh, rTarimBasin, rMongolia, rNorthChina, rSouthChina, rKorea, rJapan, rIndonesia, rKhorasan],
	iMinority :		[rTransoxiana, rKhorasan],
},
# Confucianism
{
	iCore : 		[rNorthChina, rSouthChina, rManchuria],
	iHistorical :	[rKorea],
	iPeriphery : 	[rMongolia, rTibet],
	iMinority : 	[rJapan, rIndonesia, rIndochina, rAustralia],
},
# Taoism
{
	iCore : 		[rNorthChina, rSouthChina],
	iHistorical : 	[rManchuria],
	iPeriphery : 	[rTibet, rMongolia],
},
# Zoroastrianism
{
	iCore :			[rPersia],
	iHistorical : 	[rKhorasan, rTransoxiana, rHinduKush],
	iPeriphery : 	[rMesopotamia, rTransoxiana, rLevant, rCaucasus, rAnatolia],
	iMinority : 	[rSindh, rPunjab],
},
# Shia
{
	iCore : 		[rArabia, rMesopotamia, rPersia],
	iHistorical : 	[rMaghreb, rLevant, rEgypt, rKhorasan, rTransoxiana, rCaucasus, rRajputana],
	iPeriphery : 	[rNubia, rAnatolia, rBalkans, rHindustan, rBengal, rCentralAsianSteppe, rSindh, rPunjab, rHinduKush],
	iMinority : 	[rUrals, rSiberia, rTarimBasin, rMongolia, rIberia, rDeccan, rPonticSteppe, rCrimea, rSwahiliCoast, rHornOfAfrica, rSahara, rSahel, rIndonesia],
},
)