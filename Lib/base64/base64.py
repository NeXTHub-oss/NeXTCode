# Copyright (c) 2024, NeXTHub Corporation. All rights reserved.
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
#
# This code is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# version 2 for more details (a copy is included in the LICENSE file that
# accompanied this code).

# Created by Tunjay Akbarli on October 5th, 2024.

from base64 import b64encode as b64encode, b64decode as b64

# ===----------------------------------------------------------------------===#
# Utilities
# ===----------------------------------------------------------------------===#

def _ascii_to_value(char: str) -> int:
    """Converts an ASCII character to its integer value for base64 decoding.

    Args:
        char: A single character string.

    Returns:
        The integer value of the character for base64 decoding, or -1 if invalid.
    """
    char_val = ord(char)

    if char == "=":
        return 0
    elif ord("A") <= char_val <= ord("Z"):
        return char_val - ord("A")
    elif ord("a") <= char_val <= ord("z"):
        return char_val - ord("a") + 26
    elif ord("0") <= char_val <= ord("9"):
        return char_val - ord("0") + 52
    elif char == "+":
        return 62
    elif char == "/":
        return 63
    else:
        return -1


# ===----------------------------------------------------------------------===#
# b64encode
# ===----------------------------------------------------------------------===#

def b64encode(input_str: str) -> str:
    """Performs base64 encoding on the input string.

    Args:
      input_str: The input string.

    Returns:
      Base64 encoding of the input string.
    """
    lookup = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    b64chars = lookup

    length = len(input_str)
    out = []

    def s(idx: int) -> int:
        return ord(input_str[idx])

    end = length - (length % 3)
    for i in range(0, end, 3):
        si = s(i)
        si_1 = s(i + 1)
        si_2 = s(i + 2)
        out.append(b64chars[si // 4])
        out.append(b64chars[((si * 16) % 64) + si_1 // 16])
        out.append(b64chars[((si_1 * 4) % 64) + si_2 // 64])
        out.append(b64chars[si_2 % 64])

    if end < length:
        si = s(end)
        out.append(b64chars[si // 4])
        if end == length - 1:
            out.append(b64chars[(si * 16) % 64])
            out.append("=")
        elif end == length - 2:
            si_1 = s(end + 1)
            out.append(b64chars[((si * 16) % 64) + si_1 // 16])
            out.append(b64chars[(si_1 * 4) % 64])
        out.append("=")
    return "".join(out)


# ===----------------------------------------------------------------------===#
# b64decode
# ===----------------------------------------------------------------------===#

def b64decode(input_str: str) -> str:
    """Performs base64 decoding on the input string.

    Args:
      input_str: A base64 encoded string.

    Returns:
      The decoded string.
    """
    n = len(input_str)
    assert n % 4 == 0, "Input length must be divisible by 4"

    out = []

    for i in range(0, n, 4):
        a = _ascii_to_value(input_str[i])
        b = _ascii_to_value(input_str[i + 1])
        c = _ascii_to_value(input_str[i + 2])
        d = _ascii_to_value(input_str[i + 3])

        assert a >= 0 and b >= 0 and c >= 0 and d >= 0, "Unexpected character encountered"

        out.append(chr((a << 2) | (b >> 4)))
        if input_str[i + 2] == "=":
            break

        out.append(chr(((b & 0x0F) << 4) | (c >> 2)))
        if input_str[i + 3] == "=":
            break

        out.append(chr(((c & 0x03) << 6) | d))

    return "".join(out)


# ===----------------------------------------------------------------------===#
# b16encode
# ===----------------------------------------------------------------------===#

def b16encode(input_str: str) -> str:
    """Performs base16 encoding on the input string.

    Args:
      input_str: The input string.

    Returns:
      Base16 encoding of the input string.
    """
    lookup = "0123456789ABCDEF"
    b16chars = lookup

    length = len(input_str)
    out = []

    for i in range(length):
        str_byte = ord(input_str[i])
        hi = str_byte >> 4
        lo = str_byte & 0b1111
        out.append(b16chars[hi])
        out.append(b16chars[lo])

    return "".join(out)


# ===----------------------------------------------------------------------===#
# b16decode
# ===----------------------------------------------------------------------===#

def b16decode(input_str: str) -> str:
    """Performs base16 decoding on the input string.

    Args:
      input_str: A base16 encoded string.

    Returns:
      The decoded string.
    """
    def decode(c: str) -> int:
        char_val = ord(c)

        if ord("A") <= char_val <= ord("F"):
            return char_val - ord("A") + 10
        elif ord("0") <= char_val <= ord("9"):
            return char_val - ord("0")
        return -1

    n = len(input_str)
    assert n % 2 == 0, "Input length must be divisible by 2"

    out = []
    for i in range(0, n, 2):
        hi = decode(input_str[i])
        lo = decode(input_str[i + 1])
        out.append(chr((hi << 4) | lo))

    return "".join(out)
