from flask import Flask, render_template
import util

app = Flask(__name__)

# Database credentials
username = 'raywu1990'
password = 'test'
host = '127.0.0.1'
port = '5432'
database = 'dvdrental'

@app.route('/')
def index():
	message = "Go to 127.0.0.1:5000/api/update_basket_a to update basket A"
	return message
	
@app.route('/api/update_basket_a')
def update_basket_a():
    cursor, connection = util.connect_to_db(username, password, host, port, database)
    if cursor == -1:
        return "Failed to connect to the database"
    
    try:
        util.run_and_fetch_sql(cursor, "INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry');")
        connection.commit()
        message = "Success! Go to 127.0.0.1:5000/api/unique to see your result"
    except Exception as e:
        message = f"Error: {e}"
    finally:
        util.disconnect_from_db(connection, cursor)
    
    return message

@app.route('/api/unique')
def unique_fruits():
    cursor, connection = util.connect_to_db(username, password, host, port, database)
    if cursor == -1:
        return "Failed to connect to the database"

    try:
        basket_a_fruits = util.run_and_fetch_sql(cursor, "SELECT DISTINCT fruit_a FROM basket_a;")
        basket_b_fruits = util.run_and_fetch_sql(cursor, "SELECT DISTINCT fruit_b FROM basket_b;")
        basket_a_fruits = [fruit[0] for fruit in basket_a_fruits]
        basket_b_fruits = [fruit[0] for fruit in basket_b_fruits]
        
        table_title = ["Unique Fruits in Basket A", "Unique Fruits in Basket B"]
        sql_table = list(zip(basket_a_fruits, basket_b_fruits))
    except Exception as e:
        return f"Error: {e}"
    finally:
        util.disconnect_from_db(connection, cursor)

    return render_template('index.html', sql_table=sql_table, table_title=table_title)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)

