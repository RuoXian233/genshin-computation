# 测算芙宁娜圣遗物毕业期望时间
import sys
import tqdm
import genshin.artifacts.artifact as GArtifact

state = [0, 0, 0, 0, 0]
artifacts = []
indexes = [[], [], [], [], []]

all_artifacts = []
all_indexes = []

def reset() -> None:
    global state, artifacts, indexes
    state = [0, 0, 0, 0, 0]
    artifacts = []
    indexes = [[], [], [], [], []]


def run() -> int:
    # 阶段1 刷取
    i = 0
    while sum(state) != 5:
        art = GArtifact.Artifact(GArtifact.Artifact.Kits.denouement_of_sin)
        artifacts.append(art)
        if art.kit == '黄金剧团':
            if art.part == GArtifact.Artifact.Parts.flower_of_life:
                state[0] = 1
                if i not in indexes[0]:
                    indexes[0].append(i)
            elif art.part == GArtifact.Artifact.Parts.plume_of_death:
                state[1] = 1
                if i not in indexes[1]:
                    indexes[1].append(i)
            elif art.part == GArtifact.Artifact.Parts.sands_of_eon:
                if art.primary_attribute.attribute_type == GArtifact.Artifact.PrimaryAttributeType.elemental_recharge:
                    state[2] = 1
                    if i not in indexes[2]:
                        indexes[2].append(i)
            elif art.part == GArtifact.Artifact.Parts.goblet_of_eonothem:
                if art.primary_attribute.attribute_type == GArtifact.Artifact.PrimaryAttributeType.hp_percentage:
                    state[3] = 1
                    if i not in indexes[3]:
                        indexes[3].append(i)
            elif art.part == GArtifact.Artifact.Parts.circlet_of_logos:
                if art.primary_attribute.attribute_type in (GArtifact.Artifact.PrimaryAttributeType.critical_rate, GArtifact.Artifact.PrimaryAttributeType.critical_damage):
                    state[4] = 1
                    if i not in indexes[4]:
                        indexes[4].append(i)
        i += 1
    return i + 1

if __name__ == '__main__':
    result = []
    n = 1000
    if len(sys.argv) == 2:
        try:
            n = int(sys.argv[1])
        except ValueError:
            n = 1000
    for _ in tqdm.tqdm(range(n)):
        result.append(run())
        reset()
    sys.stderr.write(f'{n} 次模拟, 平均刷取次数: {sum(result) / len(result) / 1.5}\n')
