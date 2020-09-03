import requests
import bs4
import csv
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib import style
import pyfiglet
import os

pwd = os.getcwd()
pwd+='/'
ascii_banner = pyfiglet.figlet_format("Welcome To Cricket Rankings!!")
print(ascii_banner)

style.use('dark_background')

View = True
while View:
    
    n=input("\x1b[1;36;40m Which ICC Rankings You want to see\n1.Test\n2.ODI\n3.T20\n4.Exit\x1b[0m\n")
    if n=='1'or n.lower()=='test':
        choice = 'icc-test-rankings'
        choice2 = '#TEST'
    elif n=='2'or n.lower()=='odi':
        choice = 'icc-odi-rankings'
        choice2 = '#ODI'
    elif n=='3'or n.lower()=='t20':
        choice = 'icc-t20-rankings'
        choice2 = '#T20'
    elif n=='4' or n.lower()=='exit':
        View = False
        break
    else:
        print('Wrong Option')
    
    url = "https://www.mykhel.com/cricket/{}/"
    source = requests.get(url.format(choice))
    url_bat = "https://www.mykhel.com/cricket/icc-batsmen-rankings/{}"
    source_bat = requests.get(url_bat.format(choice2))
    url_bowl = "https://www.mykhel.com/cricket/icc-bowlers-rankings/{}"
    source_bowl = requests.get(url_bowl.format(choice2)) 
    url_all = "https://www.mykhel.com/cricket/icc-all-rounders-rankings/{}"
    source_all = requests.get(url_all.format(choice2)) 
    
    soup = bs4.BeautifulSoup(source.text,'lxml')
    soup_bat = bs4.BeautifulSoup(source_bat.text,'lxml')
    soup_ball = bs4.BeautifulSoup(source_bowl.text,'lxml')
    soup_all = bs4.BeautifulSoup(source_all.text,'lxml')
    Title = soup.select('.os-ranking-heading')[0].text
    Title_bat = soup_bat.select('.os-ranking-heading')[0].text
    Title_bowl = soup_ball.select('.os-ranking-heading')[0].text
    Title_all = soup_all.select('.os-ranking-heading')[0].text
    
    #Defining Table Extraction
    ranking_table = soup.find('table',class_='os-ranking-table')
    ranking_table_data = ranking_table.tbody.find_all("tr")
    
    ranking_table_bat = soup_bat.find('table',class_='os-ranking-table')
    ranking_table_data_bat = ranking_table_bat.tbody.find_all("tr")
    
    ranking_table_ball = soup_ball.find('table',class_='os-ranking-table')
    ranking_table_data_ball = ranking_table_ball.tbody.find_all("tr")
    
    ranking_table_all = soup_all.find('table',class_='os-ranking-table')
    ranking_table_data_all = ranking_table_all.tbody.find_all("tr")
    #Top heading
    def table_headings(tabledata):
        headings=[]
        for td in tabledata[0].find_all("th"):
            headings.append(td.text.replace('\n', ' ').strip())
        return headings

    #Other 10 data  
    def other_data(tabledata,headings):
        data = []
        data.append(headings)
        for i in range(1,11):
            d=[]
            for td in tabledata[i].find_all("td"):
                d.append(td.text.replace('\n', ' ').strip())
            data.append(d)  
        return data
    
    headings = table_headings(ranking_table_data)
    data = other_data(ranking_table_data,headings)
    headings_bat = table_headings(ranking_table_data_bat)
    data_bat = other_data(ranking_table_data_bat,headings_bat)
    headings_ball = table_headings(ranking_table_data_ball)
    data_ball = other_data(ranking_table_data_ball,headings_ball)
    headings_all = table_headings(ranking_table_data_all)
    data_all = other_data(ranking_table_data_all,headings_all)
    
    lst_all_data = {'Team.csv':data,'Batsman.csv':data_bat,'Baller.csv':data_ball,'AllRounder.csv':data_all}    
    
    #Saving Into CSV
    for kname,vdata in lst_all_data.items():
        file = open(kname,mode='w',newline="")
        with file:
            write=csv.writer(file)
            write.writerows(vdata)
        file.close()
        #Reading CSV WIth Pandas
        df = pd.read_csv(pwd+kname,index_col=False)
        df.reset_index(drop=True, inplace=True)
        if kname=='Team.csv':
            print('\x1b[6;30;42m' +'\t'+ Title + '\x1b[0m')
        elif kname=='Batsman.csv':
            print('\x1b[6;30;42m' +'\t'+ Title_bat.replace('100','10') + '\x1b[0m')
        elif kname=='Baller.csv':
            print('\x1b[6;30;42m' +'\t'+ Title_bowl + '\x1b[0m')
        else:
            print('\x1b[6;30;42m' +'\t'+ Title_all + '\x1b[0m')
        print(df)
        #Plotting CSV Data
        plotselect = input("\n\x1b[1;36;40m Enter Plot Type \n1.Line Plot\n2.Scatter Plot\n3.Bar Plot\n4.Pie Chart\n5.No Need\n6.Exit\x1b[0m\n").lower()
        d=""
        if kname=='Team.csv':
            d=df['Country'][::-1]
        else:
            d=df['Player'][::-1]
        if plotselect == '1' or plotselect == 'Line Plot':
            plt.plot(d,df['Points'][::-1])
            plt.show()
        elif plotselect == '2' or plotselect == 'scatter plot':
            plt.scatter(d,df['Points'][::-1])
            plt.show()
        elif plotselect == '3' or plotselect == 'bar':
            plt.bar(d,df['Points'][::-1])
            plt.show()
        elif plotselect == '4' or plotselect == 'piechart':
            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1,])
            ax.axis('equal')
            Country = d
            Points = df['Points']
            ax.pie(Points, labels = Country,autopct='%1.2f%%')
            plt.show()
        elif plotselect == '5' or plotselect.lower() == 'no need':
            continue
        elif plotselect == '6' or plotselect.lower() == 'end script':
            break
        else:
            print("Wrong Option")
        
    
