from utils import mapping, reverse_mapping
def encrypt(str):
    
    encoded_str = ''.join(mapping.get(char, char) for char in str)
    
    return encoded_str

def decrypt(encoded_str):
    decoded_str = ''.join(reverse_mapping.get(encoded_str[i:i+7], encoded_str[i:i+7]) for i in range(0, len(encoded_str), 7))

    return decoded_str
