"""Pregunta a Jev cómo se relaciona cada periodo de crecimiento de AUM con los eventos del periodo.

Uso: TYPESAFE_API_KEY=... python3 analysis/run_jev.py
Solo lectura: llama a la API de TypeSafe y escribe analysis/results.json.
"""
import json
import os
import pathlib
import time

import requests

from data import EVENTS, FIRMS

API_URL = "https://api.typesafe.ai/v1/systemone"
OUT = pathlib.Path(__file__).with_name("results.json")

QUESTIONS = {
    "relationship": {
        "type": "choice",
        "instructions": "Given the firm profile, its AUM change in `period`, and the `events` in that period, what best describes how the events relate to the AUM change?",
        "criteria": {
            "events_drove_growth": "The events plausibly caused or strongly fueled the AUM increase.",
            "events_drove_decline": "The events plausibly caused the AUM decrease.",
            "growth_despite_events": "AUM grew even though the events were negative for markets.",
            "firm_specific": "The change is mainly explained by something specific to the firm (e.g. an acquisition), not macro events.",
            "unclear": "The data does not support a clear link.",
        },
    },
    "mechanism": {
        "type": "choice",
        "instructions": "What is the most likely primary mechanism linking the events to this firm's AUM change?",
        "criteria": {
            "market_valuation": "Asset prices rising or falling changed the value of existing assets.",
            "passive_flows": "Investors moving money into low-cost index funds and ETFs.",
            "search_for_yield_alternatives": "Low rates pushed investors into private equity, real estate, private credit.",
            "acquisition": "The firm bought another manager or business.",
            "regulation": "A regulatory change shifted assets toward or away from the firm.",
            "flight_to_safety_outflows": "Investors withdrew money or de-risked during a crisis.",
        },
    },
    "link_strength": {
        "type": "score",
        "instructions": "How strong is the link between the events and the firm's AUM change in this period?",
        "criteria": ["No link", "Weak link", "Moderate link", "Strong link"],
    },
    "price_driven": {
        "type": "noul",
        "instructions": "Is this AUM change mainly explained by market price movements rather than by new client money or acquisitions?",
    },
}


def periods():
    for firm, info in FIRMS.items():
        years = sorted(info["aum"])
        for y0, y1 in zip(years, years[1:]):
            a0, a1 = info["aum"][y0], info["aum"][y1]
            events = [d for s, e, d in EVENTS if s <= y1 and e > y0 or (s == e and y0 < s <= y1)]
            yield {
                "firm": firm,
                "firm_profile": info["profile"],
                "period": f"end of {y0} to end of {y1}",
                "aum_start_usd_bn": a0,
                "aum_end_usd_bn": a1,
                "aum_change_pct": round((a1 / a0 - 1) * 100, 1),
                "annualized_change_pct": round(((a1 / a0) ** (1 / (y1 - y0)) - 1) * 100, 1),
                "events": events,
                "_y0": y0,
                "_y1": y1,
            }


def ask(state):
    key = os.environ["TYPESAFE_API_KEY"]
    body = {"model": "jev-latest", "state": {k: v for k, v in state.items() if not k.startswith("_")},
            "questions": QUESTIONS}
    for attempt in range(5):
        r = requests.post(API_URL, json=body, timeout=60,
                          headers={"Authorization": f"Bearer {key}"})
        if r.status_code in (429, 529):
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        return r.json()
    r.raise_for_status()


def main():
    results = []
    for p in periods():
        resp = ask(p)
        results.append({**p, "model": resp["model"], "answers": resp["answers"]})
        a = resp["answers"]
        print(f"{p['firm'][:12]:12} {p['_y0']}-{p['_y1']} {p['aum_change_pct']:>7}%  "
              f"{a['relationship']['choice']:22} {a['mechanism']['choice']:30} "
              f"fuerza={a['link_strength']['score']:.2f} precio={a['price_driven']['noul']:.2f}")
    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
