import logging
import os

try:
    from tqdm.auto import tqdm

    class TqdmLoggingHandler(logging.Handler):
        def __init__(self, level=logging.INFO):
            super().__init__(level)

        def emit(self, record):
            try:
                msg = self.format(record)

                tqdm.write(msg)
                self.flush()
            except Exception:
                self.handleError(record)

    TQDM_IMPORTED = True
except ImportError:
    TQDM_IMPORTED = False


def setup_logging(loglevel):
    if loglevel is None:
        loglevel = os.environ.get("WEBUI_LOG_LEVEL")

    loghandlers = []

    if TQDM_IMPORTED:
        loghandlers.append(TqdmLoggingHandler())

    if loglevel:
        log_level = getattr(logging, loglevel.upper(), None) or logging.INFO

        logging.basicConfig(
            format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%d-%m-%Y %H:%M:%S",
            level=log_level,
            handlers=loghandlers,
        )
