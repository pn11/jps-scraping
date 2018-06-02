#coding: utf-8
 
import unittest
import re
import numpy as np

class Author():
    def __init__(self):
        self.name = ''
        self.affiliation_tag = []
        self.affiliation_name = []
        self.is_presenter = ''
    def __str__(self):
        afftag = ','.join(self.affiliation_tag)
        affname = ','.join(self.affiliation_name)
        return self.name + ' (' + affname + '(' + afftag + '))'
    def add_affiliation(self, affi_dict):
        if 'ollaboration' in self.name:
            self.affiliation_name = ['']
            return
        if 'コラボ' in self.name:
            self.affiliation_name = ['']
            return
        for tag in self.affiliation_tag:
            if tag in affi_dict:
                self.affiliation_name.append(affi_dict[tag])
            else:
                self.affiliation_name.append('')
    def to_dict(self):
        _dict = {}
        _dict['name'] = self.name
        _dict['affiliation'] = self.affiliation_name
        _dict['is_presenter'] = self.is_presenter
        return _dict

def is_circle(_str):
    '''
    丸の種類がどれでも良いようにする。
    '''
    #print('○', ord('○'))
    #print('◯', ord('◯'))
    if _str == '○' or _str == '◯':
        return True
    return False

def create_list(author_str):
    comma_pos = [itr.start() for itr in re.finditer(pattern=',', string=author_str)]
    sup_start_pos, _, sup_end_pos, _ = find_sup(author_str)
    #著者のリスト化
    author_list = []
    cpos_pre = 0
    for cpos in comma_pos:
        is_separator = True
        if sup_start_pos is None:
            pass
        else:
            for sstart, send in zip(sup_start_pos, sup_end_pos):
                #<sup>と</sup>は必ず一対一対応。
                # (ネストは考慮しない)
                if cpos >= sstart and cpos < send:
                    is_separator = False
        if is_separator:
            author_list.append(author_str[cpos_pre:cpos].strip())
            cpos_pre = cpos+1
    author_list.append(author_str[cpos_pre:].strip())
    return author_list

def find_sup(_str):
    '''
    <sup>と</sup>の位置を返す。
    '''
    sup_start_pos = [[itr.start(), itr.end()] for itr in re.finditer(pattern='<sup>', string=_str)]
    sup_end_pos = [[itr.start(), itr.end()] for itr in re.finditer(pattern='</sup>', string=_str)]
    if len(sup_start_pos) == 0:
        return None, None, None, None
    arr1 = np.array(sup_start_pos)
    arr2 = np.array(sup_end_pos)
    
    return list(arr1[:,0]), list(arr1[:,1]), list(arr2[:,0]), list(arr2[:,1])

def parse_author(author_str_list):
    author_list = []
    for author_str in author_str_list:
        author = Author()
        sstarts1, sstarts2, sends1, sends2 = find_sup(author_str)
        if sstarts1 is None:
            author.name = author_str.strip()
            author.affiliation_tag = ['']
        else:
            name = ''
            sen2_pre = 0
            for ss1, ss2, sen1, sen2 in zip(sstarts1, sstarts2, sends1, sends2):
                content = author_str[ss2:sen1].split(',')
                name += author_str[sen2_pre:ss1]
                sen2_pre = sen2
                for cont in content:
                    cont =cont.strip()
                    if is_circle(cont):
                        author.is_presenter = True
                    else:
                        author.affiliation_tag.append(cont)
                author.name = name.strip()
        author_list.append(author)  
    return author_list

def create_affi_dict(affi_str_list):
    affi_dict = {}
    for affi_str in affi_str_list:
        sstarts1, sstarts2, sends1, sends2 = find_sup(affi_str)
        if sstarts1 is None:
            affi_dict[''] = affi_str
        else:
            affi_name = ''
            sen2_pre = 0
            for ss1, ss2, sen1, sen2 in zip(sstarts1, sstarts2, sends1, sends2):
                content = affi_str[ss2:sen1].split(',')
                affi_name += affi_str[sen2_pre:ss1]
                sen2_pre = sen2
                for cont in content:
                    cont = cont.strip()
                    if is_circle(cont): continue
                    affi_dict[cont] = affi_name.strip()
    return affi_dict
