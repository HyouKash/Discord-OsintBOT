import discord
import requests
import ipinfo
import json
import time
import requests,re
import tweepy
import os
import pyautogui
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

ipinfo_token = 'a5442d52fc3446'
heure = time.ctime()
screenWidth, screenHeight = pyautogui.size()

sitesPseudo = [
    "https://ask.fm/", 
    "https://bitcoinforum.com/profile/",    
    "https://www.blogger.com/",
    "https://www.chess.com/member/", 
    "https://community.cloudflare.com/u/",
    "https://www.codecademy.com/profiles/",
    "https://www.codewars.com/users/",
    "https://www.cracked.com/members/", 
    "https://dev.to/",
    "https://www.dailymotion.com/",
    "https://hub.docker.com/u/",
    "https://www.duolingo.com/profile/",
    "https://euw.op.gg/summoner/userName=",
    "https://www.facebook.com/",
    "https://www.fandom.com/u/",
    "https://flipboard.com/@",
    "https://fortnitetracker.com/profile/all/",
    "https://www.gamespot.com/profile/",
    "https://giphy.com/",
    "https://www.github.com/",
    "https://gitlab.com/",
    "https://forum.hackthebox.eu/profile/",
    "https://hackaday.io/",
    "https://news.ycombinator.com/user?id=",
    "https://hackerone.com/",
    "https://hackerrank.com/",
    "https://imgur.com/user/",
    "https://forums.kali.org/member.php?username=",
    "https://keybase.io/",
    "https://www.kongregate.com/accounts/",
    "https://www.liveleak.com/c/",
    "https://www.mixcloud.com/",
    "https://myanimelist.net/profile/",
    "https://myspace.com/",
    "https://namemc.com/profile/",
    "https://ok.ru/",
    "https://opensource.com/users/",
    "https://psnprofiles.com/?psnId=",
    "https://pastebin.com/u/",
    "https://www.patreon.com/",
    "https://www.periscope.tv/",
    "https://www.pinterest.com/",
    "https://play.google.com/store/apps/developer?id=",
    "https://pokemonshowdown.com/users/",
    "https://pypi.org/user/",
    "https://raidforums.com/User-",
    "https://www.reddit.com/user/",
    "https://www.roblox.com/user.aspx?username=",
    "https://scratch.mit.edu/users/",
    "https://soundcloud.com/",
    "https://sourceforge.net/u/",
    "https://speedrun.com/user/",
    "https://open.spotify.com/user/",
    "https://robertsspaceindustries.com/citizens/",
    "https://steamcommunity.com/id/",
    "https://steamcommunity.com/groups/",
    "https://t.me/",
    "https://tiktok.com/@",
    "https://www.gotinder.com/@",
    "https://www.tradingview.com/u/",
    "https://tripadvisor.com/members/",
    "https://tryhackme.com/p/",
    "https://www.twitch.tv/",
    "https://mobile.twitter.com/",
    "https://data.typeracer.com/pit/profile?user=",
    "https://vimeo.com/",
    "https://www.wattpad.com/user/",
    "https://weheartit.com/",
    "https://forums.whonix.org/u/",
    "https://www.wikipedia.org/wiki/User:",
    "https://xboxgamertag.com/search/",
    "https://www.instagram.com/",
    "https://www.younow.com/",
    "https://youpic.com/photographer/",
    "https://www.youtube.com/",
    "https://allmylinks.com/",
    "https://forum.guns.ru/forummisc/blog/",
    "https://gfycat.com/@",
    "https://www.hackster.io/",
    "http://forum.igromania.ru/member.php?username=",
    "http://www.jeuxvideo.com/profil/",
    "https://www.metacritic.com/user/",
    "https://note.com/",
    "https://www.npmjs.com/~",
    "https://osu.ppy.sh/users/",
]

def get_sites_info(liste, pseudo):
    final_liste = []
    for k in liste:
        k += pseudo
        try:
            response = requests.get(k)
            if response.status_code == 200:
                final_liste.append(k)
            else:
                pass
        except:
            pass
    return final_liste
    
def get_ip_info(token, ip):
    handler = ipinfo.getHandler(ipinfo_token)
    details = handler.getDetails(ip)
    return details.all

def get_num_info(num):
    url = 'https://www.infos-numero.com/ajax/NumberInfo?num=' + num
    get_info = requests.get(url).text
    return json.loads(get_info)['info']

def get_num_infoPJ(num):
    urlPJ = 'https://www.pagesjaunes.fr/annuaireinverse/recherche?quoiqui=' + num
    get_infoPJ = requests.get(urlPJ).text
    soup = BeautifulSoup(get_infoPJ, 'html.parser')
    finalInfo = soup.find_all("a", {"class" : "denomination-links pj-lb pj-link"})[0].text.strip()
    finalInfo += "\n" + soup.find_all("a", {"class" : "adresse pj-lb pj-link"})[0].text.strip()
    return finalInfo

def get_adress_info(adress):
    urlAdressPJ = 'https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui=&ou=' + adress
    get_infosAdress = requests.get(urlAdressPJ).text
    soup = BeautifulSoup(get_infosAdress, 'html.parser')
    result = []
    for i in range(len(soup.find_all("a", {"class" : "denomination-links pj-lb pj-link"}))):
        finalInfo = soup.find_all("a", {"class" : "denomination-links pj-lb pj-link"})[i].text.strip()
        finalInfo += "\n" + soup.find_all("a", {"class" : "adresse pj-lb pj-link"})[i].text.strip()
        finalInfo += "\n" + soup.find_all("strong", {"class" : "num"})[i].text.strip()
        result.append(finalInfo)
    return result

def get_person_infos(nomPrenom, ville):
    urlPersonPJ = 'https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={}&ou={}'
    get_infosPerson = requests.get(urlPersonPJ.format(nomPrenom, ville)).text
    soup = BeautifulSoup(get_infosPerson, 'html.parser')
    result = []
    profiles_list = soup.find_all("div", {"class":"zone-bi"})
    for profile in profiles_list:
        finalInfo = [n.text.strip() for n in profile.find_all("a", {"class": "denomination-links pj-lb pj-link"})][0]
        finalInfo += "\n" + [a.text.strip() for a in profile.find_all("a", {"class": "adresse pj-lb pj-link"})][0]
        try:
            finalInfo += "\n" + [n.text.strip().replace(" ","") for n in profile.find_all("strong", {"class": "num"})][0]
        except:
            finalInfo += "\nNo num"
        result.append(finalInfo)
    return result
    
def get_twitter_info(pseudo):
    finalInfo = []
    urlMDPtwitter = 'https://twitter.com/account/begin_password_reset?account_identifier=' + pseudo
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'   
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),chrome_options=chrome_options)
    driver.get(urlMDPtwitter)
    button = driver.find_element_by_xpath('/html/body/div[2]/div/form/input[3]').click()
    Numero = driver.find_element_by_xpath('/html/body/div[2]/div/form/ul/li[1]/label/strong').text
    finalInfo.append(Numero)
    email = driver.find_element_by_xpath('/html/body/div[2]/div/form/ul/li[2]/label/strong').text
    finalInfo.append(email)
    return finalInfo

class MyClient(discord.Client):
    async def on_ready(self):
        print('Connecté au bot', self.user, "à", heure[11:19] + ".")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if '.menuinfo' in message.content :
            webhook_infosMenu = DiscordWebhook(url='WEBHOOK URL', content = None)
            embed = DiscordEmbed(title="Menu de l'OSINT Bot", description=None, color=000000)
            embed.add_embed_field(name = "1/ .ipinfo : (ex: .ipinfo 8.8.8.8)", value = "Informations sur n'importe quelle IP.", inline=False)
            embed.add_embed_field(name = "OUT - 2/ .numinfo : (ex: .numinfo 07.59.56.32.45)", value = "Informations sur n'importe quel numéro.", inline=False)
            embed.add_embed_field(name = "OUT - 3/ .adressinfo (ex: .adressinfo 80 Quai des Chartrons)", value = "Informations personnelles pour n'importe quelle adresse.", inline=False)
            embed.add_embed_field(name = "OUT - 4/ .personinfo : (ex: .personinfo Pierre Dupuis / Paris)", value = "Informations sur un Nom/Prénom.", inline=False)
            embed.add_embed_field(name = "5/ .pseudoinfo : (ex: .pseudoinfo HyouKa)", value = "Listes des sites trouvés pour le pseudo.", inline=False)
            embed.add_embed_field(name = "6/ .twitterinfo : (ex: .twitterinfo HyouKa)", value = "Site + fin de Numéro + adresse mail obfuscate.", inline=False)
            embed.set_author(name='HyouKa#2312', url='https://github.com/hyoukash', icon_url = "https://cdn.discordapp.com/avatars/777220625747148830/4d5628dc59b9c93b4f15ca45d5c5f56e.png?size=4096")
            webhook_infosMenu.add_embed(embed)
            response = webhook_infosMenu.execute()

        if '.ipinfo' in message.content :
            await message.channel.send("Recherche en cours pour l'IP : " + message.content[8:])
            ip = message.content[8:]
            infosIp = get_ip_info(ipinfo_token, ip)
            webhook_IpInfo = DiscordWebhook(url='WEBHOOK URL', content = None)
            embed = DiscordEmbed(title="Informations pour l'IP : " + ip, description=None, color=000000)
            
            for data, result in infosIp.items():
                embed.add_embed_field(name = data, value = result, inline=False)
            embed.set_author(name='HyouKa#2312', url='https://github.com/hyoukash', icon_url = "https://cdn.discordapp.com/avatars/777220625747148830/4d5628dc59b9c93b4f15ca45d5c5f56e.png?size=4096")
            webhook_IpInfo.add_embed(embed)
            response = webhook_IpInfo.execute()
        
        if '.numinfo' in message.content :
            await message.channel.send("Recherche en cours pour le numéro : " + message.content[9:])
            num = message.content[9:]
            infosNum = get_num_info(num)
            webhook_NumInfo = DiscordWebhook(url='WEBHOOK URL', content = None)               
            embed = DiscordEmbed(title = "Informations pour le numéro : " + num, description=None, color=000000)
            embed.set_author(name = 'HyouKa#2312', url = 'https://github.com/hyoukash', icon_url = "https://cdn.discordapp.com/avatars/777220625747148830/4d5628dc59b9c93b4f15ca45d5c5f56e.png?size=4096")
            embed.add_embed_field(name = "Type", value = infosNum['type_lang']['fr'], inline=False)
            embed.add_embed_field(name = "Ville", value = infosNum['ville'], inline=False)
            try:
                infosNumPJ = get_num_infoPJ(num)
                print(infosNumPJ)
                embed.add_embed_field(name = "Nom", value = infosNumPJ.split("\n")[0], inline=False)
                embed.add_embed_field(name = "Adresse", value = infosNumPJ.split("\n")[1], inline=False)
            except:
                embed.add_embed_field(name = "Opérateur", value = infosNum['carrier'], inline=False)
                pass            
            webhook_NumInfo.add_embed(embed)
            response = webhook_NumInfo.execute()

        if '.adressinfo' in message.content :
            await message.channel.send("Recherche en cours pour l'adresse : " + message.content[12:]) 
            adress = message.content[12:]
            infosAdressall = get_adress_info(adress)

            if infosAdressall==[]:
                webhook_AdressInfo = DiscordWebhook(url='WEBHOOK URL', content = None)
                embed = DiscordEmbed(title="Informations pour l'adresse' : " + adress, description=None, color=000000)
                embed.set_author(name='HyouKa#2312', url='https://github.com/hyoukash', icon_url = "https://cdn.discordapp.com/avatars/777220625747148830/4d5628dc59b9c93b4f15ca45d5c5f56e.png?size=4096")
                embed.add_embed_field(name = "Result", value = "Nothing", inline=False)

                webhook_AdressInfo.add_embed(embed)
                response = webhook_AdressInfo.execute()

            for infosAdress in infosAdressall:
                webhook_AdressInfo = DiscordWebhook(url='WEBHOOK URL', content = None)
                embed = DiscordEmbed(title="Informations pour l'adresse' : " + adress, description=None, color=000000)
                embed.set_author(name='HyouKa#2312', url='https://github.com/hyoukash', icon_url = "https://cdn.discordapp.com/avatars/777220625747148830/4d5628dc59b9c93b4f15ca45d5c5f56e.png?size=4096")
                embed.add_embed_field(name = "Nom", value = infosAdress.split("\n")[0], inline=False)
                embed.add_embed_field(name = "Adresse", value = infosAdress.split("\n")[1], inline=False)
                embed.add_embed_field(name = "Numéro", value = infosAdress.split("\n")[3], inline=False)

                webhook_AdressInfo.add_embed(embed)
                response = webhook_AdressInfo.execute()

        if '.personinfo' in message.content :
            msg = message.content.split("/ ")
            await message.channel.send("Recherche en cours pour la personne : " + msg[0][12:] + "à " + msg[1])
            nomPrenom = msg[0][12:]
            ville = msg[1]
            infosPersonAll = get_person_infos(nomPrenom, ville)
            
            if infosPersonAll==[]:
                webhook_PersonInfo = DiscordWebhook(url='WEBHOOK URL', content = None)
                embed = DiscordEmbed(title="Informations pour la personne : " + nomPrenom, description=None, color=000000)
                embed.set_author(name='HyouKa#2312', url='https://github.com/hyoukash', icon_url = "https://cdn.discordapp.com/avatars/777220625747148830/4d5628dc59b9c93b4f15ca45d5c5f56e.png?size=4096")
                embed.add_embed_field(name = "Result", value = "Nothing", inline=False)

                webhook_PersonInfo.add_embed(embed)
                response = webhook_PersonInfo.execute()

            for infosPerson in infosPersonAll:
                webhook_PersonInfo = DiscordWebhook(url='WEBHOOK URL', content = None)
                embed = DiscordEmbed(title="Informations pour la personne : " + nomPrenom, description=None, color=000000)
                embed.set_author(name='HyouKa#2312', url='https://github.com/hyoukash', icon_url = "https://cdn.discordapp.com/avatars/777220625747148830/4d5628dc59b9c93b4f15ca45d5c5f56e.png?size=4096")
                embed.add_embed_field(name = "Nom", value = infosPerson.split("\n")[0], inline=False)
                embed.add_embed_field(name = "Adresse", value = infosPerson.split("\n")[1], inline=False)
                embed.add_embed_field(name = "Numéro", value = infosPerson.split("\n")[3], inline=False)

                webhook_PersonInfo.add_embed(embed)
                response = webhook_PersonInfo.execute()
            
        if '.pseudoinfo' in message.content : 
            await message.channel.send("Recherche de site en cours pour le pseudo : " + message.content[12:])
            pseudo = message.content[12:]
            infosPseudo = get_sites_info(sitesPseudo, pseudo)
            final_infosPseudo = ""
            for k in infosPseudo :
                final_infosPseudo += k + "\n"
            await message.channel.send(final_infosPseudo)

        if '.twitterinfo' in message.content :
            await message.channel.send("Recherche d'informations du compte Twitter : " + message.content[13:])
            await message.channel.send("Connexion au proxie/VPN..")
            os.startfile(r'Mullvad VPN')
            time.sleep(2)
            pyautogui.click('VPN.png')
            time.sleep(15)
            pseudo = message.content[13:]
            infosTwitter = get_twitter_info(pseudo)
            webhook_PersonInfo = DiscordWebhook(url='WEBHOOK URL', content = None)
            embed = DiscordEmbed(title="Informations pour le compte Twitter : " + pseudo, description=None, color=000000)
            embed.set_author(name='HyouKa#2312', url='https://github.com/hyoukash', icon_url = "https://cdn.discordapp.com/avatars/777220625747148830/4d5628dc59b9c93b4f15ca45d5c5f56e.png?size=4096")
            embed.add_embed_field(name = "Site", value = "Plus d'informations : https://tinfoleak.com/", inline=False)
            embed.add_embed_field(name = "Numéro", value = "xx xx xx xx " + infosTwitter[0], inline=False)
            embed.add_embed_field(name = "Email", value = infosTwitter[1], inline=False)
            webhook_PersonInfo.add_embed(embed)
            response = webhook_PersonInfo.execute()

client = MyClient()
client.run('TOKEN')