from flask import Flask, request, render_template, url_for
import sqlite3

icafe = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('icafe.db')
    conn.row_factory = sqlite3.Row
    return conn

@icafe.route("/")
def main():
    return render_template("main.html")

@icafe.route("/admin_login")
def admin_login():
    return render_template("login.html")

@icafe.route("/admin_login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['passw']
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT username, password FROM admin_acc WHERE username = ? AND password = ?", (username, password))
        log = cur.fetchone()
        cur.close()
        con.close()
        if log:
            return render_template("admin_dashboard.html")
        else:
            return render_template("login.html")

@icafe.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")

@icafe.route("/view_pc/<int:id>")
def view_pc(id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM tech_dashboard WHERE id = ?", (id,))
    data = cur.fetchone()
    cur.close()
    con.close()
    return render_template("view_pc.html", data=data)
    
        
@icafe.route("/tech_dashboard", methods = ["POST", "GET"])
def tech_dashboard():
    if request.method == "POST":
        pc_id = request.form["id"]
        time_start = request.form["ts"]
        time_end = request.form["te"]
        details = request.form["details"]
        past_problem = request.form["pp"]
        status = request.form["status"]
        con = get_db_connection()
        cur = con.cursor()
        """
        cur.execute("INSERT INTO tech_dashboard (time_start, time_end, details, past_problem, status) VALUES (?, ?, ?, ?, ?)", (time_start, time_end, details, past_problem, status))"
        """
        cur.execute("UPDATE tech_dashboard SET time_start = ?, time_end = ?, details = ?, past_problem = ?, status = ? WHERE id = ?", (time_start, time_end, details, past_problem, status, pc_id))
        con.commit()
        cur.close()
        con.close()
        return render_template("tech_dashboard.html")
    return render_template("tech_dashboard.html")

if __name__ == '__main__':
    icafe.run(debug=True)