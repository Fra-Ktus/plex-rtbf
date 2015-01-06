import re, string
RTBF_URL	  = 'http://www.rtbf.be/'
RTBF_PROGRAM_VIDEO_URL = 'http://www.rtbf.be/video/'
RTBF_VIDEO_PAGE_URL='http://www.rtbf.be/video/embed?id=%s'
RTBF_VIDEO_STREAMING_URL = 'http://streaming.sbsbelgium.be/%s.mp4'
RTBF_BACKGROUND_URL = 'http://www.rtbf.be/sites/default/files/takeover/%s/bg_%s.jpg'       


ICON = 'rtbf_logo.png'
ART = 'art-default.png'

####################################################################################################
def Start():

  Plugin.AddPrefixHandler('/video/rtbf', MainMenu, 'RTBF', ICON, ART)
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  ObjectContainer.title1 = 'RTBF'
  ObjectContainer.content = ContainerContent.GenericVideos
  ObjectContainer.art = R(ART)
  DirectoryObject.thumb = R(ICON)
  VideoClipObject.thumb = R(ICON)
  VideoClipObject.art = R(ART)
  HTTP.CacheTime = 1800

####################################################################################################
def MainMenu():

  oc = ObjectContainer(
    objects = [
      DirectoryObject(
        key     = Callback(GetItemList, url='', title2='Videos'),
        title   = L('Videos')
      )
    ]
  )                                 
  # append programs list directly
  oc = GetProgramList(url="video/", oc=oc)
  return oc

####################################################################################################

def GetProgramList(url, oc):
  Log ("RTBF GetProgramList :" + url)
  html = HTML.ElementFromURL(RTBF_URL + url)
  programs = html.xpath('.//li[contains(@class, "col-md-2")]')
  for program in programs:
    program_url = program.xpath(".//a")[0].get("href")
    if program_url.startswith (RTBF_PROGRAM_VIDEO_URL) == True:
      program_url = program_url.split(RTBF_PROGRAM_VIDEO_URL)[1]
    Log.Info(program_url)
    title = program.xpath(".//a")[0].text
    Log.Info(title)
    do = DirectoryObject(key = Callback(GetItemList, url=program_url, title2=title), title = title)
    oc.add(do)
  return oc 
	
def GetItemList(url, title2, page=''):
  Log ("RTBF GetItemList :" + url)
  Log.Exception('GetItemList')
  cookies = HTTP.CookiesForURL(RTBF_URL)
  unsortedVideos = {}
  oc = ObjectContainer(title2=title2, view_group='InfoList', http_cookies=cookies)
  Log.Exception('videos')
  program_url = RTBF_PROGRAM_VIDEO_URL + url
  Log ("RTBF url : " + program_url)
  html = HTML.ElementFromURL(program_url)
  videos = html.xpath('.//div[contains(@class, "thumblock")]')
  if len(videos) == 0:
  	videos = html.xpath('.//li[contains(@class, "thumblock")]')
  Log.Info(videos)
  for video in videos:
    Log.Info("video:")
    try:
      video_id=video.xpath(".//a")[0].get("href").split('id=')[1]
      Log ("video url: %s" %video.xpath(".//a")[0].get("href"))
      Log ("video id: %s" %video.xpath(".//a")[0].get("href").split('id=')[1])
      video_page_url = RTBF_VIDEO_PAGE_URL % video_id
      title = video.xpath(".//a")[0].get("title")
      img = video.xpath(".//img")[0].get("src")
      #sort = video_page_url.split('/')[-1] 
      #Log.Info(video_page_url)
      #try:
      #  int(sort)  
      #  unsortedVideos[sort] = VideoClipObject(url = video_page_url, title = title, thumb=img)
      #except:
      #  Log.Exception("not a nummeric key, video not added")
      oc.add(VideoClipObject(url = video_page_url, title = title, thumb=img))
    except:
      Log.Exception("error adding VideoClipObject")
      pass
      
  #keys = unsortedVideos.keys()
  #Log.Info(keys)
  #keys.sort(reverse=True,key=int)

  #for key in keys:
  #  oc.add(unsortedVideos[key])

  pager = html.xpath('.//li[@class="pager-next"]')
  Log.Info(pager)
  Log.Info(html.xpath('.//li[@class="pager-next"]//a'))
  if pager:
    page_url = html.xpath('.//li[@class="pager-next"]//a')[0].get('href').split('?')[-1]
    Log.Info(page_url)
    # add "next page"
    oc.add(DirectoryObject(key=Callback(GetItemList, url=url, page='?'+page_url, title2='Volgende...'), title   = L('Volgende...')))
  
  return oc
  
