import re
import base64
from typing import List

class HashAnalyzer:
    HASH_PATTERNS = {
        'md5': r'^[a-fA-F0-9]{32}$',
        'sha1': r'^[a-fA-F0-9]{40}$',
        'sha224': r'^[a-fA-F0-9]{56}$',
        'sha256': r'^[a-fA-F0-9]{64}$',
        'sha384': r'^[a-fA-F0-9]{96}$',
        'sha512': r'^[a-fA-F0-9]{128}$',
        'ripemd320': r'^[a-fA-F0-9]{80}$'
    }

    @staticmethod
    def identify_hash_type(hash_string: str) -> List[str]:
        possible_types = []
        for hash_type, pattern in HashAnalyzer.HASH_PATTERNS.items():
            if re.match(pattern, hash_string):
                possible_types.append(hash_type)
        return possible_types

    @staticmethod
    def is_possible_base64(s: str) -> bool:
        try:
            if base64.b64encode(base64.b64decode(s)).decode('utf-8') == s:
                return True
        except Exception:
            return False
        return False
    