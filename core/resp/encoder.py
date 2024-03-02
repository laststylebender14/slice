from codecs import escape_encode

def encode_simple_strings_resp(resp: str = "") -> str:
    if resp == "":
        return encode_null_string_resp()
    return f"+{resp}\r\n".encode()

def encode_bulk_strings_reps(resp: str = "") -> str:
    return f"${len(resp)}\r\n{resp}\r\n".encode()

def encode_null_string_resp() -> str:
    return "$-1\r\n".encode()

def encode_redis_command(command):
    parts = [f"${len(part)}\r\n{part}\r\n" for part in command.split()]
    encoded_command = f"*{len(parts)}\r\n{''.join(parts)}"
    print(f" encoded command : {encoded_command.encode()}")
    return escape_encode(encoded_command.encode())[0]