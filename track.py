from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import os
import enum
import sqlite3


def inTable(name, cursor):
    query= "SELECT 1 FROM games WHERE title = ? LIMIT 1"
    cursor.execute(query, (name,))
    return cursor.fetchone() is not None


def add(name, URL, db):
    cursor= db.cursor()
    if inTable(name, cursor): return False

    query= "INSERT INTO games (date, title, url) VALUES (?, ?, ?)"
    cursor.execute(query, (datetime.now(), name, URL))
    db.commit()
    cursor.close()
    return True
    
def view(db, type):
    cursor= db.cursor()
    query= ""
    match type:
        case 0: # sales
            query= "SELECT date, title, orig_price, sale_price FROM games WHERE sale_price <> 'NULL'"
        case 1: # all
            query= "SELECT date, title, orig_price, sale_price FROM games"
    cursor.execute(query)
    for x in cursor:
        date= x[0]
        name= x[1]
        orig_price= x[2]
        sale_price= x[3]
        if orig_price != None:
            orig_price= "$" + str(orig_price)
        else:
            orig_price= str(orig_price)
        if sale_price != None:
            sale_price= "$" + str(sale_price)
        else:
            sale_price= str(sale_price)
        print(date + " " + name.ljust(25) + " " + orig_price.ljust(7) + " " + sale_price)
    cursor.close()
    
def remove(name, db):
    cursor= db.cursor()
    if not inTable(name, cursor): return False

    query= "DELETE FROM games WHERE title = ?"
    cursor.execute(query, (name,))
    db.commit()
    cursor.close()
    return True

def update(db):
    cursor= db.cursor()
    cursor.execute("SELECT id, url FROM games")
    for id,url in cursor:
        updateHelper(db, id, url)
    cursor.close()
    return True

def updateHelper(db, id, URL):
    today= datetime.today()
    cookies = {'birthtime': '568022401'}
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                                'Accept-Language': 'en-US, en;q=0.5'})
    webpage= requests.get(URL, headers= HEADERS, cookies= cookies)
    soup= BeautifulSoup(webpage.content, "lxml")

    # This will set the date at which information was updated
    cursor= db.cursor()

    # Trying to get the title of the game
    # This should already be given by the user when they add the entry to database
    #try:
    #    title= soup.find("div", attrs={"id" : 'appHubAppName', "class" : "apphub_AppName"})
    #    title= title.string.strip()
    #except AttributeError:
    #    title = None

    # This is to find the price of the item
    try:
        parent= soup.find("div", attrs= {"class" : "game_area_purchase_game_wrapper"})
    except AttributeError:
        parent= 0
        orig_price= None
        disc_price= None

    if (parent != 0):
        try:
            orig_price= parent.find("div", attrs={"class" : "discount_original_price"}, recursive= True)
            disc_price = parent.find("div", attrs={"class" : "discount_final_price"}, recursive= True)
            orig_price= orig_price.string.strip()
            disc_price= disc_price.string.strip()
            orig_price= orig_price[1:]
            disc_price= disc_price[1:]
        except AttributeError:
            try:
                orig_price= parent.find("div", attrs={"class" : 'game_purchase_price price',
                "data-price-final" : re.compile(r"\d*")}, recursive= True).string.strip()
                orig_price= orig_price[1:]
                disc_price= None
            except:
                orig_price= None
                disc_price= None
    
    query= "UPDATE games SET date = ?, orig_price = ?, sale_price = ? WHERE id = ?"
    cursor.execute(query, (today, orig_price, disc_price, id))
    db.commit()
    cursor.close()

