// Configuration for FRC Scouting Form
// 2026 Game: REBUILT — Pre-scouting and Match Scouting unified

const CONFIG = {
  tabs: [
    { id: "tab_pre_scouting", label: "Pre-Scouting (Pit)" },
    { id: "tab_match_scouting", label: "Match Scouting" }
  ],

  categories: {
    // PRE-SCOUTING TABS
    team_info: { label: "Team Information", tab: "tab_pre_scouting" },
    robot_hardware: { label: "Robot Hardware", tab: "tab_pre_scouting" },
    expectations: { label: "Performance Expectations", tab: "tab_pre_scouting" },
    pre_photo: { label: "Robot Photo", tab: "tab_pre_scouting", note: "Photos will NOT be sent via QR code due to size limits. Use WiFi submission." },

    // MATCH SCOUTING TABS
    match_info: { label: "Match Information", tab: "tab_match_scouting" },
    pre_match: { label: "Pre-Match Info", tab: "tab_match_scouting" },
    autonomous: { label: "Autonomous (AUTO)", tab: "tab_match_scouting" },
    teleop: { label: "Teleoperated (TELEOP)", tab: "tab_match_scouting" },
    performance: { label: "Advanced Performance Analytics", tab: "tab_match_scouting" },
    endgame: { label: "End Game & Notes", tab: "tab_match_scouting" },
    alliance_rp: { label: "Alliance Ranking Points", tab: "tab_match_scouting" },
    match_photo: { label: "Match Photo", tab: "tab_match_scouting", note: "Direct Server Submission Only." }
  },

  fields: [
    // ==============================================
    // PRE-SCOUTING FIELDS
    // ==============================================
    {
      id: "pre_team_number",
      label: "Team Number",
      type: "number",
      required: true,
      category: "team_info"
    },
    {
      id: "pre_scouter_name",
      label: "Your Name",
      type: "text",
      required: true,
      category: "team_info"
    },
    {
      id: "drive_system",
      label: "Drive System",
      type: "dropdown",
      options: ["Swerve", "Tank", "Mecanum"],
      category: "robot_hardware"
    },
    {
      id: "has_turret",
      label: "Does the robot have a Turret?",
      type: "dropdown",
      options: ["Yes - 360°", "Yes - Limited Range", "No"],
      category: "robot_hardware"
    },
    {
      id: "turret_fuel_shot_at_once",
      label: "How many FUEL is being shot at once?",
      type: "number",
      min: 0,
      category: "robot_hardware"
    },
    {
      id: "can_traverse_trench",
      label: "Can it traverse under the TRENCH?",
      type: "dropdown",
      options: ["Yes", "No"],
      category: "robot_hardware"
    },
    {
      id: "preferred_traversal",
      label: "Preferred Field Traversal",
      type: "dropdown",
      options: ["Bump", "Trench", "Both", "Neither"],
      category: "robot_hardware"
    },
    {
      id: "fuel_capacity",
      label: "FUEL Capacity (How many can it hold?)",
      type: "number",
      min: 0,
      category: "robot_hardware"
    },
    {
      id: "robot_photo_pre",
      label: "Take Robot Photo",
      type: "file",
      accept: "image/*",
      category: "pre_photo",
      wifi_only: true
    },
    {
      id: "expected_auto_fuel",
      label: "Expected AUTO FUEL in Active HUB",
      type: "number",
      min: 0,
      category: "expectations"
    },
    {
      id: "expected_auto_tower_level1",
      label: "Expect TOWER Level 1 in AUTO?",
      type: "checkbox",
      category: "expectations"
    },
    {
      id: "expected_teleop_active",
      label: "Expected TELEOP FUEL in Active HUB",
      type: "number",
      min: 0,
      category: "expectations"
    },
    {
      id: "expected_teleop_inactive",
      label: "Expected TELEOP FUEL in Inactive HUB",
      type: "number",
      min: 0,
      category: "expectations"
    },
    {
      id: "expected_max_tower",
      label: "Expected max TOWER level",
      type: "dropdown",
      options: ["None", "Level 1", "Level 2", "Level 3"],
      category: "expectations"
    },
    {
      id: "expected_minor_fouls",
      label: "Expected minor fouls",
      type: "number",
      min: 0,
      category: "expectations"
    },
    {
      id: "expected_major_fouls",
      label: "Expected major fouls",
      type: "number",
      min: 0,
      category: "expectations"
    },
    {
      id: "expected_energized_rp",
      label: "Expect ENERGIZED RP?",
      type: "checkbox",
      category: "expectations"
    },
    {
      id: "expected_supercharged_rp",
      label: "Expect SUPERCHARGED RP?",
      type: "checkbox",
      category: "expectations"
    },
    {
      id: "expected_traversal_rp",
      label: "Expect TRAVERSAL RP?",
      type: "checkbox",
      category: "expectations"
    },
    {
      id: "expected_shooter_accuracy",
      label: "Estimated Shooter Accuracy",
      type: "dropdown",
      options: ["High (>80%)", "Average (50-80%)", "Low (<50%)", "N/A"],
      category: "expectations"
    },

    // ==============================================
    // MATCH SCOUTING FIELDS
    // ==============================================
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

    // ── Pre-Match
    {
      id: "pre_loaded_fuel",
      label: "How many FUEL is this robot pre-loaded with?",
      type: "counter",
      min: 0,
      max: 8,
      category: "pre_match"
    },

    // ── Autonomous
    {
      id: "auto_fuel_active_hub",
      label: "How many FUEL was scored in the Active HUB during AUTO?",
      type: "counter",
      min: 0,
      max: 999,
      category: "autonomous"
    },
    {
      id: "auto_tower_level1",
      label: "Did this robot reach TOWER Level 1 in AUTO?",
      type: "checkbox",
      category: "autonomous"
    },

    // ── Teleoperated
    {
      id: "teleop_fuel_active_hub",
      label: "How many FUEL was scored in the Active HUB during TELEOP?",
      type: "counter",
      min: 0,
      max: 999,
      category: "teleop"
    },
    {
      id: "teleop_fuel_inactive_hub",
      label: "How many FUEL was scored in the Inactive HUB?",
      type: "counter",
      min: 0,
      max: 999,
      category: "teleop"
    },
    {
      id: "fuel_collection_source",
      label: "Where did this robot primarily collect FUEL?",
      type: "dropdown",
      options: ["Depot", "Neutral Zone", "Outpost"],
      category: "teleop"
    },

    // ── Advanced Performance
    {
      id: "preferred_traversal",
      label: "Preferred Field Traversal",
      type: "dropdown",
      options: ["Bump", "Trench", "Both", "Neither"],
      category: "performance"
    },
    {
      id: "shooter_cadence",
      label: "Shooter Cadence (Speed)",
      type: "dropdown",
      options: ["Fast (< 2 seconds)", "2 seconds to 5 seconds", "Slow (> 5 seconds)", "N/A"],
      category: "performance"
    },
    {
      id: "shooter_accuracy",
      label: "Shooter Accuracy",
      type: "dropdown",
      options: ["High (>80%)", "Average (50-80%)", "Low (<50%)", "N/A"],
      category: "performance"
    },
    {
      id: "defensive_phase_summary",
      label: "Defensive Phase Summary",
      type: "dropdown",
      options: ["Heavy Man-to-Man Defense", "Zone Defense", "Counter-Defense / Evaded", "Pinned / Stuck", "No Defense Played"],
      category: "performance"
    },

    // ── End Game
    {
      id: "max_tower_level",
      label: "What was the highest TOWER Level reached?",
      type: "dropdown",
      options: ["None", "Level 1", "Level 2", "Level 3"],
      category: "endgame"
    },
    {
      id: "minor_fouls",
      label: "How many Minor Fouls did they commit?",
      type: "counter",
      min: 0,
      max: 20,
      category: "endgame"
    },
    {
      id: "major_fouls",
      label: "How many Major Fouls did they commit?",
      type: "counter",
      min: 0,
      max: 10,
      category: "endgame"
    },
    {
      id: "general_notes",
      label: "General Notes",
      type: "textarea",
      category: "endgame"
    },

    // ── Alliance Ranking Points
    {
      id: "energized_rp",
      label: "Did the alliance earn ENERGIZED RP?",
      type: "checkbox",
      category: "alliance_rp"
    },
    {
      id: "supercharged_rp",
      label: "Did the alliance earn SUPERCHARGED RP?",
      type: "checkbox",
      category: "alliance_rp"
    },
    {
      id: "traversal_rp",
      label: "Did the alliance earn TRAVERSAL RP?",
      type: "checkbox",
      category: "alliance_rp"
    },
    {
      id: "robot_photo_match",
      label: "Take Match Photo (Optional)",
      type: "file",
      accept: "image/*",
      category: "match_photo",
      wifi_only: true
    }
  ]
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
}
