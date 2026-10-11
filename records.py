import csv
import struct
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator

RECORD_FORMAT = ">IIIHHHHHHBB"
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)
MISSING = 65535

@dataclass
class GameRecord:
    record_id: int
    game_date: int
    team_id_home: int
    pts_home: int | None
    fg_pct_home: float | None
    ft_pct_home: float | None
    fg3_pct_home: float | None
    ast_home: int | None
    reb_home: int | None
    home_team_wins: int 
    deleted: bool = False

def _optional_int(value: str) -> int | None:
    value = value.strip()
    return int(value) if value else None

def _optional_float(value: str) -> float | None:
    value = value.strip()
    return float(value) if value else None

def load_records(path: str | Path) -> Iterator[GameRecord]:
    with open(path, newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file, delimiter="\t")

        for record_id, row in enumerate(rows):
            game_date = int(datetime.strptime(
                  row["GAME_DATE_EST"], "%d/%m/%Y"
              ).strftime("%Y%m%d"))

            yield GameRecord(
                record_id=record_id,
                game_date=game_date,
                team_id_home=int(row["TEAM_ID_home"]),
                pts_home=_optional_int(row["PTS_home"]),
                fg_pct_home=_optional_float(row["FG_PCT_home"]),
                ft_pct_home=_optional_float(row["FT_PCT_home"]),
                fg3_pct_home=_optional_float(row["FG3_PCT_home"]),
                ast_home=_optional_int(row["AST_home"]),
                reb_home=_optional_int(row["REB_home"]),
                home_team_wins=int(row["HOME_TEAM_WINS"]),
            )

def _pack_int(value: int | None) -> int:
    return MISSING if value is None else value

def _pack_pct(value: float | None) -> int:
    return MISSING if value is None else round(value * 1000)

def encode_record(record: GameRecord) -> bytes:
    return struct.pack(
        RECORD_FORMAT,
        record.record_id,
        record.game_date,
        record.team_id_home,
        _pack_int(record.pts_home),
        _pack_pct(record.fg_pct_home),
        _pack_pct(record.ft_pct_home),
        _pack_pct(record.fg3_pct_home),
        _pack_int(record.ast_home),
        _pack_int(record.reb_home),
        record.home_team_wins,
        1 if record.deleted else 0 
    )

def _unpack_int(value: int) -> int | None:
    return None if value == MISSING else value

def _unpack_pct(value: int) -> float | None:
    return None if value == MISSING else value / 1000

def decode_record(data: bytes) -> GameRecord:
    (
        record_id,
        game_date,
        team_id_home,
        pts_home,
        fg_pct_home,
        ft_pct_home,
        fg3_pct_home,
        ast_home,
        reb_home,
        home_team_wins,
        deleted,
    ) = struct.unpack(RECORD_FORMAT, data[:RECORD_SIZE])

    return GameRecord(
        record_id=record_id,
        game_date=game_date,
        team_id_home=team_id_home,
        pts_home=_unpack_int(pts_home),
        fg_pct_home=_unpack_pct(fg_pct_home),
        ft_pct_home=_unpack_pct(ft_pct_home),
        fg3_pct_home=_unpack_pct(fg3_pct_home),
        ast_home=_unpack_int(ast_home),
        reb_home=_unpack_int(reb_home),
        home_team_wins=home_team_wins,
        deleted=bool(deleted),
    )
