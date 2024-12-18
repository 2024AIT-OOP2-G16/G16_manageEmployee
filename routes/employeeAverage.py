from peewee import fn
from models.employee import Employee
from models.hire import Hire

def main():
    # 年齢と平均給与を計算するクエリ
    query = (
        Employee
        .select(
            (fn.strftime('%Y', 'now') - fn.strftime('%Y', Employee.date_of_birth)).alias('age'),
            fn.AVG(Hire.salary).alias('averagesalary')
        )
        .join(Hire)
        .group_by(fn.strftime('%Y', 'now') - fn.strftime('%Y', Employee.date_of_birth))
        .order_by(fn.strftime('%Y', 'now') - fn.strftime('%Y', Employee.date_of_birth))  # 年齢順に並べる
    )

    # 結果を出力
    print("年齢別平均給与:")
    for result in query:
        print(f"年齢: {result.age}, 平均給与: {result.average_salary}")

if __name__ == '__main__':
    main()
