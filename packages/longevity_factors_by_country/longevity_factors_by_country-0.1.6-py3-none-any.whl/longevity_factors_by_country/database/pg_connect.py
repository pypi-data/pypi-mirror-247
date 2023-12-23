import psycopg2
import database.config as creds

# def connect():
    
#     # Set up a connection to the postgres server.
#     conn_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
#                   +" password="+ creds.PGPASSWORD
    
#     conn = psycopg2.connect(conn_string)
#     print("Connected!")

#     # Create a cursor object
#     cursor = conn.cursor()
    
#     return conn, cursor
    
def connect():
    engine = psycopg2.connect(
                     host = creds.PGHOST,
                     database = creds.PGDATABASE,
                     user = creds.PGUSER,
                     password = creds.PGPASSWORD,
                     port = "5432" )
    print(engine)
    return engine, engine.cursor()

def disconnect(engine):
    engine.close()
