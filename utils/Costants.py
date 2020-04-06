import enum

DFS_ROOT = "hdfs://localhost:9000/"
PARQUET_FILE_CARGO = DFS_ROOT + "tesi_siremar/siremar_cargo.parquet"
PARQUET_FILE_PRENOTATION = DFS_ROOT + "tesi_siremar/siremar_prenotation.parquet"
ASSETS = "./assets/"
IMAGE_INFO = {
    "dpi_monitor": 0
}
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1080
IMAGE_WIDTH = 1640
IMAGE_HEIGHT = 764
VERSION = "0.0.1"
APP_TITLE = "Siremar Cargo analysis"
PLACEHOLDER_PATH = "./assets/app_images/placeholder.jpg"
TEMP_IMAGE_STATISTICS = "./assets/app_images/statistics.jpg"
DATAFRAME_APPLICATION = {
    "dataframe_prenotazioni": None,
    "dataframe_cargo": None,
    "dataframe_max_mq_occupati": None,
    "dataframe_tot_mq_occupati": None
}


class levelLog(enum.Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

HOME_SCREEN = 0
ANALYTICS_SCREEN = 1