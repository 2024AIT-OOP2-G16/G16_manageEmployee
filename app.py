from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from models import Employee
from peewee import fn

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    
    query = (Employee
             .select(Employee.age, fn.AVG(Employee.salary).alias('average_salary'))
             .group_by(Employee.age))
    data = [{"age": result.age, "average_salary": result.average_salary} for result in query]
    for i in data:
        print(i)
    return render_template('index.html',data)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
