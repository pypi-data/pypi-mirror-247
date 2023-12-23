import os
import pytest
from dldock import dldock

SHARED_LIB_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'shared_lib')

@pytest.fixture(scope='function')
def setup():
    shared_lib = 'libplus.so'
    shared_lib_path = os.path.join(SHARED_LIB_DIR, shared_lib)
    dl = dldock.DlDock(shared_lib_path)
    yield dl
    dl.unload()

def test_init(setup):
    dl = setup
    assert None != dl.shared_lib()
    
def test_unload(setup):
    dl = setup
    assert 0 == dl.unload()

def test_reload(setup):
    dl = setup
    dl.reload()
    assert 0 == dl.unload()
