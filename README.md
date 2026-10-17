# XPO-ai-free-and-unlimited-


How to launch XPO-AI
17 okt 2026 · @Wim Brillouet
XPO-AI is a Base44 app (a React + Vite frontend). You run it on your computer with one command, and you publish it from the Base44 dashboard.
What you need
Tool
Why
How to get it
Node.js 18 or newer (20 LTS recommended)
Runs the app and installs packages
nodejs.org — includes npm
A Base44 account
The app's login, database and file storage live there
app.base44.com
Base44 CLI
Runs the local backend and opens the dashboard
npm install -g base44@latest
A terminal
To type the commands below
Terminal (Mac), PowerShell (Windows)
Check Node is installed with node -v. It should print v18 or higher.
Unzip and install
1. Unzip xpo.zip into a folder, for example Documents/xpo.
2. Open a terminal in that folder: cd Documents/xpo
3. Install the app's packages: npm install (takes 1–2 minutes the first time).
4. Install the Base44 CLI once: npm install -g base44@latest
5. Log in to Base44: base44 login and follow the browser prompt.
6. Connect this folder to your XPO-AI app on Base44: base44 link and pick the app. The zip has no link file, so you need this step once.
Environment settings
With base44 dev you can skip this: it fills in the app settings for you.
Only if you run the frontend on its own (npm run dev), create a file named .env.local in the project folder:
VITE_BASE44_APP_ID=your_app_id
VITE_BASE44_APP_BASE_URL=https://your-app.base44.app
Find the app ID and URL in the Base44 dashboard. Never share or upload this file.
Run it on your computer
1. In the project folder, run base44 dev.
2. Open the local address it prints (usually http://localhost:5173).
3. You should see XPO-AI with the Images and Videos tabs.
4. Stop it with Ctrl+C in the terminal.
Alternative: npm run dev starts only the frontend and talks to the live Base44 backend (needs .env.local, above).
Put it live
Pick one route:
• From the CLI: run base44 deploy in the project folder, then base44 site open to see the live site.
• Via Git + dashboard: push the code to the app's linked Git repo, then run base44 dashboard open and click Publish.
Check the live site afterwards: the Music, Games and Websites tabs should be gone.
If something goes wrong
Problem
Fix
command not found: base44
Re-run npm install -g base44@latest and open a new terminal
npm or node not found
Install Node.js, then restart the terminal
Blank page or login loop
Run base44 link again and check you picked the right app
Port 5173 already in use
Close the other dev server, or use the new port Vite prints
Errors after npm install
Delete the node_modules folder and run npm install again
More help: Base44 CLI commands · Base44 support
