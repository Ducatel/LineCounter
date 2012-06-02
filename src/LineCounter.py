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

import glob
import os.path
from langProg import *
from PyQt4 import QtCore

class LineCounter(QtCore.QThread):
    '''
    Classe qui permet de compter le nombre de ligne de code,
    ligne de commentaire, ligne blanche au sein d'un dossier et
    de ces sous dossier
    '''

    def __init__(self, directoryPath, lang,ihm=None):
        '''
        Constructeur
        @param directoryPath: (String) Chemin vers le dossier racine de l'arborescence des fichiers a analyser
        @param lang: langage utilise
        @param ihm: (Ihm) objet de l'IHM
        '''
        super(LineCounter, self).__init__(ihm)
        self._directory = directoryPath
        self._nbLineCode = 0
        self._nbBlankLine = 0
        self._nbCommentLine = 0
        self.initLanguage(lang)

    def initLanguage(self, lang):
        '''
        Methode permettant de charger le parser pour le bon
        type de fichier
        '''
        if lang == "Java":
            self.objLang = Java.Java()
        elif lang == "C":
            self.objLang = C.C()
        elif lang == "C++":
            self.objLang = Cpp.Cpp()
        elif lang == "PHP":
            self.objLang = Php.Php()
        elif lang == "Javascript":
            self.objLang = Javascript.Javascript()
        elif lang == "CSS":
            self.objLang = Css.Css()
        elif lang == "(x)HTML":
            self.objLang = Html.Html()
        elif lang == "Python":
            self.objLang = Python.Python()
        elif lang == "SQL":
            self.objLang = Sql.Sql()
                   
    def run(self):
        '''
        Methode permettant de lancer l'analyse
        @emit fileInfo
        @emit maxProgress
        @emit endOfCompute
        '''
        fileList = self.getAllFilesFiltered(self._directory)
        if len(fileList) > 0:
            self.emit(QtCore.SIGNAL("maxProgress(PyQt_PyObject)"), len(fileList))
            
        for elt in fileList:
                result = self.objLang.countLineInFile(elt)
                self._nbLineCode = self._nbLineCode + result["lineCode"]
                self._nbBlankLine = self._nbBlankLine + result["blankLine"]
                self._nbCommentLine = self._nbCommentLine + result["commentLine"]
                self.emit(QtCore.SIGNAL("fileInfo(PyQt_PyObject)"), [elt,result["lineCode"], result["blankLine"], result["commentLine"]])
        self.emit(QtCore.SIGNAL("endOfCompute(PyQt_PyObject)"), [self._nbLineCode, self._nbCommentLine, self._nbBlankLine,self.objLang.getExtension()])
        

            
    def getAllFilesFiltered(self, path):
        '''
        Methode recursive permettant de recuperer tous les fichiers a analyser
        @param path: chemin vers le dossier a analyser
        @return La liste des fichiers a analyser
        '''
        fichier = [] 
        l = glob.glob(path + os.sep + '*') 
        for i in l: 
            if os.path.isdir(i): 
                fichier.extend(self.getAllFilesFiltered(i)) 
            else:
                extension = os.path.splitext(i)[1]
                if extension in  self.objLang.getExtension():
                        fichier.append(i) 
        return fichier
