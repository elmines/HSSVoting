from typing import Callable

Key = int
EncFn = Callable[[object,Key], object]

class VotingClient(object):
    def __init__(self, pk, enc: EncFn, dec, shares, servers):
        self._pk = pk
        self._enc = enc
        self._dec = dec
        self._shares = shares
        self._servers = servers
        self._intermeds = []

    async def snd_shares(self):
        """
        This could be a networking operation later, so we use `async`
        """
        i = 0
        m = len(self._servers)
        for (i, share) in enumerate(self._shares):
            share = self._enc(share, self._pk)
            await self._servers[i % m].rcv_share(share)


    @property
    def intermeds_rcvd(self) -> bool:
        return len(self._intermeds) >= len(self._shares)

    async def compute_output(self) -> object:
        while not self.intermeds_rcvd: #TODO: Implement something  better than repeated polling
            await self._rcv_intermeds() 
        output = self._dec(self._intermeds)
        return output

    async def _rcv_intermeds(self):
        intermeds = []    
        for s in self._servers:
            subset = await s.eval()
            if subset is None: continue
            intermeds.extend(subset)
        self._intermeds = intermeds


    def _enc(self, x):
        # TODO: Encrypt the data
        return x

__all__ = ["EncFn", "VotingClient"]
