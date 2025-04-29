import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QGridLayout, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt

class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
    
        self.setStyleSheet("""
            background: #eefafd """)

        self.titlu = QLabel('Local File Management', self)
        self.titlu.setStyleSheet("font-size: 43px; font-weight: bold; text-align: center;")
        self.titlu.setFixedWidth(500)
        self.titlu.setFixedHeight(100)

        self.subtitlu = QLabel('The safest place for your files.', self)
        self.subtitlu.setStyleSheet("font-size: 23px; font-weight: bold; text-align: center;")
        self.subtitlu.setFixedWidth(500)

        self.copyrightt = QLabel('© SI 2025 \nApetroaei Cezar-Stefan\nSimion Iustin-Denis\nAnastasiei Narcis-Stefan', self)
        self.copyrightt.setStyleSheet("font-size: 11px; font-weight: bold; text-align: center;")
        self.copyrightt.setFixedWidth(500)
        

        self.buton_files = QPushButton('Manage files')
        self.buton_keys = QPushButton('Manage keys')
        self.buton_about = QPushButton('About')
        self.buton_exit = QPushButton('Exit')

        self.buton_files.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)
        self.buton_files.clicked.connect(self.afisare_tabel)

        self.buton_keys.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)
        #self.buton_keys.setMaximumWidth(200)

        self.buton_about.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)

        self.buton_exit.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)
        self.buton_exit.clicked.connect(self.close)
        self.main_widgets = [self.buton_files, self.buton_keys, self.buton_about, self.buton_exit, self.copyrightt]

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addWidget(self.titlu)
        self.vbox_layout.addWidget(self.subtitlu)
        self.vbox_layout.addSpacerItem(QSpacerItem(40, 80, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.vbox_layout.addWidget(self.buton_files)
        self.vbox_layout.addWidget(self.buton_keys)
        self.vbox_layout.addWidget(self.buton_about)
        self.vbox_layout.addWidget(self.buton_exit)
        self.vbox_layout.addSpacerItem(QSpacerItem(40, 80, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.vbox_layout.addWidget(self.copyrightt)

        self.button_widget = QWidget()
        self.button_widget.setLayout(self.vbox_layout)

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.button_widget, 0, 0, 1, 1, Qt.AlignCenter)

        self.setLayout(self.grid_layout)

        self.setGeometry(100, 100, 900, 600)
        self.setWindowTitle('Local File Management - SI Proiect')
        self.show()

    def afisare_tabel(self):

        for widget in self.main_widgets:
            widget.hide()
        
        tabel = QTableWidget(self)
        tabel.setRowCount(5) 
        tabel.setColumnCount(5)  

        for i in range(5):
            for j in range(5):
                tabel.setItem(i, j, QTableWidgetItem(f' '))

        tabel.setHorizontalHeaderLabels(['Filename', 'Path', 'Dimension', 'Encryption Date', 'State'])
        tabel.setVerticalHeaderLabels([f'No Filename {i + 1}' for i in range(5)])
        tabel.resizeColumnsToContents()

        self.vbox_layout.addWidget(tabel)
        self.buton_files.setDisabled(True)

        self.buton_back = QPushButton('Back', self)
        self.buton_back.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)
        self.vbox_layout.addWidget(self.buton_back)

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = UserInterface()
    sys.exit(app.exec_())