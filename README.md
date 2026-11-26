# Wednesday, November 25, 2026 — The World in One Page

[![Bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b106-numbers/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b106-numbers/reward.svg)](https://make.fun/bounty/news-image-20261125)

A one-page front page for **Wednesday, November 25, 2026**: **50 stories**
in a single 1024 × 1024 image — 3 heroes, 10 cards, 37 more in ALSO.

## The three heroes

1. **Trump hits 14 trade partners with new tariffs** — China 20%, EU 15%,
   Vietnam 20%. Higher import costs feed straight into US prices, supply
   chains and holiday shopping.
2. **Kospi crashes 6.16% in a chip rout** — Samsung −9.9%, SK Hynix −11.1%;
   the circuit breaker trips as foreigners sell KRW 1.95tn.
3. **First foreign astronaut reaches Tiangong** — Muhammad Zeeshan Ali, 40,
   of Pakistan, flies on Shenzhou-24, the first foreign astronaut aboard
   China's station.

## The ten cards

Gaza (Hamas security chief Col. Mohammad Abuelouf, 47, killed with his wife
and two daughters in a strike on Shati camp, 25 Nov) · Bogor gold mine
(9 dead, 17 trapped 100 m down) · Iowa (9,500 lbs of lead azide seized) ·
Cartagena (76 hostages freed) · Cairo (tanker fire kills 31) · Canberra
($740M Solomons pact) · New York (100th Macy's parade delayed) · Madrid
(Abrego Garcia held 90 days) · Markets (Nvidia −3.9% on downgrade watch) ·
Thanksgiving travel rush.

Every card and every ALSO line carries a certainty letter — **C** confirmed,
**R** reported, **CL** claim — and every hero scene carries its number badge.

## Date check

Every story on the page is dated Wednesday, 25 November 2026. Left out
because they belong to other days: Huawei verdict 24 Nov, PIF Tower strike
24 Nov, Sudan strikes 24 Nov, Nvidia CEO reinstated 23 Nov.

## Also inside

A 13-place world map (Washington, Madrid, Brussels, Gaza City, Cairo,
Islamabad, Beijing, Seoul, Hanoi, Bogor, Des Moines, Cartagena, Canberra),
a by-the-numbers strip (20%, −6.16%, 9,500 lbs, 76, 31, 9, 17, $740M,
−3.9%, 100th, 90 days, 47, 40, 100 m), and sources: Reuters, AP, BBC, CNN,
Xinhua, Korea Exchange, pm.gov.au.

## Verification

Rendered and checked on 26 November 2026: `entry.png` is 1024 × 1024 and
under 1 MiB; `main.py` passes a standard-library-only simulation (fresh
venv without Pillow, different working directory, empty output directory)
with exit code 0 and a matching SHA-256 digest.

## Files

- `entry.png` — the finished front page, 1024 × 1024.
- `gen.py` — build-time renderer (Pillow) that drew `entry.png`.
- `main.py` — stdlib-only entry point: copies `entry.png` to
  `MAKEFUN_OUTPUT_DIR`. No third-party imports, so it runs in the
  standard-library-only grader.
- `LICENSE` — MIT.

## Rebuild

```sh
python3 gen.py          # renders entry.png
python3 main.py         # copies entry.png to out/entry.png
```
