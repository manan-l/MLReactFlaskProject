from flask import Flask, request, jsonify, session, redirect, url_for, render_template, flash
from flask_dance.contrib.google import make_google_blueprint, google
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key

# Set up OAuth for Google authentication using Flask-Dance
google_bp = make_google_blueprint(
    client_id="YOUR_GOOGLE_CLIENT_ID",
    client_secret="YOUR_GOOGLE_CLIENT_SECRET",
    scope=["profile", "email"],
    redirect_url="/login/google/authorized"
)
app.register_blueprint(google_bp, url_prefix="/login")

# Load your air quality data (adjust the file path and columns as needed)
df = pd.read_csv("data.csv")  # Assumes a CSV file with columns including date, co, no, no2, o3, so2, pm2_5, pm10, nh3, AQI

def forecast_or_return_data(date_time_str):
    """
    This dummy function simulates a forecast by first checking if the given date-time exists in the dataset.
    If found, it returns the matching record. Otherwise, it generates dummy forecast data.
    """
    try:
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

    # Convert df['date'] to datetime if not already done
    df["date"] = pd.to_datetime(df["date"])
    matching = df[df["date"] == date_time]
    if not matching.empty:
        return matching.iloc[0].to_dict()
    else:
        # Generate dummy forecast data
        forecast_data = {
            "AQI": int(np.random.randint(50, 150)),
            "co": float(np.random.random()),
            "no": float(np.random.random()),
            "no2": float(np.random.random()),
            "o3": float(np.random.random()),
            "so2": float(np.random.random()),
            "pm2_5": float(np.random.random()),
            "pm10": float(np.random.random()),
            "nh3": float(np.random.random())
        }
        return forecast_data

@app.route("/")
def index():
    """Render a simple home page (could be enhanced with templates)"""
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def login():
    """Handle login via Google OAuth."""
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        user_info = resp.json()
        session["logged_in"] = True
        session["user_name"] = user_info.get("name")
        return jsonify({"message": f"Hello, {user_info.get('name')}"}), 200
    return jsonify({"error": "Failed to fetch user info"}), 400

@app.route("/logout", methods=["POST"])
def logout():
    """Log out by clearing the session."""
    session.clear()
    return redirect(url_for("index"))

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict AQI based on the provided date and time.
    Expects 'date_input', 'hour_input', and 'minute_input' in form data.
    """
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized. Please login."}), 401

    date_input = request.form.get("date_input")
    hour_input = request.form.get("hour_input")
    minute_input = request.form.get("minute_input")
    if not (date_input and hour_input and minute_input):
        return jsonify({"error": "Missing parameters"}), 400

    date_time = f"{date_input} {int(hour_input):02d}:{int(minute_input):02d}"
    forecast_data = forecast_or_return_data(date_time)
    if forecast_data:
        return jsonify({
            "Predicted_Values": forecast_data,
            "AQI": forecast_data.get("AQI")
        })
    else:
        return jsonify({"error": "Date not found in dataset."}), 404

@app.route("/data", methods=["GET"])
def get_data():
    """
    Return the air quality data in JSON format.
    Only accessible if the user is logged in.
    """
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized. Please login."}), 401

    # Select the required columns
    columns = ["date", "co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3", "AQI"]
    data = df[columns].to_dict(orient="records")
    return jsonify(data)

@app.route("/analysis", methods=["GET"])
def analysis():
    """
    Generate and return a plot (encoded as a base64 string) for the selected gas/AQI.
    Expects query parameters: gas_selection, date_input, hour_input, minute_input.
    """
    if not session.get("logged_in"):
        return jsonify({"error": "Unauthorized. Please login."}), 401

    gas_selection = request.args.get("gas_selection")
    date_input = request.args.get("date_input")
    hour_input = request.args.get("hour_input")
    minute_input = request.args.get("minute_input")
    if not (gas_selection and date_input and hour_input and minute_input):
        return jsonify({"error": "Missing parameters"}), 400

    # Prepare historical data
    df["date"] = pd.to_datetime(df["date"])
    historical_data = df[["date", gas_selection]].copy()
    historical_data = historical_data.rename(columns={gas_selection: "value"})
    historical_data["type"] = "Existing Values"

    # Prepare predicted data
    date_time = f"{date_input} {int(hour_input):02d}:{int(minute_input):02d}"
    forecast_data = forecast_or_return_data(date_time)
    if forecast_data:
        predicted_value = forecast_data.get(gas_selection)
        predicted_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        predicted_data = pd.DataFrame({
            "date": [predicted_date],
            "value": [predicted_value],
            "type": ["Predicted Value"]
        })

        # Combine historical and predicted data
        combined_data = pd.concat([historical_data, predicted_data])

        # Create the plot
        plt.figure(figsize=(10, 5))
        for label, group in combined_data.groupby("type"):
            if label == "Existing Values":
                plt.plot(group["date"], group["value"], label=label, color="#1E90FF", linewidth=2)
            else:
                plt.scatter(group["date"], group["value"], label=label, color="red", s=100)
        plt.title(f"Historical and Forecasted Values for {gas_selection.upper()}")
        plt.xlabel("Date")
        plt.ylabel(gas_selection)
        plt.legend()
        plt.tight_layout()

        # Save the plot to a bytes buffer and encode it in base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close()
        return jsonify({"plot": img_base64})
    else:
        return jsonify({"error": "No prediction available for the selected date and time."}), 404

if __name__ == "__main__":
    app.run(debug=True)
