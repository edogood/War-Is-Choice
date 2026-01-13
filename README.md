# War Is Choice (Scaffold)

## Vision
War Is Choice is a global-scale strategy simulation that treats the modern world as a coupled system. It emphasizes friction, interdependence, and imperfect control. War is a possible outcome, not the objective. The core experience is navigating logistics, legitimacy, trade, and information under uncertainty.

## What the game simulates
- **Coupled domains**: land, maritime, air, space, cyber/information, and economy/trade.
- **Logistics as the bottleneck**: fuel, food, spare parts, industrial capacity, data bandwidth, political capital, and public tolerance are tracked explicitly.
- **Information as a weapon**: reliability, latency, and distortion shape decisions.
- **Indirect power**: military pressure is mediated by access, time, and legitimacy.
- **Trade fragility**: chokepoints, risk, and disruption affect throughput.

## What the game does NOT simulate
- **Weapon-by-weapon fidelity**: effects are abstracted to pressure, disruption, and escalation.
- **Tactical combat**: no unit-level kill counts, hit probabilities, or micromanagement.
- **Detailed civilian demographics**: population, culture, or narrative lore are outside scope.

## Design philosophy
- **Friction first**: every system exists to introduce trade-offs, delays, or degradation.
- **Hierarchy over micromanagement**: global → theater → region → force group.
- **Deterministic uncertainty**: randomness is seeded and replayable.
- **Effect-based modeling**: infrastructure damage, logistics disruption, and political strain.

## High-level architecture

### Core systems
1. **World state**: the authoritative snapshot containing regions, actors, trade routes, and events.
2. **Actors/Factions**: nations, alliances, and non-state entities with distinct risk tolerance and logistics efficiency.
3. **Regions**: terrain, infrastructure health, and occupation friction that drive operational costs.
4. **Supply networks**: the logistics ledger; it degrades every turn and constrains power projection.
5. **Information state**: reliability, latency, and distortion create fog and misallocation.
6. **Trade routes**: chokepoints and risk influence global economic throughput.

### Deterministic simulation loop
- Every turn uses a seeded RNG and a fixed pipeline to ensure replayable outcomes.

## Repository structure
```
.
├── README.md                 # Vision, scope, philosophy, limitations
├── pyproject.toml             # Packaging metadata
└── src/
    └── war_is_choice/
        ├── __init__.py        # Package marker
        ├── example.py          # 10-turn minimal simulation
        ├── models.py           # Core data models
        ├── serialization.py    # JSON serialization helpers
        └── simulation.py       # Turn pipeline and reporting
```

## Core data models
- **World**: week, regions, actors, trade routes, RNG seed, event log.
- **Region**: terrain friction, urbanization, infrastructure health, insurgency, occupation cost.
- **Actor**: risk tolerance, logistics efficiency, escalation doctrine, dependencies, force groups.
- **SupplyNetwork**: fuel, food, spare parts, industrial capacity, data bandwidth, political capital, public tolerance.
- **TradeRoute**: throughput, risk, and chokepoints.
- **ForceGroup**: domain-specific readiness, sustainment, and deterrence.
- **InformationState**: reliability, latency, distortion.

## Turn resolution pipeline (weekly)
1. **Logistics degradation**: every actor’s supply network degrades from loss, delay, corruption, interdiction, and cyber interference.
2. **Information shock**: actors receive reliability and distortion shocks, reducing decision quality.
3. **Trade disruption**: trade route risk and throughput adjust based on global pressure.
4. **Regional friction**: terrain, insurgency, and infrastructure damage raise occupation and sustainment costs.
5. **Force readiness decay**: force groups degrade based on regional friction and supply resilience.
6. **Event log**: narrates the compounded friction for the week.

## Example minimal simulation
Run a 10-turn scenario with three actors (Union, Coalition, Trade League):
```bash
python -m war_is_choice.example
```
The simulation prints weekly summaries and writes a deterministic `example_world.json` snapshot.

## Known limitations
- No AI planners beyond simple pressure heuristics.
- No explicit diplomatic negotiation model (only indirect alliance effects).
- No explicit space or cyber assets beyond their abstract information/logistics effects.
- No UI; CLI output only.
