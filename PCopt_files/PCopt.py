import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import *
import os
import glob
import stat
import shutil
import subprocess
#os.startfile('chrome.exe')

UI_names = ["PCopt_UI", "More_UI", "progress_UI"];
UI = [];

defarr = ["windowscalculator",
                "windowsalarms",
                "windowscalculator",
                "3dbuilder",
                "windowscommunicationsapps",
                "windowscamera",
                "officehub",
                "skypeapp",
                "getstarted",
                "zunemusic",
                "windowsmaps",
                "solitairecollection",
                "bingfinance",
                "zunevideo",
                "bingnews",
                "onenote",
                "people",
                "windowsphone",
                "photos",
                "bingsports",
                "soundrecorder",
                "bingweather",
                "xboxapp",
                "WindowsFeedbackHub",
                "gethelp",
                "Microsoft.MixedReality.Portal",
                "Microsoft.MSPaint",
                "Microsoft.MicrosoftStickyNotes",
                "MicrosoftStickyNotes",
                "XboxGameOverlay",
                "XboxIdentityProvider",
                "XboxSpeechToTextOverlay",
                "YourPhone",
                "Microsoft.Office.OneNote",
                "3dviewer",
                "Microsoft.Xbox",
                "Microsoft.XboxGamingOverlay",
                "Microsoft.GamingApp",
                "Microsoft.GamingServices",
                "Microsoft EdgeWebView",
                "Microsoft.EdgeWebView"]

def debugger(title, message):
    QMessageBox.information(None, title, message);

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

def clean():
    files = glob.glob('C:/Users/c4m3lion/AppData/Local/Temp/*')
    os.system("taskkill /f /im explorer.exe");#kill exploreer exe it save memory
    for f in files:
        try:
            os.remove(f) #try to remove file
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))
            print('PermissionError do change')
            os.chmod(f, stat.S_IWRITE) # Ihave no idea
            try:
                shutil.rmtree(f) #try to remove folder
            except OSError as e:
                print("Error: %s : %s" % (f, e.strerror))
    
    os.system('start explorer.exe');
    debugger("Clean Pc", "Your pc is clean now!!!")


#delete edge
def deleteEdge():
    url = "C:/Program Files (x86)/Microsoft/Edge/Application/";
    files = glob.glob(url+'*');
    for f in files:
        if(f[len(f)-1] >='0' and f[len(f)-1] <='9'):
            f+="\Installer";
            #debugger("edge found on this directory: ");
            #debugger(f);
            if len(os.listdir(f) ) == 0:
                debugger("Warning","bu edge is uninstalled already!");
            else:    
                #debugger("Uninstalling!!!")
                
                os.chdir(f);
                os.system('start cmd /k setup --uninstall --force-uninstall --system-level')
    debugger("Done", "Edge Uninstalled");

#RIP
class delAppsThread(QThread):
    update_progress = pyqtSignal(int);

    def run(self):
        n = 1;
        for i in defarr:
            temp_ = "Get-AppxPackage *" + i + "* | Remove-AppxPackage";
            p = run(temp_);
            if p.returncode != 0:
                print(i, " - An error occured: %s", p.stderr);
            self.update_progress.emit(n);
            n+=1;

def evt_progFinished():
    debugger("Done!", "Apps Uninstalled");
    switchUI(0);

def evt_progress(value):
    UI[2].progressBar.setValue(value);

def deleteDefaultApps():

    prog = delAppsThread();
    prog.start();
    prog.finished.connect(evt_progFinished);
    prog.update_progress.connect(evt_progress)
    
    switchUI(2);
    UI[2].progressBar.setMaximum(len(defarr));

def switchUI(id):
    for i in UI:
        i.hide();

    UI[id].show();
    
def startUI():
    for i in UI_names:
        UI_temp = uic.loadUi("Resources/UI/"+i+".ui");
        UI.append(UI_temp);

app = QtWidgets.QApplication([]);

startUI();

UI[0].cleanBtn.clicked.connect(clean);
UI[0].moreBtn.clicked.connect(lambda: switchUI(1));

UI[1].unEdgeBtn.clicked.connect(deleteEdge);
UI[1].unDefaultBtn.clicked.connect(deleteDefaultApps);
UI[1].backBtn.clicked.connect(lambda: switchUI(0));

switchUI(0);
app.exec();