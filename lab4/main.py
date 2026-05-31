from src.Zoo import Zoo
from ZooMenu import ZooMenu
from src.ZooDataManager import ZooDataManager

def main():
    data_manager: ZooDataManager = ZooDataManager("zoo.json")
    zoo = data_manager.load()
    menu = ZooMenu(zoo)
    try:
        menu.run()
    finally:
        data_manager.save(zoo)

if __name__ == "__main__":
    main()