# Training Arc: the product story

**Written:** 24 October 2026, from the owner's choices in chat and a round of research.
**State:** the agreed direction. Version 1 of the core was built on 25 October 2026 (see AGENTS.md, Latest).

## In one line

**A gym tracker where your rival is you.** Every set, you race the person you were last time.
Now and then, your best-ever self shows up as a boss.

## Who it's for

Yash first: lifts 3 to 4 times a week, tracks pull-ups and push-ups in an Excel sheet today,
steps in his phone's fitness app, loves anime, finds most fitness apps boring. Later, anyone who
lifts and is tired of spreadsheet trackers. Built for one person first, open to others later.

## The problems it solves (owner's words, 23 to 24 Oct)

- Logging is tedious, and by the time you sit down to log, you've forgotten what you did.
- Existing apps are boring to look at and give no reason to come back.
- No app tells you what to train next in a way that fits you.
- (Later) Food tracking ignores Indian vegetarian food.

## The four pieces

### 1. The ghost (the heart of it)

On every set, your ghost from last time is right there: "Ghost: 8 reps × 17.5 kg". You do your
set, tick it or correct it, and see straight away whether you beat it.

- Beat it: a small, quick moment. "Ghost beaten."
- Match it: fine. "Tied with your ghost."
- Fall short: no drama. The ghost keeps its number for next time.
- In the dojo, your ghost is drawn as a see-through version of you, training at the same station.

Why this works: strength apps like Hevy already show last time's numbers, but as a grey column
in a table. Freeletics turned the same data into a live "ahead or behind your best" race and
calls it ghost mode. We make the ghost a character you can see, and put it on every set.

### 2. Boss fights

The boss is **your best-ever self** on one lift: "Boss: 9 pull-ups, set 5 weeks ago."

- The app summons a boss when your recent numbers say you're close to beating it. You never get
  thrown at a boss you can't touch.
- A boss fight is one big set at the end of a normal session: max reps or a heavier weight.
- Win, and your new best becomes the next boss. **Every boss you beat becomes the next boss.**
- Lose, and it ends with "To be continued". The boss comes back in a couple of weeks.

Why this works: Ring Fit Adventure keeps people exercising with boss battles where your real
effort is the attack. Quest2Fitness puts fantasy monsters on every set. Ours are real numbers
from your own history, so beating one means you actually got stronger.

### 3. Episodes

Every session is an episode, numbered, with a plain title made from what happened:

- "Ep. 14 · New best: 9 pull-ups"
- "Ep. 15 · Ghost beaten on 6 of 8 sets"
- "Ep. 16 · Boss: 10 pull-ups · To be continued"

Your history is an episode list you scroll through, not a spreadsheet. Each episode card can be
shared as an image.

(The owner did **not** want named multi-week "arcs" with a set goal, 24 Oct 2026. Bosses appear
on their own instead.)

### 4. The dojo

The home screen. A bright anime daytime courtyard where the episodes happen.

- Each muscle group is a training station: the log (back), the rope (arms), the stones (chest),
  the sandbag (legs), more later.
- A station shows its condition: rested and ready, or still recovering. Today's stations are
  marked.
- Your figure and your ghost train in the courtyard.
- Beaten bosses leave something behind in the dojo (a banner, a mark on the wall), so the place
  slowly fills with your wins.
- Secrets to find: the roof cat, the cherry tree, more later. "Secrets n/12".

## Signing in: The Oath

You join with a fighter name and an oath: a sentence only you would say, at least 4 words. To
come back, the app asks you to "Say your oath" and stamps OATH ACCEPTED. The oath never leaves
your phone; it unlocks the key that encrypts everything you log. Nobody can reset a forgotten
oath, and the app says so plainly at sign up. (Owner wanted something unique, like a passphrase
but not a copy of Vishal's, 25 Oct 2026.)

## Logging (the part everything rests on)

- Version 1: pick exercises the first time; after that, "Repeat Ep. N" gives the same session
  prefilled with your ghost's numbers. (Owner picked "pick, then repeat", 25 Oct 2026.) The app
  planning the day from what's rested comes later (`PL-01`).
- You see the whole workout as one list.
- Each set: tick it, or correct it ("did 10, not 12"). Under 10 seconds.
- No fixed split. The app picks a focus from what's rested; you can change it.
- *Open:* how equipment is handled. Proposed: a Swap button, and the app learns your gym from
  what you swap.
- *Open:* the exact set controls (tap, +/-), to be mocked up.

## What we won't do

- **No daily streak guilt.** Missed days don't reset anything. Research on streak design keeps
  finding that hard resets breed anxiety; we count episodes and wins, not unbroken days.
- **No fake loot or monsters.** Every reward in the app comes from a real number you lifted.
- **No glowing "system" HUD look**, no ink-brush style, no poetic copy (owner, 24 Oct 2026).
  Many "Solo Leveling" style apps already do the daily-quest HUD; we are not one of them.
- **No social feed in v1.** Shareable episode cards only.

## Next to Vishal's planner

Siblings, not competitors (owner, 24 Oct 2026). His app plans the week and is calm; this one
trains the body and has hype moments. Both have a living world, each with its own style.
*Later:* the two could connect, for example a finished workout showing up in his village.

## Build order

1. **Log a workout with ghost numbers** on every set, saved for real. Plain screens.
2. **Episode cards** after each session, and the episode list.
3. **The dojo home**: stations, condition, today's focus.
4. **Boss fights.**
5. Ghost and boss drawn in the dojo; easter eggs; sharing.
6. Later: nutrition, friends, the link with Vishal's app.

## Open questions

- Set controls and the in-workout screen (mockup next).
- How the first workouts are planned before there is any history.
- Bodyweight moves like pull-ups: is the ghost reps only?
- What a beaten boss leaves behind in the dojo.

## Sources consulted (24 Oct 2026)

- Hevy, previous workout values: https://help.hevyapp.com/hc/en-us/articles/36011896355479-How-to-Use-Previous-Workout-Values-to-Improve-Performance-in-Hevy
- Freeletics ghost mode: https://www.freeletics.com/en/blog/ghost-mode
- Quest2Fitness, workout RPG: https://apps.apple.com/app/id6769663664
- Ring Fit Adventure design: https://www.gamedeveloper.com/game-platforms/what-fitness-games-interest-people-ring-fit-adventure-as-an-example
- Zombies, Run! lessons (Adrian Hon): https://medium.com/@adrianhon/two-million-runners-five-cdb53cd793a1
- Strava Local Legends: https://the5krunner.com/2020/06/10/new-strava-local-legends-segments-captain-but-not-as-we-know-them
- Streak design psychology: https://smashingmagazine.com/2026/02/designing-streak-system-ux-psychology/
