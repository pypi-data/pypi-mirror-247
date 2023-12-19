import hashlib
from binascii import hexlify, unhexlify
from ecdsa import ellipticcurve
from steemhd.base58_utils.schnorr import full_pubkey_gen, point_add, point_mul, G

class EcdsaParams:
    # ECDSA curve using secp256k1 is defined by: y**2 = x**3 + 7
    # This is done modulo p which (secp256k1) is:
    # p is the finite field prime number and is equal to:
    # 2^256 - 2^32 - 2^9 - 2^8 - 2^7 - 2^6 - 2^4 - 1
    # Note that we could also get that from ecdsa lib from the curve, e.g.:
    # SECP256k1.__dict__['curve'].__dict__['_CurveFp__p']
    _p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    # Curve's a and b are (y**2 = x**3 + a*x + b)
    _a = 0x0000000000000000000000000000000000000000000000000000000000000000
    _b = 0x0000000000000000000000000000000000000000000000000000000000000007
    # Curve's generator point is:
    _Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    _Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    # prime number of points in the group (the order)
    _order = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    # field
    _field = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

    # The ECDSA curve (secp256k1) is:
    # Note that we could get that from ecdsa lib, e.g.:
    # SECP256k1.__dict__['curve']
    _curve = ellipticcurve.CurveFp( _p, _a, _b )

    # The generator base point is:
    # Note that we could get that from ecdsa lib, e.g.:
    # SECP256k1.__dict__['generator']
    _G = ellipticcurve.Point( _curve, _Gx, _Gy, _order )

def tagged_hash(data: bytes, tag: str) -> bytes:
    '''
    Tagged hashes ensure that hashes used in one context can not be used in another.
    It is used extensively in Taproot

    A tagged hash is: SHA256( SHA256("TapTweak") ||
                              SHA256("TapTweak") ||
                              data
                            )
    Returns hashlib object (can then use .digest() or hexdigest())
    '''

    tag_digest = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256( tag_digest + tag_digest + data )

def hex_str_to_int(hex_str):
    '''
    Converts a string hexadecimal to a number
    '''
    return int(hex_str, base=16)

def tweak_taproot_pubkey(pubkey: bytes, tweak: str) -> str:
    '''
    Tweaks the public key with the specified tweak. Required to create the
    taproot public key from the internal key.
    '''
    # only the x coordinate is tagged_hash'ed
    # TODO if also script spending this should include the script!)
    th = tagged_hash(pubkey[:32], tweak)
    # we convert to int for later elliptic curve  arithmetics
    th_as_int = hex_str_to_int(th.hexdigest())

    # convert public key bytes to tuple Point
    x = hex_str_to_int(pubkey[:32].hex())
    y = hex_str_to_int(pubkey[32:].hex())
    P = (x, y)

    # if y is odd then negate y (effectively P) to make it even and equiv
    # to a 02 compressed pk
    if y % 2 != 0:
        y = EcdsaParams._field - y

    P = (x, y)

    # calculated tweaked public key Q = P + th*G
    Q = point_add(P, (point_mul(G, th_as_int)))

    return f'{Q[0]:064x}{Q[1]:064x}'
