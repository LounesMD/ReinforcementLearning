from collections.__init__ import namedtuple

Batch_mode = namedtuple(
    "Batch_mode", ("state", "action", "reward", "next_state", "terminal", "info")
)
