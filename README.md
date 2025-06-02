
# 🥗 SnapMealAI

https://github.com/debanick19/SnapMealAI/blob/10f919799d81c8ec503997f7f30c49b5b8a7cee0/SnapMeal.png


SnapMealAI is a GenAI-powered nutritionist app that analyzes food images and generates a structured nutritional analysis, using Google’s Gemini 1.5 Vision-Language model. This project was built as part of the [Gen AI Exchange Bootcamp](https://cloud.google.com/) by Google Cloud and Hack2skill to showcase real-world applications of Google AI tools.

---

## 🚀 Features

- 📸 Upload any meal image
- 🔍 Get AI-generated nutritional breakdown:
  - Food item-wise calorie estimates
  - Total calorie count
  - Macronutrients (Protein, Fat, Carbs)
  - Emoji-based health score (e.g., 3/5 🍎)
  - Balanced/Healthy/Unhealthy tag
  - Personalized recommendations
- 🧠 Powered by **Gemini 1.5 Flash API**
- 💾 Local logging using SQLite
- 📊 Meal history dashboard + CSV export

---

## 🧰 Tech Stack

| Technology       | Purpose                             |
|------------------|-------------------------------------|
| [Google Gemini API](https://makersuite.google.com/) | Vision + Language-based meal analysis |
| [Streamlit](https://streamlit.io)       | Interactive UI                        |
| [SQLite](https://www.sqlite.org/index.html)          | Lightweight local data logging       |
| [Pandas](https://pandas.pydata.org/)                | Data handling and export             |
| Python, Regex    | Text parsing and backend logic      |

> 🛠️ **For production**, the app can be upgraded to use:
> - Google Cloud Firestore or BigQuery
> - Firebase Authentication
> - Vertex AI with scalable cloud APIs

---

## 🧪 Accuracy & Model Reliability

- Built using **Gemini 1.5 Flash**, a state-of-the-art vision-language model by Google.
- Able to analyze:
  - Complex food compositions
  - Varying portion sizes
  - Multi-item meals (e.g., South Indian thali)
- Outputs are to-the-point and contextually rich.

---

## 🔍 Why SnapMealAI?

| Feature | SnapMealAI | Market Apps |
|--------|------------|-------------|
| Free to Use | ✅ | ❌ (Subscription required) |
| Vision-Based Input | ✅ | ❌ |
| No Cloud Dependency | ✅ (Optional) | ❌ |
| Personalized Reports | ✅ | ❌ |
| Google AI Powered | ✅ | ❌ |

---

## 🏁 Getting Started

### 📦 Install dependencies
```bash
pip install -r requirements.txt
````

### 🔐 Add API Key

Create a `.env` file:

```
GOOGLE_API_KEY=your_gemini_api_key
```

### ▶️ Run the app

```bash
streamlit run app.py
```

---

## 🧭 Project Structure

```
SnapMealAI/
│
├── app.py                  # Main Streamlit app
├── data/meals.db           # Local SQLite database
├── SnapMeal.png            # Logo image
├── requirements.txt        # Dependencies
└── .env                    # Your API key (not committed)
```

---

## 📦 Future Roadmap

* [ ] Camera-based real-time capture
* [ ] Voice-based meal description (multilingual)
* [ ] Firebase/GCP integration for cloud scaling
* [ ] Integration with Google Fit or Apple HealthKit
* [ ] Food comparison & dietary planning module

---


## 📄 License

This project is released under the [MIT License](LICENSE).

---

## 🤝 Connect With Me

**Debanek Banarjee**
💼 Data Scientist | AI Enthusiast | Builder of SnapMealAI
📫 [LinkedIn](https://www.linkedin.com/in/debanick-banerjee/)



