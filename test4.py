

def seeIftwoCavitiesCollide(Set1, Set2, CavityGroup, CavityNum):
    if int(Set1[0] - Set1[3]/2 + .5) <= int(Set2[0] + Set2[3]/2 - .5) and int(Set1[0] + Set1[3]/2 - .5) >= int(Set2[0] - Set2[3]/2 + .5):
        if int(Set1[1] - Set1[3]/2 + .5) <= int(Set2[1] + Set2[3]/2 - .5) and int(Set1[1] + Set1[3]/2 - .5) >= int(Set2[1] - Set2[3]/2 + .5):
            if int(Set1[2] - Set1[3]/2 + .5) <= int(Set2[2] + Set2[3]/2 - .5) and int(Set1[2] + Set1[3]/2 - .5) >= int(Set2[2] - Set2[3]/2 + .5):
                CavityGroup[CavityNum[Set1]].extend(CavityGroup[CavityNum[Set2]])
                CavityGroup[CavityNum[Set2]] = []
                CavityNum[Set2] = CavityNum[Set1]


def MakeSweeperGame(Height, Width, Length, No_of_Mines):
    PointsRecord = {}

    for x in range(Width):
        for y in range(Height):
            for z in range(Length):
                PointsRecord[(x, y, z)] = ["block", 'markable']

    from random import randint
    Cavities = []
    Cavities2 = []
    CavityGroup = {}
    CavityNum = {}
    for i in range(randint(1,7)):
        if int(Width*Height*Length) > 2743:
            WidthOfBox = randint(1, int((Width*Height*Length)**(1/3)/14))
            CX, CY, CZ = randint(0, Width - 1), randint(0, Height - 1), randint(0, Length - 1)
            Cavities.append((CX, CY, CZ, WidthOfBox))
            CavityNum[(CX, CY, CZ, WidthOfBox)] = i + 1
            CavityGroup[i + 1] = [(CX, CY, CZ, WidthOfBox)]
        

    amount_of_times = len(Cavities) - 1
    if amount_of_times > 0:
        for j in range(amount_of_times):
            CompareSet1 = Cavities[0]
            Cavities2 = []
            for i in range(len(Cavities) - 1):
                seeIftwoCavitiesCollide(CompareSet1, Cavities[i+1], CavityGroup, CavityNum)
                Cavities2.append(Cavities[i+1])
            Cavities = Cavities2

    if len(CavityGroup) > 0:
        for i in CavityGroup:
            for j in CavityGroup[i]:
                CX, CY, CZ, WidthOfBox = j
                for x in range(int(CX - WidthOfBox/2 + .5), int(CX + WidthOfBox/2 + .5)):
                    for y in range(int(CY - WidthOfBox/2 + .5), int(CY + WidthOfBox/2 + .5)):
                        for z in range(int(CZ - WidthOfBox/2 + .5), int(CZ + WidthOfBox/2 + .5)):
                            PointsRecord[(x, y, z)] = [f'cavity {i} closed', 'markable']
    while No_of_Mines != 0:
        MineX, MineY, MineZ = randint(0, Width - 1), randint(0, Height - 1), randint(0, Length - 1)
        if PointsRecord[(MineX, MineY, MineZ)][0] == "block":
            PointsRecord[(MineX, MineY, MineZ)] = ["mine closed", 'markable']
            No_of_Mines -= 1
    
    return PointsRecord





