import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Set up the Streamlit page layout
st.set_page_config(page_title="Study Hours Analysis", page_icon="📊", layout="centered")

# Custom CSS for styling, animations, and button effects
st.markdown("""
    <style>
        /* Full Background Image Styling */
        body {
            background-image: url('https://example.com/your-hdr-image.jpg');
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
            height: 100vh;
            margin: 0;
            font-family: 'Arial', sans-serif;
        }

        /* Header styling with animation */
        .header {
            font-size: 30px;
            color: #4CAF50;
            animation: fadeIn 2s ease-in-out;
            text-align: center;
            margin-top: 20px;
        }
        /* Summary styling */
        .summary {
            font-size: 18px;
            color: #333;
            text-align: center;
            line-height: 1.5;
            margin-bottom: 20px;
            padding: 0 30px;
            animation: fadeInUp 2s ease-in-out;
        }
        /* Button styling with hover effect */
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #3E8E41;
        }
        /* Animation for header and summary */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Highlight selected text with black background and white text */
        .summary::selection {
            background-color: black;
            color: white;
        }
        /* Highlight important words with orange color */
        .highlight {
            color: orange;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Add header with animation
st.markdown('<h1 class="header">📊 Student Study Hours Analysis</h1>', unsafe_allow_html=True)

# Add a professional summary paragraph with subtle fade-in effect and highlighted words in orange
st.markdown("""
    <div class="summary">
        This application provides a comprehensive analysis of students' daily study hours, focusing on key metrics such as the 
        sample mean and <span class="highlight">confidence interval</span>. By uploading a CSV file with recorded study hours, 
        you can instantly assess the <span class="highlight">average study time</span> per student and visualize how it compares 
        to recommended study guidelines. Leveraging statistical tools and an interactive interface, this app offers an easy 
        way to understand and reflect on study habits.
    </div>
""", unsafe_allow_html=True)

# Step 1: Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Step 2: Read the CSV file
    data = pd.read_csv(uploaded_file)
    
    # Check if 'study_hours' column exists
    if 'study_hours' in data.columns:
        study_hours = data['study_hours'].dropna()  # Drop any missing values
        
        # Step 3: Calculate the Sample Mean
        sample_mean = study_hours.mean()
        st.write(f"### Sample Mean (Average Study Hours): {sample_mean:.2f} hours")
        
        # Step 4: Calculate the 90% Confidence Interval
        n = len(study_hours)
        sample_std = study_hours.std(ddof=1)  # Sample standard deviation
        confidence_level = 0.90
        margin_of_error = stats.t.ppf((1 + confidence_level) / 2, n - 1) * (sample_std / np.sqrt(n))
        lower_bound = sample_mean - margin_of_error
        upper_bound = sample_mean + margin_of_error
        confidence_interval = (lower_bound, upper_bound)
        
        st.write(f"### 90% Confidence Interval: ({lower_bound:.2f}, {upper_bound:.2f}) hours")

        # Step 5: Visualize the Data
        fig, ax = plt.subplots()
        ax.scatter(range(1, n + 1), study_hours, label='Study Hours', color='blue')
        ax.axhline(sample_mean, color='green', linestyle='--', label=f'Mean: {sample_mean:.2f} hours')
        ax.fill_between(range(1, n + 1), lower_bound, upper_bound, color='orange', alpha=0.2, label='90% Confidence Interval')
        
        ax.set_xlabel('Student Number')
        ax.set_ylabel('Daily Study Hours')
        ax.set_title('Daily Study Hours with Confidence Interval')
        ax.legend()
        
        st.pyplot(fig)

        # Step 6: Comparison and Reflection
        st.write("### Comparison to Recommended Study Time")
        st.write("The recommended study time is 2 hours per day.")
        
        if 2 >= lower_bound and 2 <= upper_bound:
            st.success("The recommended study time of 2 hours falls within the confidence interval.")
        else:
            st.warning("The recommended study time of 2 hours does NOT fall within the confidence interval.")
        
    else:
        st.error("The uploaded file must contain a column named 'study_hours'.")
