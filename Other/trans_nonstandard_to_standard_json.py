import json


def format_json_file(input_file, output_file=None, indent=4):
    try:
        # 读取原始JSON文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 决定输出文件名
        if output_file is None:
            output_file = input_file.replace('.json', '_formatted.json')

        # 写入格式化后的JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

        print(f"格式化完成！结果已保存至: {output_file}")

    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    input_path = "D:\\code\\Python\\QingZhi\\TestData\\SystemIntegrationTest\\DoubleLiquidWithThreeLine.json"
    format_json_file(input_path)