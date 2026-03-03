import csv

class DataReader:
    @staticmethod
    def load_users(file_path, hash_table):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                hash_table.insert(row['用户ID'], row)

    @staticmethod
    def load_relations(file_path, adj_list):
        with open(file_path, 'r', encoding='utf-8') as f:
            next(f) # 跳过表头
            for line in f:
                u, v = line.strip().split(',')
                adj_list.add_edge(u, v)