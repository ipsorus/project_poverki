import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileDialog, QToolTip, QPushButton, QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import MainWindow_poverki  #модуль главного окна PyQt
import generator_for_users_v_1_0 as generator

from datetime import datetime, date, time, timedelta
import os
import errno


class main_window(QMainWindow, MainWindow_poverki.Ui_MainWindow):
    sendData = QtCore.pyqtSignal(str, list, str, str)

    def __init__(self, parent = None):
        super(main_window, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.create)       #Запуск


    def applic_constructor(self, filepath, result, part, counter_zav, counter_applic):

        #Тип СИ (№ Гос. реестра)
        mitypeNumber = self.textEdit.toPlainText()
        print(mitypeNumber)

        #Модификация СИ
        modification = self.textEdit_2.toPlainText()

        #Дата производства СИ
        manufactureYear = self.spinBox_3.text()
        if manufactureYear == '----':
            manufactureYear = ''
        else:
            manufactureYear = int(self.spinBox_3.text())

        #Заводской номер СИ
        prefix_zav_number = self.textEdit_3.toPlainText()
        tail_zav_number = self.textEdit_5.toPlainText()

        #Номер свидетельства/извещения о непригодности СИ
        prefix_applic_number = self.textEdit_7.toPlainText()
        tail_applic_number = self.textEdit_9.toPlainText()

        #Условный шифр знака поверки
        signCipher = self.textEdit_6.toPlainText()
        signCipher = signCipher.upper()

        #Дата поверки (формат гггг-мм-дд)
        vrfDate = self.dateEdit.text()
        print(vrfDate)

        #Дата действия поверки (формат гггг-мм-дд), можно оставить пустое значение ''
        validDate = self.textEdit_24.toPlainText()

        #Методика поверки
        method = self.textEdit_10.toPlainText()

        #Знак поверки в паспорте (true/false)
        signPass = self.checkBox.isChecked()
        print(signPass)

        #Знак поверки на СИ (true/false)
        signMi = self.checkBox_2.isChecked()

        #ГПЭ
        npe_number = self.textEdit_11.toPlainText()

        #Эталоны
        uve_number = self.textEdit_12.toPlainText()

        #Стандартные образцы
        ses_number = self.textEdit_13.toPlainText()             # Тип СО

        ses_manufactureYear = self.spinBox_4.text()             # Год производства
        if ses_manufactureYear == '----':
            ses_manufactureYear = ''
        else:
            ses_manufactureYear = int(self.spinBox_4.text())
        ses_manufactureNum = self.textEdit_14.toPlainText()     # Заводской номер

        #СИ, применяемые в качестве эталонов
        mieta_number = self.textEdit_15.toPlainText()

        #СИ, применяемые при поверке
        mis_number = self.textEdit_16.toPlainText()             # Тип СИ (№ Гос. реестра)
        mis_manufactureNum = self.textEdit_17.toPlainText()     # Заводской номер

        #Вещества (материалы)
        reagent_number = self.textEdit_18.toPlainText()

        #Название файла
        name_of_file = r'заявка_' + mitypeNumber + '_часть_' + str(part) + '_записей_' + str(result) + '_шифр_' + signCipher + '.xml'

        #Путь сохранения файла
        FileFullPath = os.path.join(filepath, name_of_file)

        with open (FileFullPath, 'w', encoding='utf-8') as sample:

            header_1 = f'<?xml version="1.0" encoding="utf-8" ?>\n'
            header_2 = f'<gost:application xmlns:gost="urn://fgis-arshin.gost.ru/module-verifications/import/2020-04-14">\n'
            header = header_1 + header_2
            sample.write(header)

        for n in range(result):

            manufactureNum = prefix_zav_number + str(counter_zav) + tail_zav_number
            certNum = prefix_applic_number + str(counter_applic) + tail_applic_number

            with open (FileFullPath, 'a', encoding='utf-8') as sample_body:

                result_start = f'<gost:result>\n'
                miInfo_start = f'<gost:miInfo>\n'
                singleMI_start = f'<gost:singleMI>\n'
                mitypeNumber_str = f'<gost:mitypeNumber>{mitypeNumber}</gost:mitypeNumber>\n'
                manufactureNum_str = f'<gost:manufactureNum>{manufactureNum}</gost:manufactureNum>\n'
                manufactureYear_str = f'<gost:manufactureYear>{manufactureYear}</gost:manufactureYear>\n'
                modification_str = f'<gost:modification>{modification}</gost:modification>\n'
                singleMI_close = f'</gost:singleMI>\n'
                miInfo_close = f'</gost:miInfo>\n'

                miInfo = miInfo_start + singleMI_start + mitypeNumber_str + manufactureNum_str + manufactureYear_str + modification_str + singleMI_close + miInfo_close

                signCipher_str = f'<gost:signCipher>{signCipher}</gost:signCipher>\n'
                vrfDate_str = f'<gost:vrfDate>{vrfDate}+03:00</gost:vrfDate>\n'
                if validDate == '':
                    valid = signCipher_str + vrfDate_str
                else:
                    validDate_str = f'<gost:validDate>{validDate}+03:00</gost:validDate>\n'
                    valid = signCipher_str + vrfDate_str + validDate_str

                applicable_start = f'<gost:applicable>\n'
                certNum_str = f'<gost:certNum>{certNum}</gost:certNum>\n'
                signPass_str = f'<gost:signPass>{signPass}</gost:signPass>\n'
                signMi_str = f'<gost:signMi>{signMi}</gost:signMi>\n'
                applicable_close = f'</gost:applicable>\n'
                verification_res = applicable_start + certNum_str + signPass_str + signMi_str + applicable_close

                docTitle = f'<gost:docTitle>{method}</gost:docTitle>\n'

                means_start = f'<gost:means>\n'

                npe = ''
                uve = ''
                ses = ''
                mieta = ''
                mis = ''
                reagent = ''

                if npe_number != '':
                    npe_start = f'<gost:npe>\n'
                    npe_number_str = f'<gost:number>{npe_number}</gost:number>\n'
                    npe_close = f'</gost:npe>\n'
                    npe = npe_start + npe_number_str + npe_close

                if uve_number != '':
                    uve_start = f'<gost:uve>\n'
                    uve_number_str = f'<gost:number>{uve_number}</gost:number>\n'
                    uve_close = f'</gost:uve>\n'
                    uve = uve_start + uve_number_str + uve_close

                if ses_number != '':
                    ses_start = f'<gost:ses>\n'
                    se_start = f'<gost:se>\n'
                    ses_number_str = f'<gost:typeNum>{ses_number}</gost:typeNum>\n'
                    ses_manufactureYear_str = f'<gost:manufactureYear>{ses_manufactureYear}</gost:manufactureYear>\n'
                    ses_manufactureNum_str = f'<gost:manufactureNum>{ses_manufactureNum}</gost:manufactureNum>\n'
                    se_close = f'</gost:se>\n'
                    ses_close = f'</gost:ses>\n'
                    ses = ses_start + se_start + ses_number_str + ses_manufactureYear_str + ses_manufactureNum_str + se_close + ses_close

                if mieta_number != '':
                    mieta_start = f'<gost:mieta>\n'
                    mieta_number_str = f'<gost:number>{mieta_number}</gost:number>\n'
                    mieta_close = f'</gost:mieta>\n'
                    mieta = mieta_start + mieta_number_str + mieta_close

                if mis_number != '':
                    mis_start =	f'<gost:mis>\n'
                    mi_start = f'<gost:mi>\n'
                    mis_number_str = f'<gost:typeNum>{mis_number}</gost:typeNum>\n'
                    mis_manufactureNum_str = f'<gost:manufactureNum>{mis_manufactureNum}</gost:manufactureNum>\n'
                    mi_close = f'</gost:mi>\n'
                    mis_close =	f'</gost:mis>\n'
                    mis = mis_start + mi_start + mis_number_str + mis_manufactureNum_str + mi_close + mis_close

                if reagent_number != '':
                    reagent_start =	f'<gost:reagent>\n'
                    reagent_number_str = f'<gost:number>{reagent_number}</gost:number>\n'
                    reagent_close =	f'</gost:reagent>\n'
                    reagent = reagent_start + reagent_number_str + reagent_close

                means_close = f'</gost:means>\n'
                result_close = f'</gost:result>\n'

                body = result_start + miInfo + valid + verification_res + docTitle + means_start + npe + uve + ses + mieta + mis + reagent + means_close + result_close
                sample_body.write(body)

        with open (FileFullPath, 'a', encoding='utf-8') as sample:
            footer = f'</gost:application>\n'
            sample.write(footer)

        self.statusBar().showMessage('Формирование файла завершено!')

        print('Формирование файла завершено!')


    def create(self):
        #Общее количество записей о поверках СИ
        TOTAL_RESULTS = int(self.spinBox.text())

        #Количество записей о поверках СИ в одной заявке (не более 5000 записей)
        #Условие: Если общее количество записей не превышает 5000, то вписать значение из TOTAL_RESULTS
        RESULTS_IN_APP = int(self.spinBox_2.text())

        filepath = QFileDialog.getExistingDirectory()

        self.statusBar().showMessage(filepath)

        print(type(TOTAL_RESULTS))
        print(RESULTS_IN_APP)
        print(filepath)

        parts = TOTAL_RESULTS // RESULTS_IN_APP

        #Заводской номер СИ
        counter_zav_number = 0

        changeable_zav_number = self.textEdit_4.toPlainText()
        if changeable_zav_number != '':
            counter_zav_number = int(changeable_zav_number)

        #Номер свидетельства/извещения о непригодности СИ
        counter_applic_number = 0

        changeable_applic_number = self.textEdit_4.toPlainText()
        if changeable_applic_number != '':
            counter_applic_number = int(changeable_applic_number)

        for j in range(parts):

            if TOTAL_RESULTS <= RESULTS_IN_APP:
                self.applic_constructor(filepath, TOTAL_RESULTS, j + 1, counter_zav_number, counter_applic_number)
            elif TOTAL_RESULTS > RESULTS_IN_APP:
                self.applic_constructor(filepath, RESULTS_IN_APP, j + 1, counter_zav_number, counter_applic_number)
                TOTAL_RESULTS -= RESULTS_IN_APP
            counter_zav_number += 1
            counter_applic_number += 1
            print(counter_zav_number)
            print(counter_applic_number)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_window()
    ex.show()
    app.exec()