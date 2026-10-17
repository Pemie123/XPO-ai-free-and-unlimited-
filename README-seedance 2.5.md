How to run Seedance 2.5 reference-aware

This zip is not a program you double-click. It is an AI-agent skill: a set of instructions an AI assistant loads so it knows how to make Seedance 2.5 videos with its own built-in video tools. What's in the zip File What it does SKILL.md The main instructions: always use model seedance_2.5, 4–30 s videos (default 30 s), English prompts, aspect ratio, how to use attached reference images/videos skill.json Name, version (4.0.1), default settings and trigger words like "seedance 30s" references/prompt_guide.md How to write good prompts, with 0–10 s / 10–20 s / 20–30 s time cues and examples scripts/pipeline_tracker.py A small helper that keeps a to-do list of video jobs. It does not make videos itself The skill expects the agent to have tools named text_to_video, image_to_video, FileBatchUpload and NotifyHuman. Those exist only on the agent platform it was written for. Claude does not have them, so it can't generate videos with this skill here. What you need • An AI agent platform that supports uploading skills and has built-in text_to_video / image_to_video tools with Seedance 2.5. This skill was written for such a platform; check your platform's skill/agent settings. • Python 3.8 or newer, only if you want to run the job tracker yourself. • No API key: the skill tells the agent not to ask for one. How to run it Fix the script first pipeline_tracker.py has a typo on line 54 and crashes on start (SyntaxError: unmatched ')'). Replace that line with: STATE_FILE.write_text(json.dumps(s, indent=2, ensure_ascii=False), encoding="utf-8") I tested the fixed version: all its commands work. Option A — use it as a skill (the normal way)

Fix the script (above) and zip the seedane-2.5-30s folder again.
In your agent platform, open its skills settings and upload or install the zip.
Start a new chat and type a request with a trigger word, for example: "seedance 30s: a barista pouring latte art in a sunny cafe, vertical for TikTok".
The agent picks the skill, writes an English prompt and generates the video straight away. Attach images or videos to use them as references. Option B — run the job tracker by hand This only manages a job list in /tmp; it makes no videos. In a terminal, from the seedane-2.5-30s folder: python3 scripts/pipeline_tracker.py init python3 scripts/pipeline_tracker.py enqueue --prompt "A barista pours latte art" --duration 30 --ratio 9:16 python3 scripts/pipeline_tracker.py dispatch-next python3 scripts/pipeline_tracker.py mark job_01 done --url https://example.com/video.mp4 python3 scripts/pipeline_tracker.py summary On Windows, use python instead of python3. The state file goes to /tmp, so on Windows the tracker needs a C:\tmp folder. What you can ask for Setting Options Default Length 4–30 seconds; more than 30 is cut to 30, less than 4 is raised to 4 30 s Aspect ratio 21:9, 16:9, 4:3, 1:1, 3:4, 9:16; words like "TikTok" or "YouTube" pick it for you 16:9 References Attach images (look, character, scene) and/or videos (motion, camera); say which is which, e.g. "Image 1 = the scene, Image 2 = the character" none Language Ask in any language; the agent translates the prompt to English — For 30 s videos, describe the scene in three parts (0–10 s, 10–20 s, 20–30 s). references/prompt_guide.md has examples. If something goes wrong Problem Fix SyntaxError: unmatched ')' Apply the line-54 fix above The agent ignores the skill Use a trigger word ("seedance 30s", "seedance 2.5") or name the skill in your request The agent says it has no video tool That platform lacks text_to_video; the skill can't work there Video stops at 15 s The skill should then extend it by another 15 s; if not, ask for the "Video Extension" step References were ignored Re-attach them and spell out each one's role The skill claims Seedance 2.5 makes 30 s in one go, citing BytePlus docs. I couldn't check that here, so the actual limit depends on your platform.
About

No description, website, or topics provided.
Resources
Readme
Activity
Stars
1 star
Watchers
0 watching
Forks
0 forks
Releases
1
 (1)
XPO-ai V1.0.0
Latest
11 minutes ago
Packages
No packages published
Publish your first package
Contributors
1
 (1)
@Pemie123
