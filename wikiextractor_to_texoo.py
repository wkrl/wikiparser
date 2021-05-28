from abc import ABC, abstractmethod
from texoopy import Dataset, Document, NamedEntityAnnotation
from typing import Union
import glob
import json
import os
from tqdm import tqdm
import argparse
from bs4 import BeautifulSoup
import urllib


class AbtractKBConverter(ABC):

    @abstractmethod
    def get_kb(self) -> Dataset:
        """
        Returns the training dataset.
        :return: TeXoo dataset
        """
        pass

class WikipediaWikiExtractor(AbtractKBConverter):
    def __init__(self, path_to_wikiextractor_output: str, name: str = 'Wikipedia', annotate: bool = False, text_limit: Union[None, int] = None):
        """
        Parses the output of WikiExtractor, e.g. python3 -m wikiextractor.WikiExtractor ... --json ... enwiki-20200201-pages-articles.xml
        :param path_to_wikiextractor_output: Path to the result WikiExtractor
        :param name: Name of the dataset
        :param annotate: If references should be parsed as annotations
        :param text_limit: Cut description text after X characters to reduce memory consumption
        """
        self.path_to_wikiextractor_output: str = path_to_wikiextractor_output
        self.name: str = name
        self.annotate = annotate
        self.text_limit = text_limit
        self.parse_wikiextractor_files()

    def extract_annotations(self, soup):
        annotations = []
        text = soup.get_text()
        for a in soup.findAll('a'):
            annotation = NamedEntityAnnotation(
                begin=text.index(a.text), # assuming that the first occurence of the word is the reference
                length=len(a.text),
                text=a.text,
                source='GOLD',
                confidence=1.0,
                refId=f'https://{self.kb.language}.wikipedia.org/wiki/{a["href"]}',
                candidates=[]
            )
            annotations.append(annotation)
        return annotations

    def generate_document(self, wikipedia_page):
        text = ' '.join(wikipedia_page['text'].split('\n\n')[1:]) # remove the title from the text
        soup = BeautifulSoup(text, 'lxml')
        text = soup.get_text()

        if self.text_limit is not None:
            text = text[:self.text_limit]

        annotations = self.extract_annotations(soup) if self.annotate == True else []
        doc = Document(
            id=urllib.parse.quote(wikipedia_page['title']),
            title=wikipedia_page['title'],
            text=text,
            length=len(text),
            annotations=annotations
        )
        return doc

    def parse_wikiextractor_files(self):
        self.kb = Dataset(language='en', name=self.name)
        pattern = os.path.join(self.path_to_wikiextractor_output, '**/*')
        filepaths = [filepath for filepath in glob.glob(pattern, recursive=True) if os.path.isfile(filepath)]

        for file in filepaths:
            with open(file, 'r') as f:
                for line in f:
                    wikipedia_page = json.loads(line)
                    doc = self.generate_document(wikipedia_page)
                    self.kb.documents.append(doc)

    def get_kb(self) -> Dataset:
        return self.kb

if __name__ == '__main__':
    parser = argparse.ArgumentParser();
    parser.add_argument('--max_length', nargs=1, type=int, action='store', default=[None], help='Max article length')
    parser.add_argument('--annotate', action='store_true', default=False, help='Annotate article references')
    args = parser.parse_args()
    text_limit, annotate = args.max_length[0], args.annotate

    subfolders = [subfolder for subfolder in glob.glob('./extracted/*', recursive=False)]

    if not os.path.exists(f'./parsed/'):
        os.makedirs(f'./parsed/')

    for subfolder in tqdm(subfolders):
        kb = WikipediaWikiExtractor(subfolder, annotate=annotate, text_limit=text_limit).get_kb()
        if not os.path.exists(f'./parsed/{subfolder[-2:]}'):
            os.makedirs(f'./parsed/{subfolder[-2:]}')
        with open(f'./parsed/{subfolder[-2:]}/wikipedia_{text_limit}chars.json', 'w') as f:
            f.write(kb.to_json())
