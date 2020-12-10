import requests
import json
from flask import Flask, render_template, request
from peewee import *


url = "https://rapidapi.p.rapidapi.com/v1/search"

headers = {
    'x-rapidapi-host': "newscatcher.p.rapidapi.com",
    'x-rapidapi-key': "d6206439ddmsh11ea8fcac12d762p19a85bjsncff8122bfe9c"
    }
    
app = Flask(__name__, static_folder="Templates", static_url_path="")

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



# pg_db = PostgresqlDatabase('myschool', user='postgres', password='mhbd1996',
#                            host='localhost', port=5432)
pg_db = SqliteDatabase('test.db')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = pg_db

class Student(BaseModel):
    student_id = AutoField()
    name = CharField()
    # classname = 
    # family_status_id = ForeignKeyField(Family_status, 'Students')
    # economic_status_id = ForeignKeyField(Economic_status, 'Students')

with pg_db.connection_context():
    pg_db.create_tables([Student], safe=True)
    


# class Family_status(Model):
#     family_status_id = AutoField()
#     status = CharField()


# class Economic_status(Model):
#     economic_status_id = AutoField()
#     status = CharField()


# class Classroom(Model):
#     class_id = AutoField()
#     name = CharField()


# class Profession(Model):
#     profession_id = AutoField()
#     name = CharField()


# class Student_professions(Model):
#     student_id = ForeignKeyField(Student, 'Students_professions')
#     profession_id = ForeignKeyField(Profession, 'Students_professions')


class Meta:
        database = pg_db


    # free_text = request.args.get('free_search')
    # if not free_text:
    #     free_text = request.args.get('optional_free_text')
    #     if not free_text:
    #         return render_template('index.html')
    # country = request.args.get('country_search')
    # time_from = request.args.get('time_form_search')
    # time_to = request.args.get('time_to_search')
    # sort_by = request.args.get('sortby_search')
    # page = request.args.get('page')
    # filter_results = {}
    # all_articles = []
    # if not page:
    #     page = 1
    # else:
    #     page = str(page)
    # querystring = {"q":free_text, "media":"True", "country":country, "from":time_from, "to":time_to, "page":page}
    # print('query',querystring)
    # response = requests.request("GET", url, headers=headers, params=querystring)
    # print('COntent:',response.text)
    # res = json.loads(response.text)
    # if res['status'] == 'ok':
    #     print('WORK', response.status_code, response.text)
    #     filter_keys = ['total_hits', 'page', 'total_pages']
    #     filter_results = {key: value for key, value in res.items() if key in filter_keys}
    #     filter_results['page'] = int(filter_results['page'])
    #     filter_keys_article = ['title', 'link', 'media', 'clean_url', 'published_date']
    #     for article in res['articles']:
    #         try:     
    #             if article['media'] == None:
    #                 article['media'] = 'images/newspaper-regular.svg'
    #         except KeyError as e:
    #             print(e)
    #             article['media'] = 'images/newspaper-regular.svg'
    #             all_articles.append({key: value for key, value in article.items() if key in filter_keys_article})
    #             continue
    #         all_articles.append({key: value for key, value in article.items() if key in filter_keys_article})
    #     return render_template(
    #         'results_page.html',
    #         filter_results=filter_results,
    #         all_articles=all_articles,
    #         status=res['status'],
    #         current_url=request.url,
    #     )
    # else:
    #     print('dont work', response.status_code)
    #     return render_template(
    #         'week14\Templates\base.html',
    #         status=res['status']
    #         )
    #         # if key error puse the relvant keys to the res
            
if __name__ == '__main__':
    app.run(threaded=True, port=5000)
            

            # <!-- <p class="all-hits">Total {{filter_results["total_hits"]}} Results:</p> -->
        # <!-- <p class="page-num">This page number-{{filter_results['page']}} from-{{filter_results["total_pages"]}}, click <a href="?free_text={{free_text}}&page={{filter_results['page']+1}}">here</a> to the next page!</p> -->
