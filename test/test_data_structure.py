from data_structure.hash_table import HashTable
from data_structure.adjacency_list import AdjacencyList


def test_system():
    # 测试哈希表
    ht = HashTable()
    ht.insert("1", {"姓名": "张三"})
    assert ht.get("1")["姓名"] == "张三"

    # 测试邻接表
    al = AdjacencyList()
    al.add_edge("1", "2")
    assert "2" in al.get_neighbors("1")

    print("✅ 所有核心数据结构测试通过！")


if __name__ == "__main__":
    test_system()