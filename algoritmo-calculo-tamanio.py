# -*- coding: utf-8 -*-
"""
@Institución: IU Pascual Bravo
@Docente    : Jaime E Soto U
@asignatura : ET0155 -Fundamentos de BigData
@Tarea      : Tarea Unidad 2 - Ítem 10
"""
import time
import sys
import random
import psycopg2
from psycopg2 import Error

# Variables globales
error_con = False

# Parámetros de conexión de la Base de datos local
v_host     = "localhost"
v_port     = "5432"
v_database = "bigdata_etl"
v_user     = "postgres"
v_password = "admin"

def cargarOperaciones(conn, cur, reg, dep, mun, prod, fec, cant):
    try:
        command = '''INSERT INTO tamanio (id_registro, 
                                        id_departamento, id_municipio, id_producto, 
                                        fecha, cantidad, estado) 
                     VALUES (%s,%s,%s,%s,%s,%s,%s);'''
        cur.execute(command, (reg, dep, mun, prod, fec, cant, 'V'))
        conn.commit()
    except (Exception, Error) as error:
        print("Error en carga de operaciones: ", error)
        sys.exit("Error: Carga Operaciones!")

# CONEXIÓN A LA BASE DE DATOS
try:
    connection = psycopg2.connect(user=v_user, password=v_password, host=v_host,
                                  port=v_port, database=v_database)
    cursor = connection.cursor()
    
    print("PostgreSQL Información del Servidor")
    print("Conectado a la base de datos:", v_database, "\n")
    
    # LIMPIEZA DE TABLA
    command = '''TRUNCATE tamanio;'''
    cursor.execute(command)    
    connection.commit()    
except (Exception, Error) as error:
    print("Error de conexión: ", error)
    error_con = True
finally:
    if (error_con):            
        sys.exit("Error de conexión con servidor PostgreSQL")


# GENERACIÓN ALEATORIA DE OPERACIONES DE VENTAS
try:
    # -------------------------------------------------------------------------
    registros = 10000
    # -------------------------------------------------------------------------

    print(f"Iniciando procesamiento de {registros:,} registros...")

    # 1. TIEMPO INICIO
    tiempo_inicio = time.time()

    # Pre-cargar municipios en memoria para optimizar velocidad del bucle
    cursor.execute("SELECT id_departamento, id_municipio FROM municipios;")
    lista_municipios = cursor.fetchall()

    for iteracion in range(1, registros + 1):
        id_producto = random.randint(1, 4)                    
        cantidad = random.randint(1, 5000)            
        
        dia   = str(random.randint(1, 28)).zfill(2)
        mes   = str(random.randint(1, 12)).zfill(2)
        fecha = f"{dia}-{mes}-2023"

        # Selección aleatoria de municipio desde la lista en memoria
        mun_selected = random.choice(lista_municipios)
        id_departamento = mun_selected[0]
        id_municipio    = mun_selected[1]
        
        cargarOperaciones(connection, cursor, iteracion, id_departamento, 
                          id_municipio, id_producto, fecha, cantidad)

    # 2. TIEMPO FINAL Y CÁLCULO EN MILISEGUNDOS
    tiempo_final = time.time()
    tiempo_procesamiento_ms = (tiempo_final - tiempo_inicio) * 1000

    print("\n--------------------------------------------------")
    print(f"Carga finalizada con éxito.")
    print(f"TIEMPO DE PROCESAMIENTO: {tiempo_procesamiento_ms:.2f} ms")
    print("--------------------------------------------------\n")

    # TAMAÑO EN KILOBYTES DE LA TABLA  Y BD
    cursor.execute("SELECT ROUND(pg_total_relation_size('tamanio') / 1024.0, 2);")
    tam_tabla_kb = float(cursor.fetchone()[0])

    cursor.execute(f"SELECT ROUND(pg_database_size('{v_database}') / 1024.0, 2);")
    tam_bd_kb = float(cursor.fetchone()[0])

    porcentaje = round((tam_tabla_kb / tam_bd_kb) * 100, 4)

    print(f"Tamaño tabla 'tamanio': {tam_tabla_kb:.2f} KB")
    print(f"Tamaño Base de Datos '{v_database}': {tam_bd_kb:.2f} KB ({round(tam_bd_kb/1024.0, 2)} MB)")
    print(f"Porcentaje de almacenamiento: {porcentaje:.4f} %")

    connection.commit()
except (Exception, Error) as error:
    print("Error de procesamiento:", error)
    sys.exit("Error en la generación de datos")
finally:
    if (connection):
        connection.close()
        print("\nConexión PostgreSQL cerrada")    
        
print("Fin del proceso")