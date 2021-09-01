import ijson
from texoopy import Document, NamedEntityAnnotation
from tqdm import tqdm

kb_path = './wikipedia-kb-1chars.json'
doc_path = './wikipedia-doc-1chars.json'

num_kb = 0
num_docs = 0
max_length_kb = 0
max_length_docs = 0
prefix = 'https://en.wikipedia.org/wiki/'

doc_ids, doc_ids_with_prefix, annotation_ids = set(), set(), set()

with open(kb_path, 'r') as f:
    documents = ijson.items(f, 'documents.item')
    for doc in tqdm(documents):
        doc = Document.from_json(doc)
        doc_ids.add(doc.id)
        doc_ids_with_prefix.add(f'{prefix}{doc.id}')
        num_kb += 1
#         # max_length_kb = len(doc.text) if len(doc.text) > max_length_kb else max_length_kb

with open(doc_path, 'r') as f:
    documents = ijson.items(f, 'documents.item')
    for doc in tqdm(documents):
        doc: Document = Document.from_json(doc)
        num_docs += 1
        ann: NamedEntityAnnotation
        for ann in doc.annotations:
            annotation_ids.add(ann.refId)
        # max_length_docs = len(doc.text) if len(doc.text) > max_length_docs else max_length_docs


print(f'num_kb: {num_kb}, num_docs: {num_docs}, max_length_kb: {max_length_kb}, max_length_docs: {max_length_docs}')
print(f'#doc_ids: {len(doc_ids)}, #doc_ids_with_prefix: {len(doc_ids_with_prefix)}, #annotation_ids: {len(annotation_ids)}')
print(f'doc_ids INTERSECT annotation_ids: {len(doc_ids.intersection(annotation_ids))}, doc_ids_with_prefix INTERSECT annotation_ids: {len(doc_ids_with_prefix.intersection(annotation_ids))}')