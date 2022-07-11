import pandas as pd 
import matplotlib.pyplot as plt
from datetime import datetime as dt
import ast 

def plot(t,c):
    plot_df = [[],[]]
    df = invoice(t[0],t[1]).to_dict()
    for i in (list(df['subcategory'].items())):
        if i[1] == c:
            plot_df[0].append(df['time'][i[0]])
            plot_df[1].append(df['price'][i[0]])
    plt.plot(plot_df[0],plot_df[1],'ob')
    plt.xlabel('date')
    plt.ylabel(c)
    plt.show()

    pass

def time_obj(data): #convert srting object to date object
    for i in list(data['time'].items()):
        data['time'][i[0]] = dt.strptime(i[1],'%Y-%m-%d').date()
    pass

def analys(ca): #print each category and its subs shares
    total_cost = 0
    cat_cost = 0
    subcats_cost = {}
    print(cats)
    print(list(cats[ca].keys()))
    for i in list(cats[ca].keys()):
        subcats_cost[i] = 0
    for i in list(check_list['price'].items()):
        if check_list['category'][i[0]] != 'charge':
            total_cost += i[1]

    for i in list(check_list['category'].items()):
        if ca == i[1]:
            cat_cost += check_list['price'][i[0]]

    for i in list(subcats_cost.keys()):
        for j in list(check_list['subcategory'].items()):
            if i == j[1]:
                subcats_cost[i] += check_list['price'][j[0]]
    print('{0} costs {1}$ till now {2}%.' 
    'of all costs'.format(ca,cat_cost,round(cat_cost/total_cost*100.0)),'\n')
    for i in list(subcats_cost.items()):
        print('{0} {1}%. of {2}'.format(i[0],round(i[1]/cat_cost*100.0),ca))
    print('\n')
    return None

def invoice(t1, t2): #creat a csv file include all transactions between two times
    def between_time(time1,tin,time2): # compare times
        ti1 = dt.strptime(time1,'%Y-%m-%d').date()
        ti2 = dt.strptime(time2,'%Y-%m-%d').date()
        if ti1<tin<ti2:
            return True
        else:
            return False
    
    transactions = {'time': {}, 'category': {},
     'subcategory': {}, 'price': {},
      'related unit(s)': {}, 'responsible unit': {},
       'div': {}, 'description': {}
    }
    
    counter = 0
    for i in list(check_list['time'].items()):
        try:
            if between_time(t1, i[1], t2):
                for j in list(check_list.keys()):
                    transactions[j][counter]=check_list[j][i[0]]
            counter += 1
        except:
            pass
    df = pd.DataFrame(transactions).sort_values(by='time')
    return df

def record(text): # get order and record in notes
    def add(order,sc):  #add a sub order to check list
        if list(check_list[sc].keys()) != []:
            last = max(list(check_list[sc].keys()))
            check_list[sc][last+1] = order
        else:
            check_list[sc][0] = order
        return None
        
    def apply(un,share): #apply finansial changes in units balance
        if un == 'all':
            for i in range(len(accounts)-1):
                accounts[str(i+1)][0] += share[i]
                accounts['box'][0] += share[i]
        else:
            names = un.strip('][').split(",")
            if names[0] != '':
	            i = 0
	            for name in names:
	                accounts[name][0] += share[i]
	                accounts['box'][0] += share[i]
	                i = i + 1

        return None
 
    def div(v,price): # out put is a list include every unit share for a single transcaction
        if v == 'e':
            total_units = len(building_info['UN'])
            s = price/total_units
            share = []
            for i in range(total_units):
                share.append(s)
        elif v == 'a':
            total_area = sum(list(building_info['area'].values()))
            share = []
            for i in list(building_info['area'].values()):
                share.append(price*float(i)/total_area)
        elif v == 'r':
            res = list(building_info['residents'].values())
            total_residents = sum(res)
            share = []
            for i in res:
                share.append(price*float(i)/total_residents)
        elif v == 'p':
            par = list(building_info['PL'].values())
            total_PL = sum(par)
            share = []
            for i in par:
                share.append(price*float(i)/total_PL)
        elif v == 'd':
            var = cats[orders[1]][orders[2]]
            if var == 'c':
                share = price
            else:
                share = div(var,price)
        else:
            share = []
            shares = ast.literal_eval(v)
            for i in shares:
                share.append(price*float(i)/sum(shares))
        return share

    orders = text.split()
    subcheck = list(check_list.keys())
    if orders[0] == 'now':
        orders[0] = dt.today().date()
    else:
        time_object = dt.strptime(orders[0],'%Y-%m-%d').date()
        orders[0] = time_object
    for i in range(0, 8):
        add(orders[i],subcheck[i])
    if orders[1] == 'charge':
        price = float(orders[3])
    else:
        price = -float(orders[3])
    apply(orders[4],div(orders[6],price))
    pd.DataFrame(accounts).to_csv('accounts.csv',index_label=False)
    pd.DataFrame(check_list).to_csv('check_list.csv',index=False)
    print('\n')
    return None

def reset():
    for i in list(check_list.items()):
        check_list[i[0]] = {}
    for i in list(accounts.items()):
        accounts[i[0]] = {0:0}
    pd.DataFrame(accounts).to_csv('accounts.csv',index_label=False)
    pd.DataFrame(check_list).to_csv('check_list.csv',index=False)
    return None

cats = {           #catrgories informations
    "Ghabz": {"Water": "w", "bargh": "b", "gaz": "g", "avarez": "a"},
    "nezafat":{},
    "asansor":{},
    "parking":{},
    "tamirat":{},
    "other":{}
}

# main loop for runnig
while True:
           #read nessesary files
    check_list = pd.read_csv('check_list.csv').to_dict()
    try:
        time_obj(check_list)
    except:
        pass
    building_info = pd.read_json('building_info.json').to_dict()
    accounts = pd.read_csv('accounts.csv').to_dict()
    step1 = input('type "record" for entering an order\n'
     'type "report" to get report options\n'
     'typr "reset" to reset accounts and list\n'
      'type "exit" to end the program\n')
    if step1 == 'record':
        while True:
            line = input('type order in sort of:\n'
            'time category subcategory price related_units'
            'responsible_unit division discribtion\n'
            'type "back" to get back\n')
            if line != 'back':
                record(line)
            else:
                break
    elif step1 == 'report':
        while True:
            step2 = input('type "inv" to get invoice file\n'
            'type "fb" to get financial balance for units\n'
            'type "analys" to get categories analys\n'
            'type "plot" to draw a plot\n'
            'type "back" to get back\n')
            if step2 == 'inv':
                try:
                    t1 = input('from : ')
                    t2 = input('to: ')
                    invoice(t1,t2).to_csv('{0} to {1}.csv'.format(t1,t2), index=False)
                    print('flie created in current path\n')
                except:
                    print('wrong time or empty list\n')
            elif step2 == 'fb':
                try:
                    un = input('which unit? ')
                    print(round(accounts[un][0]),'\n')
                except:
                    print('wronf unit number\n')
            elif step2 == 'analys':
                ca = input('which category ? ')
                try:
                    analys(ca)
                except:
                    print('no costs till now or wrong name\n')
            elif step2 == 'plot':
                t = [input('from date: '),input('to date: ')]
                c = input('which subcategory ? ')
                try:
                    plot(t,c)
                except:
                    pass
                
            elif step2 == 'back':
                break
    elif step1== 'reset':
        sure = input('are you sure to clear all data? ')
        if sure == 'yes':
            reset()
        
    elif step1 == 'exit':
        break







        
