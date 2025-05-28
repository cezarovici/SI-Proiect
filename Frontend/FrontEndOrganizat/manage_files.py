import requests
import threading
import hashlib
import os # Asigură-te că os este importat
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QFileDialog, QInputDialog, QMessageBox
)
from PyQt5.QtGui import QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import pyqtSignal, QObject

class FileWorker(QObject):
    finished = pyqtSignal(object)

    def fetch_files(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.finished.emit({"type": "fetch", "data": data})
        except Exception as e:
            print(f"Error fetching files: {e}")
            self.finished.emit({"type": "fetch", "data": []})

    def post_file(self, url, file_data):
        try:
            response = requests.post(url, json=file_data)
            response.raise_for_status()
            self.finished.emit({"type": "post", "success": True, "data": response.json()})
        except Exception as e:
            print(f"Error adding file: {e}")
            error_data = None
            try: error_data = e.response.json()
            except: pass
            self.finished.emit({"type": "post", "success": False, "error": error_data or str(e)})

    def delete_file(self, url):
        try:
            response = requests.delete(url)
            response.raise_for_status()
            # DELETE poate returna 200/204 cu sau fără corp
            data = response.json() if response.content else {"message": "Deleted successfully"}
            self.finished.emit({"type": "delete", "success": True, "data": data})
        except Exception as e:
            print(f"Error deleting file: {e}")
            error_data = None
            try: error_data = e.response.json()
            except: pass
            self.finished.emit({"type": "delete", "success": False, "error": error_data or str(e)})

    def encrypt_file(self, url, payload):
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.finished.emit({"type": "encrypt", "success": True, "data": response.json()})
        except Exception as e:
            print(f"Error encrypting file: {e}")
            error_data = None
            try: error_data = e.response.json()
            except: pass
            self.finished.emit({"type": "encrypt", "success": False, "error": error_data or str(e)})
    
    def decrypt_file(self, url, payload): 
        """Trimite o cerere POST pentru decriptare."""
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.finished.emit({"type": "decrypt", "success": True, "data": response.json()})
        except Exception as e:
            print(f"Error decrypting file: {e}")
            error_data = None
            try: error_data = e.response.json()
            except: pass
            self.finished.emit({"type": "decrypt", "success": False, "error": error_data or str(e)})


class ManageFilesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Files")
        self.api_base_url = "http://localhost:8000/files/"
        self.crypto_api_url = "http://localhost:8000/crypto/" 
        self.local_shared_path = os.path.abspath("shared_crypto_files") 
        self.container_shared_path = "/app/data"
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
            QPushButton { background-color: #4CAF50; color: white; padding: 15px 32px; text-align: center; font-size: 16px; margin: 4px 2px; border-radius: 5px; }
            QPushButton:hover { background-color: #3e8e41; }
            QTableWidget { background-color: #eefafd; border: 1px solid black; }
            QHeaderView::section { background-color: #4CAF55; color: white; font-size: 14px; padding: 4px; border: 1px solid black; }
        """)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["File ID", "Original Path", "Encrypted Path", "Original Hash", "Encrypted Hash", "Algorithm ID", "Key ID", "Encryption Date", "Last Access"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        self.btn_addfile = QPushButton("Add a file", self)
        self.btn_addfile.clicked.connect(self.add_file) 
        button_layout.addWidget(self.btn_addfile)
        self.btn_deletefile = QPushButton("Delete a file", self)
        self.btn_deletefile.clicked.connect(self.delete_file_action)
        button_layout.addWidget(self.btn_deletefile)
        layout.addLayout(button_layout)

        crypto_layout = QHBoxLayout()
        self.btn_encrfile = QPushButton("Encrypt", self)
        self.btn_encrfile.clicked.connect(self.encrypt_file_action)
        crypto_layout.addWidget(self.btn_encrfile)

        self.btn_decrfile = QPushButton("Decrypt", self)
        self.btn_decrfile.clicked.connect(self.decrypt_file_action)
        crypto_layout.addWidget(self.btn_decrfile)
        layout.addLayout(crypto_layout)

        self.btn_back = QPushButton("Back", self)
        self.btn_back.clicked.connect(self.close)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

    def add_file(self):
        """Deschide dialogul pentru adăugarea unui fișier și trimite datele COREct."""
        start_directory = self.local_shared_path
        
        # Asigură-te că directorul există înainte de a deschide dialogul
        if not os.path.exists(start_directory):
            os.makedirs(start_directory)
            QMessageBox.information(self, "Info", f"Created shared directory at: {start_directory}")

        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", start_directory, "All Files (*.*)")
        
        if not file_path:
            return

        # Verifică dacă fișierul este în directorul partajat (folosind os.path.abspath)
        if not os.path.abspath(file_path).startswith(os.path.abspath(start_directory)):
            QMessageBox.warning(self, "Warning", f"Please select a file from the shared directory: {start_directory}")
            return

        algorithm_id, ok1 = QInputDialog.getInt(self, "Add File", "Enter Algorithm ID:")
        if not ok1: return

        key_id, ok2 = QInputDialog.getInt(self, "Add File", "Enter Key ID:")
        if not ok2: return

        file_name = os.path.basename(file_path)
        
        # Folosește calea din container
        original_path_in_container = f"{self.container_shared_path}/{file_name}" 
        encrypted_path_in_container = f"{self.container_shared_path}/{file_name}.enc"

        original_hash = self.calculate_hash(file_path)

        file_data = {
            "original_path": original_path_in_container,
            "encrypted_path": encrypted_path_in_container,
            "original_hash": original_hash,
            "encrypted_hash": None,
            "algorithm_id": algorithm_id,
            "key_id": key_id
        }

        self.worker = FileWorker()
        self.worker.finished.connect(self.handle_response)
        thread = threading.Thread(target=self.worker.post_file, args=(self.api_base_url, file_data))
        thread.start()

    # Asigură-te că TOATE celelalte metode (load_data, handle_response, etc.) sunt prezente!
    def load_data(self):
        self.worker = FileWorker()
        self.worker.finished.connect(self.handle_response)
        thread = threading.Thread(target=self.worker.fetch_files, args=(self.api_base_url,))
        thread.start()

    def handle_response(self, response):
        if not isinstance(response, dict) or "type" not in response:
            print("Invalid response received:", response)
            QMessageBox.warning(self, "Error", "Received an invalid response from the worker.")
            return

        response_type = response.get("type")

        if response_type == "fetch":
            if "data" in response and isinstance(response["data"], list):
                self.populate_table(response["data"])
            else:
                QMessageBox.warning(self, "Error", "Failed to load files.")
                self.populate_table([])
        elif response_type == "post":
            if response.get("success"):
                QMessageBox.information(self, "Success", f"File added successfully with ID: {response.get('data', {}).get('file_id')}")
                self.load_data()
            else:
                error = response.get('error', 'Unknown error')
                QMessageBox.warning(self, "Error", f"Failed to add file: {error}")
        elif response_type == "delete":
            if response.get("success"):
                QMessageBox.information(self, "Success", "File deleted successfully.")
                self.load_data()
            else:
                error = response.get('error', {}).get('detail', 'Unknown error')
                QMessageBox.warning(self, "Error", f"Failed to delete file: {error}")
        elif response_type == "encrypt":
            if response.get("success"):
                QMessageBox.information(self, "Success", "File encrypted successfully.")
                self.load_data()
            else:
                error = response.get('error', {}).get('detail', 'Unknown error')
                QMessageBox.warning(self, "Error", f"Failed to encrypt file: {error}")
        elif response_type == "decrypt": # Ramură nouă
            if response.get("success"):
                data = response.get("data", {})
                output_path_container = data.get("output_path", "Unknown location")
                # Converteste calea din container la calea locala pentru mesajul userului
                local_output_path = output_path_container.replace(self.container_shared_path, self.local_shared_path)
                QMessageBox.information(self, "Success", f"File decrypted successfully to:\n{local_output_path}")
            else:
                error = response.get('error', {}).get('detail', 'Unknown error')
                QMessageBox.warning(self, "Error", f"Failed to decrypt file: {error}")

    
    def populate_table(self, files):
        self.table.setRowCount(len(files))
        for i, file in enumerate(files):
            self.table.setItem(i, 0, QTableWidgetItem(str(file.get("file_id", ""))))
            self.table.setItem(i, 1, QTableWidgetItem(file.get("original_path", "")))
            self.table.setItem(i, 2, QTableWidgetItem(file.get("encrypted_path", "")))
            self.table.setItem(i, 3, QTableWidgetItem(file.get("original_hash") or "N/A"))
            self.table.setItem(i, 4, QTableWidgetItem(file.get("encrypted_hash") or "N/A"))
            self.table.setItem(i, 5, QTableWidgetItem(str(file.get("algorithm_id", ""))))
            self.table.setItem(i, 6, QTableWidgetItem(str(file.get("key_id", ""))))
            self.table.setItem(i, 7, QTableWidgetItem(file.get("encryption_date", "")))
            self.table.setItem(i, 8, QTableWidgetItem(file.get("last_access") or "N/A"))
        self.table.resizeColumnsToContents()

    def calculate_hash(self, file_path):
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except IOError as e:
            QMessageBox.warning(self, "Hashing Error", f"Could not read file to calculate hash: {e}")
            return None

    def delete_file_action(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a file to delete.")
            return
        file_id_item = self.table.item(selected_row, 0)
        if not file_id_item:
            QMessageBox.warning(self, "Warning", "Cannot get File ID from selected row.")
            return
        file_id = file_id_item.text()
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete the file with ID {file_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm != QMessageBox.Yes:
            return
        url = f"{self.api_base_url}{file_id}"
        self.worker = FileWorker()
        self.worker.finished.connect(self.handle_response)
        thread = threading.Thread(target=self.worker.delete_file, args=(url,))
        thread.start()

    def encrypt_file_action(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a file to encrypt.")
            return
        try:
            file_id = int(self.table.item(selected_row, 0).text())
            algo_id = int(self.table.item(selected_row, 5).text())
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not read data from selected row: {e}")
            return

        algo_base_name = ""
        if algo_id == 1: algo_base_name = "aes"
        elif algo_id == 2: algo_base_name = "rsa"
        else:
            QMessageBox.warning(self, "Warning", f"Unknown Algorithm ID: {algo_id}.")
            return

        implementations = [f"{algo_base_name}_open", f"{algo_base_name}_crypto"]
        implementation, ok = QInputDialog.getItem(self, "Choose Implementation", "Select the library to use:", implementations, 0, False)
        if not ok or not implementation:
            return

        payload = {"file_id": file_id, "implementation": implementation}
        url = f"{self.crypto_api_url}encrypt"
        self.worker = FileWorker()
        self.worker.finished.connect(self.handle_response)
        thread = threading.Thread(target=self.worker.encrypt_file, args=(url, payload))
        thread.start()

    def decrypt_file_action(self):
        """Gestionează acțiunea de decriptare a fișierului selectat."""
        selected_row = self.table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a file to decrypt.")
            return

        try:
            file_id = int(self.table.item(selected_row, 0).text())
            algo_id = int(self.table.item(selected_row, 5).text())
            encrypted_path = self.table.item(selected_row, 2).text()

            # Verifică dacă fișierul criptat există (în container)
            if not encrypted_path or not encrypted_path.startswith(self.container_shared_path):
                 QMessageBox.warning(self, "Warning", "Encrypted file path not found or invalid.")
                 return

        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not read data from selected row: {e}")
            return

        algo_base_name = ""
        if algo_id == 1: algo_base_name = "aes"
        elif algo_id == 2: algo_base_name = "rsa"
        else:
            QMessageBox.warning(self, "Warning", f"Unknown Algorithm ID: {algo_id}.")
            return

        implementations = [f"{algo_base_name}_open", f"{algo_base_name}_crypto"]
        implementation, ok = QInputDialog.getItem(self, "Choose Implementation", "Select the library to use:", implementations, 0, False)
        if not ok or not implementation:
            return

        payload = {"file_id": file_id, "implementation": implementation}
        url = f"{self.crypto_api_url}decrypt" # Endpoint-ul nou
        self.worker = FileWorker()
        self.worker.finished.connect(self.handle_response)
        thread = threading.Thread(target=self.worker.decrypt_file, args=(url, payload))
        thread.start()