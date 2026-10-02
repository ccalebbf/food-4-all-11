# -- Contains all Objects used for the database --

from datetime import datetime, date
from zoneinfo import ZoneInfo
from persistent import Persistent 
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping

class Distribution(Persistent):
    __module__ = 'models'

    def __init__(self, org, date, type, pax, isHalal):
        self.org = org
        self.date = datetime.strptime(date, "%Y-%m-%d").date()
        self.type = type
        self.pax = pax
        self.isHalal = isHalal
    
    def __setstate__(self, state):
        super().__setstate__(state)
        
    def __repr__(self):
        return (f"[Organisation: {self.org}, Date: {self.date}, Type: {self.type}, Number of People (Approx.): {self.pax}, Halal-Certified: {self.isHalal}]")

class Block(Persistent):
    __module__ = 'models'

    def __init__(self, block, postcode):
        self.block = block
        self.postcode = postcode
        self.latest_distribution = None
        self.distributions = PersistentMapping()
        self.deleted_distributions = PersistentList()

    def __setstate__(self, state):
        super().__setstate__(state)

    def log_distribution(self, dist_id, distribution):
        
        self.distributions[dist_id] = distribution

        if (self.latest_distribution is None or distribution.date >= self.latest_distribution.date):
            self.latest_distribution = distribution
        
        self._p_changed = True

    def rem_distribution(self, dist_id):

        if dist_id not in self.distributions:
            return
        
        removed_dist = self.distributions.pop(dist_id)
        self.deleted_distributions.append(dist_id)
        
        if removed_dist == self.latest_distribution:
            if self.distributions:
                self.latest_distribution = max(self.distributions.values(), key = lambda dist : dist.date)
            else:
                self.latest_distribution = None

        self._p_changed = True

        return removed_dist
           
    def time_since_last_distribution(self):
        if self.latest_distribution == None:
            return "No Record"
        return (datetime.now(ZoneInfo("Asia/Singapore")).date() - self.latest_distribution.date).days

    def display_distributions(self):
        if self.latest_distribution == None:
            print("No Record")
            return

        print(f"Food Distribution Records of Block {self.block}")

        sorted_dists = dict(sorted(self.distributions.items(), key = lambda item: item[1].date)) 

        for dist_id, dist in sorted_dists.items():
            print(f"ID: {dist_id}, {dist.__repr__()}")

    def __repr__(self):
        if self.latest_distribution is None:
            ld = "No Record"
            pd = 0
        else:
            ld = self.latest_distribution.__repr__()
            pd = len(self.distributions) - 1

        return(f"[Block: {self.block}, Postal Code: {self.postcode}, Latest Distribution: {ld}, Days Since Latest Distribution: {self.time_since_last_distribution()}, Number of Previous Distributions: {pd}]")

class Neighbourhood(Persistent):
    __module__ = 'models'
    
    def __init__(self, name, blocks):
        self.name = name
        self.blocks = PersistentList(blocks)

    def display_blocks(self):
        print(f"Blocks in {self.name}")
        for i in range(len(self.blocks)):
            print(self.blocks[i])
