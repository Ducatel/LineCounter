#!/usr/bin/python
# -*-coding:utf-8 -*-
'''
Created on 16 mai 2012

@author: Davis Ducatel
'''

import glob
import os.path

class LineCounter(object):
    '''
    Classe qui permet de compter le nombre de ligne de code,
    ligne de commentaire, ligne blanche au sein d'un dossier et
    de ces sous dossier (seulement pour le code C/C++, JAVA,PHP)
    '''

    def __init__(self,directoryPath,printAllFile,ihm,extensionList=[".h",".cpp"]):
        '''
        Constructeur
        @param directoryPath: (String) Chemin vers le dossier racine de l'arborescence des fichiers a analyser
        @param printAllFile: (Boolean) Si True, affiche le d�tail pour chaque fichier
        @param extensionList: (List) Liste des extensions de fichier a traiter
        @param ihm: (Ihm) objet de l'IHM
        '''
        
        self._directory=directoryPath
        self._nbLineCode=0
        self._nbBlankLine=0
        self._nbCommentLine=0
        self._nbFile=0
        self._printAllFile=printAllFile
        self._extensionList=extensionList
        self.ihm=ihm
       
    def compute(self):
        '''
        Methode permettant de lancer l'analyse
        (Affiche le/les resultat)
        '''
        self.ihm.affichage.setText("-".center(50,"-"))
        self.ihm.affichage.append("COMPUTE".center(50,"-"))
        self.ihm.affichage.append("-".center(50,"-"))
        fileList=self.getAllCppFile(self._directory)
        if len(fileList) >0:
            self.ihm.progressBar.setMaximum(len(fileList))
        counter=1
        for elt in fileList:
                self._nbFile= self._nbFile+1
                result=self.countLineInFile(elt)
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

        for elt in  self._extensionList:
            strAff+=elt+' '
        strAff+="]\n"

        self.ihm.affichage.append(strAff)

            
    def getAllCppFile(self,path):
        '''
        Methode recursive permettant de recuperer tous les fichiers a analyser
        @param path: chemin vers le dossier a analyser
        @return La liste des fichiers a analyser
        '''
        fichier=[] 
        l = glob.glob(path+os.sep+'*') 
        for i in l: 
            if os.path.isdir(i): 
                fichier.extend(self.getAllCppFile(i)) 
            else:
                extension=os.path.splitext(i)[1]
                if extension in  self._extensionList:
                        fichier.append(i) 
        return fichier
    

    def countLineInFile(self,pathFile):
        '''
        Methode permettant de calculer le nombre de lignes de chaque type au sein d'un fichier
        @param pathFile: Chemin vers le fichier a analyser
        @return Un dictionnaire contenant le nombre de lignes de chaque type pour le fichier analys�
        '''
        blankLine=0
        commentLine=0
        lineCode=0
        with open(pathFile, "r") as fichier:
                inCommentGroup=False
                while 1:
                        data=fichier.readline()
                        if not data:
                                break
                        
                        data=data.strip()
                        if data=="" :
                            blankLine=blankLine+1
                        elif inCommentGroup==True:
                                if len(data)>1:
                                        if data[0]=="*" and data[1]=="/":
                                                inCommentGroup=False
                                commentLine=commentLine+1
                        else:
                                if len(data)>1:
                                        if data[0]=="/" and data[1]=="/":
                                                commentLine=commentLine+1
                                        elif data[0]=="/" and data[1]=="*":
                                                commentLine=commentLine+1
                                                inCommentGroup=True
                                                if data[len(data)-1]=="/" and data[len(data)-2]=="*":
                                                    inCommentGroup=False
                                                
                                        else:
                                            lineCode=lineCode+1
                                else:
                                    lineCode=lineCode+1  
        result = {}
        result["blankLine"] = blankLine
        result["commentLine"] = commentLine
        result["lineCode"] = lineCode
        return  result     


