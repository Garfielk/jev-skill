# Showcase sources

These previews show community projects, not executions or benchmark results from
this repository. Click a README card to reach its author. No preview was generated
to imitate a working integration.

| Preview | Original | How it is displayed |
|---|---|---|
| Browser control | [Browser Use / Jev Ultrafast](https://github.com/browser-use/jev-ultrafast/tree/1231850a0bf1a0c0341fe408ef1668dbbfdfac46) | `browser-preview.gif`: same 91 frames and timing, resized and padded to 800 × 450; no AI redraw. |
| Tetris | [thelau / Jev Tetris](https://github.com/thelau/jev-tetris/tree/9869b602965cf002afff766013f8c068846d36aa) | `tetris-preview.png`: scaled and padded to 800 × 450 from the pinned still. A UI still is not a live-run receipt. |
| Whale city | [@gokayfem's September 18 video](https://x.com/gokayfem/status/2101022590722810271) | `whale-city.png`: original frame; `whale-preview.png` is the 800 × 450 preview. An unaltered frame at 00:06 from the author's 480 × 270 video rendition. Astra designs, Jev chooses, H3 renders. |
| MIDI composition | [cocktailpeanut / Jevthoven](https://github.com/cocktailpeanut/jevthoven/tree/e5e0c67d8bae92f96c9ce05138f55c3ab72c6aac) · [original video](https://github.com/user-attachments/assets/176c69e4-501e-4b71-8517-957cc692882a) | `jevthoven.png`: original frame; `music-preview.png` is the scaled/padded preview. An unaltered frame at 00:42. Jev selects musical parts; other code renders notes and audio. |
| Code review | [devagrawal09 / Jev Review](https://github.com/devagrawal09/jev-review/tree/31f89602797fb7bea007f8a480bf368bf564954e) | `review-preview.png`: crop (140, 0, 1140, 650) of the pinned 1280 × 1200 dashboard, scaled/padded to 800 × 450. [Full original](https://raw.githubusercontent.com/devagrawal09/jev-review/31f89602797fb7bea007f8a480bf368bf564954e/docs/dashboard.png). An author's dashboard screenshot, not our review output. |
| Decision playground | [davila7 / Jev Explained](https://github.com/davila7/jev-explained/tree/5cbe35e04609112be77b1bd447bd79b3bde7980b) | `primitives-preview.png`: full illustration scaled/padded to 800 × 450. [Full original](https://raw.githubusercontent.com/davila7/jev-explained/5cbe35e04609112be77b1bd447bd79b3bde7980b/docs/jev-primitives.png). An explanatory illustration, **not** a screenshot or API result. |

All six September 22 previews use the same canvas. Only the review dashboard is
cropped; the others keep their full frame. Resizing, padding and cropping are
mechanical, not AI-generated. Captions describe the source, not a run we performed.
[Upstream license notices](UPSTREAM-LICENSES.md).

Frames were extracted with `ffmpeg -ss SECONDS -i VIDEO -frames:v 1 OUTPUT.png`.
Media remain attributed to their original creators; the repository's code license
does not relicense third-party media.
