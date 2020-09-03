import requests
import bs4
import csv
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib import style
import pyfiglet


ascii_banner = pyfiglet.figlet_format("Welcome To Cricket Rankings!!")
print(ascii_banner)

style.use('dark_background')

View = True
while View:
    n=input("\x1b[1;36;40m Which ICC Team Rankings You want to see\n1.Test\n2.ODI\n3.T20\n4.Exit\x1b[0m\n")
    if n=='1'or n.lower()=='test':
        choice = 'icc-test-rankings'
    elif n=='2'or n.lower()=='odi':
        choice = 'icc-odi-rankings'
    elif n=='3'or n.lower()=='t20':
        choice = 'icc-t20-rankings'
    elif n=='4' or n.lower()=='exit':
        View = False
        break
    else:
        print('Wrong Option')
    
    url = "https://www.mykhel.com/cricket/{}/"
    source = requests.get(url.format(choice))
    soup = bs4.BeautifulSoup(source.text,'lxml')
    Title = soup.select('.os-ranking-heading')[0].text
    
    #Defining Table Extraction
    ranking_table = soup.find('table',class_='os-ranking-table')
    ranking_table_data = ranking_table.tbody.find_all("tr")
    #Top heading
    def table_headings(tabledata):
        headings=[]
        for td in tabledata[0].find_all("th"):
            headings.append(td.text.replace('\n', ' ').strip())
        return headings

    #Other 10 data  
    def other_data(tabledata):
        data = []
        data.append(headings)
        for i in range(1,11):
            d=[]
            for td in tabledata[i].find_all("td"):
                d.append(td.text.replace('\n', ' ').strip())
            data.append(d)  
        return data
    
    headings = table_headings(ranking_table_data)
    data = other_data(ranking_table_data)

    print('\x1b[6;30;42m' +'\t'+ Title + '\x1b[0m')
    #print(Title)
    #Saving Into CSV
    file = open('Rankings.csv',mode='w',newline="")
    with file:
        write=csv.writer(file)
        write.writerows(data)
    #Reading CSV WIth Pandas
    df = pd.read_csv('/home/lieutenant/Documents/Python3Jupyter/Rankings.csv',index_col=False)
    df.reset_index(drop=True, inplace=True)
    print(df)
    #Plotting CSV Data
    plotselect = input("\n\x1b[1;36;40m Enter Plot Type \n1.Line Plot\n2.Scatter Plot\n3.Bar Plot\n4.Pie Chart\x1b[0m\n").lower()
    if plotselect == '1' or plotselect == 'Line Plot':
        plt.plot(df['Country'][::-1],df['Points'][::-1])
        plt.show()
    elif plotselect == '2' or plotselect == 'scatter plot':
        plt.scatter(df['Country'][::-1],df['Points'][::-1])
        plt.show()
    elif plotselect == '3' or plotselect == 'bar':
        plt.bar(df['Country'][::-1],df['Points'][::-1])
        plt.show()
    elif plotselect == '4' or plotselect == 'piechart':
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1,])
        ax.axis('equal')
        Country = df['Country']
        Points = df['Points']
        ax.pie(Points, labels = Country,autopct='%1.2f%%')
        plt.show()
    else:
        print("Wrong Option")
        
    