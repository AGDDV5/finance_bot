import pandas as pd
import matplotlib.pyplot as plt
import io

def format_currency(amount):
    return f"{int(amount):,}".replace(",", " ")

def generate_dashboard(data, lang_code, text_func):
    """
    Generates a Pie Chart for expenses.
    data: list of dicts [{'category': 'Food', 'amount': 50000}, ...]
    """
    if not data:
        return None

    df = pd.DataFrame(data)
    
    # Simple Pie Chart
    plt.figure(figsize=(6, 6))
    plt.pie(df['amount'], labels=df['category'], autopct='%1.1f%%', startangle=140)
    plt.title(text_func(lang_code, 'expense'))
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def generate_excel(transactions, filename="report.xlsx"):
    """
    Generates Excel with Pandas
    """
    df = pd.DataFrame(transactions)
    # Add logic here to summarize and format columns
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Transactions', index=False)
    output.seek(0)
    return output