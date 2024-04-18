from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from domain.aggregated_data import AggregatedData
import config
from typing import List


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str
    ) -> None:
        self.data_is_reading = False
        self.acc_line_number = 0
        self.gps_line_number = 0
        self.park_line_number = 0
        self.accelerometer_file = accelerometer_filename
        self.gps_file = gps_filename
        self.parking_file = parking_filename

        self.accelerometer_data = self._read_file(self.accelerometer_file)
        self.gps_data = self._read_file(self.gps_file)
        self.parking_data = self._read_file(self.parking_file)

    def _read_file(self, filename: str) -> List[str]:
        with open(filename, 'r') as file:
            entries = [line.rstrip() for line in file]
            return entries[1:] if len(entries) > 1 else []

    def read(self) -> AggregatedData:
        data = AggregatedData(
            Accelerometer(1, 2, 3),
            Gps(4, 5),
            Parking(20, Gps(4, 5)),
            datetime.now(),
            config.USER_ID,
        )

        if self.data_is_reading:
            self.acc_line_number %= len(self.accelerometer_data)
            self.gps_line_number %= len(self.gps_data)
            self.park_line_number %= len(self.parking_data)

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
