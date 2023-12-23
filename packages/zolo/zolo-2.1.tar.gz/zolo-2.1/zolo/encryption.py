def encrypt(mapping, str):
    
    encoded_str = ''.join(mapping.get(char, char) for char in str)
    
    return encoded_str

def decrypt(reverse_mapping, encoded_str):
    decoded_str = ''.join(reverse_mapping.get(encoded_str[i:i+7], encoded_str[i:i+7]) for i in range(0, len(encoded_str), 7))

    return decoded_str
