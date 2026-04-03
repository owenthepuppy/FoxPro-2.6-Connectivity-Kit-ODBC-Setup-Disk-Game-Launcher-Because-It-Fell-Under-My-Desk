import time
import os
import tomllib
import psutil
import win32api


CONFIG_PATH = os.path.join(os.environ["APPDATA"], "FP26CKOSDGLBIFUMD", "library.toml")
PAUSE_FILE = os.path.join(os.environ["APPDATA"], "FP26CKOSDGLBIFUMD", "pause")

disk_in = False
already_launched = False
app_info = None


def run_game(app_type, app):
    if not os.path.exists(PAUSE_FILE):
        if app_type == "playnite":
            os.startfile(f"playnite://playnite/start/{app}")
        elif app_type == "steam":
            os.startfile(f"steam://rungameid/{app}")


def stop_game(game_process):
    if not os.path.exists(PAUSE_FILE):
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"].lower() == game_process.lower():
                proc.terminate()


while True:
    if os.path.exists("A:\\"):
        disk_in = True
    else:
        disk_in = False

    if not already_launched and disk_in:
        vsn = win32api.GetVolumeInformation("A:\\")[1]
        floppy_id = format(vsn, "x")

        with open(CONFIG_PATH, "rb") as f:
            config = tomllib.load(f)

        if floppy_id in config["disks"]:
            print("Launching...")
            app_info = config["disks"][floppy_id]
            run_game(app_info["app_type"], app_info["app"])
            already_launched = True
            print("Launched")
        else:
            print("Floppy ID not found in library")

    if already_launched and not disk_in:
        if app_info:
            print("Quitting...")
            stop_game(app_info["process"])
            already_launched = False
            print("Quit Game")
    time.sleep(1)
