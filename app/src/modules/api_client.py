import os
import requests
import streamlit as st


API_BASE_URLS = [
    os.getenv("PIN_API_BASE_URL"),
    "http://api:4000",
    "http://web-api:4000",
    "http://localhost:4000",
    "http://127.0.0.1:4000",
]


def _iter_base_urls():
    for base_url in API_BASE_URLS:
        if base_url:
            yield base_url.rstrip("/")


def _request(method, path: str, body: dict | None = None, params: dict | None = None):
    last_error = None
    for base_url in _iter_base_urls():
        url = f"{base_url}{path}"
        try:
            response = requests.request(method, url, json=body, params=params, timeout=8)
            response.raise_for_status()
            return response.json(), None
        except requests.RequestException as exc:
            last_error = str(exc)
    return None, last_error


def api_get(path: str, params: dict | None = None):
    """Small helper to keep API calls consistent across pages."""
    return _request("GET", path, params=params)


def api_post(path: str, body: dict):
    return _request("POST", path, body=body)


def api_put(path: str, body: dict):
    return _request("PUT", path, body=body)


def api_delete(path: str, body: dict | None = None):
    return _request("DELETE", path, body=body)


def show_api_error(err: str):
    st.error("Could not connect to API or request failed.")
    st.caption(err)
