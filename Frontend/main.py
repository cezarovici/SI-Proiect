import sys
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QInputDialog, QWidget, QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QLabel, QGridLayout, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor

class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
    
        self.setFixedSize(1000, 700)
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setColorAt(0, QColor(238, 250, 253))
        gradient.setColorAt(1, QColor(200, 220, 250))

        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

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
        

        self.buton_alg = QPushButton('Manage algorithms')
        self.buton_keys = QPushButton('Manage keys')
        self.buton_files = QPushButton('Manage files')
        self.buton_performances = QPushButton('View performances')
        self.buton_exit = QPushButton('Exit')

        self.buton_alg.setStyleSheet("""
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
        self.buton_alg.clicked.connect(self.afisare_tabel_algorithms)

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
        self.buton_keys.clicked.connect(self.afisare_tabel_keys)

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
        self.buton_files.clicked.connect(self.afisare_tabel_files)

        self.buton_performances.setStyleSheet("""
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

        self.buton_performances.clicked.connect(self.afisare_tabel_performances)

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

        #butoane secundare
        self.buton_addfile = QPushButton('Add new file', self)
        self.buton_addfile.hide()
        self.buton_addfile.setStyleSheet("""
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
        self.buton_addfile.clicked.connect(self.adauga_fisier)

        self.buton_add_key = QPushButton('Add a new key', self)
        self.buton_add_key.hide()
        self.buton_add_key.setStyleSheet("""
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
        
        self.buton_sterge_fisier = QPushButton('Delete a file')
        self.buton_sterge_fisier.setStyleSheet("""
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
        self.buton_sterge_fisier.clicked.connect(self.sterge_fisier)



        self.main_widgets = [self.buton_alg, self.buton_keys, self.buton_files, 
                             self.buton_exit, self.copyrightt, self.subtitlu, 
                             self.titlu, self.buton_performances]

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addWidget(self.titlu)
        self.vbox_layout.addWidget(self.subtitlu)
        self.vbox_layout.addSpacerItem(QSpacerItem(40, 80, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.vbox_layout.addWidget(self.buton_alg)
        self.vbox_layout.addWidget(self.buton_keys)
        self.vbox_layout.addWidget(self.buton_files)
        self.vbox_layout.addWidget(self.buton_performances)
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

    ########################### afisarea tabelului in "Manage algorithms" ################################
    def afisare_tabel_algorithms(self):
        
        for widget in self.main_widgets:
            widget.hide()

        try:
            base_path = os.path.dirname(__file__) 
            json_path = os.path.join(base_path, "algorithms.json")

            with open(json_path, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            print("Nu am gasit niciun fisier JSON.")
            return
        
        algoritmi = data["algorithms"]
        
        self.tabel_algor = QTableWidget(self)
        self.tabel_algor.setRowCount(len(algoritmi))
        self.tabel_algor.setColumnCount(6)  
        self.tabel_algor.setHorizontalHeaderLabels(["ID", "Name", "Type", "Parameters", "Created At", "Updated At"])
        self.tabel_algor.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF55;
                color: white;
                font-size: 16px;
                padding: 5px;
                border: 2px solid black;
            }                                       
        """)
        self.tabel_algor.setAlternatingRowColors(True)
        self.tabel_algor.setStyleSheet("""
            QTableWidget {
                    background-color: #eefafd;
                    border: 2px solid black;
                    }
                                    
            QTableWidget::item:nth-child(even) {
                background-color: #dff0d8;
            }
            QTableWidget::item:nth-child(odd) {
                background-color: #dbd9db;
                border: 2px solid black;
            }                        
        """)
        self.tabel_algor.setMinimumSize(700, 400)  
        self.tabel_algor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        for i, algoritm in enumerate(algoritmi):
            self.tabel_algor.setItem(i, 0, QTableWidgetItem(str(algoritm["algorithm_id"])))
            self.tabel_algor.setItem(i, 1, QTableWidgetItem(algoritm["name"]))
            self.tabel_algor.setItem(i, 2, QTableWidgetItem(algoritm["type"]))
            self.tabel_algor.setItem(i, 3, QTableWidgetItem(json.dumps(algoritm["parameters"])))
            self.tabel_algor.setItem(i, 4, QTableWidgetItem(algoritm["created_at"])) 
            self.tabel_algor.setItem(i, 5, QTableWidgetItem(algoritm["updated_at"]))

        self.tabel_algor.resizeColumnsToContents()
        self.vbox_layout.addWidget(self.tabel_algor)

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


        self.buton_back.clicked.connect(self.show_menu)
        self.nvl_func(self.tabel_algor)
        self.vbox_layout.addWidget(self.buton_back)
        


    ########################### afisarea tabelului in "Manage keys" ################################
    def afisare_tabel_keys(self):
        for widget in self.main_widgets:
            widget.hide()

        try:
            base_path = os.path.dirname(__file__) 
            json_path = os.path.join(base_path, "keys.json")

            with open(json_path, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            print("Nu am gasit niciun fisier JSON.")
            return
        
        keyss = data["keys"]

        self.tabel_keys = QTableWidget(self)
        self.tabel_keys.setRowCount(len(keyss))
        self.tabel_keys.setColumnCount(8)  
        self.tabel_keys.setHorizontalHeaderLabels([
            "ID", "Algorithm ID", "Key Name", "Key Value", 
            "Public Key", "Private Key", "Creation Date", "Expiration Date"
        ])

        self.tabel_keys.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF55;
                color: white;
                font-size: 16px;
                padding: 5px;
                border: 2px solid black;
            }                                       
        """)
        self.tabel_keys.setAlternatingRowColors(True)
        self.tabel_keys.setStyleSheet("""
            QTableWidget {
                    background-color: #eefafd;
                    border: 2px solid black;
                    }
                                    
            QTableWidget::item:nth-child(even) {
                background-color: #dff0d8;
            }
            QTableWidget::item:nth-child(odd) {
                background-color: #dbd9db;
                border: 2px solid black;
            }                        
        """)
        self.tabel_keys.setMinimumSize(700, 400)  
        self.tabel_keys.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for i, key in enumerate(keyss):
            self.tabel_keys.setItem(i, 0, QTableWidgetItem(str(key["key_id"])))
            self.tabel_keys.setItem(i, 1, QTableWidgetItem(str(key["algorithm_id"])))
            self.tabel_keys.setItem(i, 2, QTableWidgetItem(key["key_name"]))
            self.tabel_keys.setItem(i, 3, QTableWidgetItem(key["key_value"]))
            self.tabel_keys.setItem(i, 4, QTableWidgetItem(key["public_key"]))
            self.tabel_keys.setItem(i, 5, QTableWidgetItem(key["private_key"]))
            self.tabel_keys.setItem(i, 6, QTableWidgetItem(key["creation_date"])) 
            self.tabel_keys.setItem(i, 7, QTableWidgetItem(str(key["expiration_date"])))

        self.tabel_keys.resizeColumnsToContents()
        self.vbox_layout.addWidget(self.tabel_keys)

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

        # self.buton_add_key = QPushButton('Add a new key', self)
        # self.buton_add_key.setStyleSheet("""
        #     QPushButton {
        #         background-color: #4CAF50;
        #         color: white;
        #         padding: 15px 32px;
        #         text-align: center;
        #         font-size: 16px;
        #         margin: 4px 2px;
        #         border-radius: 5px;
        #     }
        #     QPushButton:hover {
        #         background-color: #3e8e41;
        #     }
        # """)

        self.buton_back.clicked.connect(self.show_menu)
        self.nvl_func(self.tabel_keys)
        self.vbox_layout.addWidget(self.buton_back)
        self.vbox_layout.addWidget(self.buton_add_key)

    
    ########################### afisarea tabelului in "Manage files" ################################
    def afisare_tabel_files(self):
        for widget in self.main_widgets:
            widget.hide()

        try:
            base_path = os.path.dirname(__file__) 
            json_path = os.path.join(base_path, "files.json")

            with open(json_path, "r") as json_file:
                data = json.load(json_file)

        except FileNotFoundError:
            print("Nu am gasit niciun fisier JSON.")
            return
        
        filess = data["files"]

        self.tabel_files = QTableWidget(self)
        self.tabel_files.setRowCount(len(filess))
        self.tabel_files.setColumnCount(9)  
        self.tabel_files.setHorizontalHeaderLabels([
            "File ID", "Original Path", "Encrypted Path", "Original Hash", 
            "Encrypted Hash", "Algorithm ID", "Key ID", "Encryption Date", "Last Access"
        ])

        self.tabel_files.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF55;
                color: white;
                font-size: 16px;
                padding: 5px;
                border: 2px solid black;
            }                                       
        """)
        self.tabel_files.setAlternatingRowColors(True)
        self.tabel_files.setStyleSheet("""
            QTableWidget {
                    background-color: #eefafd;
                    border: 2px solid black;
                    }
                                    
            QTableWidget::item:nth-child(even) {
                background-color: #dff0d8;
            }
            QTableWidget::item:nth-child(odd) {
                background-color: #dbd9db;
                border: 2px solid black;
            }                        
        """)
        self.tabel_files.setMinimumSize(700, 400)  
        self.tabel_files.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for i, file in enumerate(filess):
            self.tabel_files.setItem(i, 0, QTableWidgetItem(str(file["file_id"])))
            self.tabel_files.setItem(i, 1, QTableWidgetItem(file["original_path"]))
            self.tabel_files.setItem(i, 2, QTableWidgetItem(file["encrypted_path"]))
            self.tabel_files.setItem(i, 3, QTableWidgetItem(file["original_hash"] if file["original_hash"] else "NULL"))
            self.tabel_files.setItem(i, 4, QTableWidgetItem(file["encrypted_hash"] if file["encrypted_hash"] else "NULL"))
            self.tabel_files.setItem(i, 5, QTableWidgetItem(str(file["algorithm_id"])))
            self.tabel_files.setItem(i, 6, QTableWidgetItem(str(file["key_id"])))
            self.tabel_files.setItem(i, 7, QTableWidgetItem(file["encryption_date"])) 
            self.tabel_files.setItem(i, 8, QTableWidgetItem(file["last_access"] if file["last_access"] else "NULL"))

        self.tabel_files.resizeColumnsToContents()
        self.vbox_layout.addWidget(self.tabel_files)

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

        # self.buton_addfile = QPushButton('Add new file', self)
        # self.buton_addfile.setStyleSheet("""
        #     QPushButton {
        #         background-color: #4CAF50;
        #         color: white;
        #         padding: 15px 32px;
        #         text-align: center;
        #         font-size: 16px;
        #         margin: 4px 2px;
        #         border-radius: 5px;
        #     }
        #     QPushButton:hover {
        #         background-color: #3e8e41;
        #     }
        # """)

        # self.buton_sterge_fisier = QPushButton('Delete a file')
        # self.buton_sterge_fisier.setStyleSheet("""
        #     QPushButton {
        #         background-color: #4CAF50;
        #         color: white;
        #         padding: 15px 32px;
        #         text-align: center;
        #         font-size: 16px;
        #         margin: 4px 2px;
        #         border-radius: 5px;
        #     }
        #     QPushButton:hover {
        #         background-color: #3e8e41;
        #     }
        # """)
        # self.buton_sterge_fisier.clicked.connect(self.sterge_fisier)

        

        self.buton_back.clicked.connect(self.show_menu)
        self.nvl_func(self.tabel_files)
        
        self.vbox_layout.addWidget(self.buton_back)
        self.vbox_layout.addWidget(self.buton_addfile)
        self.vbox_layout.addWidget(self.buton_sterge_fisier)
        # self.buton_addfile.clicked.connect(self.adauga_fisier)

    ########################### afisarea tabelului in "View performances" ################################
    def afisare_tabel_performances(self):
        for widget in self.main_widgets:
            widget.hide()

        try:
            base_path = os.path.dirname(__file__) 
            json_path = os.path.join(base_path, "performances.json")

            with open(json_path, "r") as json_file:
                data = json.load(json_file)

        except FileNotFoundError:
            print("Nu am gasit niciun fisier JSON.")
            return
        
        perf = data["performances"]

        self.tabel_performances = QTableWidget(self)
        self.tabel_performances.setRowCount(len(perf))
        self.tabel_performances.setColumnCount(9)  
        self.tabel_performances.setHorizontalHeaderLabels([
            "Performance ID", "File ID", "Algorithm ID", "Key ID", "Operation Type", 
            "Execution Time (ms)", "Memory Usage (MB)", "Success", "Error Message"
        ])

        self.tabel_performances.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #4CAF55;
                color: white;
                font-size: 16px;
                padding: 5px;
                border: 2px solid black;
            }                                       
        """)
        self.tabel_performances.setAlternatingRowColors(True)
        self.tabel_performances.setStyleSheet("""
            QTableWidget {
                    background-color: #eefafd;
                    border: 2px solid black;
                    }
                                    
            QTableWidget::item:nth-child(even) {
                background-color: #dff0d8;
            }
            QTableWidget::item:nth-child(odd) {
                background-color: #dbd9db;
                border: 2px solid black;
            }                        
        """)
        self.tabel_performances.setMinimumSize(700, 400)  
        self.tabel_performances.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for i, entry in enumerate(perf):
            self.tabel_performances.setItem(i, 0, QTableWidgetItem(str(entry["performance_id"])))
            self.tabel_performances.setItem(i, 1, QTableWidgetItem(str(entry["file_id"])))
            self.tabel_performances.setItem(i, 2, QTableWidgetItem(str(entry["algorithm_id"])))
            self.tabel_performances.setItem(i, 3, QTableWidgetItem(str(entry["key_id"])))
            self.tabel_performances.setItem(i, 4, QTableWidgetItem(entry["operation_type"]))
            self.tabel_performances.setItem(i, 5, QTableWidgetItem(str(entry["execution_time_ms"])))
            self.tabel_performances.setItem(i, 6, QTableWidgetItem(str(entry["memory_usage_mb"])))
            self.tabel_performances.setItem(i, 7, QTableWidgetItem("Yes" if entry["success"] else "No"))
            self.tabel_performances.setItem(i, 8, QTableWidgetItem(entry["error_message"] if entry["error_message"] else "NULL"))

        self.tabel_performances.resizeColumnsToContents()
        self.vbox_layout.addWidget(self.tabel_performances)

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
        
        self.buton_back.clicked.connect(self.show_menu)
        self.nvl_func(self.tabel_performances)
        self.vbox_layout.addWidget(self.buton_back)
        
    ###### reafisare butoane din meniul principal #########
    def show_menu(self):
        for widget in self.main_widgets:
            widget.show()

        self.buton_back.setParent(None)
        self.buton_addfile.setParent(None)
        self.buton_sterge_fisier.setParent(None)
        for i in range(self.vbox_layout.count()):
            widget = self.vbox_layout.itemAt(i).widget()
            if isinstance(widget, QTableWidget):  
                widget.hide()

    ###afisare valori de null in celulele goale
    def nvl_func(self, tabel):
        for row in range(tabel.rowCount()):
            for col in range(tabel.columnCount()):
                item = tabel.item(row, col)
                if item is None or item.text().strip() == "":
                    tabel.setItem(row, col, QTableWidgetItem("NULL"))


    def adauga_fisier(self):
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*.*)")
        
        if not file_path:  
            return

        encrypted_path = file_path + ".enc"  # Poți schimba acest format

        # Citire și actualizare JSON
        try:
            base_path = os.path.dirname(__file__) 
            json_path = os.path.join(base_path, "files.json")
            with open(json_path, "r") as json_file:
                data = json.load(json_file)
            key_id = max((file["key_id"] for file in data["files"]), default=99) + 1  
            algorithm_id = max((file["algorithm_id"] for file in data["files"]), default=199) + 1
        except FileNotFoundError:
            data = {"files": []}

        nou_fisier = {
            "file_id": len(data["files"]) + 1,
            "original_path": file_path,
            "encrypted_path": encrypted_path,
            "original_hash": "NULL",
            "encrypted_hash": "NULL",
            "algorithm_id": algorithm_id,
            "key_id": key_id,
            "encryption_date": "2025-04-30 10:45:00",
            "last_access": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        data["files"].append(nou_fisier)

        
        with open(json_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        QMessageBox.information(self, "Success", "Added file")

    def sterge_fisier(self):
        selected_row = self.tabel_files.currentRow()  

        if selected_row == -1:  
            QMessageBox.warning(self, "Warning", "Select a file to delete!")
            return

        file_id = self.tabel_files.item(selected_row, 0).text()  

        try:
            base_path = os.path.dirname(__file__) 
            json_path = os.path.join(base_path, "files.json")
            with open(json_path, "r") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            QMessageBox.warning(self, "Warning", "Files.json not found!")
            return

        initial_length = len(data["files"])
        data["files"] = [file for file in data["files"] if str(file["file_id"]) != file_id]

        if len(data["files"]) == initial_length:
            QMessageBox.warning(self, "Warning", f"File with ID {file_id} not found!")
            return

        
        with open(json_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        QMessageBox.information(self, "Success", f"File with ID {file_id} deleted successfully!")

        
        self.tabel_files.removeRow(selected_row)

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = UserInterface()
    sys.exit(app.exec_())


    '''
    CREATE TABLE algorithms (
    algorithm_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL,
    type ENUM('symmetric', 'asymmetric') NOT NULL,
    parameters TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE keys (
    key_id INT PRIMARY KEY AUTO_INCREMENT,
    algorithm_id INT NOT NULL,
    key_name VARCHAR(100) NOT NULL,
    key_value TEXT,
    public_key TEXT,
    private_key TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiration_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(algorithm_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE files (
    file_id INT PRIMARY KEY AUTO_INCREMENT,
    original_path VARCHAR(255) NOT NULL,
    encrypted_path VARCHAR(255) NOT NULL,
    original_hash VARCHAR(64),
    encrypted_hash VARCHAR(64),
    algorithm_id INT NOT NULL,
    key_id INT NOT NULL,
    encryption_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_access TIMESTAMP,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(algorithm_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (key_id) REFERENCES keys(key_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE performance (
    performance_id INT PRIMARY KEY AUTO_INCREMENT,
    file_id INT NOT NULL,
    algorithm_id INT NOT NULL,
    key_id INT NOT NULL,
    operation_type ENUM('encrypt', 'decrypt') NOT NULL,
    execution_time_ms FLOAT NOT NULL,
    memory_usage_mb FLOAT NOT NULL,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES files(file_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (algorithm_id) REFERENCES algorithms(algorithm_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (key_id) REFERENCES keys(key_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

    ---------------------------

    INSERT INTO algorithms (name, type, parameters)
VALUES ('AES-256', 'symmetric', '{"key_size": 256, "mode": "CBC"}'),
       ('RSA-2048', 'asymmetric', '{"key_size": 2048}'),
       ('ChaCha20', 'symmetric', '{"key_size": 256, "nonce_size": 12}');

    
    
    '''