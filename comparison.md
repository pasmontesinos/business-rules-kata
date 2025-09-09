# [[Comparison of Approaches to Model Business Rules]]

---

## 🔹 Sequential Lumper Style Rules

### ⚡ Performance (7/10)
- ➕ **Immediate fail-fast**: checks are performed in order, and if any rule fails, the flow stops without evaluating the rest. This avoids unnecessary work in negative scenarios.
- ➕ **On-demand data loading**: each rule requests the information exactly when it’s needed, avoiding upfront preloading.
- ➖ **Rigid step-by-step execution**: although data is requested “inline,” each rule is directly coupled to the method’s flow. There’s no room for flexible reordering or parallelizing rules.

### 🛠️ Maintainability (4/10)
- ➕ **Single, simple method**: all logic is concentrated in one place, making it easy to locate.
- ➖ **Monolithic method**: as the number of rules grows, the method becomes longer and harder to read and maintain.
- ➖ **Unit testing difficulty**: rules are not encapsulated, so testing them in isolation is hard without running the full flow.

### 🚀 Extensibility (3/10)
- ➕ **Adding a new rule is straightforward**: just add another `if` to the flow.
- ➖ **Changes are invasive**: to add variants (e.g., rules differing by country), you’d have to directly modify the handler’s code, adding more conditionals.
- ➖ **Rigid ordering**: there’s no declarative way to reorder rules without editing the method code.

### 🔄 Reuse (2/10)
- ➖ **Embedded rules**: rule logic lives inside the handler, not as independent entities.
- ➖ **No portability**: if another part of the system needs the same rule, you must copy-paste the logic.
- ➖ **Scattered results**: each `if` throws its own exception, leading to inconsistent failure communication.

### ⚙️ Complexity (2/10)
- Minimal design complexity, but simplicity comes at the cost of poor organization and high coupling.

---

## 🔹 Sequential Splitter Style Rules

### ⚡ Performance (7/10)
- ➕ **Fail-fast execution**: same as Lumper, stops as soon as a rule fails.
- ➕ **Implicit memoization**: getters load data only once and reuse it across rules.
- ➖ **More execution hops**: splitting rules into private methods means more calls, though the cost is negligible.

### 🛠️ Maintainability (6/10)
- ➕ **Rules in separate methods**: each condition lives in its own method with a descriptive name, improving readability.
- ➖ **Fragmented orchestration**: the handler still decides the evaluation order by explicitly calling each method.

### 🚀 Extensibility (4/10)
- ➕ **Adding rules is clearer**: add a private method and call it in `_ensure_can_ride_attraction`.
- ➖ **Variants are still invasive**: if a different rule set is needed, the handler must be modified.

### 🔄 Reuse (3/10)
- ➕ **Partial reuse**: private methods can be called from other points inside the same handler.
- ➖ **Hard to port**: outside the handler, rules can’t easily be reused without copying code.

### ⚙️ Complexity (3/10)
- Adds some structure compared to Lumper, but logic remains embedded in the handler.

---

## 🔹 Sequential Specs Style Rules

### ⚡ Performance (7/10)
- ➕ **Linear evaluation**: runs in order, stopping early if a rule fails.
- ➕ **On-demand data loading**: each spec can request what it needs when executed.

### 🛠️ Maintainability (5/10)
- ➕ **Specification classes**: each rule is turned into its own class, making it easier to isolate.
- ➖ **Handler still orchestrates**: the handler remains responsible for order and invoking each spec, keeping it coupled.

### 🚀 Extensibility (4/10)
- ➕ **New rule = new class**: added cleanly.
- ➖ **Changing order or strategy** still means editing the handler.

### 🔄 Reuse (4/10)
- ➕ **Specs are portable**: they can be reused in other handlers if they receive the right data.
- ➖ **Inconsistent results**: each spec defines its own failure reason, leading to dispersion.

### ⚙️ Complexity (4/10)
- Introduces the concept of specs but without a common contract for all.

---

## 🔹 Static Context Policy (eager)

### ⚡ Performance (4/10)
- ➖ **Full upfront loading**: the context with all necessary data is built before evaluation starts.
- ➕ **Fast evaluation after load**: once the context is ready, specs are very quick.

### 🛠️ Maintainability (7/10)
- ➕ **Clear separation**: the handler builds the context and the policy decides, improving organization.
- ➕ **Declarative**: the policy maps each spec to an outcome (deny, wait, etc.) explicitly.
- ➖ **Bloated context**: as more rules appear, the context accumulates more data, even if only some rules use it.

### 🚀 Extensibility (6/10)
- ➕ **Easy to add specs**: just declare them in the policy map.
- ➖ **Cost of new data**: a rule needing new data forces changes to the context and its builder.

### 🔄 Reuse (6/10)
- ➕ **High within the same context**: rules using the same context contract are very portable.
- ➖ **Cross-context reuse is costly**: specs tied to a static context don’t work in others without modification.

### ⚙️ Complexity (6/10)
- Increases the number of pieces (policy, context, specs), but with clear responsibilities.

---

## 🔹 Context Resolver Policy (lazy)

### ⚡ Performance (7/10)
- ➕ **On-demand data**: resolver properties fetch and cache data only when needed.

### 🛠️ Maintainability (7/10)
- ➕ **Clear decoupling**: the handler delegates to the resolver and the policy.  
- ➕ **Uniform contract**: specs know they receive a resolver with a common API.
- ➖ **More parts to maintain**: resolver, policy, and specs must all be kept.

### 🚀 Extensibility (7/10)
- ➕ **New rules = new specs**: added without touching the handler.  
- ➖ **Resolver grows**: each new data need requires extending the resolver.

### 🔄 Reuse (7/10)
- ➕ **High**: specs can be reused in any handler with a compatible resolver.  
- ➖ **Dependent on the contract**: if the resolver API changes, all specs are affected.

### ⚙️ Complexity (7/10)
- Introduces a lazy resolver intermediary, increasing abstraction but also parts.

---

## 🔹 Composable Resolver Policy (lazy, typed by subdomains)

### ⚡ Performance (7/10)
- ➕ **Delegation to sub-resolvers**: each part of the context is fetched from its specialized resolver, avoiding unnecessary loads.

### 🛠️ Maintainability (7/10)
- ➕ **Smaller contracts**: each sub-resolver covers a domain slice (person, attraction, etc.).  
- ➖ **More wiring**: more classes and combinations to manage.

### 🚀 Extensibility (8/10)
- ➕ **Localized changes**: new person data? Only update `PersonResolver`.  
- ➖ **New combinations of rules**: may require creating a new combined ABC.

### 🔄 Reuse (9/10)
- ➕ **Very high**: a spec depending on `PersonResolver` can run in any policy implementing it.  
- ➖ **MRO issues in Python**: watch out for badly defined multiple inheritance.

### ⚙️ Complexity (8/10)
- Composed resolver with multiple sub-resolvers: more flexible but heavier design.

---

## 🔹 Untyped Resolver Policy (lazy, key-based)

### ⚡ Performance (7/10)
- ➕ **Key-based resolution**: specs ask for data by key, loaded only if needed.  
- ➕ **Implicit cache**: each sub-resolver caches its own data.

### 🛠️ Maintainability (6/10)
- ➕ **Lightweight implementation**: resolver is essentially a dict mapping keys to providers.  
- ➖ **Fragility**: key errors appear only at runtime; no static typing guarantees.

### 🚀 Extensibility (8/10)
- ➕ **Very flexible**: new data = new key and provider in the map.  
- ➖ **Key governance required**: without discipline, name collisions or inconsistencies may occur.

### 🔄 Reuse (8/10)
- ➕ **Highly portable**: a spec asking for `"person"` works in any policy that provides that key.  
- ➖ **String fragility**: depends on shared conventions.

### ⚙️ Complexity (6/10)
- Minimal infrastructure; complexity shifts to organizational discipline.

---

# 📊 Comparative Table (1–10)

| Approach                                 | Performance | Maintainability | Extensibility | Reuse | Complexity |
|------------------------------------------|:-----------:|:---------------:|:-------------:|:-----:|:----------:|
| Sequential **Lumper**                     |      7      |        4        |       3       |   2   |     2      |
| Sequential **Splitter**                   |      7      |        6        |       4       |   3   |     3      |
| Sequential **Specs**                      |      7      |        5        |       4       |   4   |     4      |
| **Static Context Policy** (eager)         |      4      |        7        |       6       |   6   |     6      |
| **Context Resolver Policy** (lazy)        |      7      |        7        |       7       |   7   |     7      |
| **Composable Resolver Policy** (lazy)     |      7      |        7        |       8       |   9   |     8      |
| **Untyped Resolver Policy** (lazy, key)   |      7      |        6        |       8       |   8   |     6      |
