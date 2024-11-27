import sys
import os
import jinja2
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QComboBox, 
                             QTextEdit, QVBoxLayout, QPushButton, QMessageBox, 
                             QHBoxLayout, QRadioButton, QDialog, QButtonGroup, QScrollArea,  QFileDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from vcolorpicker import getColor, useLightTheme
from PyQt5.QtGui import QColor
import xml.etree.ElementTree as ET
import re

useLightTheme(True)

class DisplayTypePopup(QDialog):
    def __init__(self, trend_names, display_type_options, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select Display Type for Each Trend")
        self.setModal(True)
        self.trend_names = trend_names
        self.display_type_options = display_type_options
        self.selected_display_types = {}
        self.selected_colors = {}

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow resizing
        scroll_area.setFixedHeight(300)  # Adjust to your desired height

        # Create a widget to hold the layout
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        # Create radio button groups and color pickers for each trend name
        for i, trend_name in enumerate(trend_names):
            # Add trend name as a label
            label = QLabel(f"{trend_name}")
            layout.addWidget(label)

            # Horizontal layout to align radio buttons and color picker button
            trend_layout = QHBoxLayout()

            # Radio button group for display types
            button_group = QButtonGroup(self)
            button_layout = QHBoxLayout()

            # Create radio buttons for display types
            for display_type, display_value in display_type_options.items():
                radio_button = QRadioButton(display_type)
                button_group.addButton(radio_button)
                button_layout.addWidget(radio_button)
                # Default selection for each line
                if display_value == 0:
                    radio_button.setChecked(True)

            # Add radio buttons layout to trend layout
            trend_layout.addLayout(button_layout)

            # Add a color picker button
            color_button = QPushButton()
            color_button.setToolTip("Change the chart's line color")
            color_button.setIcon(QIcon("./static/brush.ico"))
            color_button.clicked.connect(lambda _, idx=i, btn=color_button: self.pick_color(idx, btn))
            trend_layout.addWidget(color_button)

            # Store default color
            self.selected_colors[i] = "#FF556B2F"

            # Add trend layout to main layout
            layout.addLayout(trend_layout)
            self.selected_display_types[i] = button_group

        # Set the content widget in the scroll area
        scroll_area.setWidget(content_widget)

        # Main layout for the dialog
        main_layout = QVBoxLayout(self)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        # Create a layout for the OK button
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addStretch()  # Push the button to the right
        button_layout.addWidget(ok_button)

        # Add the OK button layout to the main layout
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def pick_color(self, index, button):
        """Open color picker and save selected color."""
        color = getColor((85,107,47))  # Open the color picker
        if color:
            if isinstance(color, tuple):  # If the color is a tuple, convert to hex
                color = QColor(int(color[0]),int(color[1]),int(color[2])).name(QColor.HexArgb)
            self.selected_colors[index] = color  # Save the selected color
            button.setStyleSheet(f"background-color: {color};")  # Update button background

    def get_selected_display_types(self):
        """Retrieve selected display types and colors."""
        display_types = []
        colors_in_argb = []

        for i, button_group in self.selected_display_types.items():
            # Get selected display type
            selected_button = button_group.checkedButton()
            display_type_text = selected_button.text()
            display_types.append(self.display_type_options[display_type_text])

            # Convert color to ARGB
            color_qcolor = self.selected_colors[i]
            unsigned_int = int(color_qcolor[1:], 16)
            if unsigned_int > 0x7FFFFFFF:
                unsigned_int = unsigned_int - 0x100000000

            colors_in_argb.append(unsigned_int)

        return display_types, colors_in_argb

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.context = {
            "serverPath":"",
            "serverVersion": "",
            "trendPathBinary":"",
            "trendPathAnalog":"",
            "trendNameAnalog": [],
            "trendNameBinary": []
        }

        self.result = {
            "RuntimeVersion": None,
            "ServerFullPath": None,
            "Path Analog":None,
            "Path Binary":None,
            "Trends": None
        }

        self.name = ""

        self.setWindowTitle("Chart Builder")
        self.setWindowIcon(QIcon("./static/favicon.ico"))

        self.existing_file_label = QLabel("Use Existing File:")
        self.existing_file_button = QPushButton('Search for Files')
        self.existing_file_button.clicked.connect(self.search_files)

        self.result_display = QLineEdit(self)
        self.result_display.setReadOnly(True)

        self.process_existing_file = QPushButton('Use this file')
        self.process_existing_file.clicked.connect(self.insert_information)

        self.name_label = QLabel("New File's name:")
        self.name_edit = QLineEdit(datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))

        self.version_label = QLabel("EBO Version:")
        self.version_edit = QLineEdit("5.0.3.117")

        self.server_path = QLabel("Server Path:")
        self.server_path_edit = QLineEdit("/Server 1")

        self.display_type_label = QLabel("Display Type:")
        self.display_type_combo = QComboBox()
        self.display_type_combo.addItems(["Line", "Discrete Line", "Digital", "Bars"])

        self.select_display_type_button_analog = QPushButton("Config Display Type for Analog")
        self.select_display_type_button_binary = QPushButton("Config Display Type for Binary")

        self.trend_path_label_analog = QLabel("Analog Trends Path:")
        self.trend_path_analog = QLineEdit("../../../../Trend/Analog Group")
                
        self.trend_names_label_analog = QLabel("Analog Trends Names:")
        self.trend_names_edit_analog = QTextEdit()

        self.trend_path_label_binary = QLabel("Binary Trends Path:")
        self.trend_path_binary = QLineEdit("../../../../Trend/Binary Group")
        
        self.trend_names_label_binary = QLabel("Binary Trends Names:")
        self.trend_names_edit_binary = QTextEdit()

        self.submit_button = QPushButton("Build")
        self.submit_button.clicked.connect(self.print_values)

        # Connect buttons to show popup
        self.select_display_type_button_analog.clicked.connect(self.show_display_type_popup_analog)
        self.select_display_type_button_binary.clicked.connect(self.show_display_type_popup_binary)
        
        layout = QVBoxLayout()
        
        layout.addWidget(self.existing_file_label)
        layout.addWidget(self.existing_file_button)
        layout.addWidget(self.result_display)
        layout.addWidget(self.process_existing_file)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.version_label)
        layout.addWidget(self.version_edit)
        layout.addWidget(self.server_path)
        layout.addWidget(self.server_path_edit)

        self.label_box = QHBoxLayout()
        self.label_box.addWidget(self.trend_names_label_analog)
        self.label_box.addWidget(self.trend_names_label_binary)

        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.trend_names_edit_analog)
        self.hbox_layout.addWidget(self.trend_names_edit_binary)

        self.label_path_box = QHBoxLayout()
        self.label_path_box.addWidget(self.trend_path_label_analog)
        self.label_path_box.addWidget(self.trend_path_label_binary)
        
        self.hbox_trend_path = QHBoxLayout()
        self.hbox_trend_path.addWidget(self.trend_path_analog)
        self.hbox_trend_path.addWidget(self.trend_path_binary)

        layout.addLayout(self.label_path_box)
        layout.addLayout(self.hbox_trend_path)
        layout.addLayout(self.label_box)        
        layout.addLayout(self.hbox_layout)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.select_display_type_button_analog)
        self.button_layout.addWidget(self.select_display_type_button_binary)

        self.footnote_label = QLabel()
        self.footnote_label.setText(
            '<p style="font-size: 10px; color: gray;">'
            'Created with <img src="./static/heart.ico" width="12" height="12" style="vertical-align: middle;"> by Muriel Carletti '
            '<a href="https://www.linkedin.com/in/muriel-carletti-130386156/">LinkedIn</a> |'
            '<a href="https://github.com/synth-me">GitHub</a>'
            '</p>'
        )
        self.footnote_label.setOpenExternalLinks(True)
        self.footnote_label.setAlignment(Qt.AlignCenter)

        layout.addLayout(self.button_layout)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.footnote_label)

        self.setLayout(layout)

    def parse_xml_file(self) -> dict:
    
        try:
            # Parse the XML file
            tree = ET.parse(self.result_display.text())
            root = tree.getroot()

            # Extract RuntimeVersion and ServerFullPath from MetaInformation
            meta_info = root.find('MetaInformation')
            if meta_info is not None:
                runtime_version = meta_info.find(".//RuntimeVersion")
                if runtime_version is not None:
                    self.result["RuntimeVersion"] = runtime_version.attrib.get('Value')

                server_full_path = meta_info.find(".//ServerFullPath")
                if server_full_path is not None:
                    self.result["ServerFullPath"] = server_full_path.attrib.get('Value')

            # Flags to check if we've already found a reference for Analog and Binary groups
            analog_reference_found = False
            binary_reference_found = False
            pattern = r"^(Binary Group|Analog Group)$"

            # Extract top-level "Trend" OI and its sub-OIs
            exported_objects = root.find('ExportedObjects')
            if exported_objects is not None:
                trend_group = exported_objects.find(".//OI[@NAME='Trend']")
                if trend_group is not None:
                    trend_groups = {"Binary Group":[], "Analog Group":[]}

                    # Extract sub-OIs under "Trend"
                    for sub_oi in trend_group.findall(".//OI"):
                        group_name = sub_oi.attrib.get('NAME')
                        if re.match(pattern,group_name):
                            for t_oi in sub_oi.findall(".//OI"):
                                sub_oi_name = t_oi.attrib.get('NAME')
                                reference_object = t_oi.find(".//Reference")

                                parse_path = lambda s: s.replace("Data", "Trend").rsplit('/', 1)[0]

                                if group_name == "Analog Group" and not analog_reference_found:
                                    analog_reference_found = reference_object.attrib.get('Object')     
                                    self.result["Path Analog"] = parse_path(analog_reference_found)                             
                                elif group_name == "Binary Group" and not binary_reference_found:
                                    binary_reference_found = reference_object.attrib.get('Object')
                                    self.result["Path Binary"] = parse_path(binary_reference_found)  
                                    
                                trend_groups[group_name].append(sub_oi_name)

                    self.result["Trends"] = trend_groups

            return self.result
        except ET.ParseError as e:
            return {}
        except FileNotFoundError:
            return {}

    def insert_information(self):        

        result = self.parse_xml_file()

        if self.result and result:
            buffer_analog_path = self.result["Path Analog"] 
            buffer_binary_path = self.result["Path Binary"]
            buffer_version     = self.result["RuntimeVersion"] 
            buffer_server      = self.result["ServerFullPath"] 

            self.version_edit.setText(buffer_version)
            self.trend_path_analog.setText(buffer_analog_path) 
            self.trend_path_binary.setText(buffer_binary_path)
            self.server_path_edit.setText(buffer_server)

            self.trend_names_edit_analog.clear() 
            self.trend_names_edit_binary.clear() 

            for trend_name in self.result["Trends"]["Binary Group"]:
                self.trend_names_edit_binary.append(trend_name.strip())   

            for trend_name in self.result["Trends"]["Analog Group"]:
                self.trend_names_edit_analog.append(trend_name.strip())

        else:
            QMessageBox.information(self, "Um problema ocorreu", "O arquivo não é compativel ou não foi escolhido")

        return None 

    def search_files(self):
        # Open a file dialog to select a directory
        files, _ = QFileDialog.getOpenFileNames(self, 'Select Files')

        if files:
            # Display the selected files
            self.result_display.clear()
            self.result_display.setText(files[0])
        else:
            self.result_display.setText("No files selected.")
    
    def show_display_type_popup_analog(self, mode= True):
        trend_names = self.trend_names_edit_analog.toPlainText().split("\n")
        trend_names = [name for name in trend_names if name]  # Filter empty lines

        if mode:
            popup = DisplayTypePopup(trend_names, {"Line": 0, "Discrete Line": 1, "Digital": 2, "Bars": 3}, self)
            if popup.exec_() == QDialog.Accepted:
                selected_types, selected_colors = popup.get_selected_display_types()
                self.context["trendNameAnalog"] = [
                    {"name": trend_names[i].strip(), "displayType": selected_types[i], "displayColor":selected_colors[i]} for i in range(len(trend_names))
                ]
        else:
            self.context["trendNameAnalog"] = [
                {"name": trend_names[i].strip(), "displayType": 0, "displayColor":"-11179217"} for i in range(len(trend_names))
            ]

    def show_display_type_popup_binary(self, mode= True):
        trend_names = self.trend_names_edit_binary.toPlainText().split("\n")
        trend_names = [name for name in trend_names if name]  # Filter empty lines
        
        if mode:
            popup = DisplayTypePopup(trend_names, {"Line": 0, "Discrete Line": 1, "Digital": 2, "Bars": 3}, self)
            if popup.exec_() == QDialog.Accepted:
                selected_types, selected_colors = popup.get_selected_display_types()
                self.context["trendNameBinary"] = [
                    {"name": trend_names[i].strip(), "displayType": selected_types[i], "displayColor":selected_colors[i]} for i in range(len(trend_names))
                ]
        else:
            self.context["trendNameBinary"] = [
                {"name": trend_names[i].strip(), "displayType": 0, "displayColor":"-11179217"} for i in range(len(trend_names))
            ]


    
    def format_xml(self) -> tuple[bool,str]:
        try:
            env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
            template = env.get_template('template.jinja2')
            output = template.render(self.context)

            if not self.name:
                self.name = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            
            with open(f"./output/{self.name}.xml", "w") as file:
                file.write(output)

            return True, f"Saved as: {self.name}.xml"
            
        except Exception as e:        
            return False, f"ERROR: {str(e)}"

    def print_values(self):
        
        self.show_display_type_popup_analog(False)
        self.show_display_type_popup_binary(False)

        self.context["serverVersion"] = self.version_edit.text().strip()
        self.context["trendPathBinary"] = self.trend_path_binary.text().strip()
        self.context["trendPathAnalog"] = self.trend_path_analog.text().strip()
        self.context["serverPath"] = self.server_path_edit.text().strip()

        self.name = self.name_edit.text().strip()

        _, log = self.format_xml()
        QMessageBox.information(self, "Operation Finished", log)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec_())


# eof 
