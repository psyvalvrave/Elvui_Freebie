# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QFrame, QStyle
from PyQt5.QtCore import Qt
from config import BOX_STYLE

class CustomQuestionBox(QDialog):
    def __init__(self, parent=None, title="Question", text=""):
        super().__init__(parent)
        # Remove native window frame for a custom look
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.initUI(title, text)
        
    def initUI(self, title, text):
        layout = QVBoxLayout(self)
        
        #Custom title bar
        titleBar = QWidget(self)
        titleBar.setObjectName("titleBar")
        titleBarLayout = QHBoxLayout(titleBar)
        titleBarLayout.setContentsMargins(5, 5, 5, 5)
        
        self.titleLabel = QLabel(title, titleBar)
        titleBarLayout.addWidget(self.titleLabel)
        titleBarLayout.addStretch(1)
        
        #Only close button in the title bar
        btnClose = QPushButton("X", titleBar)
        btnClose.setFixedSize(30, 30)
        btnClose.clicked.connect(self.reject)
        titleBarLayout.addWidget(btnClose)
        
        layout.addWidget(titleBar)
        
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: white;")
        line.setFixedHeight(2)
        layout.addWidget(line)
        
        messageLayout = QHBoxLayout()
        icon = self.style().standardIcon(QStyle.SP_MessageBoxQuestion)
        icon_label = QLabel(self)
        icon_label.setPixmap(icon.pixmap(48, 48))
        icon_label.setContentsMargins(10, 0, 0, 0)
        messageLayout.addWidget(icon_label)
        
        #Message text
        messageLabel = QLabel(text, self)
        messageLabel.setWordWrap(True)
        messageLabel.setContentsMargins(0, 0, 20, 0)
        messageLayout.addWidget(messageLabel)
        layout.addLayout(messageLayout)
        
        #Buttons layout
        btnLayout = QHBoxLayout()
        btnLayout.addStretch(1)
        btnYes = QPushButton("Yes", self)
        btnYes.clicked.connect(self.accept)
        btnLayout.addWidget(btnYes)
        btnNo = QPushButton("No", self)
        btnNo.clicked.connect(self.reject)
        btnLayout.addWidget(btnNo)
        layout.addLayout(btnLayout)
        
        self.setStyleSheet(BOX_STYLE)