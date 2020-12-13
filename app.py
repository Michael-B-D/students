import requests
import json
from flask import Flask, render_template, request
from peewee import *


app = Flask(__name__, template_folder='template')

@app.route('/',methods = ['GET', 'POST'])
def get_results():
    if request.method == 'GET':
        stu = Students.select().first()
        if not stu:
            name = 'no users'
        else:
            name = stu.name
        return render_template(
                'base.html',
                student_name = name)
    if request.method == 'POST':
        data = request.form
        print(data)
        class_to_insert = data['student_class']
        pro_to_insert = data['student_profession']
        student_name = data['student_name']
        st_class = Classrooms.select().where(Classrooms.class_name == class_to_insert).get()
        st = Students.create(name=student_name, classroom_id=st_class.class_id)
        st_pro = Profession.select().where(Profession.profession == pro_to_insert).get()
        pro = Students_professions.create(student_id=st.student_id, profession_id=st_pro.profession_id)
        # stu = (Students.select()
        #         .join(Students_professions).join(Profession)
        #         .switch(Students)
        #         .join(Classrooms)
        #         .where(Students.student_id == st.student_id))
        res = {'name':st.name,
         'class':st_class.class_name,
          'profession':st_pro.profession}
        return render_template(
                'base.html',
                student_name=res['name'],
                student_class=res['class'],
                student_profession=res['profession']
                )


pg_db = SqliteDatabase('school.db')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = pg_db


class Classrooms(BaseModel):
    class_id = AutoField()
    class_name = CharField()


class Students(BaseModel):
    student_id = AutoField()
    name = CharField()
    classroom_id = ForeignKeyField(Classrooms, 'class_name')


class Profession(BaseModel):
    profession_id = AutoField()
    profession = CharField()


class Students_professions(BaseModel):
    student_id = ForeignKeyField(Students, 'name')
    profession_id = ForeignKeyField(Profession, 'profession')


with pg_db.connection_context():
    pg_db.create_tables([Students, Classrooms, Profession, Students_professions], safe=True)
    pg_db.close()


def insert_data():
    Profession.create(profession='Math')
    Classrooms.insert(class_name='A1').execute()

    
if __name__ == '__main__':
    insert_data()
    app.run(threaded=True, port=5000)
            