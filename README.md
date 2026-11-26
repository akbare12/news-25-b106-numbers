[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b106-numbers/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b106-numbers/reward.svg)](https://make.fun/bounty/news-image-20261125)

# The World Today — Wednesday 25 November 2026

A one-page front page with **50 verified stories from Wednesday 25 November 2026**.

## Hero stories

1. **Trump hits 14 trade partners with new tariffs** — China faces 20%, the EU 15% and Vietnam 20%.
2. **Kospi plunges 6.16%** — Samsung −9.9% and SK Hynix −11.1% trigger a circuit breaker; foreigners sell KRW 1.95tn.
3. **Shenzhou-24 carries the first foreign astronaut to Tiangong** — Pakistan's Muhammad Zeeshan Ali, 40.

## Inside

- 10 featured cards (including the Hamas security chief Naeem Abu Nahel, killed 25 Nov; the Bogor gold-mine flood, 9 dead and 17 trapped; an Iowa seizure of 9,500 lbs), each with its story number badge and a C / R / CL tag.
- A numbers strip, a 13-pin map of the featured stories, and 37 more stories under ALSO TODAY.
- A two-line DATE CHECK: every story is from today, 25 Nov. Left out because they are *not* today: Huawei verdict 24 Nov, PIF Tower attack 24 Nov, Sudan strikes 24 Nov, Nvidia CEO reinstated 23 Nov. The 25 Nov Gaza story (Naeem Abu Nahel) is a featured card, never a left-out item.

## How to render

```sh
python3 gen.py        # writes entry.png (1024x1024)
python3 main.py       # copies entry.png into ./out/
```

## Sources

Reuters, AP, BBC, CNN, Xinhua, Korea Exchange, pm.gov.au.

## Files

- `gen.py` — renders `entry.png` (1024×1024) at build time with Pillow.
- `main.py` — stdlib-only entry point: copies `entry.png` into `MAKEFUN_OUTPUT_DIR`.
- `entry.png` — the submitted front page.

Built for the [news-image-20261125](https://make.fun/bounty/news-image-20261125) bounty on [make.fun](https://make.fun/bounty/news-image-20261125).
