import re, string
RTBF_URL	  = 'http://www.rtbf.be/'
RTBF_PROGRAM_VIDEO_URL = 'http://www.rtbf.be/video/'
RTBF_VIDEO_PAGE_URL='http://www.rtbf.be/video/embed?id=%s'

RTBF_INFO = 'http://www.rtbf.be/auvio/categorie/info?id=1'
RTBF_METEO = 'http://www.rtbf.be/auvio/recherche?q=meteo'
RTBF_CULTURE = 'http://www.rtbf.be/auvio/categorie/culture?id=18'
RTBF_MUSIQUE = 'http://www.rtbf.be/auvio/categorie/musique?id=23'
RTBF_DOCUMENTAIRES = 'http://www.rtbf.be/auvio/categorie/documentaires?id=31'
RTBF_ENFANTS = 'http://www.rtbf.be/auvio/categorie/enfants?id=32'
RTBF_SERIES = 'http://www.rtbf.be/auvio/categorie/series?id=35'
RTBF_FILMS = 'http://www.rtbf.be/auvio/categorie/films?id=36'
RTBF_HUMOUR = 'http://www.rtbf.be/auvio/categorie/humour?id=40'
RTBF_DIVERTISSEMENT = 'http://www.rtbf.be/auvio/categorie/divertissement?id=29'
RTBF_VIE_QUOTIDIENNE = 'http://www.rtbf.be/auvio/categorie/vie-quotidienne?id=44'
RTBF_SPORT = 'http://www.rtbf.be/auvio/categorie/sport?id=9'
RTBF_FOOTBALL = 'http://www.rtbf.be/auvio/categorie/sport/football?id=11'

ICON = 'rtbf_logo.png'
ART = 'art-default.png'

####################################################################################################
def Start():

  ObjectContainer.title1 = 'RTBF'
  ObjectContainer.content = ContainerContent.GenericVideos
  ObjectContainer.art = R(ART)
  DirectoryObject.thumb = R(ICON)
  VideoClipObject.thumb = R(ICON)
  VideoClipObject.art = R(ART)
  HTTP.CacheTime = 1800

####################################################################################################
@handler('/video/rtbf', 'RTBF', art=ART, thumb=ICON)
def MainMenu():

  oc = ObjectContainer(
    objects = [
      DirectoryObject( key = Callback(GetItemList, url=RTBF_INFO, title2='Info'), title = L('Info')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_METEO, title2='Meteo'), title = L('Meteo')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_CULTURE, title2='Culture'), title = L('Culture')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_MUSIQUE, title2='Musique'), title = L('Musique')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_DOCUMENTAIRES, title2='Documentaires'), title = L('Documentaires')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_ENFANTS, title2='Enfants'), title = L('Enfants')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_SERIES, title2='Series'), title = L('Series')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_FILMS, title2='Films'), title = L('Films')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_HUMOUR, title2='Humour'), title = L('Humour')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_DIVERTISSEMENT, title2='Divertissement'), title = L('Divertissement')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_VIE_QUOTIDIENNE, title2='Vie Quotidienne'), title = L('Vie Quotidienne')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_SPORT, title2='Sport'), title = L('Sport')),
      DirectoryObject( key = Callback(GetItemList, url=RTBF_FOOTBALL, title2='Football'), title = L('Football'))
    ]
  )                                 
  return oc

####################################################################################################

def GetProgramList(url, title, oc):
  Log ("RTBF GetProgramList :" + url)
  program_url = url
  do = DirectoryObject(key = Callback(GetItemList, url=program_url, title2=title), title = title)
  oc.add(do)
  return oc

def GetItemList(url, title2, page=''):
  Log ("RTBF GetItemList :" + url)
  Log.Exception('GetItemList')
  cookies = HTTP.CookiesForURL(RTBF_URL)
  oc = ObjectContainer(title2=title2, http_cookies=cookies)
  Log.Exception('videos')
  program_url = url
  Log ("RTBF url : " + program_url)
  html = HTML.ElementFromURL(program_url)
  videos = html.xpath('.//article')
  Log.Info(videos)
  for video in videos:
    Log.Info("video:")
    try:
      refs = video.xpath(".//a")
      for ref in refs:
        href = ref.get("href")
        if (len(href) > 10):
          video_page_url = href
          title = ref.get("title")
          if title != None:
            # find image in the img tag...
            img_tag = video.xpath(".//img")
            img_srcset = img_tag[0].get("data-srcset")
            imgs = img_srcset.split(",")
            img = imgs[0].split(" ")[0]
            #img = "http://ds1.ds.static.rtbf.be/media/program/image/ng_55a38eb6ea4db2f2d33a-324x183.png"
            video_page_url = video_page_url.replace ("https","http")
            Log ("video url: " + video_page_url)
            Log ("url title: " + title)
            Log ("url img: " + img)
            oc.add(VideoClipObject(url = video_page_url, title = title, thumb=img))
            break
    except:
      Log.Exception("error adding VideoClipObject")
      pass
  return oc


