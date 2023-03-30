import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QCheckBox, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QDialog, QGridLayout
import heiya.to_hei

author = "Hongjun Wu"
version = "1.0.0"
updated_date = "20230330"
highlight = "First implementation of Heiya GUI"

class ExtensionWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select File Extensions")
        self.setGeometry(200, 200, 400, 200)

        # Create checkboxes for common file extensions
        self.jpg_checkbox = QCheckBox(".jpg")
        self.png_checkbox = QCheckBox(".png")
        self.tif_checkbox = QCheckBox(".tif")
        self.mp4_checkbox = QCheckBox(".mp4")
        self.mkv_checkbox = QCheckBox(".mkv")

        # Create a button to start the conversion process
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        # Create a layout for the checkboxes and button
        layout = QGridLayout()
        layout.addWidget(self.jpg_checkbox, 0, 0)
        layout.addWidget(self.png_checkbox, 0, 1)
        layout.addWidget(self.tif_checkbox, 1, 0)
        layout.addWidget(self.mp4_checkbox, 1, 1)
        layout.addWidget(self.mkv_checkbox, 2, 0)
        layout.addWidget(self.ok_button, 3, 0, 1, 2)

        # Set the layout for the window
        self.setLayout(layout)

        # Store the selected extensions
        self.selected_extensions = []

    def accept(self):
        # Store the selected extensions and close the window
        if self.jpg_checkbox.isChecked():
            self.selected_extensions.append(".jpg")
        if self.png_checkbox.isChecked():
            self.selected_extensions.append(".png")
        if self.tif_checkbox.isChecked():
            self.selected_extensions.append(".tif")
        if self.mp4_checkbox.isChecked():
            self.selected_extensions.append(".mp4")
        if self.mkv_checkbox.isChecked():
            self.selected_extensions.append(".mkv")
        super().accept()


class NextWindow(QDialog):
    def __init__(self, selected_files):
        super().__init__()
        self.setWindowTitle("Select Conversion Options")
        self.setGeometry(200, 200, 400, 200)

        self.selected_files = selected_files

        # Create checkboxes for AVIF, HEIC, and H265
        self.avif_checkbox = QCheckBox("AVIF")
        self.heic_checkbox = QCheckBox("HEIC")
        self.h265_checkbox = QCheckBox("H265")

        # Create a button to start the conversion process
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_files)

        # Create a layout for the checkboxes and button
        checkbox_layout = QVBoxLayout()
        checkbox_layout.addWidget(self.avif_checkbox)
        checkbox_layout.addWidget(self.heic_checkbox)
        checkbox_layout.addWidget(self.h265_checkbox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.convert_button)

        # Create a vertical layout for the main window
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Conversion Options"))
        main_layout.addLayout(checkbox_layout)
        main_layout.addLayout(button_layout)

        # Set the layout for the window
        self.setLayout(main_layout)

    def convert_files(self):
        # Check which checkboxes are selected
        avif_selected = self.avif_checkbox.isChecked()
        heic_selected = self.heic_checkbox.isChecked()
        h265_selected = self.h265_checkbox.isChecked()

        # Check if the selected files are a directory or not
        is_directory = os.path.isdir(self.selected_files[0])

        # Convert the selected files based on the selected checkboxes
        if is_directory:
            # Open a new window with checkboxes for file extensions
            extension_window = ExtensionWindow()
            extension_window.exec_()
            selected_extensions = extension_window.selected_extensions

            for extension in selected_extensions:
                if extension == ".jpg" and avif_selected:
                    heiya.to_hei.convert_image_in_dir_to_hei(self.selected_files[0], source_format=0, target_format=0)
                if extension == ".jpg" and heic_selected:
                    heiya.to_hei.convert_image_in_dir_to_hei(self.selected_files[0], source_format=0, target_format=1)
                if extension == ".tif" and avif_selected:
                    heiya.to_hei.convert_image_in_dir_to_hei(self.selected_files[0], source_format=1, target_format=0)
                if extension == ".tif" and heic_selected:
                    heiya.to_hei.convert_image_in_dir_to_hei(self.selected_files[0], source_format=1, target_format=1)
                if extension == ".mp4" and h265_selected:
                    heiya.to_hei.convert_video_in_dir_to_h265(self.selected_files[0], source_format=0)
                if extension == ".mkv" and h265_selected:
                    heiya.to_hei.convert_video_in_dir_to_h265(self.selected_files[0], source_format=1)
                if extension == ".mov" and h265_selected:
                    heiya.to_hei.convert_video_in_dir_to_h265(self.selected_files[0], source_format=2)
        else:
            for file in self.selected_files:
                _, extension = os.path.splitext(file)

                if extension == ".jpg" and avif_selected:
                    heiya.to_hei.convert_image_to_hei(file, target_format=0)
                if extension == ".jpg" and heic_selected:
                    heiya.to_hei.convert_image_to_hei(file, target_format=1)
                if extension == ".tif" and avif_selected:
                    heiya.to_hei.convert_image_to_hei(file, target_format=0)
                if extension == ".tif" and heic_selected:
                    heiya.to_hei.convert_image_to_hei(file, target_format=1)
                if extension == ".mp4" and h265_selected:
                    heiya.to_hei.video_to_h265(file)
                if extension == ".mkv" and h265_selected:
                    heiya.to_hei.video_to_h265(file)
                if extension == ".mov" and h265_selected:
                    heiya.to_hei.video_to_h265(file)

            # Close the window when the conversion is done
            self.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heiya GUI")
        self.setGeometry(200, 200, 400, 200)

        # Create a label, list widget, and button for selecting files
        label = QLabel("Drag and drop files/folders or click the button to select files")
        self.list_widget = QListWidget()
        self.select_button = QPushButton("Select Files")
        self.delete_button = QPushButton("Delete Selected")

        # Create a button for opening the next window
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.open_next_window)

        # Create a layout for the label, list widget, and button
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.delete_button)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.list_widget)
        layout.addLayout(button_layout)
        layout.addWidget(next_button)

        # Create a central widget and set the main layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect the select button to the select_files function
        self.select_button.clicked.connect(self.select_files)

        # Connect the delete button to the delete_file function
        self.delete_button.clicked.connect(self.delete_file)

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

    def delete_file(self):
        # Delete the selected item(s) from the list widget
        for item in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(item))

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

    def open_next_window(self):
        # Get the selected files from the list widget
        selected_files = []
        for index in range(self.list_widget.count()):
            selected_files.append(self.list_widget.item(index).text())

        # Check if any files have been selected
        if len(selected_files) == 0:
            return

        # Open the next window with the selected files
        next_window = NextWindow(selected_files)
        next_window.setWindowModality(Qt.ApplicationModal)
        next_window.exec_()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

