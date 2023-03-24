from .table_mock import MockTable
import sys, os, json
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from models import MysfitModel
model = MysfitModel()

mock_table = MockTable()

def test_list_all():
    resp = model.list_items(table=mock_table)
    assert len(resp) == 12

def test_create():
    resp = model.create()

def test_get():
    resp = model.get('None','None', table=mock_table)
    assert resp.items()


    

  