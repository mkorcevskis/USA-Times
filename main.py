import sys
import requests
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class GalvenaisWidget(QWidget):
    def __init__(self, parent=None):
        super(GalvenaisWidget, self).__init__(parent)
        self.vieta_label = QLabel("Izvēlieties vietu!")
        self.vieta_label.setAlignment(Qt.AlignCenter)
        self.vieta_label.setStyleSheet("font: 20px;")
        self.vietas_izvele_combo_box = QComboBox()
        self.vietas_izvele_combo_box.addItems(vieta_dati)
        self.uzzinat_laiku_button = QPushButton("Uzzināt laiku!")
        self.uzzinat_laiku_button.setStyleSheet("font: 15px; font-weight: bold; height: 30px;")
        self.uzraksts_laiks_label = QLabel("Laiks:")
        self.uzraksts_laiks_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.laiks_label = QLabel()
        self.laiks_label.setAlignment(Qt.AlignBottom)
        self.laiks_label.setStyleSheet("font-weight: bold;")
        self.uzraksts_laika_zona_label = QLabel("Laika zona:")
        self.uzraksts_laika_zona_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.laika_zona_label = QLabel()
        self.laika_zona_label.setAlignment(Qt.AlignBottom)
        self.laika_zona_label.setStyleSheet("font-weight: bold;")
        self.uzraksts_laika_zonu_starpiba_label = QLabel("Laika zonu starpība:")
        self.uzraksts_laika_zonu_starpiba_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.laika_zonu_starpiba_label = QLabel()
        self.laika_zonu_starpiba_label.setAlignment(Qt.AlignBottom)
        self.laika_zonu_starpiba_label.setStyleSheet("font-weight: bold;")
        self.galvenais_logs_layout = QGridLayout()
        self.setLayout(self.galvenais_logs_layout)
        self.galvenais_logs_layout.setVerticalSpacing(10)
        self.galvenais_logs_layout.addWidget(self.vieta_label, 0, 0, 1, 0)
        self.galvenais_logs_layout.addWidget(self.vietas_izvele_combo_box, 1, 0, 1, 0)
        self.galvenais_logs_layout.addWidget(self.uzzinat_laiku_button, 2, 0, 2, 0)
        self.galvenais_logs_layout.addWidget(self.uzraksts_laiks_label, 3, 0)
        self.galvenais_logs_layout.addWidget(self.laiks_label, 3, 1)
        self.galvenais_logs_layout.addWidget(self.uzraksts_laika_zona_label, 4, 0)
        self.galvenais_logs_layout.addWidget(self.laika_zona_label, 4, 1)
        self.galvenais_logs_layout.addWidget(self.uzraksts_laika_zonu_starpiba_label, 5, 0)
        self.galvenais_logs_layout.addWidget(self.laika_zonu_starpiba_label, 5, 1)
        self.vietas_izvele_combo_box.currentIndexChanged.connect(lambda: self.vieta_label.setText(
            self.vietas_izvele_combo_box.currentText()))
        self.uzzinat_laiku_button.clicked.connect(self.uzzinat_laiku)

    def uzzinat_laiku(self):
        self.vieta_label.setText(self.vietas_izvele_combo_box.currentText())
        try:
            laiks_atbilde = requests.get("http://worldtimeapi.org/api/timezone/" +
                                         self.vietas_izvele_combo_box.currentText())
            laiks_dati = laiks_atbilde.json()
            self.laiks_label.setText(laiks_dati["datetime"][11:19])
            self.laika_zona_label.setText(laiks_dati["timezone"])
            self.laika_zonu_starpiba_label.setText(laiks_dati["utc_offset"] + " UTC")
        except requests.exceptions.RequestException:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Kļūda")
            msg.setWindowIcon(QIcon("logo.png"))
            msg.setText("Notikusi kļūda, veicot pieprasījumu!\nLūdzu, mēģiniet vēlreiz!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


if __name__ == "__main__":
    try:
        vieta_atbilde = requests.get("http://worldtimeapi.org/api/timezone/America")
        vieta_dati = vieta_atbilde.json()
    except requests.exceptions.RequestException:
        vieta_dati = list()

    app = QApplication(sys.argv)
    widget = GalvenaisWidget()
    win = QMainWindow()
    win.setWindowTitle("Laika uzziņas sistēma")
    win.setWindowIcon(QIcon("logo.png"))
    win.setCentralWidget(widget)
    win.setFixedSize(450, 320)
    win.show()
    sys.exit(app.exec_())
