class Updater:
    def __init__(self):
        self.repo = "https://github.com/aweirdwhale/MFMirror"
        self.url = "https://api.aweirdwhale.com/mfmirror/latest"
    def update(self):
        self.logger.info("Updating...")
        # Do the update
        self.logger.info("Update complete")