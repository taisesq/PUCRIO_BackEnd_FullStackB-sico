from flask import Flask, request, jsonify
import sqlite3
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Product Types"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

#app.run()
# Now point your browser to localhost:5000/api/docs/
#http://localhost:5000/api/docs/#/
#Fim da documentação Swegger


#API COMEÇA AQUI

# SQLite database setup
DATABASE = 'store.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Create operation
@app.route('/product_types', methods=['POST'])
def create_product_type():
    try:
        name = request.json['name']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO product_types (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product type created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Read All operation
@app.route('/get_all', methods=['GET'])
def get_all():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM product_types')
        product_types = cursor.fetchall()
        conn.close()
        return jsonify({'product_types': product_types})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Read One operation
@app.route('/get_all/<int:type_id>', methods=['GET'])
def get_one_product_type(type_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM product_types WHERE id=?', (type_id,))
        product_type = cursor.fetchone()
        conn.close()
        
        if product_type:
            return jsonify({'product_type': product_type})
        else:
            return jsonify({'message': 'Product type not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update operation
@app.route('/product_types/<int:type_id>', methods=['PUT'])
def update_product_type(type_id):
    try:
        new_name = request.json['name']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE product_types SET name=? WHERE id=?', (new_name, type_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product type updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Delete operation
@app.route('/product_types/<int:type_id>', methods=['DELETE'])
def delete_product_type(type_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM product_types WHERE id=?', (type_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product type deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    create_table()
    app.run(host="0.0.0.0",port=80800,debug=True)    
