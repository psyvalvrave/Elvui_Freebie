# Elvui_Freebie

**Elvui_Freebie** is a streamlined tool designed for World of Warcraft players to quickly download and install the ElvUI addon from [Tukui](https://tukui.org/elvui). Unlike the official installer—which requires an ElvUI Patreon subscription for accelerated downloads similar to CurseForge—Elvui_Freebie allows users to bypass these restrictions. Developed as a cost-effective solution by a student, this tool scans your default download directory for ElvUI zip files, auto-detects new versions, and seamlessly extracts them directly into your WoW AddOn folder. This simplifies the update process, reducing manual effort and saving time with each new release.

> **Note:**  
![Elvui_Freebie](https://github.com/user-attachments/assets/cc2cf663-ebef-4f68-aa84-505195535d76)


## Features

- **Automatic Update Check:**  
  The tool asynchronously checks the official website for the latest ElvUI version. If a new version is available, a red message is displayed at the top of the UI.

- **Online Download:**  
  Instead of manually visiting the website, simply click "Download Latest Online" to have the tool automatically trigger the download of the new version using Selenium in headless mode.

- **Manual Update Check:**  
  If you suspect a new version is available but the application did not indicate it at launch, click "Re-check Update" to refresh the online version information.

- **Extraction with Cleanup:**  
  After extracting the new ElvUI zip file, the tool prompts you with a custom message asking if you want to delete the zip file to keep your download folder clean.

- **Custom, Modern UI:**  
  Enjoy a sleek, frameless interface with a custom title bar and modern styling—designed with PyQt5 and enhanced by custom message boxes and dialogs.

## How to Use

### Initial Setup
1. **Download the Build:**  
   Download the latest build artifact from GitHub Actions.  
   https://github.com/psyvalvrave/Elvui_Freebie/actions/runs/14090822253/artifacts/2826229035

2. **Extract and Run:**  
   Unzip the downloaded folder and run `Elvui_Freebie.exe`.

3. **Configure Directories:**  
   - **Source Directory:** On first use, set your download directory (typically `C:\Users\<Your Username>\Downloads`).
   - **Output Directory:** Manually select your World of Warcraft AddOn folder (usually `World of Warcraft\_retail_\Interface\AddOns`).  
     *Tip:* If you're unsure where your WoW installation is located, open the Battle.net app, navigate to the WoW page, and click the gear icon (bottom left) to access settings. Choose "Show in Explorer" to reveal your installation folder.

### Other Functions
1. **Automatic Update Notification:**  
   Upon launch, the tool displays a message (by default, "You have the latest version of ElvUI installed") at the top. If a new version is detected on the official website, this message updates to a red notification stating the new version number.

2. **Online Download:**  
   Click the **Download Latest Online** button to automatically download the new version without manually visiting the website.

3. **Manual Update Check:**  
   If needed, use the **Re-check Update** button to re-query the official website for the latest version.

4. **Zip File Cleanup:**  
   After extracting an ElvUI zip file, a prompt will ask if you wish to delete the zip file from your download directory—helping you avoid clutter.

### Routine Use
After initial configuration, your selected directories are saved in a configuration file for future use. To update ElvUI:
- Simply launch Elvui_Freebie.
- Select the new ElvUI zip file if necessary.
- Click **Extract Selected** to update your AddOns with the latest version.

## Advanced Setup for Developers

For users with programming knowledge, you can convert this Python project into a standalone executable using Nuitka. This eliminates the need for a Python environment on the target machine.

### Steps to Build with Nuitka
1. **Install Nuitka and Dependencies:**
   ```bash
   pip install Nuitka pyqt5 selenium webdriver-manager
