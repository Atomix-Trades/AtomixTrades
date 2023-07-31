from flask import Flask, render_template, request
import mysql.connector
import ccxt
import subprocess

app = Flask(__name__)

# MySQL connection details
db_host = 'localhost'
db_database = 'form'
db_user = 'root'  # Update with your MySQL username
db_password = ''  # Update with your MySQL password

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
            email = request.form.get('email')
            exchange_id = request.form.get('exchange_id')
            api_key = request.form.get('api_key')
            secret = request.form.get('secret')
            password = request.form.get('password')
            asset_name = request.form.get('asset_name')
            trade_type = request.form.get('trade_type')
            trade_size = float(request.form.get('trade_size'))
            timeframe = request.form.get('timeframe')
            indicator = request.form.get('indicator')

            # Check if the selected exchange ID is valid
            if not exchange_id or exchange_id not in ccxt.exchanges:
                return "Please select a valid exchange"

            # Connect to the MySQL database
            db_connection = mysql.connector.connect(
                host=db_host,
                database=db_database,
                user='root',
                password=''
            )

            # Create a cursor to execute SQL queries
            db_cursor = db_connection.cursor()

            # Check if the user already exists in the table
            select_query = "SELECT id, email FROM newusers WHERE email = %s"
            db_cursor.execute(select_query, (email,))
            existing_user = db_cursor.fetchone()

            if existing_user:
                # Update the user's information in the database
                user_id = existing_user[0]
                if email != existing_user[1]:
                    # Insert a new user into the table if the email is different
                    insert_query = "INSERT INTO newusers (email, exchange_id, api_key, secret, password_app, asset_name, trade_type, trade_size, timeframe, indicator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    insert_values = (email, exchange_id, api_key, secret, password, asset_name, trade_type, trade_size, timeframe, indicator)
                    db_cursor.execute(insert_query, insert_values)
                else:
                    # Update the user's information if the email is the same
                    update_query = "UPDATE newusers SET exchange_id=%s, api_key=%s, secret=%s, password_app=%s, asset_name=%s, trade_type=%s, trade_size=%s, timeframe=%s, indicator=%s WHERE id=%s"
                    update_values = (exchange_id, api_key, secret, password, asset_name, trade_type, trade_size, timeframe, indicator, user_id)
                    db_cursor.execute(update_query, update_values)
            else:
                # Insert a new user into the table if the email does not exist
                insert_query = "INSERT INTO newusers (email, exchange_id, api_key, secret, password_app, asset_name, trade_type, trade_size, timeframe, indicator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                insert_values = (email, exchange_id, api_key, secret, password, asset_name, trade_type, trade_size, timeframe, indicator)
                db_cursor.execute(insert_query, insert_values)

            # Commit the changes to the database
            db_connection.commit()

            # Close the cursor and database connection
            db_cursor.close()
            db_connection.close()

            # Run bot.py
            subprocess.run(["python", "bot.py"])

            return "Information saved successfully, Bot will start"
        # except Exception as e:
        #     app.logger.error("Error occurred while saving information: {}".format(str(e)))
        #     return "Error occurred while saving information"

    # Fetch supported exchange IDs from ccxt
    exchanges = ccxt.exchanges

    return render_template('configure.html', exchanges=exchanges)

if __name__ == '__main__':
    app.run(debug=True)
