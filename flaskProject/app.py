from flask import Flask, render_template, send_file
from flasgger import Swagger

from charts import get_city_image, get_main_image
from user_database import data

app = Flask(__name__)
swagger = Swagger(app)


def get_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'


@app.route('/')
def main():
    """
    Entry point; the view for the main page
    ---
    tags:
      - Main
    description: The main page of the application
    responses:
      200:
        description: A successful response
    """
    cities = [(record.city_id, record.city_name) for record in data]
    return render_template('main.html', cities=cities)


@app.route('/main.png')
def main_plot():
    """
    The view for rendering the scatter chart
    ---
    tags:
      - Main
    description: Render the scatter chart for the main page
    responses:
      200:
        description: A successful response
    """
    img = get_main_image()
    response = send_file(img, mimetype='image/png')
    get_headers(response)
    return response


@app.route('/city/<int:city_id>')
def city(city_id):
    """
    Views for the city details
    ---
    tags:
      - City
    parameters:
      - name: city_id
        in: path
        description: ID of the city
        required: true
        type: integer
    responses:
      200:
        description: A successful response
    """
    city_record = data.get(city_id)
    return render_template('city.html', city_name=city_record.city_name, city_id=city_id,
                           city_climate=city_record.city_climate)


@app.route('/city<int:city_id>.png')
def city_plot(city_id):
    """
    Views for rendering city-specific charts
    ---
    tags:
      - City
    parameters:
      - name: city_id
        in: path
        description: ID of the city
        required: true
        type: integer
    responses:
      200:
        description: A successful response
    """
    img = get_city_image(city_id)
    response = send_file(img, mimetype='image/png')
    get_headers(response)
    return response
