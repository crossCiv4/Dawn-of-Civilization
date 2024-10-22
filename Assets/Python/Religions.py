from RFCUtils import *
from Locations import *
from Core import *

from Events import handler, popup_handler


# initialise coordinates

dCatholicPreference = CivDict({
iEgypt		: 80,
iGreece		: 80,
iMacedon	: 80,
iRome		: 95,
iEthiopia	: 80,
iByzantium	: 90,
iNorse		: 20,
iArabia		: 80,
iSpain		: 95,
iFrance		: 75,
iEngland	: 30,
iHolyRome	: 55,
iPoland		: 80,
iPortugal	: 95,
iItaly		: 90,
iRussia		: 80,
iCongo		: 80,
iGermany	: 25,
iNetherlands: 10,
iAmerica	: 20,
iMamluks	: 80,
}, 50)

def getCatholicPreference(iPlayer):
	return dCatholicPreference[iPlayer]
	

@handler("buildingBuilt")	
def onBuildingBuilt(city, iBuilding):
	iPlayer = city.getOwner()

	if iBuilding == iHinduTemple:
		if game.isReligionFounded(iBuddhism): return
		player(city).foundReligion(iBuddhism, iBuddhism, True)
		
	if iBuilding == iOrthodoxCathedral:
		if game.isReligionFounded(iCatholicism): return

		# if Cathedral is in Orthodox Core/Historical, don't found Catholicism
		if plot(city).getSpreadFactor(iOrthodoxy) >= 3: return
	
		orthodoxHolyCity = game.getHolyCity(iOrthodoxy)
	
		if orthodoxHolyCity.getOwner() != iPlayer:
			foundReligion(location(city), iCatholicism)
			catholicHolyCity = game.getHolyCity(iCatholicism)
			schism(orthodoxHolyCity, catholicHolyCity, cities.none(), cities.all().notowner(orthodoxHolyCity.getOwner()).religion(iOrthodoxy), message="TXT_KEY_SCHISM_MESSAGE_CATHEDRAL")

			if cities.owner(iPlayer).none(lambda city: city.isHasReligion(iOrthodoxy)):
				player(city).setLastStateReligion(iCatholicism)

@handler("BeginGameTurn")
def foundHinduism(iGameTurn):
	if not player(iIndia).isHuman():
		if iGameTurn == year(-2000)+1:
			if not game.isReligionFounded(iHinduism):
				if plot(92, 39).isCity():
					foundReligion((92, 39), iHinduism)


@handler("BeginGameTurn")
def checkIslam(iGameTurn):
	if not game.isReligionFounded(iIslam) and iGameTurn >= year(610):
		if plot(tMecca).isCity():
			foundReligion(tMecca, iIslam)


@handler("BeginGameTurn")
def checkJudaism(iGameTurn):
	if game.isReligionFounded(iJudaism):
		return

	if iGameTurn == year(-1000) - turns(data.iSeed % 5):
		foundReligion(selectHolyCity(plots.regions(rEgypt, rLevant, rMesopotamia), tJerusalem, False), iJudaism)


@handler("BeginGameTurn")
def checkChristianity(iGameTurn):
	if not game.isReligionFounded(iJudaism): return
	if game.isReligionFounded(iOrthodoxy): return
	
	iOffset = turns(data.iSeed % 15)
	
	if iGameTurn == year(0) + iOffset:
		holyCity = game.getHolyCity(iJudaism)
		
		if not holyCity.isHuman() and rand(2) == 0:
			foundReligion(holyCity, iOrthodoxy)
			return
			
		jewishCity = cities.all().notowner(active()).where(lambda city: city.isHasReligion(iJudaism)).random()
		if jewishCity:
			foundReligion(location(jewishCity), iOrthodoxy)


@handler("BeginGameTurn")
def checkSchism(iGameTurn):
	if not game.isReligionFounded(iOrthodoxy): return
	if game.isReligionFounded(iCatholicism): return
	if game.countReligionLevels(iOrthodoxy) < 10: return

	# Do not schism until the Byzantines have had a chance to spawn and establish themselves
	# Even if they don't actually spawn (e.g. if the human player is Rome and stable)
	if year() < year(dBirth[iByzantium]) + turns(10): return
	
	orthodoxCities = cities.all().religion(iOrthodoxy)
	
	futureCatholicCities, nonCatholicLoyalCities = orthodoxCities.split(
		lambda city: plot(city).getSpreadFactor(iCatholicism) >= RegionSpreadTypes.REGION_SPREAD_HISTORICAL and city.getOwner() != game.getHolyCity(iOrthodoxy).getOwner() and city.getOwner() != iByzantium and
		player(city).getStateReligion() != iIslam
	)

	loyalOrthodoxCities, nonAlignedOrthodoxCities = nonCatholicLoyalCities.split(
		lambda city: not is_minor(city) and plot(city).getSpreadFactor(iOrthodoxy) >= RegionSpreadTypes.REGION_SPREAD_HISTORICAL and player(city).getStateReligion() == iOrthodoxy
	)

	futureCatholicCitiesPop = futureCatholicCities.sum(lambda city: city.getPopulation())
	loyalOrthodoxCitiesPop = loyalOrthodoxCities.sum(lambda city: city.getPopulation())
	nonAlignedOrthodoxCitiesPop = nonAlignedOrthodoxCities.sum(lambda city: city.getPopulation())
	# nonCatholicLoyalCitiesPop = nonCatholicLoyalCities.sum(lambda city: city.getPopulation())

	# for debugging purposes
	# message(active(), 'Total orthodox cities: %s Future Catholic cities: (%s Pop: %s) Non-Catholic Loyal cities: (%s Pop %s) divided into two camps: Loyal Orthodox cities: (%s Pop: %s) and Non-Aligned Orthodox cities: (%s Pop: %s)' % (orthodoxCities.count(), futureCatholicCities.count(), futureCatholicCitiesPop, nonCatholicLoyalCities.count(), nonCatholicLoyalCitiesPop, loyalOrthodoxCities.count(), loyalOrthodoxCitiesPop, nonAlignedOrthodoxCities.count(), nonAlignedOrthodoxCitiesPop),color=iRed, force=True)

	# as long as "historically orthodox" regions out-populate the catholic ones, do not Schism
	# non-Aligned Orthodox (i.e. Orthodox owned by Minors or non-Orthodox civs) count for a portion of their pop
	# a lot of the non-Aligned are from the lands of the Arab conquest; Orthodoxy often disappears over time there
	if loyalOrthodoxCitiesPop + nonAlignedOrthodoxCitiesPop / 2 >= futureCatholicCitiesPop: return

	orthodoxCapital = loyalOrthodoxCities.where(lambda city: city.isCapital()).maximum(lambda city: player(city).getScoreHistory(iGameTurn))
	if not orthodoxCapital:
		orthodoxCapital = game.getHolyCity(iOrthodoxy)
		
	# many different levels of fallbacks
	catholicCapital = futureCatholicCities.where(lambda city: city.getOwner() != orthodoxCapital.getOwner()).maximum(lambda city: player(city).getScoreHistory(iGameTurn))
	if not catholicCapital:
		catholicCapital = nonAlignedOrthodoxCities.maximum(lambda city: player(city).getScoreHistory(iGameTurn))
	if not catholicCapital:
		catholicCapital = loyalOrthodoxCities.where(lambda city: city.getOwner() != orthodoxCapital.getOwner()).maximum(lambda city: player(city).getScoreHistory(iGameTurn))
	if not catholicCapital:
		return
	
	foundReligion(catholicCapital, iCatholicism)
	schism(orthodoxCapital, catholicCapital, futureCatholicCities, nonAlignedOrthodoxCities, message="TXT_KEY_SCHISM_MESSAGE")


@handler("BeginGameTurn")
def spreadJudaism():
	spreadReligionToRegion(iJudaism, [rIberia, rFrance, rLowerGermany, rCentralEurope, rPoland, rItaly, rBritain, rRuthenia, rBalkans], 1000, 10)
	spreadReligionToRegion(iJudaism, [rMesopotamia, rAnatolia, rEgypt], 600, 20)
	spreadReligionToRegion(iJudaism, [rOntario, rMaritimes, rAtlanticSeaboard, rMidwest], 1850, 10)


@handler("BeginGameTurn")
def spreadHinduismSoutheastAsia():
	lSouthEastAsianCivs = [iKhmer, iMalays, iJava]

	if not game.isReligionFounded(iHinduism): return
	if none(player(iCiv).isExisting() for iCiv in lSouthEastAsianCivs): return
	if not turn().between(500, 1200): return
	
	if not periodic(20): return
	
	contacts = players.major().where(lambda p: any(player(q).canContact(p) for q in lSouthEastAsianCivs) and player(p).getStateReligion() in [iHinduism, iBuddhism])
	if not contacts:
		return
	
	southEastAsiaCities = cities.regions(rIndochina, rIndonesia)
	potentialCities = southEastAsiaCities.where(lambda city: not city.isHasReligion(iHinduism))
	
	iMaxCitiesMultiplier = 2
	if len(potentialCities) * iMaxCitiesMultiplier >= len(southEastAsiaCities):
		spreadCity = potentialCities.random()
		if spreadCity:
			spreadCity.spreadReligion(iHinduism)


@handler("BeginGameTurn")
def spreadIslamIndonesia():
	if not game.isReligionFounded(iIslam): 
		return
		
	if not player(iJava).isExisting() and not player(iMalays).isExisting(): 
		return

	if not turn().between(1250, 1600): 
		return
	
	if not periodic(10): 
		return
	
	indonesianContacts = players.major().where(lambda p: (player(iJava).canContact(p) or player(iMalays).canContact(p)) and player(p).getStateReligion() == iIslam)
	if not indonesianContacts:
		return
		
	indonesianCities = cities.region(rIndonesia)
	potentialCities = indonesianCities.where(lambda c: not c.isHasReligion(iIslam))
	
	iMaxCitiesMultiplier = 2
	if player(iMalays).getStateReligion() == iIslam or player(iJava).getStateReligion() == iIslam: iMaxCitiesMultiplier = 5
	
	if len(potentialCities) * iMaxCitiesMultiplier >= len(indonesianCities):
		spreadCity = potentialCities.random()
		if spreadCity:
			spreadCity.spreadReligion(iIslam)


@handler("techAcquired")
def checkReformation(iTech, iTeam, iPlayer):
	if scenario() == i1700AD:
		return

	if iTech == iAcademia:
		if player(iPlayer).getStateReligion() == iCatholicism:
			if not game.isReligionFounded(iProtestantism):
				if player(iPlayer).getNumCities() > 0:
					player(iPlayer).foundReligion(iProtestantism, iProtestantism, True)
					reformation()


@handler("firstCity")
def checkReformationOnSpawn(city):
	if scenario() == i1700AD:
		return
	
	if not game.isReligionFounded(iProtestantism):
		if player(city.getOwner()).getStateReligion() == iCatholicism:
			if team(city.getTeam()).isHasTech(iAcademia):
				player(city.getOwner()).foundReligion(iProtestantism, iProtestantism, True)
				reformation()


@handler("techAcquired")
def lateReligionFounding(iTech):
	if scenario() == i1700AD:
		return
				
	for iReligion in range(iNumReligions):
		checkLateReligionFounding(iReligion, iTech)


def foundReligion(location, iReligion):
	if not location:
		return False

	city = city_(location)
	if city:
		game.setHolyCity(iReligion, city, True)
		return True
		
	return False


def selectHolyCity(area, tPreferredCity = None, bAIOnly = True):
	preferredCity = city(tPreferredCity)
	if preferredCity and not (bAIOnly and preferredCity.isHuman()):
		return preferredCity
				
	holyCity = area.cities().where(lambda city: not bAIOnly or not city.isHuman()).random()
	if holyCity:
		return location(holyCity)
		
	return None

	
def spreadReligionToRegion(iReligion, lRegions, iStartDate, iInterval):
	if not game.isReligionFounded(iReligion): return
	if turn() < year(iStartDate): return
	
	if not periodic(iInterval): return
	
	regionCities = cities.regions(*lRegions)
	religionCities = regionCities.religion(iReligion)
	
	if 2 * len(religionCities) < len(regionCities):
		spreadCity = regionCities.where(lambda city: not city.isHasReligion(iReligion) and player(city.getOwner()).getSpreadType(plot(city), iReligion) > ReligionSpreadTypes.RELIGION_SPREAD_NONE).random()
		if spreadCity:
			spreadCity.spreadReligion(iReligion)


def schism(orthodoxCapital, catholicCapital, replace, distant, message):
	replace += distant.where(lambda city: distance(city, catholicCapital) <= distance(city, orthodoxCapital))
	for city in replace:
		city.replaceReligion(iOrthodoxy, iCatholicism)
			
	if player().getStateReligion() == iOrthodoxy and not autoplay():
		eventpopup(-1, text("TXT_KEY_SCHISM_TITLE"), text(message, catholicCapital.getName()), ())
		
	for iPlayer in players.major().existing().ai().religion(iOrthodoxy):
		if 2 * replace.owner(iPlayer).count() >= player(iPlayer).getNumCities():
			player(iPlayer).setLastStateReligion(iCatholicism)


def reformation():				
	for iPlayer in players.major().existing():
		reformationChoice(iPlayer)
			
	for iPlayer in players.major().existing():
		if data.players[iPlayer].iReformationDecision == 2:
			for iTargetPlayer in players.major().existing():
				if data.players[iTargetPlayer].iReformationDecision == 0 and not player(iTargetPlayer).isHuman() and civ(iTargetPlayer) != iNetherlands and not team(iTargetPlayer).isAVassal():
					team(iPlayer).declareWar(iTargetPlayer, True, WarPlanTypes.WARPLAN_DOGPILE)
					
	pHolyCity = game.getHolyCity(iProtestantism)
	if data.players[pHolyCity.getOwner()].iReformationDecision == 0:
		pHolyCity.setNumRealBuilding(iProtestantShrine, 1)


def reformationChoice(iPlayer):
	pPlayer = player(iPlayer)
	
	if player(iPlayer).isHuman():
		return

	if pPlayer.getStateReligion() == iCatholicism:
		if chooseProtestantism(iPlayer):
			embraceReformation(iPlayer)
		elif isProtestantAnyway(iPlayer) or team(iPlayer).isAVassal():
			tolerateReformation(iPlayer)
		else:
			counterReformation(iPlayer)
	else:
		tolerateReformation(iPlayer)


def chooseProtestantism(iPlayer):
	return rand(100) >= getCatholicPreference(iPlayer)


def isProtestantAnyway(iPlayer):
	return rand(100) >= (getCatholicPreference(iPlayer)+50)/2


def embraceReformation(iPlayer):
	iNumCatholicCities = 0
	for city in cities.owner(iPlayer).religion(iCatholicism):
		iNumCatholicCities += 1
		
		if city.getPopulation() >= 8 and not chooseProtestantism(iPlayer):
			city.spreadReligion(iProtestantism)
		else:
			city.replaceReligion(iCatholicism, iProtestantism)
			
	pPlayer = player(iPlayer)
	pPlayer.changeGold(iNumCatholicCities * turns(100))
	
	pPlayer.setLastStateReligion(iProtestantism)
	pPlayer.setConversionTimer(10)
	
	if not is_minor(iPlayer):
		data.players[iPlayer].iReformationDecision = 0


def tolerateReformation(iPlayer):
	for city in cities.owner(iPlayer).religion(iCatholicism):
		if isProtestantAnyway(iPlayer):
			if city.getPopulation() <= 8 and not city.isHolyCityByType(iCatholicism):
				city.replaceReligion(iCatholicism, iProtestantism)
			else:
				city.spreadReligion(iProtestantism)

	if not is_minor(iPlayer):
		data.players[iPlayer].iReformationDecision = 1
				
def counterReformation(iPlayer):
	for city in cities.owner(iPlayer).religion(iCatholicism):
		if chooseProtestantism(iPlayer):
			if city.getPopulation() >= 8:
				city.spreadReligion(iProtestantism)
	
	if not is_minor(iPlayer):
		data.players[iPlayer].iReformationDecision = 2


def checkLateReligionFounding(iReligion, iTech):
	if infos.religion(iReligion).getTechPrereq() != iTech:
		return
		
	if game.isReligionFounded(iReligion):
		return
		
	allPlayers = players.major().existing()
	techPlayers = allPlayers.tech(iTech)
				
	if 2 * techPlayers.count() >= allPlayers.count():
		foundReligionInCore(iReligion)


def foundReligionInCore(iReligion):
	city = cities.all().where(lambda c: c.plot().getSpreadFactor(iReligion) == RegionSpreadTypes.REGION_SPREAD_CORE).random()
	if city:
		foundReligion(location(city), iReligion)


### popup handlers - transition to using Popups module ###


@popup_handler(7624)
def applyReformationDecision(playerID, netUserData, popupReturn):
	if popupReturn.getButtonClicked() == 0:
		embraceReformation(active())
	elif popupReturn.getButtonClicked() == 1:
		tolerateReformation(active())
	elif popupReturn.getButtonClicked() == 2:
		counterReformation(active())