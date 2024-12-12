from flask import Blueprint, render_template, request, redirect, url_for
from models import Employee, Hire
from datetime import datetime

# Blueprintの作成
employee_bp = Blueprint('employee', __name__, url_prefix='/employees')

@employee_bp.route('/')
def list():
    employees = Employee.select()
    return render_template('employee_list.html', title='従業員一覧', items=employees)

@employee_bp.route('/add', methods=['GET', 'POST'])
def add():
    print("ddddd")
    if request.method == 'POST':
        # Hireレコードを作成
        hire = Hire.create(
            hire_date=datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date(),
            job_title=request.form['job_title'],
            department_name=request.form['department_name'],
            employment_type=request.form['employment_type'],
            salary=int(request.form['salary']),
            status='Active'  # 初期ステータスはActive
        )

        # Employeeレコードを作成
        employee = Employee.create(
            hire_id=hire,  # hireオブジェクトを外部キーとして設定
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            gender=request.form['gender'],
            date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date(),
            email=request.form['email'],
            phone_number=request.form['phone_number'],
            address=request.form['address']
        )
        return redirect(url_for('employee.list'))
    return render_template('employee_add.html')

@employee_bp.route('/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    employee = Employee.get_or_none(Employee.employee_id == employee_id)
    if not employee:
        return redirect(url_for('employee.list'))

    if request.method == 'POST':
        # Hireレコードを更新
        hire = employee.hire_id
        hire.hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()
        # ... 他のHireフィールドも更新 ...
        hire.save()

        # Employeeレコードを更新
        employee.first_name = request.form['first_name']
        # ... 他のEmployeeフィールドも更新 ...
        employee.save()
        return redirect(url_for('employee.list'))

    return render_template('employee_edit.html', employee=employee)

@employee_bp.route('/delete/<int:employee_id>', methods=['GET', 'POST'])
def delete(employee_id):
    employee = Employee.get_or_none(Employee.employee_id == employee_id)
    if not employee:
        return redirect(url_for('employee.list'))

    if request.method == 'POST':
        hire = employee.hire_id
        employee.delete_instance()
        return redirect(url_for('employee.list'))

    return render_template('employee_delete.html', employee=employee)  # GETリクエストの場合は確認画面を表示