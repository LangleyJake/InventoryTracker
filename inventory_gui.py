#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import csv
from pathlib import Path

DATA_DIR = Path('data')
DATA_FILE = DATA_DIR / 'inventory.csv'

def load_rows():
    rows = []
    if DATA_FILE.exists():
        with open(DATA_FILE, newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f): rows.append(r)
    return rows

def save_rows(rows):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['name','sku','qty','price'])
        w.writeheader(); [w.writerow(r) for r in rows]

def add_item():
    name = name_var.get().strip(); sku = sku_var.get().strip(); qty = qty_var.get().strip(); price = price_var.get().strip() or '0'
    if not name or not sku or not qty.isdigit():
        messagebox.showerror('Error', 'Provide name, sku, numeric qty'); return
    rows = load_rows()
    if any(r['sku'].lower()==sku.lower() for r in rows):
        messagebox.showerror('Error', 'SKU already exists'); return
    rows.append({'name':name,'sku':sku,'qty':qty,'price':price}); save_rows(rows)
    refresh(); name_var.set(''); sku_var.set(''); qty_var.set(''); price_var.set('')

def refresh():
    for i in tree.get_children(): tree.delete(i)
    for r in load_rows(): tree.insert('', 'end', values=(r['sku'], r['name'], r['qty'], r['price']))

root = tk.Tk(); root.title('Inventory Tracker GUI')
frame = ttk.Frame(root, padding=10); frame.pack(fill='both', expand=True)
name_var = tk.StringVar(); sku_var = tk.StringVar(); qty_var = tk.StringVar(); price_var = tk.StringVar()
for i,(lbl,var) in enumerate([('Name',name_var),('SKU',sku_var),('Qty',qty_var),('Price',price_var)]):
    ttk.Label(frame,text=lbl).grid(row=0,column=i*2,sticky='w'); ttk.Entry(frame,textvariable=var,width=12).grid(row=0,column=i*2+1,padx=5)

ttk.Button(frame,text='Add',command=add_item).grid(row=0,column=8,padx=8)
cols=('SKU','Name','Qty','Price'); tree=ttk.Treeview(frame,columns=cols,show='headings',height=12)
for c in cols: tree.heading(c,text=c); tree.column(c,width=100)
tree.grid(row=1,column=0,columnspan=9,pady=10,sticky='nsew')
frame.rowconfigure(1,weight=1); frame.columnconfigure(1,weight=1)
refresh(); root.mainloop()
