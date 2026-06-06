# EC (UOSA.exe) right-click movement — ground truth

> **Correction (empirical, supersedes the "no tap timer" claim below).**
> Observed in EC directly: a *quick* right-click only **turns** the character to
> face the cursor — it does **not** step. Only a sustained **hold** walks/runs.
> So rapid clicks around the character spin it in place. The native decompile
> does throttle stepping (in the move executor, not a clean input-level ms
> timer), but the user-visible rule is turn-on-tap / walk-on-hold. Our CUO
> implementation reproduces this with a 150 ms tap window (above TURN_DELAY=80 ms)
> — a pragmatic approximation, not a verified EC millisecond constant. The
> "no double-click-to-step" and resolution-relative walk/run findings stand.


Investigation date: 2026-06-06. Evidence from the EC install at
`C:\Games\Electronic Arts\Ultima Online Enhanced\` (Lua in `UserInterface\Default.zip`)
and the Ghidra decompile dump `tools\ghidra\ghidra_full.jsonl`.

## TL;DR

EC's in-world right-click movement is **far simpler** than our current implementation.
EC does **not** turn-on-press, does **not** step-on-double-click, and has **no
millisecond tap/hold timer and no pixel dead-zone**. It does exactly one thing:

> While the right button is held, every movement tick it computes the 8-way
> direction from the **cursor → screen-centre** vector and a walk/run speed, and
> sends a move/turn request **whenever the direction or speed changes**.

Turn-vs-step is **not** a client gesture — it's the UO movement protocol: a request
in a *new* facing is a turn (no tile change); the *next* request in the *same*
facing is a step. CUO's `PlayerMobile.Walk()` already implements this.

**The original (pre-`63cf09aff`) CUO `MoveCharacterByMouseInput` is already a faithful
EC reproduction.** Our `63cf09aff` additions (turn-on-down, double-click-step, 150 ms
tap threshold) are the divergence, and explain the rapid-alternating-click glitches.

## 1. Where the logic lives — BINARY, not Lua

- `Default.zip` Lua **is** loaded by UOSA.exe at boot, but it only covers UI windows
  + settings. The in-world viewport movement is native C++.
- Lua only exposes settings toggles and a keybinding — no in-world move handler:
  - `Source/settingswindow.lua:551` `alwaysRun`, `:556` `enableAutorun`
  - `Source/settingswindow.lua:178` keybinding `ToggleAlwaysRun`
  - grep of all `*.lua` for `MoveCharacter / RightClick / WalkRequest / OnRightMouse`
    over the world viewport → **nothing**.
- The settings strings anchor into native settings (de)serialisation
  (`FUN_00490470`, `FUN_00491300`, `FUN_00495220`, `FUN_00497440`), which store
  `alwaysRun` → global `DAT_00e39820` and `enableAutorun` → `DAT_00e39821`.

## 2. The native movement function — `FUN_005f7300` (CONFIRMED)

Call chain (per movement tick):
`FUN_005f4d20` (move-controller update) → `FUN_005f7220` (held mover; reads cursor via
`FUN_0047bff0` = `GetCursorPos`+`ScreenToClient`) → **`FUN_005f7300`** (direction +
walk/run + send).

Key decompiled lines (`FUN_005f7300`):

```c
// centre of the world viewport, in pixels (viewport edges are normalised 0..1):
fVar13 = (vpW*0.5 + left) * screenWidth;          // centreX   (DAT_00e3d52c+0x40 = width)
fVar14 = ((top-bot)*0.5 + (1-top)) * screenHeight; // centreY  (DAT_00e3d52c+0x42 = height)
local_18 = cursorX - centreX;                      // dx
local_14 = cursorY - centreY;                      // dy
fpatan(dx, dy);                                     // angle = atan2(dx, dy)  (degrees)
dir = FUN_00485d80();                               // quantise -> 0..7, 8 = none
fVar10 = sqrt(centreX*centreX + centreY*centreY);   // |origin -> centre|
fVar11 = sqrt(dx*dx + dy*dy);                        // |cursor -> centre|

// WALK vs RUN:
if ( centreMag*0.33333334 < cursorDist / vpWidthFraction )  speed = 2;  // RUN
else if (DAT_00e39820 /*alwaysRun*/ != 0)                   speed = 2;  // RUN
else                                                        speed = 1;  // WALK

// SEND (only in live-drive mode, +0x7a != 0, i.e. RMB held):
if ( newDir != oldDir  ||  (newSpeed != oldSpeed && newDir != 8) )
    FUN_005ead30(dir, dir, (speed==2)+1);   // move/turn request, packet 0x33
```

### Direction quantiser — `FUN_00485d80` (CONFIRMED)

`atan2` angle in degrees → 8 sectors, each **45° wide, boundaries at 22.5°+k·45°**
(337.5/22.5/67.5/112.5/157.5/202.5/247.5/292.5). Returns 0–7; 8 ("none") only in a
degenerate gap. **No inner dead-zone** — any cursor offset from centre yields a
direction. (Keyboard path uses a different dx/dy-sign quantiser `FUN_00485d00`.)

### Move/turn request — `FUN_005ead30` (CONFIRMED)

EC uses move packet **0x33** (`local_c = 0x33; htons(0x33)`), 3rd byte = speed
(1 walk / 2 run) — **not** legacy 0x02. Not relevant to us (CUO already sends the
correct CUO packet via `Player.Walk`).

## 3. The actual EC rules, with literal numbers

| Question | EC answer (evidence) |
|---|---|
| Walk-vs-run distance | **Ratio, not pixels.** Run when `cursorDistFromCentre / viewportWidthFraction > (1/3)·distFromScreenOriginToCentre`. Literal constant `0.33333334` at `FUN_005f7300`. Roughly: run once the cursor is past ~1/3 of the way from centre toward the edge. **Scales with resolution** — our fixed `190 px` does not. |
| `alwaysRun` | Global `DAT_00e39820`; if set, always run. (CUO: `Profile.AlwaysRun`, already applied inside `Walk`.) |
| Dead-zone (turn-only radius) | **None.** No inner-radius compare exists; any offset picks a direction. |
| Tap vs hold timing (ms) | **No ms timer in native.** Drive mode is the boolean `+0x7a` (set while RMB held). There is no 150 ms equivalent. |
| Turn vs step | **Protocol, not gesture.** Client sends the desired direction; server/prediction turns first (facing change, no tile move) then steps on the next same-direction request. |
| Double-click right | **No double-click-to-step.** Not found in the native movement cluster. The `param_3>0` branch of `FUN_005f7300` is a *click-on-object* hit-test that *suppresses* the move, not a double-step. |
| 3rd/4th rapid click coalescing | Native re-sends a request **only when direction or speed changes** (`if newDir!=oldDir || newSpeed!=oldSpeed`). Identical repeated requests are naturally coalesced. |

Ghidra addresses to re-open: `FUN_005f7300` (math), `FUN_005f7220` (held mover),
`FUN_0047bff0` (cursor), `FUN_00485d80` (quantiser), `FUN_005ead30` (packet),
globals `DAT_00e39820`=alwaysRun, `DAT_00e39821`=enableAutorun.

## 4. CUO already matches EC — except the threshold

`PlayerMobile.Walk(direction, run)` already does turn-then-step:
`src/ClassicUO.Client/Game/GameObjects/PlayerMobile.cs` — branch
`if ((oldDirection & Mask) == (direction & Mask))` → **step** (advances X/Y, full
movement time); `else` → **turn** (`walkTime = TurnDelay`, no tile advance). So the
original loop "while RMB held, call `Walk(facing, run)` each frame" reproduces EC.

## 5. Diff vs our current `GameSceneInputHandler.cs` (after `63cf09aff`)

Our `63cf09aff` added behavior EC does **not** have. To match EC, revert to the
original hold-to-move loop and only fix the threshold:

1. **`OnRightMouseDown` — remove the turn block** (lines ~859–876). EC does not turn
   on press; the held loop handles facing. Keep only:
   `_rightMousePressed=true; _continueRunning=false; _rightMouseDownAt=Time.Ticks; StopFollowing();`
   (`_rightMouseDownAt` becomes unused — drop it with the threshold below.)
2. **`OnRightMouseDoubleClick` — remove the step block** (lines ~917–929) and
   `_justDoubleClicked`. Restore the original behavior (pathfinding-on-double-click is
   a CUO convenience and is independent of EC; keep or drop per taste, but the
   single-step-on-double-click is NOT EC and should go).
3. **`MoveCharacterByMouseInput` — remove the 150 ms tap gate** (lines ~63–68 and the
   `RIGHT_TAP_THRESHOLD` const). EC has no tap timer; the loop should move from the
   first tick the button is held.
4. **Walk-vs-run threshold** — replace the fixed `WALK_RUN_DISTANCE = 190` with EC's
   resolution-relative ratio:
   ```csharp
   // EC: run when cursor is past ~1/3 of the way from centre to the viewport edge.
   double cx = Camera.Bounds.Width  * 0.5;
   double cy = Camera.Bounds.Height * 0.5;
   double centreMag = Math.Sqrt(cx*cx + cy*cy);
   bool run = mouseRange > centreMag / 3.0;   // ≈ EC's 0.33333 ratio
   ```
   (Keep `Profile.AlwaysRun` — `Walk` already ORs it in, matching EC's `alwaysRun`.)

Net effect: right-click-hold drives continuously toward the cursor (turn then step,
walk/run by the ratio); a quick tap sends one direction request → a turn if facing
changed, a step if already facing — exactly EC. The rapid-alternating-click glitch
disappears because we stop firing extra turns on every down and extra steps on every
double-click.
