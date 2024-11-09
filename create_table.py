import psycopg2

# Verbindung zur PostgreSQL-Datenbank herstellen
connection = psycopg2.connect(
    host="127.0.0.1",
    database="loadtest_db",
    user="admin",
    password="admin",
    port="54948"  # Falls ein anderer Port verwendet wird, hier anpassen
)

# Cursor-Objekt erstellen
cursor = connection.cursor()

# SQL-Befehl zum Erstellen der Tabelle
create_table_query = '''
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
'''

# SQL-Befehl ausführen und Änderungen speichern
cursor.execute(create_table_query)
connection.commit()

# Verbindung schließen
cursor.close()
connection.close()

print("Tabelle 'products' wurde erfolgreich erstellt.")
