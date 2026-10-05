"""School Performance Portal (demo): top-bar version on the UCI Student Performance data."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "processed" / "student_por_clean.csv"
BLUE, RED = "#4C78A8", "#E45756"
st.set_page_config(page_title="School Performance Portal", page_icon="🏫", layout="wide",
                   initial_sidebar_state="collapsed")
st.markdown("""<style>
[data-testid="stSidebar"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapsedControl"]{display:none}
.topbar{background:#1f3a5f;color:#fff;padding:14px 22px;border-radius:12px;margin-bottom:10px}
.topbar b{font-size:21px}.topbar span{opacity:.75;font-size:13px;margin-left:14px}
/* navigation: plain clickable text tabs, no radio dots */
div[data-testid="stRadio"] div[role="radiogroup"]{gap:4px;border-bottom:2px solid #e6e9ef}
div[data-testid="stRadio"] label>div:first-child{display:none}
div[data-testid="stRadio"] label{padding:9px 20px;border-radius:8px 8px 0 0;cursor:pointer;margin:0}
div[data-testid="stRadio"] label:hover{background:#eef2f8}
div[data-testid="stRadio"] label:has(input:checked){background:#1f3a5f}
div[data-testid="stRadio"] label:has(input:checked) p{color:#fff;font-weight:600}
.card{background:#fff;border:1px solid #e6e9ef;border-radius:12px;padding:14px 18px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.card h2{margin:0;font-size:26px;color:#111827}.card p{margin:0;color:#6b7280;font-size:13px}
.badge{padding:3px 12px;border-radius:999px;color:#fff;font-size:14px;font-weight:600}
.hero{background:linear-gradient(135deg,#1f3a5f,#4C78A8);color:#fff;padding:38px 34px;border-radius:16px}
.hero h1{margin:0 0 8px 0;font-size:34px;color:#fff}.hero p{margin:0;font-size:16px;opacity:.92;max-width:760px}
.info{background:#f6f8fb;border-left:4px solid #4C78A8;border-radius:8px;padding:14px 16px;height:100%}
.info h4{margin:0 0 6px 0;color:#1f3a5f}.info p{margin:0;color:#4b5563;font-size:14px}
.warn{background:#fff7ed;border-left:4px solid #FB8C00;border-radius:8px;padding:14px 16px;height:100%}
.warn h4{margin:0 0 6px 0;color:#9a3412}.warn p{margin:0;color:#4b5563;font-size:14px}
</style>""", unsafe_allow_html=True)

BANDS = [(16, "Excellent", "#2E7D32"), (14, "Good", "#7CB342"), (12, "Satisfactory", "#F9A825"),
         (10, "Sufficient", "#FB8C00"), (0, "Below pass", "#D32F2F")]  # scale from Cortez & Silva (2008)
LEVELS = [b[1] for b in BANDS]
STUDY = {1: "Under 2 hrs/week", 2: "2-5 hrs/week", 3: "5-10 hrs/week", 4: "Over 10 hrs/week"}
TRAVEL = {1: "Under 15 min", 2: "15-30 min", 3: "30-60 min", 4: "Over 1 hour"}
COLS = {"name": "Name", "record": "Record", "school": "School", "age": "Age", "g1": "Period 1",
        "g2": "Period 2", "g3": "Final", "band": "Level", "absences": "Absences", "Why": "Why"}
FEMALE = ["Sita", "Anita", "Sabina", "Pooja", "Binita", "Sunita", "Nisha", "Rekha", "Kritika",
          "Manisha", "Aarati", "Sandhya", "Susmita", "Prativa", "Rojina", "Sarita"]
MALE = ["Ram", "Bikash", "Sujan", "Prakash", "Rajesh", "Anil", "Suman", "Dipesh", "Ashish",
        "Kiran", "Sandip", "Bibek", "Roshan", "Nabin", "Sagar", "Ujjwal"]
LAST = ["Sharma", "Thapa", "Shrestha", "Adhikari", "Gurung", "Karki", "Yadav", "Mahato", "Chaudhary",
        "Rai", "Tamang", "Poudel", "Bhandari", "Basnet", "Khadka", "Jha", "Mishra", "Sah", "Mandal", "Das"]
NAME_NOTE = ("Names are randomly generated for demonstration. They do not belong to the real "
             "students in the dataset.")

# EDIT THIS: rewrite in your own words so it is true for you.
WHY = (
    "I wanted a project that connects data science with something that matters in everyday life: "
    "school. Student results are shaped by many things, such as study habits, attendance and "
    "support at home, and I wanted to learn how data could help teachers notice earlier who may "
    "need extra help.\n\n"
    "I did not have access to a suitable dataset from Nepali schools, so I built the method on a "
    "well-documented public dataset from Portuguese schools. The goal is to prove the full "
    "workflow (cleaning, analysis, a usable portal, and later a prediction model) so the same "
    "work can be repeated on real Nepali data, collected with consent and with names removed."
)


def band(g):
    return next((n, c) for lo, n, c in BANDS if g >= lo)


@st.cache_data
def load():
    d = pd.read_csv(DATA)
    rng = np.random.default_rng(42)  # fixed seed: same names every run
    first = np.where(d.sex == "F", rng.choice(FEMALE, len(d)), rng.choice(MALE, len(d)))
    d.insert(0, "record", [f"REC-{i:04d}" for i in range(1, len(d) + 1)])
    d.insert(1, "name", [f"{a} {b}" for a, b in zip(first, rng.choice(LAST, len(d)))])
    d["band"] = d.g3.map(lambda g: band(g)[0])
    d["trend"] = d.g3 - d.g1
    return d


def card(col, label, val):
    col.markdown(f"<div class='card'><p>{label}</p><h2>{val}</h2></div>", unsafe_allow_html=True)


def open_profile():
    st.session_state.selected = st.session_state.pick
    st.session_state.page = PAGES[2]


def tidy(ax):
    ax.spines[["top", "right"]].set_visible(False)


df = load()
NAMES = dict(zip(df.record, df.name))
PAGES = ["Dashboard", "Students", "Profile", "Analytics", "About"]
st.markdown("<div class='topbar'><b>School Performance Portal</b>"
            "<span>Demo · public data from Portuguese schools · not for real decisions</span></div>",
            unsafe_allow_html=True)
page = st.radio("Navigation", PAGES, key="page", horizontal=True, label_visibility="collapsed")
st.write("")

# ---------------------------------------------------------------- DASHBOARD
if page == PAGES[0]:
    st.title("School Overview")
    wl = df[(df.g3 < 10) | (df.trend <= -3)].copy()
    wl["Why"] = np.where(wl.g3 < 10, "Below pass mark", "Grades fell 3+ points")
    kpis = [("Students", len(df)), ("Average final grade", f"{df.g3.mean():.1f} / 20"),
            ("Pass rate (10+)", f"{(df.g3 >= 10).mean():.0%}"), ("Needs attention", len(wl)),
            ("Excellent (16+)", int((df.g3 >= 16).sum()))]
    for col, (label, val) in zip(st.columns(5), kpis):
        card(col, label, val)
    st.write("")
    left, right = st.columns(2)
    left.subheader("⚠️ Needs attention")
    left.caption("Simple rule: final grade below 10, or a fall of 3+ points since Period 1.")
    left.dataframe(wl.sort_values("g3").head(10)[["name", "record", "g1", "g2", "g3", "Why"]]
                   .rename(columns=COLS), hide_index=True)
    right.subheader("🏆 Top performers")
    right.caption("Highest final grades.")
    right.dataframe(df.sort_values(["g3", "g2"], ascending=False).head(10)[["name", "record", "g1", "g2", "g3", "band"]]
                    .rename(columns=COLS), hide_index=True)
    st.subheader("By school")
    st.dataframe(df.groupby("school").agg(Students=("g3", "size"), Average_final=("g3", "mean"),
                 Pass_rate_pct=("g3", lambda x: (x >= 10).mean() * 100)).round(1))
    st.caption(NAME_NOTE)

# ----------------------------------------------------------------- STUDENTS
elif page == PAGES[1]:
    st.header("Students")
    c1, c2, c3 = st.columns([2, 1, 1])
    q = c1.text_input("Search by name or record number", placeholder="e.g. Sita, Thapa, or 42").strip().lower()
    schools = sorted(df.school.unique())
    school = c2.multiselect("School", schools, default=schools)
    levels = c3.multiselect("Performance level", LEVELS, default=LEVELS)
    res = df[df.school.isin(school) & df.band.isin(levels)]
    if q:
        res = res[res.name.str.lower().str.contains(q, regex=False) | res.record.str.lower().str.contains(q, regex=False)]
    st.caption(f"{len(res)} students found. {NAME_NOTE}")
    st.dataframe(res[["name", "record", "school", "age", "g1", "g2", "g3", "band", "absences"]].rename(columns=COLS),
                 hide_index=True)
    if len(res):
        st.selectbox("Select a student", res.record, key="pick", format_func=lambda r: f"{NAMES[r]} ({r})")
        st.button("Open profile →", on_click=open_profile, type="primary")

# ------------------------------------------------------------------ PROFILE
elif page == PAGES[2]:
    rec = st.session_state.get("selected")
    if not rec:
        st.info("No student selected yet. Go to **Students**, pick someone, and click *Open profile*.")
        st.stop()
    s = df[df.record == rec].iloc[0]
    level, color = band(s.g3)
    st.markdown(f"## {s['name']} <span class='badge' style='background:{color}'>{level}</span>",
                unsafe_allow_html=True)
    st.caption(f"{s.record} · School {s.school} · Age {s.age} · {NAME_NOTE}")
    m = st.columns(4)
    m[0].metric("Period 1", int(s.g1))
    m[1].metric("Period 2", int(s.g2), int(s.g2 - s.g1))
    m[2].metric("Final grade", int(s.g3), int(s.g3 - s.g2))
    m[3].metric("Cohort position", f"Top {(df.g3 >= s.g3).mean() * 100:.0f}%")
    st.subheader("Grade trend")
    st.line_chart(pd.DataFrame({"This student": [s.g1, s.g2, s.g3],
                                "School average": df[["g1", "g2", "g3"]].mean().values},
                               index=["Period 1", "Period 2", "Period 3"]))
    t1, t2, t3 = st.tabs(["Study & attendance", "Home & support", "Observations"])
    with t1:
        a, b = st.columns(2)
        a.metric("Weekly study time", STUDY[s.study_time])
        a.metric("Past class failures", int(s.failures))
        b.metric("Absences", int(s.absences), f"school average {df.absences.mean():.1f}", delta_color="off")
        b.metric("Extra paid classes", s.paid_classes.title())
    with t2:
        a, b = st.columns(2)
        a.metric("Internet at home", s.internet.title())
        a.metric("Travel time to school", TRAVEL[s.travel_time])
        b.metric("Extra school support", s.school_support.title())
        b.metric("Wants higher education", s.wants_higher_ed.title())
    with t3:
        notes = []
        if s.g3 < 10:
            notes.append("Final grade is below the pass mark of 10.")
        if s.trend <= -3:
            notes.append(f"Grades fell {int(-s.trend)} points from Period 1 to the final grade.")
        if s.trend >= 3:
            notes.append(f"Grades rose {int(s.trend)} points from Period 1 to the final grade.")
        if s.absences > df.absences.quantile(0.75):
            notes.append(f"{int(s.absences)} absences, more than 75% of students.")
        if s.failures > 0:
            notes.append("Has failed one or more classes before.")
        if s.g3 == 0 and s.g2 >= 8:
            notes.append("Final grade is 0 despite earlier passing grades. The data does not say why.")
        for n in notes or ["No flags: nothing unusual compared with the rest of the data."]:
            st.markdown("- " + n)
        st.caption("Simple rules, not predictions. They describe the record and do not explain causes.")
    st.download_button("⬇️ Download this record (CSV)", s.to_frame().T.to_csv(index=False),
                       file_name=f"{s.record}.csv", mime="text/csv")

# ---------------------------------------------------------------- ANALYTICS
elif page == PAGES[3]:
    st.header("Analytics")
    t1, t2, t3, t4 = st.tabs(["Grade trend", "Distribution", "Factors", "Earlier vs final"])
    with t1:
        st.subheader("Average grade by period")
        st.line_chart(df.groupby("school")[["g1", "g2", "g3"]].mean().T.rename(
            index={"g1": "Period 1", "g2": "Period 2", "g3": "Period 3"}))
        st.caption("GP and MS are the two schools in the data. Averages across all students in each school.")
    with t2:
        st.subheader("Final grade distribution")
        st.bar_chart(df.g3.value_counts().sort_index().rename("Students"))
        st.caption("Each bar is a grade from 0 to 20. The small bar at 0 is students with a final grade of zero.")
        st.subheader("Performance levels")
        st.bar_chart(df.band.value_counts().reindex(LEVELS).rename("Students"))
    with t3:
        absg = pd.cut(df.absences, [-1, 0, 2, 5, 10, 100], labels=["1. 0 days", "2. 1-2", "3. 3-5", "4. 6-10", "5. 11+"])
        factors = {"Weekly study time": (df.study_time, {k: f"{k}. {v}" for k, v in STUDY.items()}),
                   "Absences": (absg, None),
                   "Past class failures": (df.failures, None),
                   "Travel time to school": (df.travel_time, {k: f"{k}. {v}" for k, v in TRAVEL.items()}),
                   "Internet at home": (df.internet, None),
                   "Extra paid classes": (df.paid_classes, None)}
        pick = st.selectbox("Compare average final grade by:", list(factors))
        codes, labels = factors[pick]
        summ = df.groupby(codes, observed=True).g3.agg(Average="mean", Students="count")
        if labels:
            summ.index = [labels[i] for i in summ.index]
        summ.index = summ.index.astype(str)
        st.bar_chart(summ["Average"])
        st.dataframe(summ.round(1))
        st.caption("This shows association, not cause. Groups with few students (see the Students column) are unreliable.")
    with t4:
        st.subheader("Period 2 grade vs final grade")
        st.scatter_chart(df, x="g2", y="g3", x_label="Period 2 grade", y_label="Final grade")
        st.caption(f"Correlation {df.g2.corr(df.g3):.2f}. Earlier grades are strongly linked to final grades, "
                   "which is why we test models with and without them.")

# -------------------------------------------------------------------- ABOUT
else:
    zeros = int((df.g3 == 0).sum())
    st.markdown(
        "<div class='hero'><h1>About this project</h1>"
        "<p>A school performance portal that turns student records into clear profiles, trends and "
        "early-attention flags, built as a data science learning project and designed for "
        "honesty about what the data can and cannot say.</p></div>", unsafe_allow_html=True)

    # Optional: put your own image at app/assets/school.jpg (or .png) and it appears here
    assets = HERE / "assets"
    photo = next(assets.glob("school.*"), None) if assets.exists() else None
    if photo:
        st.write("")
        st.image(str(photo))

    st.write("")
    st.subheader("Why I chose this project")
    st.markdown(WHY)

    st.subheader("What the portal does")
    feats = [("Find any student", "Search by name or record number and open a full profile with grades, study habits and home context."),
             ("Spot who needs help", "A simple rule-based watchlist flags failing grades and big drops since Period 1."),
             ("See the bigger picture", "Trend, distribution and factor charts show how the whole school is doing.")]
    for c, (t, d) in zip(st.columns(3), feats):
        c.markdown(f"<div class='info'><h4>{t}</h4><p>{d}</p></div>", unsafe_allow_html=True)

    st.write("")
    st.subheader("The data at a glance")
    f1, f2, f3 = st.columns(3)
    with f1:
        fig, ax = plt.subplots(figsize=(5, 3.4))
        ax.hist(df.g3, bins=range(0, 22), color=BLUE, edgecolor="white")
        ax.axvline(10, color=RED, linestyle="--", label="Pass mark (10)")
        ax.set_xlabel("Final grade (0-20)")
        ax.set_ylabel("Students")
        ax.legend(frameon=False)
        tidy(ax)
        st.pyplot(fig)
        st.caption(f"Most students cluster around 10 to 14. {zeros} students have a final grade of 0.")
    with f2:
        avg = df.groupby("study_time").g3.mean()
        fig, ax = plt.subplots(figsize=(5, 3.4))
        ax.bar(["<2h", "2-5h", "5-10h", ">10h"], avg.values, color=BLUE)
        ax.set_ylim(0, 20)
        ax.set_xlabel("Weekly study time (reported in bands)")
        ax.set_ylabel("Average final grade")
        tidy(ax)
        st.pyplot(fig)
        st.caption("Higher study-time groups tend to have higher averages. That is an association, not proof.")
    with f3:
        fig, ax = plt.subplots(figsize=(5, 3.4))
        ax.scatter(df.g2, df.g3, alpha=0.35, color=BLUE, s=18)
        ax.set_xlabel("Period 2 grade")
        ax.set_ylabel("Final grade")
        tidy(ax)
        st.pyplot(fig)
        st.caption(f"Earlier grades are strongly linked to final grades (correlation {df.g2.corr(df.g3):.2f}).")

    st.subheader("Limitations")
    lims = [("Not Nepali data", "The records come from two Portuguese secondary schools. Findings here should not be assumed to hold in Nepal."),
            ("Associations, not causes", "Charts show what goes together. They cannot show what causes what."),
            ("Coarse measurements", "Study time and travel time were recorded in bands, not exact hours or minutes."),
            ("Demo names", "The data has no names. Names shown are randomly generated and only for demonstration."),
            ("Unexplained zeros", f"{zeros} students have a final grade of 0, often after passing earlier grades. The data does not say why."),
            ("Not for real decisions", "This is an educational demonstration. It must not be used to judge or decide anything about real students.")]
    for row in (lims[:3], lims[3:]):
        for c, (t, d) in zip(st.columns(3), row):
            c.markdown(f"<div class='warn'><h4>{t}</h4><p>{d}</p></div>", unsafe_allow_html=True)
        st.write("")

    st.subheader("What comes next")
    st.markdown(
        "- Train and compare regression models, with and without earlier grades, using a leakage-safe pipeline.\n"
        "- Add a prediction page that gives an *estimated* score, never a guarantee.\n"
        "- Explain which factors drive the model, with correct wording about correlation vs causation.\n"
        "- Repeat the method on real, consented, anonymized data from Nepali schools.")

    st.subheader("Data credit and license")
    st.markdown(
        "Data: Cortez, P. & Silva, A. (2008), *Using Data Mining to Predict Secondary School Student "
        "Performance*, via the UCI Machine Learning Repository "
        "(https://archive.ics.uci.edu/dataset/320/student+performance), licensed CC BY 4.0. "
        "Changes made: one private column removed, columns renamed, demo names added.")