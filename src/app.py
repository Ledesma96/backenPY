from flask import Flask, render_template, request, redirect
import os
import database as db
from flask_socketio import SocketIO, emit
from decimal import Decimal
import json

cursor = db.database.cursor(dictionary=True)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)  # Convertir Decimal a float
        return super().default(o)

template_dir=os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
tamplate_dir= os.path.join(template_dir, 'src', 'templates')
print('template_dir', template_dir)

app = Flask( __name__, template_folder=tamplate_dir)
socketio = SocketIO(app)

@app.route('/')
def home():
    cursor.execute('CREATE TABLE IF NOT EXISTS peliculas (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(50) NOT NULL, gender VARCHAR(50) NOT NULL, year YEAR NOT NULL, ratings DECIMAL(10, 2), price DECIMAL(10, 2))');

    cursor.execute('SELECT * FROM peliculas');
    result = cursor.fetchall();

    return render_template('/index.html', data = result);

@socketio.on('update')
def update_film(data):
    film_id = data['id']

    try:
        if 'price' in data and 'ratings' in data:
            price = Decimal(data['price'])
            ratings = Decimal(data['ratings'])

            cursor.execute('UPDATE peliculas SET price=%s, ratings=%s WHERE id=%s', (price, ratings, film_id))
            db.database.commit()
        
        elif 'price' in data:
            price = Decimal(data['price'])
            cursor.execute('UPDATE peliculas SET price=%s WHERE id=%s', (price, film_id))
            db.database.commit()
        
        elif 'ratings' in data:
            ratings = Decimal(data['ratings'])
            cursor.execute('UPDATE peliculas SET ratings=%s WHERE id=%s', (ratings, film_id))
            db.database.commit()

        
        cursor.execute('SELECT * FROM peliculas')
        films = cursor.fetchall() 
        
        emit('all-films', json.dumps({'data': films}, cls=DecimalEncoder), broadcast=True)
    
    except Exception as e:
        print(f"Error en update: {str(e)}")


# @app.route('/add-film', methods=['POST'])
# def add_film():
#     film_data = request.json
#     print('film_data', film_data)
    
#     # title = film_data.get('title');
#     # gender = film_data.get('gender');
#     # year = film_data.get('year');
#     # ratings = film_data.get('ratings');
#     # price = film_data.get('price');


#     # cursor.execute('INSERT INTO peliculas (title, gender, year, ratings, price) VALUES (%s, %s, %s, %s, %s)', (title, gender, year, ratings, price))
#     # db.database.commit()

#     return redirect('/')


@socketio.on('add-film')
def handle_add_film(film):
    try:
        title = film['title']
        gender = film['gender']
        year = film['year']
        ratings = film['ratings']
        price = film['price']

        cursor.execute('INSERT INTO peliculas (title, gender, year, ratings, price) VALUES (%s, %s, %s, %s, %s)', (title, gender, year, ratings, price))
        db.database.commit()

        cursor.execute('SELECT * FROM peliculas')
        films = cursor.fetchall()

        emit('all-films', json.dumps({'data': films}, cls=DecimalEncoder), broadcast=True)  # Emitir a todos los clientes conectados
    except Exception as e:
        print(f"Error en handle_add_film: {str(e)}")

@socketio.on('remove-film')
def handle_remove_film(data):
    try:
        film_id = int(data)
        cursor.execute('DELETE FROM peliculas WHERE id = %s', (film_id,))
        db.database.commit()

        cursor.execute('SELECT * FROM peliculas')
        films = cursor.fetchall()

        emit('all-films', json.dumps({'data': films}, cls=DecimalEncoder), broadcast=True) 
    except Exception as e:
        print(f"Error en handle_remove_film: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True, port = 4000)