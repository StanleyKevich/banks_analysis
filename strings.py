import time
from tqdm import tqdm

# bar = IncrementalBar('ProgresssS', max=len(range(10)))
for i in tqdm(range(10)):
    print(i)
    # print('Progress: ', end='')
    # time.sleep(.1)
    # print(f'{i*10}%', end='\r')
    time.sleep(.4)
    # bar.next()
# bar.finish()

