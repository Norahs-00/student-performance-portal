@'
# School Performance Portal

An interactive Streamlit portal that turns student records into searchable profiles, grade trends and early-attention flags, built on public student-performance data as a data science learning project.

**Live demo:** _coming soon_

> **Data note:** the data comes from two **Portuguese** secondary schools, not Nepal. Student names in the portal are **randomly generated for demonstration**; the dataset itself contains no names or IDs. Nothing here should be used to make decisions about real students.

## What it does
- **Dashboard:** key figures, a "needs attention" watchlist (simple rules), top performers
- **Students:** search by name or record number, filter by school and performance level
- **Profile:** grade trend against the school average, study and home context, observations
- **Analytics:** trend, distribution and factor charts
- **About:** project background, limitations and credits

## Project status
- [x] Data inspection and cleaning (notebook and script)
- [x] Streamlit portal
- [ ] Exploratory analysis write-up
- [ ] Regression models with a leakage-safe pipeline (with and without earlier grades)
- [ ] Prediction page and model comparison
- [ ] Repeat on consented, anonymized Nepali school data

## Data
Cortez, P. & Silva, A. (2008). *Using Data Mining to Predict Secondary School Student Performance.*
UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/320/student+performance (CC BY 4.0).

Changes made: one private column (`romantic`) removed, columns renamed, row-number record IDs and demo names added. See `src/data_preprocessing.py`.

## Run locally
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements-dev.txt
    python src/data_preprocessing.py
    streamlit run app/app.py

On Mac/Linux, activate with `source .venv/bin/activate`.

## Limitations and ethics
- Not Nepali data; findings must not be assumed to hold in Nepal.
- Charts show associations, not causes.
- Study and travel time are coarse bands, not exact values.
- 15 students have a final grade of 0 with no explanation in the data.
- Educational demonstration only; it must not decide anyone's educational opportunities.

## License
Code: MIT (see `LICENSE`). Data: CC BY 4.0 (see `data/README.md`).
'@ | Set-Content README.md

git add README.md
git commit -m "Write project README"
