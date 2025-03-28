# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QFrame, QStyle
from PyQt5.QtCore import Qt
from config import BOX_STYLE

class CustomMessageBox(QDialog):
    def __init__(self, parent=None, title="Message", text="", icon_type=None, buttons=True):
        """
        :param parent: Parent widget.
        :param title: Title text for the custom title bar.
        :param text: Message text to display.
        :param icon_type: A string ("information", "warning", "critical", "question") to indicate the icon type.
        :param buttons: If True, adds an OK button; if False, no buttons are added.
        """
        super().__init__(parent)
        self.icon_type = icon_type
        #Remove native title bar to allow a custom title bar
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.initUI(title, text, buttons)
        
    def initUI(self, title, text, buttons):
        layout = QVBoxLayout(self)
        
        titleBar = QWidget(self)
        titleBar.setObjectName("titleBar")
        titleBarLayout = QHBoxLayout(titleBar)
        titleBarLayout.setContentsMargins(5, 5, 5, 5)
        
        self.titleLabel = QLabel(title, titleBar)
        titleBarLayout.addWidget(self.titleLabel)
        titleBarLayout.addStretch(1)
        
        btnClose = QPushButton("X", titleBar)
        btnClose.setObjectName("btnClose")
        btnClose.setFixedSize(30, 30)
        btnClose.clicked.connect(self.close)
        titleBarLayout.addWidget(btnClose)
        
        layout.addWidget(titleBar)
        
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: white;")
        line.setFixedHeight(2)
        layout.addWidget(line)
        
        #Message area with optional icon
        messageLayout = QHBoxLayout()
        messageLayout.setContentsMargins(0, 0, 0, 0)
        messageLayout.setSpacing(5)
        
        if self.icon_type:
            icon = None
            itype = self.icon_type.lower()
            if itype == "information":
                icon = self.style().standardIcon(QStyle.SP_MessageBoxInformation)
            elif itype == "warning":
                icon = self.style().standardIcon(QStyle.SP_MessageBoxWarning)
            elif itype == "critical":
                icon = self.style().standardIcon(QStyle.SP_MessageBoxCritical)
            elif itype == "question":
                icon = self.style().standardIcon(QStyle.SP_MessageBoxQuestion)
            
            if icon:
                icon_label = QLabel(self)
                icon_label.setPixmap(icon.pixmap(48, 48))
                icon_label.setContentsMargins(0, 0, 0, 0)
                icon_label.setAlignment(Qt.AlignVCenter)
                messageLayout.addWidget(icon_label)
        
        messageLabel = QLabel(text, self)
        messageLabel.setWordWrap(True)
        messageLabel.setContentsMargins(0, 0, 0, 0)
        messageLabel.setAlignment(Qt.AlignVCenter)
        messageLayout.addWidget(messageLabel)
        
        layout.addLayout(messageLayout)
        
        if buttons:
            btnOk = QPushButton("OK", self)
            btnOk.clicked.connect(self.accept)
            btnLayout = QHBoxLayout()
            btnLayout.setContentsMargins(0, 0, 0, 0)
            btnLayout.addStretch(1)
            btnLayout.addWidget(btnOk)
            layout.addLayout(btnLayout)
        
        self.setStyleSheet(BOX_STYLE)
