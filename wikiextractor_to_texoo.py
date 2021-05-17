from abc import ABC, abstractmethod
from texoopy import Dataset, Document
from typing import Union
import glob
import json
import os
from tqdm import tqdm
import argparse


class AbtractKBConverter(ABC):

    @abstractmethod
    def get_kb(self) -> Dataset:
        """
        Returns the training dataset.
        :return: TeXoo dataset
        """
        pass

class WikipediaWikiExtractor(AbtractKBConverter):
    def __init__(self, path_to_wikiextractor_output: str, name: str = 'Wikipedia', text_limit: Union[None, int] = None):
        """
        Parses the output of WikiExtractor, e.g. python3 -m wikiextractor.WikiExtractor ... --json ... enwiki-20200201-pages-articles.xml
        :param path_to_wikiextractor_output: Path to the result WikiExtractor
        :param name: Name of the dataset
        :param text_limit: Cut description text after X characters to reduce memory consumption
        """
        self.path_to_wikiextractor_output: str = path_to_wikiextractor_output
        self.name: str = name
        self.text_limit = text_limit
        self.parse_wikiextractor_files()
    
    def parse_wikiextractor_files(self):
        self.kb = Dataset(language='en', name=self.name)
        pattern = os.path.join(self.path_to_wikiextractor_output, '**/*')
        filepaths = [filepath for filepath in glob.glob(pattern, recursive=True) if os.path.isfile(filepath)]
        
        for file in filepaths:            
            with open(file, 'r') as f:
                for line in f:
                    wikipedia_page = json.loads(line)
                    text = ' '.join(wikipedia_page['text'].split('\n\n')[1:])  # remove the title from the text
                    if self.text_limit is not None:
                        text = text[:self.text_limit]
                    doc = Document(id=wikipedia_page['id'], title=wikipedia_page['title'], text=text, length=len(text))
                    self.kb.documents.append(doc)

    def get_kb(self) -> Dataset:
        return self.kb

if __name__ == '__main__':
    parser = argparse.ArgumentParser();
    parser.add_argument('--max_length', nargs=1, type=int, action='store', help='Max article length')    
    args = parser.parse_args()
    
    text_limit = args.max_length[0]
    subfolders = [subfolder for subfolder in glob.glob('./extracted/*', recursive=False)]

    if not os.path.exists(f'./parsed/'):
        os.makedirs(f'./parsed/')

    for subfolder in tqdm(subfolders):
        kb = WikipediaWikiExtractor(subfolder, text_limit=text_limit).get_kb()           
        if not os.path.exists(f'./parsed/{subfolder[-2:]}'):
            os.makedirs(f'./parsed/{subfolder[-2:]}')
        with open(f'./parsed/{subfolder[-2:]}/wikipedia_{text_limit}chars.json', 'w') as f:
            f.write(kb.to_json())
