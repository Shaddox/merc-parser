# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import mercari
import yaml

import database


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def config_read():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    config = config_read()
    print(config)
    dbConnection = database.create_connection(config['database_name'])
    dbCursor = database.get_cursor(dbConnection)
    database.provision_db(dbConnection, dbCursor)
    for keyword in config['keywords']:
        print(keyword)
        currentBatchId = database.get_batch_id_for_keyword(dbConnection, dbCursor, keyword)
        productsForKeyword = mercari.search(keyword)
        database.insert_products(dbConnection, dbCursor, keyword, productsForKeyword, currentBatchId)


        # for item in mercari.search(searchTerm):
        #     print(vars(item))
        #     print(item.productName)
        #     print("{}, {}".format(item.productName, item.productURL))
        #     break

    print("Search ended.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
