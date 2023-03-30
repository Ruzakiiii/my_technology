import psycopg2
from config import *

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

except:
    print("[INFO] Error while working with PostgreSQL",)

class DataBase():

    def INSERT(Table, Column, Value):

        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {Table} ({','.join(Column)}) VALUES('{"','".join(Value)}');""")


    def SELECT(Object, Table, WHERE_Object=None, WHERE_Object_two=None):

         try:
             with connection.cursor() as cursor:
                 cursor.execute(
                     f"""SELECT {Object} FROM {Table} WHERE {WHERE_Object}={WHERE_Object_two};"""
                 )
                 a = [i for i in cursor]
                 return a

         except:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT {Object} FROM {Table} ;"""
                )
                a = [i for i in cursor]
                return a


    def DELETE(Table, WHERE_Object=None, WHERE_Object_two=None):

         try:

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""DELETE FROM {Table} WHERE {WHERE_Object}={WHERE_Object_two};"""
                )
         except:

             with connection.cursor() as cursor:
                 cursor.execute(
                     f"""DELETE FROM {Table};"""
                 )


    def UPDATE(Table, Object, Object_two, WHERE_Object=None, WHERE_Object_two=None):

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""UPDATE {Table} SET {Object}='{Object_two}' WHERE {WHERE_Object}={WHERE_Object_two};"""
                )
        except:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""UPDATE {Table} SET {Object}='{Object_two}';"""
                )


    def CREATE(Table, Column_and_Value):

        with connection.cursor() as cursor:
            cursor.execute(
               f"""CREATE TABLE {Table} ({', '.join(Column_and_Value)});"""
            )


    def DROP(Table):

        with connection.cursor() as cursor:
            cursor.execute(
               f"""DROP TABLE {Table};"""
            )

