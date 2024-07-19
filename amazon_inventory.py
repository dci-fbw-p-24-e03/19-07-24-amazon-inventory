import csv
from datetime import datetime
import functools
import sys
import time
FILENAME = 'warehouse_inventory.csv'

def load_data():
    with open(FILENAME,mode='r',newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)
    
def save_data(data):
    with open(FILENAME,mode='w',newline='') as file:
        fieldnames = ['item', 'quantity', 'expiration_date', 'price']
        writer = csv.DictWriter(file,fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            
def progress_bar(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        for i in range(21):
            time.sleep(0.1)
            sys.stdout.write('\r')
            sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
            sys.stdout.flush()
        print('\nDone')
        result = func(*args,**kwargs)
        return result
    return wrapper
def check_item_present(func):
    def wrapper(data,*args,**kwargs):
        item = kwargs.get('item')
        if any(d['item'] == item for d in data):
            return func(data,*args,**kwargs)
        else :
            print(f'Item {item} not found.')
            return
    return wrapper
        
@progress_bar
def add_item(data,item,quantity,expiration_date,price):
    data.append({
        'item':item,
        'quantity':quantity,
        'expiration_date':expiration_date,
        'price':price
    })
    save_data(data)
    return

@progress_bar
@check_item_present
def remove_item(data,item):
    '''for d in data:
        if d.get('item') == item:
            data.remove(d)'''
    data = [d for d in data if d['item'].lower()!=item.lower()]
    save_data(data)
    return
@progress_bar
@check_item_present
def update_item(data,item,quantity=None,expiration_date=None,price=None):
    for d in data:
        if d['item']== item:
            if quantity is not None:
                d['quantity']=quantity
            if expiration_date is not None:
                d['expiration_date']=expiration_date
            if price is not None:
                d['price']=price
    save_data(data)
def sort_by_expriation_date(data):
    return sorted(data,key=lambda x:datetime.strptime(x['expiration_date'],'%Y-%m-%d'))
@progress_bar
def get_full_report(data):
    if not data:
        print("No items in the inventory.")
        return None
    data = sort_by_expriation_date(data)
    print("-" * 60)
    print("\nFull Inventory Report")
    print(f"|{'Item':<20} | {'Quantity':<10} | {'Expiration Date':<20} | {'Price':<10}|")
    print("-" * 60)
    for item in data:
        print(f"|{item['item']:<20} | {item['quantity']:<10} | {item['expiration_date']:<20} | {item['price']:<10}|")
    #task:save report to pdf and send it to nizar

@check_item_present
@progress_bar
def search_item(data,item):
    found_items = [d for d in data if d['item'].lower()==item.lower()]
    print(f"\nSearch Results for '{item}'")
    print(f"{'Item':<20} {'Quantity':<10} {'Expiration Date':<20} {'Price':<10}")
    print("-" * 60)
    for item in found_items:
        print(f"{item['item']:<20} {item['quantity']:<10} {item['expiration_date']:<20} {item['price']:<10}")
@progress_bar
def get_expired_items(data):
    today=datetime.today().date()
    expired_items =[d for d in data  if datetime.strptime(d['expiration_date'],'%Y-%m-%d').date() < today]
    if not expired_items:
        print('No expired items found.')
        return []
    expired_items=sort_by_expriation_date(expired_items)
    print("\nExpired Items")
    print(f"{'Item':<20} {'Quantity':<10} {'Expiration Date':<15} {'Price':<10}")
    print("-" * 60)
    for item in expired_items:
        print(f"{item['item']:<20} {item['quantity']:<10} {item['expiration_date']:<15} {item['price']:<10}")
    return expired_items
        
