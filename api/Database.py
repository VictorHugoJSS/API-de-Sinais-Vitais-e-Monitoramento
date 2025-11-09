import psycopg2
CONNECTION=f"postgres://vitalsapp:test@timescaledb/vitals"

conn = psycopg2.connect(CONNECTION)
cursor = conn.cursor()

def init_db():
    cursor.execute("""DROP TABLE IF EXISTS alerts,vitals,devices""")
    # cursor.execute("""DROP TABLE IF EXISTS devices""")
    # cursor.execute("""DROP TABLE IF EXISTS  vitals""")
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS alerts(
                       id serial,
                       alert_type TEXT NOT NULL,
                       message TEXT NOT NULL,
                       timestamp date
                   )
                   WITH(
                       tsdb.hypertable,
                       tsdb.partition_column='timestamp',
                       tsdb.segmentby = 'alert_type',
                       tsdb.orderby = 'timestamp DESC'
                   )
                   """)
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS devices(
                       id serial,
                       data TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                       Devicename TEXT NOT NULL,
                       Devicemodel TEXT,
                       type TEXT,
                       heart_rate INTEGER,
                       temperature DOUBLE PRECISION,
                       blood_pressure DOUBLE PRECISION,
                       respiratory_rate INTEGER
                   )
                   WITH(
                       tsdb.hypertable,
                       tsdb.partition_column ='data',
                       tsdb.segmentby = 'Devicename',
                       tsdb.orderby = 'data DESC'
                   )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS vitals(
                       id serial,
                       pacientName TEXT,
                       cpf TEXT PRIMARY KEY,
                       temperature DOUBLE PRECISION,
                       heart_rate INTEGER,
                       blood_pressure DOUBLE PRECISION,
                       respiratory_rate INTEGER,
                       Devicename TEXT
                   )
                   """)
    
    cursor.execute("""CALL add_columnstore_policy('devices', INTERVAL '1 days', if_not_exists => TRUE);""")
    cursor.execute("""CALL add_columnstore_policy('alerts', INTERVAL '1 days', if_not_exists => TRUE);""")
    conn.commit()