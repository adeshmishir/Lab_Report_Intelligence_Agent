export const demoReports = [
  {
    id: 1,
    name: "CBC Report",
    date: "2026-08-12",
    dateFormatted: "12 Aug 2026",
    tests: 8,
    status: "processed",
    fileName: "cbc_report_aug12.pdf",
    results: [
      { test: "Hemoglobin", value: "13.8", unit: "g/dL", reference: "13.0–17.0", status: "normal" },
      { test: "Hematocrit", value: "41.2", unit: "%", reference: "38.5–50.0", status: "normal" },
      { test: "WBC", value: "7.5", unit: "×10³/µL", reference: "4.5–11.0", status: "normal" },
      { test: "Platelets", value: "245", unit: "×10³/µL", reference: "150–400", status: "normal" },
      { test: "HbA1c", value: "5.9", unit: "%", reference: "4.0–5.6", status: "high" },
      { test: "MCV", value: "88.0", unit: "fL", reference: "80.0–100.0", status: "normal" },
      { test: "MCH", value: "29.5", unit: "pg", reference: "27.0–33.0", status: "normal" },
      { test: "RDW", value: "13.2", unit: "%", reference: "11.5–14.5", status: "normal" },
    ],
    rawText: "Complete Blood Count (CBC)\nDate: 12 Aug 2026\nPatient: Sample Patient\n\nHemoglobin: 13.8 g/dL (Ref: 13.0–17.0)\nHematocrit: 41.2% (Ref: 38.5–50.0)\nWBC: 7.5 ×10³/µL (Ref: 4.5–11.0)\nPlatelets: 245 ×10³/µL (Ref: 150–400)\nHbA1c: 5.9% (Ref: 4.0–5.6) [HIGH]\nMCV: 88.0 fL (Ref: 80.0–100.0)\nMCH: 29.5 pg (Ref: 27.0–33.0)\nRDW: 13.2% (Ref: 11.5–14.5)",
  },
  {
    id: 2,
    name: "Metabolic Panel",
    date: "2026-08-02",
    dateFormatted: "02 Aug 2026",
    tests: 10,
    status: "processed",
    fileName: "metabolic_panel_aug02.pdf",
    results: [
      { test: "Glucose", value: "102", unit: "mg/dL", reference: "70–100", status: "high" },
      { test: "BUN", value: "15", unit: "mg/dL", reference: "7–20", status: "normal" },
      { test: "Creatinine", value: "0.9", unit: "mg/dL", reference: "0.7–1.3", status: "normal" },
      { test: "Sodium", value: "140", unit: "mEq/L", reference: "136–145", status: "normal" },
      { test: "Potassium", value: "4.1", unit: "mEq/L", reference: "3.5–5.0", status: "normal" },
      { test: "Chloride", value: "101", unit: "mEq/L", reference: "98–106", status: "normal" },
      { test: "Calcium", value: "9.5", unit: "mg/dL", reference: "8.5–10.5", status: "normal" },
      { test: "Total Protein", value: "7.0", unit: "g/dL", reference: "6.0–8.3", status: "normal" },
      { test: "Albumin", value: "4.2", unit: "g/dL", reference: "3.5–5.0", status: "normal" },
      { test: "ALP", value: "65", unit: "U/L", reference: "44–147", status: "normal" },
    ],
    rawText: "Comprehensive Metabolic Panel (CMP)\nDate: 02 Aug 2026\nPatient: Sample Patient\n\nGlucose: 102 mg/dL (Ref: 70–100) [HIGH]\nBUN: 15 mg/dL (Ref: 7–20)\nCreatinine: 0.9 mg/dL (Ref: 0.7–1.3)\nSodium: 140 mEq/L (Ref: 136–145)\nPotassium: 4.1 mEq/L (Ref: 3.5–5.0)\nChloride: 101 mEq/L (Ref: 98–106)\nCalcium: 9.5 mg/dL (Ref: 8.5–10.5)\nTotal Protein: 7.0 g/dL (Ref: 6.0–8.3)\nAlbumin: 4.2 g/dL (Ref: 3.5–5.0)\nALP: 65 U/L (Ref: 44–147)",
  },
  {
    id: 3,
    name: "Lipid Profile",
    date: "2026-07-24",
    dateFormatted: "24 Jul 2026",
    tests: 6,
    status: "processed",
    fileName: "lipid_profile_jul24.pdf",
    results: [
      { test: "Total Cholesterol", value: "210", unit: "mg/dL", reference: "<200", status: "high" },
      { test: "LDL", value: "135", unit: "mg/dL", reference: "<100", status: "high" },
      { test: "HDL", value: "52", unit: "mg/dL", reference: ">40", status: "normal" },
      { test: "Triglycerides", value: "145", unit: "mg/dL", reference: "<150", status: "normal" },
      { test: "VLDL", value: "29", unit: "mg/dL", reference: "5–40", status: "normal" },
      { test: "HbA1c", value: "5.8", unit: "%", reference: "4.0–5.6", status: "high" },
    ],
    rawText: "Lipid Profile\nDate: 24 Jul 2026\nPatient: Sample Patient\n\nTotal Cholesterol: 210 mg/dL (Ref: <200) [HIGH]\nLDL: 135 mg/dL (Ref: <100) [HIGH]\nHDL: 52 mg/dL (Ref: >40)\nTriglycerides: 145 mg/dL (Ref: <150)\nVLDL: 29 mg/dL (Ref: 5–40)\nHbA1c: 5.8% (Ref: 4.0–5.6) [HIGH]",
  },
];

export const demoTrendData = {
  "HbA1c": [
    { date: "24 Jul 2026", value: 5.8 },
    { date: "02 Aug 2026", value: null },
    { date: "12 Aug 2026", value: 5.9 },
  ],
  "Glucose": [
    { date: "24 Jul 2026", value: null },
    { date: "02 Aug 2026", value: 102 },
    { date: "12 Aug 2026", value: null },
  ],
  "LDL": [
    { date: "24 Jul 2026", value: 135 },
    { date: "02 Aug 2026", value: null },
    { date: "12 Aug 2026", value: null },
  ],
  "Hemoglobin": [
    { date: "24 Jul 2026", value: null },
    { date: "02 Aug 2026", value: null },
    { date: "12 Aug 2026", value: 13.8 },
  ],
};

export const suggestedQuestions = [
  "How has my HbA1c changed across reports?",
  "Which results moved outside the reference range?",
  "What was my latest LDL result?",
  "Compare my latest lipid panel with the previous one.",
];
