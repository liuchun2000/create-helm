import json
import sys
import os
import yaml
import base64

def process_json_file(file_path, outputPath):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        packageName = data["name"]
        path = outputPath +"/"+packageName
        try:
            os.makedirs(path, exist_ok=True)  # exist_ok=True 避免目录已存在时报错
            print(f"目录 '{path}' 及其父目录创建成功或已存在。")
        except OSError as e:
            print(f"创建目录时发生错误: {e}")

        # 获取 "chart" 键对应的值
        if "chart" in data and isinstance(data["chart"], dict):
            chart_data = data["chart"]

            if "metadata" in chart_data and isinstance(chart_data, dict):
                metadata = chart_data["metadata"]
                file_name_append = path+"/Chart.yaml"
                try:
                    with open(file_name_append, "a", encoding="utf-8") as file:
                        yaml.dump(metadata, file, default_flow_style=False, sort_keys=False)
                except IOError as e:
                    print(f"追加内容到文件时发生错误: {e}")
                print("--- 遍历结束 ---")
            if "values" in chart_data and isinstance(chart_data, dict):
                values = chart_data["values"]
                file_name_append = path + "/values.yaml"
                try:
                    with open(file_name_append, "a", encoding="utf-8") as file:
                        yaml.dump(values, file, default_flow_style=False, sort_keys=False)
                except IOError as e:
                    print(f"追加内容到文件时发生错误: {e}")
            if "values" in chart_data and isinstance(chart_data, dict):
                values = chart_data["values"]
                file_name_append = path + "/values.yaml"
                try:
                    with open(file_name_append, "a", encoding="utf-8") as file:
                        yaml.dump(values, file, default_flow_style=False, sort_keys=False)
                except IOError as e:
                    print(f"追加内容到文件时发生错误: {e}")
            if "files" in chart_data and isinstance(chart_data, dict):
                files = chart_data["files"]
                for file_info in files:
                    name = file_info["name"]
                    data = file_info["data"]

                    if not name.startswith('.'):
                        file_name_append = path + "/" + name
                        decoded_bytes = base64.b64decode(data)
                        decoded_str = decoded_bytes.decode('utf-8')
                        try:
                            with open(file_name_append, "a", encoding="utf-8") as file:
                                file.write(decoded_str)
                        except IOError as e:
                            print(f"追加内容到文件时发生错误: {file_name_append} {e}")
            if "templates" in chart_data and isinstance(chart_data, dict):
                templates = chart_data["templates"]
                for template_info in templates:
                    name = template_info["name"]
                    data = template_info["data"]
                    parts = name.split('/')
                    dir_name = parts[0]
                    file_name = parts[1]
                    hole_path = path + "/" + dir_name
                    try:
                        os.makedirs(hole_path, exist_ok=True)  # exist_ok=True 避免目录已存在时报错
                        print(f"目录 '{hole_path}' 及其父目录创建成功或已存在。")
                    except OSError as e:
                        print(f"创建目录时发生错误: {e}")
                    file_name_append = hole_path + "/" + file_name
                    decoded_bytes = base64.b64decode(data)
                    decoded_str = decoded_bytes.decode('utf-8')
                    try:
                        with open(file_name_append, "a", encoding="utf-8") as file:
                            file.write(decoded_str)
                    except IOError as e:
                        print(f"追加内容到文件时发生错误: {e}")

    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在。请确保文件路径正确。")
    except json.JSONDecodeError:
        print(f"错误: 文件 '{file_path}' 不是一个有效的 JSON 文件。")
    except Exception as e:
        print(f"发生了一个意外错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python writehelmpackage.py <json_file_path> <output_path>")
        print("示例: python writehelmpackage.py data.json /opt/log")
    else:
        json_file = sys.argv[1]
        outputPath = sys.argv[2]
        process_json_file(json_file,outputPath)
