import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import phoneBook_min #модуль главного окна PyQt
import add_new_min #модель виджета добавления нового контакта PyQt
import mainModel #модель классов и методов для телеф книги


class phoneBookMain(QMainWindow, phoneBook_min.Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__()
        self.setupUi(self)

        self.phonelist = mainModel.PhoneBook()                 #Создание экземпляра класса для списка контактов
        self.control = mainModel.Controller(self.phonelist)    #Создание экземпляра класса контроллера

        self.pushButton.clicked.connect(self.newContact)       #Запуск виджета addNew для создания нового контакта
        self.pushButton_3.clicked.connect(self.edit)           #Редактирование
        self.pushButton_4.clicked.connect(self.Search)         #Очистка поля поиска
        self.pushButton_7.clicked.connect(self.deleteContact)  #Удаление контакта
        self.pushButton_8.clicked.connect(self.toDisplay)      #Действие по кнопке Back
        
        self.actionRead_File.triggered.connect(self.readFile)  #Чтение из файла        
        self.actionSave_File.triggered.connect(self.saveFile)  #Запись в файл
        self.actionExit.triggered.connect(self.window().close) #Выход из программы


        self.listWidget.itemActivated.connect(self.itemActivated_event) #Активация элемента телеф книги кликом мыши 
        
    def itemActivated_event(self, item):             #Метод для вывода полной инфо о контакте в виджет listWidget        
        #personName = item.text()
        person = self.control.phonesArray.items[self.listWidget.row(item)]
        
        #searchRes = self.control.search(personName)  #Поиск по имени инфо о контакте
        self.listWidget.clear()
        self.listWidget.setEnabled(False)            #Деактивация listwidget, чтобы запретить активацию полей в виджете кликом
        self.listWidget.addItem(person.name)      #Вывод полной инфы о контакте в виджет
        for i in person.phones:
            self.listWidget.addItem(str(i))            
        self.listWidget.addItem(person.email)
        
        #self.listWidget_2.addItem(searchRes.idContact) 
        
        self.forEdit = person.name                #Сохранение в переменную имя и Id выбранного контакта для работы с Edit
        self.idContactEdit = person.idContact     #
        self.pushButton_3.setEnabled(True)           #Активация кнопки Edit и Del для выбранного контакта
        self.pushButton_7.setEnabled(True)           #
        self.pushButton_8.setEnabled(True)
        
    def toDisplay(self):
        self.listWidget.clear()
        self.lineEdit.clear()
        self.pushButton_3.setEnabled(False) #После нажатия кнопки Back кнопки становятся неактивными и загружаются контакты
        self.pushButton_7.setEnabled(False) #
        self.pushButton_8.setEnabled(False) #
        self.listWidget.setEnabled(True)    #Активация listwidget, чтобы можно было выбирать контакты из списка для просмотра
        self.control.sortByName()
        for item in self.control.phonesArray.items:
            self.listWidget.addItem(item.name)
        
    def newContact(self):                   #Создание экземпляра формы для добавления нового контакта
        self.addContact = addNew()
        self.addContact.sendData.connect(self.createContact)
        self.addContact.show()
        
    def createContact(self, name = None, phones = None, email = None, idContact = None):
        self.control.addSimplePerson(name, phones, email, idContact)
        self.actionSave_File.setEnabled(True)    #Активация кнопки Save после добавления первого контакта
        self.toDisplay()
        self.statusTimer()                  #Запуск таймера для статусбара
        self.statusBar.showMessage('Contact added')
        
    def edit(self):                         #Создание экземпляра формы для редактирования контакта
        searchEdit = self.control.searchForEdit(self.forEdit, self.idContactEdit)

        self.editContact = editContact(searchEdit.name, searchEdit.phones, searchEdit.email, searchEdit.idContact)
        self.editContact.sendEditedData.connect(self.editSingleContact)        
        self.editContact.show()
    
    def editSingleContact(self, name = None, phones = None, email = None, idContact = None):
        searchEdit = self.control.searchById(idContact)

        res = self.control.editContact(name, phones, email, idContact)

        self.listWidget.clear()        
        self.listWidget.addItem(res.name)
        for i in res.phones:
            self.listWidget.addItem(str(i))            
        self.listWidget.addItem(res.email)
        
    def deleteContact(self):
        searchDelete = self.control.searchById(self.idContactEdit)
        if searchDelete is not None:
            self.deleteEvent()        
            
    def deleteEvent(self):        
        reply = QMessageBox.question(self, 'Confirm Deleting',
            "Are you sure you want to delete it?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.control.deleteContact(self.forEdit, self.idContactEdit)
            self.toDisplay()
            self.statusTimer()
            self.statusBar.showMessage('Contact ' + self.forEdit + ' is deleted')   
    
    def readFile(self):
        file, _ = QFileDialog.getOpenFileName(self, "Upload Contacts")
        if len(file) > 0:
            reading = self.control.readFile(file)
            self.toDisplay()
            self.actionSave_File.setEnabled(True)
            
    def saveFile(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Backup Contacts", "*.csv")
        
        if len(filename) > 0:
            self.control.addToFile(filename)
        self.statusTimer()
        self.statusBar.showMessage('File saved')
            
    def Search(self):                                      #Поиск контакта в тел.книге        
        self.listWidget.clear()
        
        name = self.lineEdit.text()                        #Запись в переменную name введенного имени для поиска        
        
        #personId = item.text(idContact)
        #print(personId)
        
        searchRes = self.control.search_with_answ(name)    #Поиск по имени инфо о контакте

        if searchRes != False:                             #Если есть результат, выводим
            self.pushButton_8.setEnabled(True)
            for item in searchRes:
                self.listWidget.addItem(item.name)
        else:                                              #Если ничего нет, выводим сообщение и выводим список всех контактов
            self.statusTimer()
            self.statusBar.showMessage('Not Found')
    
    def statusTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.start(1800)
        self.timer.timeout.connect(self.clearStatusBar)
        self.timer.setSingleShot(True)                     #Таймер выполняется один раз        
            
    def clearStatusBar(self):
        self.statusBar.clearMessage()
        self.toDisplay()    
            
    def closeEvent(self, event):                           #Запрос на сохранение текущих данных перед закрытием
        reply = QMessageBox.question(self, 'Message',
            "Save changes before exiting?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.saveFile()                                #Сохранение данных и выход
            event.accept()
        else:
            event.accept()                                 #Выход без сохранения
            
    def keyPressEvent(self, e):                            #Выход из программы по Esc
        if e.key() == Qt.Key_Escape:
            self.close()
                
class addNew(QWidget, add_new_min.Ui_Form):
    sendData = QtCore.pyqtSignal(str, list, str, str)      #Сигнал добавления контакта
 
    def __init__(self):
        super().__init__()        
        self.setupUi(self)  
        
        #Действия по кнопкам
        self.buttonBox.rejected.connect(self.window().close) 
        self.buttonBox.accepted.connect(self.addPerson)
        
    def addPerson(self):        
        p0 = mainModel.Phone(self.lineEdit_2.text(),int(self.comboBox_2.currentIndex()))#телефоны
        p1 = mainModel.Phone(self.lineEdit_3.text(),int(self.comboBox_3.currentIndex()))#
        p2 = mainModel.Phone(self.lineEdit_4.text(),int(self.comboBox_4.currentIndex()))#
        p3 = mainModel.Phone(self.lineEdit_5.text(),int(self.comboBox_5.currentIndex()))#
        phones = []
        phone = [p0, p1, p2, p3]
        
        name = self.lineEdit.text()
        for i in range(len(phone)):
            if len(phone[i].number) != 0:
                phones.append(phone[i])
        email = self.lineEdit_6.text()
        
        idContact = str(id(name))                           #Создание уникального Id контакта через переменную "Имя"
        
        self.sendData.emit(name, phones, email, idContact)  #Запуск сигнала в MainWindow для создания контакта 
        self.closeForm()

    def closeForm(self):          
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()

        self.close()
        self.destroy()        
            
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        
class editContact(QWidget, add_new_min.Ui_Form):
    sendEditedData = QtCore.pyqtSignal(str, list, str, str) #Сигнал редактирования
 
    def __init__(self, name, phones, email, idContact):
        super().__init__()        
        self.setupUi(self) 
        self.setWindowTitle("Edit Contact")
        self.name = name
        self.phones = phones
        self.email = email
        self.idContact = idContact
            
        if len(self.name) != 0:
            self.lineEdit.setText(self.name)#Имя
            
        if self.phones != []: #телефоны
            listNumber = [self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.lineEdit_5]
            listKind = [self.comboBox_2, self.comboBox_3, self.comboBox_4, self.comboBox_5]
                           
            for p in range(len(self.phones)):  
                listNumber[p].setText(self.phones[p].number)
                listKind[p].setCurrentIndex(self.phones[p].kind)
                
        if len(self.email) != 0:
            self.lineEdit_6.setText(self.email)#Почта
            
        #Действия по кнопкам
        self.buttonBox.rejected.connect(self.window().close) 
        self.buttonBox.accepted.connect(self.editData)
            
    def editData(self):        
        p0 = mainModel.Phone(self.lineEdit_2.text(),int(self.comboBox_2.currentIndex()))#телефоны
        p1 = mainModel.Phone(self.lineEdit_3.text(),int(self.comboBox_3.currentIndex()))#
        p2 = mainModel.Phone(self.lineEdit_4.text(),int(self.comboBox_4.currentIndex()))#
        p3 = mainModel.Phone(self.lineEdit_5.text(),int(self.comboBox_5.currentIndex()))#
        
        phones = []
        phone = [p0, p1, p2, p3]
        
        name = self.lineEdit.text()
        for i in range(len(phone)):
            if len(phone[i].number) != 0:
                phones.append(phone[i])
        email = self.lineEdit_6.text()
        
        self.sendEditedData.emit(name, phones, email, self.idContact) #Посыл сигнала на редактирование контакта
        self.closeForm()

    def closeForm(self):          
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()

        self.close()
        self.destroy()
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = phoneBookMain()
    ex.show()
    app.exec()