# app/__init__.py
# This file marks the app folder as a package.

from .app import app, convert_amount, SUPPORTED_CURRENCIES, RATES

__all__ = ["app", "convert_amount", "SUPPORTED_CURRENCIES", "RATES"]
