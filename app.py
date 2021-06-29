import pymysql
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='rlagkrrbs', db='web_test', charset="utf8")
cursor = db.cursor()

# http://localhost:5000/
@app.route("/", methods=["GET"])
def hello():
    return "OK"

# http://localhost:5000/page
@app.route("/page", methods=["GET"])
def home_page():
    return render_template('index.html')

@app.route("/student", methods=["POST"])
def insert_student():
    name = request.form["name"]
    korean = request.form["korean"]
    math = request.form["math"]
    english = request.form["english"]
    sql = """
        insert into student_score (name, korean, math, english) values ('%s', %s, %s, %s)
    """ % (name, korean, math, english)
    cursor.execute(sql)
    db.commit()
    return "OK"
#
@app.route("/students", methods=["GET"])
def get_students():
    sql = """select * from student_score"""
    cursor.execute(sql)
    results = cursor.fetchall()  # ()
    #print(results)
    students_dict = []
    for result in results:
        students_dict.append({
            "id": result[0],
            "name": result[1],
            "korean": result[2],
            "math": result[3],
            "english": result[4],
        })
    return jsonify(students_dict)

@app.route("/student", methods=["PUT"])
def update_student():
    name = request.form["name"]
    korean = request.form["korean"]
    math = request.form["math"]
    english = request.form["english"]

    sql = """
        update student_score set korean=%s, math=%s, english=%s
        where name = '%s'
    """ % (korean, math, english, name)
    cursor.execute(sql)
    db.commit()
    return "OK"
#
@app.route("/student", methods=["DELETE"])
def delete_student():
    name = request.args.get("name")
    sql = """
        delete from student_score where name = %s
    """ % name
    cursor.execute(sql)
    db.commit()
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
