import requests
import threading
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QInputDialog, QLineEdit
)
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import pyqtSignal, QObject

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


class ManageKeysWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Keys")
        self.api_base_url = "http://localhost:8000/keys"  # URL API chei
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
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Key ID", "Algorithm ID", "Key Name", "Key Value",
            "Public Key", "Private Key", "Creation Date",
            "Expiration Date", "Is Active"
        ])
        layout.addWidget(self.table)

        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.btn_addkey = QPushButton("Add a key", self)
        self.btn_addkey.clicked.connect(self.add_key)
        layout.addWidget(self.btn_addkey)

        self.btn_deletekey = QPushButton("Delete a key", self)
        self.btn_deletekey.clicked.connect(self.delete_key)
        layout.addWidget(self.btn_deletekey)

        self.setLayout(layout)

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
            self.table.setItem(i, 2, QTableWidgetItem(key.get("key_name", "")))
            self.table.setItem(i, 3, QTableWidgetItem(key.get("key_value") or "N/A"))
            self.table.setItem(i, 4, QTableWidgetItem(key.get("public_key") or "N/A"))
            self.table.setItem(i, 5, QTableWidgetItem(key.get("private_key") or "N/A"))
            self.table.setItem(i, 6, QTableWidgetItem(key.get("creation_date", "")))
            self.table.setItem(i, 7, QTableWidgetItem(key.get("expiration_date") or "N/A"))
            self.table.setItem(i, 8, QTableWidgetItem("Active" if key.get("is_active") else "Inactive"))

    def add_key(self):
        # Pentru simplitate, cerem doar numele cheii și algorithm_id
        key_name, ok = QInputDialog.getText(self, "Add Key", "Enter key name:")
        if not ok or not key_name.strip():
            return
        algorithm_id, ok = QInputDialog.getInt(self, "Add Key", "Enter algorithm ID:", min=1)
        if not ok:
            return

        # Construim datele cheii (poți adăuga mai multe câmpuri)
        key_data = {
            "key_name": key_name.strip(),
            "algorithm_id": algorithm_id,
            # Alte câmpuri pot fi adăugate aici (key_value, public_key etc.)
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
