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

##################GLOBALS
myserver = addon.getSetting('NLSSServer');
user = addon.getSetting('User');
pword = addon.getSetting('Password');
cust = addon.getSetting('Customer');
myitem = addon.getSetting('Item');
Surfline = addon.getSetting('Surfline');
Transcode= addon.getSetting('Transcode');


###################SURFLINE
if Surfline == 'true':
    #xbmcgui.Dialog().ok(addonname, myitem)
    newSTream="rtmp://livestream.cdn-surfline.com/cdn-live-s3"
    #neFile="/surfline/secure/live/wc-pontohdcam?e=0&h=a984acb31092dcb45648e5514c47941d"
    #chose=myitem
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
    #neFile=breaks[chose][0]
    #mybreak=breaks[chose][1]
    #xbmcgui.Dialog().ok(addonname, mybreak,newSTream,neFile)
    #item = xbmcgui.ListItem("Test")
    #item.setProperty("PlayPath", neFile)
    #xbmc.Player().play(newSTream, item)

    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    for index in range(len(breaks)):
        #print 'Current camera :', cameras[index]
        liz=xbmcgui.ListItem(breaks[index][1])
        #liz.setInfo( type = "Video", infoLabels=video)
        aurl=breaks[index][0]
        liz.setProperty("PlayPath", aurl)
        pl.add(newSTream,liz)
    xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(pl)
    myvar=1
    while myvar==1:
        xbmc.sleep(10000)
        xbmc.Player().playnext()


###################TESTING
#myitem=1
#myserver = "https://nlss-demo.nextls.net";
#user = "rand@nlss.com";
#pword = "nlss123";
#cust = "nlss-demo";
###################TESTING
def show_dialog(header,text):
     xbmcgui.Dialog().notification(header, text, time=4000)
def show_busy_dialog():
    xbmc.executebuiltin('ActivateWindow(busydialog)')
def hide_busy_dialog():
    xbmc.executebuiltin('Dialog.Close(busydialog)')
#while xbmc.getCondVisibility('Window.IsActive(busydialog)'):
#time.sleep(100)

#################RMS AUTH###################################################
show_busy_dialog()
show_dialog("NLSS", "authenticate")
opener = urllib2.build_opener()
thedata = '<Person xmlns="http://www.nlss.com/Gateway"><location>' + cust + '</location><userID>' + user + '</userID><password>' + pword + '</password></Person>'
url = myserver + "/api/flashCURL.php"
amethod="POST"
aapi="nlssgateway"
aservice="DeviceCommands"
auuid="authenticate"
formdata2 = {"method": amethod, "api": aapi, "version": "v1", "service": aservice,
    "uuid": auuid, "requestXML": thedata}
data_encoded2 = urllib.urlencode(formdata2)
req = urllib2.Request(url, data_encoded2)
response = opener.open(req)
mydata = response.geturl()
mydata2 = response.info()
the_page = response.read()
#print mydata2
#print the_page
sessionID = mydata2.getheader('Set-Cookie')
#print sessionID
newCookie = sessionID.replace("PHPSESSID=", "")
sessionID = newCookie.replace("; path=/", "")
returndata = ElementTree.fromstring(the_page)
for info in returndata:
    aPerson = info.tag.replace("{http://www.nlss.com/Gateway}", "")
    #print aPerson, '-->', info.text
    if aPerson == 'customerID':
        customerID = info.text
#print customerID
#print sessionID
#xbmcgui.Dialog().ok(addonname, customerID,sessionID)


################DNLOOKUP####################################################
show_dialog("NLSS", "DeviceNetworkLookup")
formdata = { "sessionid" : sessionID, "method": "GET", "api" : customerID ,"version" : "v1","service" : "DeviceNetworkLookup"}
data_encoded = urllib.urlencode(formdata)
#url_camera =myserver+"/api/nlssgateway/v1/DeviceCommands/deviceNetworkLookup"
url_camera =myserver+"/api/flashCURL.php"
#print url_camera
req_camera = urllib2.Request(url_camera,data_encoded)
req_camera.add_header('Cookie', 'PHPSESSID='+sessionID)
response_camera = opener.open(req_camera)
#response_camera = urllib.urlopen(req_camera)
mydata_camera= response_camera.geturl()
mydata2_camera= response_camera.info()
the_page_camera = response_camera.read()
#print the_page_camera

##########################DRAW LIST OF SITES
show_dialog("NLSS", "Sites")
isit=0;
count=0;
stream=myserver.replace("https://","")
stream2=stream.replace("http://","")
tree2 = ElementTree.fromstring(the_page_camera)
######
theDesc=""
theWebPort=""
theRTMPPort=""
for dnl in tree2:
    aDNL=dnl.tag.replace("{http://www.nlss.com/Gateway}","")
    # print aDNL
    ############################
    myID = ""
    mySiteID = ""
    myDesc = ""
    myIcon = ""
    myPort=""
    myRTMP=""
    myStatus=""
    myModel=""
    myFirmware=""
    for char in dnl:
        aKey = char.tag.replace("{http://www.nlss.com/Gateway}", "")
        #print ' ', aKey, '-->', char.text
        if aKey == 'firmwareVersion':
            myFirmware = char.text
        if aKey == 'deviceModel':
            myModel = char.text
        if aKey == 'status':
            myStatus = char.text
        if aKey == 'deviceWebPort':
            myPort = char.text
            if count == isit:
                theWebPort = myPort
        if aKey == 'deviceRtmpPort':
            myRTMP = char.text
            if count == isit:
                theRTMPPort=myRTMP
        if aKey == 'siteID':
            mySiteID = char.text
        if aKey == 'gatewayID':
            myID=char.text
        if aKey == 'deviceName':
            myDesc=char.text
            if count==isit:
                theDesc=myDesc
    count=count+1
theWeb = myserver + ":"+theWebPort + ""
theWeb = "https://"+stream2 + "/"+theWebPort + ""
theStream = "rtmp://" + stream2 + ":" + theRTMPPort + "/live/"
##print theDesc
#print theWeb
#print theStream


#########################################LOGIN TO GW
show_dialog("NLSS", "Gateway")
#thedata2 = '<Person xmlns="http://www.nlss.com/Gateway"><location>' + cust + '</location><userID>' + user + '</userID><password>' + pword + '</password></Person>'
#opener2 = urllib2.build_opener()
url = theWeb + "/api/flashCURL.php"
#url =theWeb+"/api/nlssgateway/v1/DeviceCommands/authenticate"
#print url
amethod="POST"
aapi="nlssgateway"
aservice="DeviceCommands"
auuid="authenticate"
formdata2 = { "sessionid" : sessionID,"method": amethod, "api": aapi, "version": "v1", "service": aservice,
    "uuid": auuid, "requestXML": thedata}
data_encoded2 = urllib.urlencode(formdata2)
#print data_encoded2
reqw = urllib2.Request(url, data_encoded2)
reqw.add_header('Cookie', 'PHPSESSID='+sessionID)
responser = opener.open(reqw)
#response = urllib.urlopen(req)
gw_auth_auth = responser.geturl()
gw_auth_head = responser.info()
gw_auth = responser.read()
#print gw_auth_head
#print gw_auth




###############LOOP

############### WORKING
cameras=[]
cameras.append("6c9de80d-d837-4376-888d-28faeb667f29")
cameras.append("0e48e9d0-494f-4f67-8322-41dfbc26bf74")
cameras.append("6e755ff6-5d3c-28be-9dd7-f07be2f1b0a0")
cameras.append("7748bde2-78dc-453d-90be-40bc49615917")
cameras.append("b3e83265-479e-47f5-a140-38946910193a")
cameras.append("cb4b910b-bcd6-4e29-ad79-b62cc56f1ae3")
cameras.append("77efde67-42d0-ab63-4b66-32ab47d9621c")
cameras.append("2764ac51-4f49-425a-9d5d-d1865ce080dc")
cameras.append("67891e73-c3c3-24a5-6adf-81dddb1419f1")


pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
pl.clear()
for index in range(len(cameras)):
    #print 'Current camera :', cameras[index]
    liz=xbmcgui.ListItem(cameras[index])
    #liz.setInfo( type = "Video", infoLabels=video)
    aurl=cameras[index]+"_0_"+Transcode+".flv"
    liz.setProperty("PlayPath", aurl)
    pl.add(theStream,liz)

xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(pl)
myvar=1
#while myvar==1:
#xbmc.sleep(10000)
#  xbmc.Player().playnext()

#WINDOW = xbmcgui.Window(10000)
#WINDOW.setProperty("stream", theStream)

#run camera()
###############NOT WORKING
##8c262fde-913d-490b-8202-df411172f2e4
##4d98bd1c-72c1-6e79-b362-b5a65f16cfba
##2c713e34-189c-4c6c-84a3-017c18a8a4ab
##615f8636-24fe-e45a-eb27-f837f5469355
##ed586e83-0f4d-32af-9403-f458c5abd916
##74eeac1c-c2e1-8686-29bf-e595dbf33db7
##8214952f-4971-49ee-b6e4-df79eb2167d4
##4c556f38-cf1f-d3e8-b48c-3c26dc813164
##87b0f5e2-bbe8-485b-a00f-e9c3b2fce462

#myitem="8c262fde-913d-490b-8202-df411172f2e4"

##############################GET GW CAMERAS
#def run camera():
url_camera =theWeb + "/api/flashCURL.php"
#+"/api/nlssgateway/v1/camera"
#print url_camera
amethod="GET"
aapi="nlssgateway"
aservice="camera"
auuid=""

formdata2 = { "sessionid" : sessionID,"method": amethod, "api": aapi, "version": "v1", "service": aservice,
    "uuid": auuid, "requestXML": thedata, "argList":"deviceID/"+myitem}
data_encoded2 = urllib.urlencode(formdata2)
#print data_encoded2
reqw = urllib2.Request(url, data_encoded2)
reqw.add_header('Cookie', 'PHPSESSID='+sessionID)
response_camera = opener.open(reqw)
mydata_camera= response_camera.geturl()
mydata2_camera= response_camera.info()
the_page_camera = response_camera.read()
#print the_page_camera
#xbmcgui.Dialog().ok(addonname, the_page_camera)
count=0;
tree =ElementTree.fromstring(the_page_camera)
#theStream="rtmp://"+stream2+"/live/"
camPath=""
camDesc=""
camIP=""
#myFile += "_"+myTransWidth+"_"+iOS_BITRATE+"_"+iOS_FPS+"_"+iOS_CODEC;
#public static const iOS_WIDTH:Number = 320;
#public static const iOS_BITRATE:Number = 100;
#public static const iOS_FPS:Number = 10;
#public static const iOS_CODEC:Number = 2;
#myTranscode="640_100_10_2"
for camera in tree:
    # print camera.tag, camera.attrib
    #for char in camera:
    #count++
    aCam=camera.tag.replace("{http://www.nlss.com/Gateway}","")
    #xbmcgui.Dialog().ok(addonname, aCam)
    #print aCam
    myID = ""
    myDesc = ""
    myIcon = ""
    myPath=""
    for char in camera:
        aKey = char.tag.replace("{http://www.nlss.com/Gateway}", "")
        # if count == 2:
        #print ' ', aKey, '-->', char.text
        if aKey == 'deviceID':
            myID=char.text
            myIcon = theWeb+"/nlss/images/cameras/320x240/" + myID + ".jpg"
            myPath = myID+"_0_"+Transcode+".flv"
            #if count==myitem:
            camPath=myPath
        if aKey == 'deviceDescription':
            #if aKey == 'discoveredIPAddress':
            myDesc=char.text
            #if count==myitem:
            camDesc=myDesc
        if aKey == 'discoveredIPAddress':
            camIP=char.text

    count=count+1
hide_busy_dialog()
#xbmcgui.Dialog().ok(addonname, camDesc,theStream,camPath)
item = xbmcgui.ListItem(theDesc+" "+camDesc+ " " +camIP+" "+Transcode)
item.setProperty("PlayPath", camPath)
#item.setProperty("Title", camDesc)
#xbmc.Player().play(theStream+camPath)
#xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(theStream,item)
#time.sleep(1000)
#xbmc.Player().stop()