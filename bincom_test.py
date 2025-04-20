from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import mysql.connector


app = Flask(__name__)
app.secret_key = 'supersecretkey'  # for flash messages

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hayo24434078%",
    database="bincomphptest",
    auth_plugin='mysql_native_password'  # Use this if you have issues with authentication
)
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('home.html')

# ---------------- TASK 1: Polling Unit Results ----------------
@app.route('/polling_unit', methods=['GET', 'POST'])
def polling_unit():
    results = None
    if request.method == 'POST':
        polling_unit_name = request.form['polling_unit_name']

        cursor.execute("""
            SELECT uniqueid, polling_unit_name
            FROM polling_unit
            WHERE polling_unit_name LIKE %s
        """, ('%' + polling_unit_name + '%',))
        units = cursor.fetchall()

        if units:
            selected_id = units[0][0]
            cursor.execute("""
                SELECT party_abbreviation, party_score
                FROM announced_pu_results
                WHERE polling_unit_uniqueid = %s
            """, (selected_id,))
            results = cursor.fetchall()

    return render_template('polling_unit.html', results=results)

# ---------------- TASK 2: LGA Results ----------------
@app.route('/lga_results', methods=['GET', 'POST'])
def lga_results():
    results = []
    lgas = []

    cursor.execute("SELECT lga_id, lga_name FROM lga WHERE state_id = 25")
    lgas = cursor.fetchall()

    if request.method == 'POST':
        lga_id = int(request.form['lga_id'])
        print(f"Selected LGA ID: {lga_id}")  # 👈 this shows the submitted LGA ID
        
        cursor.execute("SELECT uniqueid FROM polling_unit WHERE lga_id = %s", (1,))
        units = cursor.fetchall()
        print("Polling Units in LGA 1:", units)

        
        cursor.execute("""
            SELECT apr.party_abbreviation, SUM(apr.party_score)
            FROM polling_unit pu
            LEFT JOIN announced_pu_results apr 
            ON pu.uniqueid = apr.polling_unit_uniqueid
            WHERE pu.lga_id = %s
            GROUP BY apr.party_abbreviation
        """, (lga_id,))
        results = cursor.fetchall()
        print("Results fetched:", results)  # 👈 this shows what came back from the DB

    return render_template('lga_results.html', lgas=lgas, results=results)

# ---------------- TASK 3: Add Polling Unit Results ----------------
@app.route('/add_polling_unit_results', methods=['GET', 'POST'])
def add_polling_unit_results():
    if request.method == 'POST':
        polling_unit_id = request.form['polling_unit_id']
        party_abbrs = request.form.getlist('party[]')
        votes = request.form.getlist('votes[]')
        entered_by_user = 'Hasan'  # Replace with dynamic value if needed
        date_entered = datetime.now()
        user_ip = request.remote_addr

        for party, vote in zip(party_abbrs, votes):
            cursor.execute("""
                INSERT INTO announced_pu_results (
                    polling_unit_uniqueid,
                    party_abbreviation,
                    party_score,
                    entered_by_user,
                    date_entered,
                    user_ip_address
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (polling_unit_id, party, vote, entered_by_user, date_entered, user_ip))
        
        conn.commit()
        flash("Polling unit results added successfully!", "success")
        return redirect(url_for('add_polling_unit_results'))

    return render_template("add_polling_unit_results.html")


if __name__ == '__main__':
    app.run(debug=True)
