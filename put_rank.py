import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os
import time

# 设置中文字体
font_path = 'C:/Windows/Fonts/simhei.ttf'  # SimHei 黑体字体路径，适用于 Windows
my_font = font_manager.FontProperties(fname=font_path)  # 加载字体


# 读取json文件并生成表格
def print_rank(rank, old_rank):
    table = {
        "排名": [],
        "昵称": [],
        "总分": [],
        "解题数": []
    }
    for person in rank:
        name = person['team_name']  # 昵称
        total_number = person['total_number']  # 总解题数
        total_score = person['total_score']  # 总分数
        team_rank = person['team_rank']  # 排名

        if old_rank is not None and name in old_rank:
            old_total_number = old_rank[name]['total_number']
            old_total_score = old_rank[name]['total_score']
            old_team_rank = old_rank[name]['team_rank']
            total_number = f"{person['total_number']} ({f'+{total_number - old_total_number}' if old_total_number < total_number else '-'})"
            total_score = f"{person['total_score']} ({f'+{total_score - old_total_score}' if old_total_score < total_score else f'{total_score - old_total_score}' if old_total_score > total_score else '-'})"
            team_rank = f"{person['team_rank']} ({f'↓{team_rank - old_team_rank}' if old_team_rank < team_rank else f'↑{old_team_rank - team_rank}' if old_team_rank > team_rank else '-'})"

        table["排名"].append(team_rank)
        table["昵称"].append(name)
        table["总分"].append(total_score)
        table["解题数"].append(total_number)

    df = pd.DataFrame(table)

    # 设置画布大小
    fig, ax = plt.subplots(figsize=(8, len(rank) * 0.25))  # 根据数据行数调整高度

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

    # 添加表头
    plt.text(0.5, 1.05, f'参加人数:{len(rank)}\n生成时间: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}',
             ha='center', va='center', fontsize=14, fontproperties=my_font,
             transform=ax.transAxes)

    # 保存为图片
    plt.savefig(f'Ranking_{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}.png')

    # 展示图片
    plt.show()


# 筛选规则
def filter_rank(rank):
    # 把rank内字典根据team_rank由低到高排序
    rank = sorted(rank, key=lambda x: x['team_rank'])

    # 根据学校进行筛选
    rank = [x for x in rank if x['school'] == 'XXX大学']

    return rank


def main():
    with open('all_rank.json', 'r', encoding='utf-8') as f:
        all_rank = json.load(f)

    # 判断了是否存在'all_rank_old.json文件
    if os.path.exists('all_rank_old.json'):
        # 重命名'all_rank.json文件
        with open('all_rank_old.json', 'r', encoding='utf-8') as f:
            all_rank_old = json.load(f)
    else:
        all_rank_old = None

    all_rank = filter_rank(all_rank)
    if all_rank_old is not None:
        all_rank_old = filter_rank(all_rank_old)
        # 修改rank_old为字典
        all_rank_old = {x['team_name']: x for x in all_rank_old}

    print_rank(all_rank, all_rank_old)


if __name__ == '__main__':
    main()
