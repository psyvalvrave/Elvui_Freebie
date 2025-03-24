import sys
import os
import zipfile
import json
import time
import re

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QListWidget, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

CONFIG_FILE = 'config_Elvui_Freebie.json'


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'last_directory': '', 'last_extraction_path': '', 'last_extracted_version': ''}


def save_config(config):
    """Save config values to JSON."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)


def check_online_version():
    """
    Opens https://tukui.org/elvui, finds the download button,
    extracts the version number, and returns it as a string.
    Returns None if something goes wrong (couldn't parse, etc.).
    """
    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    url = "https://tukui.org/elvui"
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        download_button = driver.find_element(By.ID, "download-button")
        button_text = download_button.text 

        driver.quit()

        if "ELVUI" in button_text.upper():
            version_number = button_text.split()[-1]  
            return version_number
        else:
            return None

    except Exception as e:
        print(f"An error occurred while checking the online version: {e}")
        return None

class UpdateChecker(QThread):
    #Signal to emit the online version string (empty string if none)
    updateChecked = pyqtSignal(str)

    def run(self):
        online_ver = check_online_version()
        if online_ver is None:
            self.updateChecked.emit("")  
        else:
            self.updateChecked.emit(online_ver)

class App(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.config = config
        self.online_version = None  
        self.is_newer = False

        self.initUI()

        self.pathEntry.setText(self.config.get('last_directory', ''))
        self.outputPathEntry.setText(self.config.get('last_extraction_path', ''))

        last_extracted = self.config.get('last_extracted_version', 'None')
        self.versionLabel.setText(f"Last extracted version: {last_extracted}")

         #Initially assume no update (or unknown) and update UI immediately
        self.updateLabel.setText("You have the latest version of ElvUI installed.")

        self.scan_directory(self.config.get('last_directory', ''))
        
        #Start asynchronous update check
        self.checker = UpdateChecker()
        self.checker.updateChecked.connect(self.onUpdateChecked)
        self.checker.start()

    def initUI(self):
        #Set Up UI
        mainLayout = QVBoxLayout()
        sourceLayout = QHBoxLayout()
        outputLayout = QHBoxLayout()
        versionLayout = QHBoxLayout()
        
        #title area, replace with original windows title
        self.titleBar = QWidget(self)
        self.titleBar.setObjectName("titleBar")
        
        titleBarLayout = QHBoxLayout(self.titleBar)
        titleBarLayout.setContentsMargins(0, 0, 0, 0)
        
        self.titleLabel = QLabel("Elvui Freebie", self.titleBar)
        titleBarLayout.addWidget(self.titleLabel)
        
        titleBarLayout.addStretch(1)
        
        # Minimize Button
        self.btnMin = QPushButton("-", self.titleBar)
        self.btnMin.setObjectName("btnMinimize")
        self.btnMin.clicked.connect(self.showMinimized)
        titleBarLayout.addWidget(self.btnMin)

        # Maximize/Restore Button
        self.btnMax = QPushButton("⬜", self.titleBar)
        self.btnMax.setObjectName("btnMaximize")
        self.btnMax.clicked.connect(self.toggleMaxRestore)
        titleBarLayout.addWidget(self.btnMax)

        # Close Button
        self.btnClose = QPushButton("X", self.titleBar)
        self.btnClose.setObjectName("btnClose")
        self.btnClose.clicked.connect(self.close)
        titleBarLayout.addWidget(self.btnClose)

        mainLayout.addWidget(self.titleBar)

        self.updateLabel = QLabel("")
        mainLayout.addWidget(self.updateLabel)

        #zip file source area
        self.pathEntry = QLineEdit()
        browseSourceBtn = QPushButton('Browse Source')
        browseSourceBtn.clicked.connect(self.browse_directory)

        sourceLayout.addWidget(QLabel('Select Source Directory:'))
        sourceLayout.addWidget(self.pathEntry)
        sourceLayout.addWidget(browseSourceBtn)

        #unzip target location area
        self.outputPathEntry = QLineEdit()
        browseOutputBtn = QPushButton('Browse Output')
        browseOutputBtn.clicked.connect(self.browse_output_directory)

        outputLayout.addWidget(QLabel('Select Output Directory:'))
        outputLayout.addWidget(self.outputPathEntry)
        outputLayout.addWidget(browseOutputBtn)
        
        #last version info area
        self.versionLabel = QLabel("Last extracted version: None")
        versionLayout.addWidget(self.versionLabel)

        self.fileList = QListWidget()

        extractBtn = QPushButton('Extract Selected')
        extractBtn.clicked.connect(self.extract_zip)
        
        downloadOnlineBtn = QPushButton('Download Latest Online')
        downloadOnlineBtn.clicked.connect(self.download_online)
        
        checkUpdateBtn = QPushButton('Re-check Update')
        checkUpdateBtn.clicked.connect(self.check_update)
        
        mainLayout.addWidget(downloadOnlineBtn)
        mainLayout.addWidget(checkUpdateBtn)
        mainLayout.addLayout(sourceLayout)
        mainLayout.addWidget(QLabel('ElvUI Zip Files:'))
        mainLayout.addWidget(self.fileList)
        mainLayout.addLayout(outputLayout)
        mainLayout.addLayout(versionLayout)
        mainLayout.addWidget(extractBtn)
        self.btnMin.setFixedSize(30, 30)
        self.btnMax.setFixedSize(30, 30)
        self.btnClose.setFixedSize(30, 30)

        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 600, 400)

    def browse_directory(self):
        """Check the last source directory"""
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory', self.pathEntry.text())
        if directory:
            self.config['last_directory'] = directory
            save_config(self.config)
            self.pathEntry.setText(directory)
            self.scan_directory(directory)

    def browse_output_directory(self):
        """Check the last output directory"""
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory', self.outputPathEntry.text())
        if directory:
            self.config['last_extraction_path'] = directory
            save_config(self.config)
            self.outputPathEntry.setText(directory)

    def scan_directory(self, directory):
        """Scan the downloading directory to find elvui related zip file"""
        if directory:
            files = os.listdir(directory)
            zip_files = [file for file in files if file.endswith('.zip') and file.lower().startswith('elvui')]
            self.fileList.clear()
            self.fileList.addItems(zip_files)

    def extract_zip(self):
        """Function for extracting zip files"""
        selected_items = self.fileList.selectedItems()
        input_directory = self.pathEntry.text()
        output_directory = self.outputPathEntry.text()
    
        for item in selected_items:
            zip_path = os.path.join(input_directory, item.text())
            # Extract the contents of the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_directory)
            
            filename_no_ext = os.path.splitext(item.text())[0]
            version_name = filename_no_ext.replace("elvui-", "")
            match = re.search(r"(\d+\.\d+)", filename_no_ext, re.IGNORECASE)
            if match:
                version_name = match.group(1)  
            else:
                #Fallback in case regex fails: remove the prefix and extra characters
                version_name = filename_no_ext.replace("elvui-", "").strip()
            self.config['last_extracted_version'] = version_name
            save_config(self.config)
            self.versionLabel.setText("Last extracted version: " + version_name)
            
            #Ask user if they want to delete the zip file
            reply = QMessageBox.question(
                self,
                "Delete File",
                f"Do you want to delete {item.text()} after extraction?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                try:
                    os.remove(zip_path)
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not delete {item.text()}: {e}")
        #Start asynchronous update check once extraction
        self.checker = UpdateChecker()
        self.checker.updateChecked.connect(self.onUpdateChecked)
        self.checker.start()
    
        QMessageBox.information(self, 'Success', 'Selected files extracted.')
        #Update file list to remove deleted files
        self.scan_directory(input_directory)

        
    def download_online(self):
        """Shows a message box while downloading the latest version online."""
        wait_box = QMessageBox(self)
        wait_box.setWindowTitle("Please Wait")
        wait_box.setText("Downloading new version, please wait...")
        wait_box.setStandardButtons(QMessageBox.Ok)
        wait_box.setWindowModality(Qt.ApplicationModal)
        wait_box.show()
        QApplication.processEvents()
        
        """
        Uses Selenium in headless mode to trigger the download of the latest ElvUI zip.
        The download folder is set in the Chrome options.
        """
        try:
            #Set up Chrome in headless mode
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.get("https://tukui.org/elvui")
            download_button = driver.find_element(By.ID, "download-button")
            download_button.click()  
            time.sleep(3)  
            driver.quit()
            wait_box.close()
            QMessageBox.information(self, "Download", "Download initiated and (hopefully) completed.")
            self.scan_directory(self.config.get('last_directory', ''))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred during download: {e}")
            
    def onUpdateChecked(self, online_ver):
        """Check is new update available on official website"""
        self.online_version = online_ver
        last_local = self.config.get('last_extracted_version', '0.0')
        if online_ver == "":
            self.updateLabel.setText("Could not determine the ElvUI version.")
        else:
            try:
                if float(online_ver) > float(last_local):
                    self.updateLabel.setText(
                        f"<span style='color:red; font-weight:bold;'>New ElvUI version available: {online_ver}</span>"
                    )
                else:
                    self.updateLabel.setText("You have the latest version of ElvUI installed.")
            except ValueError:
                if online_ver != last_local:
                    self.updateLabel.setText(
                        f"<span style='color:red; font-weight:bold;'>New ElvUI version available: {online_ver}</span>"
                    )
                else:
                    self.updateLabel.setText("You have the latest version of ElvUI installed.")
    
    def check_update(self):
        """Show a message box while re-checking the online version, then update the UI."""
        wait_box = QMessageBox(self)
        wait_box.setWindowTitle("Please Wait")
        wait_box.setText("Checking for updates, please wait...")
        wait_box.setWindowModality(Qt.ApplicationModal)
        wait_box.show()
        QApplication.processEvents()

        online_version = check_online_version()
        wait_box.close()

        self.online_version = online_version
        last_local = self.config.get('last_extracted_version', '0.0')
        if online_version is None:
            self.updateLabel.setText("Could not determine the ElvUI version.")
        else:
            try:
                if float(online_version) > float(last_local):
                    self.updateLabel.setText(
                        f"<span style='color:red; font-weight:bold;'>New ElvUI version available: {online_version}</span>"
                    )
                else:
                    self.updateLabel.setText("You have the latest version of ElvUI installed.")
            except ValueError:
                if online_version != last_local:
                    self.updateLabel.setText(
                        f"<span style='color:red; font-weight:bold;'>New ElvUI version available: {online_version}</span>"
                    )
                else:
                    self.updateLabel.setText("You have the latest version of ElvUI installed.")
                    
    def apply_styles(app):
        """Style modification"""
        app.setStyle("Fusion")
        style_sheet = """

            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: #3c3f41;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4e5254;
            }
            QLineEdit {
                background-color: #3c3f41;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
            }
            QListWidget {
                background-color: #3c3f41;
                border: 1px solid #555;
                border-radius: 4px;
            }
            QLabel {
                font-size: 14px;
            }
        """
        app.setStyleSheet(style_sheet)
            
    def toggleMaxRestore(self):
        """Toggles between normal size and maximized."""
        if self.isMaximized():
            self.showNormal()
            self.btnMax.setText("⬜")
        else:
            self.showMaximized()
            self.btnMax.setText("❐")
            
    def mousePressEvent(self, event):
        """Remember the position of the mouse for window dragging."""
        if event.button() == Qt.LeftButton:
            if event.pos().y() <= self.titleBar.height():
                self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        """Move the window as the mouse moves."""
        if event.buttons() == Qt.LeftButton and self.dragPos is not None:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Reset drag position on mouse release."""
        if event.button() == Qt.LeftButton:
            self.dragPos = None

    


def main():
    config = load_config()
    app = QApplication(sys.argv)
    App.apply_styles(app)
    ex = App(config)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
