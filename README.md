# CS50-FINAL-PROJECT
CS50 project, I've decided to upload it here for everyone if anyone wants to get some ideas and stuff.  


# STBYApp

#### Video Demo: [https://youtu.be/oMf8_DEmZhg](https://youtu.be/oMf8_DEmZhg)

## Description

This Flask-based web application offers a versatile standby mode interface, featuring a clock for displaying the current time, which helps users keep track of their study sessions. It provides real-time weather updates to keep users informed about their environment and a study performance tracking feature that allows users to monitor their study habits and productivity. The built-in timer can also be utilized for various tasks, such as timing study sessions or breaks. Together, these functionalities create a user-friendly interface that enhances daily activities and productivity.

## Project Files and Their Functions

This application is a Flask-based web service that provides a standby mode interface with various features including a clock, weather information, study performance tracking, and a timer. 

### Flask Application (app.py)

1. **Setup and Configuration**

   ```python
   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_performance.db'
   db = SQLAlchemy(app)
   ```

   This section initializes the Flask application and configures SQLAlchemy to use a SQLite database. SQLite is an excellent choice for me to use on small to medium-sized applications due to the ease of implementing it and how simple it is.

2. **Data Model**

   ```python
   class StudyPerformance(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       subject = db.Column(db.String(100), nullable=False)
       rating = db.Column(db.Integer, nullable=False)
   ```

   This defines the structure for storing study performance data. Using SQLAlchemy's ORM (Object-Relational Mapping) provides a clean, Pythonic interface for database operations and abstracts away the underlying SQL.

3. **Route Handlers**

   - **Index Route:**

     ```python
     @app.route('/')
     def index():
         return render_template('index.html')
     ```

     This renders the main page of the application. Using Flask's `render_template` function allows for dynamic content generation in HTML files.

   - **Submit Rating Route:**

     ```python
     @app.route('/submit_rating', methods=['POST'])
     def submit_rating():
         subject = request.form.get('subject')
         rating = request.form.get('rating')
         new_performance = StudyPerformance(subject=subject, rating=rating)
         db.session.add(new_performance)
         db.session.commit()
         return redirect(url_for('index'))
     ```

     This handler processes the submission of performance ratings. It demonstrates proper form handling, database interaction, and the use of redirects for better user experience.

   - **Weather Route:**

     ```python
     @app.route('/weather', methods=['POST'])
     def weather():
         city = request.json.get('city')
         api_key = '32ead8811e93e081aee1b26ded2ed91a'
         url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
         
         response = requests.get(url)
         
         if response.status_code == 200:
             data = response.json()
             temperature = data['main']['temp']
             weather_description = data['weather'][0]['description']
             return {'temperature': temperature, 'description': weather_description}
         else:
             return {'error': 'City not found'}, 404
     ```

     This route integrates with the OpenWeatherMap API to fetch real-time weather data. I demonstrated my ability to handle external API calls, process JSON responses, and return appropriate data or error messages.

   - **Past Performances Route:**

     ```python
     @app.route('/past_performances')
     def past_performances():
         performances = StudyPerformance.query.all()
         average_rating = db.session.query(db.func.avg(StudyPerformance.rating)).scalar()
         return render_template('past_performances.html', performances=performances, average_rating=average_rating)
     ```

     This route retrieves all past performances and calculates the average rating, demonstrating efficient use of SQLAlchemy for database queries and aggregations.

### HTML Templates

#### index.html

The main page template includes several key features:

1. Clock and Date Display: Uses JavaScript to update time and date in real-time.
2. Weather Section: Allows users to fetch weather information for a specific city.
3. Study Performance Rating: Enables users to submit study performance ratings.
4. Timer: Implements a countdown timer with start, pause, and reset functionality.
5. Color Customization: Allows users to customize the application's color scheme.

We wanted to make good use of CSS variables for theming and JavaScript for dynamic functionality. The modular structure with separate sections helps me to debug any functions easily, and add new features to each function easier.

#### past_performances.html

This template displays the history of study performance ratings and includes:

1. Theme Toggle: Allows switching between light and dark themes.
2. Color Picker: Enables customization of the primary color.
3. Performance Table: Displays past study performances in a structured format.

We have used CSS variables and JavaScript for theme switching, we wanted to demonstrate good practices for creating a user interface that is very flexible and user-customizable.

## Overall Architecture and Design Choices

1. **MVC Pattern**: Our Application follows a Model-View-Controller pattern, separating data (StudyPerformance model), presentation (HTML templates), and logic (Flask routes).
2. **RESTful API Design**: We use appropriate HTTP methods (GET, POST) for different operations that align with RESTful principles.
3. **Template Engine**: We use Jinja2 templating to allow dynamic content generation and code reuse in HTML files which makes it easier for us to improve the UI interface.
4. **External API Integration**: We use the weather functionality to demonstrate how to integrate external services by API's, this helps to enhance the application features.
5. **Database Abstraction**: We choose SQLAlchemy because it provides a powerful ORM, allowing for database-agnostic code and simplifying data operations, which makes it easier for us to create databases, lighter to run.
6. **Frontend Interactivity**: We extensively use JS Script and HTML templates, this creates a responsive and dynamic UI interface for the user.
7. **Customization Options**: We gave the User the ability to change themes and customize the website, this allows us to enhance the user experience and accessibility.
8. **Modular Design**: We separated functions and sections of code between routes and templates, this allows for a easier maintenance, debugging code and scalability

Our application goal is to provide an example of a full-stack web application, integrating frontend technologies with a Python backend, database management, and external API integration. The design choices we made facilitate maintainability, scalability, and debugging and a good user experience.

## Design Decisions

- **User Interface Simplicity**: We really wanted to keep things clean and intuitive. By making features like the clock and timer easily accessible, we aimed to help users focus on their studies without unnecessary distractions.

- **Horizontal Layout**: We chose a horizontal layout for the interface because it allows users to view multiple features at a glance. This design not only enhances usability but also creates a more organized and visually appealing experience. It helps users seamlessly switch between the clock, weather updates, and study tracking without feeling overwhelmed.

- **Color Customization**: We introduced a feature that allows users to customize the app's colors. Everyone has different preferences, and letting users choose their color scheme adds a personal touch that can make the app feel more inviting and enjoyable to use.

- **Performance Tracking**: We included a study performance tracking feature to motivate users to reflect on their habits, helping them stay accountable and boost their productivity.

- **Timer Functionality**: The built-in timer was designed with flexibility in mind, catering to various study techniques like the Pomodoro Technique.


