from __future__ import annotations

from pathlib import Path
from random import Random

from .models import (
    Actor,
    ForceGroup,
    InformationState,
    Region,
    SupplyNetwork,
    TradeRoute,
    World,
)
from .serialization import save_world
from .simulation import resolve_turn, summarize_world


def build_example_world(seed: int = 7) -> World:
    regions = {
        "North Arc": Region(
            name="North Arc",
            terrain_friction=0.4,
            urbanization=0.7,
            infrastructure_health=0.8,
            insurgency=0.2,
            occupation_cost=0.6,
            controlling_actor="Union",
        ),
        "Equatorial Belt": Region(
            name="Equatorial Belt",
            terrain_friction=0.6,
            urbanization=0.5,
            infrastructure_health=0.6,
            insurgency=0.4,
            occupation_cost=0.7,
            controlling_actor="Coalition",
        ),
        "Maritime Hub": Region(
            name="Maritime Hub",
            terrain_friction=0.3,
            urbanization=0.8,
            infrastructure_health=0.9,
            insurgency=0.1,
            occupation_cost=0.5,
            controlling_actor="Trade League",
        ),
    }

    union = Actor(
        name="Union",
        risk_tolerance=0.4,
        logistics_efficiency=0.8,
        escalation_doctrine=0.6,
        dependencies={"energy": 0.7, "food": 0.5},
        supply=SupplyNetwork(
            fuel=90,
            food=85,
            spare_parts=80,
            industrial_capacity=92,
            data_bandwidth=88,
            political_capital=70,
            public_tolerance=75,
        ),
        information=InformationState(reliability=0.8, latency=0.6, distortion=0.2),
        force_groups=[
            ForceGroup(
                name="Union Ground",
                domain="land",
                readiness=0.75,
                sustainment=0.7,
                deterrence=0.6,
                posture="stabilize",
                region="North Arc",
            ),
            ForceGroup(
                name="Union Air",
                domain="air",
                readiness=0.8,
                sustainment=0.6,
                deterrence=0.7,
                posture="deny",
                region="North Arc",
            ),
        ],
        alliances=["Trade League"],
    )

    coalition = Actor(
        name="Coalition",
        risk_tolerance=0.6,
        logistics_efficiency=0.6,
        escalation_doctrine=0.7,
        dependencies={"rare_materials": 0.6, "capital": 0.8},
        supply=SupplyNetwork(
            fuel=70,
            food=65,
            spare_parts=60,
            industrial_capacity=72,
            data_bandwidth=70,
            political_capital=60,
            public_tolerance=68,
        ),
        information=InformationState(reliability=0.7, latency=0.8, distortion=0.3),
        force_groups=[
            ForceGroup(
                name="Coalition Maritime",
                domain="maritime",
                readiness=0.7,
                sustainment=0.6,
                deterrence=0.5,
                posture="protect",
                region="Equatorial Belt",
            )
        ],
        alliances=[],
    )

    trade_league = Actor(
        name="Trade League",
        risk_tolerance=0.2,
        logistics_efficiency=0.9,
        escalation_doctrine=0.3,
        dependencies={"trade": 0.9, "data": 0.7},
        supply=SupplyNetwork(
            fuel=80,
            food=78,
            spare_parts=82,
            industrial_capacity=85,
            data_bandwidth=95,
            political_capital=88,
            public_tolerance=90,
        ),
        information=InformationState(reliability=0.85, latency=0.5, distortion=0.15),
        force_groups=[
            ForceGroup(
                name="Trade League Cyber",
                domain="cyber",
                readiness=0.8,
                sustainment=0.8,
                deterrence=0.4,
                posture="shield",
                region="Maritime Hub",
            )
        ],
        alliances=["Union"],
    )

    trade_routes = [
        TradeRoute(
            name="Northern Corridor",
            origin="North Arc",
            destination="Maritime Hub",
            throughput=90,
            risk=0.2,
            chokepoint=True,
        ),
        TradeRoute(
            name="Southern Passage",
            origin="Equatorial Belt",
            destination="Maritime Hub",
            throughput=70,
            risk=0.3,
            chokepoint=False,
        ),
    ]

    return World(
        week=0,
        regions=regions,
        actors={"Union": union, "Coalition": coalition, "Trade League": trade_league},
        trade_routes=trade_routes,
        rng_seed=seed,
    )


def run_example(turns: int = 10, seed: int = 7) -> None:
    world = build_example_world(seed)
    rng = Random(seed)
    print("Starting simulation")
    print(summarize_world(world))
    for _ in range(turns):
        report = resolve_turn(world, rng)
        print("\nTurn", report.week)
        for note in report.notes:
            print("-", note)
    output_path = Path("example_world.json")
    save_world(world, output_path)
    print("\nFinal snapshot saved to", output_path)


if __name__ == "__main__":
    run_example()
