# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import time

import mercari
import yaml

import database
import email_manager
import html_logger


def config_read():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config = config_read()
    print(config)
    dbConnection = database.create_connection(config['database_name'])
    dbCursor = database.get_cursor(dbConnection)
    database.provision_db(dbConnection, dbCursor)

    while True:
        print("Iteration starting...")
        breakBetweenKeywords = random.randint(config['timeouts']['lower_bound_keyword_search'],
                                              config['timeouts']['upper_bound_keyword_search'])
        for keyword in config['keywords']:
            print(keyword)
            currentBatchId = database.get_batch_id_for_keyword(dbConnection, dbCursor, keyword)
            try:
                productsForKeyword = mercari.search(keyword)
                database.insert_products(dbConnection, dbCursor, keyword, productsForKeyword, currentBatchId)
            except BaseException as e:
                print(e)
                print("Error with keyword " + keyword)
                print("Reverting batch ID...")
                database.revert_batchId_for_keyword(dbConnection, dbCursor, keyword, currentBatchId)
                time.sleep(breakBetweenKeywords)
                # Start over on the next keyword ...
                continue

            time.sleep(breakBetweenKeywords)

        allNewProducts = database.find_new_products_for_all_keywords(dbCursor)
        print(allNewProducts)
        if config["email"]['want'] and allNewProducts:
            email_manager.build_and_send_email_with_new_stuff(config['email'], allNewProducts)
        if config["logs"]["want"] and allNewProducts:
            html_logger.create_html_log(allNewProducts, config["logs"]["path"])
        print("Iteration ended")
        breakBetweenIterations = random.randint(config['timeouts']['lower_bound_search'],
                                                config['timeouts']['upper_bound_search'])
        time.sleep(breakBetweenIterations)
