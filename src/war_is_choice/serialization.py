import json
from pathlib import Path
from typing import Dict

from .models import (
    Actor,
    ForceGroup,
    InformationState,
    Region,
    SupplyNetwork,
    TradeRoute,
    World,
)


def world_from_snapshot(snapshot: Dict[str, object]) -> World:
    regions = {
        name: Region(**data) for name, data in snapshot["regions"].items()
    }
    actors = {}
    for name, data in snapshot["actors"].items():
        supply = SupplyNetwork(**data["supply"])
        info = InformationState(**data["information"])
        force_groups = [ForceGroup(**fg) for fg in data["force_groups"]]
        actors[name] = Actor(
            name=data["name"],
            risk_tolerance=data["risk_tolerance"],
            logistics_efficiency=data["logistics_efficiency"],
            escalation_doctrine=data["escalation_doctrine"],
            dependencies=data["dependencies"],
            supply=supply,
            information=info,
            force_groups=force_groups,
            alliances=data.get("alliances", []),
        )
    trade_routes = [TradeRoute(**route) for route in snapshot["trade_routes"]]
    return World(
        week=snapshot["week"],
        regions=regions,
        actors=actors,
        trade_routes=trade_routes,
        rng_seed=snapshot["rng_seed"],
        events=list(snapshot.get("events", [])),
    )


def save_world(world: World, path: Path) -> None:
    path.write_text(json.dumps(world.snapshot(), indent=2))


def load_world(path: Path) -> World:
    snapshot = json.loads(path.read_text())
    return world_from_snapshot(snapshot)
