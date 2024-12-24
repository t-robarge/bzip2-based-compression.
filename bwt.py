import os
import sys
import marshal
import itertools
import argparse
from operator import itemgetter
from functools import partial
from collections import Counter
import array
termchar = 17
def ibwt(msg):
 ## Overhead
# - record unique index of each value in BWT
# - sort this indexed list by byte
# - create a dict to map each sorted element to its corresponding element in BWT
  bwt_indexed = [(byte, idx) for idx, byte in enumerate(msg)]
  sorted_bwt_indexed = sorted(bwt_indexed, key=lambda x: x[0])
  mapping = {sorted_bwt_indexed[i]: bwt_indexed[i] for i in range(len(sorted_bwt_indexed))}
  # we start with term character
  og_string = bytearray([17])
  # lets find it in our sorted array
  for i in range(len(sorted_bwt_indexed)):
      if sorted_bwt_indexed[i][0] == 17:
          target_idx = i
          break

  # BACKTRACK 
  # iterate over len of the BWT - 1 to get all characters
  # we know first element in sorted is $
  cur_char = sorted_bwt_indexed[target_idx]
  for i in range(len(msg) - 1):
    # we grab the index of cur_char in the sorted list
    # the element at that index in bwt is the preceding character
    og_string.append(mapping[cur_char][0])
    #og_string.append(msg[sorted_bwt_indexed.index(cur_char)])
    # we now look at the char we just added, but we need its index to correctly locate it in the sorted array, how do we get it?
    # we already have it!!! - sorted_bwt_indexed.index(cur_char)
    # combine these in a tuple and this becomes the new char and its corresponding index
    cur_char = mapping[cur_char]
    #cur_char = (msg[sorted_bwt_indexed.index(cur_char)], sorted_bwt_indexed.index(cur_char))
   
  # the string should be in its original state after termination
  return (og_string[1:])[::-1]

# Burrows-Wheeler Transform fncs
def radix_sort(values, key, step=0):
    sortedvals = []
    radix_stack = []
    radix_stack.append((values, key, step))

    while len(radix_stack) > 0:
        values, key, step = radix_stack.pop()
        if len(values) < 2:
            for value in values:
                sortedvals.append(value)
            continue

        bins = {}
        for value in values:
            bins.setdefault(key(value, step), []).append(value)

        for k in sorted(bins.keys()):
            radix_stack.append((bins[k], key, step + 1))
    return sortedvals
            
# memory efficient BWT
def bwt(msg):
    def bw_key(text, value, step):
        return text[(value + step) % len(text)]
    msg = msg + termchar.to_bytes(1, byteorder='big')

    bwtM = bytearray()

    rs = radix_sort(range(len(msg)), partial(bw_key, msg))
    for i in rs:
        bwtM.append(msg[i - 1])

    return bwtM[::-1]
def mtf(msg):
    # Initialise the list of characters (i.e. the dictionary)
    dictionary = bytearray(range(256))
    
    # Transformation
    compressed_text = bytearray()
    rank = 0

    # read in each character
    for c in msg:
        rank = dictionary.index(c) # find the rank of the character in the dictionary
        compressed_text.append(rank) # update the encoded text
        
        # update the dictionary
        dictionary.pop(rank)
        dictionary.insert(0, c)

    #dictionary.sort() # sort dictionary
    return compressed_text # Return the encoded text as well as the dictionary

# inverse move-to-front
def imtf(compressed_msg):
    compressed_text = compressed_msg
    dictionary = bytearray(range(256))

    decompressed_img = bytearray()

    # read in each character of the encoded text
    for i in compressed_text:
        # read the rank of the character from dictionary
        decompressed_img.append(dictionary[i])
        
        # update dictionary
        e = dictionary.pop(i)
        dictionary.insert(0, e)
        
    return decompressed_img # Return original string


if __name__ == '__main__':
    with open("textfile.txt", 'rb') as f:
        msgb = f.read()
    with open("output.txt", 'r') as f:
        msg = f.read()

  
    #string = input("Enter text here:\n")

    ### stop
    encoded = bwt(msgb)
    encoded = mtf(encoded)

    decoded = imtf(encoded)
    decoded = ibwt(decoded)

    with open('output.txt', 'wb') as file: file.write(decoded)