import sqlite3
from os.path import isfile

def connect_db(): 
    pass

def create_database_notas(connection, cursor): 
    pass

def add_record(connection, cursor, um_registo): 
    pass

def add_several_records(connection, cursor, varios_registos): 
    pass

def print_table_notas(connection, cursor): 
    pass

def print_table_notas_one_record(connection, cursor): 
    pass

def print_table_notas_size_record(connection, cursor, size = 2): 
    pass


um_registo = (123, '2021/2022', 'AD', 20)
varios_registos=[ (1000,'2021/2022','AD',10),
(1000,'2021/2022','ITW',10),
(1001,'2021/2022','AD',17),
(1000,'2021/2022','ITW',17)]

if __name__ == '__main__':
    conn, cursor = connect_db()
    add_record(conn, cursor, um_registo)
    add_several_records(conn, cursor, varios_registos)
    print_table_notas(conn, cursor)
    print_table_notas_one_record(conn, cursor)  
    print_table_notas_size_record(conn, cursor)
    conn.close()