import requests
import threading
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QInputDialog
)
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import pyqtSignal, QObject

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class Worker(QObject):
    finished = pyqtSignal(object)

    def fetch_keys(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.finished.emit(data)
        except Exception as e:
            print(f"Error fetching keys: {e}")
            self.finished.emit([])

    def post_key(self, url, key_data):
        try:
            response = requests.post(url, json=key_data)
            response.raise_for_status()
            self.finished.emit(response.json())
        except Exception as e:
            print(f"Error adding key: {e}")
            self.finished.emit(None)

    def delete_key(self, url):
        try:
            response = requests.delete(url)
            response.raise_for_status()
            self.finished.emit(True)
        except Exception as e:
            print(f"Error deleting key: {e}")
            self.finished.emit(False)

    def generate_key(self, key_length: int = 2048):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_length
        )
        public_key = private_key.public_key()

        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return public_bytes.decode(), private_bytes.decode()


class ManageKeysWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Keys")
        self.api_base_url = "http://localhost:8000/keys"
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setFixedSize(1000, 700)
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 1, 1)
        gradient.setColorAt(0, QColor(238, 250, 253))
        gradient.setColorAt(1, QColor(200, 220, 250))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Key ID", "Algorithm ID", "Public Key", "Private Key (partial)"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.table)

        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.btn_addkey = QPushButton("Add a key", self)
        self.btn_addkey.clicked.connect(self.add_key)
        layout.addWidget(self.btn_addkey)

        self.btn_generate_rsa = QPushButton("Generate RSA Key", self)
        self.btn_generate_rsa.clicked.connect(self.generate_rsa_key)
        layout.addWidget(self.btn_generate_rsa)

        self.btn_deletekey = QPushButton("Delete a key", self)
        self.btn_deletekey.clicked.connect(self.delete_key)
        layout.addWidget(self.btn_deletekey)

        self.setLayout(layout)

    def generate_rsa_key(self):
        key_id, ok = QInputDialog.getText(self, "Generate RSA Key", "Enter Key ID:")
        if not ok or not key_id:
            return

        algorithm_id = "2"  # RSA

        try:
            worker = Worker()
            public_key, private_key = worker.generate_key()

            key_data = {
                "key_id": key_id,
                "algorithm_id": algorithm_id,
                "public_key": public_key,
                "private_key": private_key
            }

            def handle_response(response):
                if response is None:
                    QMessageBox.warning(self, "Error", "Nu s-a putut genera și salva cheia.")
                else:
                    QMessageBox.information(self, "Success", "Cheia RSA a fost generată și salvată.")
                    self.load_data()

            self.worker = Worker()
            self.worker.finished.connect(handle_response)
            thread = threading.Thread(target=self.worker.post_key, args=(self.api_base_url, key_data))
            thread.start()

        except Exception as e:
            print(f"Eroare la generarea cheii RSA: {e}")
            QMessageBox.warning(self, "Error", "A apărut o eroare la generarea cheii.")



    def load_data(self):
        self.worker = Worker()
        self.worker.finished.connect(self.populate_table)
        thread = threading.Thread(target=self.worker.fetch_keys, args=(self.api_base_url,))
        thread.start()

    def populate_table(self, keys):
        if not isinstance(keys, list):
            keys = []
        self.table.setRowCount(len(keys))
        for i, key in enumerate(keys):
            self.table.setItem(i, 0, QTableWidgetItem(str(key.get("key_id", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(str(key.get("algorithm_id", ""))))
            self.table.setItem(i, 2, QTableWidgetItem(key.get("public_key") or "N/A"))
            private = key.get("private_key", "N/A")
            self.table.setItem(i, 3, QTableWidgetItem(private[:50] + "..." if private != "N/A" else "N/A"))

    def add_key_to_db(self, key_id, algorithm_id, public_key, private_key):
        key_data = {
            "key_id": key_id,
            "algorithm_id": algorithm_id,
            "public_key": public_key,
            "private_key": private_key
        }

        success_flag = []

        def handle_response(response):
            success_flag.append(response is not None)

        self.worker = Worker()
        self.worker.finished.connect(handle_response)
        thread = threading.Thread(target=self.worker.post_key, args=(self.api_base_url, key_data))
        thread.start()
        thread.join()

        return success_flag[0] if success_flag else False

    def add_key(self):
        key_id, ok = QInputDialog.getText(self, "Add Key", "Enter Key ID:")
        if not ok or not key_id:
            return

        algorithm_id, ok = QInputDialog.getText(self, "Add Key", "Enter Algorithm ID (1-AES, 2-RSA):")
        if not ok or not algorithm_id:
            return

        public_key, ok = QInputDialog.getText(self, "Add Key", "Enter Public Key:")
        if not ok:
            return

        private_key = ""  

        if algorithm_id == "2":
            private_key, ok = QInputDialog.getText(self, "Add Key", "Enter Private Key:")
            if not ok:
                return

        key_data = {
            "key_id": key_id,
            "algorithm_id": algorithm_id,
            "public_key": public_key,
            "private_key": private_key
        }

        self.worker = Worker()
        self.worker.finished.connect(self.handle_add_response)
        thread = threading.Thread(target=self.worker.post_key, args=(self.api_base_url, key_data))
        thread.start()


    def handle_add_response(self, response):
        if response is None:
            QMessageBox.warning(self, "Error", "Failed to add key.")
        else:
            QMessageBox.information(self, "Success", "Key added successfully.")
            self.load_data()

    def delete_key(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Warning", "Please select a key to delete.")
            return

        key_id_item = self.table.item(selected, 0)
        if not key_id_item:
            QMessageBox.warning(self, "Warning", "Selected row has no key ID.")
            return

        key_id = key_id_item.text()
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete the key with ID {key_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        url = f"{self.api_base_url}/{key_id}"
        self.worker = Worker()
        self.worker.finished.connect(self.handle_delete_response)
        thread = threading.Thread(target=self.worker.delete_key, args=(url,))
        thread.start()

    def handle_delete_response(self, success):
        if success:
            QMessageBox.information(self, "Success", "Key deleted successfully.")
            self.load_data()
        else:
            QMessageBox.warning(self, "Error", "Failed to delete key.")
