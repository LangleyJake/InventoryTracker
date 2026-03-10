#!/usr/bin/env python3
import argparse, csv, sys
from dataclasses import dataclass, asdict
from pathlib import Path

DATA_DIR = Path('data')
DATA_FILE = DATA_DIR / 'inventory.csv'

@dataclass
class Item:
    name: str
    sku: str
    qty: int
    price: float = 0.0

def load_items():
    items = []
    if DATA_FILE.exists():
        with open(DATA_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                items.append(Item(r['name'], r['sku'], int(r['qty']), float(r.get('price', 0) or 0)))
    return items

def save_items(items):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name','sku','qty','price'])
        writer.writeheader()
        for it in items:
            writer.writerow(asdict(it))

def find_index(items, sku):
    for i, it in enumerate(items):
        if it.sku.lower() == sku.lower():
            return i
    return -1

def cmd_add(args):
    items = load_items()
    if find_index(items, args.sku) != -1:
        sys.exit(f"SKU {args.sku} already exists")
    items.append(Item(args.name, args.sku, args.qty, args.price or 0.0))
    save_items(items)
    print('Added:', args.sku)

def cmd_list(_):
    items = load_items()
    if not items:
        print('No items yet.')
        return
    for it in items:
        print(f"{it.sku:10} | {it.name:20} | qty={it.qty:4} | ${it.price:0.2f}")

def cmd_update(args):
    items = load_items()
    idx = find_index(items, args.sku)
    if idx == -1:
        sys.exit('SKU not found')
    it = items[idx]
    if args.name is not None:
        it.name = args.name
    if args.qty is not None:
        it.qty = args.qty
    if args.price is not None:
        it.price = args.price
    items[idx] = it
    save_items(items)
    print('Updated:', args.sku)

def cmd_remove(args):
    items = load_items()
    idx = find_index(items, args.sku)
    if idx == -1:
        sys.exit('SKU not found')
    items.pop(idx)
    save_items(items)
    print('Removed:', args.sku)

def cmd_search(args):
    items = load_items()
    q = (args.query or '').lower()
    for it in items:
        if q in it.name.lower() or q in it.sku.lower():
            print(f"{it.sku:10} | {it.name:20} | qty={it.qty:4} | ${it.price:0.2f}")

def cmd_export(args):
    items = load_items()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name','sku','qty','price'])
        writer.writeheader()
        for it in items:
            writer.writerow(asdict(it))
    print('Exported to', out)

def build_parser():
    p = argparse.ArgumentParser(description='Inventory Tracker CLI')
    sub = p.add_subparsers(required=True)

    ap = sub.add_parser('add'); ap.add_argument('--name', required=True); ap.add_argument('--sku', required=True); ap.add_argument('--qty', type=int, required=True); ap.add_argument('--price', type=float); ap.set_defaults(func=cmd_add)
    lp = sub.add_parser('list'); lp.set_defaults(func=cmd_list)
    up = sub.add_parser('update'); up.add_argument('--sku', required=True); up.add_argument('--name'); up.add_argument('--qty', type=int); up.add_argument('--price', type=float); up.set_defaults(func=cmd_update)
    rp = sub.add_parser('remove'); rp.add_argument('--sku', required=True); rp.set_defaults(func=cmd_remove)
    sp = sub.add_parser('search'); sp.add_argument('--query', required=True); sp.set_defaults(func=cmd_search)
    ep = sub.add_parser('export'); ep.add_argument('--out', required=True); ep.set_defaults(func=cmd_export)
    return p

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
