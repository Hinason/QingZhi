import json
import shutil
from pathlib import Path


def replace_position_ids(data):
    # 创建id到positionname的映射字典
    id_map = {}
    for assay in data.get("assaysmodel", []):
        for position in assay.get("positions", []):
            pos_id = position.get("id", "")
            pos_name = position.get("positionname", "")
            if pos_id:
                id_map[pos_id] = f"{pos_id} {pos_name}"

    # 递归遍历和替换所有字符串
    def process_value(item):
        if isinstance(item, dict):
            return {k: process_value(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [process_value(elem) for elem in item]
        elif isinstance(item, str):
            return id_map.get(item, item)
        return item

    return process_value(data)


def process_file(file_path):
    # 读取和处理数据
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    modified_data = replace_position_ids(data)

    # 写回原文件
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(modified_data, f, indent=2, ensure_ascii=False)

    print(f"处理完成")


# 示例使用
if __name__ == "__main__":
    target_file = "D:\\code\\Python\\QingZhi\\TestData\\UnitTest\\20250120.json"  # 替换为你的文件路径
    process_file(target_file)