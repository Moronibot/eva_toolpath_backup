import os
from evasdk import Eva, EvaError, RobotState


class ToolpathBackupTool:
    def __init__(self, eva: Eva, toolpath_dir=None):
        self.eva = eva
        self.toolpath_dir = toolpath_dir

    def _check_and_stop(self):
        """ Checks whether Eva is in READY state and prompts to stop it if needed """

    def backup(self):
        """ Downloads all toolpaths """

    def restore(self):
        """ Loads all toolpaths to robot """

    def clean_toolpath_list(self):
        """ Deletes all toolpaths on the robot """

    def backup_and_wipe(self):
        """ Downloads then wipes the toolpath list on the robot """


if __name__ == '__main__':
    IP = None
    TOKEN = None
    robot = Eva(IP, TOKEN)
    toolpath_tool = ToolpathBackupTool(robot)
