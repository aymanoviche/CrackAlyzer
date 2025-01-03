import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional, List
from hashidentifer import HashAnalyzer

class OnlineCracker:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 10

    def crack_gromweb(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                result = soup.find('em', class_='long-content string')
                if result:
                    return result.text.strip()
        except Exception as e:
            print(f"Erreur Gromweb: {str(e)}")
        return None

    def crack_md5online(self, hash_string: str) -> Optional[str]:
        try:
            url = "https://www.md5online.org/md5-decrypt.html"
            data = {'hash': hash_string}
            response = requests.post(url, headers=self.headers, data=data, timeout=self.timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                result = soup.find('b')
                if result:
                    return result.text.strip()
        except Exception as e:
            print(f"Erreur MD5Online: {str(e)}")
        return None

    def crack_md5hashing(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                result = soup.find('div', class_='text-center')
                if result:
                    text = result.get_text()
                    match = re.search(r'Plain Text: (.+)', text)
                    if match:
                        return match.group(1).strip()
        except Exception as e:
            print(f"Erreur MD5Hashing: {str(e)}")
        return None

    def crack_hash(self, hash_string: str, hash_types: List[str]) -> Dict[str, Optional[str]]:
        results = {}
        
        for hash_type in hash_types:
            if hash_type.upper() == 'MD5':
                # Try all services
                services = [
                    (self.crack_gromweb, f"https://md5.gromweb.com/?md5={hash_string}"),
                    (self.crack_md5online, hash_string),
                    (self.crack_md5hashing, f"https://md5hashing.net/hash/{hash_string}")
                ]
                
                for service_func, args in services:
                    result = service_func(args)
                    if result:
                        results[hash_type] = result
                        return results
                
                results[hash_type] = None
            else:
                results[hash_type] = None
        
        return results

    def convert_md5_file(self, input_file: str) -> None:
        """Convertit un fichier de hachages MD5 au format requis"""
        converted_lines = []
        
        with open(input_file, 'r', encoding='latin-1') as infile:
            content = infile.read()
            
        if ':' in content and ' ' in content:
            return
            
        with open(input_file, 'r', encoding='latin-1') as infile:
            for line in infile:
                parts = line.strip().split()
                if len(parts) == 2:
                    name, hash_value = parts
                    converted_lines.append(f"{hash_value}:{name}")
        
        final_output = ' '.join(converted_lines)
        
        with open(input_file, 'w', encoding='utf-8') as outfile:
            outfile.write(final_output)
