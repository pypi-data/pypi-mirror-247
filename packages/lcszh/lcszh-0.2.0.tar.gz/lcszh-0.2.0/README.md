# 流程数智化通用函数
| 功能              | 函数                              | 输入                    | 输出                                        |
|-----------------|---------------------------------|-----------------------|-------------------------------------------|
| 配置文件读取          | read_config                     | 配置文件的路径               | 配置文件内容组成的字典(dict)                         |
| 文件目录判断          | check_and_creat_dir             | 目录路径                  | 存在：返回True<bre>； 不存在：创建目录，返回False          |
| 多边形面积计算         | get_PolygonArea                 | 各顶点位置坐标               | 面积                                        |
| 括号中内容获取         | get_bracketed_content           | 文本字符串                 | 文本中所有小括号中的内容组成的list                       |
| E-mail提取        | get_email                       | 文本字符串                 | email<br>email在文本中的位置<br>email的域名<br>     |
| 括号及其中内容去除       | rm_bracketed                    | 文本字符串                 | 不含括号及括号中的内容的文本                            |
| 符号去除            | rm_symbol                       | 文本字符串                 | 没有符号的纯文本                                  |
| 最长公共序列获取        | get_max_subseq                          | 两段文本字符串               | 两段文本的最长公公序列                               |
| 最长公共字串获取        |  get_max_comstr                  | 两段文本字符串               | 两段文本的最长公共字符串                              |
| 中文判断            | is_chinese                      | 文本字符串                 | 包含中文:True<br>不包含中文：False                  |
| 字符串全角转半角        | change_strQ2B                   | 字符串                   | 均转化为半角字符的字符串                              |
| json文件读取        | read_json                       | json文件路径              | json格式内容                                  |
| 将json数据写入json文件 | write_json                      | 保存的文件名<bre>要保存的数据     | json文件                                    |
| 读取csv数据         | read_csv                        | csv文件的路径，数据格式参数       | 列表(list)或字典(dic)格式的数据                     |
| 将数据写入csv文件      | write_csv                       | 列表(list)或字典(dic)格式的数据 | csv文件                                     |
| 读取excel数据       | read_excel                      | excel文件的路径，数据格式参数     | 列表(list)或字典(dic)格式的数据                     |
| 将数据写入excel文件    | write_excel                     | 列表(list)或字典(dic)格式的数据 | excel文件                                   |
| 读取txt文件         | read_txt                        | txt文件的路径              | 列表(list)格式的数据                             |
| 将数据写入txt文件      | write_txt                       | 列表(list)格式的数据         | txt文件                                     |
| 读取docx文档        | read_word                       | word文件的路径             | 列表(list)格式的数据                             |
| 计算两个向量的相似度      | compute_vecsimilar_one_2_one    | 两个向量                  | 两个向量的相似度                                  |
| 计算一个向量和多个向量的相似度 | compute_vecsimilar__one_2_many  | 一个向量和一个包含多个向量的列表      | 最大相似度下标<br>最大相似度对应相似度                     |
| 计算多个向量和多个向量的相似度 | compute_vecsimilar__many_2_many | 两个分别包含多个向量的列表         | 第一个列表中的每条向量和第二个列表向量中相似度最高的下标<br>最大相似度对应相似度 |
| 生成词云            | word_cloud_diagram         | 需要生成词云的文本<br>词云图片保存路径 | 词云图片<br>用来生成词云的词                  |
