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

Created on 1 juin 2012

@author: David Ducatel
'''

class Sql(object):
    '''
        class qui gere le langage SQL
    '''     
    
    def __init__(self):
        self.extensionList=['.sql']
    
    def countLineInFile(self,pathFile):
        '''
        Methode permettant de calculer le nombre de lignes de chaque type au sein d'un fichier
        @param pathFile: Chemin vers le fichier a analyser
        @return Un dictionnaire contenant le nombre de lignes de chaque type pour le fichier analyse
        '''
        blankLine=0
        commentLine=0
        lineCode=0
        with open(pathFile, "r") as fichier:
            while 1:
                    data=fichier.readline()
                    if not data:
                        break
                    
                    data=data.strip()
                    if data=="" :
                        blankLine+=1 
                    elif len(data)>=2:
                        if data[0:2]=="--":
                            commentLine+=1
                        else:
                            lineCode+=1
                    else:
                        lineCode+=1
  
        result = {}
        result["blankLine"] = blankLine
        result["commentLine"] = commentLine
        result["lineCode"] = lineCode
        return  result     
        
    def getExtension(self):
        '''
        Retourne les extensions de fichier associer au langage
        '''
        return self.extensionList