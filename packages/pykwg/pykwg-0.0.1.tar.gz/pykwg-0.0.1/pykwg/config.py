import os


class Config:
    def __init__(self):
        self.base_address = os.environ.get(
            "KWG_BASE_ADDRESS", "http://stko-kwg.geog.ucsb.edu/"
        )
