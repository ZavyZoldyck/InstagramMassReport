from sys import exit
from os import _exit
import subprocess


from os import path
import urllib
import requests

from proxybroker import Broker
from colorama import Fore, init
import time
import os
from libs.proxy_harvester import find_proxies

from multiprocessing import Process
from colorama import Fore, Back, Style

init(convert=True)

async def show(proxies, proxy_list):
    while (len(proxy_list) < 50):
        proxy = await proxies.get()
        if proxy is None: break

        print_success("[" + str(len(proxy_list) + 1) + "/50]", "Proxy bulundu:", proxy.as_json()["host"] + ":" + str(proxy.as_json()["port"]))
        
        proxy_list.append(
            proxy.as_json()["host"] + ":" + str(proxy.as_json()["port"])
        )

        pass
    pass


def find_proxies():
    proxy_list = []
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(
            types=['HTTPS'], limit=50), show(proxies, proxy_list)
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)
    
    if (len(proxy_list) % 5 != 0 and len(proxy_list) > 5):
        proxy_list = proxy_list[:len(proxy_list) - (len(proxy_list) % 5)]

    return proxy_list


page_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
}

report_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Host": "help.instagram.com",
    "Origin": "help.instagram.com",
    "Pragma": "no-cache",
    "Referer": "https://help.instagram.com/contact/497253480400030",
    "TE": "Trailers",
}

def random_str(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def report_profile_attack(username, proxy):
    ses = Session()

    if (proxy != None):
        ses.proxies = {
            "https": "https://" + proxy,
            "http": "https://" + proxy
        }
    
    user_agent = get_user_agent()

    page_headers["User-Agent"] = user_agent
    report_headers["User-Agent"] = user_agent

    try:
        res = ses.get("https://www.facebook.com/", timeout=10)
    except:
        print_error("Request Error (FacebookRequestsError)")
        return

    if (res.status_code != 200):
        print_error("Request Error (STATUS CODE:", res.status_code, ")")
        return

    if ('["_js_datr","' not in res.text):
        print_error("Request Error (CookieErrorJSDatr)")
        return
    
    try:
        js_datr = res.text.split('["_js_datr","')[1].split('",')[0]
    except:
        print_error("Request Error (CookieParsingError)")
        return

    page_cookies = {
        "_js_datr": js_datr
    }

    try:
        res = ses.get("https://help.instagram.com/contact/497253480400030", cookies=page_cookies, headers=page_headers, timeout=10)
    except:
        print_error("Request Error (InstagramRequestsError)")
        return

    if (res.status_code != 200):
        print_error("Request Error (STATUS CODE:", res.status_code, ")")
        return
    
    if ("datr" not in res.cookies.get_dict()):
        print_error("Request Error (CookieErrorDatr)")
        return
    
    if ('["LSD",[],{"token":"' not in res.text):
        print_error("Request Error (CookieErrorLSD)")
        return

    if ('"__spin_r":' not in res.text):
        print_error("Request Error (CookieErrorSpinR)")
        return

    if ('"__spin_b":' not in res.text):
        print_error("Request Error (CookieErrorSpinB)")
        return

    if ('"__spin_t":' not in res.text):
        print_error("Request Error (CookieErrorSpinT)")
        return

    if ('"server_revision":' not in res.text):
        print_error("Request Error (CookieErrorRev)")
        return

    if ('"hsi":' not in res.text):
        print_error("Request Error (CookieErrorHsi)")
        return

    try:
        lsd = res.text.split('["LSD",[],{"token":"')[1].split('"},')[0]
        spin_r = res.text.split('"__spin_r":')[1].split(',')[0]
        spin_b = res.text.split('"__spin_b":')[1].split(',')[0].replace('"',"")
        spin_t = res.text.split('"__spin_t":')[1].split(',')[0]
        hsi = res.text.split('"hsi":')[1].split(',')[0].replace('"',"")
        rev = res.text.split('"server_revision":')[1].split(',')[0].replace('"',"")
        datr = res.cookies.get_dict()["datr"]
    except:
        print_error("Request Error (CookieParsingError)")
        return

    report_cookies = {
        "datr": datr
    }

    report_form = {
        "jazoest": "2723",
        "lsd": lsd,
        "instagram_username": username,
        "Field241164302734019_iso2_country_code": "TR",
        "Field241164302734019": "Türkiye",
        "support_form_id": "497253480400030",
        "support_form_hidden_fields": "{}",
        "support_form_fact_false_fields": "[]",
        "__user": "0",
        "__a": "1",
        "__dyn": "7xe6Fo4SQ1PyUhxOnFwn84a2i5U4e1Fx-ey8kxx0LxW0DUeUhw5cx60Vo1upE4W0OE2WxO0SobEa81Vrzo5-0jx0Fwww6DwtU6e",
        "__csr": "",
        "__req": "d",
        "__beoa": "0",
        "__pc": "PHASED:DEFAULT",
        "dpr": "1",
        "__rev": rev,
        "__s": "5gbxno:2obi73:56i3vc",
        "__hsi": hsi,
        "__comet_req": "0",
        "__spin_r": spin_r,
        "__spin_b": spin_b,
        "__spin_t": spin_t
    }

    try:
        res = ses.post(
            "https://help.instagram.com/ajax/help/contact/submit/page",
            data=report_form,
            headers=report_headers,
            cookies=report_cookies,
            timeout=10
        )
    except:
        print_error("Request Error (FormRequestsError)")
        return
    
    if (res.status_code != 200):
        print_error("Request Error (STATUS CODE:", res.status_code, ")")
        return
    
    print_success("Successfully reported!")

def report_video_attack(video_url, proxy):
    ses = Session()
    if (proxy != None):
        ses.proxies = {
            "https": "https://" + proxy,
            "http": "https://" + proxy
        }
    
    user_agent = get_user_agent()

    page_headers["User-Agent"] = user_agent
    report_headers["User-Agent"] = user_agent

    try:
        res = ses.get("https://www.facebook.com/", timeout=10)
    except Exception as e:
        print_error("Request Error (FacebookRequestsError)", e)
        return

    if (res.status_code != 200):
        print_error("Request Error (STATUS CODE:", res.status_code, ")")
        return

    if ('["_js_datr","' not in res.text):
        print_error("Request Error (CookieErrorJSDatr)")
        return
    
    try:
        js_datr = res.text.split('["_js_datr","')[1].split('",')[0]
    except:
        print_error("Request Error (CookieParsingError)")
        return

    page_cookies = {
        "_js_datr": js_datr
    }

    try:
        res = ses.get("https://help.instagram.com/contact/497253480400030", cookies=page_cookies, headers=page_headers, timeout=10)
    except:
        print_error("Request Error (InstagramRequestsError)")
        return

    if (res.status_code != 200):
        print_error("Request Error (STATUS CODE:", res.status_code, ")")
        return
    
    if ("datr" not in res.cookies.get_dict()):
        print_error("Request Error (CookieErrorDatr)")
        return
    
    if ('["LSD",[],{"token":"' not in res.text):
        print_error("Request Error (CookieErrorLSD)")
        return

    if ('"__spin_r":' not in res.text):
        print_error("Request Error (CookieErrorSpinR)")
        return

    if ('"__spin_b":' not in res.text):
        print_error("Request Error (CookieErrorSpinB)")
        return

    if ('"__spin_t":' not in res.text):
        print_error("Request Error (CookieErrorSpinT)")
        return

    if ('"server_revision":' not in res.text):
        print_error("Request Error (CookieErrorRev)")
        return

    if ('"hsi":' not in res.text):
        print_error("Request Error (CookieErrorHsi)")
        return

    try:
        lsd = res.text.split('["LSD",[],{"token":"')[1].split('"},')[0]
        spin_r = res.text.split('"__spin_r":')[1].split(',')[0]
        spin_b = res.text.split('"__spin_b":')[1].split(',')[0].replace('"',"")
        spin_t = res.text.split('"__spin_t":')[1].split(',')[0]
        hsi = res.text.split('"hsi":')[1].split(',')[0].replace('"',"")
        rev = res.text.split('"server_revision":')[1].split(',')[0].replace('"',"")
        datr = res.cookies.get_dict()["datr"]
    except:
        print_error("Request Error (CookieParsingError)")
        return

    report_cookies = {
        "datr": datr
    }

    report_form = {
        "jazoest": "2723",
        "lsd": lsd,
        "sneakyhidden": "",
        "Field419623844841592": video_url,
        "Field1476905342523314_iso2_country_code": "TR",
        "Field1476905342523314": "Türkiye",
        "support_form_id": "440963189380968",
        "support_form_hidden_fields": '{"423417021136459":false,"419623844841592":false,"754839691215928":false,"1476905342523314":false,"284770995012493":true,"237926093076239":false}',
        "support_form_fact_false_fields": "[]",
        "__user": "0",
        "__a": "1",
        "__dyn": "7xe6Fo4SQ1PyUhxOnFwn84a2i5U4e1Fx-ey8kxx0LxW0DUeUhw5cx60Vo1upE4W0OE2WxO0SobEa81Vrzo5-0jx0Fwww6DwtU6e",
        "__csr": "",
        "__req": "d",
        "__beoa": "0",
        "__pc": "PHASED:DEFAULT",
        "dpr": "1",
        "__rev": rev,
        "__s": "5gbxno:2obi73:56i3vc",
        "__hsi": hsi,
        "__comet_req": "0",
        "__spin_r": spin_r,
        "__spin_b": spin_b,
        "__spin_t": spin_t
    }

    try:
        res = ses.post(
            "https://help.instagram.com/ajax/help/contact/submit/page",
            data=report_form,
            headers=report_headers,
            cookies=report_cookies,
            timeout=10
        )
    except:
        print_error("Request Error (FormRequestsError)")
        return
    
    if (res.status_code != 200):
        print_error("Request Error (STATUS CODE:", res.status_code, ")")
        return
    
    print_success("Successfully reported!")


def print_success(message, *argv):
    print(Fore.GREEN + "[ IMR | SUCCESS ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")

def print_error(message, *argv):
    print(Fore.RED + "[ IMR | FAILED ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")

def print_status(message, *argv):
    print(Fore.BLUE + "[ * ] " + Style.RESET_ALL + Style.BRIGHT, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")

def ask_question(message, *argv):
    message = Fore.BLUE + "[ ? ] " + Style.RESET_ALL + Style.BRIGHT + message
    for arg in argv:
        message = message + " " + arg
    print(message, end="")
    ret = input(": ")
    return ret

def parse_proxy_file(fpath):
    if (path.exists(fpath) == False):
        print("")
        print_error("Proxy file not found! (I wonder if you're taking the wrong path?)")
        print_error("Exiting From Program")
        exit(0)
    
    proxies = []
    with open(fpath, "r") as proxy_file:
        for line in proxy_file.readlines():
            line = line.replace(" ", "")
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            
            if (line ==  ""):
                continue
            
            proxies.append(line)
    
    if (len(proxies) > 50):
        proxies = random.choices(proxies, 50)
        
    print("")
    print_success(str(len(proxies)) + " Proxies have been installed!")

    return proxies

logo = f"""
    

{Fore.LIGHTCYAN_EX} ██╗███╗   ███╗██████╗    
{Fore.LIGHTWHITE_EX}██║████╗ ████║██╔══██╗    
{Fore.LIGHTRED_EX}  ██║██╔████╔██║██████╔╝    
{Fore.LIGHTCYAN_EX} ██║██║╚██╔╝██║██╔══██╗   
{Fore.LIGHTWHITE_EX}██║██║ ╚═╝ ██║██║  ██║      
{Fore.LIGHTRED_EX}  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝        
                                                                                           
                                                     
                                                                                                              
                                                                                                                                                                         


      """



def print_logo():
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + logo + Style.RESET_ALL + Style.BRIGHT +"\n")
    print(Fore.LIGHTYELLOW_EX + "                                   Developer: Martizio"+ Style.RESET_ALL + Style.BRIGHT)
    print(Style.RESET_ALL + Style.BRIGHT, Style.BRIGHT)


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def profile_attack_process(username, proxy_list):
    if (len(proxy_list) == 0):
        for _ in range(10):
            report_profile_attack(username, None)
        return

    for proxy in proxy_list:
        report_profile_attack(username, proxy)

def video_attack_process(video_url, proxy_list):
    if (len(proxy_list) == 0):
        for _ in range(10):
            report_video_attack(video_url, None)
        return

    for proxy in proxy_list:
        report_video_attack(video_url, proxy)

def video_attack(proxies):
    video_url = ask_question("Enter the link of the video you want to report")
    print(Style.RESET_ALL)
    if (len(proxies) == 0):
        for k in range(5):
            p = Process(target=video_attack_process, args=(video_url, [],))
            p.start()
            print_status(str(k + 1) + ". Transaction Opened!")
            if (k == 5): print()
        return

    chunk = list(chunks(proxies, 10))

    print("")
    print_status("Video complaint attack is on!\n")

    i = 1
    for proxy_list in chunk:
        p = Process(target=video_attack_process, args=(video_url, proxy_list,))
        p.start()
        print_status(str(i) + ". Transaction Opened!")
        if (k == 5): print()
        i = i + 1

def GetUUID():
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n") + 2
    uuid = uuid[pos1:-15]
    return uuid.encode("utf-8")


def hwid():
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n") + 2
    uuid = uuid[pos1:-15]
    return uuid


def profile_attack(proxies):
    username = ask_question("Enter the username of the person you want to report")
    print(Style.RESET_ALL)
    if (len(proxies) == 0):
        for k in range(5):
            p = Process(target=profile_attack_process, args=(username, [],))
            p.start()
            print_status(str(k + 1) + ". Transaction Opened!")
        return

    chunk = list(chunks(proxies, 10))

    print("")
    print_status("Profile complaint attack is starting!\n")

    i = 1
    for proxy_list in chunk:
        p = Process(target=profile_attack_process, args=(username, proxy_list,))
        p.start()
        print_status(str(i) + ". Transaction Opened!")
        if (k == 5): print()
        i = i + 1



def main():
    os.system('title Instagram Mass Report ^| Developed by Martizio ^| V1')
    print(Fore.MAGENTA + '[ TRY ] ' + Fore.WHITE + 'Load API...')
    print(" ")
    time.sleep(2)
    print(Fore.LIGHTGREEN_EX + '[ SUCCESS ] ' + Fore.WHITE + 'Requests API Loaded !')
    time.sleep(0.9)
    print(Fore.LIGHTGREEN_EX + '[ SUCCESS ] ' + Fore.WHITE + 'Facebook API Loaded !')
    print(" ")
    print(" ")
    print(" ")

    proxies = []

    print(Fore.MAGENTA + '[ TRY ] ' + Fore.WHITE + 'Scrape Proxys from API')
    print(" ")
    print(" ")

    rfinder = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=https&timeout=7000&country=ALL&anonymity=elite&ssl=no')
    LISTPROXY = rfinder.text
    proxies = str(LISTPROXY)
    

    print_success(str(len(proxies)) + " Number of proxy found!\n")


    

    print("")
    print(Fore.LIGHTMAGENTA_EX + "[ CHOOSE ] " + Fore.WHITE + "1 - Report Profile")
    print(Fore.LIGHTMAGENTA_EX + "[ CHOOSE ] " + Fore.WHITE + "1 - Report a video")
    print(" ")

    report_choice = input(Fore.WHITE + "Choose option : ")
    print("")

    if (report_choice.isdigit() == False):
        print_error("The answer is not understood.")
        exit(0)
    
    if (int(report_choice) > 2 or int(report_choice) == 0):
        print_error("The answer is not understood.")
        exit(0)

    if (int(report_choice) == 1):
        profile_attack(proxies)
    elif (int(report_choice) == 2):
        video_attack(proxies)

if __name__ == "__main__":
    print_logo()
    try:
        main()
        print(Style.RESET_ALL)
    except KeyboardInterrupt:
        print("\n\n" + Fore.RED + "[*] Program is closing!")
        print(Style.RESET_ALL)
        _exit(0)
