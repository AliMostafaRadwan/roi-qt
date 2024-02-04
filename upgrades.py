import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QRect

class ImageROISelector(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_pixmap = None

        self.row_label = QLabel('Rows:', self)
        self.row_entry = QLineEdit(self)

        self.col_label = QLabel('Columns:', self)
        self.col_entry = QLineEdit(self)

        self.roi_rects = []  # List to store multiple ROI rectangles

        self.roi_count_label = QLabel('', self)  # New label for displaying ROI count

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        upload_button = QPushButton('Upload Image', self)
        upload_button.clicked.connect(self.upload_image)
        layout.addWidget(upload_button)

        layout.addWidget(self.image_label)

        layout.addWidget(self.row_label)
        layout.addWidget(self.row_entry)

        layout.addWidget(self.col_label)
        layout.addWidget(self.col_entry)

        layout.addWidget(self.roi_count_label)  # Add ROI count label to the layout

        self.setCentralWidget(central_widget)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Image ROI Selector')

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)', options=options)

        if file_name:
            image = QImage(file_name)
            self.image_pixmap = QPixmap.fromImage(image.scaled(1000, 1000, Qt.KeepAspectRatio))
            self.image_label.setPixmap(self.image_pixmap)
            self.image_label.mousePressEvent = self.mouse_press_event
            self.image_label.mouseMoveEvent = self.mouse_move_event  # Connect mouseMoveEvent
            self.image_label.mouseReleaseEvent = self.mouse_release_event

    def mouse_press_event(self, event):
        # Initialize temp rectangle
        self.temp_roi_rect = QRect(event.pos(), event.pos())  
        self.temp_roi_rect_valid = True

    def mouse_move_event(self, event):
        if hasattr(self, "temp_roi_rect"):
            if self.temp_roi_rect_valid:
                self.temp_roi_rect.setBottomRight(event.pos())  # Update temp rectangle
                self.display_roi(temp=True)  # Display temp rectangle

    def mouse_release_event(self, event):
        if hasattr(self, "temp_roi_rect"):
            if self.temp_roi_rect_valid:
                self.temp_roi_rect.setBottomRight(event.pos())  # Update temp rectangle
                self.roi_rects.append(self.temp_roi_rect.normalized())  # Add final ROI rectangle to list
                self.temp_roi_rect_valid = False
                self.display_roi()  # Display all ROIs

    def display_roi(self, temp=False):
        if self.image_pixmap:
            pixmap_copy = self.image_pixmap.copy()
            painter = QPainter(pixmap_copy)
            painter.setPen(Qt.red)
            for roi_rect in self.roi_rects:
                painter.drawRect(roi_rect)  # Display all ROI rectangles
            if temp and hasattr(self, "temp_roi_rect") and self.temp_roi_rect_valid:
                painter.drawRect(self.temp_roi_rect)  # Display temp rectangle
            painter.end()
            self.image_label.setPixmap(pixmap_copy)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageROISelector()
    window.show()
    sys.exit(app.exec_())
