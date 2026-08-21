#!/usr/bin/env python3
"""
CAIE 9701 Topic ID Audit & Fix Script
Author: Seven (CAIE 9701 Senior Examiner)
Date: 2026-08-21

Usage:
  python3 topic_audit.py db.json                    # 生成审计报告
  python3 topic_audit.py db.json --fix-known        # 修正已知错误模式
  python3 topic_audit.py db.json --fill-empty       # 空topic填充默认值
  python3 topic_audit.py db.json --full-report      # 完整详细报告

Output: topic_audit_report.json
"""

import json
import sys
import os
from collections import defaultdict, Counter

# ============================================================
# Part 1: Correct topic_id → name mapping (CAIE 9701 Syllabus)
# ============================================================

TOPIC_NAME_MAP = {
    # ch01: Atomic Structure & Electrons in Atoms
    "ch01_t01": "Isotopes & relative atomic mass",
    "ch01_t02": "Mass spectrometry",
    "ch01_t03": "Electronic structure",
    "ch01_t04": "Ionisation energy",
    "ch01_t05": "Atomic orbitals",
    "ch01_t06": "Periodic trends (AS)",

    # ch03: Atoms, Molecules and Stoichiometry
    "ch03_t01": "Mole concept & Avogadro constant",
    "ch03_t02": "Relative atomic/molecular mass",
    "ch03_t03": "Empirical & molecular formula",
    "ch03_t04": "Chemical equations & stoichiometry",
    "ch03_t05": "Limiting reagent & yield",
    "ch03_t06": "Gas volumes & molar volume",
    "ch03_t07": "Solutions & concentration",

    # ch04: Chemical Bonding
    "ch04_t01": "Ionic bonding",
    "ch04_t02": "Covalent bonding",
    "ch04_t03": "Metallic bonding",
    "ch04_t04": "VSEPR & molecular shapes",
    "ch04_t05": "Electronegativity & bond polarity",
    "ch04_t06": "Intermolecular forces",
    "ch04_t07": "σ and π bonds",
    "ch04_t08": "Delocalisation & resonance",
    "ch04_t09": "Bonding & physical properties",

    # ch05: States of Matter
    "ch05_t01": "Gases & ideal gas equation",
    "ch05_t02": "Kinetic theory of gases",
    "ch05_t03": "Liquids & vapour pressure",
    "ch05_t04": "Solids & crystal structures",
    "ch05_t05": "Phase changes",
    "ch05_t06": "Solutions & colligative properties",
    "ch05_t07": "Real gases & deviations",

    # ch06: Enthalpy Changes
    "ch06_t01": "Exothermic & endothermic reactions",
    "ch06_t02": "Standard enthalpy changes",
    "ch06_t03": "Hess's Law",
    "ch06_t04": "Bond energies",
    "ch06_t05": "Enthalpy of solution/hydration",
    "ch06_t06": "Calorimetry",

    # ch07: Redox Reactions
    "ch07_t01": "Oxidation numbers",
    "ch07_t02": "Redox reactions & agents",
    "ch07_t03": "Balancing redox equations",
    "ch07_t04": "Redox titrations",
    "ch07_t05": "Electrochemical cells (AS)",

    # ch08: Equilibria
    "ch08_t01": "Reversible reactions & dynamic equilibrium",
    "ch08_t02": "Le Chatelier's principle",
    "ch08_t03": "Equilibrium constants (Kc, Kp)",
    "ch08_t04": "Industrial applications",
    "ch08_t05": "Acid-base equilibria",
    "ch08_t06": "Buffer solutions",
    "ch08_t07": "Solubility product (Ksp)",
    "ch08_t08": "Partition coefficient",

    # ch09: Rates of Reaction
    "ch09_t01": "Rate of reaction & measurement",
    "ch09_t02": "Collision theory",
    "ch09_t03": "Factors affecting rate",
    "ch09_t04": "Rate equations & order",
    "ch09_t05": "Rate-determining step",
    "ch09_t06": "Catalysis",
    "ch09_t07": "Arrhenius equation",

    # ch10: Periodicity
    "ch10_t01": "Periodic table structure",
    "ch10_t02": "Periodic trends (physical)",
    "ch10_t03": "Periodic trends (chemical)",
    "ch10_t04": "Third period elements",
    "ch10_t05": "Transition elements (intro)",
    "ch10_t06": "Uses of periodic table",

    # ch11: Group 2
    "ch11_t01": "Group 2 metals & reactions",
    "ch11_t02": "Thermal stability",
    "ch11_t03": "Solubility trends",
    "ch11_t04": "Uses of Group 2 compounds",
    "ch11_t05": "Anomalous properties of Be",

    # ch12: Group 17
    "ch12_t01": "Halogens & their properties",
    "ch12_t02": "Halogen reactions",
    "ch12_t03": "Halide ions & tests",
    "ch12_t04": "Disproportionation & uses",

    # ch13: Nitrogen and Sulfur
    "ch13_t01": "Nitrogen & its compounds",
    "ch13_t02": "Sulfur & its compounds",
    "ch13_t03": "Environmental chemistry",
    "ch13_t04": "Fertilisers",

    # ch14: Introduction to Organic Chemistry
    "ch14_t01": "Homologous series & functional groups",
    "ch14_t02": "Nomenclature",
    "ch14_t03": "Structural isomerism",
    "ch14_t04": "Stereoisomerism (cis/trans)",
    "ch14_t05": "Reaction mechanisms (intro)",
    "ch14_t06": "Organic analysis techniques",

    # ch15: Hydrocarbons
    "ch15_t01": "Alkanes & free radical substitution",
    "ch15_t02": "Alkenes & electrophilic addition",
    "ch15_t03": "Markovnikov's rule",
    "ch15_t04": "Polymerisation (addition)",
    "ch15_t05": "Cracking & reforming",
    "ch15_t06": "Environmental impact",

    # ch16: Halogenoalkanes
    "ch16_t01": "Nucleophilic substitution (SN1/SN2)",
    "ch16_t02": "Elimination reactions",
    "ch16_t03": "CFCs & ozone depletion",
    "ch16_t04": "Uses & properties",

    # ch17: Alcohols, Esters and Carboxylic Acids (pre-split)
    "ch17_t01": "Alcohols: reactions & synthesis",
    "ch17_t02": "Esters: formation & hydrolysis",
    "ch17_t03": "Phenol",
    "ch17_t04": "Carboxylic acids & acyl chlorides",

    # ch18: Carbonyl Compounds
    "ch18_t01": "Aldehydes & ketones: reactions",
    "ch18_t02": "2,4-DNPH & Tollens' reagent",
    "ch18_t03": "Reduction of carbonyls",
    "ch18_t04": "Nucleophilic addition mechanism",
    "ch18_t05": "Iodoform reaction",

    # ch19: Lattice Energy
    "ch19_t01": "Born-Haber cycles",
    "ch19_t02": "Lattice energy factors",

    # ch20: Electrochemistry A2
    "ch20_t01": "Electrolysis",
    "ch20_t02": "Electrode potentials & Nernst",

    # ch21: Further Aspects of Equilibria
    "ch21_t01": "Acids, bases, buffers & Ksp (A2)",

    # ch22: Reaction Kinetics A2
    "ch22_t02": "Rate equations & catalysis (A2)",

    # ch23: Entropy and Gibbs Free Energy
    "ch23_t01": "Entropy & Gibbs free energy",

    # ch24: Transition Elements
    "ch24_t01": "Transition elements: complexes & colour",

    # ch25: Benzene
    "ch25_t01": "Benzene & electrophilic substitution",

    # ch26: Carboxylic Acids and Derivatives A2
    "ch26_t01": "Carboxylic acids: acidity & reactions",
    "ch26_t02": "Acyl chlorides",
    "ch26_t03": "Esterification & hydrolysis",
    "ch26_t04": "Amides",
    "ch26_t05": "Acidity comparison",
    "ch26_t06": "Synthetic applications",

    # ch27: Organic Nitrogen Compounds
    "ch27_t01": "Amines, amides, amino acids & azo",

    # ch28: Polymerisation (pre-split)
    "ch28_t01": "Addition polymerisation",
    "ch28_t02": "Condensation polymerisation",
    "ch28_t03": "Polyesters & polyamides",
    "ch28_t04": "Polymer degradation",

    # ch29: Organic Synthesis
    "ch29_t01": "Multi-step organic synthesis",

    # ch30: Analytical Chemistry
    "ch30_t01": "NMR, chromatography & mass spec (A2)",
}

# Known over-tagged patterns (likely incorrect combinations)
KNOWN_OVER_TAG_PATTERNS = [
    # Pattern: (set of topic_ids, likely_correct_single, description)
    (frozenset(["ch01_t02", "ch01_t03"]), ["ch01_t01"], "Mass spec + Electronic structure → likely just Isotopes"),
    (frozenset(["ch01_t04", "ch01_t05"]), ["ch01_t04"], "Ionisation energy + Atomic orbitals → likely just IE"),
    (frozenset(["ch03_t01", "ch03_t02"]), ["ch03_t01"], "Mole concept + Relative mass → likely just Mole concept"),
    (frozenset(["ch03_t04", "ch03_t05"]), ["ch03_t04"], "Stoichiometry + Limiting reagent → likely just Stoichiometry"),
    (frozenset(["ch05_t04", "ch05_t05"]), ["ch05_t04"], "Solids + Phase changes → likely just Solids"),
    (frozenset(["ch06_t05", "ch06_t06"]), ["ch06_t05"], "Enthalpy of solution + Calorimetry"),
    (frozenset(["ch08_t06", "ch08_t07"]), ["ch08_t06"], "Buffers + Ksp"),
    (frozenset(["ch08_t04", "ch08_t05"]), ["ch08_t04"], "Industrial + Acid-base"),
    (frozenset(["ch04_t03", "ch04_t09"]), ["ch04_t03"], "Metallic bonding + Physical properties"),
    (frozenset(["ch07_t03", "ch07_t04"]), ["ch07_t03"], "Balancing redox + Redox titrations"),
    (frozenset(["ch10_t03", "ch10_t04"]), ["ch10_t03"], "Periodic trends chemical + Third period"),
]

# Default topic for each chapter (fallback when no topic assigned)
CHAPTER_DEFAULT_TOPIC = {
    "ch01": "ch01_t01",
    "ch03": "ch03_t04",
    "ch04": "ch04_t02",
    "ch05": "ch05_t01",
    "ch06": "ch06_t01",
    "ch07": "ch07_t02",
    "ch08": "ch08_t01",
    "ch09": "ch09_t01",
    "ch10": "ch10_t01",
    "ch11": "ch11_t01",
    "ch12": "ch12_t01",
    "ch13": "ch13_t01",
    "ch14": "ch14_t01",
    "ch15": "ch15_t01",
    "ch16": "ch16_t01",
    "ch17": "ch17_t01",
    "ch18": "ch18_t01",
    "ch19": "ch19_t01",
    "ch20": "ch20_t01",
    "ch21": "ch21_t01",
    "ch22": "ch22_t02",
    "ch23": "ch23_t01",
    "ch24": "ch24_t01",
    "ch25": "ch25_t01",
    "ch26": "ch26_t01",
    "ch27": "ch27_t01",
    "ch28": "ch28_t01",
    "ch29": "ch29_t01",
    "ch30": "ch30_t01",
    "ch00": None,  # ch00 needs manual classification
}


def load_db(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_db(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved to {path}")


def audit(db_path):
    """Generate comprehensive audit report."""
    data = load_db(db_path)
    qs = data['questions']
    total = len(qs)

    report = {
        "summary": {},
        "by_chapter": {},
        "by_topic": {},
        "empty_topics": [],
        "over_tagged": [],
        "known_wrong_patterns": [],
        "suspicious_single_topic": [],
        "ch00_unassigned": [],
    }

    # --- Summary ---
    empty = [q for q in qs if not q.get('topic_ids')]
    single = [q for q in qs if len(q.get('topic_ids', [])) == 1]
    multi = [q for q in qs if len(q.get('topic_ids', [])) > 1]

    report["summary"] = {
        "total_questions": total,
        "empty_topics": len(empty),
        "single_topic": len(single),
        "multiple_topics": len(multi),
        "empty_pct": round(len(empty) / total * 100, 1),
        "single_pct": round(len(single) / total * 100, 1),
        "multi_pct": round(len(multi) / total * 100, 1),
    }

    # --- By chapter ---
    ch_stats = defaultdict(lambda: {"total": 0, "empty": 0, "single": 0, "multi": 0})
    for q in qs:
        ch = q.get('chapter_id', '?')
        ch_stats[ch]["total"] += 1
        n = len(q.get('topic_ids', []))
        if n == 0:
            ch_stats[ch]["empty"] += 1
        elif n == 1:
            ch_stats[ch]["single"] += 1
        else:
            ch_stats[ch]["multi"] += 1
    report["by_chapter"] = dict(ch_stats)

    # --- By topic ---
    topic_counter = Counter()
    for q in qs:
        for t in q.get('topic_ids', []):
            topic_counter[t] += 1
    report["by_topic"] = {
        t: {
            "count": c,
            "name": TOPIC_NAME_MAP.get(t, "UNKNOWN"),
        }
        for t, c in sorted(topic_counter.items())
    }

    # --- Empty topics list ---
    report["empty_topics"] = [
        {
            "id": q['id'],
            "chapter_id": q.get('chapter_id'),
            "source": q.get('source'),
            "paper_type": q.get('paper_type'),
        }
        for q in empty
    ]

    # --- Over-tagged list ---
    report["over_tagged"] = [
        {
            "id": q['id'],
            "topic_ids": q.get('topic_ids'),
            "topic_names": [TOPIC_NAME_MAP.get(t, "?") for t in q.get('topic_ids', [])],
            "source": q.get('source'),
        }
        for q in multi
    ]

    # --- Known wrong patterns ---
    for q in qs:
        topics = set(q.get('topic_ids', []))
        for pattern, likely_correct, desc in KNOWN_OVER_TAG_PATTERNS:
            if pattern == topics:
                report["known_wrong_patterns"].append({
                    "id": q['id'],
                    "current_topics": list(topics),
                    "current_names": [TOPIC_NAME_MAP.get(t, "?") for t in topics],
                    "likely_correct": likely_correct,
                    "likely_correct_names": [TOPIC_NAME_MAP.get(t, "?") for t in likely_correct],
                    "description": desc,
                    "source": q.get('source'),
                })

    # --- ch00 unassigned ---
    report["ch00_unassigned"] = [
        {
            "id": q['id'],
            "source": q.get('source'),
            "paper_type": q.get('paper_type'),
            "year": q.get('year'),
        }
        for q in qs if q.get('chapter_id') == 'ch00'
    ]

    # --- ch00 paper type analysis ---
    ch00_papers = defaultdict(lambda: {"P1": 0, "P2": 0, "P3": 0, "P4": 0, "P5": 0})
    for q in qs:
        if q.get('chapter_id') == 'ch00':
            pt = q.get('paper_type', '?')
            src = q.get('source', 'unknown')
            ch00_papers[src][pt] += 1
    report["ch00_paper_analysis"] = dict(ch00_papers)

    return report


def fix_known_patterns(db_path, output_path):
    """Fix known over-tagged patterns."""
    data = load_db(db_path)
    qs = data['questions']
    fixes = []

    for q in qs:
        topics = set(q.get('topic_ids', []))
        for pattern, likely_correct, desc in KNOWN_OVER_TAG_PATTERNS:
            if pattern == topics:
                old_topics = q['topic_ids']
                q['topic_ids'] = likely_correct
                fixes.append({
                    "id": q['id'],
                    "old": old_topics,
                    "new": likely_correct,
                    "reason": desc,
                })
                break

    save_db(data, output_path)

    print(f"\n=== Known Pattern Fixes: {len(fixes)} questions ===")
    fix_summary = Counter()
    for f in fixes:
        key = f"{f['old']} → {f['new']}"
        fix_summary[key] += 1
    for pattern, count in fix_summary.most_common():
        print(f"  {count}x: {pattern}")

    return fixes


def fill_empty_topics(db_path, output_path):
    """Fill empty topic_ids with chapter default."""
    data = load_db(db_path)
    qs = data['questions']
    fills = []

    for q in qs:
        if not q.get('topic_ids'):
            ch = q.get('chapter_id', '')
            default = CHAPTER_DEFAULT_TOPIC.get(ch)
            if default:
                old_topics = q.get('topic_ids', [])
                q['topic_ids'] = [default]
                fills.append({
                    "id": q['id'],
                    "chapter": ch,
                    "assigned": default,
                    "topic_name": TOPIC_NAME_MAP.get(default, "UNKNOWN"),
                })

    save_db(data, output_path)

    print(f"\n=== Empty Topic Fills: {len(fills)} questions ===")
    fill_summary = Counter()
    for f in fills:
        fill_summary[f"{f['chapter']} → {f['assigned']}"] += 1
    for pattern, count in fill_summary.most_common():
        print(f"  {count}x: {pattern}")

    return fills


def generate_full_report(db_path, output_report_path):
    """Generate full detailed report as JSON."""
    report = audit(db_path)
    save_db(report, output_report_path)

    # Print summary
    s = report["summary"]
    print(f"\n{'='*60}")
    print(f"CAIE 9701 Topic Audit Report")
    print(f"{'='*60}")
    print(f"Total questions: {s['total_questions']}")
    print(f"Empty topics:    {s['empty_topics']} ({s['empty_pct']}%)")
    print(f"Single topic:    {s['single_topic']} ({s['single_pct']}%)")
    print(f"Multiple topics: {s['multiple_topics']} ({s['multi_pct']}%)")

    print(f"\n{'='*60}")
    print(f"By Chapter:")
    print(f"{'='*60}")
    for ch in sorted(report["by_chapter"].keys()):
        st = report["by_chapter"][ch]
        print(f"  {ch}: total={st['total']}, empty={st['empty']}, single={st['single']}, multi={st['multi']}")

    print(f"\n{'='*60}")
    print(f"Topic Usage Distribution:")
    print(f"{'='*60}")
    for t, info in sorted(report["by_topic"].items(), key=lambda x: -x[1]["count"]):
        name = info["name"]
        count = info["count"]
        bar = "█" * (count // 5)
        print(f"  {t:12s} ({count:4d}) {name:45s} {bar}")

    print(f"\n{'='*60}")
    print(f"Known Wrong Patterns: {len(report['known_wrong_patterns'])} questions")
    print(f"{'='*60}")
    pattern_summary = Counter()
    for item in report["known_wrong_patterns"]:
        key = f"{item['current_topics']} → {item['likely_correct']}"
        pattern_summary[key] += 1
    for pattern, count in pattern_summary.most_common():
        print(f"  {count}x: {pattern}")

    print(f"\n{'='*60}")
    print(f"ch00 Unassigned: {len(report['ch00_unassigned'])} questions")
    print(f"{'='*60}")

    print(f"\nFull report saved to: {output_report_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 topic_audit.py <db.json> [--fix-known] [--fill-empty] [--full-report]")
        sys.exit(1)

    db_path = sys.argv[1]
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found")
        sys.exit(1)

    if "--fix-known" in sys.argv:
        output = db_path.replace(".json", "_fixed_known.json")
        fix_known_patterns(db_path, output)
    elif "--fill-empty" in sys.argv:
        output = db_path.replace(".json", "_filled.json")
        fill_empty_topics(db_path, output)
    elif "--full-report" in sys.argv:
        output = "topic_audit_report.json"
        generate_full_report(db_path, output)
    else:
        # Default: generate report
        report = audit(db_path)
        s = report["summary"]
        print(f"Total: {s['total_questions']} | Empty: {s['empty_topics']} ({s['empty_pct']}%) | Single: {s['single_topic']} | Multi: {s['multiple_topics']}")
        print(f"\nKnown wrong patterns: {len(report['known_wrong_patterns'])}")
        print(f"ch00 unassigned: {len(report['ch00_unassigned'])}")
        print("\nUse --full-report for detailed output, --fix-known to auto-fix patterns, --fill-empty to fill defaults.")


if __name__ == "__main__":
    main()
