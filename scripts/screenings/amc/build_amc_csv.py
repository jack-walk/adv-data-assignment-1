from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
ROOT = REPO_ROOT / "data/import/screenings/raw/amc"
OUT_PATH = ROOT / "amc.csv"

THEATER_META = {
    "bay-plaza-13": {
        "theater": "AMC Bay Plaza Cinema 13",
        "address": "2210 Bartow Avenue, Bronx, NY 10475",
        "borough": "Bronx",
        "neighborhood": "Baychester",
        "zip": "10475",
        "slug": "amc-bay-plaza-cinema-13",
    },
    "84th-st-6": {
        "theater": "AMC 84th Street 6",
        "address": "2310 Broadway, New York, NY 10024",
        "borough": "Manhattan",
        "neighborhood": "Upper West Side",
        "zip": "10024",
        "slug": "amc-84th-street-6",
    },
    "orpheum-7": {
        "theater": "AMC Orpheum 7",
        "address": "1538 Third Ave, New York, NY 10028",
        "borough": "Manhattan",
        "neighborhood": "Upper East Side",
        "zip": "10028",
        "slug": "amc-orpheum-7",
    },
    "village-7": {
        "theater": "AMC Village 7",
        "address": "66 Third Ave, New York, NY 10003",
        "borough": "Manhattan",
        "neighborhood": "East Village",
        "zip": "10003",
        "slug": "amc-village-7",
    },
    "19th-st-east-6": {
        "theater": "AMC 19th St. East 6",
        "address": "890 Broadway, New York, NY 10003",
        "borough": "Manhattan",
        "neighborhood": "Union Square",
        "zip": "10003",
        "slug": "amc-19th-st-east-6",
    },
    "lincoln-square-13": {
        "theater": "AMC Lincoln Square 13",
        "address": "1998 Broadway, New York, NY 10023",
        "borough": "Manhattan",
        "neighborhood": "Lincoln Square",
        "zip": "10023",
        "slug": "amc-lincoln-square-13",
    },
    "34th-st-14": {
        "theater": "AMC 34th Street 14",
        "address": "312 West 34th Street, New York, NY 10001",
        "borough": "Manhattan",
        "neighborhood": "Midtown",
        "zip": "10001",
        "slug": "amc-34th-street-14",
    },
    "kips-bay-15": {
        "theater": "AMC Kips Bay 15",
        "address": "570 Second Avenue, New York, NY 10016",
        "borough": "Manhattan",
        "neighborhood": "Kips Bay",
        "zip": "10016",
        "slug": "amc-kips-bay-15",
    },
    "magic-johnson-harlem-9": {
        "theater": "AMC Magic Johnson Harlem 9",
        "address": "2309 Frederick Douglass Blvd, New York, NY 10027",
        "borough": "Manhattan",
        "neighborhood": "Harlem",
        "zip": "10027",
        "slug": "amc-magic-johnson-harlem-9",
    },
    "bay-terrace-6": {
        "theater": "AMC Bay Terrace 6",
        "address": "211-01 26th Ave, Bayside, NY 11360",
        "borough": "Queens",
        "neighborhood": "Bayside",
        "zip": "11360",
        "slug": "amc-bay-terrace-6",
    },
    "fresh-meadows-7": {
        "theater": "AMC Fresh Meadows 7",
        "address": "190-02 Horace Harding Blvd., Fresh Meadows, NY 11365",
        "borough": "Queens",
        "neighborhood": "Fresh Meadows",
        "zip": "11365",
        "slug": "amc-fresh-meadows-7",
    },
    "staten-island-11": {
        "theater": "AMC DINE-IN Staten Island 11",
        "address": "2655 Richmond Avenue, Staten Island, NY 10314",
        "borough": "Staten Island",
        "neighborhood": "New Springville",
        "zip": "10314",
        "slug": "amc-staten-island-11",
    },
    "empire-25": {
        "theater": "AMC Empire 25",
        "address": "234 West 42nd Street, New York, NY 10036",
        "borough": "Manhattan",
        "neighborhood": "Times Square",
        "zip": "10036",
        "slug": "amc-empire-25",
    },
}

DURATION_RE = re.compile(r"^\d+\s*HR\s*\d+\s*MIN$", re.I)
TIME_RE = re.compile(r"\b(\d{1,2}:\d{2}(?:am|pm))\b", re.I)
HEADER_DATE_RE = re.compile(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s+([A-Za-z]{3})\s+(\d{1,2})$")
DOW_MAP = {
    "Mon": "Monday",
    "Tue": "Tuesday",
    "Wed": "Wednesday",
    "Thu": "Thursday",
    "Fri": "Friday",
    "Sat": "Saturday",
    "Sun": "Sunday",
}


def fmt_time(t12: str) -> str:
    return datetime.strptime(t12.upper(), "%I:%M%p").strftime("%-I:%M %p")


def parse_time_minutes(t12: str) -> int:
    t = datetime.strptime(t12.upper(), "%I:%M%p")
    return t.hour * 60 + t.minute


def is_peak(day_name: str, t12: str) -> bool:
    mins = parse_time_minutes(t12)
    fri_start = 17 * 60 + 59
    sat_sun_start = 11 * 60 + 29
    end = 23 * 60 + 1

    if day_name == "Friday":
        return fri_start <= mins <= end
    if day_name in {"Saturday", "Sunday"}:
        return sat_sun_start <= mins <= end
    if day_name in {"Monday", "Tuesday", "Wednesday", "Thursday"}:
        return fri_start <= mins <= end
    return False


def parse() -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    issues: list[str] = []

    for folder, metadata in sorted(THEATER_META.items()):
        folder_path = ROOT / folder

        for text_file in sorted(folder_path.glob("2026-11-*.txt")):
            date_str = text_file.stem
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            day_name = dt.strftime("%A")
            lines = [ln.strip() for ln in text_file.read_text(errors="ignore").splitlines()]

            header_match = None
            for ln in lines[:30]:
                m = HEADER_DATE_RE.match(ln)
                if m:
                    header_match = m
                    break

            if header_match:
                header_day = DOW_MAP[header_match.group(1)]
                header_dom = int(header_match.group(3))
                if header_day != day_name or header_dom != dt.day:
                    issues.append(
                        f"Header mismatch: {text_file} -> '{header_match.group(0)}' vs filename {date_str}"
                    )
            else:
                issues.append(f"No header date found: {text_file}")

            parse_end = len(lines)
            for idx, ln in enumerate(lines):
                if "Trailers and InfoPlay Trailer for" in ln:
                    parse_end = idx
                    break

            title_indexes: list[int] = []
            for i in range(parse_end - 1):
                current_line = lines[i]
                next_line = lines[i + 1]
                if not current_line:
                    continue
                if DURATION_RE.match(next_line):
                    title_indexes.append(i)

            for idx, start_idx in enumerate(title_indexes):
                film = re.sub(r"\s+", " ", lines[start_idx]).strip()
                end_idx = title_indexes[idx + 1] if idx + 1 < len(title_indexes) else parse_end
                block = lines[start_idx:end_idx]

                open_caption = False
                found_time = False

                for ln in block[1:]:
                    if "Open Caption (On-screen Subtitles)" in ln:
                        open_caption = True
                        continue
                    if ln == "Closed Caption":
                        open_caption = False
                        continue

                    for tm in TIME_RE.findall(ln):
                        found_time = True
                        rows.append(
                            {
                                "Date": date_str,
                                "Day of week": day_name,
                                "Film": film,
                                "Showtime": fmt_time(tm),
                                "Peak hours?": "Yes" if is_peak(day_name, tm) else "No",
                                "Open captioned?": "Yes" if open_caption else "No",
                                "Theater": metadata["theater"],
                                "Company": "AMC",
                                "Address": metadata["address"],
                                "Borough": metadata["borough"],
                                "Neighborhood": metadata["neighborhood"],
                                "Zip Code": metadata["zip"],
                                "URL": f"https://www.amctheatres.com/movie-theatres/new-york-city/{metadata['slug']}/showtimes?date={date_str}",
                                "Notes": "",
                            }
                        )

                if not found_time:
                    issues.append(f"No showtimes parsed: {text_file} :: {film}")

    rows.sort(
        key=lambda r: (
            r["Date"],
            r["Theater"],
            r["Film"],
            datetime.strptime(r["Showtime"], "%I:%M %p"),
        )
    )
    return rows, issues


def write_csv(rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "Date",
        "Day of week",
        "Film",
        "Showtime",
        "Peak hours?",
        "Open captioned?",
        "Theater",
        "Company",
        "Address",
        "Borough",
        "Neighborhood",
        "Zip Code",
        "URL",
        "Notes",
    ]

    with OUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    parsed_rows, parse_issues = parse()
    write_csv(parsed_rows)

    bad_time_rows = 0
    for row in parsed_rows:
        try:
            datetime.strptime(row["Showtime"], "%I:%M %p")
        except ValueError:
            bad_time_rows += 1

    print(f"CSV written: {OUT_PATH}")
    print(f"Rows: {len(parsed_rows)}")
    print(f"Issues: {len(parse_issues)}")
    print(f"Bad time rows: {bad_time_rows}")
    if parse_issues:
        print("Sample issues:")
        for issue in parse_issues[:20]:
            print(f"- {issue}")
