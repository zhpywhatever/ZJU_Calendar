import json


def get_train_text(file_path):
    """
    从指定文件路径读取数据并返回处理后的数据列表。

    :param file_path: 要读取的JSON文件路径
    :return: 处理后的数据列表
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        processing_data = json.load(file)

    result = []
    for row in processing_data:
        content_id = row['fields']['ID']['text']
        content_text = row['fields']['text']['text']
        result.append({'content_id': content_id, 'content_text': content_text})

    return result


def add_train_texts(data, output_file_path):
    """
    将处理后的数据写入指定的文件路径。

    :param data: 处理后的数据列表
    :param output_file_path: 要写入的文件路径
    """
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for item in data:
            outfile.write(str(item))

# def add_train_texts(data, output_file_path):
#     """
#     将处理后的数据写入指定的文件路径。
#
#     :param data: 处理后的数据列表
#     :param output_file_path: 要写入的文件路径
#     """
#     with open(output_file_path, 'w', encoding='utf-8') as outfile:
#         for item in data:
#             outfile.write(item)


# 示例用法
input_file_path = 'output.json'
output_file_path = 'resources/output.txt'

# 获取处理后的数据
train_texts = get_train_text(input_file_path)

# 将数据写入新的文件
add_train_texts(train_texts, output_file_path)
