# Ideas: a living register

**Started:** 23 October 2026 · **Owner:** Yash
**State:** living document. Nothing here is approved to build unless its entry says **Agreed**
and gives a date. Nothing in this file is a code change.

## How to use this file

**For the owner:** skim the map. Tell the assistant `KEEP`, `LATER` or `NO` for any entry, in
chat. Your words and the date get recorded in the entry.

**For the assistant:**
- Add new ideas under the right theme with the next free ID. Never renumber.
- `KEEP` means "write a plan", not "build". Agreed ideas get their own `docs/<idea>-plan.md`.
- If an idea is rejected, record why, so it is never pitched again.
- When an idea ships, record the date and what was checked. Leave the entry.

Statuses: **Idea**, **Discussing**, **Agreed**, **In build**, **Shipped**, **Parked** (with the
condition to revisit), **Rejected** (with the reason).

## The map

### A. The core (version 1)

| ID | Idea | Status |
|---|---|---|
| `AU-01` | The Oath: sign up with a fighter name and an oath; data encrypted on the device | Built 25 Oct 2026, not deployed |
| `GH-01` | Your ghost on every set, from the last time you did the exercise | Built 25 Oct 2026, not deployed |
| `BS-01` | Boss fights against your best-ever self, summoned when you're close | Built 25 Oct 2026, not deployed |
| `EP-01` | Episodes: every session numbered, with a plain title from what happened | Built 25 Oct 2026, not deployed |
| `HI-01` | History and progress charts | Built 25 Oct 2026, not deployed |
| `LG-01` | Logging: pick exercises, then repeat; tick or correct each set | Built 25 Oct 2026, not deployed |

### B. Next candidates

| ID | Idea | Status |
|---|---|---|
| `TG-01` | Training Grounds: a place outside the village, built from your won blocks. Each muscle group builds its own spot (push wall, pull tower, leg stairs, arm forge), neglect grows grass over it, ghost blocks show as dashed outlines, bosses become pillars, sky follows light/dark. Plus a power level (passing 9000 is an easter egg), forms per exercise, and ranks from consistency | **Agreed** 26 Oct 2026, valley + dojo + climb built 26 Oct 2026 (owner: "TRAINING GROUND", on neglect showing: "NO I LOVE IT", on power level, forms and ranks: "LOVE ALL OF IT", "THis is it"). Mockups next |
| `BR-01` | Stack brand: blocks as the tracking shape, yellow on concrete, new icon | **Agreed** 26 Oct 2026 (owner: "lets do stack"). Built 26 Oct 2026 |
| `DM-01` | Dark and light mode, Auto follows the phone | **Agreed** 26 Oct 2026 (owner: "add a dark/light mode thing to it, deploy it"). Built 26 Oct 2026 |
| `OF-01` | Offline first: the app opens and saves with no signal, and syncs by itself when back online | **Agreed** 26 Oct 2026 (owner: "its always synced and live aand even works without the internet (only syncs when internet th)"). Built 26 Oct 2026 |
| `AU-02` | Change your oath (re-wrap the key, no data re-encryption needed) | Idea |
| `SH-01` | Share an episode card as an image | Idea |
| `EG-01` | Easter eggs and secrets to find (owner wants these, 24 Oct 2026) | Idea |
| `RT-01` | Rest timer between sets | Idea |
| `PL-01` | The app plans today's workout from what's rested | Idea |

### C. The world and the character

| ID | Idea | Status |
|---|---|---|
| `WD-01` | A world or scene (dojo, mountain) that reacts to what happened in a session | Parked |
| `CH-01` | A 3D or illustrated character with a see-through blue ghost copy | Parked |

**Why parked (25 Oct 2026):** five rounds of mockups didn't land; animating the character for
each exercise doesn't scale (owner). **Revisit when:** the owner has used v1 at the gym for a week
or two and knows where a world would actually add something. Mockups are in the "Training Arc:
today's workout" design canvas on claude.ai. Liked so far: the ghost walking into the dojo, a
see-through blue copy of your character (not a cartoon ghost), the dojo at the foot of a
mountain idea.

### D. Later

| ID | Idea | Status |
|---|---|---|
| `NU-01` | Nutrition as one-tap meal cards; must handle Indian vegetarian food | Parked until the workout loop is in use |
| `VL-01` | Connect with Vishal's planner (a finished workout shows up in his village) | Parked: siblings first, connected later (owner, 24 Oct 2026) |

## Not pursued (and why)

| Idea | Why |
|---|---|
| Named multi-week "arcs" with a goal | Owner didn't like it (24 Oct 2026). Bosses appear on their own instead. |
| A predicting "smart coach" as the selling point | Owner: "thats obvious nothing cool about it" (24 Oct 2026). Fine under the hood. |
| Retro arcade, ink brush, dark "system" HUD, shonen poster looks | Owner rejected each (23 to 24 Oct 2026). |
| A girl character as the stand-in | Owner disliked it (24 Oct 2026). |
| Kakashi, Goku or other licensed characters | Owned by their studios; the app is meant to be public. |
| Calling an AI model inside the app | Claude is the coding partner only (owner, 23 Oct 2026). |
| Making money from this app | Money is a separate project (owner, 23 Oct 2026). |

## Change log

- **26 October 2026:** Training Grounds art direction set: side view, richly illustrated, our own (owner: "Side views", "Rich illustrations, super rich", "make it our own"). Block-cube version rejected (owner: "thats just a bunch on blocks you're making it look like tetris"). Rebuilt as one valley with depth, one scale, paths and a stream. Rule: nothing floats; objects on the hill are placed on its measured surface and the build refuses anything hovering (owner asked for physics like Vishal's: "nothing is going in directions or ways it isn't supposed to"). Tap to explore agreed (owner: "tapping on the elements to go into them"): the valley shows each place's base, tapping opens it. First two inside views drawn: the climb (hill, legs) and the dojo (rank, power level, forms; replaces the You screen) (owner: "do both dojo and hill").
- **26 October 2026:** TG-01 Training Grounds agreed as the world (sibling to Vishal's village: his is where you live, yours is where you train). Anime feel from Naruto, Demon Slayer, DBZ, without their names or art. Block silhouettes rejected (owner: "sounds silly").
- **26 October 2026:** BR-01 (Stack brand) and DM-01 (dark mode) agreed and built.
- **26 October 2026:** OF-01 agreed and built: works offline, syncs on its own, a sync chip on
  home shows the state.
- **25 October 2026:** version 1 built (AU-01, GH-01, BS-01, EP-01, HI-01, LG-01). World and
  character parked. Register rewritten around the shipped core.
- **24 October 2026:** pivot to logging first; product story agreed (ghost, bosses, episodes,
  dojo).
- **23 October 2026:** register started from the brainstorm.
