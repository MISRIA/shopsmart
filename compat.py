import sys
import importlib.metadata

if sys.version_info < (3, 10):
    try:
        from importlib_metadata import packages_distributions
        importlib.metadata.packages_distributions = packages_distributions
        print("DEBUG: Monkeypatched importlib.metadata.packages_distributions for Python < 3.10")
    except ImportError:
        print("DEBUG: importlib-metadata not found, could not monkeypatch.")
