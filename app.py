from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'  # For flash messages

# Initialize the database connection
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    expenses = cursor.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        category = request.form['category']
        
        conn = sqlite3.connect('expenses.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)',
                       (description, amount, category))
        conn.commit()
        conn.close()
        flash('Expense added successfully!')
        return redirect(url_for('index'))
    
    return render_template('add_expense.html')

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()
    flash('Expense deleted successfully!')
    return redirect(url_for('index'))

@app.route('/chart-data')
def chart_data():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/')
def home():
    return "Hello, Flask is working !"

if '__name__' == '__main__':
    print("Starting flask app")
    init_db()
    app.run(debug=True, use_reloader=False)