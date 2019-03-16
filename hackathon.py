from lxml import html
from lxml.etree import tostring
import requests


presidents = "ford carter reagan bush clinton obama"

#*****NOTE: FORD DOESN'T WORK
year = [["FORD","1976","1977"],["CARTER","1977","1981"],["REAGAN","1981","1989"],["BUSH1","1989","1993"],["CLINTON","1993","2001"],["BUSH2","2001","2009"]]
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
# print(out_thing)
startyear = out_thing[1]
endyear= out_thing[2]
jobsum=0
for year in range(int(startyear),int(endyear)):
    url = "https://api.census.gov/data/timeseries/bds/firms?get=estabs_entry_rate,estabs_exit_rate,estabs_entry,net_job_creation,ifsize&for=us:*&year2="+ str(year) + "&key=b2fe9fbe9c805f2fb54e8c0398c97450a3132cde"
    page = requests.get(url)
    result = page.json()
    for x in range(1,len(result)):
        jobsum+= int(result[x][3])


print("The net sum of job creation in " + str(name.capitalize()) + "'s complete administration is " + str(jobsum))
print("This indicates that per year an average of number of " + str(int((int(jobsum)/(int(endyear)-int(startyear))))) + " jobs were created")

net_poverty = 0
url_poverty_endyear = 'https://api.census.gov/data/timeseries/poverty/histpov2?get=PCTPOV&for=us:*&time=' + str(endyear) + '&RACE=1' + "&key=b2fe9fbe9c805f2fb54e8c0398c97450a3132cde"
url_poverty_startyear = 'https://api.census.gov/data/timeseries/poverty/histpov2?get=PCTPOV&for=us:*&time=' + str(startyear) + '&RACE=1' + "&key=b2fe9fbe9c805f2fb54e8c0398c97450a3132cde"


page = requests.get(url_poverty_endyear)
api_data_poverty_endyear = page.json()
page = requests.get(url_poverty_startyear)
api_data_poverty_startyear = page.json()
net_poverty = float(api_data_poverty_endyear[1][0]) - float(api_data_poverty_startyear[1][0])
increase_or_decrease = ""
if net_poverty < 0:
    increase_or_decrease = "decrease"
else:
    increase_or_decrease = "increase"
print("When " + name.upper() + " was president, the country experienced a ", abs(round(net_poverty, 1)), "% " + increase_or_decrease +" in poverty rate")


