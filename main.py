# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import mercari
import yaml

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
    for searchTerm in config['keywords']:
        for item in mercari.search(searchTerm):
            print(item.productName)
            print("{}, {}".format(item.productName, item.productURL))

    print("Search ended.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
