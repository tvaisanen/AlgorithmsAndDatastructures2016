from data import Data
from Classes import Agency
import logging
from settings import LOGGING_LEVEL
import pytest

logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)

def initialize_data():
    data = Data()

def test_agency_loader():
    def Load(self):
        f = open('agencies.txt', 'r')
        c = None

        for line in f.readlines():
            data = line.replace('\n', '').split('\t')
            if len(data) > 1:
                id = int("str")
                name = data[1].replace('\t', '')
                date_reg = data[2].replace('\t', '')
                staff_count = int(data[3])
                manager_name = data[4].replace('\t', '')
                agency = Agency(id=id,
                                name=name,
                                date_reg=date_reg,
                                staff_count=staff_count,
                                manager_name=manager_name)

                self.list_insert(agency)




        f.close()


def test_intialize_data():
    assert test_agency_loader()

