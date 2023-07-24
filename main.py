import sys
import random
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox


class DigitLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Arial", 48, QFont.Bold))
        self.setText("0")
        self.setFixedWidth(self.fontMetrics().boundingRect("0").width() * 2)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.contentsRect()
        painter.setPen(QPen(Qt.black, 2))
        painter.drawRect(rect.adjusted(2, 2, -2, -2))

        super().paintEvent(event)


class SlotMachine(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Slot Machine")
        self.setFixedSize(400, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)

        self.digits = []
        for _ in range(4):
            digit_label = DigitLabel()
            self.digits.append(digit_label)
            layout.addWidget(digit_label)

        self.countdown_label = QLabel("10")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.countdown_label)

        self.spin_button = QPushButton("Spin")
        self.spin_button.clicked.connect(self.spin_button_clicked)
        layout.addWidget(self.spin_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_digits)

        self.countdown = 5  # Countdown time in seconds

    def spin_button_clicked(self):
        if self.timer.isActive():
            self.timer.stop()
            self.show_spin_button()
        else:
            self.spin_button.hide()  # Hide the spin button
            self.timer.start(10)  # Adjust the interval for faster spinning (10 milliseconds)
            self.start_countdown()  # Start the countdown

    def start_countdown(self):
        self.countdown = 5
        self.update_countdown()

    def update_countdown(self):
        self.countdown -= 1
        self.countdown_label.setText(str(self.countdown))
        if self.countdown == 0:
            self.timer.stop()
            self.show_spin_button()
            winning_number = "0330"
            for i, digit_label in enumerate(self.digits):
                digit_label.setText(winning_number[i])
            self.show_result_message(winning_number)
        else:
            QTimer.singleShot(1000, self.update_countdown)  # Update countdown every 1 second

    def show_spin_button(self):
        self.spin_button.show()

    def show_result_message(self, number):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Result")
        msg_box.setText(f"Congratulations! You stopped at {number}. You're a winner!")
        msg_box.exec()

    def update_digits(self):
        for i, digit_label in enumerate(self.digits):
            self.digits[i].setText(str(random.randint(0, 9)))

    def resizeEvent(self, event):
        font = QFont("Arial", 48, QFont.Bold)
        metrics = self.fontMetrics()
        font.setStretch(metrics.horizontalAdvance("0") * 100 / metrics.boundingRect("0").width())
        for digit_label in self.digits:
            digit_label.setFont(font)
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    slot_machine = SlotMachine()
    slot_machine.show()

    sys.exit(app.exec())
