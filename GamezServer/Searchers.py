import GamezServer
import urllib
import urllib2

from GamezServer.IPTorrents import IPTorrents
from GamezServer.NZBFinder import NZBFinder
from GamezServer.UsenetCrawler import UsenetCrawler
from GamezServer.DAO import DAO


class Searchers(object):
    """description of class"""

    def GetSearcher(self, searcherName, forceNew):
        if searcherName == "usenetCrawler":
            return UsenetCrawler(forceNew)
        if searcherName == "nzbfinder":
            return NZBFinder(forceNew)
        if searcherName == "iptorrents":
            return IPTorrents(forceNew)
        return None

    def SendToSab(self, sabnzbdBaseUrl, sabnzbdApiKey, nzbLink, nzbTitle, wantedGameId):
        dao = DAO()
        nzbTitle = "[" + str(wantedGameId) + "] - " + nzbTitle
        category = dao.GetSiteMasterData('sabnzbdCategory')
        sabUrl = sabnzbdBaseUrl
        if not sabUrl.endswith('/'):
            sabUrl = sabUrl + "/"
        sabUrl = sabUrl + "sabnzbd/api"
        sabUrl = sabUrl + "?apikey=" + sabnzbdApiKey
        sabUrl = sabUrl + "&mode=addurl&name=" + urllib.quote_plus(nzbLink)
        sabUrl = sabUrl + "&nzbname=" + urllib.quote_plus(nzbTitle)
        if category is not None and category != "":
            sabUrl = sabUrl + "&cat=" + category
        sabRequest = urllib2.Request(sabUrl, headers={'User-Agent': "GamezServer"})
        response = urllib2.urlopen(sabRequest)
        sabRespData = response.read()
        return sabRespData

    def send_to_rtorrent(self, rtorrentBaseUrl, rtorrentUsername, rtorrentPassword, torrentLink):
        dao = DAO()
        rtorrentAuthMethod = "Digest"
        category = dao.GetSiteMasterData('rtorrentLabel')
        rpcURL = rtorrentBaseUrl
        #TODO: write RPC requests
        rtorrentRespData = ""
        return rtorrentRespData
