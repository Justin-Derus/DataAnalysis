import pandas as pd
import datetime as dt
import calendar
import numpy as np

# Information needed for transactions table
customer_table = pd.read_csv(".\PowerBI\PremiumDogOutlet\customer.csv")
customer_table = customer_table.drop(columns=['CustomerName','PhoneNumber','Address','Email'])
datetimes = [] # Populated with every day of the year for 7 years
branch_table = pd.read_csv(".\PowerBI\PremiumDogOutlet\\branch.csv")
branch_table = branch_table.drop(columns=['Country','State','City','Address','ZIPCODE'])
employee_table = pd.read_csv(".\PowerBI\PremiumDogOutlet\employee.csv")
employee_table = employee_table.drop(columns=['ManagerID','EmployeeName'])

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



def transactions(customer_probibility: list, dates: dt.datetime):
    # Possible customers
    customer_list = customer_table.values.tolist()
    anon = customer_list.pop(0)
    possible_customers = [anon, list(range(1,len(customer_list)))]

    branch_grouping = [
        [1,2,5,11,12,13,15,16,19,20], # Small 10%
        [4,8,9,10,14,18],             # Medium 25%
        [3,6,7,17]                    # Big 65%
    ]
    employee_probs = [.85,.15] # odds an employee sells an item (NOT cashier)

    # Transaction Loop
    with open("./transactions2019.sql", "w", encoding="utf-8") as f:
        for day in dates:
            if day.year == 2019 and day.month == 1:
                for branch_number in range(1,20):
                    #-------------------- Branch --------------------------------------------------
                    if(branch_number in branch_grouping[0]): # Small
                        transactions_amount = np.random.randint(50,100)
                    elif(branch_number in branch_grouping[1]): # Medium
                        transactions_amount = np.random.randint(100,200)
                    else: 
                        transactions_amount = np.random.randint(200,350) # Large

                    for x in range(transactions_amount):
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
                        sql = "INSERT INTO `Transactions` (CustomerID, Date, BranchID, EmployeeID) VALUES ("

                        sql_values = str(customer_chosen) + ", " + str(day) + ", " + str(branch_number) + ", " + str(employee_chosen) + ");"
                        sql += sql_values
                        f.write(sql + "\n")
    return


prob2019 = [.75,.25]
transactions(prob2019,datetimes)
