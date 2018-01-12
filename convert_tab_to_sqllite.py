#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import os

import unicodecsv

os.remove('philosopherz.db')
con = sqlite3.connect('philosopherz.db')
cur = con.cursor()
cur.execute("CREATE TABLE philosopherz(philosopher TEXT, quote BLOB)")

with open('philosopherz.txt', 'rb') as input_file:
    reader = unicodecsv.reader(input_file, delimiter="\t")
    data = [row for row in reader]
    # print(data)

cur.executemany("INSERT INTO philosopherz (philosopher, quote) VALUES (?, ?);", data)
con.commit()