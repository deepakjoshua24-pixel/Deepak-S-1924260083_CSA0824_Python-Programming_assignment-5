# Part A design notes
## A1 Data acquisition and storage
CSV fields: station, date, hour, PM2.5, PM10, NO, temperature. Expected issues: blank/NA, negative values, implausibly high sensor values, duplicate station-time rows, malformed dates/hours, inconsistent station case/whitespace, Fahrenheit at Thiruvanmiyur and Porur, missing columns, delimiter/encoding errors.
SQLite: stations(station_id INTEGER PRIMARY KEY, station_name TEXT UNIQUE, temperature_unit TEXT); readings(station_id INTEGER, day TEXT, hour INTEGER, pm25 REAL, pm10 REAL, no REAL, temperature_c REAL, PRIMARY KEY(station_id,day,hour), FOREIGN KEY station_id). Index (station_id,day). CSV requires repeated full scans; SQL supports filtered/grouped queries and indexes.
## A2 Cleaning and normalisation
Convert blanks/NA to missing; median-impute numeric columns for this demonstration; reject malformed rows; set out-of-range values missing; deduplicate by station/date/hour; convert Fahrenheit with (F-32)*5/9. Min-max: (x-min)/(max-min); z-score: (x-mean)/population_sd. Min-max suits bounded visual scaling; z-score suits comparisons around a mean. Date YYYY-MM-DD, station title case, numeric values floating point in standard units.
## A3 Charts and summary
Monthly trend=line; station comparison=bar; temperature vs PM2.5=scatter; worst hours=bar or box plot. Daily summary: station, day, minimum, maximum, mean, valid count, produced with SQL GROUP BY.
## A4 Debugging and profiling
Use print for temporary values, assert invariants, logging levels for durable diagnostics, pdb breakpoints for step-through. Use perf_counter for end-to-end timing, timeit for isolated functions, cProfile for call-level hotspots.
## A5 AI design
Lexicon score adds +1/-1 and flips the next sentiment word after not/never/no. Extractive summary ranks sentences by frequencies of non-stop words. Rule chatbot extracts station and pollutant keywords and uses parameterised SQL. Limitations: sarcasm, context, spelling, ambiguous questions and limited vocabulary.
