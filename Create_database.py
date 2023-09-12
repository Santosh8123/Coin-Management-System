import mysql.connector

if(__name__ == "__main__"):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pass1234")
    
    sql = 'create database Information_of_Coins';
    cursor = mydb.cursor()
    cursor.execute(sql)
    mydb.close()