import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 设置中文字体
font_path = 'C:/Windows/Fonts/simhei.ttf'  # SimHei 黑体字体路径，适用于 Windows
my_font = font_manager.FontProperties(fname=font_path)  # 加载字体

# 读取json文件并生成表格
def print_rank(rank):
    table = {
        "排名": [],
        "昵称": [],
        "总分": [],
        "结题数": []
    }
    for person in rank:
        name = person['team_name']  # 昵称
        total_number = person['total_number']  # 总解题数
        total_score = person['total_score']  # 总分数
        team_rank = person['team_rank']  # 排名

        table["排名"].append(team_rank)
        table["昵称"].append(name)
        table["总分"].append(total_score)
        table["结题数"].append(total_number)

    df = pd.DataFrame(table)

    # 设置画布大小
    fig, ax = plt.subplots(figsize=(8, len(rank) * 0.8))  # 根据数据行数调整高度

    # 隐藏轴
    ax.axis('tight')
    ax.axis('off')

    # 创建表格
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # 遍历表格的所有单元格，手动设置中文字体
    for key, cell in table.get_celld().items():
        cell.set_text_props(fontproperties=my_font)  # 设置中文字体

    # 调整表格字体大小
    table.auto_set_font_size(False)
    table.set_fontsize(11)

    # 保存为图片
    plt.savefig('table_image_with_chinese.png')

    # 展示图片
    plt.show()


def main():
    with open('all_rank.json', 'r', encoding='utf-8') as f:
        all_rank = json.load(f)

    # 把rank内字典根据team_rank由低到高排序
    all_rank = sorted(all_rank, key=lambda x: x['team_rank'])

    # 根据学校进行筛选
    all_rank = [x for x in all_rank if x['school'] == 'XXX大学']

    print_rank(all_rank)


if __name__ == '__main__':
    main()
