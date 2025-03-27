
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run

from typing import Optional

from src.constants import APP_HOST, APP_PORT
from src.pipline.prediction_pipeline import USvisaData, USvisaClassifier
from src.pipline.training_pipeline import TrainPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.no_of_adults: Optional[str] = None
        self.no_of_children: Optional[str] = None
        self.no_of_weekend_nights: Optional[str] = None
        self.no_of_week_nights: Optional[str] = None
        self.type_of_meal_plan: Optional[str] = None
        self.required_car_parking_space: Optional[str] = None
        self.room_type_reserved: Optional[str] = None
        self.lead_time: Optional[str] = None
        self.arrival_year: Optional[str] = None
        self.arrival_month: Optional[str] = None
        self.arrival_date: Optional[str] = None
        self.market_segment_type: Optional[str] = None
        self.repeated_guest: Optional[str] = None
        self.no_of_previous_cancellations: Optional[str] = None
        self.no_of_previous_bookings_not_canceled: Optional[str] = None
        self.avg_price_per_room: Optional[str] = None
        self.no_of_special_requests: Optional[str] = None
        

    async def get_usvisa_data(self):
        form = await self.request.form()
        self.no_of_adults = form.get("no_of_adults")
        self.no_of_children = form.get("no_of_children")
        self.no_of_weekend_nights = form.get("no_of_weekend_nights")
        self.no_of_week_nights = form.get("no_of_week_nights")
        self.type_of_meal_plan = form.get("type_of_meal_plan")
        self.required_car_parking_space = form.get("required_car_parking_space")
        self.room_type_reserved = form.get("room_type_reserved")
        self.lead_time = form.get("lead_time")
        self.arrival_year = form.get("arrival_year")
        self.arrival_month = form.get("arrival_month")
        self.arrival_date = form.get("arrival_date")
        self.market_segment_type = form.get("market_segment_type")
        self.repeated_guest = form.get("repeated_guest")
        self.no_of_previous_cancellations = form.get("no_of_previous_cancellations")
        self.no_of_previous_bookings_not_canceled = form.get("no_of_previous_bookings_not_canceled")
        self.avg_price_per_room = form.get("avg_price_per_room")
        self.no_of_special_requests = form.get("no_of_special_requests")
        

@app.get("/", tags=["authentication"])
async def index(request: Request):

    return templates.TemplateResponse(
            "usvisa.html",{"request": request, "context": "Rendering"})


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_usvisa_data()
        
        usvisa_data = USvisaData(
                                no_of_adults= form.no_of_adults,
                                no_of_children = form.no_of_children,
                                no_of_weekend_nights = form.no_of_weekend_nights,
                                no_of_week_nights = form.no_of_week_nights,
                                type_of_meal_plan=form.type_of_meal_plan, 
                                required_car_parking_space= form.required_car_parking_space,
                                room_type_reserved= form.room_type_reserved,
                                lead_time = form.lead_time,
                                arrival_year= form.arrival_year,
                                arrival_month= form.arrival_month,
                                arrival_date= form.arrival_date,
                                market_segment_type= form.market_segment_type,
                                repeated_guest= form.repeated_guest,
                                no_of_previous_cancellations= form.no_of_previous_cancellations,
                                no_of_previous_bookings_not_canceled= form.no_of_previous_bookings_not_canceled,
                                avg_price_per_room= form.avg_price_per_room,
                                no_of_special_requests= form.no_of_special_requests,
                                
                                )
        
        usvisa_df = usvisa_data.get_usvisa_input_data_frame()

        model_predictor = USvisaClassifier()

        value = model_predictor.predict(dataframe=usvisa_df)[0]

        status = None
        if value == 0:
            status = "Not_Canceled"
        else:
            status = "Canceled"

        return templates.TemplateResponse(
            "usvisa.html",
            {"request": request, "context": status},
        )
        
    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)