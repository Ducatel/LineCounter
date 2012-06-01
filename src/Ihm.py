#!/usr/bin/python
# -*-coding:utf-8 -*-
#!/usr/bin/python
# -*-coding:utf-8 -*-
'''
Created on 16 mai 2012

@author: Davis Ducatel
'''

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import LineCounter

class Ihm(QtGui.QWidget):
    def __init__(self):
        super(Ihm, self).__init__()
        self.extensionFilterList=[['.h','.cpp'],['.h','.c'],['.h','.cpp','.c'],['.java'],['.php']]
        self.dirPath=QtCore.QDir('')
        self.initUI()

    
    def initUI(self):
        layoutPrinc = QtGui.QGridLayout()

        layoutPrinc.addWidget(QtGui.QLabel('Dossier racine du projet: '),0,0,1,2)
        self.pathLabel=QtGui.QLabel('Aucun dossier choisi...')
        layoutPrinc.addWidget(self.pathLabel,0,2,1,2)

        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setTextVisible(True)
        layoutPrinc.addWidget(self.progressBar,1,0,1,4)

        self.affichage= QtGui.QTextEdit(self)
        self.affichage.setReadOnly(True)
        layoutPrinc.addWidget(self.affichage,2,0,5,4)

        self.printAllFile = QtGui.QCheckBox('Afficher le detail pour chaque fichier', self)
        layoutPrinc.addWidget(self.printAllFile,7,0,1,4)

        layoutPrinc.addWidget(QtGui.QLabel('Filtre de fichier: '),8,0)
        self.fileFilter=QtGui.QComboBox(self)
        for filterType in self.extensionFilterList:
            textFileFilter=''
            for extension in filterType:
                textFileFilter+=extension+' '
            self.fileFilter.addItem(textFileFilter)
        layoutPrinc.addWidget(self.fileFilter,8,1,1,3)

        self.chooseFileButton = QtGui.QPushButton('Dossier', self)
        self.chooseFileButton.clicked.connect(self.chooseFileAction)
        layoutPrinc.addWidget(self.chooseFileButton,9,0,1,2)
        
        self.goButton = QtGui.QPushButton('Count', self)
        self.goButton.setDisabled(True)
        self.goButton.clicked.connect(self.goButtonAction)
        layoutPrinc.addWidget(self.goButton,9,2,1,2)   

        self.setLayout(layoutPrinc)
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowIcon(QtGui.QIcon('../ressources/icon.png'))
        self.setWindowTitle('Line Counter')    
        self.show()
        
    def chooseFileAction(self):
        fileName = QtGui.QFileDialog.getExistingDirectory(self, "Choisir un fichier")
        if fileName:
            self.goButton.setDisabled(False)
            self.pathLabel.setText(fileName)
            self.dirPath.setPath(fileName)
            self.progressBar.setValue(0)
            self.affichage.clear()

    def goButtonAction(self):
        printAllFile=False
        if self.printAllFile.checkState() == QtCore.Qt.Checked:
            printAllFile=True
            
        
        line=LineCounter.LineCounter(str(self.dirPath.path().toUtf8())
                                     ,printAllFile,self
                                     ,self.extensionFilterList[self.fileFilter.currentIndex()])
        line.compute()
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ihm = Ihm()
    sys.exit(app.exec_())
