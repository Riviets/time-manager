import abc
import csv

class ItemsManager(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *args):
        pass

    @staticmethod
    def clear_list(lst):
        lst.clear()

    @staticmethod
    def fill_items(path, lst, ItemClass):
        lst.clear()
        with open(path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    item = ItemClass.from_row(row)
                    lst.append(item)

    @staticmethod
    def refresh_csv_file(path, lst):
        with open(path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for item in lst:
                writer.writerow(item.to_row())
    @staticmethod
    def number_of_items(csv_path):
        with open(csv_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            return sum(1 for _ in reader)