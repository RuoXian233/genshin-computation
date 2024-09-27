# genshin-computation
A python library to emulate numeric calculation in game Genshin Impact

All data used in calculation and associated to game comes from the Internet


Python 实现的《原神》数值计算系统，内部使用到的游戏相关数据均来自于互联网


## Installation

## 安装方法


- **Just clone the repository and write a simple python script using the library**
- **克隆本仓库，使用库内 API 编写需要实现功能的脚本即可**
- **Don't forgot to execute `pip install -r requirements.txt` to install dependencies**
- **务必执行 `pip install -r requirements.txt` 来安装所需依赖**


## Examples

## 使用示例
- 模拟圣遗物的刷取及强化
- Emulating: Obtain an artifact & Artifact enhancement

```python
    import genshin.artifacts.artifact as GArtifact
    import genshin.artifacts.enhancement as Enhancement


    art = GArtifact.Artifact(GArtifact.Artifact.Kits.denouement_of_sin)
    # 刷取 `谐律` 组圣遗物 (包含 `逐影猎人` 和 `黄金剧团` 套装)
    art.show()
    # 显示出圣遗物属性面板

    # 将圣遗物一次性强化至 20 级
    Enhancement.ArtifactEnhancement(art).upgrade(20)
    
    # 展示强化后圣遗物属性面板
    art.show()
```

