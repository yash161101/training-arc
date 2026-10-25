export const GROUPS = ['Back', 'Chest', 'Shoulders', 'Arms', 'Legs', 'Core'];

const raw = [
  ['pull-ups', 'Pull-ups', 'Back', 1],
  ['chin-ups', 'Chin-ups', 'Back', 1],
  ['lat-pulldown', 'Lat pulldown', 'Back', 0],
  ['seated-row', 'Seated cable row', 'Back', 0],
  ['barbell-row', 'Barbell row', 'Back', 0],
  ['db-row', 'One-arm dumbbell row', 'Back', 0],
  ['t-bar-row', 'T-bar row', 'Back', 0],
  ['deadlift', 'Deadlift', 'Back', 0],
  ['rack-pull', 'Rack pull', 'Back', 0],
  ['inverted-row', 'Inverted row', 'Back', 1],
  ['face-pull', 'Face pull', 'Shoulders', 0],
  ['push-ups', 'Push-ups', 'Chest', 1],
  ['bench-press', 'Bench press', 'Chest', 0],
  ['incline-bench', 'Incline bench press', 'Chest', 0],
  ['db-bench', 'Dumbbell bench press', 'Chest', 0],
  ['incline-db-press', 'Incline dumbbell press', 'Chest', 0],
  ['chest-press', 'Chest press machine', 'Chest', 0],
  ['cable-fly', 'Cable fly', 'Chest', 0],
  ['pec-deck', 'Pec deck', 'Chest', 0],
  ['dips', 'Dips', 'Chest', 1],
  ['ohp', 'Overhead press', 'Shoulders', 0],
  ['db-shoulder-press', 'Dumbbell shoulder press', 'Shoulders', 0],
  ['shoulder-press-machine', 'Shoulder press machine', 'Shoulders', 0],
  ['lateral-raise', 'Lateral raise', 'Shoulders', 0],
  ['cable-lateral-raise', 'Cable lateral raise', 'Shoulders', 0],
  ['rear-delt-fly', 'Rear delt fly', 'Shoulders', 0],
  ['shrugs', 'Shrugs', 'Shoulders', 0],
  ['bicep-curl', 'Dumbbell curl', 'Arms', 0],
  ['barbell-curl', 'Barbell curl', 'Arms', 0],
  ['hammer-curl', 'Hammer curl', 'Arms', 0],
  ['preacher-curl', 'Preacher curl', 'Arms', 0],
  ['cable-curl', 'Cable curl', 'Arms', 0],
  ['incline-curl', 'Incline dumbbell curl', 'Arms', 0],
  ['tricep-pushdown', 'Tricep pushdown', 'Arms', 0],
  ['rope-pushdown', 'Rope pushdown', 'Arms', 0],
  ['overhead-extension', 'Overhead tricep extension', 'Arms', 0],
  ['skull-crusher', 'Skull crusher', 'Arms', 0],
  ['close-grip-bench', 'Close-grip bench press', 'Arms', 0],
  ['bench-dips', 'Bench dips', 'Arms', 1],
  ['squat', 'Squat', 'Legs', 0],
  ['goblet-squat', 'Goblet squat', 'Legs', 0],
  ['leg-press', 'Leg press', 'Legs', 0],
  ['rdl', 'Romanian deadlift', 'Legs', 0],
  ['leg-extension', 'Leg extension', 'Legs', 0],
  ['leg-curl', 'Leg curl', 'Legs', 0],
  ['hip-thrust', 'Hip thrust', 'Legs', 0],
  ['split-squat', 'Bulgarian split squat', 'Legs', 0],
  ['calf-raise', 'Calf raise', 'Legs', 0],
  ['bodyweight-squat', 'Bodyweight squat', 'Legs', 1],
  ['plank', 'Plank (seconds)', 'Core', 1],
  ['hanging-leg-raise', 'Hanging leg raise', 'Core', 1],
  ['cable-crunch', 'Cable crunch', 'Core', 0],
  ['ab-wheel', 'Ab wheel rollout', 'Core', 1],
  ['crunches', 'Crunches', 'Core', 1],
  ['russian-twist', 'Russian twist', 'Core', 1],
];

export const LIBRARY = raw.map(([id, name, group, bw]) => ({ id, name, group, bw: !!bw }));

export function allExercises(custom = []) {
  return [...LIBRARY, ...custom];
}

export function findExercise(id, custom = []) {
  return allExercises(custom).find((e) => e.id === id) || null;
}
