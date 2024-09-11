# Expense Tracker - Personal Finance Manager
Expense Tracker is a desktop application built in Python using the Tkinter and ttkbootstrap libraries for the user interface, SQLite for data storage, and matplotlib for data visualization. The application helps users track their income and expenses, visualize financial data, and generate summaries of financial health over specific time periods.

## Features
### Track Income and Expenses:
- Add new income and expense transactions.
- Edit or delete existing transactions.
- Categorize expenses into predefined categories.
### Summaries:
- View a summary of total income, expenses, and balance.
- Monthly summary for current income, expenses, and net balance.
### Visualizations:
#### Dashboard with different charts to visualize financial data:
- Pie chart for total balance (income vs. expenses).
- Monthly balance breakdown.
- Bar chart of expenses grouped by categories.
- Line chart to track expenses over time.
### Data Storage:
Data is persisted locally in a SQLite database.

## Usage
### Main Dashboard
- When the app starts, you will see the Main Dashboard with an overview of your total and monthly income, expenses, and balance.
- A "+" button is available to quickly add income or expenses.
### Transactions
- Navigate to the "Transactions" tab to view all your income and expense records.
- You can edit or delete transactions from this tab.
### Visualizations
In the "Visualizations" tab, you can view detailed charts that help analyze your spending.

## Application Structure
- main.py: The main entry point for the application. Handles the GUI, interaction with the database, and dashboard.
- visualizations.py: Contains functions for generating various data visualizations (pie, bar, and line charts).
- db.py: Handles database connections, table creation, and data queries (income, expenses, categories).
- images/: Directory containing any necessary image files (e.g., app icons).

## Screenshots
### Main Dashboard

![image](https://github.com/user-attachments/assets/636b0953-ef45-474f-bbee-2c82f272d9bc)
### Visualizations

![image](https://github.com/user-attachments/assets/7b70b26c-832f-4cfc-81ca-3a424c69bbeb)

## Future Improvements
- User Authentication: Add a login system to allow multiple users to track their finances individually.
- Recurring Transactions: Add functionality for recurring income or expenses (e.g., monthly rent or salary).
- Export Data: Ability to export reports in CSV or PDF format.
- Predictive Analysis: Add machine learning models to predict future expenses based on previous spending patterns.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
If you have any questions or issues, feel free to open an issue on the repository or contact me at [magdalenamalek52@gmail.com].
