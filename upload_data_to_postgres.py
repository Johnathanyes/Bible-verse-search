import psycopg2

connect = psycopg2.connect("dbname=VerseLookup user=postgres password=Johnpost12!1@")
cursor = connect.cursor()

with open("data/NIV_bible.sql", "r", encoding="utf-8") as file:
    sql = file.read()
cursor.execute(sql)

connect.commit()
cursor.close()
connect.close()
print("all done")