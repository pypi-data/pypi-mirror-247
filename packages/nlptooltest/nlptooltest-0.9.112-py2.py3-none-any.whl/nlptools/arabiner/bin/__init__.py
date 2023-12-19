from nlptools.DataDownload import downloader
import os
from nlptools.arabiner.utils.helpers import load_checkpoint

tagger = None
tag_vocab = None
train_config = None

filename = 'Wj27012000.tar'
path =downloader.get_appdatadir()
model_path = os.path.join(path, filename)
print('1',model_path)
tagger, tag_vocab, train_config = load_checkpoint(model_path)