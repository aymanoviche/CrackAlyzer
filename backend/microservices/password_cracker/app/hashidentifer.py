import re
import hashlib
import base64
import codecs
from typing import List, Dict

import re
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

    HASH_SERVICES = {
        'md5': ['https://md5.gromweb.com/?md5={hash}'],
        'sha1': ['https://sha1.gromweb.com/?hash={hash}','https://md5hashing.net/hash/sha1/{hash}'],
        'sha224': ['https://md5hashing.net/hash/sha224/{hash}'],
        'sha256': ['https://md5hashing.net/hash/sha256/{hash}'],
        'sha384': ['https://md5hashing.net/hash/sha384/{hash}'],
        'sha512': ['https://md5hashing.net/hash/sha512/{hash}'],
        'ripemd320': ['https://md5hashing.net/hash/ripemd320/{hash}']
    }

    @staticmethod
    def identify_hash_type(hash_string: str) -> List[str]:
        possible_types = []
        for hash_type, pattern in HashAnalyzer.HASH_PATTERNS.items():
            if re.match(pattern, hash_string):
                possible_types.append(hash_type)
        return possible_types

    @staticmethod
    def is_possible_rot13(text: str) -> bool:
        """Check if the string could be ROT13 encoded"""
        return bool(re.match(r'^[a-zA-Z0-9]+$', text))

    @staticmethod
    def is_possible_base64(text: str) -> bool:
        """Check if the string could be Base64 encoded"""
        try:
            # Try to decode as base64
            decoded = base64.b64decode(text)
            # Check if decoded result contains printable ASCII
            return all(32 <= byte <= 126 for byte in decoded)
        except:
            return False

    @staticmethod
    def additional_analysis(hash_string: str) -> Dict[str, float]:
        """
        Perform additional analysis to determine hash probability
        Returns confidence scores for each detected type
        """
        scores = {}
        
        # Length-based scoring
        if len(hash_string) == 32:
            scores['MD5'] = 0.9
        if len(hash_string) == 40:
            scores['SHA1'] = 0.9
        if len(hash_string) == 64:
            scores['SHA256'] = 0.9
        if len(hash_string) == 128:
            scores['SHA512'] = 0.9
            
        # Character distribution analysis
        hex_char_ratio = len(re.findall(r'[a-fA-F0-9]', hash_string)) / len(hash_string)
        if hex_char_ratio > 0.9:
            for hash_type in ['MD5', 'SHA1', 'SHA256', 'SHA512']:
                if hash_type in scores:
                    scores[hash_type] += 0.1
                    
        # ROT13 analysis
        if HashAnalyzer.is_possible_rot13(hash_string):
            scores['ROT13'] = 0.7
            
        # Base64 analysis
        if HashAnalyzer.is_possible_base64(hash_string):
            scores['Base64'] = 0.8
            
        return scores