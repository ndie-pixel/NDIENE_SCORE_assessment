import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)


def parse_csv(csv_data):
    rows = csv_data.strip().split('\n')
    parsed_data = []
    for row in rows:
        name, score = row.split(',')
        parsed_data.append([name.strip(), int(score.strip())])
    return parsed_data


def create_table():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores (name TEXT, score INTEGER)''')
    conn.commit()
    conn.close()

def insert_data(name, score):
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()

def get_top_scorers():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute("SELECT name, score FROM scores")
    data = c.fetchall()
    
    if not data:
        return []
    
    top_score = max([score for _, score in data])
    top_scorers = sorted([name for name, score in data if score == top_score])
    conn.close()
    
    return top_scorers, top_score


@app.route('/add_score', methods=['POST'])
def add_score():
    data = request.json
    name = data.get('name')
    score = data.get('score')
    
    if not name or not isinstance(score, int):
        return jsonify({"error": "Invalid input"}), 400
    
    insert_data(name, score)
    return jsonify({"message": "Score added successfully"}), 201

@app.route('/top_scorers', methods=['GET'])
def top_scorers():
    top_scorers, top_score = get_top_scorers()
    return jsonify({"top_scorers": top_scorers, "score": top_score}), 200

if __name__ == '__main__':
    create_table()  
    app.run(debug=True, use_reloader=False)
