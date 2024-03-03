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
    return escape_encode(encoded_command.encode())[0]


def encode_integer(value: int) -> str:
    if value >= 0:
        return b":" + str(value).encode("ascii") + b"\r\n"
    else:
        return b":-" + str(abs(value)).encode("ascii") + b"\r\n"
