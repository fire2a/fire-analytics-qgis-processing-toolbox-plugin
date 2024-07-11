import boto3
from qgis.PyQt.QtCore import QObject, QThread, pyqtSignal, Qt
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QLabel, QMessageBox

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
        
        self.setWindowTitle("Select S3 Folder or File")
        
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
        self.list_widget.addItems(folders)
        self.loader_thread.quit()
        self.loader_thread.wait()
        
    def load_error(self, message):
        self.loader_thread.quit()
        self.loader_thread.wait()
        QMessageBox.critical(self, "Error", message)
        self.reject()

    def select_clicked(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            self.selected_item = selected_items[0].text()
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please select a folder.")

    def get_selected_item(self):
        return self.selected_item
