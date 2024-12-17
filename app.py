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
@app.route('/',methods=['GET', 'POST'])
def index():
    query = (Employee
             .select(Employee.age, fn.AVG(Employee.salary).alias('average_salary'))
             .group_by(Employee.age))
    data = [{"age_labels": result.age, "avg_salary_data": result.average_salary} for result in query]

    if request.method == 'POST':
        data = request.json  
        if not data:
            return ({"error": "JSONデータがありません"})
    else:
        return render_template('index.html',data=data)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
