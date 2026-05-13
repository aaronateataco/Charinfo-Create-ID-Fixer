import sys
import os

def fix_charinfo(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False
    
    try:
        with open(file_path, 'rb') as f:
            data = bytearray(f.read())
        
        if len(data) < 9:
            print(f"Error: File '{file_path}' is too small ({len(data)} bytes).")
            return False
        
        old_val = data[0x08]
        # Set bit 7 to 1, bit 6 to 0 (UUIDv4 variant 10)
        # 0x80 is 10000000, 0x3F is 00111111
        new_val = (old_val & 0x3F) | 0x80
        
        if old_val == new_val:
            print(f"File '{file_path}' already has the correct variant bits (0x{old_val:02X}).")
            return True
        
        data[0x08] = new_val
        
        fixed_path = file_path
        # Optional: Save to a new file or overwrite. 
        # For now, let's overwrite as requested "automatically edit".
        with open(fixed_path, 'wb') as f:
            f.write(data)
            
        print(f"Fixed '{file_path}': 0x{old_val:02X} -> 0x{new_val:02X}")
        return True
    except Exception as e:
        print(f"An error occurred while processing '{file_path}': {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_charinfo.py <file1.charinfo> [file2.charinfo ...]")
    else:
        for path in sys.argv[1:]:
            fix_charinfo(path)
