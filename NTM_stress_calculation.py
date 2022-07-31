# This is a sample Python script.

# 1. Import `QApplication` and all the required widgets
from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtWidgets import QFileDialog, QGridLayout, QWidget, QTabWidget, QPushButton, QTableWidget, QComboBox
from PyQt6.QtWidgets import QVBoxLayout, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
import appstats

class Main_window(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("BEAM and NTM, stress")

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)


class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Extraction_FAT")
        self.tabs.addTab(self.tab2, "Input_data")
        self.tabs.addTab(self.tab3, "Checking")
        self.tabs.addTab(self.tab4, "Results_FAT")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Work with tab_2 "Input_Data"
        self.tab2.grid_layout = QGridLayout(self.tab2)

        self.combobox_input_direction = QComboBox()
        self.combobox_input_direction.addItems(["As is", "Reversed"])
        self.combobox_input_value_Z = QComboBox()
        self.combobox_input_value_Z.addItems(["Relative to COG", "Absolute"])

        self.push_button = QtGui.QFont()
        self.push_button.setFamily("Arial black")
        self.push_button.setPointSize(10)

        self.to_check_button = QPushButton("Click to check")
        self.to_check_button.clicked.connect(self.sending2check_window)
        self.to_check_button.setFixedWidth(150)
        self.to_check_button.setFont(self.push_button)

        self.label_input_direction = QtWidgets.QLabel('Z  Direction:')
        self.label_input_value = QtWidgets.QLabel('Value Z:')

        self.Table_Input = Table()
        self.columns = [" Cross-section name", "Area, mm2", "IYG, mm4",
                        "ZG, mm", "Upp", "Low", "Row 1", "Row 2", "Row 3", "Row 4", "Element number"]

        # set the font of columns headers
        column_font = QtGui.QFont()
        column_font.setFamily("Arial black")
        column_font.setPointSize(9)

        self.Table_Input.setColumnCount(len(self.columns))
        self.Table_Input.setRowCount(40)
        self.Table_Input.setHorizontalHeaderLabels(self.columns)

        for column_number in range(len(self.columns)):
            self.Table_Input.horizontalHeaderItem(column_number).setFont(column_font)
        self.Table_Input.horizontalHeader().setDefaultSectionSize(95)
        ###_________________________________________________###

        self.tab2.grid_layout.addWidget(self.Table_Input, 1, 0, 1, 6)
        self.tab2.grid_layout.addWidget(self.combobox_input_direction, 0, 1, 1, 1)
        self.tab2.grid_layout.addWidget(self.combobox_input_value_Z, 0, 3, 1, 1)
        self.tab2.grid_layout.addWidget(self.label_input_direction, 0, 0, 1, 1)
        self.tab2.grid_layout.addWidget(self.label_input_value, 0, 2, 1, 1)
        self.tab2.grid_layout.addWidget(self.to_check_button, 3, 4, 1, 1)
        self.tab2.grid_layout.addItem(QtWidgets.QSpacerItem(2, 2, QtWidgets.QSizePolicy.Policy.Expanding,
                                                            QtWidgets.QSizePolicy.Policy.Minimum), 0, 5, 1, 1)

        # working_with_Extraction_window
        self.grid_layout_extraction = QGridLayout(self.tab1)
        self.table_extraction = Table()
        self.table_extraction.lst_extraction_labels = ["TableValues", "FE", "LC", "NodeA_ID", "NodeB_ID", "N_elem",
                                                       "T1a_elem", "T1b_elem", "T2a_elem", "T2b_elem", "M1a_elem", "M1b_elem",
                                                       "M2a_elem", "M2b_elem"]

        self.table_extraction.setColumnCount(len(self.table_extraction.lst_extraction_labels))

        afont = QtGui.QFont()
        afont.setFamily("Arial black")
        afont.setPointSize(9)

        self.table_extraction.setHorizontalHeaderLabels(self.table_extraction.lst_extraction_labels)

        for header_number in range(len(self.table_extraction.lst_extraction_labels)):
            self.table_extraction.horizontalHeaderItem(header_number).setFont(afont)
        self.table_extraction.horizontalHeader().setDefaultSectionSize(95)

        self.button_open_file = QPushButton("Open_file")
        self.clear_file = QPushButton("Clear list")

        self.button_open_file.clicked.connect(lambda: self.reading_files_from_extraction())
        self.clear_file.clicked.connect(self.clear_clicked)
        self.grid_layout_extraction.addWidget(self.table_extraction, 1, 1, 1, 3)
        self.grid_layout_extraction.addWidget(self.button_open_file, 0, 1, 1, 1)
        self.grid_layout_extraction.addWidget(self.clear_file, 0, 2, 1, 1)
        self.grid_layout_extraction.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Policy.Expanding,
                                                                  QtWidgets.QSizePolicy.Policy.Minimum), 0, 3, 1, 1)

        # working with tab_3 "Checking and calculation"
        self.grid_layout_checking = QGridLayout(self.tab3)
        # table for checking entered data
        self.table_checking = Table()
        table_checking_labels = ["Location ID", "Area, mm2", "Inertia, mm4",
                                 "Z, mm", "Element number"]
        #self.table_checking.setRowCount(40)
        self.table_checking.setColumnCount(len(table_checking_labels))
        self.table_checking.horizontalHeader().setDefaultSectionSize(140)
        self.table_checking.setHorizontalHeaderLabels(table_checking_labels)
        for header_number in range(len(table_checking_labels)):
            self.table_checking.horizontalHeaderItem(header_number).setFont(afont)
        self.grid_layout_checking.addWidget(self.table_checking, 0, 1, 1, 3)
        # table for calculation subtleties
        # self.table_calculation = Table()
        # table_calculation_labels = ["Prefix to remove", "UL name", "LL name"]
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setFixedWidth(150)
        self.calculate_button.setFont(self.push_button)
        self.grid_layout_checking.addWidget(self.calculate_button, 1, 2, 1, 1)
        self.grid_layout_checking.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Policy.Expanding,
                                                                  QtWidgets.QSizePolicy.Policy.Minimum), 1, 3, 1, 1)
        self.grid_layout_checking.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Policy.Expanding,
                                                                  QtWidgets.QSizePolicy.Policy.Minimum), 1, 1, 1, 1)

        self.grid_layout_results = QGridLayout(self.tab4)
        self.table_result = Table()
        self.grid_layout_results.addWidget(self.table_result)



    def reading_files_from_extraction(self):

        path = QFileDialog.getOpenFileName(self, "Open load case file", "*.csv")
        self.lst_load = []

        with open(path[0], "r") as load_flow:
            for every_row in load_flow.readlines():
                if every_row.startswith(" ;FE"):
                    self.lst_load.append(every_row.split(";")[1:len(self.table_extraction.lst_extraction_labels)])
        self.table_extraction.set_data(self.lst_load)

    def clear_clicked(self):
        self.table_extraction.clearContents()
        self.table_extraction.setRowCount(0)

    def sending2check_window(self):
        rowCount = self.Table_Input.rowCount()
        columnCount = self.Table_Input.columnCount()
        list_location = [[] for number_row in range(rowCount)]
        for row in range(rowCount):
            widgetItem_checking = self.Table_Input.item(row, 0)
            if widgetItem_checking and (widgetItem_checking.text() and widgetItem_checking.text() != ''):
                for column in range(columnCount):
                    widgetItem = self.Table_Input.item(row, column)
                    try:
                        if widgetItem.text() == '':
                            raise Exception("There is empty deleted cell")
                        else:
                            list_location[row].append(widgetItem.text())
                    except:
                        list_location[row].append(0)

        list_location = [list_number for list_number in list_location if list_number != []]
        complete_location_lst = []
        element_lst = []

        for input_lists in list_location:
            #self.columns
            for index in range(len(input_lists[4:-1])):
                location_element_lst = []
                if (not self.columns[4+index].startswith("Row")) and (input_lists[4+index] != 0):
                    location_element_lst.append(input_lists[0]+"_"+self.columns[4+index]+"_"+str(input_lists[10]))
                    location_element_lst.append(input_lists[1])
                    location_element_lst.append(input_lists[2])
                    if self.combobox_input_direction.currentText() == "As is":
                        location_element_lst.append(float(input_lists[4+index])-float(input_lists[3]))
                    else:
                        location_element_lst.append(-float(input_lists[4 + index]) - float(input_lists[3]))
                    location_element_lst.append(input_lists[10])
                    #element_lst.append(input_lists[10])

                elif input_lists[4+index] != 0 and self.columns[4+index].startswith("Row"):
                    location_element_lst.append(input_lists[0]+"_"+self.columns[4+index]+"_"+str(input_lists[10]))
                    location_element_lst.append(input_lists[1])
                    location_element_lst.append(input_lists[2])
                    if self.combobox_input_direction.currentText() == "As is":
                        location_element_lst.append(str(input_lists[4 + index]))
                    else:
                        location_element_lst.append(-str(input_lists[4 + index]))
                    location_element_lst.append(input_lists[10])
                    #element_lst.append(input_lists[10])

                if len(location_element_lst) > 0:
                    complete_location_lst.append(location_element_lst)
        #print(1)
        self.table_checking.setRowCount(len(complete_location_lst))

        for widget_row in range(len(complete_location_lst)):
            for widget_column, item in enumerate(complete_location_lst[widget_row]):
                new_item = QTableWidgetItem(str(item))
                self.table_checking.setItem(widget_row, widget_column, new_item)

        try:
            data = self.lst_load
            self.calculate_button.clicked.connect(lambda: self.calculating_stress(data, complete_location_lst))
        except:
            message_box = QMessageBox(text="Please check th Extraction and Input tabs!")
            message_box.show()
            message_box.exec()

    def calculating_stress(self, data_loads, data_location):
        result_dict = dict()
        for index_location in range(len(data_location)):
            result_dict[data_location[index_location][0]] = dict()
            temp_variable = "FE1D:" + str(data_location[index_location][4])


            for index_loads in range(len(data_loads)):
                if temp_variable in data_loads[index_loads]:
                    key = data_loads[index_loads][1]
                    result_dict[data_location[index_location][0]][key] = []

                    result_dict[data_location[index_location][0]][key].append(data_loads[index_loads][4])
                    result_dict[data_location[index_location][0]][key].append(data_loads[index_loads][11])
                    result_dict[data_location[index_location][0]][key].append(data_loads[index_loads][12])
                    N_element = -float(data_loads[index_loads][4].strip())
                    M2a = -float(data_loads[index_loads][11].strip())
                    M2b = -float(data_loads[index_loads][12].strip())

                    ss_a = N_element/float(data_location[index_location][1]) + M2a*float(data_location[index_location][3])/float(data_location[index_location][2])
                    ss_b = N_element/float(data_location[index_location][1]) + M2b*float(data_location[index_location][3])/float(data_location[index_location][2])
                    result_dict[data_location[index_location][0]][key].append(ss_a)
                    result_dict[data_location[index_location][0]][key].append(ss_b)

        Location_unitary = [*result_dict]
        Load_unitary = [*result_dict[Location_unitary[0]]]

        Load_unitary.insert(0, 'Location_name')
        self.table_result.setColumnCount(len(Load_unitary))
        self.table_result.setRowCount(len(Location_unitary))
        self.table_result.setHorizontalHeaderLabels(Load_unitary)

        for number_row, location in enumerate(Location_unitary):
            new_item = QTableWidgetItem(location)
            self.table_result.setItem(number_row, 0, new_item)
            for number_column, load in enumerate(Load_unitary):
                if number_column != 0:
                    if abs(float(result_dict[location][load][3])) >= abs(float(result_dict[location][load][4])):
                        new_item = QTableWidgetItem(str(result_dict[location][load][3]))
                        self.table_result.setItem(number_row, number_column, new_item)
                    else:
                        new_item = QTableWidgetItem(str(result_dict[location][load][4]))
                        self.table_result.setItem(number_row, number_column, new_item)


        print(1)


class Table(QtWidgets.QTableWidget):
    def __init__(self, *args):
        super().__init__()

    def copy(self):
        copied_cells = sorted(self.selectedIndexes())
        copy_text = ''
        max_column = copied_cells[-1].column()
        for c in copied_cells:
            try:
                copy_text += self.item(c.row(), c.column()).text().replace('\n', '')

            except :
                pass

            if c.column() == max_column:
                copy_text += '\n'
            else:
                copy_text += '\t'

        QtWidgets.QApplication.clipboard().setText(copy_text)
        return None

    def paste(self):
        try:
            idxs = self.selectedIndexes()
            strow = idxs[0].row()
            stcol = idxs[0].column()
            enrow = idxs[-1].row()
            encol = idxs[-1].column()
            numrow = enrow - strow + 1
            numcol = encol - stcol + 1
        except:
            print('no cell selected')
            return

        rows = QtWidgets.QApplication.clipboard().text().splitlines(False)
        if numrow == 1 and numcol == 1:
            # Pastes all clipboard data if one cell is selected
            for i in range(len(rows)):
                items = rows[i].split('\t')
                for j in range(len(items)):
                    if (len(items[j]) > 0) and (stcol + j + 1 <= self.columnCount()):
                        if strow + i + 1 > self.rowCount():
                            self.setRowCount(self.rowCount() + 1)
                        self.setItem(strow + i, stcol + j, QtWidgets.QTableWidgetItem(items[j]))
        else:
            # this works if more than one cell is selected
            for i in range(numrow):
                items = rows[(i + 1) % len(rows) - 1].split('\t')
                for j in range(numcol):
                    item = items[(j + 1) % len(items) - 1]
                    self.setItem(strow + i, stcol + j, QtWidgets.QTableWidgetItem(item))

    def set_data(self, data):
        self.setRowCount(len(data))
        for n in range(len(data)):
            for m, item in enumerate(data[n]):
                new_item = QTableWidgetItem(item)
                self.setItem(n, m + 1, new_item)

    def delete(self):
        for c in sorted(self.selectedIndexes()):
            try:
                self.item(c.row(), c.column()).setText('')
            except:
                pass

    def cut(self):
        self.copy()
        self.delete()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        if event.key() == QtCore.Qt.Key.Key_C and (event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier):
            """ copies selected items to the clipboard """
            self.copy()

        # ==============================================================================================================

        if event.key() == QtCore.Qt.Key.Key_V and (event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier):
            """ pastes  data from clipboard """
            self.paste()

        # ==============================================================================================================

        if event.key() == QtCore.Qt.Key.Key_X and (event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier):
            """ pastes  data from clipboard """
            self.cut()

        # ==============================================================================================================

        if event.key() == QtCore.Qt.Key.Key_Delete:
            """ deletes data in multiple cells """
            self.delete()

        # ==============================================================================================================

        if event.key() == QtCore.Qt.Key.Key_A and (event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier):
            """ pastes  data from clipboard """
            self.selectAll()

        # ==============================================================================================================

        if event.key() == QtCore.Qt.Key.Key_S and (event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier):
            """ This switches colors in cells if they are colored. Use: ctrl + s """
            for c in sorted(self.selectedIndexes()):
                # print(self.item(c.row(), c.column()).background().color() == QtGui.QColor(0, 255, 0))
                if c.column() == 2:
                    if self.item(c.row(), c.column()).text() == 'Yes':
                        self.item(c.row(), c.column()).setText('No')
                        self.item(c.row(), c.column()).setBackground(QtGui.QColor(128, 128, 128))
                    else:
                        self.item(c.row(), c.column()).setText('Yes')
                        self.item(c.row(), c.column()).setBackground(QtGui.QColor(0, 255, 0))
                if c.column() > 2:
                    try:
                        if self.item(c.row(), c.column()).background().color() == QtGui.QColor(0, 255, 0):
                            self.item(c.row(), c.column()).setBackground(QtGui.QColor(128, 128, 128))
                        else:
                            self.item(c.row(), c.column()).setBackground(QtGui.QColor(0, 255, 0))
                    except:
                        pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec())
