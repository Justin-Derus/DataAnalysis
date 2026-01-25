import pandas as pd
import datetime as dt
import calendar
import numpy as np

pd.set_option('display.max_rows',None)         # commented out, pandas does not display full table by default must set option
pd.set_option('display.max_columns',None)
# Information needed for transactions table
customer_table = pd.read_csv(".\customer.csv")
customer_table = customer_table.drop(columns=['CustomerName','PhoneNumber','Address','Email'])
datetimes = [] # Populated with every day of the year for 7 years
branch_table = pd.read_csv(".\\branch.csv")
branch_table = branch_table.drop(columns=['Country','State','City','Address','ZIPCODE'])
employee_table = pd.read_csv(".\employee.csv")
employee_table = employee_table.drop(columns=['ManagerID','EmployeeName'])
product_table = pd.read_csv(".\product.csv")

years = [2019,2020,2021,2022,2023,2024,2025]
months = [1,2,3,4,5,6,7,8,9,10,11,12]
for year in years:
    for month in months:
        num_days = calendar.monthrange(year, month)[1]
        for day in range(num_days):
            day = day + 1
            x = dt.datetime(year,month,day) # datetime object, YYYY-MM-DD HH:MM:SS
            datetimes.append(x)

# Rules for transaction generation
# 1) Every year, the customer signup rate goes up 2.5%-5% starting at 25% (i.e. 75% are anon with CustomerID = 0)
# 2) Number of transactions per date is between 75 - 350 (75 - 150 small, 150 - 250 med, 250 - 350 big "city")
# 3) Branch ID is randomly assigned but will be skewed towards "big city" branches
# 4) Employees will be chosen at random at a rate of about 10% of the time (this shows that an employee just swayed the customer to buy product (NOT CASHIER))
product_grouping = [
        ["Dog Food"], # 50%   
        ["Dog Chew","Dog Toy","Dog Treats"], # 30%
        ["Pet Comfort"], # 15%
        ["Dog Apparel", "Dog Supplement", "Health", "Hygiene", "Pet Hardware"] # 5%
    ]

products = product_table.loc[:,["ProductID","ProductName","Category","Price"]]
product_prob = [0.6,0.25,0.1,0.05]



def transactions(customer_probibility: list, dates: dt.datetime, product_df: pd.DataFrame, product_probability: list):

    # Possible customers
    customer_list = customer_table.values.tolist()
    anon = customer_list.pop(0)
    possible_customers = [anon, list(range(1,len(customer_list)))]

    branch_grouping = [
        [1,2,5,11,12,13,15,16,19,20], # Small 10%
        [4,8,9,10,14,18],             # Medium 25%
        [3,6,7,17]                    # Big 65%
    ]
    employee_probs = [.83,.17] # odds an employee sells an item (NOT cashier)

    with open("./last_transaction_id.txt","r",encoding="utf-8") as fr:
        latest_transactionID = int(fr.read())

    transactionID = latest_transactionID

    # Transaction Loop
    with open("./transactions2024_12.sql", "w", encoding="utf-8") as f: # Change this
        for day in dates:
            if day.year == 2024 and day.month == 12:                     # Change this
                for branch_number in range(1,21):
                    #-------------------- Branch --------------------------------------------------
                    if(branch_number in branch_grouping[0]): # Small
                        transactions_amount = np.random.randint(50,100)
                    elif(branch_number in branch_grouping[1]): # Medium
                        transactions_amount = np.random.randint(100,200)
                    else: 
                        transactions_amount = np.random.randint(200,350) # Large
                    if day.month == 12: # holiday season
                        transactions_amount = transactions_amount * 1.27
                        transactions_amount = int(transactions_amount)
                    else: 
                        #transactions_amount = int(transactions_amount * np.random.uniform(1.15, 1.25)) # Change this for 2020
                        transactions_amount = int(transactions_amount * 1.02)
                    for transaction in range(1, transactions_amount - 1):
                        #print("***************New Transaction**************")
                        #-------------------- Customer ------------------------------------------------
                        customer_choice = np.random.choice([0,1],p=customer_probibility) # between 0 and full list of customers
                        customer_chosen = np.random.choice(possible_customers[customer_choice])

                        #-------------------- Employee ------------------------------------------------
                        branch_employees = employee_table[employee_table["BranchID"] == branch_number]
                        employee_list = branch_employees['EmployeeID'].to_list()
                        possible_employees = [[None], employee_list]
                        employee_choice = np.random.choice([0,1], p=employee_probs)# Between null and actual employee (15%)
                        employee_chosen = np.random.choice(possible_employees[employee_choice])
                        # datetime object, YYYY-MM-DD HH:MM:SS
                        if employee_choice != 0:
                            sql_transactions_insert = (
                                "INSERT INTO `Transactions` (CustomerID, Date, BranchID, EmployeeID) VALUES ("
                                f"{customer_chosen}, '{day}', {branch_number}, {employee_chosen});"
                            )
                            f.write(sql_transactions_insert + "\n")
                        else:
                            sql_transactions_insert = (
                                "INSERT INTO `Transactions` (CustomerID, Date, BranchID) VALUES ("
                                f"{customer_chosen}, '{day}', {branch_number});"
                            )
                            f.write(sql_transactions_insert + "\n")

                        # Rules
                        # 1) Products are chosen at random based on a categorical probability
                        # 2) Products are more likely to be bought if one brand is bought (next item on list chances go up) 
                        # 3) Count of products are chosen randomly 
                        # 4) Anything not food related goes up around holidays
                        # 5) Unit count also increases around holidays
                        # 6) 
                        #-------------------- Product ------------------------------------------------
                        itemlistlength = np.random.randint(1,5)
                        for item in range(itemlistlength):
                            product_cat_choice = np.random.choice([0,1,2,3], p=product_probability)
                            product_cat_chosen = np.random.choice(product_grouping[product_cat_choice])
                            product_cat_list = product_df[product_df['Category'] == product_cat_chosen]
                            items = product_cat_list['ProductID'].tolist()
                            product_chosen = np.random.choice(items)
                            product_info = product_df[product_df["ProductID"] == product_chosen]
                            #print(product_info)
                            unit_total = np.random.randint(1,3)
                            sale = unit_total * product_info['Price'].values[0]
                            #print("Units: " + str(unit_total) + " * " + str(product_info['Price'].values[0]) + " = " + str(sale))
                            sql_transaction_items = "INSERT INTO `TransactionItems` (TransactionID, SaleTotal, UnitTotal, ProductID) VALUES ("
                            text = str(transactionID) + ", " + str(sale) + ", " + str(unit_total) + ", " + str(product_info['ProductID'].values[0])
                            print(str(transactionID))
                            sql_transaction_items += text + ");"
                            f.write(sql_transaction_items + "\n")
                        transactionID += 1
    with open("./last_transaction_id.txt","w") as fw:
        fw.write(str(transactionID))
    return



customer_signup= [.68,.32]
transactions(customer_signup,datetimes,products,product_prob)

#customer_signup_increase = round(np.random.uniform(2.5, 5),2)
#customer_signup_increase = customer_signup_increase / 100

#customer_signup[0] -= customer_signup_increase # anonymous customers decrease
#customer_signup[1] += customer_signup_increase