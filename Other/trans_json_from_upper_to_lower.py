import json
import os


def convert_keys_to_lowercase(obj):
    if isinstance(obj, dict):
        return {k.lower(): convert_keys_to_lowercase(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_keys_to_lowercase(elem) for elem in obj]
    else:
        return obj


# 处理单个文件
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    converted_data = convert_keys_to_lowercase(data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(converted_data, file, indent=4, ensure_ascii=False)


# 处理目录中的所有JSON文件
def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            process_file(file_path)


# 使用示例
process_file('../TestData/UnitTest/20250120.json')