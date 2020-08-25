import tensorflow as tf
import pandas as pd
import numpy as np
import os
import datetime

def main():

    # PARAMETERS
    # Past days_input days to predict next days_output days
    minutes_15_input = 24 #6h
    minutes_15_output = 4 #1h
    DEV_LIST = ['sm45']

    today = datetime.date.today().strftime("%d %m %Y").split(" ")

    filename = today[1] + "_" + today[2] + "_" + "sm45.csv"

    filename_path = 'csv/' + today[1] + "_" + today[2]

    #date_split = '2020-02-20 06:00:00' #Treino até fim de janeiro, teste a partir disso

    # Read dataset 
    dataset = pd.read_csv(os.path.join(filename_path,filename), parse_dates=['time'], index_col=['time'])
    dataset_15_minutes = dataset #[:'2020-03-01 14:00:00':]

    model_path = os.path.join(os.getcwd(), 'model')
    # Load Model
    model = tf.keras.models.load_model(model_path)


    data_valid = dataset_15_minutes.iloc[-24*24:]
    fator_norm = np.nanmax(data_valid.values)
    
    X_valid = data_valid.values / fator_norm
    X_valid = X_valid.reshape((24,minutes_15_input,1))

    y_pred = model.predict(X_valid)
    y_pred = y_pred * fator_norm

    # Get the last 2 hours
    last_2_hours = data_valid.tail(2*minutes_15_output)

    plot_values = last_2_hours.tail(2*minutes_15_output).reset_index()

    # Create time for the 1 hour ahead
    start_time = plot_values['time'][len(plot_values) - 1] + datetime.timedelta(minutes=15)
    end_time =  plot_values['time'][len(plot_values) - 1] + datetime.timedelta(minutes=60)
    # Store the 1 hour prediction ahead 
    values_pred = y_pred[-1]

    # Create another dataframe with the predictions
    d = {'time': pd.date_range(start = start_time, end = end_time,freq='15min'),'Value':values_pred.T}
    df = pd.DataFrame(data=d)

    # Concat the last 2 hours + 1 hour prediction ahead
    #plot_values_concat = pd.concat([plot_values, df]).reset_index()

    # Save to CSV
    df.to_csv("ceos_inference.csv", index=False)

if __name__ == "__main__":
    main()
