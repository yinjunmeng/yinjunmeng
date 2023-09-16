import unittest
from homework1 import main_test,Getfile_contents,Delete_useless,cos_sim
from unittest.mock import patch, mock_open
from io import StringIO
import os
import jieba


class MyTestCase(unittest.TestCase):
    def test_Getfile_contents(self):
        with open('temp.txt', 'w', encoding='utf-8') as temp_file:    # 创建一个临时文本文件供测试使用
            temp_file.write('This is a test text.')
        content = Getfile_contents('temp.txt')                        # 测试文件存在的情况
        self.assertEqual(content, 'This is a test text.')


    # 测试读取存在的文件并检查内容是否正确
    def test_read_existing_file(self):
        file_path = 'test_file.txt'
        expected_content = 'This is a test file content.'
        with open(file_path, 'w') as file:
            file.write(expected_content)
        with open(file_path, 'r') as file:
            actual_content = file.read()
        self.assertEqual(actual_content, expected_content)


    # 测试读取不存在的文件并检查是否引发了FileNotFoundError异常
    def test_read_non_existing_file(self):
        file_path = 'non_existing_file.txt'

        with self.assertRaises(FileNotFoundError):
            with open(file_path, 'r') as file:
                file.read()


    # 测试使用不同的编码方式读取文件并确保内容正确
    def test_read_with_different_encodings(self):
        file_path = 'encoded_file.txt'
        content = '这是一个测试文件内容。'
        # 以不同编码方式保存文件
        encodings = ['utf-8', 'utf-16', 'iso-8859-1']
        for encoding in encodings:
            with open(file_path, 'w', encoding="utf-8") as file:
                file.write(content)
            with open(file_path, 'r', encoding="utf-8") as file:
                actual_content = file.read()
            self.assertEqual(actual_content, content)


    # 测试读取二进制文件并检查内容是否正确
    def test_read_binary_file(self):
        file_path = 'binary_file.bin'
        expected_content = b'\x48\x65\x6c\x6c\x6f\x2c\x20\x57\x6f\x72\x6c\x64'
        with open(file_path, 'wb') as file:
            file.write(expected_content)
        with open(file_path, 'rb') as file:
            actual_content = file.read()
        self.assertEqual(actual_content, expected_content)


    # 测试文件的大小是否正确
    def test_file_size(self):
        file_path = 'test_file_size.txt'
        expected_size = 1024  # 1 KB
        with open(file_path, 'wb') as file:
            file.write(b'0' * expected_size)
        actual_size = os.path.getsize(file_path)
        self.assertEqual(actual_size, expected_size)


    #测试垃圾处理函数
    def test_Delete_useless2(self):
        input_text = "I am a boy，hey."
        expected_output = ["I","am","a","boy","hey"]
        cleaned_text = Delete_useless(input_text)
        self.assertEqual(cleaned_text, expected_output)


   # 测试空文本输入
    def test_delete_useless_empty_text(self):
        text = ""
        expected_result = []
        self.assertEqual(Delete_useless(text), expected_result)


    def test_delete_useless_all_punctuation(self):
        # 测试只包含标点符号的文本
        text = "，。！？"
        expected_result = [",", "。", "！", "？"]
        self.assertEqual(Delete_useless(text), expected_result)


    def test_cos_sim(self):
        final_content1 = ["这", "是", "一段", "示例文本"]
        final_content2 = ["这", "是", "另外一段", "示例文本"]
        similarity = cos_sim(final_content1, final_content2)
        expected_similarity = 0.75
        tolerance = 0.1
        self.assertAlmostEqual(similarity, expected_similarity, delta=tolerance)



if __name__ == '__main__':
    unittest.main()

