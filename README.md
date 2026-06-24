# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

Output code
================================================================================
🐾 PAWPAL+ SYSTEM TEST - Multiple Owners and Pets
================================================================================

================================================================================
OWNER 1: JORDAN
================================================================================

✓ Created Owner: Jordan
  Available time today: 195 minutes
  Availability: {'morning': 60, 'afternoon': 90, 'evening': 45}

✓ Added pets to Jordan:
  - Mochi (Dog, 3 years old)
  - Max (Cat, 5 years old, ['sensitive stomach'])

📋 Creating tasks for Mochi:
  ✓ Morning walk (20 min, high priority)
  ✓ Feed Mochi (10 min, high priority)
  ✓ Evening walk (20 min, high priority)
  ✓ Playtime with Mochi (30 min, medium priority)
  ✓ Training session (15 min, low priority)

📋 Creating tasks for Max:
  ✓ Clean litter box (10 min, high priority)
  ✓ Feed Max (5 min, high priority)
  ✓ Brush Max (15 min, low priority)
  ✓ Play with Max (20 min, medium priority)

────────────────────────────────────────────────────────────────────────────────
📅 GENERATING SCHEDULE FOR JORDAN
────────────────────────────────────────────────────────────────────────────────

Schedule for Jordan:

📍 Mochi:
  1. Feed Mochi (10 min) - Priority: high
  2. Morning walk (20 min) - Priority: high
  3. Evening walk (20 min) - Priority: high
  4. Playtime with Mochi (30 min) - Priority: medium
  5. Training session (15 min) - Priority: low
  Subtotal: 95 minutes

📍 Max:
  1. Feed Max (5 min) - Priority: high
  2. Clean litter box (10 min) - Priority: high
  3. Play with Max (20 min) - Priority: medium
  4. Brush Max (15 min) - Priority: low
  Subtotal: 50 minutes

Total tasks: 9
Total duration: 145 minutes
Fits available time: Yes


================================================================================
OWNER 2: ALEX
================================================================================

✓ Created Owner: Alex
  Available time today: 195 minutes
  Availability: {'morning': 45, 'afternoon': 60, 'evening': 90}

✓ Added pets to Alex:
  - Buddy (Dog, 7 years old, ['arthritis'])
  - Luna (Cat, 2 years old)

📋 Creating tasks for Buddy:
  ✓ Gentle morning walk (25 min, high priority)
  ✓ Feed Buddy (10 min, high priority)
  ✓ Medication (5 min, high priority)
  ✓ Afternoon nap spot (10 min, medium priority)
  ✓ Grooming (20 min, low priority)

📋 Creating tasks for Luna:
  ✓ Feed Luna (5 min, high priority)
  ✓ Litter box check (5 min, high priority)
  ✓ Playtime (30 min, high priority)
  ✓ Window perch time (15 min, low priority)

────────────────────────────────────────────────────────────────────────────────
📅 GENERATING SCHEDULE FOR ALEX
────────────────────────────────────────────────────────────────────────────────

Schedule for Alex:

📍 Buddy:
  1. Medication (5 min) - Priority: high
  2. Feed Buddy (10 min) - Priority: high
  3. Gentle morning walk (25 min) - Priority: high
  4. Afternoon nap spot (10 min) - Priority: medium
  5. Grooming (20 min) - Priority: low
  Subtotal: 70 minutes

📍 Luna:
  1. Feed Luna (5 min) - Priority: high
  2. Litter box check (5 min) - Priority: high
  3. Playtime (30 min) - Priority: high
  4. Window perch time (15 min) - Priority: low
  Subtotal: 55 minutes

Total tasks: 9
Total duration: 125 minutes
Fits available time: Yes


================================================================================
📊 SYSTEM SUMMARY
================================================================================

Owner 1: Jordan
  Pets: 2
  Total tasks: 9
  Pending tasks: 9
  Total scheduled time: 145 minutes / 195 available
  Schedule valid: ✅ YES

Owner 2: Alex
  Pets: 2
  Total tasks: 9
  Pending tasks: 9
  Total scheduled time: 125 minutes / 195 available
  Schedule valid: ✅ YES

================================================================================
✅ TEST COMPLETE!
================================================================================
