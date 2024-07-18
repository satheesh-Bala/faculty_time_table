# app.py
from flask import Flask, render_template, redirect, url_for, request, session,flash
from config import Config
from models import db, User, Faculty,TimeSlot
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_initial_user():
    with app.app_context():
        if User.query.filter_by(username='admin').first() is None:
            admin = User(username='admin')
            admin.set_password('123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")

@app.route('/asign_periods', methods=['GET', 'POST'])
def asign_periods():
    if 'username' not in session:
        return redirect(url_for('login'))
    faculty_members = Faculty.query.all()
    return render_template('asign_periods.html',faculties=faculty_members)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username']=username
            return redirect(url_for('time_slots_by_date'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/faculty_list')
def faculty_list():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    faculty_members = Faculty.query.all()
    return render_template('faculty_list.html', faculty_members=faculty_members)

@app.route('/add_faculty', methods=['GET', 'POST'])
def add_faculty():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    current_username = session['username']
    if request.method == 'POST':
        name = request.form['name']
        designation=request.form["designation"]
        id_number = request.form['id_number']
        mail = request.form['mail']
        created_by = current_username
        print("current user name:", current_username)
        is_active = 1

        new_faculty = Faculty(
            name=name,
            designation=designation,
            id_number=id_number,
            mail=mail,
            created_by=created_by,
            is_active=is_active,
            created_on=datetime.utcnow()
        )

        db.session.add(new_faculty)
        db.session.commit()

        return redirect(url_for('faculty_list'))
    return render_template('add_faculty.html')

@app.route('/time_slots', methods=['GET', 'POST'])
def manage_time_slots():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        date = request.form['date']
        faculty_id = request.form['faculty_id']
        
        period_data = {
            'period_1': 1 if request.form.get('period_1') else 0,
            'period_2': 1 if request.form.get('period_2') else 0,
            'period_3': 1 if request.form.get('period_3') else 0,
            'period_4': 1 if request.form.get('period_4') else 0,
            'period_5': 1 if request.form.get('period_5') else 0,
            'period_6': 1 if request.form.get('period_6') else 0,
            'period_7': 1 if request.form.get('period_7') else 0,
            'period_8': 1 if request.form.get('period_8') else 0
        }
        
        new_time_slot = TimeSlot(
            date=date,
            faculty_id=faculty_id,
            **period_data
        )
        db.session.add(new_time_slot)
        db.session.commit()
        flash('Time slot added successfully')
        return redirect(url_for('time_slots_by_date'))
    

@app.route('/', methods=['GET'])
def time_slots_by_date():
    if 'username' not in session:
        return redirect(url_for('login'))

    selected_date = request.args.get('date')
    time_slots = None

    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        time_slots = TimeSlot.query.filter_by(date=selected_date).all()

        # Create default time slots for all faculty members if not already existing
        faculty_members = Faculty.query.all()
        for faculty in faculty_members:
            if not any(slot.faculty_id == faculty.id for slot in time_slots):
                new_time_slot = TimeSlot(
                    date=selected_date,
                    faculty_id=faculty.id,
                    period_1=0,
                    period_2=0,
                    period_3=0,
                    period_4=0,
                    period_5=0,
                    period_6=0,
                    period_7=0,
                    period_8=0
                )
                db.session.add(new_time_slot)
                db.session.commit()

        # Refresh time slots after adding default entries
        time_slots = TimeSlot.query.filter_by(date=selected_date).all()
        print(time_slots)
        print(time_slots[0].period_1)

    return render_template('index.html', time_slots=time_slots, selected_date=selected_date)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_initial_user()
    app.run(host='0.0.0.0', debug=True)
