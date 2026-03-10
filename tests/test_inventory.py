import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('inventory','src/inventory_tracker.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_add(tmp_path):
    mod.DATA_DIR = tmp_path / 'data'
    mod.DATA_FILE = mod.DATA_DIR / 'inventory.csv'
    class A: pass
    a=A(); a.name='USB'; a.sku='USB-1'; a.qty=2; a.price=1.0
    mod.cmd_add(a)
    assert mod.load_items()[0].sku == 'USB-1'
