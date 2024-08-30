# Expense Tracker
#### Introduction
This is to implement a CLI app to manage expenses 
#### Usage
You can interact  with the system through the following commands
make sure you have python on your system

Command
```shell
py expense-tracker add --description "Lunch" --amount 20
`````
Output
# Expense added successfully (ID: 1)

Command
```shell
py expense-tracker add --description "Dinner" --amount 10
```
Output
# Expense added successfully (ID: 2)

Command
```shell
py expense-tracker list
```
Output
# ID  Date       Description  Amount
# 1   2024-08-06  Lunch        $20
# 2   2024-08-06  Dinner       $10

Command
```shell
py expense-tracker summary
```
Output
# Total expenses: $30

Command
```shell
py expense-tracker delete --id 1
```
Output
# Expense deleted successfully

Command
```shell
py expense-tracker summary
```
Output
# Total expenses: $20

Command
```shell
py expense-tracker summary --month 8
```
Output
# Total expenses for August: $20

