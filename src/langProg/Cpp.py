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

class Cpp(object):
    '''
        class qui gere le langage C++
    '''     
    
    def __init__(self):
        self.extensionList=['.cpp','.h']
    
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
                                                if data[len(data)-2:]=="*/":
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
        
    def getExtension(self):
        '''
        Retourne les extensions de fichier associer au langage
        '''
        return self.extensionList