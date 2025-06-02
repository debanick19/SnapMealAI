import streamlit as st
import os
import sqlite3
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai
import pandas as pd
import re

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Database
DB_PATH = "data/meals.db"
os.makedirs("data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            food_items TEXT,
            total_calories INTEGER,
            protein INTEGER,
            fat INTEGER,
            carbs INTEGER,
            health_tag TEXT,
            health_score TEXT,
            recommendations TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_gemini_response(input_text, image_parts, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, image_parts[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    else:
        raise FileNotFoundError("No file uploaded")

def insert_meal_log(username, food_items, total_calories, protein, fat, carbs, health_tag, health_score, recommendations):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO meal_logs (username, date, food_items, total_calories, protein, fat, carbs, health_tag, health_score, recommendations) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (username, datetime.now().strftime("%Y-%m-%d %H:%M"), food_items, total_calories, protein, fat, carbs, health_tag, health_score, recommendations))
    conn.commit()
    conn.close()

def load_user_logs(username):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM meal_logs WHERE username = ?", conn, params=(username,))
    conn.close()
    return df

# Initialize
init_db()

# UI Config
st.set_page_config(page_title="SnapMealAI", page_icon="🥗", layout="wide")
st.image("SnapMeal.png", use_column_width=True)
st.markdown("""
    <h1 style='text-align: center; color: #2E8B57;'>🥗 SnapMealAI – Eat Smart, Live Strong 💪</h1>
    <hr style='border: 2px solid #2E8B57;'>
""", unsafe_allow_html=True)

username = st.text_input("👤 Enter your name:", key="username")

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("📤 Upload Your Meal")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

with col2:
    if uploaded_file:
        st.image(uploaded_file, caption="📸 Meal Snapshot", use_column_width=True)

input_text = st.text_input("📝 Any specific input for analysis?", key="input")
submit = st.button("🔍 Analyze and Log Meal")

input_prompt = """
You are a certified nutritionist AI.

Analyze the food items in the image and return:
1. List all recognizable food items with:
   - Quantity (e.g., 2 eggs, 1 bowl rice)
   - Individual calorie count (if relevant)
   - Total calorie contribution
   - Format: Item Name (quantity): Total Calories – Details if needed

2. Total estimated calorie count for the full meal.

3. Total estimated macronutrient breakdown:
   - Protein: XX grams
   - Fat: XX grams
   - Carbohydrates: XX grams

4. One-line health assessment of the meal.

5. Health Tag:
   - Healthy 🟢
   - Balanced 🟡
   - Unhealthy 🔴

6. Health score (1–5) and a short sentence with emoji: e.g., 3/5 🍏

7. One recommendation to make it healthier.

Be concise and clear.
"""

if submit and username.strip() != "" and uploaded_file is not None:
    image_data = input_image_setup(uploaded_file)
    try:
        response = get_gemini_response(input_text, image_data, input_prompt)
        st.subheader("📋 Nutrition Analysis")
        st.write(response)

        lines = response.split("\n")
        total = 0
        food_summary = []
        protein = fat = carbs = 0
        health_tag = ""
        health_score = ""
        recommendations = []

        for line in lines:
            line_lower = line.lower()

            if 'total' in line_lower and 'calorie' in line_lower and total == 0:
                numbers = re.findall(r'(\d+)', line)
                if numbers:
                    nums = [int(n) for n in numbers]
                    total = sum(nums) // len(nums)

            if "protein" in line_lower and protein == 0:
                match = re.search(r'(\d+)(?:[-–](\d+))?', line)
                if match:
                    protein = (int(match.group(1)) + int(match.group(2))) // 2 if match.group(2) else int(match.group(1))

            if "fat" in line_lower and fat == 0:
                match = re.search(r'(\d+)(?:[-–](\d+))?', line)
                if match:
                    fat = (int(match.group(1)) + int(match.group(2))) // 2 if match.group(2) else int(match.group(1))

            if "carb" in line_lower and carbs == 0:
                match = re.search(r'(\d+)(?:[-–](\d+))?', line)
                if match:
                    carbs = (int(match.group(1)) + int(match.group(2))) // 2 if match.group(2) else int(match.group(1))

            if any(tag in line_lower for tag in ["healthy", "unhealthy", "balanced"]):
                if "healthy" in line_lower:
                    health_tag = "Healthy 🟢"
                elif "balanced" in line_lower:
                    health_tag = "Balanced 🟡"
                elif "unhealthy" in line_lower:
                    health_tag = "Unhealthy 🔴"

            if "score" in line_lower and health_score == "":
                health_score = line.strip()

            if any(keyword in line_lower for keyword in ["suggest", "alternative", "recommend"]):
                recommendations.append(line.strip())

            if 'calorie' in line_lower and 'total' not in line_lower:
                food_summary.append(line.strip())

        insert_meal_log(
            username,
            "\n".join(food_summary),
            total,
            protein,
            fat,
            carbs,
            health_tag,
            health_score,
            "\n".join(recommendations)
        )

        st.success("✅ Meal logged!")
        st.info(f"🥩 Protein: {protein}g | 🧈 Fat: {fat}g | 🍚 Carbs: {carbs}g")
        if health_tag:
            st.success(f"📊 Health Tag: {health_tag}")
        if health_score:
            st.success(f"🧘‍♂️ {health_score}")
        if recommendations:
            st.subheader("💡 Recommendations:")
            for rec in recommendations:
                st.markdown(f"- {rec}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

if username.strip() != "":
    st.subheader("📊 Your Meal History")
    logs_df = load_user_logs(username)
    if not logs_df.empty:
        st.dataframe(logs_df[["date", "food_items", "protein", "fat", "carbs", "health_tag", "health_score", "recommendations"]].sort_values(by="date", ascending=False))
        st.bar_chart(logs_df.set_index("date")["protein"])
        csv = logs_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Meal History as CSV",
            data=csv,
            file_name=f"{username}_meal_logs.csv",
            mime='text/csv')
    else:
        st.info("📭 No meals logged yet. Upload a meal image above.")
else:
    st.info("📝 Enter your name to track your progress.")
