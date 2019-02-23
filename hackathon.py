from lxml import html
from lxml.etree import tostring
import requests


presidents = "ford carter reagen bush clinton obama"
year = [["FORD","1976","1977"],["CARTER","1977","1981"],["REAGEN","1981","1989"],["BUSH1","1989","1993"],["CLINTON","1993","2001"],["BUSH2","2001","2009"]]
quit = False
out_thing = []
name = input("Enter the last name of a president from 1974 to 2014")
name: str = name.upper()

for num in range(6):
    temp = []
    temp = year[num]
    if temp[0] == name:
        out_thing.append(temp[0])
        out_thing.append(temp[1])
        out_thing.append(temp[2])
print(out_thing)

endyear= out_thing[2]
url = "https://api.census.gov/data/timeseries/bds/firms?get=estabs_entry_rate,estabs_exit_rate,estabs_entry,net_job_creation,ifsize&for=us:*&year2="+ endyear + "&key=b2fe9fbe9c805f2fb54e8c0398c97450a3132cde"

page = requests.get(url)
tree = html.fromstring(page.content)

api_data = tostring(tree).decode("utf-8")

api_data = api_data[4:-5]

api_data = api_data.split(",\n")



for i in range(len(api_data)):
    api_data[i] = api_data[i][1:-1]
    api_data[i] = api_data[i].split(", ")
    for j in range(len(api_data[i])):
        api_data[i][j] = api_data[i][j].replace('"', '').split(",")

sum=0

for x in range(1,14):
    sum+= int(api_data[x][0][3])


print("The net sum of job creation in " + str(name) + "'s last term is " + str(sum))








