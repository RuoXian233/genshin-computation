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
