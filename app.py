import pandas as pd
import streamlit as st
import plotly.express as px
from fpdf import FPDF

# Load data
df = pd.read_excel("T1.xlsx")
df.replace("TH", pd.NA, inplace=True)

subjects = ["BM","BI","MM","SAINS","SEJ","PAI","PM","RBT","PSV","PJPK","GEO","BIN","ASK"]

# Convert to Int64 (keeps integers + allows NaN)
for col in subjects:
    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

st.title("Dashboard Pelajar")

kelas = st.selectbox("Select Class", sorted(df["KELAS"].unique()))
filtered_class = df[df["KELAS"] == kelas]

student = st.selectbox("Select Student", filtered_class["Nama"])
student_data = filtered_class[filtered_class["Nama"] == student].iloc[0]

# Report Card Table (clean integers, show 'Absent')
report_card = pd.DataFrame({
    "Subject": subjects,
    "Markah": [
        int(student_data[subj]) if pd.notna(student_data[subj]) else " "
        for subj in subjects
    ]
})
st.subheader(f"Report Card: {student}")
st.table(report_card)

# Average score (ignore NaN)
avg_score = report_card["Score"].replace("Absent", pd.NA).dropna().astype(int).mean()
st.metric("Overall Average Score", round(avg_score, 0))

# PDF generator
def create_report_card(student_name, kelas, tahun, scores):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="School Report Card", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Name: {student_name}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Class: {kelas}   Year: {tahun}", ln=True, align="L")
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    for subject, score in scores.items():
        display_score = "Absent" if pd.isna(score) else str(int(score))
        pdf.cell(80, 10, txt=subject, border=1)
        pdf.cell(30, 10, txt=display_score, border=1, ln=True)

    avg_score = pd.Series(list(scores.values())).dropna().astype(int).mean()
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Overall Average: {round(avg_score,0)}", ln=True)

    return pdf.output(dest="S").encode("latin-1")

scores = {subj: student_data[subj] for subj in subjects}
pdf_bytes = create_report_card(student, student_data["KELAS"], student_data["TAHUN"], scores)

st.download_button(
    label="Download Report Card (PDF)",
    data=pdf_bytes,
    file_name=f"{student}_report_card.pdf",
    mime="application/pdf",
)
