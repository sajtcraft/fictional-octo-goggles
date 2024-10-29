import tkinter as tk
from tkinter import messagebox
import subprocess, os, webbrowser, time, threading, shutil, atexit
from urllib.request import urlretrieve

# Paths, URLs, and version
downloads_folder = os.path.expanduser("~/Downloads")
appx_filename = "Minecraft-1.7.0.13.Appx"
appx_path = os.path.join(downloads_folder, appx_filename)
download_url = "https://drive.google.com/file/d/1naIu8cfXUi2flMV4Gsb-pQ8th4yZXz-m/view?usp=sharing"
news_url = "https://sajtrealms.blogspot.com"
externalservers_url = "https://raw.githubusercontent.com/sajtcraft/fictional-octo-goggles/refs/heads/main/externalservers.txt"

# URL for the latest launcher script and version check file
launcher_url = "https://raw.githubusercontent.com/sajtcraft/fictional-octo-goggles/refs/heads/main/launcher.py"
version_check_url = "https://raw.githubusercontent.com/sajtcraft/fictional-octo-goggles/refs/heads/main/version.txt"
current_version = "1.0.1"

# Paths for externalservers and launcher
mc_data_path = os.path.join(os.path.expanduser("~"), 'AppData', 'Local', 'Packages',
                            'Microsoft.MinecraftUWP_8wekyb3d8bbwe', 'LocalState', 'games', 'com.mojang', 'minecraftpe')
local_externalservers = os.path.join(os.path.dirname(__file__), 'externalservers.txt')
local_launcher = os.path.join(os.path.dirname(__file__), 'launcher.py')

# Function to check for launcher updates
def check_for_updates():
    try:
        # Download the latest version info
        latest_version_path = os.path.join(os.path.dirname(__file__), 'latest_version.txt')
        urlretrieve(version_check_url, latest_version_path)
        
        with open(latest_version_path, 'r') as f:
            latest_version = f.read().strip()
        
        if latest_version != current_version:
            messagebox.showinfo("Update Available", "Updating to the latest version of the launcher.")
            download_launcher_update()
        else:
            print("Launcher is up-to-date.")
            
        os.remove(latest_version_path)  # Clean up temporary version file
    except Exception as e:
        print("Failed to check for updates:", e)

# Function to download and replace the launcher script
def download_launcher_update():
    try:
        urlretrieve(launcher_url, local_launcher)
        print("Launcher updated successfully.")
        messagebox.showinfo("Update Complete", "Please restart the launcher to use the new version.")
    except Exception as e:
        print("Failed to download update:", e)

# If externalservers.txt isn't there, download it
def download_server_file():
    try:
        urlretrieve(externalservers_url, local_externalservers)
        print("Downloaded externalservers.txt")
    except Exception as e:
        print("Couldn’t download externalservers.txt:", e)

def replace_server_file():
    target_server_file = os.path.join(mc_data_path, 'external_servers.txt')
    try:
        shutil.copy(local_externalservers, target_server_file)
        print("Replaced externalservers.txt in Minecraft folder")
    except Exception as e:
        print("Couldn’t replace externalservers.txt:", e)

# Call auto-update on start
check_for_updates()
download_server_file()
replace_server_file()

def cleanup():
    if os.path.exists(local_externalservers):
        try:
            os.remove(local_externalservers)
            print("Removed local externalservers.txt")
        except Exception as e:
            print("Error deleting file:", e)

atexit.register(cleanup)

def check_for_appx_download():
    while not os.path.exists(appx_path):
        time.sleep(5)
    install_appx()

def install_appx():
    try:
        subprocess.run(f"powershell Add-AppxPackage -Path '{appx_path}'", shell=True, check=True)
        messagebox.showinfo("Launcher", "Minecraft installed!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Install failed: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

def open_download_page():
    if not os.path.exists(appx_path):
        messagebox.showwarning("File Not Found",
                               f".appx file for MCPE missing:\n\n{appx_path}\n\nOpening download page.")
        webbrowser.open(download_url)
        threading.Thread(target=check_for_appx_download, daemon=True).start()
    else:
        install_appx()

def launch_minecraft():
    download_server_file()
    replace_server_file()
    try:
        subprocess.run("start minecraft://", shell=True, check=True)
        messagebox.showinfo("Launcher", "Launching Minecraft!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Launch failed: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

def open_servers_page():
    webbrowser.open(news_url)

root = tk.Tk()
root.title("Minecraft Launcher")
root.geometry("350x250")

tk.Label(root, text="SajtRealms", font=("Arial", 12)).pack(pady=20)

tk.Button(root, text="Install Minecraft", font=("Arial", 12), command=open_download_page).pack(pady=10)
tk.Button(root, text="Launch Client", font=("Arial", 12), command=launch_minecraft).pack(pady=10)
tk.Button(root, text="Changelog", font=("Arial", 12), command=open_news_page).pack(pady=10)

root.mainloop()
