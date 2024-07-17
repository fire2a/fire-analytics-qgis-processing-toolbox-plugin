import boto3
from qgis.PyQt.QtCore import QObject, QThread, pyqtSignal
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QMessageBox

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
        
        self.setWindowTitle(self.display_title(prefix))
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
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

    def display_title(self, prefix):
        if prefix.count("/") == 1:
            return "Select a Location"
        elif prefix.count("/") == 2:
            return "Select a year"
        elif prefix.count("/") == 3:
            return "Select a month"
        elif prefix.count("/") == 4:
            return "Select a day"
        elif prefix.count("/") == 5:
            return "Select a folder"
        
    


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
