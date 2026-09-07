# Author: Dominic van der Zypen
# Last modified: 2026-09-07
# Goal: provide a simple 32-bit hash function
# Use: python my_hash.py "<string>"
# ------------------------------
import sys;
# ------------------------------
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
    bin_raw = f"{(my_number & ((1 << 32) - 1)):032b}";
    grouped = " ".join(bin_raw[i:i+4] for i in range(0, 32, 4));
    print(f"{grouped} // 0x{my_number:08x}");
# --------- MAIN MAIN ----------
my_string = sys.argv[1]; # string from command line!
my_hash = simple_hash(my_string);
print_32(my_hash);
