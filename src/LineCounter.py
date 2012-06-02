#!/usr/bin/python
# -*-coding:utf-8 -*-
'''
Created on 16 mai 2012

@author: Davis Ducatel
'''

import glob
import os.path
from langProg import *

class LineCounter(object):
    '''
    Classe qui permet de compter le nombre de ligne de code,
    ligne de commentaire, ligne blanche au sein d'un dossier et
    de ces sous dossier
    '''

    def __init__(self,directoryPath,printAllFile,ihm,lang):
        '''
        Constructeur
        @param directoryPath: (String) Chemin vers le dossier racine de l'arborescence des fichiers a analyser
        @param printAllFile: (Boolean) Si True, affiche le detail pour chaque fichier
        @param lang: langage utilise
        @param ihm: (Ihm) objet de l'IHM
        '''
        self._directory=directoryPath
        self._nbLineCode=0
        self._nbBlankLine=0
        self._nbCommentLine=0
        self._nbFile=0
        self._printAllFile=printAllFile
        self.ihm=ihm
        self.initLanguage(lang)
        print(self.objLang)
        

    def initLanguage(self,lang):
        if lang == "Java":
            self.objLang=Java.Java()
        elif lang =="C":
            self.objLang=C.C()
        elif lang =="C++":
            self.objLang=Cpp.Cpp()
        elif lang =="PHP":
            self.objLang=Php.Php()
        elif lang =="Javascript":
            self.objLang=Javascript.Javascript()
        elif lang =="CSS":
            self.objLang=Css.Css()
        elif lang =="(x)HTML":
            self.objLang=Html.Html()
        elif lang =="Python":
            self.objLang=Python.Python()
        elif lang =="SQL":
            self.objLang=Sql.Sql()
       
    def compute(self):
        '''
        Methode permettant de lancer l'analyse
        (Affiche le/les resultat)
        '''
        self.ihm.affichage.setText("-".center(50,"-"))
        self.ihm.affichage.append("COMPUTE".center(50,"-"))
        self.ihm.affichage.append("-".center(50,"-"))
        fileList=self.getAllFilesFiltered(self._directory)
        if len(fileList) >0:
            self.ihm.progressBar.setMaximum(len(fileList))
        counter=1
        for elt in fileList:
                self._nbFile= self._nbFile+1
                #result=self.countLineInFile(elt)
                result=self.objLang.countLineInFile(elt)
                self._nbLineCode=self._nbLineCode+result["lineCode"]
                self._nbBlankLine=self._nbBlankLine+result["blankLine"]
                self._nbCommentLine=self._nbCommentLine+result["commentLine"]
                self.ihm.progressBar.setValue(counter)
                counter+=1
                if self._printAllFile:
                    self.ihm.affichage.append("File: {0} \nLine code: {1} \nComment line: {2} \nBlank line: {3}\n\n"
                          .format(elt,result["lineCode"], result["commentLine"], result["blankLine"]))

        if self._printAllFile:
            self.ihm.affichage.append("-".center(50,"-"))
            self.ihm.affichage.append("TOTAL".center(50,"-"))
            self.ihm.affichage.append("-".center(50,"-"))

        self.ihm.affichage.append("Line code: {0} \nComment line: {1} \nBlank line: {2}\nFile: {3} \nTotal line: {4}\n"
              .format(self._nbLineCode,self._nbCommentLine,self._nbBlankLine,self._nbFile,(self._nbLineCode+self._nbCommentLine+self._nbBlankLine)))
        strAff="File Filter: [ "

        for elt in  self.objLang.getExtension():
            strAff+=elt+' '
        strAff+="]\n"

        self.ihm.affichage.append(strAff)

            
    def getAllFilesFiltered(self,path):
        '''
        Methode recursive permettant de recuperer tous les fichiers a analyser
        @param path: chemin vers le dossier a analyser
        @return La liste des fichiers a analyser
        '''
        fichier=[] 
        l = glob.glob(path+os.sep+'*') 
        for i in l: 
            if os.path.isdir(i): 
                fichier.extend(self.getAllFilesFiltered(i)) 
            else:
                extension=os.path.splitext(i)[1]
                if extension in  self.objLang.getExtension():
                        fichier.append(i) 
        return fichier