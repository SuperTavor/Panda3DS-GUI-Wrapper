import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import toml
from settingsGUI import Ui_settingsMenu as gui

# Utility function to update TOML configuration
def update_config(file_path, section_name, key, new_value):
    try:
        config = toml.load(file_path)
        if section_name not in config:
            config[section_name] = {}
        config[section_name][key] = new_value
        with open(file_path, 'w') as toml_file:
            toml.dump(config, toml_file)
        print(f"Updated '{section_name}.{key}' to '{new_value}' successfully!")
    except Exception as e:
        print(f"Error updating TOML file: {str(e)}")

# Settings Menu
class Settings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = gui()
        self.ui.setupUi(self)
        self.ui.OKButton.clicked.connect(self.ok)
        self.load_config()

    def load_config(self):
        try:
            config = toml.load('res/config.toml')
            self.ui.discordRpcCheckBox.setChecked(config['General'].get('EnableDiscordRPC', False))
            self.ui.shaderJitCheckBox.setChecked(config['GPU'].get('EnableShaderJIT', False))
            self.ui.chargerPluggedCheckBox.setChecked(config['Battery'].get('ChargerPlugged', False))
            self.ui.readOnlySdCheckBox.setChecked(config['SD'].get('WriteProtectVirtualSD', False))
            self.ui.virtualSDCheckBox.setChecked(config['SD'].get('UseVirtualSD', False))
            battery_percentage = config['Battery'].get('BatteryPercentage')
            if battery_percentage is not None:
                self.ui.percentageLineEdit.setText(str(battery_percentage))
        except Exception as e:
            print(f"Error loading config.toml: {str(e)}")

    def ok(self):
        discord_rpc_value = self.ui.discordRpcCheckBox.isChecked()
        update_config('res/config.toml', 'General', 'EnableDiscordRPC', discord_rpc_value)

        shader_jit_value = self.ui.shaderJitCheckBox.isChecked()
        update_config('res/config.toml', 'GPU', 'EnableShaderJIT', shader_jit_value)

        charger_plugged_value = self.ui.chargerPluggedCheckBox.isChecked()
        update_config('res/config.toml', 'Battery', 'ChargerPlugged', charger_plugged_value)

        read_only_sd_value = self.ui.readOnlySdCheckBox.isChecked()
        update_config('res/config.toml', 'SD', 'WriteProtectVirtualSD', read_only_sd_value)

        virtual_sd_value = self.ui.virtualSDCheckBox.isChecked()
        update_config('res/config.toml', 'SD', 'UseVirtualSD', virtual_sd_value)

        if self.ui.percentageLineEdit.text():
            try:
                batteryPercentage = int(self.ui.percentageLineEdit.text())
                if batteryPercentage > 100:
                    error_msg = QMessageBox()
                    error_msg.setIcon(QMessageBox.Critical)
                    error_msg.setWindowTitle("Error")
                    error_msg.setText("Invalid value")
                    error_msg.setInformativeText("Battery percentage is not valid, int is larger than 100.")
                    error_msg.setStandardButtons(QMessageBox.Ok)
                    error_msg.exec_()
                else:
                    update_config("res/config.toml", 'Battery', "BatteryPercentage", batteryPercentage)
                    msg = QMessageBox()
                    msg.setWindowTitle("Settings Modified.")
                    msg.setText("Modified settings. You can now close the settings window safely.")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
            except:
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText("Invalid value")
                error_msg.setInformativeText("Battery percentage is not valid, type is supposed to be int")
                error_msg.setStandardButtons(QMessageBox.Ok)
                error_msg.exec_()

                    
            


def main():
    app = QApplication(sys.argv)
    window = Settings()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()

