import sys
import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, QProcess
import webbrowser
from homeGUI import Ui_MainWindow
import settingsFunc
# Home Menu
class PandaGui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionLoadRom.triggered.connect(self.loadRom)
        self.actionView.triggered.connect(self.openSpreadsheet)
        self.actionModify.triggered.connect(self.openSettings)
        self.actionVisit_Original_Repo.triggered.connect(self.visitOriginalRepo)
        self.actionVisit_this_wrapper_s_repo.triggered.connect(self.visitWrapperRepo)
        self.settingsWindow = None
        self.setAcceptDrops(True)

    def visitOriginalRepo(self):
        webbrowser.open("https://github.com/wheremyfoodat/Panda3DS")
    def visitWrapperRepo(self):
        webbrowser.open("https://github.com/SuperTavor/Panda3DS-GUI-Wrapper")     
    def loadRom(self):
        file_filter = "Decrypted 3DS ROMs (*.3ds);;Decrypted CCI ROMs (*.cci);;CXI Files (*.cxi);;APP Files (*.app);;ELF files (*.elf);;AXF Files (*.axf);; 3DSX Files (*.3dsx)"

        file_paths, _ = QFileDialog.getOpenFileNames(self, 'Open File', '', file_filter)

        if file_paths:
            print("Selected files:")
            for file_path in file_paths:
                try:
                    os.chdir('res')  # Set working directory to 'res' only for alber.exe execution
                    alber_process = QProcess()
                    alber_process.start('alber.exe', [file_path])
                    alber_process.waitForFinished()
                except FileNotFoundError:
                    error_msg = QMessageBox()
                    error_msg.setIcon(QMessageBox.Critical)
                    error_msg.setWindowTitle("Error")
                    error_msg.setText("An error occurred!")
                    error_msg.setInformativeText("alber.exe not found.")
                    error_msg.setStandardButtons(QMessageBox.Ok)
                    error_msg.exec_()
                finally:
                    os.chdir('..')  # Restore working directory back to the previous value
        else:
            print("No files selected")
            
    def loadRomDnD(self, file_path):
        try:
            os.chdir('res')  # Set working directory to 'res' only for alber.exe execution
            alber_process = QProcess()
            alber_process.start('alber.exe', [file_path])
            alber_process.waitForFinished()
        except FileNotFoundError:
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("Error")
            error_msg.setText("An error occurred!")
            error_msg.setInformativeText("alber.exe not found.")
            error_msg.setStandardButtons(QMessageBox.Ok)
            error_msg.exec_()
        finally:
            os.chdir('..')  # Restore working directory back to the previous value


    def openSpreadsheet(self):
        webbrowser.open("https://docs.google.com/spreadsheets/d/1nWZTzfaMPkZdyhqHEawMRBaP0qSMmQdxrVfAbgapYrM/edit#gid=0")

    def openSettings(self):
        if self.settingsWindow is None or not self.settingsWindow.isVisible():
            self.settingsWindow = settingsFunc.Settings()
            self.settingsWindow.show()
            self.settingsWindow.activateWindow()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if os.path.isfile(file_path):
            self.loadRomDnD(file_path)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PandaGui()
    window.show()
    sys.exit(app.exec_())
