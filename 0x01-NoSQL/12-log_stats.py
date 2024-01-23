#!/usr/bin/env python3
"""
module for Python script that provides some stats about
Nginx logs stored in MongoDB
"""

from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["logs"]

col = db["nginx"]

total = db.command("dbstats")["objects"]

print(f"{total} logs")

print("Methods:")

methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

for method in methods:
    count = col.count_documents({"method": method})
    print(f"\t{method}: {count}")

status = col.count_documents({"method": "GET", "path": "/status"})

print(f"{status} status check")
