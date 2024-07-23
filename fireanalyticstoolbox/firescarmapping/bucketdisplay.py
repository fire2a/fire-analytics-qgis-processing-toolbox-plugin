import boto3
from qgis.PyQt.QtCore import QObject, QThread, pyqtSignal
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QMessageBox, QLabel, QLineEdit, QFormLayout

class S3Loader(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, bucket_name, aws_access_key_id, aws_secret_access_key, prefix=''):
        super().__init__()
        self.bucket_name = bucket_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.prefix = prefix

    def run(self):
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name="us-east-1"
            )

            folders = []
            paginator = s3.get_paginator('list_objects_v2')
            for result in paginator.paginate(Bucket=self.bucket_name, Prefix=self.prefix, Delimiter='/'):
                if 'CommonPrefixes' in result:
                    for prefix in result['CommonPrefixes']:
                        folders.append(prefix['Prefix'])

            self.finished.emit(folders)
        except Exception as e:
            self.error.emit(f"Failed to list prefixes in bucket: {str(e)}")

class S3SelectionDialog(QDialog):
    def __init__(self, bucket_name, aws_access_key_id, aws_secret_access_key, prefix='', parent=None):
        super().__init__(parent)
        self.bucket_name = bucket_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.prefix = prefix
        
        title, description = self.display_title_and_description(prefix)
        self.setWindowTitle(title)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.description_label = QLabel(description)
        self.layout.addWidget(self.description_label)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        
        self.select_button = QPushButton("Select")
        self.select_button.clicked.connect(self.select_clicked)
        self.layout.addWidget(self.select_button)
        
        self.selected_item = None
        
        self.loader_thread = QThread()
        self.loader = S3Loader(bucket_name, aws_access_key_id, aws_secret_access_key, prefix)
        self.loader.moveToThread(self.loader_thread)
        self.loader.finished.connect(self.load_finished)
        self.loader.error.connect(self.load_error)
        self.loader_thread.started.connect(self.loader.run)
        
        self.loader_thread.start()

    def closeEvent(self, event):
        if self.loader_thread.isRunning():
            self.loader_thread.quit()
            self.loader_thread.wait()
        event.accept()

    def load_finished(self, folders):
        display_folders = [folder.split('/')[-2] + '/' for folder in folders]  # Obtener solo los nombres de las carpetas
        self.list_widget.addItems(display_folders)
        self.loader_thread.quit()
        self.loader_thread.wait()
        
    def load_error(self, message):
        self.loader_thread.quit()
        self.loader_thread.wait()
        QMessageBox.critical(self, "Error", message)
        self.reject()

    def display_title_and_description(self, prefix):
        parts = prefix.strip('/').split('/')
        if len(parts) == 1:
            title = "Select a Location"
            description = ""
        elif len(parts) == 2:
            title = "Select a year"
            description = f"Location: {parts[1]}"
        elif len(parts) == 3:
            title = "Select a month"
            description = f"Location: {parts[1]}, Year: {parts[2]}"
        elif len(parts) == 4:
            title = "Select a day"
            description = f"Location: {parts[1]}, Year: {parts[2]}, Month: {parts[3]}"
        elif len(parts) == 5:
            title = "Select a folder"
            description = f"Location: {parts[1]}, Year: {parts[2]}, Month: {parts[3]}, Day: {parts[4]}"
        else:
            title = ""
            description = ""
        return title, description 
        
    def select_clicked(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            selected_folder_name = selected_items[0].text()
            self.selected_item = self.prefix + selected_folder_name  # Concatenar el prefijo completo
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please select a folder.")

    def get_selected_item(self):
        return self.selected_item

class AWSCredentialsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter AWS Credentials")
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.aws_access_key_id_input = QLineEdit()
        self.aws_secret_access_key_input = QLineEdit()
        self.aws_secret_access_key_input.setEchoMode(QLineEdit.Password)

        self.layout.addRow("AWS Access Key ID:", self.aws_access_key_id_input)
        self.layout.addRow("AWS Secret Access Key:", self.aws_secret_access_key_input)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

    def get_credentials(self):
        return self.aws_access_key_id_input.text(), self.aws_secret_access_key_input.text()
