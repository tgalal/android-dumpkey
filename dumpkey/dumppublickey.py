# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import os
import M2Crypto as m2
import sys
unistr = str if sys.version_info >= (3, 0) else unicode
def gcd(a, b):
    # Return the GCD of a and b using Euclid's Algorithm
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    # Cryptomath Module
    # http://inventwithpython.com/hacking (BSD Licensed)

    # Returns the modular inverse of a % m, which is
    # the number x such that a*x % m = 1

    if gcd(a, m) != 1:
        return None # no mod inverse if a & m aren't relatively prime

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def check(pubkey):
    """
    :param pubkey:  EVP_PKEY
    """
    rsa = pubkey.get_rsa()
    pubexp = rsa.e
    modulus = int(pubkey.get_modulus(), 16)
    expect = "\x00\x00\x00\x01\x03"
    if pubexp != expect:
        raise Exception("Public exponent should be %s but is %s " % (expect, pubexp ))

    if modulus.bit_length() != 2048:
        raise Exception("Modulus should be 2048 bits long but is %s bits" % modulus.bit_length())


def print_rsa(pubkey):
    """
    :param pubkey: EVP_PKEY | str
    """

    if type(pubkey) is unistr:
        if not os.path.exists(pubkey):
            raise Exception("%s does not exist" % pubkey)
        tcs = m2.X509.load_cert(pubkey)
        pubkey = tcs.get_pubkey()

    check(pubkey)

    N = int(pubkey.get_modulus(), 16)
    result = ""

    nwords = N.bit_length() / 32 # of 32 bit integers in modulus

    result += "{"
    result += str(nwords)

    B = 2 ** 32
    N0inv = int(B - findModInverse(N, B))

    result += ","
    result += hex(N0inv)

    R = 2 ** N.bit_length()
    RR = (R * R) % N  #2^4096 mod N

    result += ",{"

    # Write out modulus as little endian array of integers.
    for i in range(0, nwords):
        n = N % B
        result += str(n)

        if i != nwords - 1:
            result += ","

        N = N / B

    result += "}"

    # Write R^2 as little endian array of integers.
    result += ",{"

    for i in range(0, nwords):
        rr = RR % B
        result += str(rr)

        if i != nwords -1:
            result += ","

        RR = RR / B

    result += "}"

    result += "}"
    return result
