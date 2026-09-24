import pandas as pd
from pathlib import Path

CSV_PATH = Path("data/flights_2025/flights_2025.csv")
OUTPUT_PATH = Path("../frontend/src/airportData.ts")

df = pd.read_csv(
    CSV_PATH,
    usecols=[
        "ORIGIN_AIRPORT_ID",
        "DEST_AIRPORT_ID",
    ],
)

ids = sorted(
    set(df["ORIGIN_AIRPORT_ID"].dropna().astype(int))
    | set(df["DEST_AIRPORT_ID"].dropna().astype(int))
)

with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
    file.write("export const airports = [\n")

    for airport_id in ids:
        file.write(
            f'  {{ id: {airport_id}, label: "{airport_id}" }},\n'
        )

    file.write("];\n")

print(f"Generated {len(ids)} airport IDs.")
print(f"Output: {OUTPUT_PATH}")