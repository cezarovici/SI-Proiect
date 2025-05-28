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
            self.finished.emit({"type": "fetch", "data": response.json()})
        except Exception as e:
            print(f"Error fetching keys: {e}")
            self.finished.emit({"type": "fetch", "data": []})

    def post_key(self, url, key_data):
        try:
            response = requests.post(url, json=key_data)
            response.raise_for_status()
            self.finished.emit({"type": "post", "success": True, "data": response.json()})
        except Exception as e:
            print(f"Error adding key: {e}")
            error_data = None
            try: error_data = e.response.json()
            except: pass
            self.finished.emit({"type": "post", "success": False, "error": error_data or str(e)})

    def delete_key(self, url):
        try:
            response = requests.delete(url)
            response.raise_for_status()
            self.finished.emit({"type": "delete", "success": True})
        except Exception as e:
            print(f"Error deleting key: {e}")
            self.finished.emit({"type": "delete", "success": False})

    def generate_key(self, key_length: int = 2048):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_length)
        public_key = private_key.public_key()
        private_bytes = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
        public_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return public_bytes.decode(), private_bytes.decode()

class ManageKeysWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Keys")
        self.api_base_url = "http://localhost:8000/keys/"
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
            QPushButton { background-color: #4CAF50; color: white; padding: 15px 32px; font-size: 16px; border-radius: 5px; }
            QPushButton:hover { background-color: #3e8e41; }
        """)
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5) # Am adăugat Key Name și am scos cheile
        self.table.setHorizontalHeaderLabels(["Key ID", "Algorithm ID", "Key Name", "Has Public Key?", "Has Private/Value?"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        self.btn_addkey = QPushButton("Add AES Key", self)
        self.btn_addkey.clicked.connect(self.add_aes_key)
        layout.addWidget(self.btn_addkey)

        self.btn_generate_rsa = QPushButton("Generate RSA Key", self)
        self.btn_generate_rsa.clicked.connect(self.generate_rsa_key)
        layout.addWidget(self.btn_generate_rsa)

        self.btn_deletekey = QPushButton("Delete Selected Key", self)
        self.btn_deletekey.clicked.connect(self.delete_key_action)
        layout.addWidget(self.btn_deletekey)

        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def load_data(self):
        self.worker = Worker()
        self.worker.finished.connect(self.handle_response)
        thread = threading.Thread(target=self.worker.fetch_keys, args=(self.api_base_url,))
        thread.start()

    def handle_response(self, response):
        if not isinstance(response, dict) or "type" not in response:
            QMessageBox.warning(self, "Error", "Invalid response.")
            return

        rtype = response.get("type")
        if rtype == "fetch":
            self.populate_table(response.get("data", []))
        elif rtype == "post":
            if response.get("success"):
                QMessageBox.information(self, "Success", "Key added successfully.")
                self.load_data()
            else:
                QMessageBox.warning(self, "Error", f"Failed to add key: {response.get('error')}")
        elif rtype == "delete":
            if response.get("success"):
                QMessageBox.information(self, "Success", "Key deleted successfully.")
                self.load_data()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete key.")

    def populate_table(self, keys):
        if not isinstance(keys, list): keys = []
        self.table.setRowCount(len(keys))
        for i, key in enumerate(keys):
            self.table.setItem(i, 0, QTableWidgetItem(str(key.get("key_id", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(str(key.get("algorithm_id", ""))))
            self.table.setItem(i, 2, QTableWidgetItem(key.get("key_name", "N/A")))
            self.table.setItem(i, 3, QTableWidgetItem("Yes" if key.get("public_key") else "No"))
            # Verificăm dacă e AES (are key_value) sau RSA (are private_key)
            has_private = "Yes" if (key.get("private_key") or key.get("key_value")) else "No"
            self.table.setItem(i, 4, QTableWidgetItem(has_private))
        self.table.resizeColumnsToContents()

    def add_aes_key(self):
        key_name, ok1 = QInputDialog.getText(self, "Add AES Key", "Enter Key Name:")
        if not ok1 or not key_name: return

        key_value, ok2 = QInputDialog.getText(self, "Add AES Key", "Enter AES Key/Password:")
        if not ok2 or not key_value: return

        key_data = {
            "algorithm_id": 1, # AES
            "key_name": key_name,
            "key_value": key_value,
            "public_key": None,
            "private_key": None
        }
        self.post_key_thread(key_data)

    def generate_rsa_key(self):
        key_name, ok = QInputDialog.getText(self, "Generate RSA Key", "Enter Key Name:")
        if not ok or not key_name: return

        try:
            worker = Worker()
            public_key, private_key = worker.generate_key()
            key_data = {
                "algorithm_id": 2, # RSA
                "key_name": key_name,
                "public_key": public_key,
                "private_key": private_key,
                "key_value": None
            }
            self.post_key_thread(key_data)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to generate RSA key: {e}")

    def post_key_thread(self, key_data):
        self.worker = Worker()
        self.worker.finished.connect(self.handle_response)
        thread = threading.Thread(target=self.worker.post_key, args=(self.api_base_url, key_data))
        thread.start()

    def delete_key_action(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Warning", "Please select a key to delete.")
            return

        key_id_item = self.table.item(selected, 0)
        if not key_id_item:
            QMessageBox.warning(self, "Warning", "Selected row has no key ID.")
            return

        key_id = key_id_item.text()
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete key ID {key_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes: return

        url = f"{self.api_base_url}{key_id}"
        self.worker = Worker()
        self.worker.finished.connect(self.handle_response)
        thread = threading.Thread(target=self.worker.delete_key, args=(url,))
        thread.start()