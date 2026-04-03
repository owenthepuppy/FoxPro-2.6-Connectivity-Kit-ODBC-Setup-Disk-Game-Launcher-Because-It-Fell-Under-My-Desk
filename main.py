import time
import os
import tomllib
import psutil

CONFIG_PATH = "A:\\autorun.toml"

disk_in = False
already_launched = False


def run_game(app_type, app):
    if data["launcher"] == "playnite":
        os.startfile(f"playnite://playnite/start/{app}")
    elif data["launcher"] == "steam":
        os.startfile(f"steam://rungameid/{app}")


def stop_game(game_process):
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"].lower() == game_process.lower():
            proc.terminate()


while True:
    if os.path.exists(CONFIG_PATH):
        disk_in = True
    else:
        disk_in = False

    if not already_launched and disk_in:
        print("Launching...")
        with open("A:\\autorun.toml", "rb") as f:
            data = tomllib.load(f)
            run_game(data["app_type"], data["app"])
        already_launched = True
        print("Launched")

    if already_launched and not disk_in:
        print("Quitting...")
        stop_game(data["process"])
        already_launched = False
        print("Quit Game")
    time.sleep(1)
