from Core import *
from RFCUtils import *

import BugPath as path

import Setup
import os

EXPORT_MAPS_PATH = "Assets/Maps"

IMAGE_LOCATION = os.getcwd() + "\Mods\\DoC-Cross-Overhaul\\Export"
iLongestName = len("Netherlands") #Netherlands currently has the longest civ name

gc = CyGlobalContext()

def getTLBR(lPlots):
	lPlotX = [plot.getX() for plot in plots.of(lPlots)]
	lPlotY = [plot.getY() for plot in plots.of(lPlots)]
	TL = (min(lPlotX), min(lPlotY))
	BR = (max(lPlotX), max(lPlotY))
	return TL, BR

def getCivName(iPlayer):
	if civ(player(iPlayer)) == iHolyRome:
		return "HolyRome"
	elif civ(player(iPlayer)) == iTurks:
		return "Turks"
	elif civ(player(iPlayer)) == iOttomans:
		return "Ottomans"
	return name(iPlayer)

def exportFlip(iPlayer, (lHumanFlipPlot, lAIFlipPlots)):
	sLocation = "FlipZones"
	sName = getCivName(iPlayer)
	sDictName = "dBirthArea"
	
	BL, TR = getTLBR(lHumanFlipPlot)
	lExtended = lHumanFlipPlot + lAIFlipPlots
	BLai, TRai = getTLBR(lExtended)
	
	tExceptions = None
	lExceptions = plots.rectangle(BLai, TRai).without(lExtended)
	if lExceptions:
		tExceptions = ("dBirthAreaExceptions", lExceptions)
	
	lExtraDictList = None
	if lAIFlipPlots:
		lExtraDictList = [("dExtendedBirthArea", (BLai, TRai))]
		
	writeTRBLDictFile(sLocation, sName, (BL, TR), sDictName, tExceptions, lExtraDictList = lExtraDictList)
	
	show("Flipzone of %s exported" % sName) 

def exportCore(iPlayer):
	sLocation = "Cores"
	sName = getCivName(iPlayer)
	sDictName = "dCoreArea"
	
	lCorePlots = plots.core(iPlayer)
	BL, TR = getTLBR(lCorePlots)

	tExceptions = None
	lExceptions = plots.rectangle(BL, TR).land().where(lambda p: not (p.isPeak() and location(p) not in lPeakExceptions) and not p.isPlayerCore(iPlayer))
	if lExceptions:
		tExceptions = ("dCoreAreaExceptions", lExceptions)
	
	writeTRBLDictFile(sLocation, sName, (BL, TR), sDictName, tExceptions)
	
	show("Core of %s exported" % sName) 

def exportSettlerMap(iPlayer):
	sLocation = "SettlerValues"
	sName = getCivName(iPlayer)
	valueFunction = getSettlerValue
	writeMapFile(sLocation, sName, valueFunction, iPlayer = iPlayer, bDictStyle = True)
	
	show("Settlermap of %s exported" % sName)
	
def getSettlerValue(plot, *args, **kwargs):
	iPlayer = kwargs.get('iPlayer', None)
	
	if plot.isWater():
		return 0
	elif plot.isPeak() and location(plot) in lPeakExceptions:
		return 0
		
	if iPlayer is not None:
		return plot.getPlayerSettlerValue(iPlayer)
		
	return 0

def exportWarMap(iPlayer):
	sLocation = "WarMaps"
	sName = getCivName(iPlayer)
	valueFunction = getWarValue
	writeMapFile(sLocation, sName, valueFunction, iPlayer = iPlayer, bDictStyle = True)
	
	show("Warmap of %s exported" % sName)
	
def getWarValue(plot, *args, **kwargs):
	iPlayer = kwargs.get('iPlayer', None)
	if iPlayer is not None:
		return plot.getPlayerWarValue(iPlayer)
	return 0


#TODO: use export to csv function in map branch when merged
def exportRegionMap():
	sLocation = "other"
	sName = "RegionMap"
	valueFunction = getRegionValue
	writeMapFile(sLocation, sName, valueFunction, sMapName = "tRegionMap")
	
	show("Regionmap exported")
	
def getRegionValue(plot, *args, **kwargs):

	#TODO: bAutoWater should be removed if water features get their own region ID
	bAutoWater = True
	if plot.isWater() and bAutoWater:
		return -1
		
	return plot.getRegionID()


def exportAreaExport(lPlots, bWaterException, bPeakException):
	if not lPlots:
		show("No area selected")
		return
	
	x_coords, y_coords = zip(*lPlots)
	tTL = (min(x_coords), min(y_coords))
	tBR = (max(x_coords), max(y_coords))
	
	exceptions = [location(p) for p in plots.rectangle(tTL, tBR) if location(p) not in lPlots and not p.isWater()]

	file_path = "%s/%s/%s" % (path.getModDir(), EXPORT_MAPS_PATH, "Export/Area.txt")
	file = open(file_path, "w")
	
	try:
		content = "rectangle = (%s,\t%s)\nexceptions = %s\nlist = %s" % (tTL, tBR, exceptions, lPlots)
		file.write(content)
		show("Area exported")
	finally:
		file.close()
		
	"""
	if lPlots:
		sLocation = "other"
		sName = "NewArea"
		sDictName = "NewArea"
	
		BL, TR = getTLBR(lPlots)
		
		tExceptions = None
		lExceptions = plots.start(BL).end(TR).where(lambda p: location(p) not in lPlots)
		
		if bWaterException:
			lExceptions = plots.start(BL).end(TR).where(lambda p: p.isWater() or p in lExceptions)
		if bPeakException:
			lExceptions = plots.start(BL).end(TR).where(lambda p: p.isPeak() or p in lExceptions)
			
		if lExceptions:
			tExceptions = ("Exceptions", lExceptions)
			
		writeTRBLDictFile(sLocation, sName, (BL, TR), sDictName, tExceptions, False)
		
		show("Area exported")
	else:
		show("No area selected")
	"""


def writeMapFile(sFileLocaton, sName, valueFunction, *args, **kwargs):
	sMapName = kwargs.get('sMapName', None)
	bDictStyle = kwargs.get('bDictStyle', False)
	
	file = open(IMAGE_LOCATION + "\\" + sFileLocaton + "\\" + sName + ".txt", 'wt')

	try:
		if sMapName:
			file.write(sMapName + " = ( \n")
		else:
			file.write("(")
		for y in reversed(range(iWorldY)):
			sLine = "(\t"
			for x in range(iWorldX):
				plot = plot_(x, y)
				iValue = valueFunction(plot, *args, **kwargs)
				sLine += "%d,\t" % iValue
			if y == 0 and bDictStyle:
				sLine += ")),"
			else:
				sLine += "),\n"
			file.write(sLine)
		if not bDictStyle:
			file.write(")")
	finally:
		file.close()

def writeTRBLDictFile(sFileLocaton, sName, tSquare, sDictName, tExceptions = None, bIsDictionary = True, lExtraDictList = None):
	BL, TR = tSquare
	
	sIdentifierText = ""
	if bIsDictionary:
		sIdentifier = "i" + sName
		# allign tabs
		iTabs = (iLongestName - len(sName) - 1) // 4 + 1
		sIdentifierText = sIdentifier + " :" + iTabs*"\t"
	
	file = open(IMAGE_LOCATION + "\\" + sFileLocaton + "\\" + sName + ".txt", 'wt')
	try:
		file.write("# " + sDictName + "\n")
		file.write(sIdentifierText + "("+ str(BL) + ",\t" + str(TR) + ")")
		if bIsDictionary:
			file.write(",")
			
		if tExceptions:
			sExceptionName, lExceptions = tExceptions
			file.write("\n\n# " + sExceptionName + "\n")
			file.write(sIdentifierText + str(lExceptions))
			if bIsDictionary:
				file.write(",")
				
		if lExtraDictList:
			for sListName, lList in lExtraDictList:
				file.write("\n\n# " + sListName + "\n")
				file.write(sIdentifierText + str(lList))
				if bIsDictionary:
					file.write(",")
	finally:
		file.close()