# -*- coding: utf-8 -*-
import HTMLParser
import cookielib
import os
import re
import urllib
import urllib2
import unicodedata
import zlib
import json
import shutil
import bs4

try:
    import xbmc
    import xbmcvfs
    import xbmcaddon
    import xbmcgui
except ImportError:
    from tests.stubs import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs

__addon__ = xbmcaddon.Addon()
__version__ = __addon__.getAddonInfo('version')  # Module version
__scriptname__ = __addon__.getAddonInfo('name')
__language__ = __addon__.getLocalizedString
__profile__ = unicode(xbmc.translatePath(__addon__.getAddonInfo('profile')), 'utf-8')
__temp__ = unicode(xbmc.translatePath(os.path.join(__profile__, 'temp', '')), 'utf-8')


def normalizeString(str):
    return unicodedata.normalize(
        'NFKD', unicode(unicode(str, 'utf-8'))
    ).encode('utf-8', 'ignore')


def log(msg):
    xbmc.log((u"### [%s] - %s" % (__scriptname__, msg,)).encode('utf-8'), level=xbmc.LOGDEBUG)


def notify(msg_id):
    xbmc.executebuiltin((u'Notification(%s,%s)' % (__scriptname__, __language__(msg_id))).encode('utf-8'))


class NapisyHelper:
    BASE_URL = "http://napisy24.pl"

    def __init__(self):
        self.urlHandler = URLHandler()

    def get_subtitle_list(self, item):
        if item["tvshow"]:
            search_results = self._search_tvshow(item)
            results = self._build_tvshow_subtitle_list(search_results, item)
            log("Results: %s" % results)
        else:
            search_results = self._search_movie(item)
            # results = self._build_movie_subtitle_list(search_results, item)

        return results

    def download(self, id, zip_filename):
        ## Cleanup temp dir, we recomend you download/unzip your subs in temp folder and
        ## pass that to XBMC to copy and activate
        if xbmcvfs.exists(__temp__):
            shutil.rmtree(__temp__)
        xbmcvfs.mkdirs(__temp__)

        subtitle_type_map = ["sru", "sr", "tmp", "mdvd", "mpl2"]
        subs_format = int(__addon__.getSetting("subs_format"))

        query = {"napisId": id,
                 "typ": subtitle_type_map[subs_format]}

        f = self.urlHandler.request(self.BASE_URL + "/download", query, referer=self.BASE_URL)

        if f is None and self.login(True):
            f = self.urlHandler.request(self.BASE_URL + "/download", query, referer=self.BASE_URL)

        with open(zip_filename, "wb") as subFile:
            subFile.write(f)
        subFile.close()
        xbmc.sleep(500)

        xbmc.executebuiltin(('XBMC.Extract("%s","%s")' % (zip_filename, __temp__,)).encode('utf-8'), True)

    def login(self, notify_success=False):
        username = __addon__.getSetting("username")
        password = __addon__.getSetting("password")
        post_data = {"username": username, "passwd": password, "Submit": ""}
        content = self.urlHandler.request(self.BASE_URL + "/cb-login", data=post_data)

        if content.find('http://napisy24.pl/cb-logout') > -1:
            self.urlHandler.save_cookie();

            if notify_success:
                notify(32014)

            return True
        else:
            notify(32005)
            return False

    # return list of tv-series from the site`s search
    def _search_tvshow(self, item):
        results = []

        search_string = re.split(r'\s\(\w+\)$', item["tvshow"])[0]

        data = {"serial": search_string.encode("utf-8").lower(), "sezon": item["season"], "epizod": item["episode"]}
        search_result = self.urlHandler.request(self.BASE_URL + "/run/pages/serial_napis.php", None, data)
        if search_result is None:
            return results  # return empty set

        search_result = json.loads(search_result, encoding="utf-8")

        return search_result

    def _build_tvshow_subtitle_list(self, search_results, item):
        results = []
        total_downloads = 0
        language = "pl"
        lang3 = xbmc.convertLanguage(language, xbmc.ISO_639_2)

        if lang3 in item["3let_language"]:
            for result in search_results:
                html = bs4.BeautifulSoup(result["table"], "html.parser")
                versions = [tag["data-wydanie"] for tag in html.find_all("h6", attrs={"data-wydanie": True})][0].split(
                    "; ")
                total_downloads += int(result["pobran"])

                for version in versions:
                    title = "%s.%s" % (result["serial"].title().replace(" ", "."), version)
                    language = "pl"
                    video_file_size = re.findall("([\d.]+) MB", result["table"])[0]

                    results.append({
                        'lang_index': item["3let_language"].index(lang3),
                        'filename': title,
                        'language_name': xbmc.convertLanguage(language, xbmc.ENGLISH_NAME),
                        'language_flag': language,
                        'id': result["napisid"],
                        'rating': int(result["pobran"]),
                        'sync': self._is_synced(item, video_file_size, title),
                        'hearing_imp': False,
                        'is_preferred': lang3 == item['preferredlanguage']
                    })

            # Fix the rating
            if total_downloads:
                for it in results:
                    it["rating"] = str(min(int(round(it["rating"] / float(total_downloads), 1) * 8), 5))

        return sorted(results, key=lambda x: (x['is_preferred'], x['lang_index'], x['sync'], x['rating']), reverse=True)

    def _is_synced(self, item, video_file_size, version):
        sync = False

        if len(video_file_size) > 0:
            video_file_size = float(video_file_size)
            file_size = round(item["file_original_size"] / float(1048576), 2)
            if file_size == video_file_size:
                sync = True

        if not sync:
            sync = self._calc_rating(version, item["file_original_path"]) >= 3.8

        return sync

    def _calc_rating(self, vesrion, file_original_path):
        file_name = os.path.basename(file_original_path)
        folder_name = os.path.split(os.path.dirname(file_original_path))[-1]

        vesrion = re.sub(r'\W+', '.', vesrion).lower()
        file_name = re.sub(r'\W+', '.', file_name).lower()
        folder_name = re.sub(r'\W+', '.', folder_name).lower()
        log("# Comparing Releases:\n [subtitle-rls] %s \n [filename-rls] %s \n [folder-rls] %s" % (
            vesrion, file_name, folder_name))

        vesrion = vesrion.split('.')
        file_name = file_name.split('.')[:-1]
        folder_name = folder_name.split('.')

        if len(file_name) > len(folder_name):
            diff_file = list(set(file_name) - set(vesrion))
            rating = (1 - (len(diff_file) / float(len(file_name)))) * 5
        else:
            diff_folder = list(set(folder_name) - set(vesrion))
            rating = (1 - (len(diff_folder) / float(len(folder_name)))) * 5

        log("\n rating: %f (by %s)" % (round(rating, 1), "file" if len(file_name) > len(folder_name) else "folder"))

        return round(rating, 1)

    def _search_movie(self, item):
        query = {
            "page": 1,
            "lang": 0,
            "search": item["title"],
            "typ": 1
        }
        search_results = self.urlHandler.request(self.BASE_URL + "/szukaj", query)
        pass


class URLHandler:
    def __init__(self):
        self.cookie_filename = os.path.join(__profile__, "cookiejar.txt")
        self.cookie_jar = cookielib.LWPCookieJar(self.cookie_filename)
        if os.access(self.cookie_filename, os.F_OK):
            self.cookie_jar.load()

        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))
        self.opener.addheaders = [('Accept-Encoding', 'gzip'),
                                  ('Accept-Language', 'en-us,en;q=0.5'),
                                  ('Pragma', 'no-cache'),
                                  ('Cache-Control', 'no-cache'),
                                  ('User-Agent',
                                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]

    def request(self, url, query_string=None, data=None, ajax=False, referer=None, cookie=None, decode_zlib=True):
        if data is not None:
            data = urllib.urlencode(data)
        if query_string is not None:
            query_string = urllib.urlencode(query_string)
            url += "?" + query_string
        if ajax:
            self.opener.addheaders += [('X-Requested-With', 'XMLHttpRequest')]
        if referer is not None:
            self.opener.addheaders += [('Referer', referer)]
        if cookie is not None:
            self.opener.addheaders += [('Cookie', cookie)]

        content = None
        log("Getting url: %s" % (url))
        try:
            response = self.opener.open(url, data)

            if response.code == 200:
                content = response.read()

                if decode_zlib and response.headers.get('content-encoding', '') == 'gzip':
                    try:
                        content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
                    except zlib.error:
                        pass

                if response.headers.get('content-type', '') == 'application/json':
                    content = json.loads(content, encoding="utf-8")

            response.close()
        except Exception as e:
            log("Failed to get url: %s\n%s" % (url, e.message))
            # Second parameter is the filename
        return content

    def save_cookie(self):
        self.cookie_jar.save()
