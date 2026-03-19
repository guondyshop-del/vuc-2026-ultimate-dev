"""
VUC-2026 Pytest Configuration
Shared fixtures and async test setup
"""

import asyncio
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark test as async")


@pytest.fixture(scope="session")
def event_loop_policy():
    return asyncio.DefaultEventLoopPolicy()
