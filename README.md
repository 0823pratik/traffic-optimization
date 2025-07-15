# 🚦 Bangalore Traffic Choke Point Analyzer

> **A Streamlit-based ML app to detect, analyze, and report traffic congestion hotspots in Bengaluru using local insights, satellite patterns, and machine learning.**

---

## ❗ Problem Statement

Bangalore’s traffic isn’t just a meme anymore — it’s a crisis.

> It took **2 hours and 15 minutes** to cover **11 km** in Bangalore traffic on a *Saturday late night*. One commuter was stuck for **100 minutes** at a single choke point on ORR, wondering why there wasn’t a signal or a traffic cop at that location.  
>  
> But instead of adding another *“Bangalore traffic meme”*, he asked:  
> **“Why not fix it?”**

Google Maps now offers **BigQuery-based traffic management insights**, which could help governments analyze road stress. However, direct use of this requires a paid API, authorization, and advanced pipeline setup.

---

## ✅ What I'm Doing Now

> ⚠️ **No APIs or paid services used.**  
> For this demo, we're using a **locally curated CSV file** that captures:
> 
> - Real Bangalore locations
> - Actual congestion delays (user-sourced or satellite-verified)
> - Time slots and weekdays
> - Specific reasons (e.g., signal gaps, flyover merges)

This enables:

-  Filtering based on day and reason
-  ML-based delay severity predictions
-  Nearby area influence (geo-context aware)
-  Unicode PDF/CSV report generation
-  Add choke points with form — data grows with time

> ⚙️ This no-cost, lightweight solution mimics what BigQuery-based apps could achieve — ideal for **proof of concept**, **hackathons**, or **early-stage deployment**.

---

##  Features

| Feature | Description |
|--------|-------------|
|  Filter by Day & Reason | View choke points by weekday or cause |
|  ML-Based Predictions | Predict congestion severity from selected inputs |
|  Nearby Area Influence | Predicts severity using neighboring points |
|  Smart Report Export | Unicode PDF & CSV with emoji severity markers |
|  Add Choke Point | Append new data entries from the UI |
|  Any Reason Logic | Simulate predictions without needing a specific cause |

---
## Results - What You Get from This App
When you launch and use the app, you gain **actionable insights** and **downloadable outputs** to support smarter, real-world decisions.

### Filtered Choke Point Insights  
You can filter congestion points based on:
- **Day of the week** (e.g., Monday, Saturday)
- **Reason** (e.g., No signal, Flyover bottleneck, etc.)

📝 Instantly view a **refined list** of traffic hotspots matching your criteria — great for spotting patterns like *"Friday evening tech park congestion."*

---
<img width="1919" height="958" alt="image" src="https://github.com/user-attachments/assets/aad61da2-bd48-420c-8e53-37322712748b" />
<img width="1919" height="913" alt="image" src="https://github.com/user-attachments/assets/13450f25-a61d-4f0b-9dce-ab9a896471d0" />

### 📄 Report Generation  
After filtering or predicting, users can export insights as reports:

- **PDF Report**  
    - Color-coded severity (🔴 High, 🟠 Medium, 🔵 Low)  
    - Emojis for visual clarity  
    - Includes time slots, locations, delay data  
    - Clean fonts and professional layout — ready for sharing

- **CSV Report**  
    - Structured raw data  
    - Perfect for spreadsheets, dashboards, or analysis workflows  
    - Fields: `lat, lon, area, delay_minutes, time_slot, day_of_week, reason`

 Both reports are instantly downloadable and saved in your project folder.

---

###  Add New Choke Points  
Users can contribute new traffic points using the app’s built-in form.  
Each new entry is:
- Instantly added to the dataset  
- Available for future analysis and model retraining

Enables **community-driven, real-time data enrichment**.

---
<img width="1919" height="947" alt="image" src="https://github.com/user-attachments/assets/06d00037-2519-4b21-8cbd-e515fb650823" />

###  ML-Based Congestion Prediction  
Select:
- Day  
- Time slot  
- Area  
- Reason (or choose **"Any Reason"** for a broader view)

 The app predicts:
- **Congestion Severity**: 🔵 Low, 🟠 Medium, 🔴 High  
- **Contextual Confidence**: Inferred from real congestion trends

It also auto-displays the **Top 3 most frequently congested areas** based on current data.

---

### Nearby Area Awareness  
When a selected area has limited data, but **nearby locations (within 1.5 km)** show recurring congestion, the app boosts prediction reliability by:
- **Inheriting congestion context from nearby zones**  
- Reducing false negatives for less-reported regions

---
<img width="1919" height="900" alt="image" src="https://github.com/user-attachments/assets/02783530-601b-4925-9735-0ba8b5a22457" />

---


##  ML Model

- Model: `LogisticRegression`
- Inputs: `day`, `time_slot`, `reason`, `area`
- Output: Delay Level → `Low / Medium / High`
- Enhanced with:  
   `"Any Reason"` simulation  
   Nearby location-based adjustments (1.5 km radius)

---

## 📂 File Structure

```
bangalore-choke-points-demo/
│
├── app.py                    # Main Streamlit application
├── choke_points.csv          # Primary data file
├── choke_point_report.csv    # Generated CSV report
├── choke_point_report.pdf    # Generated PDF report
├── report.pdf                # Older sample report
├── requirements.txt          # Python dependencies
├── .streamlit/               # Streamlit config files
└── README.md                 # You're reading this
```

---

##  Run the App

### Installation

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit fpdf2 pandas scikit-learn
```

###  Launch the Streamlit App

```bash
python -m streamlit run app.py
```

Then open the local URL in your browser.

---

## 🗂️ Data Format

Stored in **`choke_points.csv`**, looks like this:

```csv
lat,lon,area,delay_minutes,time_slot,day_of_week,reason
12.9352,77.6144,ORR - Agara,100,10:00 PM - 12:00 AM,Saturday,No signal or traffic cop
12.9843,77.5489,Yeshwanthpur Circle,75,8:00 AM - 10:30 AM,Tuesday,Bad signal timing and pedestrian crossings
...
```

You can also add new entries via the form in the app.

---

## 📄 Reports

After filtering or predicting:

- 🧾 **PDF report**: color-coded, emoji-based, formatted with area and delay insights  
- 📊 **CSV report**: structured format for sharing, editing, and visualization

---

## 🔮 Future Advancements

We can plan to expand this into a powerful civic-tech platform:

-  **Google BigQuery integration** for large-scale traffic analytics
-  **Heatmap overlays** from satellite + traffic sensors
-  **Crowdsourced submission portal** with moderation & ranking
-  **Signal timing suggestions** for traffic departments
-  **Historical time-series heatmaps**
-  **AI-based pattern clustering** (e.g. weekend vs weekday vs event-based)
-  **Ward-wise dashboards** for BBMP and local authorities

---

## 🤝 Contribute

This is just the beginning. You can contribute by:

- Adding new data points via the app
- Forking and improving model accuracy
- Raising issues or suggesting features
- Helping with real-time data integrations (if you have sources)

---

## 📜 License

Licensed under the **MIT License** — use, modify, deploy.

---

## 👨‍💻 Developed by

**Pratik Raj**  
🚦 Traffic Optimization Researcher • UG at IIT Tirupati • Intern at IIT Bhilai  
[🔗 GitHub](https://github.com/0823pratik/traffic-optimization) · [💼 LinkedIn](https://www.linkedin.com/in/pratik-raj-295472280/)
