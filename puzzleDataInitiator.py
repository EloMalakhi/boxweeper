

def seeIftwoCavitiesCollide(Set1, Set2, CavityGroup, CavityNum):
#   INPUTS (in sequential order):
#   Set1: type =  (int, int, int, int): 1st = X coord of Cavity Corner,
#                                       2nd = y coord of Cavity corner
#                                       3rd = z coord of Cavity corner
#                                       4th = height/width/length of cavity
#   Set2: type =  (int, int, int, int): 1st = X coord of #2 Cavity Corner,
#                                       2nd = y coord of #2 Cavity corner
#                                       3rd = z coord of #2 Cavity corner
#                                       4th = height/width/length of #2 cavity
#   OUTPUTS: there are no outputs because the change occurs in the shared data-ref
#            CavityGroup and CavityNum

    if int(Set1[0] - Set1[3]/2 + .5) <= int(Set2[0] + Set2[3]/2 - .5) and int(Set1[0] + Set1[3]/2 - .5) >= int(Set2[0] - Set2[3]/2 + .5):
        if int(Set1[1] - Set1[3]/2 + .5) <= int(Set2[1] + Set2[3]/2 - .5) and int(Set1[1] + Set1[3]/2 - .5) >= int(Set2[1] - Set2[3]/2 + .5):
            if int(Set1[2] - Set1[3]/2 + .5) <= int(Set2[2] + Set2[3]/2 - .5) and int(Set1[2] + Set1[3]/2 - .5) >= int(Set2[2] - Set2[3]/2 + .5):
                # if the cavities collide then both cavities must be merged to become one cavity
                # one CavityGroup List item must eat up the other CavityGroup List item
                # the eaten CavityGroupList item must become empty
                # and its corresponding Spacial List item must also become empty
                # to prevent the collision of a nonexistent cavity with an existing one

                CavityGroup[CavityNum[Set1]].extend(CavityGroup[CavityNum[Set2]])
                CavityGroup[CavityNum[Set2]] = []
                CavityNum[Set2] = CavityNum[Set1]


def MakeSweeperGame(Height, Width, Length, No_of_Mines):
#   INPUT (in sequential order):
#         in box units
#   Height: int:  corresponding to the total height of the box
#   Width:  int:  corresponding to the total width or depth of the box
#   Length: int:  corrresponding to the total length or distance from left to right of the box
#   No_of_Mines: int:  the amount of mines being randomly generated in the cube

#   OUTPUT:
#   PointsRecord: {(x: int, y: int, z: int): [description_of_box: str, mark_status: str]
# #                (x: int, y: int, z: int): [description_of_box: str, mark_status: str]
# #                (x: int, y: int, z: int): [description_of_box: str, mark_status: str]
#                  (x: int, y: int, z: int): [description_of_box: str, mark_status: str], etc} # all the keys corresponding to all the points

    PointsRecord = {}

    # first make each box location an empty block
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
        # this loop generates between 1 and 7 cavities in the cube
        # the dimensions of each cavity is as follows:
        #    x: 1 to int(Width/14)
        #    y: 1 to int(Height/14)
        #    z: 1 to int(Length/14)
        if int(Width*Height*Length) > 2743:
            # randint(1, 0) will produce an error
            # so Width*Height*Length must be 14^3 or greater
            WidthOfBox = randint(1, int((Width*Height*Length)**(1/3)/14))
            CX, CY, CZ = randint(0, Width - 1), randint(0, Height - 1), randint(0, Length - 1)
            # the starting location for the cavity in the 3D box
            Cavities.append((CX, CY, CZ, WidthOfBox))
            # above: storing the spacial arrangement of the cavity
            CavityNum[(CX, CY, CZ, WidthOfBox)] = i + 1
            # above and below: tying the cavity name to the cavity spacial arrangement
            CavityGroup[i + 1] = [(CX, CY, CZ, WidthOfBox)]

    # these lines go through all the cavities and merge the cavities
    # which touch each other
    amount_of_times = len(Cavities) - 1
    if amount_of_times > 0:
        for j in range(amount_of_times):
            CompareSet1 = Cavities[0]
            Cavities2 = []
            for i in range(len(Cavities) - 1):
                seeIftwoCavitiesCollide(CompareSet1, Cavities[i+1], CavityGroup, CavityNum)
                Cavities2.append(Cavities[i+1])
            Cavities = Cavities2

    # go through all the given blocks and turn whatever ones fit the cavity spacial
    # arrangements into cavity blocks
    if len(CavityGroup) > 0:
        for i in CavityGroup:
            for j in CavityGroup[i]:
                CX, CY, CZ, WidthOfBox = j
                for x in range(int(CX - WidthOfBox/2 + .5), int(CX + WidthOfBox/2 + .5)):
                    for y in range(int(CY - WidthOfBox/2 + .5), int(CY + WidthOfBox/2 + .5)):
                        for z in range(int(CZ - WidthOfBox/2 + .5), int(CZ + WidthOfBox/2 + .5)):
                            PointsRecord[(x, y, z)] = [f'cavity {i} closed', 'markable']

    while No_of_Mines != 0:
        # go through all the mines placing them on blocks and not on cavity blocks
        MineX, MineY, MineZ = randint(0, Width - 1), randint(0, Height - 1), randint(0, Length - 1)
        if PointsRecord[(MineX, MineY, MineZ)][0] == "block":
            PointsRecord[(MineX, MineY, MineZ)] = ["mine closed", 'markable']
            No_of_Mines -= 1
    
    return PointsRecord





