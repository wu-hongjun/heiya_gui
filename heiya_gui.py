import sys
import os
import time
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QCheckBox, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
                             QListWidget, QProgressBar, QMessageBox, QGridLayout)
import heiya.to_hei

author = "Hongjun Wu"
version = "1.2.0"
updated_date = "20230812"
highlight = "Added a button to clear the list."

class ConversionWorker(QThread):
    progress_signal = pyqtSignal(int)  # Explicitly define the signal type as int
    finished_signal = pyqtSignal()

    def __init__(self, selected_files, conversion_function):
        super().__init__()
        self.selected_files = selected_files
        self.conversion_function = conversion_function

    def run(self):
        total_files = len(self.selected_files)
        for index, file_path in enumerate(self.selected_files):
            self.conversion_function(file_path)
            percent_complete = int((index + 1) / total_files * 100)  # Convert to int before emitting
            self.progress_signal.emit(percent_complete)
        self.finished_signal.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heiya GUI")
        self.setGeometry(200, 200, 500, 350)

        # Create a label, list widget, and button for selecting files
        label = QLabel("Drag and drop files/folders or click the button to select files")
        self.list_widget = QListWidget()
        self.select_button = QPushButton("Select Files")

        # Create checkboxes for file extensions and conversion options
        self.jpg_checkbox = QCheckBox(".jpg")
        self.jpg_checkbox.setChecked(True)
        self.png_checkbox = QCheckBox(".png")
        self.tif_checkbox = QCheckBox(".tif")

        self.avif_checkbox = QCheckBox("AVIF")
        self.avif_checkbox.setChecked(True)
        self.heic_checkbox = QCheckBox("HEIC")
        self.h265_checkbox = QCheckBox("H265")

        # Create a grid layout for the checkboxes
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("From"), 0, 0)
        grid_layout.addWidget(QLabel("To"), 0, 1)
        grid_layout.addWidget(self.jpg_checkbox, 1, 0)
        grid_layout.addWidget(self.png_checkbox, 2, 0)
        grid_layout.addWidget(self.tif_checkbox, 3, 0)
        grid_layout.addWidget(self.avif_checkbox, 1, 1)
        grid_layout.addWidget(self.heic_checkbox, 2, 1)
        grid_layout.addWidget(self.h265_checkbox, 3, 1)

        # Create a progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        # Create a button to start the conversion process
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_files)
        self.convert_button.clicked.connect(self.reset_progress_bar)

        # Create a button for deleting a selected item
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_selected_item)
        delete_button.clicked.connect(self.reset_progress_bar)

        # Create a button for clearing the list
        clear_button = QPushButton("Clear List")
        clear_button.clicked.connect(self.clear_list)
        clear_button.clicked.connect(self.reset_progress_bar)


        # Create a layout for the label, list widget, checkboxes, and buttons
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(clear_button)
        layout.addWidget(label)
        layout.addWidget(self.list_widget)
        layout.addLayout(button_layout)
        layout.addLayout(grid_layout)  # Add the grid layout to the main layout

        
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.convert_button)

        # Create a central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect the select button to the select_files function
        self.select_button.clicked.connect(self.select_files)

        # Enable drag and drop for the list widget
        self.list_widget.setAcceptDrops(True)
        self.setAcceptDrops(True)

    def select_files(self):
        # Open a file dialog to select files
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setOption(QFileDialog.DontUseNativeDialog)
        filenames = file_dialog.getOpenFileNames()[0]

        # Add the selected files to the list widget
        for filename in filenames:
            self.list_widget.addItem(filename)

    def dragEnterEvent(self, event):
        # Allow drag and drop events to be accepted by the list widget
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # Allow drag and drop events to be accepted by the list widget
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Add the dropped files/folders to the list widget
        for url in event.mimeData().urls():
            file_path = str(url.toLocalFile())
            if os.path.isfile(file_path) or os.path.isdir(file_path):
                self.list_widget.addItem(file_path)

    def delete_selected_item(self):
        # Get the currently selected item in the list widget and delete it
        current_item = self.list_widget.currentItem()
        if current_item:
            self.list_widget.takeItem(self.list_widget.row(current_item))

    def clear_list(self):
        self.list_widget.clear()

    def convert_files(self):
        # Check which checkboxes are selected
        avif_selected = self.avif_checkbox.isChecked()
        heic_selected = self.heic_checkbox.isChecked()
        h265_selected = self.h265_checkbox.isChecked()

        jpg_selected = self.jpg_checkbox.isChecked()
        png_selected = self.png_checkbox.isChecked()
        tif_selected = self.tif_checkbox.isChecked()

        # Define the conversion function
        def conversion_function(file_path):
            # Check if the selected files are a directory or not
            is_directory = os.path.isdir(file_path)

            # Convert the selected files based on the selected checkboxes
            if is_directory:
                if jpg_selected and avif_selected:
                    heiya.to_hei.convert_image_in_dir_to_hei(file_path, source_format=0, target_format=0)
                if jpg_selected and heic_selected:
                    heiya.to_hei.convert_image_in_dir_to_hei(file_path, source_format=0, target_format=1)
                if png_selected and avif_selected:
                    heiya.to_hei.convert_image_in_dir_to_hei(file_path, source_format=2, target_format=0)
                if png_selected and heic_selected:
                    heiya.to_hei.convert_image_in_dir_to_hei(file_path, source_format=2, target_format=1)
                if tif_selected and avif_selected:
                    heiya.to_hei.convert_image_in_dir_to_hei(file_path, source_format=1, target_format=0)
                if tif_selected and heic_selected:
                    heiya.to_hei.convert_image_in_dir_to_hei(file_path, source_format=1, target_format=1)

            else:
                _, extension = os.path.splitext(file_path)

                if (jpg_selected or png_selected or tif_selected) and avif_selected:
                    heiya.to_hei.convert_image_to_hei(file_path, target_format=0)
                if (jpg_selected or png_selected or tif_selected) and heic_selected:
                    heiya.to_hei.convert_image_to_hei(file_path, target_format=1)

        # Get the selected files from the list widget
        selected_files = [self.list_widget.item(index).text() for index in range(self.list_widget.count())]

        # Check if any files have been selected
        if not selected_files:
            return

        # Create a worker thread for the conversion
        self.worker = ConversionWorker(selected_files, conversion_function)
        self.worker.progress_signal.connect(self.update_progress_bar)
        self.worker.finished_signal.connect(self.conversion_finished)
        self.worker.start()


    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def reset_progress_bar(self):
        self.progress_bar.setValue(0)

    def conversion_finished(self):
        # Display a message box when the conversion is finished
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Conversion completed!")
        msg.setWindowTitle("Info")
        msg.exec_()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
