import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
from fpdf import FPDF
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from fpdf import FPDF
import base64

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.set_text_color(40, 40, 40)
        self.cell(200, 10, " Bengaluru Choke Point Report", ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(200, 10, "Generated via Streamlit | www.google.com/maps", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def congestion_color(level):
    if level == "High": return (255, 80, 80)     # Red
    if level == "Medium": return (255, 204, 0)   # Yellow
    return (0, 200, 0)                           # Green

def generate_pdf(df, filename="choke_point_report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for _, row in df.iterrows():
        level = row['congestion_level']
        color = congestion_color(level)
        pdf.set_text_color(*color)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 10, f"{row['area']} -- {row['delay_minutes']} mins ({level})", ln=True)

        pdf.set_text_color(80, 80, 80)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 8, f"{row['day_of_week']}, {row['time_slot']} | Reason: {row['reason']}", ln=True)
        pdf.cell(0, 8, f"Suggested Fix: {row['suggested_fix']}", ln=True)
        pdf.ln(5)

    pdf.output(filename)

    # Return downloadable content
    with open(filename, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return base64_pdf

# ========== Setup ==========
st.set_page_config(page_title="Fix Bengaluru Choke Points", layout="wide")
st.title("🚦 Fix Bengaluru Choke Points — No More Memes, Let’s Solve It!")

# ========== Load Data ==========
FILE = "choke_points.csv"

def load_data():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
    else:
        df = pd.DataFrame(columns=["lat", "lon", "area", "delay_minutes", "time_slot", "day_of_week", "reason"])
    return df

df = load_data()

# ========== Suggested Fix Mapping ==========
suggestions = {
    "No signal or traffic cop": "Add traffic signal or assign cop",
    "Too many crossings": "Install pedestrian skywalk",
    "Merging roads": "Add lane dividers and signage",
    "U-turn chaos": "Create structured U-turns",
    "Poor lane discipline": "Deploy traffic enforcement",
}
df["suggested_fix"] = df["reason"].map(suggestions).fillna("Review manually")

# ========== Sidebar Filters (Fixed Day Order) ==========
st.sidebar.title("🔍 Filter Choke Points")

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_options = ["All"] + [day for day in day_order if day in df['day_of_week'].unique()]
reason_options = ["All"] + sorted(df['reason'].unique())

filter_day = st.sidebar.selectbox("Filter by Day", day_options)
filter_reason = st.sidebar.selectbox("Filter by Reason", reason_options)

filtered_df = df.copy()
if filter_day != "All":
    filtered_df = filtered_df[filtered_df['day_of_week'] == filter_day]
if filter_reason != "All":
    filtered_df = filtered_df[filtered_df['reason'] == filter_reason]

# ========== Display Map ==========
st.markdown("""
This dashboard shows **realistically simulated** traffic choke points in Bengaluru using Google Maps insights and local knowledge.  
Each point shows the location, average delay, possible reason, and suggested fix.
""")

m = folium.Map(location=[12.9716, 77.5946], zoom_start=12)

for _, row in filtered_df.iterrows():
    popup = f"""
    <b>{row['area']}</b><br>
    Delay: {row['delay_minutes']} mins<br>
    Time: {row['time_slot']} ({row['day_of_week']})<br>
    Reason: {row['reason']}<br>
    <i>Suggested Fix:</i> {row['suggested_fix']}
    """
    folium.Marker([row['lat'], row['lon']], tooltip=row['area'], popup=popup, icon=folium.Icon(color="red")).add_to(m)

st_folium(m, width=1000, height=600)

# ========== Show Data Table ==========
st.subheader("📋 Choke Point Table")
st.dataframe(filtered_df, use_container_width=True)

# ========== Add New Submission ==========
st.subheader("📝 Submit a New Choke Point")

with st.form("submit_form"):
    lat = st.text_input("Latitude")
    lon = st.text_input("Longitude")
    area = st.text_input("Area Name")
    delay = st.number_input("Estimated Delay (in minutes)", 5, 300, 60)
    time_slot = st.text_input("Time Slot (e.g., 6PM - 9PM)")
    day_of_week = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    reason = st.text_area("Possible Reason")
    submit = st.form_submit_button("Submit")

if submit:
    new_entry = pd.DataFrame([{
        "lat": float(lat), "lon": float(lon), "area": area,
        "delay_minutes": delay, "time_slot": time_slot,
        "day_of_week": day_of_week, "reason": reason
    }])
    new_entry.to_csv(FILE, mode='a', index=False, header=False)
    st.success("Choke point submitted!")

# ========== Export Cleaned Report to CSV ==========
if st.button("📤 Export Cleaned Report to CSV"):
    export_df = filtered_df.copy()
    export_df["congestion_level"] = pd.cut(export_df["delay_minutes"], bins=[0, 30, 90, 300], labels=["Low", "Medium", "High"])
    export_df["suggested_fix"] = export_df["reason"].map(suggestions).fillna("Review manually")

    # Sort by congestion level and delay
    export_df = export_df.sort_values(by=["congestion_level", "delay_minutes"], ascending=[False, False])

    # Reorder columns for clarity
    export_df = export_df[[
        "area", "lat", "lon", "day_of_week", "time_slot", "delay_minutes",
        "reason", "congestion_level", "suggested_fix"
    ]]

    export_df.to_csv("choke_point_report.csv", index=False)
    
    st.success("🧾 Report saved as **choke_point_report.csv** (sorted & structured).")
    # Open file and provide download button
    with open("choke_point_report.csv", "rb") as f:
        st.download_button(
            label="📥 Download CSV Report",
            data=f,
            file_name="choke_point_report.csv",
            mime="text/csv"
        )

# ========== Generate and Download Color PDF Report ==========
if st.button("📕 Generate & Download PDF Report"):
    report_df = filtered_df.copy()
    report_df["congestion_level"] = pd.cut(report_df["delay_minutes"], bins=[0, 30, 90, 300], labels=["Low", "Medium", "High"])
    report_df["suggested_fix"] = report_df["reason"].map(suggestions).fillna("Review manually")

    # Sort for better readability
    report_df = report_df.sort_values(by=["congestion_level", "delay_minutes"], ascending=[False, False])
    pdf_base64 = generate_pdf(report_df)

    st.success(" PDF generated. Click below to download.")
    href = f'<a href="data:application/pdf;base64,{pdf_base64}" download="bengaluru_choke_points.pdf">📥 Download PDF Report</a>'
    st.markdown(href, unsafe_allow_html=True)


# ========== ML Upgrade: Predict Congestion Level with Area + Reason + Context ==========
st.subheader("🤖 Predict Congestion Severity (ML Demo with Location Awareness)")

from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter
from math import radians, cos, sin, asin, sqrt

# Reason Clustering
general_reason_map = {
    "No signal or traffic cop": "Lack of traffic control",
    "Too many crossings": "Pedestrian interference",
    "Bottleneck near junction": "Junction bottleneck",
    "Poor lane discipline": "Driver behavior",
    "No underpass or U-turn": "Road design issue",
    "Merging roads with no signal coordination": "Merge conflict",
    "Bad signal timing and pedestrian crossings": "Signal timing issue",
    "Bottleneck due to flyover merging": "Flyover merge",
    "School traffic and no lane enforcement": "School zone",
    "Multiple U-turns and bus stops on main road": "Bus/U-turn congestion",
    "Frequent metro construction-related blockage": "Construction",
    "Auto-rickshaw stand clogging exit": "Parking conflict",
    "Tech park outflow with no signals": "Tech park crowd",
    "Broken signals and parked vehicles": "Broken infra",
    "Unregulated pedestrian crossing": "Pedestrian interference",
    "High-speed entry and narrow merge": "Merge conflict",
    "ORR merge + bus depot exit": "High-volume merge",
    "Construction + school zone overlap": "Construction",
    "Rash turns & poor markings": "Driver behavior"
}

# Haversine helper
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

if len(df) >= 10:
    df_ml = df.copy()
    df_ml["delay_level"] = pd.cut(df_ml["delay_minutes"], bins=[0, 30, 90, 300], labels=["Low", "Medium", "High"])
    df_ml["general_reason"] = df_ml["reason"].map(general_reason_map).fillna("Other")

    # Fix weekday order
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df_ml["day_of_week"] = pd.Categorical(df_ml["day_of_week"], categories=day_order, ordered=True)

    # Encode categorical features
    le_day = LabelEncoder()
    le_time = LabelEncoder()
    le_reason = LabelEncoder()
    le_area = LabelEncoder()

    X = pd.DataFrame({
        "day": le_day.fit_transform(df_ml['day_of_week']),
        "time": le_time.fit_transform(df_ml['time_slot']),
        "reason": le_reason.fit_transform(df_ml['general_reason']),
        "area": le_area.fit_transform(df_ml['area'])
    })
    y = df_ml["delay_level"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    st.write(f"📊 Model Accuracy: `{acc * 100:.2f}%`")

    st.markdown("### 🔍 Try Predicting Delay Severity Below:")
    
    reason_options = list(le_reason.classes_)
    reason_options.insert(0, "Any Reason")  # Add 'Any Reason' on top

    with st.form("predict_form"):
        form_days = [d for d in day_order if d in le_day.classes_]
        test_day = st.selectbox("Day", form_days)
        test_time = st.selectbox("Time Slot", le_time.classes_)
        test_reason = st.selectbox("Reason", reason_options)
        test_area = st.selectbox("Area", le_area.classes_)
        predict_btn = st.form_submit_button("Predict")

    if predict_btn:
        # Get lat/lon of selected area
        area_lat = df[df['area'] == test_area]['lat'].values[0]
        area_lon = df[df['area'] == test_area]['lon'].values[0]

        if test_reason != "Any Reason":
            test_input = pd.DataFrame([{
                "day": le_day.transform([test_day])[0],
                "time": le_time.transform([test_time])[0],
                "reason": le_reason.transform([test_reason])[0],
                "area": le_area.transform([test_area])[0]
            }])
            pred = model.predict(test_input)[0]
            st.success(f"📍 Predicted Congestion Level for **{test_area}** with reason *'{test_reason}'*: `{pred}`")

        else:
            # Simulate predictions for all reasons
            simulated_preds = []
            for r in le_reason.classes_:
                test_input = pd.DataFrame([{
                    "day": le_day.transform([test_day])[0],
                    "time": le_time.transform([test_time])[0],
                    "reason": le_reason.transform([r])[0],
                    "area": le_area.transform([test_area])[0]
                }])
                simulated_preds.append(model.predict(test_input)[0])

            most_common = Counter(simulated_preds).most_common(1)[0][0]
            st.success(f"📍 Predicted Congestion Level for **{test_area}** *(any reason)*: `{most_common}`")

        # Show influence from nearby areas
        df["distance_km"] = df.apply(lambda row: haversine(area_lat, area_lon, row["lat"], row["lon"]), axis=1)
        nearby = df[df["distance_km"] <= 1.5]

        if len(nearby) > 1:
            common_level = pd.cut(nearby["delay_minutes"], bins=[0, 30, 90, 300], labels=["Low", "Medium", "High"]).mode()[0]
            st.info(f"🧭 Nearby areas (within 1.5 km) show most common congestion: **{common_level}**")

    # Highlight top congested areas
    st.markdown("### 🏙️ Top High Congestion Areas (Based on Current Data)")
    top_areas = df_ml[df_ml["delay_level"] == "High"]["area"].value_counts().head(3)
    for area, count in top_areas.items():
        st.write(f"🔴 {area} — {count} high congestion reports")

else:
    st.warning("Need at least 10 entries to train ML model.")
