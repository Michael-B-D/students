import requests
import json
from flask import Flask, render_template, request
from peewee import *


app = Flask(__name__, template_folder='template')

@app.route('/',methods = ['GET', 'POST', 'DELETE'])
def get_results():
    if request.method == 'GET':
        stu = Student.select().first()
        if not stu:
            name = 'no users'
        else:
            name = stu.name
        return render_template(
                'base.html',
                student_name = name)
    if request.method == 'POST':
        data = request.form
        st = Student.create(name=data['student_name'])
        print(data)
        stu = Student.select().where(Student.student_id == st.student_id).get()
        return render_template(
                'base.html',
                student_name=stu.name)

pg_db = SqliteDatabase('test.db')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = pg_db

class Student(BaseModel):
    student_id = AutoField()
    name = CharField()


with pg_db.connection_context():
    pg_db.create_tables([Student], safe=True)
    
    
if __name__ == '__main__':
    app.run(threaded=True, port=5000)
            