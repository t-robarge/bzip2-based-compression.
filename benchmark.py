import bwt_huffman
from gzip import compress, decompress
import lzma
import time
import os
from matplotlib import pyplot as plt

def time_complexity():
    data = {}
    # Gzip
    with open('textfile.txt', 'rb') as f: txt = f.read()
    start = time.time()
    encode = compress(txt)
    decode = decompress(encode)
    end = time.time()
    data['GZip'] = float(format((end - start) * 1000, '.2f'))
    # Bzip2
    with open('textfile.txt', 'rb') as f: txt = f.read()
    start = time.time()
    encode,decoder_ring = bwt_huffman.compress(txt, False)
    decode = bwt_huffman.decompress(encode, decoder_ring, False)
    end = time.time()
    data['ATZip'] = float(format((end - start) * 1000, '.2f'))
    # LZMAzip
    with open('textfile.txt', 'rb') as f: txt = f.read()
    start = time.time()
    encode = lzma.compress(txt)
    decode = lzma.decompress(encode)
    end = time.time()
    data['LZMA'] = float(format((end - start) * 1000, '.2f'))
    # Plot
    plt.bar(data.keys(),data.values(), color = 'blue',width =.5)
    for i in data:
        plt.text(i, data[i], data[i], ha = 'center')
    plt.xlabel("Zip Algorithm")
    plt.ylabel("Runtime (ms)")
    plt.title(" Runtimes of Zip Algorithms (Compression + Decompression)")
    plt.show()
def compression_ratio():
    data = {}
    strtfile_size = os.path.getsize('textfile.txt')
    #strtfile_size = os.path.getsize('test1.bmp')
    with open('textfile.txt', 'rb') as f: txt = f.read()
   # with open('test1.bmp','rb') as f: txt = f.read()
    # ATZip
    encode = bwt_huffman.compress(txt,True)
    with open('encoded1.txt', 'wb') as f: f.write(encode[0])
    endfile_size = os.path.getsize('encoded1.txt')
    ratio = strtfile_size/endfile_size
    data['ATZip'] = float(format(ratio, '.2f'))
    # Gzip
    encode = compress(txt)
    with open('encoded2.txt','wb') as f: f.write(encode)
    endfile_size = os.path.getsize('encoded2.txt')
    ratio = strtfile_size/endfile_size
    data['Gzip'] = float(format(ratio, '.2f'))
    # LZMA
    encode = lzma.compress(txt)
    with open('encoded3.txt','wb') as f: f.write(encode)
    endfile_size = os.path.getsize('encoded3.txt')
    ratio = strtfile_size/endfile_size
    data['LZMAZip'] = float(format(ratio, '.2f'))
    plt.bar(data.keys(),data.values(), color = 'green',width =.5)
    for i in data:
        plt.text(i, data[i], data[i], ha = 'center')
    plt.xlabel("Zip Algorithm")
    plt.ylabel("Compression Ratio")
    plt.title("Compression Ratios of Zip Algorithms")
    plt.show()




if __name__ == '__main__':
    time_complexity()
    compression_ratio()


