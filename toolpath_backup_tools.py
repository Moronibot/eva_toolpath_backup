""" Class to allow easy bulk download/upload of toolpaths to a robot """
import json
import os
from evasdk import Eva, EvaError, RobotState


class ToolpathBackupTool:
    """
    Init will generate a directory if one is not specified.
    Assumption is that the user be downloading toolpaths rather than uploading them.
    """
    def __init__(self, eva: Eva, download_dir: str = None):
        self.eva = eva
        if not download_dir:
            self.download_dir = f"{self.eva.name()['name']}".replace(' ', '_').lower()
        elif download_dir:
            self.download_dir = download_dir

    def _check_make_dir(self) -> None:
        """ If download directory folder doesn't exist, creates one """
        if not os.path.isdir(self.download_dir):
            os.mkdir(self.download_dir)

    def _save_toolpath(self, toolpath_data: dict) -> None:
        """ Saves toolpath data as toolpath name in a json file with pretty print """
        toolpath_path = toolpath_data['name'] + '.json'
        with open(os.path.join(self.download_dir, toolpath_path), 'w') as toolpath_file:
            json.dump(toolpath_data, toolpath_file, indent=4)

    def _stop_robot(self) -> None:
        """ Stops the robot """
        print("Stopping robot...")
        with self.eva.lock():
            self.eva.control_stop_loop(wait_for_ready=True)
        if self.eva.data_snapshot_property('control')['state'] == RobotState.READY.value:
            print("Robot stopped...")
        else:
            raise EvaError("Robot not stopped. Exiting.")

    def _robot_running(self) -> bool:
        """ Checks whether Eva running or not """
        robot_state = self.eva.data_snapshot_property('control')['state']
        if robot_state == RobotState.RUNNING.value:
            return True
        return False

    def backup(self) -> None:
        """ Downloads all toolpaths """
        stored_toolpaths = self.eva.toolpaths_list()
        for toolpaths in stored_toolpaths:
            self._save_toolpath(self.eva.toolpaths_retrieve(toolpaths['id']))

    def restore(self) -> None:
        """ Loads all toolpaths to robot """
        for toolpath_files in os.listdir(self.download_dir):
            with open(os.path.join(self.download_dir, toolpath_files), 'r') as single_toolpath:
                toolpath_contents = json.load(single_toolpath)
            self.eva.toolpaths_save(toolpath_contents['name'], toolpath_contents['toolpath'])

    def clean_toolpath_list(self) -> None:
        """ Deletes all toolpaths on the robot """
        if self._robot_running():
            self._stop_robot()
        stored_toolpaths = self.eva.toolpaths_list()
        for toolpaths in stored_toolpaths:
            self.eva.toolpaths_delete(toolpaths['id'])

    def backup_and_wipe(self) -> None:
        """ Downloads then wipes the toolpath list on the robot """
        if self._robot_running():
            self._stop_robot()
        self._check_make_dir()
        self.backup()
        self.clean_toolpath_list()


if __name__ == '__main__':
    IP = '10.10.60.175'
    TOKEN = '8a3e603de9cccb0be3ac12e79fa8493a837d29f5'
    robot = Eva(IP, TOKEN)
    toolpath_tool = ToolpathBackupTool(robot)
