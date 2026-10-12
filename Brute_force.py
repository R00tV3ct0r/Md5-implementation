from Md5 import md5

def brute_collision(bits=32):
    # we convert bytes in hexa 
    hexa = bits // 4
    known_md5 = {}
    i = 0
    while True:
        # we keep the first bits of the md5 value
        first_bits_md5 = md5(str(i))[:hexa]
        # we check if it is know
        if first_bits_md5 in known_md5:
            # we found a collision
            return known_md5[first_bits_md5], i, first_bits_md5
        # we update and continue
        known_md5[first_bits_md5] = i
        i += 1

# due to the birthday problem we can calculate a collision with in 2^(n/2)
first_value, second_value, first_bits_md5 = brute_collision(32)
print(first_value, second_value, first_bits_md5)   