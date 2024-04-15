from flask import Flask, request, render_template
import numpy as np
import joblib
from prometheus_flask_instrumentator import Instrumentator
app = Flask(__name__)

# Define all the features
features = [
    "acc_x_dashboard_left", "acc_y_dashboard_left", "acc_z_dashboard_left",
    "acc_x_above_suspension_left", "acc_y_above_suspension_left", "acc_z_above_suspension_left",
    "acc_x_below_suspension_left", "acc_y_below_suspension_left", "acc_z_below_suspension_left",
    "gyro_x_dashboard_left", "gyro_y_dashboard_left", "gyro_z_dashboard_left",
    "gyro_x_above_suspension_left", "gyro_y_above_suspension_left", "gyro_z_above_suspension_left",
    "gyro_x_below_suspension_left", "gyro_y_below_suspension_left", "gyro_z_below_suspension_left",
    "mag_x_dashboard_left", "mag_y_dashboard_left", "mag_z_dashboard_left",
    "mag_x_above_suspension_left", "mag_y_above_suspension_left", "mag_z_above_suspension_left",
    "temp_dashboard_left", "temp_above_suspension_left", "temp_below_suspension_left",
    "timestamp_gps_left", "latitude_left", "longitude_left", "speed_left",
    "acc_x_dashboard_right", "acc_y_dashboard_right", "acc_z_dashboard_right",
    "acc_x_above_suspension_right", "acc_y_above_suspension_right", "acc_z_above_suspension_right",
    "acc_x_below_suspension_right", "acc_y_below_suspension_right", "acc_z_below_suspension_right",
    "gyro_x_dashboard_right", "gyro_y_dashboard_right", "gyro_z_dashboard_right",
    "gyro_x_above_suspension_right", "gyro_y_above_suspension_right", "gyro_z_above_suspension_right",
    "gyro_x_below_suspension_right", "gyro_y_below_suspension_right", "gyro_z_below_suspension_right",
    "mag_x_dashboard_right", "mag_y_dashboard_right", "mag_z_dashboard_right",
    "mag_x_above_suspension_right", "mag_y_above_suspension_right", "mag_z_above_suspension_right",
    "temp_dashboard_right", "temp_above_suspension_right", "temp_below_suspension_right",
    "timestamp_gps_right", "latitude_right", "longitude_right", "speed_right"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract features from the form and convert to the appropriate data type
        feature_values = [float(request.form[feature]) for feature in features]
        features_array = np.array([feature_values])  # Convert list to numpy array for model
        model=joblib.load("model_.h5")
        # Predict using the model
        prediction = model.predict(features_array)
        if prediction ==0:
            res='Paved Road, Asphalt Road, No Speed Bump, Good Road Left, Good Road Right'
        elif prediction ==1:
            res='Paved Road, Asphalt Road, No Speed Bump, Regular Road Left, Regular Road Right'
        elif prediction ==2:
            res='Paved Road, Asphalt Road, No Speed Bump, Good Road Left, Regular Road Right'
        elif prediction ==3:
            res='Paved Road, Asphalt Road, No Speed Bump, Regular Road Left, Good Road Right'
        elif prediction ==4:
            res='Paved Road, Asphalt Road, Speed Bump Asphalt, Regular Road Left, Regular Road Right'
        elif prediction ==5:
            res='Unpaved Road, Dirt Road, No Speed Bump, Regular Road Left, Regular Road Right'
        elif prediction==6:
            res='Unpaved Road, Dirt Road, No Speed Bump, Regular Road Left, Bad Road Right'
        elif prediction==7:
            res='Unpaved Road, Dirt Road, No Speed Bump, Bad Road Left, Bad Road Right'
        elif prediction==8:
            res='Paved Road, Cobblestone Road, No Speed Bump, Bad Road Left, Bad Road Right'
        elif prediction==9:
            res='Paved Road, Cobblestone Road, No Speed Bump, Regular Road Left, Bad Road Right'
        elif prediction==10:
            res='Paved Road, Cobblestone Road, No Speed Bump, Regular Road Left, Regular Road Right'
        elif prediction==11:
            res='Paved Road, Cobblestone Road, No Speed Bump, Good Road Left, Regular Road Right'
        elif prediction==12:
            res='Paved Road, Cobblestone Road, No Speed Bump, Good Road Left, Good Road Right'
        elif prediction==13:
            res='Paved Road, Cobblestone Road, No Speed Bump, Regular Road Left, Good Road Right'
        elif prediction==14:
            res='Unpaved Road, Dirt Road, No Speed Bump, Bad Road Left, Regular Road Right'
        elif prediction==15:
            res='Paved Road, Cobblestone Road, No Speed Bump, Bad Road Left, Regular Road Right'
        elif prediction==16:
            res='Paved Road, Cobblestone Road, Speed Bump Cobblestone, Bad Road Left, Bad Road Right'
        elif prediction==17:
            res='Paved Road, Cobblestone Road, Speed Bump Cobblestone, Bad Road Left, Regular Road Right'
        elif prediction==18:
            res='Paved Road, Cobblestone Road, Speed Bump Cobblestone, Regular Road Left, Regular Road Right'
        elif prediction==19:
            res='Paved Road, Cobblestone Road, Speed Bump Cobblestone, Regular Road Left, Bad Road Right'
        elif prediction==20:
            res='Unpaved Road, Dirt Road, No Speed Bump, Good Road Left, Good Road Right'
        elif prediction==21:
            res='Unpaved Road, Dirt Road, No Speed Bump, Regular Road Left, Good Road Right'
        elif prediction==22:
            res='Unpaved Road, Dirt Road, No Speed Bump, Good Road Left, Regular Road Right'
        elif prediction==23:
            res='Paved Road, Asphalt Road, No Speed Bump, Bad Road Left, Bad Road Right'
        elif prediction==24:
            res='Paved Road, Asphalt Road, No Speed Bump, Bad Road Left, Regular Road Right'
        elif prediction==25:
            res='Paved Road, Asphalt Road, Speed Bump Asphalt, Regular Road Left, Good Road Right'
        elif prediction==26:
            res='Paved Road, Asphalt Road, Speed Bump Asphalt, Good Road Left, Good Road Right'
        elif prediction==27:
            res='Paved Road, Asphalt Road, No Speed Bump, Regular Road Left, Bad Road Right'
        elif prediction==28:
            res='Paved Road, Asphalt Road, No Speed Bump, Speed Bump Asphalt, Regular Road Left, Regular Road Right'
        
        # Render results template with the prediction result
        return render_template('results.html', prediction=res)
    return render_template('index.html', features=features)



Instrumentator().instrument(app).expose(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8005)

