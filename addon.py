import sys
import urlparse
import xbmcaddon
import xbmcplugin
import xbmcgui
import urllib
import urllib2
from xml.etree import ElementTree
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
base_url = sys.argv[0]




#addon_handle = int(sys.argv[1])
myserver = addon.getSetting('NLSSServer');
user = addon.getSetting('User');
pword = addon.getSetting('Password');
cust = addon.getSetting('Customer');



if myserver == 'surfline':
    newSTream="rtmp://livestream.cdn-surfline.com/cdn-live-s3"
    neFile="/surfline/secure/live/wc-pontohdcam?e=0&h=a984acb31092dcb45648e5514c47941d"
    chose=user
    breaks=[]
    breaks.append(["/surfline/secure/live/wc-delmarcam?e=0&h=c0db264dadf5f645aa57c8b181d2193d", "Del Mar"])
    breaks.append(["/surfline/secure/live/wc-cardiffcam?e=0&h=7bb47612d894e43259ce72979572940e","Cardiff Reef"])
    breaks.append(["/surfline/secure/live/wc-beaconscam?e=0&h=5c65c0b105a9ba8636ca37071c03204e", "Beacons"])
    breaks.append(["/surfline/secure/live/wc-grandviewcam?e=0&h=dbfcb78a983dab5bfb1764b302048ee1","Grandview"])
    breaks.append(["/surfline/secure/live/wc-pontohdcam?e=0&h=a984acb31092dcb45648e5514c47941d","Ponto"])
    breaks.append(["/surfline/secure/live/wc-tamarackcam?e=0&h=d8959b95c5b27ab9249b4a09ec294f63","Tamarack"])
    breaks.append(["/surfline/secure/live/wc-oceansidecacam?e=0&h=104586ca27a46edc0bf443950a326acb", "Oceanside Harbor"])
    breaks.append(["/surfline/secure/wc-oceansidepiernscam?e=0&h=981d3492043d2d6e878066cc9a0768f4", "Oceanside Pier North"])
    breaks.append(["/surfline/secure/live/wc-osidepiersscam?e=0&h=d0cd50a3a2f78fb7bba3f14c90b8ab28","Oceanside Pier South"])
    neFile=breaks[chose][0]
    mybreak=breaks[chose][1]
    xbmcgui.Dialog().ok(addonname, mybreak,newSTream,neFile)
    item = xbmcgui.ListItem("Test")
    item.setProperty("PlayPath", neFile)
    xbmc.Player().play(newSTream, item)

#addon.add_video_item({'url': newSTream},{'title': 'Del Mar'},{'PlayPath': '/surfline/secure/live/wc-delmarcam?e=0&h=c0db264dadf5f645aa57c8b181d2193d'})
#base_url = sys.argv[0]
#addon_handle = int(sys.argv[1])
#args = urlparse.parse_qs(sys.argv[2][1:])
#xbmcplugin.setContent(addon_handle, 'movies')

url =myserver+"/api/nlssgateway/v1/DeviceCommands/authenticate"
data = '<Person xmlns="http://www.nlss.com/Gateway"><location>'+cust+'</location><userID>'+user+'</userID><password>'+pword+'</password></Person>'

opener = urllib2.build_opener()
req = urllib2.Request(url, data)
response = opener.open(req)
mydata= response.geturl()
mydata2= response.info()
the_page = response.read()
#xbmcgui.Dialog().ok(addonname, the_page)


myCookie=mydata2.getheader('Set-Cookie')
#print myCookie
newCookie=myCookie.replace("PHPSESSID=","")
myCookie=newCookie.replace("; path=/","")
#print myCookie

#headers={'Cookie':"PHPSESSID="+myCookie}
url_camera =myserver+"/api/nlssgateway/v1/camera"
req_camera = urllib2.Request(url_camera)
req_camera.add_header('Cookie', 'PHPSESSID='+myCookie)
#print req_camera.headers
response_camera = opener.open(req_camera)
mydata_camera= response_camera.geturl()
mydata2_camera= response_camera.info()
the_page_camera = response_camera.read()
count=0;
stream=myserver.replace("https://","")
stream2=stream.replace("http://","")

#xbmcgui.Dialog().ok(addonname, the_page_camera)
#self.getControl( 48 ).reset()
tree = ElementTree.fromstring(the_page_camera)
theStream="rtmp://"+stream2+"/live/"
thePath=""
theDesc=""
for camera in tree:
    # print camera.tag, camera.attrib
    #for char in camera:
            #count++
    aCam=camera.tag.replace("{http://www.nlss.com/Gateway}","")
    #print aCam
    myID = ""
    myDesc = ""
    myIcon = ""
    myPath=""
    for char in camera:
        aKey = char.tag.replace("{http://www.nlss.com/Gateway}", "")
        #print ' ', aKey, '-->', char.text
        if aKey == 'deviceID':
            myID=char.text
            myIcon = myserver+"/nlss/images/cameras/320x240/" + myID + ".jpg"
            myPath = myID+"_0_0_0_0_0.flv"
            if count==2:
                thePath=myPath
        if aKey == 'deviceDescription':
            myDesc=char.text
            if count==2:
                theDesc=myDesc

    count=count+1
#li = xbmcgui.ListItem(label=myDesc)
#li.setIconImage(myIcon)
#li.setArt({'thumb': myIcon, 'poster': myIcon, 'fanart': myIcon})
#li.seProperty( "deviceID", myID )
#itemurl = '%s?service=%s&url=%s' % ( base_url , 'camera' , myID )
#xbmcplugin.addDirectoryItem( handle = addonname, url = itemurl , listitem=li)
xbmcgui.Dialog().ok(addonname, theDesc,theStream,thePath)
#xbmc.Player().play(item=theStream playPath=thePath)
#item = xbmcgui.ListItem("Test")
#item.setProperty("PlayPath", thePath)

############xbmc.Player().play(theStream+thePath)

#self.getControl( 48 ).addItem( li )
#print myID,myDesc,myIcon
# print ' |',char.tag,'-->', char.text
#xbmcplugin.endOfDirectory(addon_handle)
#print mydata_camera
#print mydata2_camera
#print the_page_camera
