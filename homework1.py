import re
import jieba
from collections import Counter
import numpy as np


def  Getfile_contents(path):           # 获取文件内容
    str = ''
    with open(path, "r", encoding='UTF-8') as f:
        line = f.readline()
        while line:                    # 如果一次没有都玩文件，后续可以继续读
            str = str + line
            line = f.readline()        # 内容过大时继续读取文件操作，存在就读取，不存在退出
        print("读取数据内容任务完成")
        f.close()                      # 关闭文件
        return str                     # 提取读取文件数据


def Delete_useless(content):
    content = jieba.lcut(content)
    result = []
    for tags in content:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", tags)):      # 至少一个汉字、数字、字母、下划线 与 tags作比较，存在则放入队列中
            result.append(tags)                                # 将分好的数据放到列表中
        else:
            pass                                               # 没有需要放的汉字后退出循环
    return result


def cos_sim(final_content1, final_content2):  # str1，str2是分词后的标签列表
    finalcontent1 = (Counter(final_content1))
    finalcontent2 = (Counter(final_content2))
    content_final1 = []
    content_final2 = []
    for temp in set(final_content1 + final_content2):
        content_final1.append(finalcontent1[temp])
        content_final2.append(finalcontent2[temp])
    content_final1 = np.array(content_final1)
    content_final2 = np.array(content_final2)
    return content_final1.dot(content_final2) / \
           (np.sqrt(content_final1.dot(content_final1)) * np.sqrt(content_final2.dot(content_final2)))



if __name__ == '__main__':
    path1 = "D:\python_test\orig.txt"
    path2 = "D:\python_test\orig_0.8_add.txt"
    save_path = 'D:\python_test\save.txt'
    content1 = Getfile_contents(path1)
    content2 = Getfile_contents(path2)
    final_content1 = Delete_useless(content1)                    #jieba分词后
    print('final_content1=' + str(final_content1))  # jieba分词后
    final_content2 = Delete_useless(content2)                    #jieba分词后
    print('final_content2=' + str(final_content2))  # jieba分词后
    similarity = cos_sim(final_content1,final_content2)
    print('余弦相似度的计算分值：' + str(cos_sim(final_content1,final_content2)))
    f = open(save_path, 'w', encoding="utf-8")
    f.write("文章相似度： %.4f" % similarity)
    f.close()


