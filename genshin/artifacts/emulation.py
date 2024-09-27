from dataclasses import dataclass
import time
from typing import Any, Callable

from .artifact import Artifact
import tqdm
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

import abc


# 简单的模拟器, 适用于圣遗物刷取的模拟计算
def simple_emulator(n: int, condition: Callable[[Artifact], bool], plot: bool = False) -> None:
    all_counts = []
    arts = []
    print(f'[模拟器] 准备执行 {n} 次模拟 ...')
    st = time.time()
    for i in tqdm.tqdm(range(n)):
        count = 0
        while True:
            count += 1
            art = Artifact(Artifact.Kits.denouement_of_sin)

            if condition(art):        
                all_counts.append(count)
                arts.append(art)            
                break

    print(f'[试验结果] {n} 次模拟, 共刷取 {sum(all_counts)} 件圣遗物, 平均消耗 {sum(all_counts) / len(all_counts) * 15} 点体力可获得匹配圣遗物 (即刷取秘境约 {sum(all_counts) / len(all_counts) / 1.5} 次)')
    print(f'[试验结果] 平均概率密度: {n / sum(all_counts) * 100}%')
    max_score = 0
    max_index = 0
    for i, art in enumerate(arts):
        current_score = Artifact.evaluate_by_crit(art)
        if current_score > max_score:
            max_score = current_score
            max_index = i
    
    print(f'[试验结果] 最高初始分: {max_score}, 圣遗物属性如下:')
    arts[max_index].show()
    et = time.time()
    print(f'[模拟器] 模拟已完成, 总用时 {round(et - st, 3)} 秒')

    if plot:
        matplotlib.use('TkAgg')        
        plt.rcParams['font.family'] = 'WenQuanYi Micro Hei'
        plt.xlabel('试验次数')
        plt.ylabel('刷取个数')
        plt.plot(np.array([_ for _ in range(n)]), all_counts)
        plt.show()     
