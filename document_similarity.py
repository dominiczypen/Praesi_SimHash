# Author: Dominic van der Zypen
# Last modified: 2026-09-07
# Goal: demo for Hamming distance of two documents
# Use: python document_similarity.py <ascii_file_1.txt> <ascii_file_2.txt>
# ------------------------------
import sys;
# ------------------------------
def hamming_distance(a, b):
    return (a ^ b).bit_count();
# ------------------------------
def read_file(my_txt_file):
    with open(my_txt_file, "r", encoding="utf-8") as file:
        content = file.read().strip() #strip for \n and or \0 at end of file
    return content;
# ------------------------------
def simhash_fingerprint(text):
    i = 0;
    voting_vector = [0] * 32; # get vector [0, 0, ...,0] of length 32
    number_of_votes= len(text) - 2;
    while (i < number_of_votes):
        trigram = text[i:i+3]; # --> trigram -> +3..!
        h = simple_hash(trigram);
        # -> update voting vector: increment at positions of 1 of h!
        for j in range(32):
            if (h & 1): voting_vector[j] += 1;
            h = h >> 1;
        i += 1; # otherwise we get infinite loop
    return bitwise_majority(voting_vector, number_of_votes);
# ------------------------------
def bitwise_majority(voting_vector, number_of_votes):
    resultat = 0;
    for j in range(32):
        if (( voting_vector[j] << 1) >= number_of_votes):
            resultat = resultat ^ (1 << j); # switch bit number j to 1
    return resultat
# ====== HASH PART =============
def rotate(uint32):
    # right rotation
    return ((uint32 & 1) << 31) ^ (uint32 >> 1); # tested -> OK!
# ------------------------------
def scramble_32(uint32):
    # swap bits in even position with those in odd position
    mask01 = 0x55555555; # -> 01010101...
    return ((uint32 & mask01) << 1) ^ ((uint32 >> 1) & mask01);
                                                  # tested -> OK!
# ------------------------------
def simple_hash(my_string):
    h = 5154429 & 0xFFFFFFFF; #initialize hash value h
    for c in my_string.encode('utf-8'):
        # XOR c "all over" hash value h
        h = (h ^ (c << 8) ^ (c << 16) ^ (c << 24)) & 0xFFFFFFFF;
        # Daniel J. Bernsteins "times 33" trick:
        h = (((h << 5) + h) + c) & 0xFFFFFFFF; 
        h = rotate(h); # right rotate by 1 pos
        h = scramble_32(h); # swap bits in odd and even position
    return h
# ------------------------------
def print_32(my_number):
    # print uint32 grouped in 4 bits
    my_number = my_number & 0xFFFFFFFF;
    bin_raw = f"{my_number :032b}";
    grouped = " ".join(bin_raw[i:i+4] for i in range(0, 32, 4));
    print(f"{grouped} // 0x{my_number:08x}");
# ========= MAIN MAIN ==========
docA = sys.argv[1]; # string from command line!
docB = sys.argv[2]; # string from command line!
textA = read_file(docA);
textB = read_file(docB);
fingerprintA = simhash_fingerprint(textA);
fingerprintB = simhash_fingerprint(textB);
print(f"Fingerprint von File A:");
print_32(fingerprintA);
print(f"Fingerprint von File B:");
print_32(fingerprintB);
print(f"XOR der Fingerprints:");
print_32(fingerprintA ^ fingerprintB);
print(f"HAMMING-DISTANZ: {hamming_distance(fingerprintA, fingerprintB)}");
