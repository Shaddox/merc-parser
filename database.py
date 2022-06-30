import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    # finally:
    # if conn:
    #     conn.close()


def get_cursor(connection):
    return connection.cursor()


def provision_db(conn, cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
    [id] INTEGER PRIMARY KEY,
    [mercariId] INTEGER,
    [keyword] TEXT,
    [name] TEXT,
    [productURL] TEXT,
    [imageURL] TEXT,
    [price] INTEGER,
    [status] TEXT,
    [soldOut] TEXT,
    [batchId] INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS latest_batch_ids(
    [id] INTEGER PRIMARY KEY,
    [keyword] TEXT,
    [batchId] INTEGER
    )
    ''')
    conn.commit()


def get_batch_id_for_keyword(connection, cursor, keyword):
    result = cursor.execute("SELECT batchId from latest_batch_ids WHERE keyword = :keyword",
                            {"keyword": keyword}).fetchone()
    print(result)
    if not result:
        result = 0
        cursor.execute('''
        INSERT INTO latest_batch_ids(keyword, batchId) VALUES (
        :keyword, :batchId )
        ''', {
            "keyword": keyword,
            "batchId": result
        })
    else:
        result = result[0]
        cursor.execute('''
        UPDATE latest_batch_ids SET
        batchId = :newBatchId
        WHERE batchId = :oldBatchId AND keyword = :keyword
        ''', {
            "newBatchId": result + 1,
            "oldBatchId": result,
            "keyword": keyword
        })
        result = result + 1
    connection.commit()
    print(result)
    return result


def insert_products(connection, cursor, keyword, products, batchId):
    for product in products:
        cursor.execute('''
        INSERT INTO products (mercariId, keyword, name, productURL, imageURL, price,status, soldOut, batchId) VALUES(
        :mercariId, :keyword, :name, :productURL, :imageURL, :price, :status, :soldOut, :batchId
        )
        ''', {
            "mercariId": product.id,
            "keyword": keyword,
            "name": product.productName,
            "productURL": product.productURL,
            "imageURL": product.imageURL,
            "price": product.price,
            "status": product.status,
            "soldOut": product.soldOut,
            "batchId": batchId
        })
    connection.commit()


def find_new_products_for_keyword(cursor, keyword, batchId):
    newProducts = cursor.execute('''
    SELECT mercariId, name, productURL, imageURL, price, status, soldOut FROM products p1 WHERE
    p1.keyword = :keyword AND p1.batchId = :currentBatchId
    EXCEPT
    SELECT mercariId, name, productURL, imageURL, price, status, soldOut FROM products p2 WHERE
    p2.keyword = :keyword and p2.batchId = :oldBatchId
    ''', {
        "keyword": keyword,
        "currentBatchId": batchId,
        "oldBatchId": batchId - 1
    }).fetchAll()

    return newProducts

def find_new_products_for_all_keywords(cursor):
    newProducts = cursor.execute('''
    SELECT mercariId, name, productURL, imageURL, price, status, soldOut FROM products p1 
    INNER JOIN latest_batch_ids b1 ON 
    (p1.batchId = b1.batchId and p1.keyword = b1.keyword)
    WHERE b1.batchId != 0 
    ''').fetchAll()
    return newProducts