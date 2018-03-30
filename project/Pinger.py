
from subprocess import call, DEVNULL


class Pinger:

    def ping(self, hostname: str) -> int:
        """Returns an int representing the ping result

        Return codes:
        - 0: success
        - 1: not reply
        - 2: error
        """
        return 2


class OsPinger(Pinger):

    def ping(self, hostname: str) -> int:
        return call(["ping", "-c", "1", "-W", "1", hostname], stdout=DEVNULL, stderr=DEVNULL)
