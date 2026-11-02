# adv-data-assignment-1

By Jack Walker | Advanced Data Journalism

## About this project

In this repository, we parse all film screenings at AMC theaters in New York City from Monday, Nov. 2, 2026 to Sunday, Nov. 8, 2026, and store them in a .CSV file.

Then we analyze whether theaters are complying with New York City's open caption laws, which mandate that a certain number of film screenings be shown with captions, and at various times of the day, so that Deaf and hard of hearing moviegoers can have an array of options.

This analysis found that, while the city's AMC theaters provide several open captioned screenings each week, they all fall short from fully meeting the city's open caption laws within the time frame provided.

## How to run the code

1. **Manually collect** webpage data from AMC New York City theaters by copy and pasting into .txt files based on date and venue (see `data/import/screenings/raw/amc/`)
2. **Convert .txt files** into a parsed .CSV showtime file using `scripts/build_amc_csv.py`. \(NOTE: this Python script was written with AI, and not intended to be the bulk of the assignment, but rather just a step to get my data ready.\)
3. **Run through our first analysis**, `notebooks/screenings/amc/amc_total_req.ipynb`, to determine whether the theaters are complying with the city's mininum for the number of open captioned screenings per film in a given week.
4. **Run through our second analysis**, `notebooks/screenings/amc/amc_time_req.ipynb`, to determine whether the theaters are complying with the city's mininum for the number of open captioned screenings per film presented IN PEAK HOURS during a given week.
5. **Export findings** into .CSV files in `data/export/screenings/amc/`

## Data outputs
* Movie screenings that qualify for our analysis: `screenings-filtered-dataset/amc_screenings_relevant_to_law.csv`
* The number of screenings per theater and rates of violation: `violations-by-total/theater_violation_totals.csv`
** The number of screenings violating open caption frequency laws per AMC theater: `violations-by-total/screenings_per_theater.csv`
* The number of screenings violating open caption time of day laws per AMC theater: `violations-by-time/time_violations.csv`

## Organization

- `scripts/` — Python scripts, including .txt file parser (build_amc_csv.py)
- `notebooks/` — Analysis notebooks
- `notes/` — Project notes for personal use
- `data/import/` — Imported data (like showtime raw .txt files)
- `data/export/` — Exported data (like counts and rates)