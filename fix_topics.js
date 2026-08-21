#!/usr/bin/env node
/**
 * CAIE 9701 Topic Audit & Fix Script (Node.js)
 * Based on Seven's topic_audit.py, adapted for website chapter_id numbering.
 *
 * Usage: node fix_topics.js
 */
const fs = require('fs');
const path = require('path');

const DB_PATH = path.join(__dirname, 'db.json');

// ── Seven's TOPIC_NAME_MAP (syllabus chapter IDs) ──────────────────────────
const TOPIC_NAME_MAP = {
  "ch01_t01": "Isotopes & relative atomic mass",
  "ch01_t02": "Mass spectrometry",
  "ch01_t03": "Electronic structure",
  "ch01_t04": "Ionisation energy",
  "ch01_t05": "Atomic orbitals",
  "ch01_t06": "Periodic trends (AS)",
  "ch03_t01": "Mole concept & Avogadro constant",
  "ch03_t02": "Relative atomic/molecular mass",
  "ch03_t03": "Empirical & molecular formula",
  "ch03_t04": "Chemical equations & stoichiometry",
  "ch03_t05": "Limiting reagent & yield",
  "ch03_t06": "Gas volumes & molar volume",
  "ch03_t07": "Solutions & concentration",
  "ch04_t01": "Ionic bonding",
  "ch04_t02": "Covalent bonding",
  "ch04_t03": "Metallic bonding",
  "ch04_t04": "VSEPR & molecular shapes",
  "ch04_t05": "Electronegativity & bond polarity",
  "ch04_t06": "Intermolecular forces",
  "ch04_t07": "σ and π bonds",
  "ch04_t08": "Delocalisation & resonance",
  "ch04_t09": "Bonding & physical properties",
  "ch05_t01": "Gases & ideal gas equation",
  "ch05_t02": "Kinetic theory of gases",
  "ch05_t03": "Liquids & vapour pressure",
  "ch05_t04": "Solids & crystal structures",
  "ch05_t05": "Phase changes",
  "ch05_t06": "Solutions & colligative properties",
  "ch05_t07": "Real gases & deviations",
  "ch06_t01": "Exothermic & endothermic reactions",
  "ch06_t02": "Standard enthalpy changes",
  "ch06_t03": "Hess's Law",
  "ch06_t04": "Bond energies",
  "ch06_t05": "Enthalpy of solution/hydration",
  "ch06_t06": "Calorimetry",
  "ch07_t01": "Oxidation numbers",
  "ch07_t02": "Redox reactions & agents",
  "ch07_t03": "Balancing redox equations",
  "ch07_t04": "Redox titrations",
  "ch07_t05": "Electrochemical cells (AS)",
  "ch08_t01": "Reversible reactions & dynamic equilibrium",
  "ch08_t02": "Le Chatelier's principle",
  "ch08_t03": "Equilibrium constants (Kc, Kp)",
  "ch08_t04": "Industrial applications",
  "ch08_t05": "Acid-base equilibria",
  "ch08_t06": "Buffer solutions",
  "ch08_t07": "Solubility product (Ksp)",
  "ch08_t08": "Partition coefficient",
  "ch09_t01": "Rate of reaction & measurement",
  "ch09_t02": "Collision theory",
  "ch09_t03": "Factors affecting rate",
  "ch09_t04": "Rate equations & order",
  "ch09_t05": "Rate-determining step",
  "ch09_t06": "Catalysis",
  "ch09_t07": "Arrhenius equation",
  "ch10_t01": "Periodic table structure",
  "ch10_t02": "Periodic trends (physical)",
  "ch10_t03": "Periodic trends (chemical)",
  "ch10_t04": "Third period elements",
  "ch10_t05": "Transition elements (intro)",
  "ch10_t06": "Uses of periodic table",
  "ch11_t01": "Group 2 metals & reactions",
  "ch11_t02": "Thermal stability",
  "ch11_t03": "Solubility trends",
  "ch11_t04": "Uses of Group 2 compounds",
  "ch11_t05": "Anomalous properties of Be",
  "ch12_t01": "Halogens & their properties",
  "ch12_t02": "Halogen reactions",
  "ch12_t03": "Halide ions & tests",
  "ch12_t04": "Disproportionation & uses",
  "ch13_t01": "Nitrogen & its compounds",
  "ch13_t02": "Sulfur & its compounds",
  "ch13_t03": "Environmental chemistry",
  "ch13_t04": "Fertilisers",
  "ch14_t01": "Homologous series & functional groups",
  "ch14_t02": "Nomenclature",
  "ch14_t03": "Structural isomerism",
  "ch14_t04": "Stereoisomerism (cis/trans)",
  "ch14_t05": "Reaction mechanisms (intro)",
  "ch14_t06": "Organic analysis techniques",
  "ch15_t01": "Alkanes & free radical substitution",
  "ch15_t02": "Alkenes & electrophilic addition",
  "ch15_t03": "Markovnikov's rule",
  "ch15_t04": "Polymerisation (addition)",
  "ch15_t05": "Cracking & reforming",
  "ch15_t06": "Environmental impact",
  "ch16_t01": "Nucleophilic substitution (SN1/SN2)",
  "ch16_t02": "Elimination reactions",
  "ch16_t03": "CFCs & ozone depletion",
  "ch16_t04": "Uses & properties",
  "ch17_t01": "Alcohols: reactions & synthesis",
  "ch17_t02": "Esters: formation & hydrolysis",
  "ch17_t03": "Phenol",
  "ch17_t04": "Carboxylic acids & acyl chlorides",
  "ch18_t01": "Aldehydes & ketones: reactions",
  "ch18_t02": "2,4-DNPH & Tollens' reagent",
  "ch18_t03": "Reduction of carbonyls",
  "ch18_t04": "Nucleophilic addition mechanism",
  "ch18_t05": "Iodoform reaction",
  "ch19_t01": "Born-Haber cycles",
  "ch19_t02": "Lattice energy factors",
  "ch20_t01": "Electrolysis",
  "ch20_t02": "Electrode potentials & Nernst",
  "ch21_t01": "Acids, bases, buffers & Ksp (A2)",
  "ch22_t02": "Rate equations & catalysis (A2)",
  "ch23_t01": "Entropy & Gibbs free energy",
  "ch24_t01": "Transition elements: complexes & colour",
  "ch25_t01": "Benzene & electrophilic substitution",
  "ch26_t01": "Carboxylic acids: acidity & reactions",
  "ch26_t02": "Acyl chlorides",
  "ch26_t03": "Esterification & hydrolysis",
  "ch26_t04": "Amides",
  "ch26_t05": "Acidity comparison",
  "ch26_t06": "Synthetic applications",
  "ch27_t01": "Amines, amides, amino acids & azo",
  "ch28_t01": "Addition polymerisation",
  "ch28_t02": "Condensation polymerisation",
  "ch28_t03": "Polyesters & polyamides",
  "ch28_t04": "Polymer degradation",
  "ch29_t01": "Multi-step organic synthesis",
  "ch30_t01": "NMR, chromatography & mass spec (A2)",
  // ch22_t01 not in Seven's map — treat as ch22_t02
  "ch22_t01": "Rate equations & catalysis (A2)",
  // ch31 topics (not in Seven's map, keep from existing data)
  "ch31_t01": "Analytical Techniques (AS)",
};

// ── Known over-tag patterns (from Seven's script) ──────────────────────────
const KNOWN_OVER_TAG_PATTERNS = [
  [new Set(["ch01_t02", "ch01_t03"]), ["ch01_t01"], "Mass spec + Electronic structure → Isotopes"],
  [new Set(["ch01_t04", "ch01_t05"]), ["ch01_t04"], "Ionisation energy + Atomic orbitals → IE"],
  [new Set(["ch03_t01", "ch03_t02"]), ["ch03_t01"], "Mole concept + Relative mass → Mole concept"],
  [new Set(["ch03_t04", "ch03_t05"]), ["ch03_t04"], "Stoichiometry + Limiting reagent → Stoichiometry"],
  [new Set(["ch05_t04", "ch05_t05"]), ["ch05_t04"], "Solids + Phase changes → Solids"],
  [new Set(["ch06_t05", "ch06_t06"]), ["ch06_t05"], "Enthalpy of solution + Calorimetry"],
  [new Set(["ch08_t06", "ch08_t07"]), ["ch08_t06"], "Buffers + Ksp"],
  [new Set(["ch08_t04", "ch08_t05"]), ["ch08_t04"], "Industrial + Acid-base"],
  [new Set(["ch04_t03", "ch04_t09"]), ["ch04_t03"], "Metallic bonding + Physical properties"],
  [new Set(["ch07_t03", "ch07_t04"]), ["ch07_t03"], "Balancing redox + Redox titrations"],
  [new Set(["ch10_t03", "ch10_t04"]), ["ch10_t03"], "Periodic trends chemical + Third period"],
];

// ── Website chapter_id → Syllabus chapter_id mapping ───────────────────────
const WEBSITE_TO_SYLLABUS = {
  ch01: 'ch01', ch02: 'ch03', ch03: 'ch04', ch04: 'ch05',
  ch05: 'ch06', ch06: 'ch07', ch07: 'ch08', ch08: 'ch09',
  ch09: 'ch10', ch10: 'ch11', ch11: 'ch12', ch12: 'ch13',
  ch13: 'ch14', ch14: 'ch15', ch15: 'ch16', ch16: 'ch17',
  ch17: 'ch18', ch18: 'ch18', ch19: 'ch19', ch20: 'ch28',
  ch21: 'ch21', ch22: 'ch22', ch23: 'ch23', ch24: 'ch20',
  ch25: 'ch21', ch26: 'ch22', ch27: 'ch27', ch28: 'ch24',
  ch29: 'ch29', ch30: 'ch25', ch31: 'ch31', ch32: 'ch17',
  ch33: 'ch26', ch34: 'ch27', ch35: 'ch28', ch36: 'ch29',
  ch37: 'ch30',
};

// ── Default topic per syllabus chapter (from Seven's script) ────────────────
const CHAPTER_DEFAULT_TOPIC = {
  "ch01": "ch01_t01", "ch03": "ch03_t04", "ch04": "ch04_t02",
  "ch05": "ch05_t01", "ch06": "ch06_t01", "ch07": "ch07_t02",
  "ch08": "ch08_t01", "ch09": "ch09_t01", "ch10": "ch10_t01",
  "ch11": "ch11_t01", "ch12": "ch12_t01", "ch13": "ch13_t01",
  "ch14": "ch14_t01", "ch15": "ch15_t01", "ch16": "ch16_t01",
  "ch17": "ch17_t01", "ch18": "ch18_t01", "ch19": "ch19_t01",
  "ch20": "ch20_t01", "ch21": "ch21_t01", "ch22": "ch22_t02",
  "ch23": "ch23_t01", "ch24": "ch24_t01", "ch25": "ch25_t01",
  "ch26": "ch26_t01", "ch27": "ch27_t01", "ch28": "ch28_t01",
  "ch29": "ch29_t01", "ch30": "ch30_t01",
  "ch31": "ch31_t01", // not in Seven's map, keep existing
};

// ── Main ────────────────────────────────────────────────────────────────────
function main() {
  const db = JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
  const qs = db.questions;
  let fixCount = 0, fillCount = 0;
  const fixLog = {}, fillLog = {};

  // Step 1: Fix known over-tag patterns
  for (const q of qs) {
    const topics = new Set(q.topic_ids || []);
    for (const [pattern, likely, desc] of KNOWN_OVER_TAG_PATTERNS) {
      if (pattern.size === topics.size && [...pattern].every(t => topics.has(t))) {
        const old = JSON.stringify(q.topic_ids);
        q.topic_ids = [...likely];
        fixCount++;
        const key = `${old} → ${JSON.stringify(likely)}`;
        fixLog[key] = (fixLog[key] || 0) + 1;
        break;
      }
    }
  }

  // Step 1b: Fix ch22_t01 → ch22_t02 (not in Seven's syllabus map)
  let ch22fix = 0;
  for (const q of qs) {
    if (q.topic_ids && q.topic_ids.includes('ch22_t01')) {
      q.topic_ids = q.topic_ids.map(t => t === 'ch22_t01' ? 'ch22_t02' : t);
      ch22fix++;
    }
  }

  // Step 2: Fill empty topics
  for (const q of qs) {
    if (!q.topic_ids || q.topic_ids.length === 0) {
      const webCh = q.chapter_id;
      if (webCh === 'ch00') continue; // skip ch00
      const syllabusCh = WEBSITE_TO_SYLLABUS[webCh];
      if (!syllabusCh) continue;
      const defaultTopic = CHAPTER_DEFAULT_TOPIC[syllabusCh];
      if (!defaultTopic) continue;
      q.topic_ids = [defaultTopic];
      fillCount++;
      const key = `${webCh} → ${defaultTopic}`;
      fillLog[key] = (fillLog[key] || 0) + 1;
    }
  }

  // Save
  fs.writeFileSync(DB_PATH, JSON.stringify(db, null, 2));

  // Report
  console.log('=== Fix Results ===');
  console.log(`Known pattern fixes: ${fixCount}`);
  for (const [k, v] of Object.entries(fixLog).sort((a,b) => b[1]-a[1])) {
    console.log(`  ${v}x: ${k}`);
  }
  console.log(`ch22_t01 → ch22_t02: ${ch22fix}`);
  console.log(`\nEmpty topic fills: ${fillCount}`);
  for (const [k, v] of Object.entries(fillLog).sort((a,b) => b[1]-a[1])) {
    console.log(`  ${v}x: ${k}`);
  }

  // Verify
  let stillEmpty = 0, stillMulti = 0;
  for (const q of qs) {
    if (!q.topic_ids || q.topic_ids.length === 0) stillEmpty++;
    if (q.topic_ids && q.topic_ids.length > 1) stillMulti++;
  }
  console.log(`\n=== Post-fix Status ===`);
  console.log(`Total: ${qs.length} | Empty: ${stillEmpty} | Multi: ${stillMulti}`);
  console.log(`  (ch00 empty: ${qs.filter(q => q.chapter_id === 'ch00' && (!q.topic_ids || q.topic_ids.length === 0)).length})`);
}

main();
