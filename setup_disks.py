import questionary
import os
import tomllib
import tomli_w
import win32api
import requests


def get_floppy_id():
    vsn = win32api.GetVolumeInformation("A:\\")[1]
    floppy_id = format(vsn, "x")
    return floppy_id


def playnite():
    print(
        "You need to get the applications database ID, please follow these instructions:"
    )
    print("1. Select the app you want in Playnite")
    print(
        "2. Click More next to play and then click Edit, you can also hover over Play or More and click the pencil icon"
    )
    print("3. Click Advanced at the top of the new dialog window")
    print("4. Copy the DATABASE ID, NOT the Game ID")
    print("5. Paste it here and close the dialog window if you want")
    app_id = questionary.text("Please enter the database ID:").ask()
    return app_id


def steam():  # i HIGHLY reccommend you don't try to read this, if you do, you will probably have a headache for the next day
    print("You need to get the Steam App ID for the game you want")
    choice = questionary.select(
        "Please choose an option:",
        [
            "Enter App ID manually",
            "Enter name of game and attempt to find the App ID automatically",
            "Cancel",
        ],
    ).ask()
    if choice == "Cancel":
        return None
    elif choice[6] == "A":  # This is so horrible of a way to do this but, it works :)
        return questionary.text("Please enter the App ID:").ask()
    else:
        while True:
            while True:
                name = questionary.text("Enter the name of the game to choose:").ask()
                app_info = requests.get(
                    "https://store.steampowered.com/api/storesearch/",
                    params={"term": name, "l": "en", "cc": "US"},
                ).json()
                if app_info["items"]:
                    break
                else:
                    choice = questionary.select(
                        "No app found, would you like to try again, choose another method or cancel?",
                        ["Try again", "Choose another method", "Cancel"],
                    ).ask()
                    if choice == "Cancel":
                        return
                    elif choice != "Try again":
                        return steam()  # yep!
            app = app_info["items"][0]
            if questionary.confirm(f"Is {app["name"]} the game you chose?").ask():
                return app["id"]
            else:
                choice = questionary.select(
                    "No app found, would you like to try again, choose another method or cancel?",
                    ["Try again", "Choose another method", "Cancel"],
                ).ask()
                if choice == "Cancel":
                    return
                elif choice != "Try again":
                    return steam()  # yep!


def setup_disk():
    print("Please insert your disk now and press any key once it's inserted...")
    questionary.press_any_key_to_continue().ask()
    success = False
    while True:
        try:
            floppy_id = get_floppy_id()
            success = True
            break
        except Exception as e:
            print("Error:", e)
            if not questionary.confirm(
                "There was a problem reading the disk, would you like to try again?"
            ).ask():
                break
    if success:
        print("Got ID of:", floppy_id)
        while True:
            app_type = questionary.select(
                "Please choose a method to launch the app:",
                ["Playnite", "Steam", "Cancel"],
            ).ask()
            if app_type == "Playnite":
                app_id = playnite()
            elif app_type == "Steam":
                app_id = steam()
            else:
                return
            if app_id:
                break
            else:
                if not questionary.confirm(
                    "You didn't finish the App ID process, would you like to try again?"
                ).ask():
                    return
        # if they're at this point, they have a hopefully fine app id, yayayayayayayayayyaayayya, this code is HORRIBLE
        print(
            "Now, you need to get your app's main process exe name, basically, you need to find the name of the exe that is what you would click the X on to close the app, you can try going in task manager when it's running and looking for it."
        )
        while True:
            process_name = questionary.text("Please enter the proccess name/exe:").ask()
            if not process_name:
                if not questionary.confirm(
                    "You didn't enter a process name, would you like to try again?"
                ).ask():
                    return
            break
        print("App Type:", app_type)
        print("App ID:", app_id)
        print("Process Name:", process_name)
        if not questionary.confirm(
            "Does this all look correct? (if not, you need to restart everything all over again)"
        ).ask():
            print(
                "I'm sorry, I can't make a UI to fix errors right now. This code has been a PAIN to make"
            )
            return
        with open(CONFIG_PATH, "rb") as f:
            config = tomllib.load(f)
        config["disks"][floppy_id] = {
            "app_type": app_type.lower(),
            "app": app_id,
            "process": process_name,
        }
        with open(CONFIG_PATH, "wb") as f:
            tomli_w.dump(config, f)
        print("Setup complete!")  # that was painful
        print("Now, eject the disk and press any key to continue")
        questionary.press_any_key_to_continue().ask()
        os.remove(PAUSE_FILE)


CONFIG_PATH = os.path.join(os.environ["APPDATA"], "FP26CKOSDGLBIFUMD", "library.toml")
PAUSE_FILE = os.path.join(os.environ["APPDATA"], "FP26CKOSDGLBIFUMD", "pause")

print("Welcome to the floppy disk setup app!")
while True:
    match questionary.select(
        "Please choose an option:", ["Setup individual disk", "Bulk Setup", "Exit"]
    ).ask():
        case "Exit":
            print("Goodbye!")
            break
        case "Setup individual disk":
            open(PAUSE_FILE, "w").close()
            setup_disk()
