from .get_year_results_renting_management import Results
from .download_bill_photo import Photo
from .get_sum_price_bills import PriceBill
# from .generate_report import generate_report
from .generate_csv import AssetCsv
from .get_bill_files import BillFiles
from .generate_bill_for_rent import BillRent
from .get_sum_price_rents import PriceRent
from .get_all_days_rented import SumAllDaysRented
from .generate_bills_csv_details import BillsCsvDetailed

__all__ = [
    Results,
    Photo,
    PriceBill,
    # generate_report,
    AssetCsv,
    BillFiles,
    BillRent,
    PriceRent,
    SumAllDaysRented,
    BillsCsvDetailed,
]