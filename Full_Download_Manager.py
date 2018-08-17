from PyQt5.QtWidgets import QMainWindow , QFileDialog , QApplication , qApp , QMessageBox
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QImage , QPixmap
from PyQt5.QtCore import pyqtSignal , QObject
from os import path , system , chdir , mkdir
from sys import argv , platform
from humanize import naturalsize as nz , naturaltime as nt
from urllib import request as ur
import pafy , time , threading , pycurl

#>---------------------------------------------------------------------------------------------------------------------<

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"main.ui"))

class MainApp(QMainWindow, FORM_CLASS):
   def __init__(self,parent=None):
       super(MainApp,self).__init__(parent)
       QMainWindow.__init__(self)
       self.setupUi(self)
       self._new_window = None
       self.Handle_Button()
       self.setWindowTitle("Downoad Manager")

   def Handle_Button(self):
       self.pushButton_2.clicked.connect(self.Handle_Browse)
       self.pushButton_5.clicked.connect(self.Youtube_Browse)
       self.pushButton_7.clicked.connect(self.Playlist_Browse)
       self.pushButton_11.clicked.connect(self.Get_Video_Youtube)
       self.pushButton_22.clicked.connect(self.Playlist_Search)
       self.pushButton.clicked.connect(self.Start_Threading)
       self.pushButton_8.clicked.connect(self.Start_Threading_2)
       self.pushButton_9.clicked.connect(self.Start_Threading_3)
       self.pushButton_3.clicked.connect(self.Terminate_Download)
       self.pushButton_10.clicked.connect(self.Terminate_Download)
       self.pushButton_12.clicked.connect(self.Terminate_Download)

   def Handle_Browse(self):
       location = QFileDialog.getExistingDirectory(self, "Select Download Location", directory='.')
       self.lineEdit.setText(location)
       QApplication.processEvents()

   def Youtube_Browse(self):
       save_location = QFileDialog.getExistingDirectory(self, "Select Download Location", directory='.')
       self.lineEdit_9.setText(save_location)
       QApplication.processEvents()

   def Playlist_Browse(self):
       save_location = QFileDialog.getExistingDirectory(self ,"Select Download Location" ,directory='.')
       self.lineEdit_11.setText(save_location)
       QApplication.processEvents()

   def Get_Video_Youtube(self):
       link = self.lineEdit_10.text()
       #link = "https://www.youtube.com/watch?v=wlJzRAUexV0"
       try:
           video = pafy.new(link)
           self.label_27.setText(video.title)
           imageurl = video.thumb
           imageurlopen = ur.urlopen(imageurl).read()
           image = QImage()
           image.loadFromData(imageurlopen)
           mypixmap = QPixmap(image)
           self.label_11.setPixmap(mypixmap)
           self.label_28.setText(video.author)
           self.textBrowser.setText(video.duration)
           self.label_40.setText(video.description)
           st = video.streams
           for s in st:
               size = nz(s.get_filesize())
               data = '{} {} {} {}'.format(s.mediatype, s.extension, s.quality, size)
               self.comboBox_2.addItem(data)
               QApplication.processEvents()
       except Exception as e:
           print(e)

   def Playlist_Search(self):
       url = self.lineEdit_12.text()
       #url = "https://www.youtube.com/playlist?list=PLY_6uAtgkYXmXFl-zzZ0wQErGi4AbgSkn"
       playlist = pafy.get_playlist(url)
       videos = playlist['items']
       length = str(len(videos))
       self.length = length
       self.label_29.setText(playlist['title'])
       self.label_38.setText(playlist['description'])
       author = str(playlist['author'])
       self.label_36.setText(author)
       QApplication.processEvents()

   def Progress_Bar(self,Prog_value,speed,Dl_size,name,T_size,e_time):
       self.label_5.setText(name)
       self.label_9.setText(speed+"  KB/S")
       self.label_8.setText(Dl_size)
       self.label_13.setText(e_time)
       self.progressBar.setValue(Prog_value)
       self.label_6.setText(T_size)

   def Progress_Bar_2(self,total,recvd,rate,eta):
       self.progressBar_2.setValue((recvd * 100) / total)
       size = nz(total)
       self.textBrowser_2.setText("  "+nz(recvd)+" Of "+size)
       self.textBrowser_3.setText("  "+str(round(rate)) +"  KB/S")
       if round(eta, 0) > 60:
           m = int(round(eta, 0) / 60)
           s = round(eta, 0) % 60
           self.textBrowser_9.setText(str(m) + " Min " + str(s) + " Sec")
       else:
           self.textBrowser_9.setText(str(round(eta, 0)) + " Sec")

   def Progress_Bar_3(self,total,recvd,rate,eta,current,thumb):
       self.progressBar_3.setValue((recvd * 100) / total)
       size = nz(recvd)
       total_size = nz(total)
       self.textBrowser_22.setText("    " + str(round(rate)) + "   KB/S")
       self.textBrowser_23.setText("    " + size + "   Of   " + total_size)
       if round(eta, 0) > 60:
           m = int(round(eta, 0) / 60)
           s = round(eta, 0) % 60
           self.textBrowser_25.setText(str(m) + " Min " + str(int(s)) + " Sec")
       else:
           self.textBrowser_25.setText(str(round(eta, 0)) + " Sec")
       self.textBrowser_24.setText("    " + str(current) + "   Of   " + self.length)
       def set_thumbnail():
           imageurlopen = ur.urlopen(thumb).read()
           image = QImage()
           image.loadFromData(imageurlopen)
           mypixmap = QPixmap(image)
           self.label_16.setPixmap(mypixmap)
       thread = threading.Thread(target=set_thumbnail)
       thread.start()

   def Handle_Options(self,check):
       if check==True :
           if self.checkBox_9.isChecked() :
                   option = int(self.comboBox_3.currentIndex())
                   op = str(platform)
                   if option == 0:
                       qApp.exit()
                   elif option == 1 :
                       if op =="windows":
                           system('shutdown -s')
                       elif op =="linux":
                           system('poweroff')
                   elif option == 2:
                       if op =="windows":
                           system(r'%windir%\system32\rundll32.exe powrprof.dll,SetSuspendState Hibernate')
                       elif op =="linux":
                           system('systemctl suspend ')
                   elif option == 3:
                       if op =="windows":
                           system('shutdown -r')
                       elif op =="linux":
                           system('reboot')
           else:
               QMessageBox.about(self , "Download Complete" , "Download Finished" )

   def Start_Threading(self):
       url = self.lineEdit_2.text()
       location = self.lineEdit.text()
       Start_Thread = ThreadClass()
       Start_Thread.data.connect(self.Progress_Bar)
       Start_Thread.stat.connect(self.Handle_Options)
       thread = threading.Thread(target=Start_Thread.run,args=(url,location))
       thread.start()

   def Start_Threading_2(self):
       url = self.lineEdit_10.text()
       dest = self.lineEdit_9.text()
       qual = self.comboBox_2.currentIndex()
       Start_Thread_2 = ThreadClass_2()
       Start_Thread_2.progress.connect(self.Progress_Bar_2)
       Start_Thread_2.stat2.connect(self.Handle_Options)
       thread = threading.Thread(target=Start_Thread_2.run , args=(url,dest,qual))
       thread.start()

   def Start_Threading_3(self):
       url = self.lineEdit_12.text()
       dest = self.lineEdit_11.text()
       Start_Thread_3 = ThreadClass_3()
       Start_Thread_3.Progress_data.connect(self.Progress_Bar_3)
       Start_Thread_3.stat3.connect(self.Handle_Options)
       thread = threading.Thread(target=Start_Thread_3.run , args=(url,dest))
       thread.start()

   def Terminate_Download(self):
       qApp.exit()

# >---------------------------------------------------------------------------------------------------------------------<

class ThreadClass(QObject):
   data = pyqtSignal(int,str,str,str,str,str)
   stat = pyqtSignal(bool)

   def __init__(self, parent=None):
       super(ThreadClass, self).__init__(parent)

   def run(self,url,location):
       f_name = url.split("/")[-1]
       file_name = path.join(location, f_name)
       try:
           c = pycurl.Curl()
           c.setopt(c.URL, url)
           def curl_progress(total_size, downloaded, upload_t, upload_d):
               try:
                   precent = int(downloaded * 100/total_size)
               except:
                   precent = 0
               global start_time
               if downloaded == 0:
                   start_time = time.time()
                   return
               duration = time.time() - start_time
               speed = str(int(downloaded / (1024 * duration)))
               e_time = ((total_size/1024) / int(speed))
               downloaded = nz(downloaded)
               self.data.emit(precent,speed,downloaded,file_name,nz(total_size),nt(e_time))

           #c.setopt(c.MAX_RECV_SPEED_LARGE, 50000)
           if path.exists(file_name):
               f = open(file_name, "ab")
               c.setopt(pycurl.RESUME_FROM, path.getsize(file_name))
           else:
               f = open(file_name, "wb")
           c.setopt(c.WRITEDATA, f)
           c.setopt(c.NOPROGRESS, 0)
           c.setopt(c.PROGRESSFUNCTION, curl_progress)
           c.perform()
           self.stat.emit(True)
       except Exception as e:
           print(e)

# >---------------------------------------------------------------------------------------------------------------------<

class ThreadClass_2(QObject):
    progress = pyqtSignal(float,float,float,float)
    stat2 = pyqtSignal(bool)

    def __init__(self,parent=None):
        super(ThreadClass_2, self).__init__(parent)

    def run(self,url,location,quality):
        try:
            video = pafy.new(url)
            st = video.streams
            def progress(total, recvd, ratio, rate, eta):
                self.progress.emit(total,recvd,rate,eta)
            download = st[quality].download(filepath=location, quiet=True, callback=progress)
            self.stat2.emit(True)
        except Exception as e:
            print(e)

# >---------------------------------------------------------------------------------------------------------------------<

class ThreadClass_3(QObject):
    Progress_data = pyqtSignal(float,float,float,float,int,str)
    stat3 = pyqtSignal(bool)

    def __init__(self,parent = None):
        super(ThreadClass_3, self).__init__(parent)

    def run(self,url,location):
        try:
            playlist = pafy.get_playlist(url)
            videos = playlist['items']
            chdir(location)
            if path.exists(str(playlist['title'])):
                chdir(str(playlist['title']))
            else:
                mkdir(str(playlist['title']))
                chdir(str(playlist['title']))

            for current, video in enumerate(videos, start=1):
                p = video['pafy']
                best = p.getbest(preftype='mp4')
                image = p.thumb
                def progress(total, recvd, ratio, rate, eta):
                    self.Progress_data.emit(total,recvd,rate,eta,current,image)
                best.download(quiet=True, callback=progress)
                self.stat3.emit(True)
        except Exception as e:
            print(e)

# >---------------------------------------------------------------------------------------------------------------------<

def main() :
     app = QApplication(argv)
     window = MainApp()
     window.show()
     app.exec_()

if __name__ == '__main__':
     main()
