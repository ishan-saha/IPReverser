import json
import requests
import pandas
import time
import art
from colorama import Fore, Back, Style

delay = 1 # seconds to wait for yougetsignal to respond
base_url = "https://domains.yougetsignal.com/domains.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "https://www.yougetsignal.com/",
    "Origin": "https://www.yougetsignal.com"
}
def format_text(title,item, log=0):
    if log==1:
        text = Style.BRIGHT + Fore.RED + " [-] " + Fore.RESET + Fore.YELLOW + title + Fore.RESET + Fore.BLUE + item + Fore.RESET
    else:
        cr = '\r\n'
        section_break=cr + '*'*20 + cr 
        item=str(item)
        text= Style.BRIGHT+ Fore.RED + title + Fore.RESET + Fore.YELLOW +section_break + Fore.BLUE + item + Fore.YELLOW + section_break + Fore.RESET
    return text

def reverse_ip_lookup(ip):
    params = {
        "remoteAddress": ip
    }
    response = requests.post(base_url, params=params, headers=headers)
    response_json = response.json()
    return response_json

def get_domain_list(response_json):
    domain_list = []
    if response_json["status"]=="Success" and response_json["domainCount"] != '0':
        for domain in response_json["domainArray"]:
            if len(domain) != 0:
                domain_list.append(domain[0])
    return domain_list

def ip_loader():
    ip_list = []
    with open("target.txt", "r") as f:
        for line in f:
            ip_list.append(line.strip())
    return ip_list

def list_to_excel(domain_list):
    df = pandas.DataFrame(domain_list)
    df.to_excel("domains.xlsx", index=False)

def main():
    banner = art.text2art("IPReverser",font='slant') + "\n\t\t\t- by Ishan Saha"
    print(format_text(banner,"Add the IP in the target.txt file"))
    all_domains = []
    try:
        ip_list = ip_loader()
        print(format_text("Note: ","targets selected!",1))
        for ip in ip_list:
            time.sleep(delay)
            response_json = reverse_ip_lookup(ip)
            domain_list = get_domain_list(response_json)
            print(format_text("Data Extracted for "+str(ip)+": ",str(domain_list),1))
            all_domains.extend(domain_list)
        list_to_excel(all_domains)
        print()
        print(format_text('Note: ','Adding extracted information to excel!',1))
    except KeyboardInterrupt:
        print(format_text("Note: ","User Interupted! Exiting!",1))
        exit()
    except Exception as e:
        print(format_text(e,''))    

if "__main__" == __name__:
    main()
