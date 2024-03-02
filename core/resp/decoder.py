from typing import List
from codecs import escape_decode

def decode_redis_command(data: str) -> List[str]:
    data = escape_decode(data)[0].decode().strip()
    
    if not data:
        raise ValueError("Empty RESP message")

    # Split the data by carriage returns
    lines = data.splitlines()

    # Check for valid message format (first element starts with "*")
    if not lines[0].startswith("*"):
        raise ValueError("Invalid RESP message format")

    num_elements = int(lines[0][1:],10)

    if len(lines) != (num_elements * 2 + 1):
        raise ValueError("Malformed RESP message: number of elements mismatch")

    result = []
    for i in range(1, len(lines), 2):  # Skip the first line and iterate by pairs
        # Extract the argument type and length
        try:
            arg_length = int(lines[i][1:], 10)
            arg_type = lines[i][0]
        except (IndexError, ValueError):
            raise ValueError(f"Malformed RESP message: invalid argument format at line {i}")

        # Extract and decode the argument based on type
        if arg_type == "$":  # String
            arg_data = lines[i + 1][:arg_length]
            if len(arg_data) == arg_length:
                result.append(arg_data)
            else:
                raise ValueError(f"argument data and it's length doens't match")
        elif arg_type == "*":  # Nested multi-bulk message (not currently supported)
            raise ValueError("Nested multi-bulk messages not supported yet.")
        else:
            raise ValueError(f"Unsupported RESP argument type: {arg_type}")


    return result
