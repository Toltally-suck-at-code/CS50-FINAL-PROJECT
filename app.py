from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_performance.db'
db = SQLAlchemy(app)

class StudyPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    subject = request.form.get('subject')
    rating = request.form.get('rating')
    new_performance = StudyPerformance(subject=subject, rating=rating)
    db.session.add(new_performance)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/weather', methods=['POST'])
def weather():
    city = request.json.get('city')  # Use request.json to get the city from the JSON body
    api_key = '32ead8811e93e081aee1b26ded2ed91a'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    print(f"Fetching weather for city: {city}")  # Debugging statement
    response = requests.get(url)  # This line uses the requests library
    
    if response.status_code == 200:
        data = response.json()
        print(f"API Response: {data}")  # Debugging statement to see the full response
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        return {'temperature': temperature, 'description': weather_description}
    else:
        print(f"Error fetching weather: {response.text}")  # Debugging statement for error
        return {'error': 'City not found'}, 404

@app.route('/past_performances')
def past_performances():
    performances = StudyPerformance.query.all()
    average_rating = db.session.query(db.func.avg(StudyPerformance.rating)).scalar()
    return render_template('past_performances.html', performances=performances, average_rating=average_rating)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)