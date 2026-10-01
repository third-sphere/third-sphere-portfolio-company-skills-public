# Music

A trailer lives on its track. The edit this skill makes: the track's quiet opening plays under
Acts 1 and 2; on the turn beat it hard-cuts into the climax, which is back-timed so the final
chord cuts off during the title card, and the hall decay fades out the last second.

## Finding a track
`find_music.py "<piece or mood>"` searches Wikimedia Commons and lists only files whose license
field says public domain. Prefer recordings marked **GOV** (U.S. Marine Band, Air Force Band, Army
Band, Navy Band): the performance is a federal work, and pieces in their repertoire are usually
public-domain compositions. **Three** layers must be clear: the composition, the recording, and
any **arrangement**. Band recordings of orchestral works are usually transcriptions, and a
transcription is its own copyrightable work. A federal band performing a recent private
arranger's transcription (e.g. Holst's Mars, U.S. Air Force Band, 1998, "transcription by Merlin
Patterson") has a clear performance and composition but an arrangement that still needs clearing.
Check the file description for "transcription" or "arranged by". An orchestral recording of the
original score has no arrangement layer.

Good trailer shapes: an overture or symphonic finale with a quiet opening and a big ending
(Wagner's Tannhäuser overture worked; Dvořák's New World finale, Holst's Mars, Sousa marches for
something lighter). The piece must have a sustained loud section at least as long as Act 3.

Other public-domain bases: US sound recordings published 1925 or earlier (Music Modernization Act;
the cutoff moves forward one year each January). Musopen releases many recordings as public
domain. Stock libraries (licensed) and AI-generated tracks are not public domain; if the user
picks one, record the license terms instead.

## Setting the edit points
`music_map.py <file> --act3 <seconds>` prints loudness every 5 s and suggests:
- `opening_in`: where the music becomes audible.
- `climax_end`: just after the final chord cuts off, keeping ~2 s of decay.
- `suggested_opening_gain_db`: lifts the quiet opening so it reads, while keeping it about 12 dB
  under the climax (the balance approved on an earlier trailer; one data point, so listen).
- `climax_window_ok`: whether the climax stays loud for the whole of Act 3.
It was validated against a hand analysis of the Tannhäuser track (cutoff within 0.5 s, gain
within 1 dB). Two known blind spots, both met on real tracks:
- **Pieces that open loud** (Dvořák's New World finale): `opening_in` comes back as 0, which is
  wrong for this edit. Find a quiet passage in the loudness map yourself, ideally one that swells
  at its end, and set `opening_in` so the swell lands on the turn (swell time minus Acts 1-2 length).
- **Rhythmic endings with rests** (Holst's Mars ends in hammer blows): `climax_window_ok` reports
  False because the rests count as dips. Listen; for a trailer those rests are usually a feature.
Listen to the result anyway.

Record in `script.json["music"]`: `file`, `opening_in`, `climax_end`, `opening_gain_db`,
`credit`, `rights_basis`. Keep the file out of git (it can be 40+ MB) and write its source URL in
`assets/music/SOURCE.md`.

## Loudness
`mix.py` mixes music and hits, runs loudnorm to -14 LUFS (the social-platform target), then
measures and trims, because single-pass loudnorm lands about 2 dB hot on this material. The
limiter must run with `level=false` or its make-up gain undoes the trim.
