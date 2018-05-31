#coding: utf-8
 
import requests
from bs4 import BeautifulSoup
import json

def create_author_list(author_div):
    authors_str = [str(a) for a in author_div.contents]
    #authors_list = ''.join(authors_str).split(',') # 所属が複数の場合に失敗するので保留
    authors_list = ''.join(authors_str)
    return authors_list

def extract_sessions(url, sessions):
    request = requests.get(url)
    html = request.content
    soup = BeautifulSoup(html, "html.parser")

    current_session = None
    div_main = soup.find(id='main')
    for cont in div_main.contents: # セッションごとに構造化されていないため上から順に読み出す。
        if cont.name == 'div':
            class_name = cont.get('class')[0]
            if class_name == 'container1': # 時間と場所の取得
                h4 = cont.find('h4')
                time_place_id = h4.find('a').get('id')
                time_place_str = h4.text
                sessions[time_place_id] = {'session place': time_place_str}
                current_session = sessions[time_place_id]
                current_session['talks'] = []
            if class_name == 'container': # 各講演情報の取得
                try:
                    number = cont.find(class_='number').text
                    title = cont.find(class_='title').text
                    authors = create_author_list(cont.find(class_='au'))
                    affiliations = create_author_list(cont.find(class_='aff'))
                    talk = {'number': number, 'title': title,
                    'authors': authors, 'affiliations': affiliations}
                    current_session['talks'].append(talk)
                    if authors is None:
                        print(talk)
                    if affiliations is None:
                        print(talk)
                except AttributeError:
                    talk = {'number': number, 'title': '取消',
                    'authors': '', 'affiliations': ''}
                    current_session['talks'].append(talk)
            if class_name == 'break':
                title = cont.text
                talk = {'number': '', 'title': title,
                    'authors': '', 'affiliations': ''}
                current_session['talks'].append(talk)
        if cont.name=='h5':
            current_session['session name'] = cont.text

fields = {
    'sr': '素粒子論領域',
    'sj': '素粒子実験領域',
    'rk': '理論核物理領域',
    'jk': '実験核物理領域',
    'u' : '宇宙線・宇宙物理領域',
    'si': 'ビーム物理領域',
    '01': '領域1： 原子分子、量子エレクトロニクス、放射線',
    '02': '領域2： プラズマ',
    '03': '領域3： 磁性', 
    '04': '領域4： 半導体、メゾスコピック系、量子輸送',
    '05': '領域5： 光物性',
    '06': '領域6： 金属（液体金属、準結晶）、低温（超低温、超伝導、密度波）',
    '07': '領域7： 分子性固体',
    '08': '領域8： 強相関電子系',
    '09': '領域9： 表面・界面、結晶成長',
    '10': '領域10： 構造物性（誘電体、格子欠陥、Ｘ線・粒子線、フォノン）',
    '11': '領域11： 物性基礎論、統計力学、流体物理、応用数学、社会経済物理',
    '12': '領域12： ソフトマター物理、化学物理、生物物理',
    '13': '領域13： 物理教育、物理学史、環境物理'
}

for field_id, field_name in fields.items():
    url = 'http://w4.gakkai-web.net/jps_search/2018sp/data/html/program' + field_id + '.html'
    print('Processing ' + field_name + '...')
    sessions = {}
    extract_sessions(url, sessions)
    print(sessions)
    json_file = open('json/'+field_id+'.json', 'w')
    json.dump(sessions, json_file, ensure_ascii=False, indent=2)
    json_file.close()

