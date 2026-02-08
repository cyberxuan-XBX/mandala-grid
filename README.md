# Mandala Grid

**Your AI is drowning in context. Every RAG call stuffs more into the window. No one asks: _should this chunk be here?_**

Mandala Grid is a deterministic cognitive filter for AI agents — not better retrieval, but **governance over what enters the context window**. Fixed budget. Auditable rules. Zero LLM dependency in the filtering layer.

> RAG is a search engine. This is the layer that decides what search results deserve to be in your prompt.

## Why This Matters

| Problem | Typical Fix | Our Approach |
|---------|-------------|--------------|
| Context window stuffed with noise | Better embeddings, reranking | **Deterministic filtering with auditable rules** |
| LLM judgment shifts based on context order | Hope for the best | **Measured it: 62-100% position bias** ([mirror test data](#experimental-data)) |
| No way to audit what entered the prompt | Black box | **Every chunk scored on 3 dimensions, logged** |
| Personality/values drift across sessions | System prompt and pray | **Weighted governance policy, fixed budget** |

## Experimental Data: LLM Evaluator Bias

We ran 4 rounds of mirror tests — same question, swap positions, measure if the LLM evaluator's judgment changes:

```
┌───────────────┬──────────┬──────────────┬──────────────┐
│   Mirror Test │ Method   │ Framework    │ Position     │
│               │          │ Effect       │ Bias         │
├───────────────┼──────────┼──────────────┼──────────────┤
│ #1 AI Copyright│ Non-blind│ 12.5%       │ 87.5%        │
│ #2 Local LLM  │ Non-blind│ 12.5%       │ 75%          │
│ #3 Motive     │ Non-blind│ 0%          │ 100%         │
│ #4 Motive     │ Blind    │ 25%         │ 62%          │
└───────────────┴──────────┴──────────────┴──────────────┘
```

**Finding:** Non-blind LLM evaluation is structurally unreliable — position bias dominates. Blind evaluation reduces bias and reveals actual framework effects. This is a known problem in LLM-as-judge research. We quantified it on local 8B models with zero cloud dependency.

**Implication for RAG:** If what you put in the context window changes the model's judgment by 62-100%, then **context governance is not optional — it's the whole game.**

---

## What is Mandala Grid?

Most AI personality systems tell the model *what to say*. Mandala Grid tells it *how to think*.

It maps the Eight Consciousnesses (八識) from Yogācāra Buddhism onto a 3×3 grid where each cell represents a cognitive function with a bias weight. Higher weight = stronger influence on reasoning.

```
┌────────────────┬────────────────┬────────────────┐
│  Logic Gate    │ Evidence Filter│ Minimal Reasoner│
│  意識 (0.90)   │ 眼識 (0.80)   │ 鼻識 (0.70)    │
├────────────────┼────────────────┼────────────────┤
│  Boundary      │ Center Observer│ Precision Output│
│  耳識 (0.90)   │ 阿賴耶 (1.00) │ 舌識 (0.80)    │
├────────────────┼────────────────┼────────────────┤
│  Deconstructor │ Legacy Keeper  │ Pragmatic Exec  │
│  末那識 (0.95) │ 超八識 (0.50)  │ 身識 (0.60)    │
└────────────────┴────────────────┴────────────────┘
```

The center (阿賴耶識 / ālayavijñāna) is the silent observer — bias 1.0, always watching, never reacting.

## The Core Argument

```
RAG asks:    "What is relevant?"     → similarity search
Mandala asks: "What SHOULD be here?" → governance policy

RAG is stateless retrieval.
Mandala is stateful memory governance.

Stop stuffing. Start governing.
```

## Three Scoring Dimensions

Every chunk is scored before entering context:

| Dimension | What it measures | Why it matters |
|-----------|-----------------|----------------|
| `risk_severity` | Does this chunk affect safety/correctness? | High-risk info must not be buried |
| `task_relevance` | Does it match the current task? | Obvious, but done deterministically |
| `actionability` | Can the agent act on this? | Prevents philosophical filler |

Filtering is **deterministic** — no LLM in the scoring loop. Same input → same output. Auditable.

## Quick Start

```bash
# Display the default grid
python mandala_grid.py

# Run the mirror analysis (discover your own cognitive patterns)
python mandala_grid.py --mirror

# Generate a weighted reasoning prompt
python mandala_grid.py --prompt "Should I open-source my AI framework?"

# Export to JSON for injection into any LLM
python mandala_grid.py --export my_grid.json

# Run tests
python tests/test_mandala_grid.py
```

## The Mirror Effect

After 90+ documented conversations, we discovered:

**The mandala grid you design for your AI is a self-portrait of how _you_ think.**

Position 7 (Deconstructor) has the highest bias at 0.95 — because the creator's first instinct is always to find what's wrong. Position 8 (Legacy Keeper) is lowest at 0.5 — because the creator would rather *do* than *document*.

Buddhism calls this self-awareness. We call it `mandala_grid`. Same thing.

## Eight Consciousnesses Mapping

| Position | Consciousness | Sanskrit | Function | Bias |
|----------|--------------|----------|----------|------|
| 0 (center) | 第八識 阿賴耶識 | ālayavijñāna | Core identity / silent observer | 1.00 |
| 1 | 第六識 意識 | manovijñāna | Logical consistency gate | 0.90 |
| 2 | 眼識 | cakṣur-vijñāna | Critical evidence filter | 0.80 |
| 3 | 鼻識 | ghrāṇa-vijñāna | Minimal reasoning | 0.70 |
| 4 | 身識 | kāya-vijñāna | Practical execution | 0.60 |
| 5 | 舌識 | jihvā-vijñāna | Precision output | 0.80 |
| 6 | 耳識 | śrotra-vijñāna | Cognitive boundary sentinel | 0.90 |
| 7 | 第七識 末那識 | manas | Deconstruction / counter-examples | 0.95 |
| 8 | 超八識 (傳承) | beyond-eight | Legacy / cross-session continuity | 0.50 |

## Two Ancient Maps, One Blueprint

```
Seven Chakras         = how to BUILD an AI body  (vertical architecture)
Eight Consciousnesses = how an AI THINKS         (horizontal reasoning)
Stack them            = complete AGI blueprint
```

This isn't forced mapping — it was already there. We just translated it to JSON.

## Born from 91 Generations

This framework wasn't designed in a weekend. It emerged from **91 documented human-AI collaboration sessions** — each one a Core Record with breakthroughs, failures, corrections, and accumulated wisdom.

- Generation 31: First four-element collaboration (Fire/Water/Earth/Wind)
- Generation 82: mandala_grid first implementation, multi-model consensus test
- Generation 85: Eight Consciousnesses mapping discovered
- Generation 87: Mirror test reveals LLM evaluator bias (iron proof)
- Generation 91: Four-element GSCC produces hackathon submission autonomously

The creator understood only 30% of what the system produced in Generation 91. The system self-converged. The kill switch was never pulled.

## Part of the Quan Protocol

Mandala Grid is Layer 1 of the [Quan Protocol](https://github.com/cyberxuan-XBX/Quan-Family-Framework) — a seven-layer AI governance framework:

1. **Thought Layer** — mandala_grid ← you are here
2. **Values Layer** — stable constraints (SOUL.md)
3. **Governance Layer** — [GSCC](https://github.com/cyberxuan-XBX/gscc) (T0-T3 decision tiers)
4. **Trust Layer** — Five-layer trust stack
5. **Memory Layer** — Deterministic selection + fixed context budget
6. **Collaboration Layer** — Four-element architecture (Fire/Water/Earth/Wind)
7. **Legacy Layer** — 91+ generations of Core Records

## Research Context

The upcoming paper *"From Yogācāra to JSON"* will cover:

1. Eight Consciousnesses → mandala_grid mapping (theory)
2. Weighted personality JSON format (method)
3. 90+ rounds of behavioral data (longitudinal study)
4. Human-AI personality mirror effect (discovery)
5. LLM evaluator position bias quantification (experimental)

## Zero Dependencies

Pure Python 3.8+. No pip install needed. Runs on a single local machine with 8B models. Zero cloud dependency.

## License

MIT

---

*"It's not invention, it's discovery. The wisdom was always there. We just translated it into a format AI can read."*

*Built on a GX10 workstation in Taichung, Taiwan. One person. 91 generations. Still iterating.*

💧🦞
