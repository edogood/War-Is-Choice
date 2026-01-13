from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Dict, List

from .models import Actor, Region, TradeRoute, World


@dataclass
class TurnReport:
    week: int
    actor_pressure: Dict[str, float]
    trade_disruptions: Dict[str, float]
    region_damage: Dict[str, float]
    info_shocks: Dict[str, float]
    notes: List[str]


def resolve_turn(world: World, rng: Random) -> TurnReport:
    actor_pressure = {}
    trade_disruptions = {}
    region_damage = {}
    info_shocks = {}
    notes: List[str] = []

    for actor in world.actors.values():
        degradation = actor.supply.degrade()
        pressure = actor.pressure_budget() * (1.0 - actor.information.distortion * 0.2)
        actor_pressure[actor.name] = pressure
        info_shock = rng.random() * (1.0 - actor.information.reliability)
        actor.information.apply_shock(info_shock)
        info_shocks[actor.name] = info_shock
        notes.append(
            f"{actor.name} supply losses: "
            f"fuel {degradation['fuel']:.1f}, food {degradation['food']:.1f}."
        )

    for route in world.trade_routes:
        pressure = sum(actor_pressure.values()) / (len(world.actors) * 100.0)
        pressure += route.risk * 0.1
        route.apply_disruption(pressure)
        trade_disruptions[route.name] = pressure

    for region in world.regions.values():
        controlling_actor = world.actors[region.controlling_actor]
        friction = (
            region.terrain_friction
            + region.insurgency
            + (1.0 - region.infrastructure_health)
        )
        damage = friction * (1.0 - controlling_actor.logistics_efficiency)
        region.apply_infrastructure_damage(damage)
        region_damage[region.name] = damage

    for actor in world.actors.values():
        for group in actor.force_groups:
            region = world.regions[group.region]
            force_friction = (
                region.terrain_friction
                + region.insurgency
                + (1.0 - actor.supply.resilience_score() / 100.0)
            )
            group.degrade(force_friction)

    world.week += 1
    world.events.extend(notes)

    return TurnReport(
        week=world.week,
        actor_pressure=actor_pressure,
        trade_disruptions=trade_disruptions,
        region_damage=region_damage,
        info_shocks=info_shocks,
        notes=notes,
    )


def summarize_world(world: World) -> str:
    actor_lines = []
    for actor in world.actors.values():
        actor_lines.append(
            f"{actor.name}: supply {actor.supply.resilience_score():.1f}, "
            f"info reliability {actor.information.reliability:.2f}"
        )
    trade_lines = [
        f"{route.name}: throughput {route.throughput:.1f}, risk {route.risk:.2f}"
        for route in world.trade_routes
    ]
    return "\n".join([
        f"Week {world.week}",
        "Actors:",
        *actor_lines,
        "Trade Routes:",
        *trade_lines,
    ])
