# Dec Page Intelligence Agent

A 4-day prototype demonstrating production-grade agentic AI patterns applied to a homeowners insurance switch decision workflow. Built to demonstrate architectural and engineering thinking, not for production use.

## The use case

A customer shopping homeowners coverage hands over their current Dec Page. The system extracts everything, enriches with synthetic property intelligence, generates a competing Proposed Quote, and produces a side-by-side comparison with agent talking points.

## Architecture

Five-stage Prompt Chaining workflow following Anthropic's [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) guidance:

1. **Classifier**: identifies policy form (HO-3, HO-5, HO-6, HO-8)
2. **Dec Page Extractor**: extracts structured fields with per-field confidence scoring
3. **Risk Analyzer**: combines extraction with synthetic Home Factors data to identify coverage gaps and property risk factors
4. **Quote Generator**: deterministic logic (no LLM) for coverage recommendations and directional premium
5. **Comparator / Packager**: side-by-side comparison and agent-ready narrative

## Key design decisions

- **Workflow with LLM nodes, not autonomous agent loop.** Anthropic's recommendation for production agentic systems in regulated contexts.
- **Stage 4 is deliberately deterministic.** Pricing is rules-based work, not language work. Removing the LLM here is a poka-yoke pattern that eliminates the possibility of pricing hallucinations.
- **Per-field confidence scoring.** Granular human-in-the-loop routing rather than per-document confidence.
- **Synthetic Home Factors integration.** Demonstrates the strategic value of property intelligence beyond what is already on the dec page.
- **Audit logging at every stage.** Every decision logged for compliance traceability.

## How to run

```bash
git clone https://github.com/kumar-parupudi/dec-page-agent.git
cd dec-page-agent
python3 -m venv venv
source venv/bin/activate
pip install anthropic pydantic streamlit python-dotenv
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
streamlit run app.py
```

## What this is and what it is not

**What this is:** A prototype demonstrating architectural sophistication, hands-on agentic AI engineering at a workflow-with-LLM-nodes altitude, and the discipline of regulated-industry AI design.

**What this is not:** Production code. The eval harness is light, audit logging writes to JSON disk files, error handling is incomplete, pricing logic uses simple multipliers rather than real rate tables, and the Home Factors data is synthetic.

## Built with

- Anthropic Claude API (claude-sonnet-4)
- Pydantic for structured outputs and schema validation
- Streamlit for the demo UI
- Plain Python orchestration (no agentic framework, by design)

## References

- Anthropic Engineering, "Building Effective Agents": https://www.anthropic.com/research/building-effective-agents

---

Built by Kumar Parupudi · May 2026
