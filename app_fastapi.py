import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import pandas as pd
import pickle

app = FastAPI()
model = pickle.load(open("flight_rf.pkl", "rb"))

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory = Path(__file__).parent.absolute() / "static"),
    name = "static",
)

@app.get("/", response_class=HTMLResponse)
def get_home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
def get_prediction(request: Request, Dep_Time: str = Form(...), Arrival_Time: str = Form(...), stops: int = Form(...), airline: str = Form(...), Source: str = Form(...), Destination: str = Form(...)):
    # print(Dep_Time, Arrival_Time, stops, airline, Source, Destination)

    # Date_of_Journey
    Journey_day = int(pd.to_datetime(Dep_Time, format="%Y-%m-%dT%H:%M").day)
    Journey_month = int(pd.to_datetime(Dep_Time, format ="%Y-%m-%dT%H:%M").month)
    # print("Journey Date : ",Journey_day, Journey_month)

    # Departure
    Dep_hour = int(pd.to_datetime(Dep_Time, format ="%Y-%m-%dT%H:%M").hour)
    Dep_min = int(pd.to_datetime(Dep_Time, format ="%Y-%m-%dT%H:%M").minute)
    # print("Departure : ",Dep_hour, Dep_min)

    # Arrival
    Arrival_hour = int(pd.to_datetime(Arrival_Time, format ="%Y-%m-%dT%H:%M").hour)
    Arrival_min = int(pd.to_datetime(Arrival_Time, format ="%Y-%m-%dT%H:%M").minute)
    # print("Arrival : ", Arrival_hour, Arrival_min)

    # Duration
    dur_hour = abs(Arrival_hour - Dep_hour)
    dur_min = abs(Arrival_min - Dep_min)
    # print("Duration : ", dur_hour, dur_min)

    # Total Stops
    Total_stops = stops
    # print(Total_stops)

    # Airline
    Jet_Airways = 0
    IndiGo = 0
    Air_India = 0
    Multiple_carriers = 0
    SpiceJet = 0
    Vistara = 0
    GoAir = 0
    Multiple_carriers_Premium_economy = 0
    Jet_Airways_Business = 0
    Vistara_Premium_economy = 0
    Trujet = 0

    if(airline=='Jet Airways'):
        Jet_Airways = 1
    elif (airline=='IndiGo'):
        IndiGo = 1
    elif (airline=='Air India'):
        Air_India = 1
    elif (airline=='Multiple carriers'):
        Multiple_carriers = 1
    elif (airline=='SpiceJet'):
        SpiceJet = 1
    elif (airline=='Vistara'):
        Vistara = 1
    elif (airline=='GoAir'):
        GoAir = 1
    elif (airline=='Multiple carriers Premium economy'):
        Multiple_carriers_Premium_economy = 1
    elif (airline=='Jet Airways Business'):
        Jet_Airways_Business = 1
    elif (airline=='Vistara Premium economy'):
        Vistara_Premium_economy = 1   
    elif (airline=='Trujet'):
        Trujet = 1

    # print(Jet_Airways,
    #     IndiGo,
    #     Air_India,
    #     Multiple_carriers,
    #     SpiceJet,
    #     Vistara,
    #     GoAir,
    #     Multiple_carriers_Premium_economy,
    #     Jet_Airways_Business,
    #     Vistara_Premium_economy,
    #     Trujet)

    # Source
    # Banglore = 0 (not in column)
    s_Delhi = 0
    s_Kolkata = 0
    s_Mumbai = 0
    s_Chennai = 0

    if (Source == 'Delhi'):
        s_Delhi = 1
    elif (Source == 'Kolkata'):
        s_Kolkata = 1
    elif (Source == 'Mumbai'):
        s_Mumbai = 1
    elif (Source == 'Chennai'):
        s_Chennai = 1

    # print(s_Delhi,
    #     s_Kolkata,
    #     s_Mumbai,
    #     s_Chennai)

    # Destination
    # Banglore = 0 (not in column)
    d_Cochin = 0
    d_Delhi = 0
    d_New_Delhi = 0
    d_Hyderabad = 0
    d_Kolkata = 0
    if (Destination == 'Cochin'):
        d_Cochin = 1
    elif (Destination == 'Delhi'):
        d_Delhi = 1
    elif (Destination == 'New_Delhi'):
        d_New_Delhi = 1
    elif (Destination == 'Hyderabad'):
        d_Hyderabad = 1
    elif (Destination == 'Kolkata'):
        d_Kolkata = 1

    # print(
    #     d_Cochin,
    #     d_Delhi,
    #     d_New_Delhi,
    #     d_Hyderabad,
    #     d_Kolkata
    # )
    
    column_names  = ['Total_Stops', 'Journey_day', 'Journey_month', 'Dep_hour',
   'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours',
   'Duration_mins', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
   'Airline_Jet Airways', 'Airline_Jet Airways Business',
   'Airline_Multiple carriers',
   'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
   'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
   'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
   'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
   'Destination_Kolkata', 'Destination_New Delhi']
    
    user_data = [
        Total_stops,
        Journey_day,
        Journey_month,
        Dep_hour,
        Dep_min,
        Arrival_hour,
        Arrival_min,
        dur_hour,
        dur_min,
        Air_India,
        GoAir,
        IndiGo,
        Jet_Airways,
        Jet_Airways_Business,
        Multiple_carriers,
        Multiple_carriers_Premium_economy,
        SpiceJet,
        Trujet,
        Vistara,
        Vistara_Premium_economy,
        s_Chennai,
        s_Delhi,
        s_Kolkata,
        s_Mumbai,
        d_Cochin,
        d_Delhi,
        d_Hyderabad,
        d_Kolkata,
        d_New_Delhi
    ]

    # create a dataframe from user data
    new_data = pd.DataFrame([user_data], columns = column_names)
    # get the predicted price from the trained model
    prediction = model.predict(new_data)
    # predicted result
    output = round(prediction[0], 2)

    return templates.TemplateResponse("index.html", {"request": request, "prediction_text": "Your flight price is Rs. {}".format(output)})

if __name__ == "__main__":
    uvicorn.run(app)
