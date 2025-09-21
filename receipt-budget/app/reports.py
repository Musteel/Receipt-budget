import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def category_pie_chart(output_path='category_pie_chart.png'):
    conn = sqlite3.connect('data/receipts.db')
    df = pd.read_sql_query('SELECT category, SUM(price) as total FROM items GROUP BY category', conn)
    conn.close()

    plt.figure(figsize=(6, 6))
    plt.pie(df['total'], labels=df['category'], autopct='%1.1f%%', startangle=140)
    plt.title('Spending by Category')
    plt.savefig(output_path)
    plt.close()