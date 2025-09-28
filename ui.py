#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 10:42:19 2025

@author: angelinachen
"""
# ui.py
import streamlit as st
import schema  # your schema.py file

schema.insert_sample_providers()

st.set_page_config(page_title="Therapy Providers", layout="wide")
st.title("Therapy Providers Directory")

# --- Fetch providers from Snowflake via schema.py ---
providers = schema.fetch_providers_from_db()

# --- Handle empty database ---
if not providers:
    st.warning("No providers found in the database.")
    st.stop()

# --- Search input ---
search_term = st.text_input("Search providers (any field)")

# --- Filters ---
# City filter
cities = sorted(list(set(p["city"] for p in providers if p["city"])))
selected_city = st.sidebar.selectbox("City", ["All"] + cities)

# Price slider
price_mins = [p["price_min"] for p in providers if p.get("price_min") is not None]
price_maxs = [p["price_max"] for p in providers if p.get("price_max") is not None]

min_price = min(price_mins) if price_mins else 0
max_price = max(price_maxs) if price_maxs else 1000

if min_price == max_price:
    price_range = (min_price, max_price)
else:
    price_range = st.sidebar.slider(
        "Price Range",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )

# --- Filter and search ---
filtered_providers = []
for p in providers:
    # City filter
    if selected_city != "All" and p["city"] != selected_city:
        continue
    # Price filter
    if not (price_range[0] <= p["price_min"] <= price_range[1]):
        continue
    # Search filter (checks all fields)
    if search_term:
        term = search_term.lower()
        found = False
        for key, value in p.items():
            if isinstance(value, list):
                if any(term in str(v).lower() for v in value):
                    found = True
                    break
            elif value is not None:
                if term in str(value).lower():
                    found = True
                    break
        if not found:
            continue
    filtered_providers.append(p)

st.sidebar.markdown(f"**{len(filtered_providers)} providers found**")

# --- Display providers ---
for p in filtered_providers:
    st.markdown("---")
    st.subheader(p["name"])
    st.markdown(f"**Genders:** {', '.join(p['genders']) if p['genders'] else 'N/A'}")
    st.markdown(f"**Specialties:** {', '.join(p['specialties']) if p['specialties'] else 'N/A'}")
    st.markdown(f"**Therapy Types:** {', '.join(p['therapy_types']) if p['therapy_types'] else 'N/A'}")
    st.markdown(f"**Focus Tags:** {', '.join(p['focus_tags']) if p['focus_tags'] else 'N/A'}")
    st.markdown(f"**Insurances:** {', '.join(p['insurances']) if p['insurances'] else 'N/A'}")
    st.markdown(f"**Price:** ${p['price_min']} - ${p['price_max']}")
    st.markdown(f"**Location:** {p['city']}, {p['province']}")
    st.markdown(f"**Email:** {p['contact_email']}")
    st.markdown(f"**Phone:** {p['contact_phone']}")


providers = schema.fetch_providers_from_db()
print("Providers fetched:", providers)  
