from typing import Any, Dict

from sphinx.application import Sphinx

from .authors import setup as setup_authors
from .inject import setup as setup_inject


def setup(app: Sphinx) -> Dict[str, Any]:
    setup_inject(app)
    setup_authors(app)
    return {"parallel_read_safe": True}


__all__ = ["setup"]
