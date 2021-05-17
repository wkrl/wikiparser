import wget
import glob

def download_data():
    if len(glob.glob('./*.xml.*')) == 0:
        url = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream.xml.bz2'
        wget.download(url)

if __name__ == '__main__':
    download_data()
