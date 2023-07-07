import os
import xml.etree.ElementTree as ET
import subprocess
from astropy.table import Table, Column
import numpy as np
import copy
import shutil
import bibtexparser


def detex(str):
    str = str.replace('}','')
    str = str.replace('{','')
    str = str.replace('$','')
    str = str.replace('\'','')
    return(str)

assoc_dict = {'Article Title': 'title', 
              'DOI': 'doi',
              'Year': 'year',
              'Volume': 'volume',
              'Page Range': 'pages',
              'Issue': 'number',
              'URL': 'adsurl',              
}

journal_map = {'\\apj': 'The Astrophysical Journal',
               '\\apjl': 'The Astrophysical Journal Letters',
               '\\apjs': 'The Astrophysical Journal Supplement Series',
               '\\aj': 'The Astronomical Journal',
               '\\mnras': 'Monthly Notices of the Royal Astronomical Society',
               '\\aap': 'Astronomy and Astrophysics',
               '\\araa': 'Annual Review of Astronomy and Astrophysics',
               '\\aapr': 'The Astronomy and Astrophysics Review',
               '\\apss': 'Astrophysics and Space Science',
               '\\nat': 'Nature',
               '\\aplett': 'Astrophysics Letters',
               '\\pasp': 'Publications of the Astronomical Society of the Pacific',
               '\\icarus': 'Icarus',
               '\\aaps': 'Astronomy and Astrophysics Supplement Series',
               '\\ap&ss': 'Astrophysics and Space Science',
               '\\ssr': 'Space Science Reviews',
               '\\jgr': 'Journal of Geophysical Research',
               '\\planss': 'Planetary and Space Science',
               '\\jrasc': 'Journal of the Royal Astronomical Society of Canada'}

tree = ET.parse('CCV-10026565.xml')

with open('export-bibtex.bib') as bibtex_file:
    bibtex_database = bibtexparser.load(bibtex_file)

nsdict = {'sec': "generic-cv/"}

root = tree.getroot()

pubs = root.findall('section')[-1].findall('section')[-1]
for entry in bibtex_database.entries:
    if entry['ENTRYTYPE'] == 'article':
        template = copy.deepcopy(pubs.findall('section')[0])
        try:
            template.attrib.pop('recordId')
        except KeyError:
            pass
        fields = template.findall('field')
        for field in fields:
            print(field.attrib['label'])
            for k in assoc_dict.keys():
                if field.attrib['label'] == k:
                    print('---> ', field.find('value').text)
                    try:
                        field.find('value').text = detex(entry[assoc_dict[k]])
                    except KeyError:
                        pass
                    print('---> ', field.find('value').text)
                if field.attrib['label'] == 'Authors':
                    authorstr = detex(entry['author'])
                    Nauthor = len(authorstr.split(' and '))
                    if len(authorstr) > 990:
                        authorstr = authorstr.split(' and ')[0] + '{0}'.format(Nauthor)+ ' others including E. Rosolowsky'
                    else:
                        authorstr = authorstr.replace(' and ', '; ')
                    field.find('value').text = authorstr
                    print('---> ', field.find('value').text)
                # if field.attrib['label'] == 'Publication Status':
                #     field.find('value').text = 'Published'
                if field.attrib['label'] == 'Refereed?':
                    if entry['journal'] == '\\jrasc':
                        field.find('lov').text = 'No'
                    else:
                        field.find('lov').text = 'Yes'
                if field.attrib['label'] == 'Open Access?':
                    field.find('lov').text = 'Yes'
                if field.attrib['label'] == 'Journal':
                    if '\\' in entry['journal']:
                        field.find('value').text = journal_map[entry['journal']]
                    else:
                        field.find('value').text = entry['journal']
                    print('---> ', field.find('value').text)
    pubs.insert(0, template)
tree.write('new-ccv.xml')