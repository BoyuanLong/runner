import os

def fmt_key(key: str) -> str:
    '''Maintain correct formatting for keys in key-value pairs'''
    key = str(key).strip()
    if '-' not in key:
        key = f'--{key}' if len(key) > 1 else f'-{key}'
    return key


def fmt_value(value: str) -> str:
    '''Maintain correct formatting for values in key-value pairs'''
    return str(value).strip()


def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path
