# Open-Caption Compliance Checklist (Weekly)

Use this checklist (NYC open-caption law) from:
- data/import/policies/open-caption-law_official.pdf
- data/import/policies/open-caption-law_plain-language.pdf

## 1) Scope / applicability
- Theater had more than 10 total showings that week.
- Film had an open-caption version available (if distributed without OC, exempt).
- Film had at least 4 showings in the week (otherwise no minimum count requirement under the quarter-rule).

## 2) Core weekly OC minimum per film
For each theater + film + week:
- Let total showings = T.
- Required OC count = R = min(4, ceil(0.25 * T)), applied when T >= 4.
- Pass if actual OC showings >= R.

## 3) Timing distribution tests
For the same theater + film + week:
https://www.amctheatres.com/movie-theatres/new-york-city/amc-orpheum-7/showtimes?date=2026-11-02
### Peak hours definition
- Friday: 5:59 PM–11:01 PM
- Saturday/Sunday: 11:29 AM–11:01 PM

### Peak allocation rule
- At least half of required OC showings in peak hours.
- Exception: if fewer than 1/8 of film showings are in peak hours, then all peak-hour showings must be OC.

### Weekday evening rule (outside peak)
- For required OC showings outside peak, at least half should be Mon–Thu, starting after 5:59 PM and finishing before 11:01 PM.
- Exception: if fewer than 1/8 of film showings are after 5:59 PM Mon–Thu, then all such showings must be OC.

## 4) Overlap rule
- OC showings that overlap each other cannot be counted toward minimum required OC counts, unless overlap was not practicable to avoid.

## 5) Public notice rule
- OC showings must be advertised like all other showings, and clearly marked as OC.

## 6) Records rule
- Theater should maintain compliance records for 3 years.

## Data needed to say “definitive pass/fail”
From this dataset, most fields are present. For definitive legal-grade checks, add:
- Runtime (to verify “finish before 11:01 PM”).
- Screen/auditorium and exact start/end timestamps (to test overlap).
- Evidence that OC version was/was not distributed for exempt films.
- Archived public listing snapshots (proof of OC labeling in ads).
