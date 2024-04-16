from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str
    ) -> None:
        
        self.accelerometer_file = accelerometer_filename
        self.gps_file = gps_filename
        self.parking_file = parking_filename

        with open(self.accelerometer_file) as file:
            entries = [line.rstrip() for line in file]
            entries = entries[1:]
            self.accelerometer_data = entries

        with open(self.gps_file) as file:
            entries = [line.rstrip() for line in file]
            entries = entries[1:]
            self.gps_data = entries

        with open(self.parking_file) as file:
            entries = [line.rstrip() for line in file]
            entries = entries[1:] 
            self.parking_data = entries

    def read(self) -> AggregatedData:
        data = AggregatedData(
            Accelerometer(1, 2, 3),
            Gps(4, 5),
            Parking(20, Gps(4, 5)),
            datetime.now(),
            config.USER_ID,
        )

        if self.data_is_reading:
            if self.acc_line_number > len(self.accelerometer_data) - 1:
                self.acc_line_number = 0
                
            if self.gps_line_number > len(self.gps_data) - 1:
                self.gps_line_number = 0
            
            if self.park_line_number > len(self.parking_data) - 1:
                self.park_line_number = 0

            acceleration = self.accelerometer_data[self.acc_line_number].split(',')
            x, y, z = acceleration
            data.accelerometer = Accelerometer(x, y, z)

            gps = self.gps_data[self.gps_line_number].split(',')
            lat_gps, long_gps = gps
            data.gps = Gps(long_gps, lat_gps)

            parking = self.parking_data[self.park_line_number].split(',')
            long_park, lat_park, empty_count = parking
            data.parking = Parking(empty_count, Gps(long_park, lat_park))
            
            self.acc_line_number += 1
            self.gps_line_number += 1
            self.park_line_number += 1
        
        return data
    
    def startReading(self, *args, **kwargs):
        self.data_is_reading = True
        self.acc_line_number = 0
        self.gps_line_number = 0
        self.park_line_number = 0

    def stopReading(self, *args, **kwargs):
        self.data_is_reading = False