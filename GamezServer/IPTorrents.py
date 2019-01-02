import urllib2
from xml.etree import ElementTree

import Searchers
from GamezServer.DAO import DAO


class IPTorrents(object):

    def __init__(self, forceNew=False):
        self.forceNew = forceNew

    def search(self, wantedGameId):
        dao = DAO()
        iptorrentsEnabled = dao.GetSiteMasterData("iptorrentsEnabled")
        iptorrentsRssURL = dao.GetSiteMasterData("iptorrentsRssURL")
        rtorrentEnabled = dao.GetSiteMasterData("rtorrentEnabled")
        rtorrentBaseUrl = dao.GetSiteMasterData("rtorrentBaseUrl")
        rtorrentUsername = dao.GetSiteMasterData("rtorrentUsername")
        rtorrentPassword = dao.GetSiteMasterData("rtorrentPassword")
        rtorrentLabel = dao.GetSiteMasterData("rtorrentLabel")
        rtorrentDir = dao.GetSiteMasterData("rtorrentDir")
        if (
                iptorrentsEnabled is not None and iptorrentsEnabled == "true"
                and iptorrentsRssURL is not None and iptorrentsRssURL != ""
                and rtorrentEnabled is not None and rtorrentEnabled == "true"
                and rtorrentUsername is not None and rtorrentUsername != ""
                and rtorrentPassword is not None and rtorrentPassword != ""
                and rtorrentPassword is not None and rtorrentPassword != ""
                and rtorrentBaseUrl is not None and rtorrentBaseUrl != ""
                and rtorrentLabel is not None and rtorrentLabel != ""
                and rtorrentDir is not None and rtorrentDir != ""
        ):
            return self.search_and_send_to_downloader(iptorrentsRssURL,
                                                      rtorrentBaseUrl, rtorrentUsername, rtorrentPassword,
                                                      wantedGameId)
        else:
            return ""

    def search_and_send_to_downloader(self, iptorrentsRssURL,
                                      rtorrentBaseUrl, rtorrentUsername, rtorrentPassword,
                                      wantedGameId):
        webRequest = urllib2.Request(iptorrentsRssURL, None, {'User-Agent': "GamezServer"})
        response = urllib2.urlopen(webRequest)
        gameData = response.read()
        treeData = ElementTree.fromstring(gameData)
        for matchedElement in treeData.findall('./channel/item'):
            torrentTitle = matchedElement.find('title').text
            torrentLink = matchedElement.find('link').text
            torrentId = hash(torrentTitle)
            if self.forceNew:
                continue
            searchers = Searchers.Searchers()
            sabRespData = searchers.send_to_rtorrent(rtorrentBaseUrl, rtorrentUsername, rtorrentPassword, torrentLink)
            if sabRespData == b'ok\n':
                dao = DAO()
                dao.LogMessage("Snatched Game" + torrentTitle, "Info")
                dao.UpdateWantedGameStatus(wantedGameId, "Snatched")
                dao.AddSnatchedHistory("IPTorrents", torrentId)
                return "Snatched Game: " + torrentTitle
