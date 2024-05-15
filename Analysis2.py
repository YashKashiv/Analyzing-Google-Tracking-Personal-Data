import numpy as np
import sqlite3
from tqdm import tqdm
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import style
from datetime import datetime

style.use("ggplot")

conn = sqlite3.connect("mylife.db")
c = conn.cursor()

day = 86400 #seconds
year = 365*day

slide = 1*day
window = 1*year

def words_graph():
    save_dir = "word_images"

    c.execute("SELECT max(unix) FROM words")
    max_time = c.fetchall()[0][0]

    c.execute("SELECT min(unix) FROM words")
    min_time = c.fetchall()[0][0]
    print(min_time, max_time)

    start = min_time
    end = min_time + window
    counter = 0

    while end < max_time:
        print(counter)
        c.execute(f"SELECT word FROM words WHERE unix > {start} and unix < {end}")
        data = c.fetchall()

        words = [i[0] for i in data]
        word_counter = Counter(words)
        common_words = [topic[0] for topic in word_counter.most_common(15)]
        y_pos = np.arange(len(common_words))
        word_counts = [topic[1] for topic in word_counter.most_common(15)]
        
        plt.figure(figsize=(12, 7))
        plt.bar(y_pos, word_counts, align="center", alpha=0.5)
        plt.xticks(y_pos, common_words)
        plt.ylabel("Volume")
        plt.title(f"{datetime.fromtimestamp(end).day}-{datetime.fromtimestamp(end).month}-{datetime.fromtimestamp(end).year}")
        plt.savefig(f"{save_dir}/{counter}.png")
        
        counter += 1
        start += slide
        end += slide


words_graph()