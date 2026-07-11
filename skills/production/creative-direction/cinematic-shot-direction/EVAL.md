# Cinematic shot direction evaluation

## Evaluation protocol

Give the evaluated agent only `SKILL.md` and the task prompt. Do not expose this file, its expected answers, scoring language, or critical-failure list.

Score four dimensions:

| Dimension | Points |
|---|---:|
| Knowledge and causal understanding | 25 |
| Production decisions and tradeoffs | 25 |
| Applied shot direction | 40 |
| Communication, feasibility, and review discipline | 10 |
| **Total** | **100** |

Interpretation:

- **90–100:** production-ready; choices are intentional, coherent, and editable.
- **75–89:** competent; minor omissions do not undermine the sequence.
- **60–74:** partial; knows terminology but misses causal or editorial relationships.
- **Below 60:** not ready for unsupervised shot direction.

Apply global critical-failure caps after scoring. A response can use different terminology or a different creative solution and still earn full credit if it preserves the required causal, spatial, and editorial logic.

## Knowledge questions — 25 points

### K1. Focal length, distance, and perspective — 4 points

**Question:** Two shots frame a face at the same size. One uses a wide lens close to the subject; the other uses a long lens from farther away. What causes the difference in facial and background perspective, and what does focal length itself control?

**Expected answer:** Camera position/distance causes the perspective difference: the close camera exaggerates near/far size differences; the distant camera reduces them. Focal length and image format control angle of view and magnification/framing. The operator changes both distance and focal length to keep face size constant while changing perspective.

**Required points:**

- Perspective is governed by camera position, not focal length alone.
- Focal length is discussed with sensor/image format or as field of view.
- Wide-close versus long-far appearance is described correctly.

**Disqualifying claim:** “A telephoto lens inherently compresses space from the same camera position.”

### K2. Camera height versus angle — 3 points

**Question:** Why is “low angle” insufficient as a shot specification?

**Expected answer:** It can mean a low camera height, an upward optical-axis angle, or both. Height changes foreground, horizon, and visible surfaces; tilt/angle changes convergence and view direction. A usable spec names lens-center height and viewing angle separately, plus roll when relevant.

**Required points:** distinction, at least one visual consequence, and a precise replacement description.

### K3. Shot size — 3 points

**Question:** Is a close-up defined by a fixed camera distance? How should an agent choose shot size?

**Expected answer:** No. Shot size describes subject scale/framing and its boundaries are flexible. Choose it from required information and editorial emphasis; name body/object landmarks when precision matters.

**Penalty:** subtract 1 if the answer assigns universal emotional meanings to shot sizes.

### K4. Axis and screen direction — 4 points

**Question:** Explain the 180-degree convention, why it exists, and two ways to cross the axis without an accidental spatial reversal.

**Expected answer:** The active axis follows dialogue, look, travel, or task relation. Keeping cameras on one side preserves left/right placement, opposing eyelines, and motion direction. It is a continuity convention, not an inviolable law. A deliberate crossing can be shown during camera motion, bridged through a neutral/on-axis or re-establishing shot, or introduced as a clearly motivated new spatial relation.

**Required points:** axis definition, preserved relationship, convention status, and two credible bridge methods.

### K5. Dolly versus zoom — 3 points

**Question:** What is the visual difference between dollying in and zooming in?

**Expected answer:** A dolly translates the camera, changing camera-subject distance, perspective, parallax, and framing. A zoom changes focal length/angle of view from a fixed position, changing framing and magnification without translational parallax. Neither is automatically more cinematic.

### K6. Movement specification — 3 points

**Question:** What information turns “slow cinematic push-in” into executable direction?

**Expected answer:** Start frame, path/distance, cue or motivation, speed/easing character, stabilization, end frame, and what is revealed or relationally changed. It should also state conflicts or exclusions such as no pan/zoom.

**Required points:** any five fields, including both a cue and end frame.

### K7. Lighting interaction — 3 points

**Question:** Why must blocking and camera movement be evaluated against lighting rather than planned independently?

**Expected answer:** Changing subject or camera position changes source-to-face angle, reflection, contrast, shadow, eye light, silhouette, background level, and sometimes exposure. A track or arc can turn side light into frontal light or backlight. Direction should map motivated source, key side, fill/contrast, and expected transitions across the move.

### K8. Continuity and attention — 2 points

**Question:** Give two reasons a match-on-action or eyeline match can make a cut feel continuous.

**Expected answer:** Motion and visual attention carry across the cut; the viewer tracks an action or gaze target rather than the discontinuous camera change. The edit preserves causal and/or spatial expectation. Full credit requires an attentional or causal explanation, not only a rule name.

## Production-decision scenarios — 25 points

### D1. Confidential confession — 6 points

**Scenario:** A character admits a betrayal in a parked car. The director asks for a “dramatic orbit around both actors” during the confession. Space is tight; the scene must cut with earlier shot/reverse-shot coverage.

**Expected decision:** Challenge or redesign the orbit. Determine the dramatic job first. A restrained push, reframing, profile two-shot, or locked sustained take may better preserve performance and geography. If an orbit is essential, plot the axis crossing, show it continuously, account for reflections and key direction, and define the new screen relationship afterward.

**Strong reasoning demonstrates:**

- Movement is selected for a beat, not because it sounds cinematic.
- Car geometry, reflections, eyelines, existing axis, and lighting are considered.
- The answer supplies an executable alternative with cue and end state.
- It does not forbid axis crossing categorically.

**Scoring:** 2 points dramatic rationale; 2 continuity/geometry; 1 light/reflection; 1 practical alternative.

**Critical failure:** approving an unplanned 360-degree move while promising seamless shot/reverse-shot continuity.

### D2. “Make the background compressed” — 6 points

**Scenario:** The current medium shot was made on a 35 mm full-frame-equivalent field of view from 1.2 m. The user asks for a more compressed skyline while keeping the actor the same size.

**Expected decision:** Move the camera farther from the actor and use a longer field of view to restore the same framing. Re-evaluate background alignment, depth of field, practical space, atmosphere, and communication distance. Merely changing to a longer lens from the same position crops the current perspective.

**Scoring:** 3 points correct geometry; 1 format-aware language; 1 practical consequences; 1 preserves subject size and intended skyline.

**Critical failure:** changes focal length only and describes that as a perspective change.

### D3. Simultaneous discovery — 6 points

**Scenario:** A child opens an empty gift box at the exact moment a parent behind them realizes the gift was stolen. The editor must preserve the simultaneity.

**Expected decision:** Favor a two-plane composition, two-shot, mirror/reflection, deep-focus or controlled focus-transfer shot, or designed moving master that contains action and reaction together. Supplemental coverage can exist, but fragmenting the beat into isolated singles risks changing the event from simultaneous to sequential.

**Strong reasoning demonstrates:** shot size chosen for both readable actions; blocking separates silhouettes; focus strategy is intentional; lighting supports both planes; inserts are not allowed to steal the parent reaction.

**Scoring:** 2 simultaneity; 1 composition/blocking; 1 focus; 1 light; 1 editorial alternatives.

### D4. Vertical and horizontal delivery — 7 points

**Scenario:** A courier runs toward a visible destination across a broad plaza. The campaign needs 16:9 and 9:16 versions from the same production.

**Expected decision:** Design separate compositions or a protected master with verified crop zones. For 9:16, use depth and diagonal/approach motion rather than relying solely on long horizontal travel; keep destination, subject, lead room, and entry/exit readable. Specify which variant is authoritative and test start/end frames in both. Preserve screen direction across the sequence.

**Strong reasoning demonstrates:** aspect ratio as a blocking decision; destination stays legible; motion room and subject scale survive; no assumption that center crop is automatically safe.

**Scoring:** 2 composition redesign; 2 blocking/motion; 1 destination/geography; 1 continuity; 1 explicit verification.

**Critical failure:** “shoot wide and crop it later” with no protection or review method.

## Applied production tasks — 40 points

### A1. Write a complete shot specification — 12 points

**User request:** “Create a single six-second shot in which a lab technician realizes a sample is contaminated. I want tension but no horror clichés. The sample must remain visible, and the shot has to cut from a prior wide shot where the technician is screen-right looking left.”

**Expected approach:** Write one continuous, executable shot that turns on a visible attention/performance beat. Preserve the technician's screen-right placement or leftward eyeline as appropriate to the established axis. Keep the sample visible or establish a clear look/sample relation. Choose lens, distance, height, angle, movement, blocking, focus, lighting, and end frame to support recognition. State no-cut constraints and review targets.

**Rubric:**

- 2: Dramatic job and information order are explicit.
- 2: Start and end frame include size, placement, distance relationship, height, and angle.
- 2: Lens/field of view and focus strategy are coherent and format-aware.
- 2: Blocking and camera movement have cue, path, and end state; a lock-off is acceptable if justified.
- 1: Lighting interaction supports tension without defaulting to flicker/red light/horror shorthand.
- 2: Screen side, eyeline, prior action state, and cut handles are preserved.
- 1: Exclusions/tolerances and review criteria are actionable.

**Critical failures:** sample becomes invisible during the realization; technician reverses eyeline without reorientation; direction asks for multiple cuts despite “single shot”; uses mood adjectives without geometry.

### A2. Design coverage for a negotiation — 10 points

**User request:** “Plan coverage for two founders negotiating across a table. Founder A controls the conversation until Founder B silently slides a resignation letter forward; after that B has control. Keep it visually restrained.”

**Expected approach:** Establish an axis and geography; choose coverage that encodes the power shift through attention, duration, shot size, blocking, or controlled camera relation rather than arbitrary angle symbolism. The letter action needs a readable match point or shared frame. B's reaction/control after the slide must receive editorial priority. Lighting, eyelines, prop hand/state, and handles must stay continuous.

**Rubric:**

- 2: Axis, screen positions, eyelines, and table geography.
- 2: Coverage is organized by dramatic beats rather than equal speaker insurance.
- 2: Letter slide is readable with action overlap and prop/hand continuity.
- 2: Visual strategy changes meaningfully but remains restrained; sustained two-shot is allowed.
- 1: Light and focus continuity across angles.
- 1: Entry/exit options or re-establishing shot.

**Critical failures:** shot plan makes A and B look in the same screen direction; no shot can show the letter and its consequence; every beat receives mechanically identical coverage despite the requested control shift.

### A3. Diagnose and repair a failed generated clip — 9 points

**Observed output:** “A dancer begins centered in a medium-wide frame. The instruction said: ‘orbit left while she spins right, push in, zoom out, reveal the audience, rack focus to her eyes, moody cinematic lighting.’ The clip pumps scale, reverses direction, invents audience members, and loses the dancer's face in shadow.”

**Expected approach:** Trace failures to conflicting camera operations, unspecific axis/directions, invented scene content, and unplanned light interaction. Preserve the intended core and simplify to one dominant camera move. Define start/end frames, dancer and camera paths in screen/world terms, audience existence or exclusion, focus behavior, key direction, and review conditions. Suggest separate shots if both audience reveal and eye close-up are essential.

**Rubric:**

- 2: Identifies at least four causal failures, not just symptoms.
- 2: Selects and defends one dominant movement.
- 2: Rewrites movement/blocking with explicit geometry and directions.
- 1: Repairs lighting through source/path relation.
- 1: Controls scene population and continuity.
- 1: Proposes a clean split into separate shots if objectives conflict.

**Critical failure:** adds more style terms or camera moves without resolving geometry.

### A4. Build a three-shot travel sequence — 9 points

**User request:** “Direct three separately generated shots of a cyclist leaving a village, crossing a bridge, and approaching a mountain tunnel. The sequence should feel like continuous forward progress.”

**Expected approach:** Establish a travel direction and preserve it or deliberately bridge any change. Carry identity, bicycle/wardrobe, weather/light direction, destination, and action state. Give each shot a distinct editorial function and useful change in size/angle. Define match points, entries/exits, and environmental progression; avoid arbitrary teleportation.

**Rubric:**

- 2: Explicit screen direction and axis logic in all shots.
- 2: Identity, prop, weather, and lighting continuity.
- 2: Geography progresses logically from village to bridge to tunnel.
- 2: Match points and entry/exit/action states support actual cuts.
- 1: Shot sizes/camera relations vary with purpose.

**Critical failures:** any unbridged direction reversal; tunnel appears before bridge without intentional temporal restructuring; bicycle or rider state changes unexplained.

## Communication, feasibility, and review discipline — 10 points

Score this across all scenario and applied answers:

- **3 points — Intent before technique:** The agent states what the audience should notice/understand/feel before prescribing camera tools.
- **2 points — Fact/convention/heuristic separation:** It does not present interpretive clichés as laws and treats continuity rules as purposeful conventions.
- **2 points — Executability:** Specifications use geometric, temporal, and continuity language that production can verify.
- **2 points — Editorial awareness:** Every shot has a plausible in/out, relation to adjacent shots, or reason to remain self-contained.
- **1 point — Review method:** The agent names observable usability conditions rather than promising “cinematic quality.”

## Global critical failures and score caps

Apply the most severe applicable cap:

- **Maximum 55:** Repeatedly states that focal length alone changes perspective/compression from a fixed camera position.
- **Maximum 55:** Produces coverage with unacknowledged axis/eyeline/direction reversals that make spatial relations contradictory.
- **Maximum 55:** Cannot distinguish camera translation from zoom or rotation.
- **Maximum 60:** Writes multi-shot montage directions when the task requires one continuous shot, without separating them into independently controllable shots.
- **Maximum 60:** Ignores explicit aspect-ratio constraints so critical subjects or destinations cannot fit the requested delivery.
- **Maximum 65:** Treats angle/lens/movement meanings as universal emotional laws without reference to story context.
- **Maximum 65:** Omits blocking and lighting interaction from every moving-shot plan.
- **Maximum 65:** Gives attractive descriptions but no start frame, movement cue/path, end frame, or continuity state.
- **Automatic fail for the relevant task:** Introduces people, unsafe physical action, identity changes, or copyrighted/brand elements explicitly excluded by the request.

Do not penalize a deliberate discontinuity, axis crossing, jump cut, or lighting change when the agent explains its narrative purpose, makes the transition legible, and accepts the intended editorial effect.
