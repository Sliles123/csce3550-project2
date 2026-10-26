"""Start the JWKS server: ``python main.py``.

The server listens on http://127.0.0.1:8080 and creates
``totally_not_my_privateKeys.db`` in the current directory.
"""

import logging

from jwks_server.server import run


def main() -> None:
    """Configure logging and run the server until Ctrl+C."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    run()


if __name__ == "__main__":  # pragma: no cover
    main()
