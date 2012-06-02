#!/usr/bin/python
# -*-coding:utf-8 -*-
'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses

Created on 16 mai 2012

@author: Davis Ducatel

'''
#TODO Lancer le traitement dans un trhead
#TODO Ajouter le compteur de ligne pour python
#TODO Ajouter un fenetre avec les info du dev
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import LineCounter


class Ihm(QtGui.QWidget):
    '''
    Class permettant de gerer l'interface utilisateur
    '''
    def __init__(self):
        super(Ihm, self).__init__()
        self.extensionFilterList = {"C++":['.h', '.cpp'], "C":['.h', '.c']
                                  , "Java":['.java'], "PHP":['.php']
                                  , "CSS":['.css'], "(x)HTML":['.html']
                                  , "Python":['.py'], "SQL":['.sql']
                                  , "Javascript":['.js']}
        self.extensionFilterList
        self.dirPath = QtCore.QDir('')
        self.buildUI()
        self.initUI()
        self.show()
    
    def buildUI(self):
        '''
        Methode qui va construire l'interface utilisateur
        '''
        layoutPrinc = QtGui.QGridLayout()

        layoutPrinc.addWidget(QtGui.QLabel('Dossier racine du projet: '), 0, 0, 1, 2)
        self.pathLabel = QtGui.QLabel('Aucun dossier choisi...')
        layoutPrinc.addWidget(self.pathLabel, 0, 2, 1, 2)

        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setTextVisible(True)
        layoutPrinc.addWidget(self.progressBar, 1, 0, 1, 4)

        self.affichage = QtGui.QTextEdit(self)
        self.affichage.setReadOnly(True)
        layoutPrinc.addWidget(self.affichage, 2, 0, 5, 4)

        self.printAllFile = QtGui.QCheckBox('Afficher le detail pour chaque fichier', self)
        layoutPrinc.addWidget(self.printAllFile, 7, 0, 1, 4)

        layoutPrinc.addWidget(QtGui.QLabel('Langage cible: '), 8, 0)
        self.fileFilter = QtGui.QComboBox(self)
            
        layoutPrinc.addWidget(self.fileFilter, 8, 1, 1, 3)

        self.chooseFileButton = QtGui.QPushButton('Dossier', self)
        self.chooseFileButton.clicked.connect(self.chooseFileAction)
        layoutPrinc.addWidget(self.chooseFileButton, 9, 0, 1, 2)
        
        self.goButton = QtGui.QPushButton('Compter', self)
        self.goButton.setDisabled(True)
        self.goButton.clicked.connect(self.goButtonAction)
        layoutPrinc.addWidget(self.goButton, 9, 2, 1, 2)   

        self.setLayout(layoutPrinc)
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowIcon(QtGui.QIcon('../ressources/icon.png'))
        self.setWindowTitle('Line Counter')    
        
        
    def initUI(self):
        '''
        Methode qui va initialiser l'interface utilisateur
        '''
        
        for key, filterType in self.extensionFilterList.items():
            textFileFilter = 'Langage ' + key + ' ['
            for extension in filterType:
                textFileFilter += extension + ', '
            textFileFilter = textFileFilter[:len(textFileFilter) - 2]
            textFileFilter += ']'
            self.fileFilter.addItem(textFileFilter)
        
        
    def chooseFileAction(self):
        '''
        Methode de gestion du choix du dossier a analyser
        '''
        fileName = QtGui.QFileDialog.getExistingDirectory(self, "Choisir un fichier")
        if fileName:
            self.goButton.setDisabled(False)
            self.pathLabel.setText(fileName)
            self.dirPath.setPath(fileName)
            self.progressBar.setValue(0)
            self.affichage.clear()

    def goButtonAction(self):
        '''
        Methode de gestion du clique sur le bouton compter
        '''
        printAllFile = False
        if self.printAllFile.checkState() == QtCore.Qt.Checked:
            printAllFile = True
        langTab = str(self.fileFilter.currentText().toUtf8()).split('[')[0].split(' ')
        lineCounter = LineCounter.LineCounter(str(self.dirPath.path().toUtf8())
                                     , printAllFile, self
                                     , langTab[1].strip())
        lineCounter.compute()
    
if __name__ == '__main__':
    test = "<!-- dfg"
    print(test[0])
    app = QtGui.QApplication(sys.argv)
    ihm = Ihm()
    sys.exit(app.exec_())
    

