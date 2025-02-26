import VKParser
import TGParser
from result import result1, result2
import tools

def main():
    
    flag = 1
    while flag != 0:
        print('1. Parse VK with date settings')
        print('2. Parse VK and TG with preset date settings')
        print('3. Parse VK with preset date settings')
        print('4. Parse TG with preset date settings')
        print('5. Take results from database')
        flag = input('Function: ')
        match(flag):
            case '1':
                startdate, enddate = tools.input_dates('', '')
                VKParser.parse(startdate, enddate)
            case '2':
                startdate, enddate = tools.input_dates('01.01.2024','01.01.2025')
                tm1 = tools.timer(0, 0,0)
                VKParser.parse(startdate, enddate)
                TGParser.parse()
                tm2 = tools.timer(1,0,0)
                tools.timer(2, tm1, tm2)
            case '3':
                startdate, enddate = tools.input_dates('01.01.2024','01.01.2025')
                tm1 = tools.timer(0,0,0)
                VKParser.parse(startdate, enddate)
                tm2 = tools.timer(1,0,0)
                tools.timer(2, tm1, tm2)
            case '4':
                startdate, enddate = tools.input_dates('01.01.2024','01.01.2025')
                tm1 = tools.timer(0, 0,0)
                TGParser.parse()
                tm2 = tools.timer(1,0,0)
                tools.timer(2, tm1, tm2)
            case '5':
                result1()
            case _:
                flag = 0

main()