import pymysql
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='rlagkrrbs', db='web_test', charset="utf8")
cursor = db.cursor()

# 연결됐는지 확인 화면에 ok라고 뜸
# http://localhost:5000/
@app.route("/", methods=["GET"])
def hello():
    return "OK"

# templates폴더 안에 html 열기
# http://localhost:5000/page
@app.route("/page", methods=["GET"])
def home_page():
    return render_template('index.html')

# insert는 POST 사용
# db로 클라이언트에서 입력한 이름 한국어 수학 영어 점수를 insert함
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

# select는 GET 사용
# db에서 select로 가져온 데이터들(results)을
# ajax를 통해 html과 연동하여 클라이언트 화면에 이름과 점수를 보이게함
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

# 수정할 때는 PUT 사용
# 클라이언트에서 이름, 한국어, 수학, 영어 입력값을 받아와서 db update함
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

# 삭제는 DELETE
# 클라이언트에서 입력한 이름을 가져와서 db에서 입력한 이름만 삭제
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
