import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_excel("T1.xlsx")
df.replace("TH", pd.NA, inplace=True)

# Convert numeric columns
subjects = ["BM","BI","MM","SAINS","SEJ","PAI","PM","RBT","PSV","PJPK","GEO","BIN","ASK"]
for col in subjects:
    df[col] = pd.to_numeric(df[col], errors="coerce")

st.title("📊 Academic Performance Dashboard")

# Class filter
kelas = st.selectbox("Select Class", sorted(df["KELAS"].unique()))
filtered_class = df[df["KELAS"] == kelas]

# Average scores by subject
avg_scores = filtered_class[subjects].mean()
fig_avg = px.bar(avg_scores, x=avg_scores.index, y=avg_scores.values,
                 title=f"Average Scores in {kelas}", labels={"x":"Subject","y":"Average Score"})
st.plotly_chart(fig_avg)

# Student filter
student = st.selectbox("Select Student", filtered_class["Nama"])
student_data = filtered_class[filtered_class["Nama"] == student].iloc[0]
fig_student = px.bar(student_data[subjects], title=f"{student}'s Scores")
st.plotly_chart(fig_student)

import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_excel("T1.xlsx")
df.replace("TH", pd.NA, inplace=True)

subjects = ["BM","BI","MM","SAINS","SEJ","PAI","PM","RBT","PSV","PJPK","GEO","BIN","ASK"]
for col in subjects:
    df[col] = pd.to_numeric(df[col], errors="coerce")

st.title("📊 Academic Performance Dashboard")

kelas = st.selectbox("Select Class", sorted(df["KELAS"].unique()))
filtered_class = df[df["KELAS"] == kelas]

student = st.selectbox("Select Student", filtered_class["Nama"])
student_data = filtered_class[filtered_class["Nama"] == student].iloc[0]

# Report Card Table
report_card = pd.DataFrame({
    "Subject": subjects,
    "Score": [student_data[subj] for subj in subjects]
})
st.subheader(f"Report Card: {student}")
st.table(report_card)

# Overall average
avg_score = report_card["Score"].mean()
st.metric("Overall Average Score", round(avg_score, 2))

# Convert to CSV for download
csv = report_card.to_csv(index=False).encode("utf-8")
