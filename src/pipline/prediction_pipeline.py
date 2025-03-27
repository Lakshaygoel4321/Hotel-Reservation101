import os
import sys

import numpy as np
import pandas as pd
from src.entity.config_entity import USvisaPredictorConfig
from src.entity.s3_estimator import USvisaEstimator
from src.exception import USvisaException
from src.logger import logging
from src.utils.main_utils import read_yaml_file
from pandas import DataFrame


class USvisaData:
    def __init__(self,
                no_of_adults,
                no_of_children,
                no_of_weekend_nights,
                no_of_week_nights,
                type_of_meal_plan,
                required_car_parking_space,
                room_type_reserved,
                lead_time,
                arrival_year,
                arrival_month,
                arrival_date,
                market_segment_type,
                repeated_guest,
                no_of_previous_cancellations,
                no_of_previous_bookings_not_canceled,
                avg_price_per_room,
                no_of_special_requests



                
                ):
        """
        Usvisa Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.no_of_adults = no_of_adults
            self.no_of_children = no_of_children
            self.no_of_weekend_nights = no_of_weekend_nights
            self.no_of_week_nights = no_of_week_nights
            self.type_of_meal_plan = type_of_meal_plan
            self.required_car_parking_space = required_car_parking_space
            self.room_type_reserved = room_type_reserved
            self.lead_time = lead_time
            self.arrival_year = arrival_year
            self.arrival_month = arrival_month
            self.arrival_date = arrival_date
            self.market_segment_type = market_segment_type
            self.repeated_guest = repeated_guest
            self.no_of_previous_cancellations = no_of_previous_cancellations
            self.no_of_previous_bookings_not_canceled = no_of_previous_bookings_not_canceled
            self.avg_price_per_room = avg_price_per_room
            self.no_of_special_requests = no_of_special_requests

            

        except Exception as e:
            raise USvisaException(e, sys) from e

    def get_usvisa_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from USvisaData class input
        """
        try:
            
            usvisa_input_dict = self.get_usvisa_data_as_dict()
            return DataFrame(usvisa_input_dict)
        
        except Exception as e:
            raise USvisaException(e, sys) from e


    def get_usvisa_data_as_dict(self):
        """
        This function returns a dictionary from USvisaData class input 
        """
        logging.info("Entered get_usvisa_data_as_dict method as USvisaData class")

        try:
            input_data = {
                "no_of_adults": [self.no_of_adults],
                "no_of_children": [self.no_of_children],
                "no_of_weekend_nights": [self.no_of_weekend_nights],
                "no_of_week_nights": [self.no_of_week_nights],
                "type_of_meal_plan": [self.type_of_meal_plan],
                "required_car_parking_space": [self.required_car_parking_space],
                "room_type_reserved": [self.room_type_reserved],
                "lead_time": [self.lead_time],
                "arrival_year": [self.arrival_year],
                "arrival_month": [self.arrival_month],
                "arrival_date": [self.arrival_date],
                "market_segment_type": [self.market_segment_type],
                "repeated_guest": [self.repeated_guest],
                "no_of_previous_cancellations": [self.no_of_previous_cancellations],
                "no_of_previous_bookings_not_canceled": [self.no_of_previous_bookings_not_canceled],
                "avg_price_per_room": [self.avg_price_per_room],
                "no_of_special_requests": [self.no_of_special_requests],
                
            }

            logging.info("Created usvisa data dict")

            logging.info("Exited get_usvisa_data_as_dict method as USvisaData class")

            return input_data

        except Exception as e:
            raise USvisaException(e, sys) from e

class USvisaClassifier:
    def __init__(self,prediction_pipeline_config: USvisaPredictorConfig = USvisaPredictorConfig(),) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            # self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise USvisaException(e, sys)


    def predict(self, dataframe) -> str:
        """
        This is the method of USvisaClassifier
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of USvisaClassifier class")
            model = USvisaEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result =  model.predict(dataframe)
            
            return result
        
        except Exception as e:
            raise USvisaException(e, sys)