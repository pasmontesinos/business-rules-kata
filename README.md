# Magic Park Rules Kata

## Theme
- Magic Park: an automatic guardian decides whether a person can ride an attraction, whether they need a fast pass, a companion, or must wait due to capacity/weather.
- Expandable scopes: attractions, parades, shops, restaurants.

## Learning Goals
- Distinguish cost, complexity and extensibility between eager vs. lazy contexts.
- Design declarative rules with minimal requirements and explicit evaluation order.
- Implement short-circuiting and per-request cache to improve performance.
- Measure impact (resolved calls, simulated latency) and reason about trade‑offs.

## Incremental Requirements (TDD Path)

Each iteration adds a small, verifiable capability. Keep the domain simple and prioritize clear, ordered, and measurable rules.

- Given a `RideAttractionCommand` persist a registration of a person riding an attraction.
- Given height below minimum, deny access.
- Given adverse weather conditions, indicate to wait.
- Given full attraction capacity, indicate to wait.
- Given attraction under maintenance, indicate to wait.
- Given attraction closed, deny access.
- Given peak hours and a popular attraction, require a fast pass.

