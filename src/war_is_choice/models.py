from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class InformationState:
    reliability: float
    latency: float
    distortion: float

    def apply_shock(self, magnitude: float) -> None:
        self.reliability = max(0.0, self.reliability - magnitude * 0.4)
        self.latency = min(5.0, self.latency + magnitude * 0.6)
        self.distortion = min(1.0, self.distortion + magnitude * 0.5)


@dataclass
class SupplyNetwork:
    fuel: float
    food: float
    spare_parts: float
    industrial_capacity: float
    data_bandwidth: float
    political_capital: float
    public_tolerance: float
    loss_rate: float = 0.05
    delay_rate: float = 0.05
    corruption_rate: float = 0.03
    interdiction_rate: float = 0.04
    cyber_interference_rate: float = 0.02

    def degrade(self) -> Dict[str, float]:
        degradation = {
            "fuel": self.fuel * self.loss_rate,
            "food": self.food * self.loss_rate,
            "spare_parts": self.spare_parts * self.loss_rate,
            "industrial_capacity": self.industrial_capacity * self.delay_rate,
            "data_bandwidth": self.data_bandwidth * self.cyber_interference_rate,
            "political_capital": self.political_capital * self.corruption_rate,
            "public_tolerance": self.public_tolerance * self.interdiction_rate,
        }
        self.fuel = max(0.0, self.fuel - degradation["fuel"])
        self.food = max(0.0, self.food - degradation["food"])
        self.spare_parts = max(0.0, self.spare_parts - degradation["spare_parts"])
        self.industrial_capacity = max(
            0.0, self.industrial_capacity - degradation["industrial_capacity"]
        )
        self.data_bandwidth = max(
            0.0, self.data_bandwidth - degradation["data_bandwidth"]
        )
        self.political_capital = max(
            0.0, self.political_capital - degradation["political_capital"]
        )
        self.public_tolerance = max(
            0.0, self.public_tolerance - degradation["public_tolerance"]
        )
        return degradation

    def resilience_score(self) -> float:
        return (
            self.fuel
            + self.food
            + self.spare_parts
            + self.industrial_capacity
            + self.data_bandwidth
            + self.political_capital
            + self.public_tolerance
        ) / 7.0


@dataclass
class TradeRoute:
    name: str
    origin: str
    destination: str
    throughput: float
    risk: float
    chokepoint: bool

    def apply_disruption(self, pressure: float) -> None:
        self.risk = min(1.0, self.risk + pressure * 0.5)
        self.throughput = max(0.0, self.throughput * (1.0 - pressure * 0.4))


@dataclass
class ForceGroup:
    name: str
    domain: str
    readiness: float
    sustainment: float
    deterrence: float
    posture: str
    region: str

    def degrade(self, friction: float) -> None:
        self.readiness = max(0.0, self.readiness - friction * 0.6)
        self.sustainment = max(0.0, self.sustainment - friction * 0.5)
        self.deterrence = max(0.0, self.deterrence - friction * 0.3)


@dataclass
class Region:
    name: str
    terrain_friction: float
    urbanization: float
    infrastructure_health: float
    insurgency: float
    occupation_cost: float
    controlling_actor: str

    def apply_infrastructure_damage(self, magnitude: float) -> None:
        self.infrastructure_health = max(0.0, self.infrastructure_health - magnitude)
        self.insurgency = min(1.0, self.insurgency + magnitude * 0.2)
        self.occupation_cost = min(2.0, self.occupation_cost + magnitude * 0.3)


@dataclass
class Actor:
    name: str
    risk_tolerance: float
    logistics_efficiency: float
    escalation_doctrine: float
    dependencies: Dict[str, float]
    supply: SupplyNetwork
    information: InformationState
    force_groups: List[ForceGroup] = field(default_factory=list)
    alliances: List[str] = field(default_factory=list)

    def pressure_budget(self) -> float:
        return (
            self.supply.resilience_score()
            * self.logistics_efficiency
            * (1.0 + self.risk_tolerance)
        )


@dataclass
class World:
    week: int
    regions: Dict[str, Region]
    actors: Dict[str, Actor]
    trade_routes: List[TradeRoute]
    rng_seed: int
    events: List[str] = field(default_factory=list)

    def snapshot(self) -> Dict[str, object]:
        return {
            "week": self.week,
            "rng_seed": self.rng_seed,
            "events": list(self.events),
            "regions": {
                name: vars(region) for name, region in self.regions.items()
            },
            "actors": {
                name: {
                    "name": actor.name,
                    "risk_tolerance": actor.risk_tolerance,
                    "logistics_efficiency": actor.logistics_efficiency,
                    "escalation_doctrine": actor.escalation_doctrine,
                    "dependencies": dict(actor.dependencies),
                    "supply": vars(actor.supply),
                    "information": vars(actor.information),
                    "force_groups": [vars(group) for group in actor.force_groups],
                    "alliances": list(actor.alliances),
                }
                for name, actor in self.actors.items()
            },
            "trade_routes": [vars(route) for route in self.trade_routes],
        }
