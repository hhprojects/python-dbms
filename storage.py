from records import GameRecord, RECORD_SIZE, encode_record, decode_record
import math

BLOCK_SIZE = 4096
RECORDS_PER_BLOCK = BLOCK_SIZE // RECORD_SIZE

class DiskStorage:
    def __init__(self, path):
        self.path = path
        self.block_size = BLOCK_SIZE
        self.records_per_block = RECORDS_PER_BLOCK
        self.num_records = 0
        self.num_blocks = 0
        self.blocks_read = 0

    def write_records(self, records: list[GameRecord]) -> None:
        self.num_records = len(records)
        self.num_blocks = math.ceil(self.num_records / self.records_per_block)
        with open(self.path, "wb") as file:
            for start in range(0, len(records), self.records_per_block):
                block = b"".join(encode_record(r) for r in records[start:start + self.records_per_block])
                block = block.ljust(self.block_size, b"\x00")
                file.write(block)
        


    def read_block(self, block_id: int) -> bytes:
        if not 0 <= block_id < self.num_blocks:
            raise IndexError(f"block_id {block_id} out of range [0, {self.num_blocks})")
        self.blocks_read += 1
        with open(self.path, "rb") as file:
            file.seek(block_id * self.block_size)
            block = file.read(self.block_size)
        return block

    def read_record(self, record_id: int) -> GameRecord: 
        if not 0 <= record_id < self.num_records:
            raise IndexError(f"record_id {record_id} is out of range [0, {self.num_records})")
        record_block = record_id // self.records_per_block
        block = self.read_block(record_block)

        record_slot = record_id % self.records_per_block
        offset = record_slot * RECORD_SIZE
        record_data = block[offset: offset + RECORD_SIZE]
        return decode_record(record_data)
        
    def update_record(self, record_id: int, record: GameRecord) -> None: ...
