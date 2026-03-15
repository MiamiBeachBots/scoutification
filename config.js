// Configuration for FRC Scouting Form
// 2026 Game: REBUILT — Pre-match strategy collection

const CONFIG = {
  fields: [
    // ── Match Information ──────────────────────────────────
    {
      id: "match_number",
      label: "Match Number",
      type: "number",
      required: true,
      min: 1,
      category: "match_info"
    },
    {
      id: "team_number",
      label: "Team Number",
      type: "number",
      required: true,
      category: "match_info"
    },
    {
      id: "alliance",
      label: "Alliance",
      type: "dropdown",
      required: true,
      options: ["Red", "Blue"],
      category: "match_info"
    },
    {
      id: "scouter_name",
      label: "Your Name",
      type: "text",
      required: true,
      category: "match_info"
    },

    // ── Pre-Match ──────────────────────────────────────────
    {
      id: "pre_loaded_fuel",
      label: "How many FUEL is this robot pre-loaded with?",
      type: "counter",
      min: 0,
      max: 8,
      category: "pre_match"
    },

    // ── Autonomous ─────────────────────────────────────────
    {
      id: "auto_fuel_active_hub",
      label: "How many FUEL do you expect in the Active HUB during AUTO?",
      type: "counter",
      min: 0,
      max: 999,
      category: "autonomous"
    },
    {
      id: "auto_tower_level1",
      label: "Do you expect this robot to reach TOWER Level 1 in AUTO?",
      type: "checkbox",
      category: "autonomous"
    },

    // ── Teleoperated ───────────────────────────────────────
    {
      id: "teleop_fuel_active_hub",
      label: "How many FUEL do you expect in the Active HUB during TELEOP?",
      type: "counter",
      min: 0,
      max: 999,
      category: "teleop"
    },
    {
      id: "teleop_fuel_inactive_hub",
      label: "Do you expect any FUEL in the Inactive HUB? (estimate)",
      type: "counter",
      min: 0,
      max: 999,
      category: "teleop"
    },
    {
      id: "fuel_collection_source",
      label: "Where does this robot primarily collect FUEL?",
      type: "dropdown",
      options: ["Depot", "Neutral Zone", "Outpost"],
      category: "teleop"
    },

    // ── End Game ───────────────────────────────────────────
    {
      id: "max_tower_level",
      label: "What is the highest TOWER Level you expect this robot to reach?",
      type: "dropdown",
      options: ["None", "Level 1", "Level 2", "Level 3"],
      category: "endgame"
    },
    {
      id: "minor_fouls",
      label: "How many Minor Fouls do you expect from this robot?",
      type: "counter",
      min: 0,
      max: 20,
      category: "endgame"
    },
    {
      id: "major_fouls",
      label: "How many Major Fouls do you expect from this robot?",
      type: "counter",
      min: 0,
      max: 10,
      category: "endgame"
    },

    // ── Alliance Ranking Points ────────────────────────────
    {
      id: "energized_rp",
      label: "Do you expect ENERGIZED RP? (alliance scores 100+ Active HUB FUEL)",
      type: "checkbox",
      category: "alliance_rp"
    },
    {
      id: "supercharged_rp",
      label: "Do you expect SUPERCHARGED RP? (alliance scores 360+ Active HUB FUEL)",
      type: "checkbox",
      category: "alliance_rp"
    },
    {
      id: "traversal_rp",
      label: "Do you expect TRAVERSAL RP? (alliance earns 50+ Tower Points)",
      type: "checkbox",
      category: "alliance_rp"
    }
  ],

  categories: {
    match_info:  "Match Information",
    pre_match:   "Pre-Match",
    autonomous:  "Autonomous (AUTO) — Expectations",
    teleop:      "Teleoperated (TELEOP) — Expectations",
    endgame:     "End Game — Expectations",
    alliance_rp: "Alliance Ranking Points — Predictions"
  }
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
}
