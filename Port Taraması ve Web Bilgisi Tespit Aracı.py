import socket
import threading
import time
import os
import dns.resolver
import requests
import subprocess
import platform
from termcolor import colored
from tabulate import tabulate
from tqdm import tqdm
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import whois
import re


def scan_ports(ip, port_range=(1, 500)):
    open_ports = []
    print(f"\nTarama başlatılıyor: {ip} üzerinde {port_range[0]}-{port_range[1]} portları")

    with tqdm(total=port_range[1] - port_range[0] + 1, desc="Port Tarama", ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed} < {remaining}, {rate_fmt}]") as pbar:
        def scan_single_port(port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
            pbar.update(1)

        with ThreadPoolExecutor(max_workers=50) as executor:
            for port in range(port_range[0], port_range[1] + 1):
                executor.submit(scan_single_port, port)

    return open_ports


def get_dns_info(domain):
    print(colored(f"DNS kayıtları için sorgulama yapılıyor: {domain}", 'cyan'))
    try:
        result = dns.resolver.resolve(domain, 'A')
        return [str(ip) for ip in result]
    except Exception as e:
        return [f"Hata: {str(e)}"]


def check_cloudflare(ip):
    print(colored(f"{ip} için Cloudflare kontrolü yapılıyor...", 'yellow'))
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(f'http://{ip}', headers=headers, timeout=3)
        if 'cf-ray' in response.headers:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        return False


def check_hosting(ip):
    print(colored(f"{ip} için hosting sağlayıcısı sorgulama yapılıyor...", 'magenta'))
    try:
        w = whois.whois(ip)
        hosting_provider = w.get('org', 'Bilinmeyen Hosting')
        return hosting_provider
    except Exception as e:
        return "Hosting Bilgisi Alınamadı"

def telnet_test(ip, port=25):
    print(colored(f"Telnet testi yapılıyor: {ip} port {port}", 'green'))
    try:
        telnet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        telnet.settimeout(3)
        telnet.connect((ip, port))
        return True
    except socket.error as e:
        return False

def get_target_ip(domain):
    print(colored(f"{domain} için gerçek IP adresi sorgulama yapılıyor...", 'blue'))
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None
    

def get_real_ip_info(domain):
    print(colored(f"{domain} için gerçek IP ve Cloud IP kontrol ediliyor...", 'blue'))
    real_ip = get_target_ip(domain)
    if not real_ip:
        return "Hedef IP alınamadı"

    cloudflare_status = check_cloudflare(real_ip)
    return real_ip, cloudflare_status


def get_technologies(domain):
    print(colored(f"Web teknolojileri tespiti yapılıyor: {domain}", 'cyan'))
    try:
        url = f'https://api.wappalyzer.com/lookup?url={domain}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Web teknolojisi tespiti yapılamadı."}
    except Exception as e:
        return {"error": str(e)}


def print_table(data):
    print(tabulate(data, headers=["Port", "Risk Seviyesi"], tablefmt="fancy_grid"))


def main():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

    target_domain = input(colored("Tarama yapacağınız hedef domaini girin: ", 'yellow'))
    
    
    target_ip = get_target_ip(target_domain)
    if not target_ip:
        print(colored("Hedef IP adresi çözümlenemedi. Lütfen geçerli bir domain girin.", 'red'))
        return

    print(colored(f"Target IP: {target_ip}", 'cyan'))

    
    open_ports = scan_ports(target_ip)
    risk_data = []
    for port in open_ports:
        risk_data.append([port, "Orta" if port < 1024 else "Düşük"])
    print_table(risk_data)

    
    dns_info = get_dns_info(target_domain)
    print(colored(f"DNS Kayıtları: {', '.join(dns_info)}", 'cyan'))

    
    cloudflare_status = check_cloudflare(target_ip)
    print(colored(f"Cloudflare var mı? {'Evet' if cloudflare_status else 'Hayır'}", 'yellow'))

    
    hosting_provider = check_hosting(target_ip)
    print(colored(f"Hosting Sağlayıcısı: {hosting_provider}", 'magenta'))

    
    telnet_status = telnet_test(target_ip)
    print(colored(f"Port 25 telnet testi: {'Başarılı' if telnet_status else 'Başarısız'}", 'green'))

    
    real_ip, cloudflare_status = get_real_ip_info(target_domain)
    if real_ip:
        print(colored(f"Gerçek IP: {real_ip}", 'blue'))
        print(colored(f"Cloudflare'da mı? {'Evet' if cloudflare_status else 'Hayır'}", 'yellow'))

    
    technologies = get_technologies(target_domain)
    print(f"Web Teknolojileri: {technologies}")

    print(colored("\nTarama işlemi tamamlandı.", 'cyan'))

if __name__ == "__main__":
    main()
