from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="bincomtest",
        user="postgres",
        password="Hayo24434078",
        port=5432
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/polling_unit', methods=['GET', 'POST'])
def polling_unit():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        pu_id = request.form['polling_unit_id']
        cur.execute("SELECT party_abbreviation, party_score FROM announced_pu_results WHERE polling_unit_uniqueid = %s", (pu_id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('polling_unit.html', results=results, pu_id=pu_id)

    cur.execute("SELECT uniqueid, polling_unit_name FROM polling_unit")
    polling_units = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('polling_unit.html', polling_units=polling_units)

@app.route('/lga_result', methods=['GET', 'POST'])
def lga_result():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        lga_id = request.form['lga_id']
        cur.execute("""
            SELECT apr.party_abbreviation, SUM(apr.party_score) 
            FROM announced_pu_results apr
            JOIN polling_unit pu ON apr.polling_unit_uniqueid = pu.uniqueid
            WHERE pu.lga_id = %s
            GROUP BY apr.party_abbreviation
        """, (lga_id,))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('lga_result.html', results=results, lga_id=lga_id)

    cur.execute("SELECT lga_id, lga_name FROM lga WHERE state_id = 25")
    lgas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('lga_result.html', lgas=lgas)

@app.route('/new_polling_unit', methods=['GET', 'POST'])
def new_polling_unit():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        pu_name = request.form['pu_name']
        lga_id = request.form['lga_id']
        party_scores = request.form.getlist('party_score')
        party_names = request.form.getlist('party_abbreviation')

        cur.execute("INSERT INTO polling_unit (polling_unit_name, lga_id) VALUES (%s, %s) RETURNING uniqueid",
                    (pu_name, lga_id))
        pu_id = cur.fetchone()[0]

        for party, score in zip(party_names, party_scores):
            cur.execute("INSERT INTO announced_pu_results (polling_unit_uniqueid, party_abbreviation, party_score) VALUES (%s, %s, %s)",
                        (pu_id, party, int(score)))

        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')

    cur.execute("SELECT lga_id, lga_name FROM lga WHERE state_id = 25")
    lgas = cur.fetchall()
    cur.execute("SELECT DISTINCT party_abbreviation FROM announced_pu_results")
    parties = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template('new_polling_unit.html', lgas=lgas, parties=parties)

if __name__ == '__main__':
    app.run(debug=True)
