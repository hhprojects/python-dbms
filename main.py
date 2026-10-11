from records import RECORD_SIZE, load_records, encode_record, decode_record
from storage import DiskStorage

if __name__ == "__main__":
    records = list(load_records("data/games.txt"))
    print(f"First Record: {records[0]}")

    disk = DiskStorage("data/storage.txt")
    disk.write_records(records)

    print(f"Record size: {RECORD_SIZE} bytes")
    print(f"Total records: {disk.num_records}")
    print(f"Records per block: {disk.records_per_block}")
    print(f"Data blocks: {disk.num_blocks}")

    print(f"Read record: {disk.read_record(26650)}")