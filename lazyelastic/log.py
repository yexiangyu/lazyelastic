import logging

LOG = logging.getLogger("lazyelastic")

CHANNEL = logging.StreamHandler()

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

CHANNEL.setFormatter(FORMATTER)
LOG.addHandler(CHANNEL)

LOG.setLevel(logging.INFO)
LOG.propagate = False
