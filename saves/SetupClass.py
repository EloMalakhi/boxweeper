class Setup(object):
    def __init(self):
        pass

    def set(self, Matrix, error, EnoughInformation, pf, IF, mode):
        self.FileMatrix = Matrix  # the dictionary translating modes into presetFiles and IndexFiles
        # form for Matrix:
        # [
        #    {mode1: presetFile1,
        #     mode2: presetFile2,
        #     mode3: presetFile3,
        #     mode4: presetFile4, etc},

        #    {mode1: indexFile1,
        #     mode2: indexFile2,
        #     mode3: indexFile3,
        #     mode4: indexFile4, etc}
        # ]
        self.error = error  # invalid error display used during the preset defining period
        self.EnoughInformation = EnoughInformation # True or False value used during the preset defining period
        self.PresetFile = pf    # the program-decided file for establishing the presets for the game based on the selected mode
        self.indexFile = IF  # the program-decided file for the game based on the selected mode
        self.mode = mode # which mode the user selected