from model import Data_Extractor, Data_Cleaning
from multiprocessing import Manager, Process
import time 

if __name__ == '__main__':
    initial = time.time()
    data_extraction = Data_Extractor('https://www.polkastarter.com/projects')

    data_extraction.main()

    data_cleaner = Data_Cleaning(data_extraction)

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

    end = time.time()
    print(f"The duration of the proccess was: {end - initial} sec")
