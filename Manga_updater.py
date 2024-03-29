#Code by: Gerasimos Pnevmatikakis(SoTilted)
import time
from bs4 import BeautifulSoup
import requests
import json
import pyttsx3

def main():
    engine = pyttsx3.init()
    url='https://www.readmng.com/'#First source.
    url2='https://asuratoon.com/'#Second source.
    url3='https://luminousscans.com/'#Third source.
    url4='https://reapercomics.com/'#Fourth source.
    url5='https://mangakatana.com/'#Fifth source.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }#When we request using this, the website thinks its a user and not a bot and we dont get the captcha.
    #<--------------------getting the websites.-------------------->
    #reaperscans = requests.get(url4, headers=headers)
    luminousscans = requests.get(url3, headers=headers)
    asurascans = requests.get(url2, headers=headers)
    readmng=requests.get(url, headers=headers)
    #<--------------------parsing the html.-------------------->
    doc=BeautifulSoup(readmng.text,"html.parser")
    doc2=BeautifulSoup(asurascans.text,"html.parser")
    doc3=BeautifulSoup(luminousscans.text,"html.parser")
    #doc4=BeautifulSoup(reaperscans.text,"html.parser")


    Update_check_dic={}#This dictionary will hold the latest updated manga title and chapter of EVERY source.

    #<-------------------------------------updating the checking dictionary.------------------------------------->
    manga1=doc.find_all(class_='miniListDesc')#We find the class that holds the latest manga updates.
    #manga=manga.find_all('miniListDesc')#find chapter names and numbers.
    manga2=doc.find_all(class_='chapterBox')
    for i in range(len(manga1)):#traverse through the chapters, check if dictionary already has the manga title.
        if str(manga1[i].h2.string).strip('\n') in Update_check_dic:
            continue
        else:
            if manga2[i].a is not None and manga1[i].h2 is not None:      
                Update_check_dic[str(manga1[i].h2.string).strip('\n')]=float(str(manga2[i].a.string).strip('\n'))#add to dictionary.

    #<-------------------------------------same thing for second source.------------------------------------->
    #We do the same as above, but because the website is different, we need to find the class that holds
    #the latest manga updates and find the chapters and numbers.Also,the string format is different.
    manga=doc2.find_all(class_='luf')
    for i in range(len(manga)):
        if manga[i].h4.string in Update_check_dic:
            if (manga[i].li.a.string.split(' ')[1]).isdigit():
                if Update_check_dic[manga[i].h4.string]<float(manga[i].li.a.string.split(' ')[1]):
                    Update_check_dic[manga[i].h4.string]=float(manga[i].li.a.string.split(' ')[1])
                else:
                    continue
        else:
            if (manga[i].li.a.string.split(' ')[1]).isdigit():
                Update_check_dic[manga[i].h4.string]=float(manga[i].li.a.string.split(' ')[1])
    #<-------------------------------------same thing for third source.------------------------------------->
    #This is the exact same code because this website was probably made by the same person as above.
    manga=doc3.find_all(class_='luf')
    for i in range(len(manga)):
        if manga[i].h4.string in Update_check_dic:
            
            if Update_check_dic[manga[i].h4.string]<float(manga[i].li.a.string.split(' ')[1]):
                Update_check_dic[manga[i].h4.string]=float(manga[i].li.a.string.split(' ')[1])
            else:
                continue
        else:
            if manga[i].li is not None:
                Update_check_dic[manga[i].h4.string]=float(manga[i].li.a.string.split(' ')[1])
    #<-------------------------------------same thing for fourth source.------------------------------------->

    #<-------------------------------------Reading, checking and writting the json file(Database).------------------------------------->
    Updated=[] 

    with open('/home/gerasimos/repos/Manga_update_notifier/Manga_Base.json', 'r') as openfile:
        # Reading from json file
        Database = json.load(openfile)#this holds our database.

    for i in Update_check_dic:#We check the updated manga.
        if i in Database:#Checks if it is a manga that i read.
            if Update_check_dic[i]>Database[i]['chapter']:#Checks if the chapter number is bigger, hence if it is updated.
                chapter_difference=Update_check_dic[i]-Database[i]['chapter']#We save the chapter difference so i dont have to remember how many
                #chapters i have to read.
                Updated.append((i,Update_check_dic[i],chapter_difference))#We save a tuple of (manga title,chapter number,chapter difference) in a list.
                Database[i]['chapter']=Update_check_dic[i]#we update our Database.
                Database[i]['chapter difference']+=float(chapter_difference)#same here.



    New_Database = json.dumps(Database, indent = 1)#This is the updated Database.
    # Writing to sample.json
    with open("/home/gerasimos/repos/Manga_update_notifier/Manga_Base.json", "w") as outfile:
        outfile.write(New_Database)#we overwrite the previous data with the new data.

    #print(len(json_object))
    if len(Updated)==0:#If the list is empty, it means no new manga updated since last check.
        print('No new manga updates since last scheduled check.\n') #I dont use this print since i run this script on start-up of my laptop.
        engine.say('No new manga updates since last scheduled check.')#text to speech
        engine.runAndWait()
    else:
        for manga in Updated:#Prints the manga title, chapter and how many unread chapters i have.
            print(f'{manga[0]} chapter {manga[1]} has been updated.\nYou have not read the last {int(manga[2])} chapters.')#Same reason as before.
            engine.say(f'{manga[0]} chapter {manga[1]} has been updated.\nYou have not read the last {int(manga[2])} chapters.')#text to speech
            engine.runAndWait()

main()