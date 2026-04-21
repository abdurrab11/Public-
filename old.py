#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║           A.R.S.T - Abd Ur Rab Security Toolkit                 ║
    ║              Network Analysis & System Reconnaissance             ║
    ╚══════════════════════════════════════════════════════════════════╝
    Author  : Abd Ur Rab
    Version : 2.0
    Platform: Termux / Linux / macOS
    Use     : Authorized Security Testing Only
"""

import socket
import requests
import os
import sys
import time
import platform
import subprocess
import json
import threading
from datetime import datetime
from urllib.parse import urlparse

# ANSI Color Codes for Termux
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class ARSToolkit:
    def __init__(self):
        self.author = "Abd Ur Rab"
        self.version = "2.0"
        self.running = True
        
    def clear(self):
        os.system('clear' if os.name != 'nt' else 'cls')
        
    def banner(self):
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
        ▄▄▄       ██▀███   ▄████▄   ██░ ██  █    ██   ██████ 
       ▒████▄    ▓██ ▒ ██▒▒██▀ ▀█  ▓██░ ██▒ ██  ▓██▒▒██    ▒ 
       ▒██  ▀█▄  ▓██ ░▄█ ▒▒▓█    ▄ ▒██▀▀██░▓██  ▒██░░ ▓██▄   
       ░██▄▄▄▄██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒░▓█ ░██ ▓▓█  ░██░  ▒   ██▒
        ▓█   ▓██▒░██▓ ▒██▒▒ ▓███▀ ░░▓█▒░██▓▒▒█████▓ ▒██████▒▒
        ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ░▒ ▒  ░ ▒ ░░▒░▒░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░
         ▒   ▒▒ ░  ░▒ ░ ▒░  ░  ▒    ▒ ░▒░ ░░░▒░ ░ ░ ░ ░▒  ░ ░
         ░   ▒     ░░   ░ ░         ░  ░░ ░ ░░░ ░ ░ ░  ░  ░  
             ░  ░   ░     ░ ░       ░  ░  ░   ░           ░  
                          ░                                  
{Colors.END}
{Colors.RED}{Colors.BOLD}              ╔═══════════════════════════════════════╗
              ║   ABD UR RAB SECURITY TOOLKIT v2.0    ║
              ║     Authorized Use Only ⚡            ║
              ╚═══════════════════════════════════════╝{Colors.END}
{Colors.YELLOW}  Author: {Colors.CYAN}{self.author}{Colors.YELLOW} | Platform: {Colors.CYAN}{platform.system()}{Colors.END}
        """
        print(banner)
        
    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            return response.json().get('ip', 'Unavailable')
        except:
            return f"{Colors.RED}No Internet{Colors.END}"
            
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return f"{Colors.RED}Unavailable{Colors.END}"
            
    def get_location_info(self, ip):
        try:
            response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=5)
            data = response.json()
            return {
                'city': data.get('city', 'N/A'),
                'region': data.get('region', 'N/A'),
                'country': data.get('country_name', 'N/A'),
                'org': data.get('org', 'N/A'),
                'timezone': data.get('timezone', 'N/A')
            }
        except:
            return None
            
    def system_info(self):
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}[+] SYSTEM INTELLIGENCE{Colors.END}")
        print(f"{Colors.CYAN}╔{'═'*50}╗{Colors.END}")
        info = {
            "Hostname": socket.gethostname(),
            "OS": f"{platform.system()} {platform.release()}",
            "Architecture": platform.machine(),
            "Processor": platform.processor() or "Unknown",
            "Python Ver": platform.python_version(),
            "Termux": "Yes" if 'TERMUX_VERSION' in os.environ else "No"
        }
        for key, value in info.items():
            print(f"{Colors.CYAN}║{Colors.END} {Colors.YELLOW}{key:<15}{Colors.END}: {Colors.GREEN}{value}{Colors.END}")
        print(f"{Colors.CYAN}╚{'═'*50}╝{Colors.END}")
        
    def network_info(self):
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}[+] NETWORK RECONNAISSANCE{Colors.END}")
        print(f"{Colors.CYAN}╔{'═'*50}╗{Colors.END}")
        
        local_ip = self.get_local_ip()
        public_ip = self.get_public_ip()
        
        print(f"{Colors.CYAN}║{Colors.END} {Colors.YELLOW}{'Local IP':<15}{Colors.END}: {Colors.GREEN}{local_ip}{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END} {Colors.YELLOW}{'Public IP':<15}{Colors.END}: {Colors.GREEN}{public_ip}{Colors.END}")
        
        if public_ip and 'No Internet' not in public_ip:
            loc = self.get_location_info(public_ip)
            if loc:
                print(f"{Colors.CYAN}║{Colors.END} {Colors.YELLOW}{'Location':<15}{Colors.END}: {Colors.GREEN}{loc['city']}, {loc['country']}{Colors.END}")
                print(f"{Colors.CYAN}║{Colors.END} {Colors.YELLOW}{'ISP/Org':<15}{Colors.END}: {Colors.GREEN}{loc['org']}{Colors.END}")
                print(f"{Colors.CYAN}║{Colors.END} {Colors.YELLOW}{'Timezone':<15}{Colors.END}: {Colors.GREEN}{loc['timezone']}{Colors.END}")
                
        print(f"{Colors.CYAN}╚{'═'*50}╝{Colors.END}")
        
    def live_clock(self):
        while self.running:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sys.stdout.write(f"\r{Colors.BOLD}{Colors.YELLOW}[⏱]  {Colors.CYAN}{now}{Colors.END} {Colors.YELLOW}|{Colors.END} {Colors.GREEN}Live{Colors.END}")
            sys.stdout.flush()
            time.sleep(1)
            
    def port_scanner(self, target, ports):
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}[+] PORT SCANNING {target}{Colors.END}")
        print(f"{Colors.CYAN}╔{'═'*50}╗{Colors.END}")
        print(f"{Colors.CYAN}║{Colors.END} {Colors.YELLOW}{'PORT':<10}{'STATE':<10}{'SERVICE':<20}{Colors.END}")
        print(f"{Colors.CYAN}╠{'═'*50}╣{Colors.END}")
        
        open_ports = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                print(f"{Colors.CYAN}║{Colors.END} {Colors.GREEN}{port:<10}{'OPEN':<10}{service:<20}{Colors.END}")
                open_ports.append(port)
            sock.close()
            
        if not open_ports:
            print(f"{Colors.CYAN}║{Colors.END} {Colors.RED}No open ports found in range{Colors.END}")
        print(f"{Colors.CYAN}╚{'═'*50}╝{Colors.END}")
        return open_ports
        
    def ping_host(self, host):
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}[+] PINGING {host}{Colors.END}")
        param = '-c' if platform.system().lower() != 'windows' else '-n'
        command = ['ping', param, '4', host]
        try:
            output = subprocess.check_output(command, universal_newlines=True)
            print(f"{Colors.GREEN}{output}{Colors.END}")
        except:
            print(f"{Colors.RED}[!] Host unreachable or ping blocked{Colors.END}")
            
    def dns_lookup(self, domain):
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}[+] DNS RESOLUTION {domain}{Colors.END}")
        try:
            ip = socket.gethostbyname(domain)
            print(f"{Colors.GREEN}[✓] {domain} resolves to {ip}{Colors.END}")
            
            # Reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                print(f"{Colors.GREEN}[✓] PTR Record: {hostname}{Colors.END}")
            except:
                pass
        except socket.gaierror:
            print(f"{Colors.RED}[!] Could not resolve {domain}{Colors.END}")
            
    def whois_lookup(self, domain):
        print(f"\n{Colors.MAGENTA}{Colors.BOLD}[+] WHOIS LOOKUP {domain}{Colors.END}")
        try:
            import whois
            w = whois.whois(domain)
            print(f"{Colors.CYAN}Registrar:{Colors.END} {w.registrar}")
            print(f"{Colors.CYAN}Creation:{Colors.END} {w.creation_date}")
            print(f"{Colors.CYAN}Expiration:{Colors.END} {w.expiration_date}")
            print(f"{Colors.CYAN}Name Servers:{Colors.END} {', '.join(w.name_servers) if isinstance(w.name_servers, list) else w.name_servers}")
        except ImportError:
            print(f"{Colors.YELLOW}[!] Install python-whois: pip install python-whois{Colors.END}")
            print(f"{Colors.CYAN}[*] Fallback: Opening browser whois...{Colors.END}")
            os.system(f"termux-open-url https://who.is/whois/{domain}" if 'TERMUX_VERSION' in os.environ else f"xdg-open https://who.is/whois/{domain}")
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.END}")
            
    def menu(self):
        print(f"""
{Colors.BOLD}{Colors.YELLOW}    ╔════════════════════════════════════════════════════╗
    ║              OPERATIONAL MODULES                    ║
    ╠════════════════════════════════════════════════════╣
    ║  {Colors.CYAN}[1]{Colors.YELLOW} System Intelligence      {Colors.CYAN}[5]{Colors.YELLOW} DNS Resolver         ║
    ║  {Colors.CYAN}[2]{Colors.YELLOW} Network Reconnaissance   {Colors.CYAN}[6]{Colors.YELLOW} WHOIS Lookup         ║
    ║  {Colors.CYAN}[3]{Colors.YELLOW} Port Scanner             {Colors.CYAN}[7]{Colors.YELLOW} Clear Screen         ║
    ║  {Colors.CYAN}[4]{Colors.YELLOW} Ping Host                {Colors.CYAN}[0]{Colors.YELLOW} Exit Arsenal         ║
    ╚════════════════════════════════════════════════════╝{Colors.END}
        """)
        
    def run(self):
        self.clear()
        self.banner()
        
        # Start live clock in background
        clock_thread = threading.Thread(target=self.live_clock, daemon=True)
        clock_thread.start()
        
        time.sleep(1)  # Let clock show
        
        while True:
            self.menu()
            choice = input(f"{Colors.BOLD}{Colors.CYAN}[AbdUrRab@ARS-Toolkit]~> {Colors.END}").strip()
            
            if choice == '1':
                self.system_info()
            elif choice == '2':
                self.network_info()
            elif choice == '3':
                target = input(f"{Colors.YELLOW}[?] Enter target IP/Host: {Colors.END}").strip()
                ports_input = input(f"{Colors.YELLOW}[?] Ports (e.g., 22,80,443 or 1-1000): {Colors.END}").strip()
                
                ports = []
                if '-' in ports_input:
                    start, end = map(int, ports_input.split('-'))
                    ports = range(start, end+1)
                else:
                    ports = [int(p.strip()) for p in ports_input.split(',') if p.strip().isdigit()]
                    
                if not ports:
                    ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]
                    
                self.port_scanner(target, ports)
            elif choice == '4':
                host = input(f"{Colors.YELLOW}[?] Enter host to ping: {Colors.END}").strip()
                self.ping_host(host)
            elif choice == '5':
                domain = input(f"{Colors.YELLOW}[?] Enter domain: {Colors.END}").strip()
                self.dns_lookup(domain)
            elif choice == '6':
                domain = input(f"{Colors.YELLOW}[?] Enter domain: {Colors.END}").strip()
                self.whois_lookup(domain)
            elif choice == '7':
                self.clear()
                self.banner()
            elif choice == '0':
                print(f"\n{Colors.GREEN}[✓] ARS Toolkit shutting down. Stay ethical, {self.author}.{Colors.END}")
                self.running = False
                break
            else:
                print(f"{Colors.RED}[!] Invalid option{Colors.END}")
                
            input(f"\n{Colors.YELLOW}[Press Enter to continue...]{Colors.END}")

if __name__ == "__main__":
    try:
        tool = ARSToolkit()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Interrupted by user{Colors.END}")
        sys.exit(0)
