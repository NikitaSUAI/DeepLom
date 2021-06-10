import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pyannote.database.util import load_rttm
import pandas as pd
import numpy as np
import multiprocessing

def draw(*args):
    p = multiprocessing.Process(target=_draw, args=args)
    p.start()
    p.join()
    print("Realy end")
    return 3, 5

def _draw(annotation, path):
    print("process Start")
    res = dict()
    map = dict()
    count = 1
    for i in annotation:
        tmp = i.split()
        try:
            res[map[tmp[7]]].append((float(tmp[3]),
                                float(tmp[3]) + float(tmp[4])))
        except BaseException:
            map[tmp[7]] = count
            count += 1
            res[map[tmp[7]]] = [(float(tmp[3]),
                            float(tmp[3]) + float(tmp[4])), ]
    arr = {i:[] for i in res}
    for i, j in res.items():
        for k in j:
            arr[i].append([s for s in range(int(k[0]*4), int(k[1]*4))])

    colors = "bgrcmykw"
    fig, ax = plt.subplots()
    for i, j in arr.items():
        arr[i] = np.concatenate(j)
        ax.scatter(arr[i]/(4 * 60), [i for k in arr[i]], c=colors[i%len(
        colors)], marker="_")
    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_xlabel("Время (М)")
    ax.set_ylabel("Говорящие")
    plt.savefig(path)
    print("process End")
    return res, count-1

if __name__ == "__main__":
    import sys
    import os
    print(sys.argv[1])
    # if len(sys.argv) == 4:
    #     lst = ["TS3007a.Mix-Headset", "yv", "TS3003a.Mix-Headset", "EN2002b.Mix-Headset", "IS1009a.Mix-Headset", "IS1009c.Mix-Headset", "ES2004a.Mix-Headset"]
    #     tmp = load_rttm("/home/nikittossii/Documents/DeeepLom/rttm/MixHeadset.test.rttm")
    #     for i in lst:
    #         with open(f"real/rttm/{i}.rttm", "w") as f:
    #             tmp[i].write_rttm(f)


    # elif len(sys.argv) == 3:
    #     tmp = load_rttm(sys.argv[1])
    #     for key, val in tmp.items():
    #         out = os.path.dirname(sys.argv[1])
    #         with open(f"{out}/{key}.rttm", "w") as f:
    #             val.write_rttm(f)
    # else:
    if True:
        name = ".".join(os.path.basename(sys.argv[1]).split(".")[:-1])
        print(name)
        out = f"images/{sys.argv[2]}/{name}.png"
        with open(sys.argv[1]) as f:
            _draw(f, out)
