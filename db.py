import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="carwala"
)

mycursor = mydb.cursor()

query = """
CREATE TABLE IF NOT EXISTS cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    brandname VARCHAR(255), 
    carname VARCHAR(255),
    carlink TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
mycursor.execute(query)


def insert_car_data(data):
    mycursor = mydb.cursor()
    
    query = """
    INSERT INTO cars (
        brandname,
        carname,
        carlink
    ) VALUES (%s, %s, %s)
    """

    values = (
        data.get("brandname"),
        data.get("carname"),
        data.get("carlink")
    )

    mycursor.execute(query, values)
    mydb.commit()
    print("Data inserted successfully")

def fetch_all_cars():
    mycursor = mydb.cursor(dictionary=True)  # get result as dict
    
    query = "SELECT * FROM cars"
    mycursor.execute(query)
    
    result = mycursor.fetchall()
    return result

query = """
CREATE TABLE IF NOT EXISTS variants (
    id INT AUTO_INCREMENT PRIMARY KEY,

    carname VARCHAR(255),
    variantname VARCHAR(255),
    varianturl TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
mycursor.execute(query)

def insert_variants_data(fullVariantsObjectList):
    mycursor = mydb.cursor()

    query = """
    INSERT INTO variants (
        carname,
        variantname,
        varianturl
    ) VALUES (%s, %s, %s)
    """

    values = []

    for carname, variants in fullVariantsObjectList.items():
        for variantname, varianturl in variants.items():
            values.append((carname, variantname, varianturl))

    if values:
        mycursor.executemany(query, values)
        mydb.commit()
        print("Variants data inserted successfully")