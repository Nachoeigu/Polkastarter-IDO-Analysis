from model import Data_Extractor
from multiprocessing import Manager, Process

data_extraction = Data_Extractor('https://www.polkastarter.com/projects')

data_extraction.main()

data_cleaner = Data_Cleaning()

manager = Manager()
lista = manager.list()
processes = []
for index in range(len(getattr(data_cleaner, 'list_of_responses'))):
    proc = Process(target = data_cleaner.parsing_data, args = [index, lista])
    processes.append(proc)

for p in processes:
    p.start()
for p in processes:
    p.join()

data_cleaner.generating_dataframe(lista)

data_cleaner.returning_table()
