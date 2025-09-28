#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI for Therapy Providers Directory using Streamlit and FastAPI backend
"""
import streamlit as st
import requests

st.set_page_config(page_title="Therapy Providers", layout="wide")
st.title("Therapy Providers Directory")

# --- Backend URL ---
backend_url = "http://127.0.0.1:8000/search/providers"

try:
    occ_response = requests.get("http://127.0.0.1:8000/unique/occupations")
    occ_response.raise_for_status()
    occupations = occ_response.json()
except Exception as e:
    st.error(f"Error fetching occupations: {e}")
    occupations = []

# --- Sidebar filters ---
occupation = st.sidebar.selectbox("Occupation", ["All"] + occupations)
specialty = st.sidebar.text_input("Specialty")
insurance = st.sidebar.text_input("Insurance")
gender = st.sidebar.text_input("Gender Identity")
services = st.sidebar.text_input("Services Offered")
session = st.sidebar.text_input("Session Offering Options")
rate = st.sidebar.slider("Hourly Rate", 0, 500, 10)
city_input = st.sidebar.text_input("City")  # Allow free-text input
limit = st.sidebar.slider("Max providers to fetch", 1, 100, 50)

# --- Prepare query parameters ---
params = {
    "occupation": occupation if occupation != "All" else None,
    "specialty": specialty if specialty else None,
    "insurance": insurance if insurance else None,
    "session": session if session else None,
    "gender": gender if gender else None,
    "services": services if services else None,
    "rate": rate if rate >= 0 else None,
    "city": city_input if city_input else None,
    "limit": limit
}

print(params)

# --- Fetch providers from backend ---
try:
    response = requests.get(backend_url, params=params)
    response.raise_for_status()
    providers = response.json()
except Exception as e:
    st.error(f"Error fetching providers from backend: {e}")
    st.stop()

# --- Handle empty results ---
if not providers:
    st.warning("No providers found for your search criteria.")
    st.stop()

# --- Search input for client-side filtering ---
search_term = st.text_input("Search providers (any field)")

# --- Filter based on search term ---
filtered_providers = []
for p in providers:
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
    st.subheader(f"{p.get('FIRST_NAME', 'N/A')} {p.get('LAST_NAME', 'N/A')}")
    st.markdown(f"**Role:** {p.get('PROVIDER_ROLE', 'N/A')}")
    st.markdown(f"**Gender Identity:** {p.get('GENDER_IDENTITY', 'N/A')}")
    st.markdown(f"**Insurance:** {p.get('INSURANCE', 'N/A')}")
    st.markdown(f"**Hourly Rate:** ${p.get('HOURLY_RATE', 'N/A')}")
    st.markdown(f"**Session Options:** {p.get('SESSION_OPTIONS', 'N/A')}")
    st.markdown(f"**Specialized Support:** {p.get('SPECIALIZED_SUPPORT', 'N/A')}")
    st.markdown(f"**Services Offered:** {p.get('SERVICES_OFFERED', 'N/A')}")
    st.markdown(f"**Registration Number:** {p.get('REGISTRATION_NUMBER', 'N/A')}")
    st.markdown(f"**Email:** {p.get('EMAIL', 'N/A')}")
    st.markdown(f"**Address:** {p.get('ADDRESS', 'N/A')}")