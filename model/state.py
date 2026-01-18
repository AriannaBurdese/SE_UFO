from dataclasses import dataclass
@dataclass
class State:
    id: str
    name: str
    capital: str
    lat:float
    lng : float
    area: int
    population: int
    neighbors: str

    def __str__(self):
        return f"{self.id}: {self.name}"

    def __repr__(self):
        return f"{self.id}: {self.name}"

    def __hash__(self):
        return hash(self.id)



