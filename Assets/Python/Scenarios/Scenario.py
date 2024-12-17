from Resources import setupScenarioResources
from DynamicCivs import checkName
from Slots import findSlot, findMinorSlot, addPlayer, initWars
from GoalHandlers import event_handler_registry
from Periods import dScenarioPeriods, setPeriod

from Core import *
from RFCUtils import *
from Civilizations import *
from Parsers import *


START_HISTORY = -3000

LEADER_DATES = {
	iRamesses: -1300,
	iCleopatra: -50,
	iSargon: -2400,
	iHammurabi: -1800,
	iWentAntu: -2000,
	iAshurbanipal: -660,
	iQinShiHuang: -247,
	iTaizong: 630,
	iHongwu: 1370,
	iSunQuan: 200,
	iGaozong: 1120,
	iMursili: -1600,
	iPericles: -450,
	iAlexanderTheGreat: -330,
	iAsoka: -260,
	iChandragupta: 320,
	iShivaji: 1680,
	iGandhi: 1930,
	iHiram: -980,
	iHannibal: -210,
	iAbuFaris: 1394,
	iTaharqa: -690,
	iAhoeitu: 900,
	iCyrus: -550,
	iDarius: -520,
	iKhosrow: 540,
	iJuliusCaesar: -50,
	iAugustus: -20,
	iPacal: 620,
	iRajendra: 1020,
	iKrishnaDevaRaya: 1510,
	iEzana: 320,
	iZaraYaqob: 1440,
	iMenelik: 1890,
	iLeLoi: 1400,
	iTopiltzin: 900,
	iKanishka: 130,
	iWangKon: 920,
	iSejong: 1420,
	iSuryavarman: 1120,
	iJustinian: 530,
	iBasil: 980,
	iSriJayanasa: 700,
	iTunPerak: 1450,
	iKammu: 790,
	iOdaNobunaga: 1580,
	iMeiji: 1870,
	iRagnar: 800,
	iChristian: 1620,
	iGerhardsen: 1950,
	iBumin: 550,
	iAlpArslan: 1070,
	iTamerlane: 1370,
	iHarun: 790,
	iAlMuizz: 953,
	iSaladin: 1180,
	iBaibars: 1260,
	iSimeon: 893,
	iSongtsen: 620,
	iLobsangGyatso: 1650,
	iRahman: 920,
	iYaqub: 1190,
	iHayamWuruk: 1350,
	iSuharto: 1950,
	iIsabella: 1480,
	iPhilip: 1560,
	iCharlemagne: 770,
	iLouis: 1650,
	iNapoleon: 1800,
	iDeGaulle: 1950,
	iAlfred: 880,
	iElizabeth: 1560,
	iVictoria: 1840,
	iChurchill: 1940,
	iBarbarossa: 1160,
	iCharles: 1550,
	iFrancis: 1800,
	iAnawrahta: 1050,
	iBayinnaung: 1550,
	iYaroslav: 1050,
	iDawud: 1300,
	iMansaMusa: 1320,
	iCasimir: 1340,
	iSobieski: 1680,
	iPilsudski: 1930,
	iWalesa: 1990,
	iAfonso: 1140,
	iJoao: 1490,
	iMaria: 1830,
	iHuaynaCapac: 1500,
	iLorenzo: 1470,
	iCavour: 1860,
	iGenghisKhan: 1210,
	iKublaiKhan: 1260,
	iMontezuma: 1440,
	iTughluq: 1330,
	iAkbar: 1560,
	iNaresuan: 1590,
	iMongkut: 1860,
	iGustav: 1620,
	iIvan: 1540,
	iPeter: 1690,
	iCatherine: 1770,
	iAlexanderI: 1810,
	iMehmed: 1450,
	iSuleiman: 1520,
	iAtaturk: 1930,
	iMbemba: 1510,
	iAbbas: 1590,
	iWillemVanOranje: 1570,
	iWilliam: 1650,
	iFrederick: 1740,
	iBismarck: 1880,
	iWashington: 1790,
	iLincoln: 1860,
	iRoosevelt: 1940,
	iSanMartin: 1820,
	iPeron: 1950,
	iJuarez: 1860,
	iSantaAnna: 1850,
	iCardenas: 1940,
	iBolivar: 1820,
	iPedro: 1840,
	iVargas: 1930,
	iMacDonald: 1870,
	iTrudeau: 1970,
	iHiawatha: 1450,
	iTigranes: -95,
	iAshot: 862,
	iAndranik: 1914,
	iAriadne: -1700,
	iMithridates: -140,
	iAgamemnon: -1200,
	iBulan: 740,
}

RELIGION_FOUNDING_DATES = {
	iJudaism: -2000,
	iOrthodoxy: 40,
	iCatholicism: 500,
	iProtestantism: 1521,
	iIslam: 622,
	iHinduism: -1500,
	iBuddhism: 80,
	iConfucianism: -500,
	iTaoism: -400,
	iZoroastrianism: -600,
	iShia: 680,
}

WONDER_ORIGINAL_BUILDERS = {
	iPalaceOfMinos: (iMinoans, -1900),
	iGreatLighthouse : (iEgypt, -284),
	iGreatLibrary : (iEgypt, -285),
	iPyramids : (iEgypt, -2600),
	iGreatSphinx : (iEgypt, -2500),
	iHangingGardens : (iBabylonia, -600),
	iIshtarGate : (iBabylonia, -575),
	iAlKhazneh : (iIndependent, 100),
	iSalsalBuddha : (iIndependent, 570),
	iJewishShrine : (iIndependent, -957),
	iShwedagonPaya : (iIndependent, 1362),
	iCatholicShrine : (iRome, 318),
	iTaoistShrine : (iChina, 1460),
	iGreatWall : (iChina, -221),
	iConfucianShrine : (iChina, -205),
	iDujiangyan : (iChina, -256),
	iTerracottaArmy : (iChina, -210),
	iForbiddenPalace : (iChina, 1420),
	iGrandCanal : (iChina, 618),
	iPorcelainTower : (iChina, 1431),
	iOracle : (iGreece, -800),
	iParthenon : (iGreece, -438),
	iTempleOfArtemis : (iGreece, -323),
	iColossus : (iGreece, -280),
	iHinduShrine : (iIndia, -322),
	iBuddhistShrine : (iIndia, -260),
	iIronPillar : (iIndia, 375),
	iNalanda : (iIndia, 427),
	iVijayaStambha : (iIndia, 1448),
	iKhajuraho : (iIndia, 885),
	iGreatCothon : (iPhoenicia, -600),
	iMoaiStatues : (iPolynesia, 1250),
	iApadanaPalace : (iPersia, -488),
	iZoroastrianShrine : (iPersia, -400),
	iGreatMausoleum : (iPersia, -350),
	iGondeshapur : (iPersia, 256),
	iAquaAppia : (iRome, -312),
	iFlavianAmphitheatre : (iRome, 80),
	iTempleOfKukulkan : (iMaya, 800),
	iMonolithicChurch : (iEthiopia, 1181),
	iJetavanaramaya : (iDravidia, 273),
	iCheomseongdae : (iKorea, 632),
	iPyramidOfTheSun : (iToltecs, 200),
	iOrthodoxShrine : (iByzantium, 335),
	iTheodosianWalls : (iByzantium, 413),
	iHagiaSophia : (iByzantium, 537),
	iMountAthos : (iByzantium, 800),
	iUniversityOfSankore : (iMali, 988),
	iGreatAdobeMosque : (iMali, 1300),
	iItsukushimaShrine : (iJapan, 1593),
	iHimejiCastle : (iJapan, 1333),
	iGurEAmir : (iTurks, 1404),
	iDomeOfTheRock : (iArabia, 692),
	iSpiralMinaret : (iArabia, 851),
	iIslamicShrine : (iArabia, 692),
	iHouseOfWisdom : (iArabia, 754),
	iAlamut : (iArabia, 1090),
	iPotalaPalace : (iTibet, 1694),
	iBorobudur : (iJava, 825),
	iPrambanan : (iJava, 850),
	iEscorial : (iSpain, 1584),
	iMezquita : (iMoors, 785),
	iNotreDame : (iFrance, 1260),
	iVersailles : (iFrance, 1661),
	iLouvre : (iFrance, 1692),
	iKrakDesChevaliers : (iFrance, 1140),
	iWatPreahPisnulok : (iKhmer, 1113),
	iOxfordUniversity : (iEngland, 1096),
	iProtestantShrine : (iHolyRome, 1503),
	iSaintThomasChurch : (iHolyRome, 1496),
	iSaltCathedral : (iPoland, 1330),
	iOldSynagogue : (iPoland, 1407),
	iTorreDeBelem : (iPortugal, 1519),
	iSantaMariaDelFiore : (iItaly, 1436),
	iSanMarcoBasilica : (iItaly, 1063),
	iSistineChapel : (iItaly, 1541),
	iSilverTreeFountain : (iMongols, 1220),
	iFloatingGardens : (iAztecs, 1350),
	iShalimarGardens : (iTimurids, 1642),
	iHarmandirSahib : (iTimurids, 1604),
	iTajMahal : (iTimurids, 1653),
	iRedFort : (iTimurids, 1648),
	iSaintSophia : (iRussia, 1031),
	iKremlin : (iRussia, 1495),
	iSaintBasilsCathedral : (iRussia, 1561),
	iTopkapiPalace : (iOttomans, 1465),
	iBlueMosque : (iOttomans, 1616),
	iImageOfTheWorldSquare : (iIran, 1629),
	iBourse : (iNetherlands, 1602),
	iAmberRoom : (iGermany, 1700),
}

DEFAULT_CIV_DESCRIPTIONS = {}


@handler("fontsLoaded")
def loadCivDescriptions():
	global DEFAULT_CIV_DESCRIPTIONS
	DEFAULT_CIV_DESCRIPTIONS = dict((iCiv, infos.civ(iCiv).getDescriptionKeyPersistent()) for iCiv in infos.civs())


class GreatWall(object):

	def __init__(self, *args, **kwargs):
		self.tGraphicsTL = kwargs.get("tGraphicsTL")
		self.tGraphicsBR = kwargs.get("tGraphicsBR")
		self.lGraphicsExceptions = kwargs.get("lGraphicsExceptions", [])
		self.lBorderExceptions = kwargs.get("lBorderExceptions", [])
		self.lClearCulture = kwargs.get("lClearCulture", [])
		
		self.lEffectAreas = kwargs.get("lEffectAreas", [])
		
	def apply(self):
		city = getBuildingCity(iGreatWall, False)
		if not city:
			return
			
		iOwner = city.getOwner()
		iOldArea = city.getArea()
		iNewArea = plots.capital(iAmerica).getArea()
		
		greatWall = plots.rectangle(self.tGraphicsTL, self.tGraphicsBR)
		
		for plot in greatWall.expand(1).land().without(self.lBorderExceptions):
			plot.setArea(iNewArea)
			
		for plot in plots.of(self.lClearCulture):
			plot.setOwner(-1)
		
		for plot in greatWall.without(self.lGraphicsExceptions):
			plot.setOwner(iOwner)
		
		for plot in plots.sum(plots.rectangle(*tCorners).without(self.lGraphicsExceptions).land() for tCorners in self.lEffectAreas):
			plot.setWithinGreatWall(True)


class Revealed(object):

	def __init__(self, *args, **kwargs):
		self.lLandRegions = kwargs.get("lLandRegions", [])
		self.lCoastRegions = kwargs.get("lCoastRegions", [])
		self.lSeaAreas = kwargs.get("lSeaAreas", [])
	
	def getArea(self):	
		landPlots = plots.regions(*self.lLandRegions).where(CyPlot.isOwned)
		coastPlots = plots.regions(*self.lCoastRegions).coastal().expand(1).water()
		seaPlots = plots.sum(plots.rectangle(*tArea) for tArea in self.lSeaAreas).water()
		
		return landPlots + coastPlots + seaPlots
			

class Scenario(object):

	def __init__(self, *args, **kwargs):
		self.iStartYear = kwargs.get("iStartYear")
		self.fileName = kwargs.get("fileName")
		
		self.lCivilizations = kwargs.get("lCivilizations", [])
		
		self.dCivilizationDescriptions = kwargs.get("dCivilizationDescriptions", {})
		
		self.dOwnedTiles = kwargs.get("dOwnedTiles", {})
		self.iCultureTurns = kwargs.get("iCultureTurns", 0)
		
		self.lTribalVillages = kwargs.get("lTribalVillages", [])
		
		self.dRevealed = kwargs.get("dRevealed", {})
		
		self.dGreatPeopleCreated = kwargs.get("dGreatPeopleCreated", {})
		self.dGreatGeneralsCreated = kwargs.get("dGreatGeneralsCreated", {})
		
		self.dColonistsAlreadyGivenPreIndustrial = kwargs.get("dColonistsAlreadyGivenPreIndustrial", {})
		
		self.lInitialWars = kwargs.get("lInitialWars", [])
		
		self.lAllGoalsFailed = kwargs.get("lAllGoalsFailed", [])
		self.lGoalsSucceeded = kwargs.get("lGoalsSucceeded", [])
		self.setupGoals = kwargs.get("setupGoals", lambda *args: None)
		
		self.createStartingUnits = kwargs.get("createStartingUnits", lambda: None)
		self.updateData = kwargs.get("updateData", lambda: None)
		
		self.greatWall = kwargs.get("greatWall", GreatWall())
	
	def adjustTurns(self, bFinal=True):
		iStartTurn = getGameTurnForYear(self.iStartYear, START_HISTORY, game.getCalendar(), game.getGameSpeedType())
		
		game.setStartYear(START_HISTORY)
		game.setStartTurn(iStartTurn)
		game.setGameTurn(iStartTurn)
		
		if bFinal:
			game.setMaxTurns(game.getEstimateEndTurn() - iStartTurn)
		
	def setupCivilizations(self):
		for iCiv, description in DEFAULT_CIV_DESCRIPTIONS.items():
			infos.civ(iCiv).setDescriptionKeyPersistent(description)
	
		for iCiv, description in self.dCivilizationDescriptions.items():
			infos.civ(iCiv).setDescriptionKeyPersistent(description)
	
		for i, iCiv in enumerate(lBirthOrder):
			infos.civ(iCiv).setDescription("%02d" % i)
			
		for iCiv in range(iNumCivs):
			iCivStartYear = infos.civ(iCiv).getStartingYear()
			infos.civ(iCiv).setPlayable(iCivStartYear != 0 and iCivStartYear >= self.iStartYear)
		
		for civ in self.lCivilizations:
			civ.info.setPlayable(civ.isPlayable())
	
	def setupLeaders(self):
		self.adjustTurns(False)
	
		for iCiv in range(iNumCivs):
			leaders = infos.leaders().where(lambda iLeader: infos.civ(iCiv).isOriginalLeader(iLeader) and iLeader in LEADER_DATES).sort(lambda iLeader: LEADER_DATES.get(iLeader, 2020))
			if not leaders:
				continue
			
			before, after = leaders.split(lambda iLeader: LEADER_DATES.get(iLeader, 2020) < self.iStartYear)
			if not after or (before and since(year(LEADER_DATES.get(before.last(), 2020))) < until(year(LEADER_DATES.get(after.first(), 2020)))):
				after = after.including(before.last())
				
			for iLeader in range(iNumLeaders):
				infos.civ(iCiv).setLeader(iLeader, infos.civ(iCiv).isOriginalLeader(iLeader) and iLeader in after)
	
	def init(self):
		event_handler_registry.reset()
		
		initWars(game.getActivePlayer())
		
		for civ in self.lCivilizations:
			iCiv = civ.iCiv
			bMinor = not civ.isPlayable()
			
			if game.getActiveCivilizationType() == iCiv:
				continue
			
			iPlayer = bMinor and findMinorSlot(iCiv) or findSlot(iCiv)
			addPlayer(iPlayer, iCiv, bAlive=True, bMinor=bMinor)
			
			initWars(iPlayer)
	
		events.fireEvent("playerCivAssigned", game.getActivePlayer(), game.getActiveCivilizationType())
		events.fireEvent("playerCivAssigned", gc.getBARBARIAN_PLAYER(), iBarbarian)

		data.dSlots[game.getActiveCivilizationType()] = game.getActivePlayer()
		data.dSlots[iBarbarian] = gc.getBARBARIAN_PLAYER()
	
	def initGoals(self, iPlayer, goals):
		iCiv = civ(iPlayer)
		
		if iCiv in self.lAllGoalsFailed:
			for goal in goals:
				goal.fail()
				
		for iGoalCiv, iGoalIndex in self.lGoalsSucceeded:
			if iCiv == iGoalCiv:
				goals[iGoalIndex].succeed()
		
		self.setupGoals(iCiv, goals)
		
	def apply(self):
		self.adjustTurns()
	
		for civilization in self.lCivilizations:
			civilization.apply()
		
		setupScenarioResources()
		
		self.updatePeriods()
		self.createStartingUnits()
		
		self.greatWall.apply()
		self.adjustTerritories()
		
		self.adjustReligions()
		self.adjustWonders()
		self.adjustGreatPeople()
		self.adjustColonists()
		
		self.revealTiles()
		
		self.initDiplomacy()
		
		self.restoreCivs()
		self.restoreLeaders()
		
		self.updateData()
		self.updateNames()
		self.updateCityWork()
	
	def adjustTerritories(self):
		for city in cities.all():
			for _ in range(turns(self.iCultureTurns)):
				city.doPlotCulture(False, city.getOwner(), city.getModifiedCultureRate(), True)
		
		for iCiv, lTiles in self.dOwnedTiles.items():
			for plot in plots.of(lTiles):
				convertPlotCulture(plot, slot(iCiv), 100, True)
	
	def adjustReligions(self):
		for iReligion, iFoundingYear in RELIGION_FOUNDING_DATES.items():
			if game.isReligionFounded(iReligion):
				game.setReligionGameTurnFounded(iReligion, year(iFoundingYear))
		
		game.setVoteSourceReligion(1, iCatholicism, False)
	
	def adjustWonders(self):
		for iWonder, (iCiv, iYear) in WONDER_ORIGINAL_BUILDERS.items():
			city = getBuildingCity(iWonder, False)
			iEarliestYear = game.getTurnYear(year(min(iYear, self.iStartYear)))
			if city:
				city.setBuildingOriginalOwner(iWonder, iCiv)
				city.setBuildingOriginalTime(iWonder, iEarliestYear)
			elif iYear < self.iStartYear:
				game.incrementBuildingClassCreatedCount(infos.building(iWonder).getBuildingClassType())
	
	def adjustGreatPeople(self):
		for iCiv, iGreatPeople in self.dGreatPeopleCreated.items():
			player(iCiv).changeGreatPeopleCreated(iGreatPeople)
		
		for iCiv, iGreatGenerals in self.dGreatGeneralsCreated.items():
			player(iCiv).changeGreatPeopleCreated(iGreatGenerals)
	
	def adjustColonists(self):
		iStartTurn = scenarioStartTurn()
		
		for iCiv, iColonists in self.dColonistsAlreadyGivenPreIndustrial.items():
			data.players[iCiv].iExplorationTurn = iStartTurn
			data.players[iCiv].iColonistsAlreadyGivenPreIndustrial = iColonists
	
	def revealTiles(self):
		for iGroup, revealed in self.dRevealed.items():
			revealedPlots = revealed.getArea()
			revealedPlots = revealedPlots.expand(1).unique()
			
			for iPlayer in players.group(iGroup):
				iTeam = player(iPlayer).getTeam()
				for plot in revealedPlots + plots.birth(iPlayer) + plots.core(iPlayer):
					plot.setRevealed(iTeam, True, False, -1)
	
	def initDiplomacy(self):
		for iAttacker, iDefender, iWarPlan in self.lInitialWars:
			team(iAttacker).declareWar(player(iDefender).getTeam(), False, iWarPlan)
	
	def restoreCivs(self):
		for iCiv in range(iNumCivs):
			infos.civ(iCiv).setPlayable(infos.civ(iCiv).getStartingYear() != 0)
	
	def restoreLeaders(self):
		for iCiv in range(iNumCivs):
			for iLeader in range(iNumLeaders):
				infos.civ(iCiv).setLeader(iLeader, infos.civ(iCiv).isOriginalLeader(iLeader))
	
	def updateNames(self):
		for iPlayer in players.major():
			checkName(iPlayer)
	
	def updateCityWork(self):
		for city in cities.all():
			city.AI_updateAssignWork()
	
	def updatePeriods(self):
		for iYear, dPeriods in dScenarioPeriods.items():
			if self.iStartYear >= iYear:
				for iCiv, iPeriod in dPeriods.items():
					setPeriod(iCiv, iPeriod)
