from parser import parse
from result import result1, result2

def main():
    domains = ['incident_nsk', 'chp54','novosibka','novosibmy','public161146762']

    flag = 1
    while flag != 0:
        print('1. Parse')
        print('2. Results')
        print('3. Posts')
        flag = input('Function: ')
        match(flag):
            case '1':
                N = input('Choose the period of parse: ')
                parse(DOMAIN_LIST=domains, PERIOD=int(N))
            case '2':
                result1()
            case '3':
                result2()
            case _:
                flag = 0

main()