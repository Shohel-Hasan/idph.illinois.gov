import requests, re, os, csv 
from bs4 import BeautifulSoup as BS
import pandas as pd


if not os.path.exists('Data'):
    os.mkdir('Data')

def csvMaker(filename):
    if not os.path.exists('Data/'+filename+'.csv'):
        with open('Data/' + filename +'.csv','w',newline='',errors='ignore') as f:
            wr = csv.writer(f)
            wr.writerow([
                'Facility Name',
                'Facility Address',
                'Docket',
                'Date',
                'Fine Assessment Amount',
            ])

csvMaker(filename='Data')

def csvWriter(data,filename):
    with open('Data/' + filename +'.csv','a',newline='',errors='ignore') as f:
        wr = csv.writer(f)
        wr.writerow(data)

def toExcel():
    try:
        df = pd.read_csv('Data/Data.csv')
        df.to_excel('Data/Data.xlsx',index=False)
    except:
        pass 
    try:
        os.remove('Data/Data.csv')
    except:
        pass 

def main(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.2171.95 Safari/537.36'}
    s = requests.Session()
    res = s.get(url=url,headers=headers)
    soup = BS(res.text,'lxml')
    try:
        table_tr = soup.find('table')
        lines = table_tr.text.splitlines()
        facility_name = ''
        facility_addr = ''
        docker = ''
        date = ''
        amount = ''
        data = []
        for line in lines:
            if 'FACILITY NAME:' in line.strip():
                facility_name = line.replace('FACILITY NAME:','').strip()
                print("FACILITY NAME:",facility_name)
                data.append(facility_name)
            else:
                facility_name = ''
            if 'FACILITY ADDRESS:' in line.strip():
                facility_addr = line.replace('FACILITY ADDRESS:','').strip()
                print('FACILITY ADDRESS:',facility_addr)
                data.append(facility_addr)
            else:
                facility_addr = ''
            if 'DOCKET #:' in line.strip():
                docker = line.replace('DOCKET #:','').strip()
                print('DOCKET #:',docker)
                data.append(docker)
            else:
                docker = ''
            if line.strip().startswith('On'):
                date = line.split('sent',1)[0].replace('On','').strip()
                amount = line.split('$')[1].split('.')[0].strip()
                print("Date: ",date)
                print("Amount: ",amount)
                data.append(date)
                data.append(amount)
                csvWriter(data=data,filename='Data')
                data.clear()
            else:
                date = ''
                amount = ''
            if line.strip().startswith('By'):
                csvWriter(data=data,filename='Data')
                data.clear()
            
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main(url='https://idph.illinois.gov/about/nursing_homes_violations06/quarterly_report_4-06.htm')
    toExcel()