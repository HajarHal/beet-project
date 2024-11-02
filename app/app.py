from flask import Flask, request, jsonify, render_template
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from google.cloud import storage
from google.cloud import aiplatform
import io
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

storage_client = storage.Client()

def load_data_from_gcs(bucket_name, blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    data = blob.download_as_text()
    return pd.read_csv(io.StringIO(data))

bucket_name = 'beet-bucket-1'
blob_name = 'cropland_daa.csv'
data = load_data_from_gcs(bucket_name, blob_name)

def create_map(data):
    m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(m)
    color_map = {
        "Unsuitable for beet cultivation": "red",
        "Highly suitable for beet cultivation": "green",
        "Moderately suitable": "orange",
        "Marginally suitable - interventions needed": "yellow"
    }

    for _, row in data.iterrows():
        popup_text = (
            f"Latitude: {row['Latitude']}<br>"
            f"Longitude: {row['Longitude']}<br>"
            f"Suitability: {row['suitability_label']}<br>"
            f"cec: {row['cec']}<br>"
            f"phh2o: {row['phh2o']}<br>"
            f"soc: {row['soc']}<br>"
            f"silt: {row['silt']}<br>"
            f"sand: {row['sand']}<br>"
            f"clay: {row['clay']}<br>"
            f"wv0010: {row['wv0010']}<br>"
            f"nitrogen: {row['nitrogen']}<br>"
            f"tmin_oct_nov: {row['tmin_oct_nov']}<br>"
            f"tmax_jan_jun: {row['tmax_jan_jun']}<br>"
            f"prec_oct_mar: {row['prec_oct_mar']}"
        )
        color = color_map.get(row['suitability_label'], "gray")
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=popup_text,
            icon=folium.Icon(color=color)
        ).add_to(marker_cluster)

    return m

def make_online_prediction(project_id, location, endpoint_id, instance):
    aiplatform.init(project=project_id, location=location)
    endpoint_name = f"projects/{project_id}/locations/{location}/endpoints/{endpoint_id}"
    endpoint = aiplatform.Endpoint(endpoint_name=endpoint_name)
    prediction = endpoint.predict(instances=[instance])
    return prediction

def format_prediction_results(prediction_result):
    predictions = prediction_result.predictions[0]
    classes = predictions['classes']
    scores = predictions['scores']
    result = [{"class": class_name, "score": f"{score * 100:.2f}%"} for class_name, score in zip(classes, scores)]
    max_score_index = scores.index(max(scores))
    final_class = {"class": classes[max_score_index], "score": f"{scores[max_score_index] * 100:.2f}%"}

    return result, final_class

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualisation')
def visualisation():
    m = create_map(data)
    map_html = m._repr_html_()
    return render_template('visualisation.html', map_html=map_html)

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/predict', methods=['POST'])
def predict():
    clay = request.form.get('clay')
    sand = request.form.get('sand')
    silt = request.form.get('silt')
    wv0010 = request.form.get('wv0010')
    cec = request.form.get('cec')
    nitrogen = request.form.get('nitrogen')
    soc = request.form.get('soc')
    phh2o = request.form.get('phh2o')
    tmin_oct_nov = request.form.get('tmin_oct_nov')
    tmax_jan_jun = request.form.get('tmax_jan_jun')
    prec_oct_mar = request.form.get('prec_oct_mar')

    instance = {
        "clay": float(clay),
        "sand": float(sand),
        "silt": float(silt),
        "wv0010": float(wv0010),
        "cec": float(cec),
        "nitrogen": float(nitrogen),
        "soc": float(soc),
        "phh2o": float(phh2o),
        "tmin_oct_nov": float(tmin_oct_nov),
        "tmax_jan_jun": float(tmax_jan_jun),
        "prec_oct_mar": float(prec_oct_mar)
    }

    try:
        project_id = 'beet-project'
        location = 'us-central1'
        endpoint_id = '3703033116558884864'
        
        prediction_result = make_online_prediction(project_id, location, endpoint_id, instance)
        formatted_results, final_class = format_prediction_results(prediction_result)

        return render_template("prediction.html", predictions=formatted_results, final_class=final_class), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
