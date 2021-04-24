# contents of test_module.py with source code and the test
from pathlib import Path

import io
import contextlib

class MockWebsite:
    def __init__(self, html):
        self.reader = io.BytesIO(bytes(html, 'utf-8'))

    def read(self):
        return self.reader.read()

html = "<div></div>"
website = MockWebsite(html)
website.read().decode("utf-8")

@contextlib.contextmanager
def mockurl():
    html = "<div></div>"
    yield MockWebsite(html)

with open(mockurl()) as o:
    print(o)

###



@contextlib.contextmanager
def mockurl(remote_url, timeout=None):
    yield MockURL()

def mockurl_builder(tlscontext=None):
    mock_opener = type('MockOpener', (object,), {})()
    mock_opener.open = mockurl
    return mock_opener

class MockURL:
    def __init__(self):
        self.reader = io.BytesIO(b"a" * real_length)

    def info(self):
        return {"Content-Length": str(report_length)}

    def read(self, length=None):
        return self.reader.read(length)

with open(mockurl_builder()) as o:
    print(o)

####


def getssh():
    """Simple function to return expanded homedir ssh path."""
    return Path.home() / ".ssh"


def test_getssh(monkeypatch):
    # mocked return function to replace Path.home
    # always return '/abc'
    def mockreturn():
        return Path("/abc")

    # Application of the monkeypatch to replace Path.home
    # with the behavior of mockreturn defined above.
    monkeypatch.setattr(Path, "home", mockreturn)

    # Calling getssh() will use mockreturn in place of Path.home
    # for this test with the monkeypatch.
    x = getssh()
    assert x == Path("/abc/.ssh")
