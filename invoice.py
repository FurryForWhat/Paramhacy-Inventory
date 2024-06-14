import tools

def display_invoice():
    tools.print_in_middle("Invoice Section")
    tools.print_with_borders("Press 1 to create invoice")
    tools.print_with_borders("Press 2 to view history")
    ran = True
    while ran:
        U_input = input("Here➡️  ")
        if U_input == '1':
            ran = False
            create_invoice()
        elif U_input == '2':
            ran = False
            pass
        else:
            print("Invalid Input❌❌")

def create_invoice():
    client,database,collection = tools.mongo_connect()
    total_amount = 0
    total_item = 0
    buy_flag = False
    purchase_name = {}
    purchase_Q = {}
    purchase_P = {}
    j = 0
    print('Phone_number should start with 09xxxxxxxxx')
    buyer:list = input("Enter client data: (name,age,Phone_number)-> ").split(',')
    
    while buy_flag == False:
        medic_flag = False
        while medic_flag == False:
            medic_name = input("Enter medic name:")
            for i in collection.find({},{"_id":0,"medic name":1}):
                if i["medic name"] == medic_name:
                    medic_flag = True
            if medic_flag != True:
                print("No item found!!")    
        medic_quantity_flag = False 
        while medic_quantity_flag == False:
            medic_Q = input("Enter quantity:")   
            medic_P = 0
            for i in collection.find({},{"_id":0,"medic name":1,"quantity":1,"sale":1}):
                if i["medic name"] == medic_name:
                    if int(i["quantity"]) < int(medic_Q):
                        print("Insufficient medical, avaliable stocks: ",i["quantity"])
                    else:    
                        for_medic_name = "medic name"+str(j)
                        for_medic_Q = "quantity"+str(j)
                        for_medic_P = "price"+str(j)
                        j += 1
                        purchase_name.update({for_medic_name:i["medic name"]})
                        purchase_Q.update({for_medic_Q:medic_Q})
                        purchase_P.update({for_medic_P:i["sale"]})
                        total_item += int(medic_Q)
                        medic_P = int(i["sale"])
                        medic_quantity_flag = True
                        pre_data = i['quantity']
                        pre_dict = {'quantity':pre_data}
                        new_data = int(i['quantity']) - int(medic_Q)
                        new_dict = {"$set":{'quantity':new_data}}
                        collection.update_one(pre_dict,new_dict)
        total_amount += medic_P*int(medic_Q)
        for i in range(len(purchase_name)):
            print(f'You had purchased:{list(purchase_name.values())[i]} for {list(purchase_Q.values())[i]} items and each cost {list(purchase_P.values())[i]}')
        buy_option = input("Do you want more, Y/N?")
        if buy_option.lower() == 'n':
            buy_flag = True
    
    user_data = [list(buyer),list(purchase_name.values()),list(purchase_P.values()),list(purchase_Q.values()),total_amount]
    # print(user_data)
    storing_invoice(user_data)
    print(f"It will cost: {total_amount}")

def storing_invoice(user_data):
    Date,Time = tools.today_date()
    Time = f'{Time[0]} hr:{Time[1]} min:{Time[2]} sec'
    invoice_client,invoice_database,invoice_collection = tools.mongo_invoice()
    log = {'Date':Date,'Time':Time,'Name':str(user_data[0][0]),'Items':str(user_data[1]),'Price_per_each':str(user_data[2]),'Quantity':str(user_data[3]),'Total Price':str(user_data[4])}
    
    invoice_collection.insert_one(log)
    print("Successful...")
    
def view_history():
    tools.print_with_borders("Press 1 history of today")
    tools.print_with_borders("Press 2 history of this month")
    tools.print_with_borders("Press 3 to customize month")
    tools.print_with_borders("Press 4 to exit")
    his_flag = True
    while his_flag:
        user_input = input("Here➡️  :")
        if user_input == "1":
            # his_flag = False
            history_today()
        elif user_input == "2":
            # his_flag = False
            history_thisMonth()
        elif user_input == "3":
            # his_flag = False
            custom_history()
        elif user_input == "4":
            his_flag = False
            return
        else:
            print("Invalid Options")
 
def history_today():
    client,database,collection = tools.mongo_invoice()
    date,time = tools.today_date()
    year = date[2]
    day= date[0]
    month = date[1]   
    count = 0
    for i in collection.find({},{"_id":0,"Date":1,"Total Price":1,"Name":1,"Items":1,"Price_per_each":1,"Quantity":1}):
        #myDay,myMonth,myYear
        temp_day = i["Date"][0]
        temp_month = i["Date"][1]
        temp_year = i["Date"][2]
        if temp_day == day and temp_month == month and temp_year == year:
            count += 1
            print(f"{count} Buyer:{i["Name"]} Purchased item:{i["Items"]} Quantity:{i["Quantity"]} Total:{i["Total Price"]}")
                  
def history_thisMonth():
    client,database,collection = tools.mongo_invoice()
    date,time= tools.today_date()
    year = date[2]
    day= date[0]
    month = date[1]
    
    for i in collection.find({},{"_id":0,"Date":1,"Total Price":1,"Name":1,"Items":1,"Price_per_each":1,"Quantity":1}):
        pass

def custom_history():
    pass
           
history_today()