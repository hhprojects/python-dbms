from records import RECORD_SIZE, load_records, encode_record, decode_record

if __name__ == "__main__":
    records = load_records("data/games.txt")
    first = next(records)

    encoded = encode_record(first)
    decoded = decode_record(encoded)

    print(f"Record Size: {RECORD_SIZE} bytes")
    print(f"Encoded Length: {len(encoded)} bytes")
    print(f"First Record: {decoded}")