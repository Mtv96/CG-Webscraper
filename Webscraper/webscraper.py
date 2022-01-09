import requests
import tkinter as tk
import os
from tkinter import Text
from bs4 import BeautifulSoup as SoupsUp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#tkinter
root = tk.Tk()
#background
canvas = tk.Canvas(root, height = 500, width = 700, bg = "#333333")
canvas.pack()

searchTerm = tk.StringVar()
pathLoc = tk.StringVar()

def submit():
    search = searchTerm.get()
    pathLo = pathLoc.get()
    #selenium
    #chromedriver path (include 'r' infront of quotation marks)
    driver = webdriver.Chrome(pathLo)
    driver.get("https://sfbay.craigslist.org/")
    find = driver.find_element_by_name("query")
    #search input
    find.send_keys(search)
    find.send_keys(Keys.RETURN)

    #bs4
    #selenium gets current url
    URL = driver.current_url
    #bs4 requests URL
    page = requests.get(URL)
    soup = SoupsUp(page.content, "html.parser")
    show = soup.find(class_ = "rows")
    elements = show.find_all('li',class_="result-row")
    searchTerm.set('')
    pathLoc.set('')
    file = "cgLinks.txt"
    f = open(file, "w")
    for element in elements:
        #getting price and stripping the rest of the tag
        price = element.find('span', class_= 'result-price')
        if price is not None:
            pricee = price.text.strip()
        #getting name and stripping the rest of the tag
        name = element.find('a', class_= "result-title hdrlnk")
        namee = name.text.strip()
        #getting name and stripping the rest of the tag
        location = element.find('span', {'class':"result-hood"})
        #since craigslist location has a whitespace in front of it, we must have a condition for it
        if location is not None:
            locationn = location.text.strip()
        #nonetype error ignored
        try:
            link = element.find('a',"result-image gallery")['href']
        except TypeError:
            continue
        f.write("\n" + "Name: " + namee + "    Price: " + pricee + " Location: " + locationn + "\n" + link + "\n")
 
    driver.quit()
    print("All Done!")
    myLabel4 = tk.Label(frame, text = "All Done!",bg = "white", font = ("Arial", 25))
    myLabel4.pack()
    f.close()
     

    
#frame
frame = tk.Frame(root, bg = "white")
frame.place(relwidth = 0.8, relheight = 0.8, relx = 0.1, rely = 0.1)

#title label
myLabel1 = tk.Label(frame, text = "Craigslist Webscraper Bot",bg = "white", font = ("Arial", 25))
myLabel1.pack()

#warning label
myLabel6 = tk.Label(frame, text = "1.) If unresponsive, please wait a moment",bg = "white", font = ("Arial", 9))
myLabel6.pack()

#warning 2 label
myLabel9 = tk.Label(frame, text = "2.) If Chrome doesn't close in 20 secs, just close chrome and the program because output file is done",bg = "white", font = ("Arial", 9))
myLabel9.pack()

#search label
myLabel2 = tk.Label(frame, text = "Search:",bg = "white", font = ("Arial", 12))
myLabel2.pack()

#search entry bar
searchEntry = tk.Entry(frame, textvariable = searchTerm, font = ('Arial',12),bg = 'lightgrey')
searchEntry.pack()

#Chromedriver location label
myLabel3 = tk.Label(frame, text = "Chromedriver location:",bg = "white", font = ("Arial", 12))
myLabel3.pack()

#Chromedriver location entry bar
pathEntry = tk.Entry(frame, textvariable = pathLoc, font = ('Arial',12), bg = 'lightgrey')
pathEntry.pack()

#submit button
submitButton = tk.Button(frame, text = 'Search', command = submit)
submitButton.pack()



root.mainloop()


    







 
