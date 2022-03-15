import urllib.request
import re
import struct
import sys
import ssl

try:
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2

# Disable Certificate Error from Urllib
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_song_title(url):
    encoding = 'latin1' # default: iso-8859-1 for mp3 and utf-8 for ogg streams
    request = urllib2.Request(url,headers={'Icy-MetaData': 1}) 
    try: #check if the url is valid 
        response = urllib2.urlopen(request,context=ctx)

    except Exception as err :
        return {"Error_Message":" Url not valid"}

    try: # check if the url support icecast/shoutcast metadata
        metaint = int(response.headers['icy-metaint'])
    except:
        return {"message":"Url resource does not Support Icy Metadata "}

    for _ in range(15): # # title may be empty initially, try several times
        response.read(metaint)  # skip to metadata
        metadata_length = struct.unpack('B', response.read(1))[0] * 16  # length byte
        metadata = response.read(metadata_length).rstrip(b'\0')
        # extract title from the metadata
        m = re.search(br"StreamTitle='([^']*)';", metadata)
        if m:
            title = m.group(1).decode(encoding)
            if title:
                if title.find('text='):
                    new_title=title.split('song_spot')[0].replace('text=','').replace('"', '')
                    return { "streamTitle" :new_title}
                else:
                    return { "streamTitle" :title}
     
    return {"message":"title not found"}
        