
import dateparser
import datetime
import pandas as pd
import pytz
import os

parsers = {"ac24_title_date.tsv": "%a %b %d %H:%M:%S %Z %Y",
"aeronet_title_date.tsv": "%Y-%m-%dT%H:%M:%S%z",
"aktualne_title_date.tsv": "%d. %m. %Y %H:%M",
"blesk_title_date.tsv": "%d. %m. %Y %H:%M",
"idnes_title_date.tsv": "%Y-%m-%dT%H:%M%Z",
"lidovky": dateparser.parse,
"parlamentnilisty_title_date.tsv": "%d.%m.%Y %H:%M",
"protiproud_title_date.tsv": "%d. %m. %Y",
"sputnik_title_date.tsv": "%Y-%m-%dT%H:%M",
"stredoevropan_title_date.tsv": "%Y-%m-%dT%H:%M:%S%z"}

input_files = ["ac24_title_date.tsv",
               "aeronet_title_date.tsv",
               "aktualne_title_date.tsv",
               "blesk_title_date.tsv",
               "idnes_title_date.tsv",
               "parlamentnilisty_title_date.tsv",
               "protiproud_title_date.tsv",
               "sputnik_title_date.tsv",
               "stredoevropan_title_date.tsv"
               ] 

def localize(dt):
    '''Convert naive time to local time'''
    if dt.tzinfo is not None:
       return dt
    return pytz.utc.localize(dt)

def safe_parse(date, parser):
    try:
        return datetime.datetime.strptime(date, parser)
    except ValueError:
        return datetime.datetime(2019, 2, 4)

def read_file(file_name, parser):
    dataframe = pd.read_csv(os.path.join("data", file_name), sep="\t", names=["title", "date"])
    dataframe = dataframe.assign(title=dataframe.title.str.lstrip("#"),
                                 source=file_name.split("_")[0],
                                 parsed_date=dataframe.date.apply(lambda x: localize(safe_parse(x, parser))))
    return dataframe
    
def get_compound_data():
    frames = [read_file(file, parsers[file]) for file in input_files]
    return pd.concat(frames)

def get_stopwords():
    words = set(map(str.strip, open(os.path.join('data', 'stopwords-cs.txt')).readlines()))
    return words
