from flask import Flask, render_template, request
from models import initialize_database
from routes import blueprints

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.json  
        if not data:
            return ({"error": "JSONデータがありません"})
    else:
        # テスト段階では固定データを使用
        data = {
            "age_labels": [20, 30, 40, 50],
            "avg_salary_data": [30,35,40,45],
            "male_female_ratio": [61, 39]
        }
    return render_template('index.html',data=data)

@app.route('/graph')
def chart_do():
    # data = request.json //本番環境ではこれを使う
    #テスト段階ではこちらを使う
    data = {
        'age_labels': [18, 25, 27, 29, 31],
        'avg_salary_data': [34, 45, 50, 52, 55]
    }
    return render_template('graph.html', data=data)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
