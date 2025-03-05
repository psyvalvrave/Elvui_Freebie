import sys
import os
import zipfile
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QListWidget, QFileDialog, QMessageBox)

config_file = 'config_Elvui_Freebie.json'

def load_config():
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'last_directory': '', 'last_extraction_path': '', 'last_extracted_version': ''}

def save_config(config):
    with open(config_file, 'w') as f:
        json.dump(config, f)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.config = load_config()
        self.pathEntry.setText(self.config.get('last_directory', ''))
        self.outputPathEntry.setText(self.config.get('last_extraction_path', ''))
        self.versionLabel.setText("Last extracted version: " + self.config.get('last_extracted_version', 'None'))
        self.scan_directory(self.config.get('last_directory', ''))  
    def initUI(self):
        self.setWindowTitle('Elvui Freebie')

        # Layouts
        mainLayout = QVBoxLayout()
        sourceLayout = QHBoxLayout()
        outputLayout = QHBoxLayout()
        versionLayout = QHBoxLayout()

        # Source directory components
        self.pathEntry = QLineEdit()
        browseSourceBtn = QPushButton('Browse Source')
        browseSourceBtn.clicked.connect(self.browse_directory)

        sourceLayout.addWidget(QLabel('Select Source Directory:'))
        sourceLayout.addWidget(self.pathEntry)
        sourceLayout.addWidget(browseSourceBtn)

        # Output directory components
        self.outputPathEntry = QLineEdit()
        browseOutputBtn = QPushButton('Browse Output')
        browseOutputBtn.clicked.connect(self.browse_output_directory)

        outputLayout.addWidget(QLabel('Select Output Directory:'))
        outputLayout.addWidget(self.outputPathEntry)
        outputLayout.addWidget(browseOutputBtn)

        # Version display
        self.versionLabel = QLabel("Last extracted version: None")
        versionLayout.addWidget(self.versionLabel)

        # File list
        self.fileList = QListWidget()

        # Extract button
        extractBtn = QPushButton('Extract Selected')
        extractBtn.clicked.connect(self.extract_zip)

        # Adding widgets to the main layout
        mainLayout.addLayout(sourceLayout)
        mainLayout.addWidget(QLabel('ElvUI Zip Files:'))
        mainLayout.addWidget(self.fileList)
        mainLayout.addLayout(outputLayout)
        mainLayout.addLayout(versionLayout)
        mainLayout.addWidget(extractBtn)

        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 600, 400)


    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory', self.pathEntry.text())
        if directory:
            self.config['last_directory'] = directory
            save_config(self.config)
            self.pathEntry.setText(directory)
            self.scan_directory(directory)

    def browse_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory', self.outputPathEntry.text())
        if directory:
            self.config['last_extraction_path'] = directory
            save_config(self.config)
            self.outputPathEntry.setText(directory)

    def scan_directory(self, directory):
        if directory:
            files = os.listdir(directory)
            zip_files = [file for file in files if file.endswith('.zip') and file.startswith('elvui')]
            self.fileList.clear()
            self.fileList.addItems(zip_files)

    def extract_zip(self):
        selected_items = self.fileList.selectedItems()
        input_directory = self.pathEntry.text()
        output_directory = self.outputPathEntry.text()
        for item in selected_items:
            zip_path = os.path.join(input_directory, item.text())
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_directory)
            # Save the version extracted
            version_name = os.path.splitext(item.text())[0]
            self.config['last_extracted_version'] = version_name
            save_config(self.config)
            self.versionLabel.setText("Last extracted version: " + version_name)
        QMessageBox.information(self, 'Success', 'Selected files extracted')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
