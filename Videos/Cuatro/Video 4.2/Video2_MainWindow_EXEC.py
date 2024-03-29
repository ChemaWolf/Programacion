import sys
from time import sleep

from PyQt5 import QtCore, QtWidgets

#Revisar
from .Video_1.Video1_OpenGL_Rotation import PyQtOpenGL

from Video2_MainWindow_Complex_UI_Network import Ui_MainWindow
from Video2_Networking_TCPServer_TCPClient import TcpServer, TcpClient
                                    

class MainWindow_EXEC():
   
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)   
        

        self.ui.button_start_server.clicked.connect(self.start_server)
        
        
        self.ui.button_client_1.clicked.connect(self.connect_to_server_1)   
        self.ui.lineEdit_client_1.returnPressed.connect(self.send_data_1)    

        self.ui.button_client_2.clicked.connect(self.connect_to_server_2)   
        self.ui.lineEdit_client_2.returnPressed.connect(self.send_data_2)                
        
        
        self.init_tabs()
        
        self.MainWindow.show()
        sys.exit(app.exec_()) 

    
    def connect_to_server_1(self):
    
        self.tcp_client_1 = TcpClient(line_edit_widget=self.ui.lineEdit_client_1, text_widget=self.ui.textEdit_client_1)
        self.tcp_client_1.connect_server()              
        self.ui.button_client_1.setEnabled(False)
        
        
        self.tcp_client_1.socket.readyRead.connect(self.tcp_client_1.read_data)
        self.tcp_client_1.socket.disconnected.connect(self.server_disconnect_1)        
        self.tcp_client_1.socket.error.connect(self.server_error_1)

    def server_disconnect_1(self):
        self.tcp_client_1.socket.close()
        self.ui.button_client_1.setEnabled(True)
        
    def server_error_1(self):
        error = "Error: {}".format(self.tcp_client_1.socket.errorString())
        self.display_text_1(error)
        self.tcp_client_1.socket.close()
        self.ui.button_client_1.setEnabled(True)    

    def display_text_1(self, text):
        self.ui.textEdit_client_1.append(text) 

    def send_data_1(self):
        self.tcp_client_1.write_data()
                
    
    def connect_to_server_2(self):
    
        self.tcp_client_2 = TcpClient(line_edit_widget=self.ui.lineEdit_client_2, text_widget=self.ui.textEdit_client_2)
        self.tcp_client_2.connect_server()              
        self.ui.button_client_2.setEnabled(False)
        
    
        self.tcp_client_2.socket.readyRead.connect(self.tcp_client_2.read_data)
        self.tcp_client_2.socket.disconnected.connect(self.server_disconnect_2)        
        self.tcp_client_2.socket.error.connect(self.server_error_2)

    def server_disconnect_2(self):
        self.tcp_client_2.socket.close()
        self.ui.button_client_2.setEnabled(True)
        
    def server_error_2(self):
        error = "Error: {}".format(self.tcp_client_2.socket.errorString())
        self.display_text_2(error)
        self.tcp_client_2.socket.close()
        self.ui.button_client_2.setEnabled(True)    

    def display_text_2(self, text):
        self.ui.textEdit_client_2.append(text) 

    def send_data_2(self):
        self.tcp_client_2.write_data()   
               
    
    def start_server(self):
        self.tcp_server = TcpServer()
                
    
    def init_tabs(self):
        open_gl = PyQtOpenGL(parent=self.ui.frame_gl)   
        open_gl.setMinimumSize(300, 300)                
        open_gl.paint_0 = False
        open_gl.paint_1 = False
        open_gl.paint_2 = False
        open_gl.resize_lines = False 
        open_gl.paint_rotation = False

        
        self.ui.comboBox.hide()
        self.drop_combo = DragDropCombo(self.MainWindow)
        self.drop_combo.setMinimumSize(QtCore.QSize(141, 0))
        self.ui.horizontalLayout_2.addWidget(self.drop_combo)
        
        
        self.ui.pushButton.hide()

        self.drop_button = DragDropButton('DropButton', self.MainWindow)
        self.drop_button.setMinimumSize(QtCore.QSize(161, 0))
        self.ui.horizontalLayout_2.addWidget(self.drop_button)


        self.update_tree()
        self.update_calendar()
        self.update_progressbar()
        

    def update_tree(self): 
        self.ui.treeWidget.headerItem().setText(1, 'Header 2')
        self.ui.treeWidget.topLevelItem(0).setText(1, "Item 2")
        self.ui.treeWidget.topLevelItem(0).addChild(QtWidgets.QTreeWidgetItem())
        self.ui.treeWidget.topLevelItem(0).child(0).setText(1, "Subitem 2")
        
    def print_tree(self):
        header0 = self.ui.treeWidget.headerItem().text(0)
        header1 = self.ui.treeWidget.headerItem().text(1)
        print(header0 + '\n' + header1 + '\n')        
        
    
    def update_calendar(self):
        self.ui.calendarWidget.selectionChanged.connect(self.update_date)

    def update_date(self):
        self.ui.dateEdit.setDate(self.ui.calendarWidget.selectedDate())      
    
    
    def update_progressbar(self):
        self.ui.radioButton_start.clicked.connect(self.start_progressbar)
        self.ui.radioButton_stop.clicked.connect(self.stop_progressbar)
        self.ui.radioButton_reset.clicked.connect(self.reset_progressbar)
        self.progress_value = 0
        self.stop_progress = False

    def progressbar_counter(self, start_value=0):
        self.run_thread = RunThread(parent=None, counter_start=start_value)
        self.run_thread.start()
        self.run_thread.counter_value.connect(self.set_progressbar)
                
    def set_progressbar(self, counter):
        if not self.stop_progress:
            self.ui.progressBar.setValue(counter)        
                   
    def start_progressbar(self):
        self.stop_progress = False
        self.progress_value = self.ui.progressBar.value()        
        self.progressbar_counter(self.progress_value)
           
    def stop_progressbar(self):
        self.stop_progress = True
        try: self.run_thread.stop()
        except: pass
           
    def reset_progressbar(self):
        self.stop_progressbar()
        self.progress_value = 0
        self.stop_progress = False
        self.ui.progressBar.reset()
        

class RunThread(QtCore.QThread):   
    counter_value = QtCore.pyqtSignal(int)             
    def __init__(self, parent=None, counter_start=0):
        super(RunThread, self).__init__(parent)
        self.counter = counter_start
        self.is_running = True
        
    def run(self):
        while self.counter < 100 and self.is_running == True:
            sleep(0.1)
            self.counter += 1
            print(self.counter)
            self.counter_value.emit(self.counter)     
            
    def stop(self):
        self.is_running = False
        print('stopping thread...')
        self.terminate()


class DragDropButton(QtWidgets.QPushButton):
    
    def __init__(self, text, parent):
        super().__init__(text, parent)       
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        self.setText(event.mimeData().text())
    

class DragDropCombo(QtWidgets.QComboBox):    

    def __init__(self, parent):
        super().__init__(parent)        
        self.setAcceptDrops(True)
                            
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()                            

    def dropEvent(self, event):
        self.addItem(event.mimeData().text())
        
         
        
if __name__ == "__main__":
    MainWindow_EXEC()
