# Elvui_Freebie

**Elvui_Freebie** is a streamlined tool designed for World of Warcraft players to quickly download and install the ElvUI addon from [Tukui](https://tukui.org/elvui). Unlike the official installer, which requires an ElvUI Patreon subscription for accelerated downloads similar to CurseForge, Elvui_Freebie allows users to bypass these restrictions. As a cost-effective solution developed by a student, this tool facilitates the scanning of your default download directory, auto-detection of ElvUI zip files, and seamless extraction directly into your WoW Addon folder. This simplifies the update process, reducing manual efforts and saving time with each new ElvUI release.<br />

## How to Use 

### Initial Setup
1. **Run the Code:** Yes, run the code in your machine with terminal or IDE. 
2. **Select the Download Directory:** On first use, manually set your download directory (typically `C:\Users\<Your Username>\Downloads`).
3. **Set the Output Directory:** Manually select your World of Warcraft Addon folder as the output directory. This is usually located at `World of Warcraft\_retail_\Interface\AddOns`.

   If you are unsure where your WoW installation is, open the Battle.net app, navigate to the World of Warcraft page, and click the gear icon in the bottom left corner to open settings. Click "Show in Explorer" to display your WoW folder.<br />

### Routine Use
After the initial setup, both directories will be saved in the configuration file for future use. To update ElvUI, simply start Elvui_Freebie, select the new ElvUI zip file, and click to extract it with one click. This process will automatically update your AddOns with the latest version of ElvUI.

## Advanced Setup for Developers
For users with programming knowledge, there is an option to convert this Python script into an executable file using tools like PyInstaller. This conversion facilitates a more convenient deployment and use of the tool without the need for a Python environment. To create an executable:

1. **Install PyInstaller:** Run `pip install pyinstaller` from your command line.
2. **Generate the Executable:** Navigate to the script's directory and run `pyinstaller --onefile --windowed Elvui_Freebie.py`.
3. **Use the Executable:** The executable will be created in the `dist` directory within your script's directory. You can move this file to any location on your computer for easier access.
