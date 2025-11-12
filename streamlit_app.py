
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE SETUP ---
st.set_page_config(page_title="EPM5033 Health Data Dashboard", layout="wide")
st.title("📊 EPM5033 Health Data Analytics Dashboard")
st.markdown("### Assessment 1 — Blood Sugar, BMI, and Demographics Analysis")

# --- DATA UPLOAD ---
st.sidebar.header("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Data successfully uploaded!")
else:
    st.info("Please upload your dataset to start.")
    st.stop()

# --- DATA PREVIEW ---
st.subheader("1️⃣ Dataset Preview and Cleaning")
st.write("Below is a quick look at your dataset:")
st.dataframe(df.head())

# Basic info
st.write("**Shape:**", df.shape)
st.write("**Missing Values:**")
st.write(df.isnull().sum())

# Drop duplicates button
if st.button("Remove Duplicates"):
    df = df.drop_duplicates()
    st.success("Duplicates removed!")

# --- EXPLORATORY ANALYSIS ---
st.subheader("2️⃣ Exploratory Data Analysis")

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
if numeric_cols:
    chosen_var = st.selectbox("Select a numeric variable for distribution:", numeric_cols)
    fig, ax = plt.subplots()
    sns.histplot(df[chosen_var], kde=True, ax=ax)
    st.pyplot(fig)

# --- SCATTER PLOT ---
st.subheader("3️⃣ Relationship Between Variables")
if len(numeric_cols) >= 2:
    x_var = st.selectbox("Select X variable:", numeric_cols, index=0)
    y_var = st.selectbox("Select Y variable:", numeric_cols, index=1)
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x=x_var, y=y_var, ax=ax)
    st.pyplot(fig)

# --- BOX PLOT BY CATEGORY ---
st.subheader("4️⃣ Boxplot by Category")
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
if categorical_cols:
    cat_var = st.selectbox("Select a categorical variable:", categorical_cols)
    num_var = st.selectbox("Select a numeric variable:", numeric_cols)
    fig, ax = plt.subplots()
    sns.boxplot(x=cat_var, y=num_var, data=df, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- BINARY / BMI ANALYSIS ---
st.subheader("5️⃣ Binary Variable Analysis")
if "BMI" in df.columns:
    bmi_bins = [0, 18.5, 24.9, 29.9, 100]
    bmi_labels = ["Underweight", "Normal", "Overweight", "Obese"]
    df["BMI_Category"] = pd.cut(df["BMI"], bins=bmi_bins, labels=bmi_labels)

    if "BloodSugar" in df.columns:
        fig, ax = plt.subplots()
        sns.barplot(x="BMI_Category", y="BloodSugar", data=df, ci=None, ax=ax)
        st.pyplot(fig)

st.markdown("---")
st.markdown("👨‍💻 *Developed by Sahil Zagade — EPM5033 Assessment 1*")
