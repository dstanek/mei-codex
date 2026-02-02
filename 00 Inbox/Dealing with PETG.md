The “hairy” / “cotton candy” stuff is called **stringing** or **oozing**, and it’s super common with PETG. The good news is you can usually reduce it a _lot_ with tuning.

Here’s a practical checklist you can work through.

---

## 1. Lower your nozzle temperature (a bit)

PETG loves to ooze when it’s too hot.
- Typical PETG range: **220–250°C**
- If you’re at 245–250°C, try dropping by **5°C steps** until:
    - Stringing gets better, **but**
    - Layer adhesion and extrusion still look strong (no gaps, brittle parts)

**Watch for:**
- Too hot → tons of strings + blobby corners
- Too cold → under-extrusion, weak layers, poor bed adhesion

---

## 2. Retraction tuning (biggest lever)

PETG usually needs **more retraction** than PLA but not crazy high.

### For a direct drive extruder

- Retraction distance: start around **0.8–1.2 mm**
- Retraction speed: **25–40 mm/s**
    

### For a Bowden setup

- Retraction distance: **4–6 mm** (sometimes up to 7, but don’t jump there first)
- Retraction speed: **30–50 mm/s**
    

General tips:
- Increase **distance** a bit at a time (0.5 mm increments)
- If you go too high, you can get:
    - Ground filament
    - Heat-creep clogs
- Keep speed moderate; PETG can get jammy if you retract crazy fast

If your slicer has it, enable:
- **“Combing: Not in skin / Within infill”** or equivalent
- **“Avoid crossing perimeters”** – reduces travel moves across open air.

---

## 3. Travel speed & coasting

The less time the nozzle spends travelling, the less it can drool.

- Travel speed: **150–200 mm/s** is common on modern printers
    - If you’re at 80–100 mm/s, try bumping it up.
- Enable **coasting** (if your slicer supports it):
    - This tells the printer to stop extruding a tiny bit before the end of a segment and let residual pressure finish the line.
    - Start with a very small coasting volume and increase gradually if needed.

---

## 4. Enable “Wipe” / “Retract then move” features

Most slicers have some form of:
- **Wipe nozzle while retracting**
- **Wipe on retraction**
- **Z-hop only when retracted** (optional but nice insurance)

This helps:
- The nozzle drags back over the already-extruded plastic as it retracts
- That tends to clean off the little blob that would turn into a string mid-air

---

## 5. Cooling & fan settings

PETG usually likes **less fan** than PLA, but cooling still impacts stringing.

- Try a fan at **20–40%** after the first couple layers.
- If you run fan off, PETG stays gooey longer and can string more.
- Too high fan can hurt layer adhesion or cause brittle parts — so adjust gradually.

---

## 6. Dry your filament

PETG is hygroscopic, and **wet PETG strings like crazy**.

Signs of wet PETG:

- Popping / hissing from nozzle while printing
- Rough/matte surface instead of smooth
- Tons of random micro-blobs and strings everywhere

If you suspect moisture:

- Dry spool at ~**60°C for 4–6 hours** in a filament dryer or oven with **accurate** temp control.
- Then re-test with the same settings.

---

## 7. Tune with a retraction/stringing test

Rather than guessing, run a quick test model:

- Search for **“PETG retraction test tower”** or **“stringing test”** models on Printables/Thingiverse.
- Print several with different:
    - Temps (e.g., 240 / 235 / 230 / 225°C)
    - Retraction distances (e.g., 0.8 / 1.0 / 1.2 mm direct drive or 4 / 5 / 6 mm Bowden)

Keep notes like:

`Test 1: 235°C, 1.0 mm retract, 35 mm/s, travel 180 mm/s → moderate strings Test 2: 230°C, 1.0 mm retract, 35 mm/s, travel 200 mm/s → fewer strings Test 3: 230°C, 1.2 mm retract, 35 mm/s, travel 200 mm/s → almost clean`

Once you find a combo you like, save it as a **PETG profile** in your slicer.

---

## 8. Accept a _little_ PETG stringing + post-process

Even with perfect tuning, PETG often has _some_ hair. That’s normal.

Easy cleanup:

- Quick pass with:
    - **Heat gun** (light, sweeping motion—don’t melt the part)
    - Or a **hair dryer on hot**
- Or just:
    - Fingernails / small pliers to pull off bigger wisps

---

## If you want, I can go specific

If you tell me:

- Printer model
- Slicer (PrusaSlicer, Bambu Studio, Cura, etc.)
- Current PETG temps, retraction, and fan settings

…I can suggest concrete values to try (e.g. “set this checkbox and these exact numbers”) tailored to your setup.