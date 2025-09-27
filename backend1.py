#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 09:13:29 2025

@author: angelinachen
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import Schema

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/providers")
def get_providers():
    providers = Schema.fetch_providers_from_db()
    return providers  # list of dicts, arrays as Python lists
