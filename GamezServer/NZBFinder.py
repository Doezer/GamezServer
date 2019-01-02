import GamezServer
from GamezServer.DAO import DAO
import urllib
from xml import etree
from xml.etree import ElementTree
import urllib2
import Searchers


class NZBFinder(object):
    defaultCategory = "1000"
    categories = {
        'Nintendo 3DS': '1011',
        'Sega Dreamcast': '1082',
        'Nintendo Gamecube': '1083',
        'Nintendo DS': '1010',
        'Sony Playstation 2': '1081',
        'Sony Playstation 3': '1080',
        'Sony PSP': '1020',
        'Nintendo Wii': '1030,1060',
        'Microsoft Xbox': '1040',
        'Microsoft Xbox 360': '1050,1070'
    };

    def __init__(self, forceNew=False):
        self.forceNew = forceNew

    def search(self, platform, title, wantedGameId):
        dao = DAO()
        nzbFinderEnabled = dao.GetSiteMasterData("nzbFinderEnabled")
        nzbFinderApiKey = dao.GetSiteMasterData("nzbFinderApiKey")
        sabnzbdEnabled = dao.GetSiteMasterData("sabnzbdEnabled")
        sabnzbdApiKey = dao.GetSiteMasterData("sabnzbdApiKey")
        sabnzbdBaseUrl = dao.GetSiteMasterData("sabnzbdBaseUrl")
        if (
                nzbFinderEnabled != None and nzbFinderEnabled == "true" and nzbFinderApiKey != None and nzbFinderApiKey != "" and sabnzbdEnabled != None and sabnzbdEnabled == "true" and sabnzbdApiKey != None and sabnzbdApiKey != "" and sabnzbdBaseUrl != None and sabnzbdBaseUrl != ""):
            return self.SearchAndSendToSab(nzbFinderApiKey, sabnzbdApiKey, platform, title, wantedGameId,
                                           sabnzbdBaseUrl)
        else:
            return ""

    def SearchAndSendToSab(self, nzbFinderApiKey, sabnzbdApiKey, platform, title, wantedGameId, sabnzbdBaseUrl):
        cat = self.categories.get(platform, self.defaultCategory)
        nzbFinderUrl = "https://nzbfinder.ws/api?apikey=" + nzbFinderApiKey + "&t=search&q=" + urllib.quote_plus(
            title) + "cat=" + cat

        webRequest = urllib2.Request(nzbFinderUrl, None, {'User-Agent': "GamezServer"})
        response = urllib2.urlopen(webRequest)
        gameData = response.read()
        treeData = ElementTree.fromstring(gameData)
        for matchedElement in treeData.findall('./channel/item'):
            nzbTitle = matchedElement.find('title').text
            nzbLink = matchedElement.find('link').text
            nzbFinderNzbId = matchedElement.find("guid").text.split('/')[
                len(matchedElement.find("guid").text.split('/')) - 1]
            if (self.forceNew):
                continue
            searchers = Searchers.Searchers()
            sabRespData = searchers.SendToSab(sabnzbdBaseUrl, sabnzbdApiKey, nzbLink, nzbTitle, wantedGameId)
            if (sabRespData == b'ok\n'):
                dao = DAO()
                dao.LogMessage("Snatched Game" + nzbTitle, "Info")
                dao.UpdateWantedGameStatus(wantedGameId, "Snatched")
                dao.AddSnatchedHistory("nzbFinder", nzbFinderNzbId)
                return "Snatched Game: " + nzbTitle
