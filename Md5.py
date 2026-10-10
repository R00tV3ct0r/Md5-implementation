# sources : 
# https://www.youtube.com/watch?v=5MiMK45gkTY
# https://en.wikipedia.org/wiki/MD5

# table 
K = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
]

# index 
s = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]

def rotate(x, n):
    x &= 0xFFFFFFFF
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF     


def md5(message):
    # Init
    A = 0x67452301   
    B = 0xefcdab89   
    C = 0x98badcfe   
    D = 0x10325476  

    data = message.encode("utf-8")
    size = len(data) * 8 

    # we add 1
    data += b"\x80"

    #we add some 0 until 512 - 64 bits (if the text is longueur than 512 bit we go to 1024 - 64 on we continue like that)
    data += b"\x00" * ((56 - len(data) % 64) % 64)
    data += size.to_bytes(8, "little")

    # now that the padding is done we process every 512 bit bloc
    for offset in range(0, len(message), 64):
        block = data[offset:offset + 64] # 64 = 512 bit
        # we create 16 group of 32 bit
        M = [int.from_bytes(block[i:i+4], "little") for i in range(0, 64, 4)]

        # keep a copy of the original value to add it at the end
        A0, B0, C0, D0 = A, B, C, D

        for i in range(64):
            # we calul the 4 round of MD5
            # we calcul : rotate(F(B, C, D, i) + A + input + K[i]), s[i]) + B
            if i < 16:
                F = (B & C) | ((~B) & D)
                j = i
            elif i >= 16 and i < 32:
                j = (5 * i + 1) % 16
                F = (D & B) | ((~D) & C)
            elif i >= 32 and i < 48:
                j = (3 * i + 5) % 16
                F = B ^ C ^ D
            else:
                j = (7 * i) % 16
                F = C ^ (B | (~D))

            A_prime = D
            B_prime = (rotate((F + A + M[j] + K[i]), s[i]) + B) & 0xFFFFFFFF
            C_prime = B
            D_prime = C

            # we update 
            A, B, C, D = A_prime, B_prime, C_prime, D_prime

        # We add the original values
        A = (A + A0) & 0xFFFFFFFF
        B = (B + B0) & 0xFFFFFFFF
        C = (C + C0) & 0xFFFFFFFF
        D = (D + D0) & 0xFFFFFFFF

    # MD5 outputs is in little-endian !!!
    return A.to_bytes(4, "little").hex() + B.to_bytes(4, "little").hex() + C.to_bytes(4, "little").hex() + D.to_bytes(4, "little").hex()


if __name__ == "__main__":
    message = "Hello World!"
    print(message)
    hash = md5(message)
    print(hash)