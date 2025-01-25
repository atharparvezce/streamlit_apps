import streamlit as st
import pandas as pd
import datetime as dt
import random

# App Title
st.title("AI-Powered Study Planner")
st.markdown("Optimize your study schedule with AI and stay on track for success!")

# Step 1: Input Section
st.header("📋 Enter Your Study Details")
subjects = st.text_area("Enter Subjects (comma-separated)", placeholder="e.g., Math, Science, History")
difficulty_levels = st.text_area("Enter Difficulty Levels for Each Subject (comma-separated, 1-5)", placeholder="e.g., 3, 4, 2")

# Step 2: Enter a Date Range for Initial and Deadline Times
study_period = st.date_input("Select your study period (Initial Date and Deadline Date)", [])

available_time = st.slider("Daily Study Time (hours)", 1, 12, 4)

# Step 3: Input Validation and Timetable Generation
def validate_and_generate_timetable(subjects, study_period, available_time, difficulty_levels):
    subject_list = [s.strip() for s in subjects.split(',') if s.strip()]
    difficulty_list = [d.strip() for d in difficulty_levels.split(',') if d.strip()]

    if not subject_list or not study_period or not difficulty_list:
        st.error("All fields (Subjects, Study Period, Difficulty Levels) must be filled.")
        return None

    if len(subject_list) != len(difficulty_list):
        st.error("The number of subjects and difficulty levels must match.")
        return None
    
    # Extract initial and deadline dates from the selected study period
    initial_time, deadline_time = study_period

    # Calculate number of days between initial time and deadline time
    days_left = (deadline_time - initial_time).days if (deadline_time - initial_time).days > 0 else 1  # Avoid zero days
    
    # Allocate study time per subject based on the difficulty levels
    difficulty_levels_int = list(map(int, difficulty_list))
    total_difficulty = sum(difficulty_levels_int) if sum(difficulty_levels_int) > 0 else 1  # Avoid zero difficulty

    # Study allocation based on difficulty and total time available
    study_allocation = [(difficulty / total_difficulty) * available_time * days_left for difficulty in difficulty_levels_int]

    # Create timetable DataFrame
    timetable = pd.DataFrame({
        "Subject": subject_list,
        "Difficulty Level": difficulty_levels_int,
        "Daily Study Time (hrs)": [round(time, 2) for time in study_allocation]
    })

    return timetable

# Step 4: Generate Timetable
if st.button("Generate Timetable"):
    timetable = validate_and_generate_timetable(subjects, study_period, available_time, difficulty_levels)
    if timetable is not None:
        st.success("🎉 Timetable generated successfully!")
        st.table(timetable)

# Step 5: Progress Tracking
st.header("📊 Track Your Progress")
subject_progress = st.text_area("Enter Your Progress (comma-separated percentages)", placeholder="e.g., 20, 50, 80")
if st.button("Update Progress"):
    subject_list = [s.strip() for s in subjects.split(',') if s.strip()]
    if subject_progress:
        progress = [int(p.strip()) for p in subject_progress.split(',') if p.strip()]
        if len(progress) == len(subject_list):
            progress_df = pd.DataFrame({
                "Subject": subject_list,
                "Progress (%)": progress
            })
            st.success("✅ Progress updated!")
            st.table(progress_df)
        else:
            st.error("The number of progress entries must match the number of subjects.")

# Step 6: Motivational Quotes
st.header("💡 Motivational Quote of the Day")
quotes = [
    "Believe you can and you're halfway there.",
    "Success is not the key to happiness. Happiness is the key to success.",
    "The secret of getting ahead is getting started.",
    "The best way to predict the future is to create it.",
    "Don't watch the clock; do what it does. Keep going.",
]
st.info(random.choice(quotes))

# Step 7: Study Tips
st.header("📚 Study Tips")
st.markdown(
    "- Break your study sessions into smaller, focused intervals (e.g., 25 minutes with a 5-minute break).\n"
    "- Eliminate distractions by keeping your phone away.\n"
    "- Review your notes regularly and practice past questions.\n"
    "- Stay hydrated and take short walks to refresh your mind.\n"
    "- Reward yourself after completing a session to stay motivated."
)
