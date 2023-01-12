from alive_progress import alive_bar
import time

total = 15
with alive_bar(total) as bar:
    for etapa in range(total):
        # print(etapa)
        bar()
        time.sleep(1)
