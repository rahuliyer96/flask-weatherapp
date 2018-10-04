from flask import Flask, render_template,request
import requests
from flask_sqlalchemy import SQLAlchemy
import pprint

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        new_city=request.form.get('city')
        if new_city:
            db.session.add(City(name=new_city))
            db.session.commit()

    cities =  City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=05560cf3177657c1ed0d4c154212db40'
    weather_data=[]
    for city in cities:
        r=requests.get(url.format(city.name)).json()
        weather = {
            'city':city.name,
            'temperature':r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon':r['weather'][0]['icon']
        }
        weather_data.append(weather)
        print(weather)

    return render_template('weather.html',weather_data=weather_data)

if __name__=="__main__":
    app.run(debug=True)