# The VC Roundtable skill

A table of 7 Claudes, each playing a top VC firm, hears your startup pitch, grills you, and votes fund or pass. Every firm that passes tells you exactly what to fix.

Made by **Alex Chen** ([@nocodealex](https://instagram.com/nocodealex)), an AI creator who builds free Claude Code skills. More at [chen.media](https://chen.media).

`/roundtable` asks what you are raising and for what, your pitch as text (one slide or point per paragraph), and the real facts behind it. Then it seats 7 Claude sub-agents, each judging the way that firm says in public that it judges startups:

| Firm | Always at the table? |
|---|---|
| Y Combinator: a small team that ships fast, talks to users and can say what it does in one line | yes |
| Sequoia: a clear why now, a big market, a company that could still matter in 20 years | yes |
| a16z: technical founders building software that changes how a whole industry works | yes |
| Benchmark, Founders Fund, Accel, Lightspeed, Kleiner Perkins, General Catalyst, Index Ventures | 4 dealt in each run |

It runs like a real meeting:

1. **The pitch.** You paste it in.
2. **The grilling.** Every firm asks you its 2 hardest questions, each tied to your exact words. You answer them in one message.
3. **The vote.** Every firm votes **fund, fund if, or pass**, quoting your pitch and your answers.
4. **The fix.** Every pass and every fund-if must say exactly what to change. A small script throws out any vote that quotes words you never said, or that passes without a fix. A coach Claude reads every vote and ranks the 3 changes that win the most firms.

## Install

Paste this into Claude Code:

```
https://github.com/alexyc9381/vc-roundtable-skill
Install this skill, then confirm /roundtable works.
```

Or as a plugin:

```
/plugin marketplace add alexyc9381/vc-roundtable-skill
/plugin install vc-roundtable-skill@vc-roundtable-skill
```

Or copy the folder yourself:

```bash
git clone https://github.com/alexyc9381/vc-roundtable-skill
cp -r vc-roundtable-skill/skills/roundtable ~/.claude/skills/
```

Needs Claude Code (it spawns sub-agents) and Python 3.8+. Nothing to pip install, no API keys.

## Use it

```
/roundtable              # it asks for your pitch, grills you, then the vote
/roundtable --firms 10   # every firm at the table
/roundtable --seed 7     # the same table again, to compare two versions of your pitch fairly
```

You get `.roundtable/REPORT.md`: how many firms would fund you, how each one voted and why, what each one wants fixed, and the 3 fixes worth the most votes.

## The roundtable prompt

Every firm gets this rule, word for word:

> You only know what is in `.roundtable/case.json`: the founder's goal, their pitch (numbered paragraphs), the facts they pasted, and their answers to the grilling once there are some. Judge the pitch the way your firm says in public that it judges startups, honestly and as hard as a real partner meeting. Every point you make quotes the founder's exact words. Never invent facts about the founder, the company, the market or the numbers. You are a Claude playing this firm's public advice, not the firm itself.

The full steps are in [`skills/roundtable/SKILL.md`](skills/roundtable/SKILL.md).

## What a run looks like

A demo run on a made-up startup is in [`examples/demo-run/`](examples/demo-run/): the pitch, the grilling, every firm's vote and fix, and the report.

## Good to know

- 15-17 sub-agents per run (7 firms twice, plus the coach), so it uses some of your Claude plan.
- Nothing is sent to anyone.
- The firms are Claudes playing each firm's public investing advice. They are not the real firms, and no firm made or endorses this. Use it to fix your pitch before the real meeting.
- It is not made by Anthropic.

Run the tests with:

```bash
python3 -m unittest discover -s tests
```
