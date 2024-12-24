from collections import Counter
import heapq
def encode(msg):
    # Count the frequency of each byte inyh the message
    freq_table = Counter(msg)

    # Build the Huffman tree
    heap = [[weight, [byte, ""]] for byte, weight in freq_table.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    # Generate the Huffman codes
    huff_codes = dict(heapq.heappop(heap)[1:])

    # Create the decoder ring
    decoder_ring = {byte: code for byte, code in huff_codes.items()}

    # Encode the message using the Huffman codes
    encoded_msg = ''.join([huff_codes[byte] for byte in msg])

    return encoded_msg, decoder_ring

def decode(cmsg, decoderRing):
    byteMsg = bytearray()
    current_code = ""

    # Swap the keys and values of the decoder ring
    decoder_ring_swapped = {code: char for char, code in decoderRing.items()}

    for char in cmsg:
        current_code += char
        if current_code in decoder_ring_swapped:
            byte = decoder_ring_swapped[current_code]
            byteMsg.append(ord(byte))
            current_code = ""

    return byteMsg

if __name__ == "__main__":
    msg = b"Benchmark your implementation on several inputs and compare your implementation with several other compression software (e.g. zip, rar, bzip, gzip). The compression ratio is the ratio between the uncompressed size and compressed size of a file. What are the compression ratios for each file? How does enabling or disabling the move-to-front and BWT affect the compression ratio, compression time, and decompression time"
    encoded_msg, decoder_ring = encode(msg)
    print("Encoded message:", encoded_msg)
    print("Decoder ring:", decoder_ring)
    decoded_msg = decode(encoded_msg, decoder_ring)
    print("Decoded message:", decoded_msg)

