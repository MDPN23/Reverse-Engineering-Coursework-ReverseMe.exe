import hashlib

def make_serial_from_name(name: str) -> int:    
    # 1. Calculate SHA-256 digest from the name
    name_bytes = name.encode('utf-8')
    hasher = hashlib.sha256()
    hasher.update(name_bytes)
    digest = hasher.digest() 
    
    # 2. Calculate custom sum
    # loop: for (int i = 0; i < 32 && dig[i] != 0; i++)
    custom_sum = 0
    for i in range(len(digest)):
        byte_value = digest[i] 

        if byte_value == 0:
            break
        t = byte_value * i
        term = t * t + 0x50
        custom_sum = (custom_sum + term) & 0xFFFFFFFF
        
    # 3. Final XOR
    FINAL_XOR_KEY = 0x12345678
    serial = custom_sum ^ FINAL_XOR_KEY
    
    return serial & 0xFFFFFFFF

def main():
    # input test name
    name_to_test = "Lorem Ipsum Dolor Sit Amet"
    
    # Calculate serial
    serial_number = make_serial_from_name(name_to_test)
    
    # Output results
    print(f"Name: \"{name_to_test}\"")

    # Print in decimal format
    print(f"Serial (Decimal): {serial_number}")

    # Print in hexadecimal format
    print(f"Serial (Hexadecimal): {serial_number:08X}")

if __name__ == "__main__":
    main()