# -*- coding: utf-8 -*-
# Cell 3: Complete Website Code

from flask import Flask, render_template_string

# ==========================================
# 🔥 FIREBASE CLOUD DATABASE SETUP 🔥
# ==========================================
import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Bypass to prevent crash on server reload
if not firebase_admin._apps:
    try:
        # Render Environment se secret key uthana
        firebase_key_string = os.environ.get('FIREBASE_JSON')
        if firebase_key_string:
            firebase_key = json.loads(firebase_key_string)
            cred = credentials.Certificate(firebase_key)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("🚀 STATUS: Firebase Successfully Connected to Matrix! 🔥")
        else:
            print("⚠️ WARNING: FIREBASE_JSON environment variable not found.")
            db = None
    except Exception as e:
        print(f"❌ Firebase Init Error: {e}")
        db = None
else:
    db = firestore.client()
# ==========================================

app = Flask(__name__)

# ============== CSS STYLES (Mobile Optimized for OPPO F23 5G) ==============
MOBILE_CSS = """
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #fff;
    min-height: 100vh;
    overflow-x: hidden;
}

/* Sidebar */
.sidebar {
    position: fixed;
    left: -280px;
    top: 0;
    width: 280px;
    height: 100vh;
    background: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%);
    transition: 0.3s ease;
    z-index: 1000;
    padding: 20px;
    box-shadow: 5px 0 30px rgba(0,255,136,0.1);
}

.sidebar.active {
    left: 0;
}

.sidebar-header {
    text-align: center;
    padding: 20px 0;
    border-bottom: 2px solid #00ff88;
}

.profile-pic {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: linear-gradient(45deg, #00ff88, #00d4ff);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    margin: 0 auto 15px;
    box-shadow: 0 0 30px rgba(0,255,136,0.4);
}

.sidebar h2 {
    color: #00ff88;
    font-size: 20px;
}

.sidebar p {
    color: #888;
    font-size: 12px;
    margin-top: 5px;
}

.nav-links {
    margin-top: 30px;
    list-style: none;
}

.nav-links li {
    margin: 10px 0;
}

.nav-links a {
    color: #fff;
    text-decoration: none;
    display: flex;
    align-items: center;
    padding: 12px 15px;
    border-radius: 10px;
    transition: 0.3s;
}

.nav-links a:hover, .nav-links a.active {
    background: rgba(0,255,136,0.2);
    color: #00ff88;
}

.nav-links a span {
    margin-left: 15px;
}

/* Menu Toggle */
.menu-toggle {
    position: fixed;
    top: 15px;
    left: 15px;
    z-index: 1001;
    background: linear-gradient(45deg, #00ff88, #00d4ff);
    border: none;
    padding: 12px 15px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 20px;
}

/* Overlay */
.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 999;
    display: none;
}

.overlay.active {
    display: block;
}

/* Main Content */
.main-content {
    padding: 80px 15px 30px;
    max-width: 100%;
}

.page-title {
    color: #00ff88;
    font-size: 24px;
    margin-bottom: 20px;
    text-align: center;
    text-shadow: 0 0 20px rgba(0,255,136,0.5);
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
    border: 1px solid rgba(0,255,136,0.2);
    backdrop-filter: blur(10px);
}

.card h3 {
    color: #00ff88;
    margin-bottom: 10px;
    font-size: 16px;
}

.card p {
    color: #ccc;
    font-size: 14px;
    line-height: 1.6;
}

/* Code Blocks */
.code-block {
    background: #0d0d1a;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    overflow-x: auto;
    border-left: 4px solid #00ff88;
}

.code-block code {
    color: #00ff88;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    white-space: pre-wrap;
    word-break: break-all;
}

/* Copy Button */
.copy-btn {
    background: linear-gradient(45deg, #00ff88, #00d4ff);
    border: none;
    padding: 8px 15px;
    border-radius: 5px;
    color: #000;
    font-weight: bold;
    margin-top: 10px;
    cursor: pointer;
    font-size: 12px;
}

/* Tips Box */
.tip-box {
    background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,212,255,0.1));
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
    border-left: 4px solid #00d4ff;
}

.tip-box h4 {
    color: #00d4ff;
    margin-bottom: 8px;
    font-size: 14px;
}

/* Warning Box */
.warning-box {
    background: rgba(255,107,107,0.1);
    border-radius: 10px;
    padding: 15px;
    margin: 15px 0;
    border-left: 4px solid #ff6b6b;
}

.warning-box h4 {
    color: #ff6b6b;
    margin-bottom: 8px;
}

/* Table */
.cmd-table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 12px;
}

.cmd-table th, .cmd-table td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.cmd-table th {
    background: rgba(0,255,136,0.2);
    color: #00ff88;
}

/* Contact Info */
.contact-item {
    display: flex;
    align-items: center;
    padding: 15px;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    margin: 10px 0;
}

.contact-item span {
    margin-left: 15px;
    font-size: 14px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    margin-top: 30px;
    border-top: 1px solid rgba(255,255,255,0.1);
    color: #666;
    font-size: 12px;
}
</style>
"""

# ============== JAVASCRIPT ==============
MOBILE_JS = """
<script>
function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('active');
    document.querySelector('.overlay').classList.toggle('active');
}

function copyCode(id) {
    const code = document.getElementById(id).innerText;
    navigator.clipboard.writeText(code);
    alert('✅ Code Copied!');
}

// Close sidebar on overlay click
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.overlay').addEventListener('click', toggleSidebar);
});
</script>
"""

# ============== SIDEBAR COMPONENT ==============
SIDEBAR = """
<button class="menu-toggle" onclick="toggleSidebar()">☰</button>
<div class="overlay"></div>
<nav class="sidebar">
    <div class="sidebar-header">
        <div class="profile-pic">👤</div>
        <h2>Saddam Khan</h2>
        <p>Termux Developer</p>
    </div>
    <ul class="nav-links">
        <li><a href="/" class="{home_active}">🏠<span>Home</span></a></li>
        <li><a href="/profile" class="{profile_active}">👤<span>Profile</span></a></li>
        <li><a href="/termux-basics" class="{basics_active}">📱<span>Termux Basics</span></a></li>
        <li><a href="/shizuku-setup" class="{shizuku_active}">⚡<span>Shizuku Setup</span></a></li>
        <li><a href="/useful-commands" class="{commands_active}">💻<span>Useful Commands</span></a></li>
        <li><a href="/tips-tricks" class="{tips_active}">🎯<span>Tips & Tricks</span></a></li>
        <li><a href="/packages" class="{packages_active}">📦<span>Best Packages</span></a></li>
        <li><a href="/contact" class="{contact_active}">📞<span>Contact</span></a></li>
    </ul>
</nav>
"""

# ============== PAGE 1: HOME ==============
@app.route('/')
def home():
    sidebar = SIDEBAR.format(home_active="active", profile_active="", basics_active="",
                             shizuku_active="", commands_active="", tips_active="",
                             packages_active="", contact_active="")
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Termux & Shizuku Guide</title>
        {MOBILE_CSS}
    </head>
    <body>
        {sidebar}
        <main class="main-content">
            <h1 class="page-title">🚀 Termux & Shizuku Guide</h1>

            <div class="card">
                <h3>👋 Welcome!</h3>
                <p>Is website mein aapko milega complete guide Termux aur Shizuku ke baare mein. Android ko powerful terminal banao bina root ke!</p>
            </div>

            <div class="card">
                <h3>📱 Kya Hai Termux?</h3>
                <p>Termux ek powerful terminal emulator hai Android ke liye. Isse aap Linux commands run kar sakte ho apne phone pe!</p>
            </div>

            <div class="card">
                <h3>⚡ Kya Hai Shizuku?</h3>
                <p>Shizuku se aap bina root ke system-level permissions access kar sakte ho. Termux ke saath use karne se aur bhi powerful ho jaata hai!</p>
            </div>

            <div class="tip-box">
                <h4>💡 Quick Start</h4>
                <p>Sidebar mein jaake sabhi pages explore karo. Profile page mein owner ki details hain!</p>
            </div>

            <div class="card">
                <h3>🎯 Is Guide Mein Kya Hai?</h3>
                <p>✅ Termux Basic Commands<br>
                ✅ Shizuku Setup Guide<br>
                ✅ Useful Packages<br>
                ✅ Tips & Tricks<br>
                ✅ Advanced Commands</p>
            </div>
        </main>
        <footer class="footer">
            Made with ❤️ by Saddam Khan | 2025
        </footer>
        {MOBILE_JS}
    </body>
    </html>
    """)

# ============== PAGE 2: PROFILE ==============
@app.route('/profile')
def profile():
    sidebar = SIDEBAR.format(home_active="", profile_active="active", basics_active="",
                             shizuku_active="", commands_active="", tips_active="",
                             packages_active="", contact_active="")
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Profile - Saddam Khan</title>
        {MOBILE_CSS}
        <style>
            .profile-header {{
                text-align: center;
                padding: 30px 20px;
                background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,212,255,0.1));
                border-radius: 20px;
                margin-bottom: 20px;
            }}
            .profile-avatar {{
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: linear-gradient(45deg, #00ff88, #00d4ff);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 50px;
                margin: 0 auto 20px;
                box-shadow: 0 0 40px rgba(0,255,136,0.5);
                animation: pulse 2s infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ box-shadow: 0 0 40px rgba(0,255,136,0.5); }}
                50% {{ box-shadow: 0 0 60px rgba(0,255,136,0.8); }}
            }}
            .profile-name {{
                font-size: 28px;
                color: #00ff88;
                margin-bottom: 10px;
            }}
            .profile-title {{
                color: #888;
                font-size: 16px;
            }}
            .info-card {{
                background: rgba(255,255,255,0.05);
                border-radius: 15px;
                padding: 20px;
                margin: 15px 0;
            }}
            .info-item {{
                display: flex;
                align-items: center;
                padding: 15px 0;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .info-item:last-child {{
                border-bottom: none;
            }}
            .info-icon {{
                width: 45px;
                height: 45px;
                background: linear-gradient(45deg, #00ff88, #00d4ff);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                margin-right: 15px;
            }}
            .info-text h4 {{
                color: #fff;
                font-size: 14px;
                margin-bottom: 5px;
            }}
            .info-text p {{
                color: #00ff88;
                font-size: 16px;
            }}
            .skills-section {{
                margin-top: 20px;
            }}
            .skill-tag {{
                display: inline-block;
                background: rgba(0,255,136,0.2);
                color: #00ff88;
                padding: 8px 15px;
                border-radius: 20px;
                margin: 5px;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        {sidebar}
        <main class="main-content">
            <div class="profile-header">
                <div class="profile-avatar">👨‍💻</div>
                <h1 class="profile-name">Saddam Khan</h1>
                <p class="profile-title">Termux & Android Developer</p>
            </div>

            <div class="info-card">
                <div class="info-item">
                    <div class="info-icon">👤</div>
                    <div class="info-text">
                        <h4>Full Name</h4>
                        <p>Saddam Khan</p>
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-icon">📧</div>
                    <div class="info-text">
                        <h4>Email</h4>
                        <p>khansaddam93667@gmail.com</p>
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-icon">📱</div>
                    <div class="info-text">
                        <h4>Phone</h4>
                        <p>+91 88509 75949</p>
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-icon">📍</div>
                    <div class="info-text">
                        <h4>Location</h4>
                        <p>India</p>
                    </div>
                </div>
            </div>

            <div class="card">
                <h3>🎯 About Me</h3>
                <p>Main ek passionate Android enthusiast hun jo Termux aur Shizuku ke through Android ki full potential explore karta hun. Is website mein maine apna saara knowledge share kiya hai!</p>
            </div>

            <div class="card skills-section">
                <h3>🛠️ Skills</h3>
                <span class="skill-tag">Termux</span>
                <span class="skill-tag">Shizuku</span>
                <span class="skill-tag">Linux</span>
                <span class="skill-tag">Python</span>
                <span class="skill-tag">Shell Scripting</span>
                <span class="skill-tag">Android</span>
                <span class="skill-tag">Networking</span>
            </div>
        </main>
        <footer class="footer">
            Made with ❤️ by Saddam Khan | 2025
        </footer>
        {MOBILE_JS}
    </body>
    </html>
    """)

# ============== PAGE 3: TERMUX BASICS ==============
@app.route('/termux-basics')
def termux_basics():
    sidebar = SIDEBAR.format(home_active="", profile_active="", basics_active="active",
                             shizuku_active="", commands_active="", tips_active="",
                             packages_active="", contact_active="")
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Termux Basics</title>
        {MOBILE_CSS}
    </head>
    <body>
        {sidebar}
        <main class="main-content">
            <h1 class="page-title">📱 Termux Basics</h1>

            <div class="card">
                <h3>📥 Step 1: Download Termux</h3>
                <p>Termux ko F-Droid se download karo (Play Store wala outdated hai)</p>
                <div class="code-block">
                    <code id="code1">[f-droid.org](https://f-droid.org/en/packages/com.termux/)</code>
                </div>
                <button class="copy-btn" onclick="copyCode('code1')">📋 Copy Link</button>
            </div>

            <div class="card">
                <h3>🔄 Step 2: First Update</h3>
                <p>Termux open karte hi ye commands run karo:</p>
                <div class="code-block">
                    <code id="code2">pkg update -y && pkg upgrade -y</code>
                </div>
                <button class="copy-btn" onclick="copyCode('code2')">📋 Copy</button>
            </div>

            <div class="card">
                <h3>📂 Step 3: Storage Access</h3>
                <p>Internal storage access ke liye:</p>
                <div class="code-block">
                    <code id="code3">termux-setup-storage</code>
                </div>
                <button class="copy-btn" onclick="copyCode('code3')">📋 Copy</button>
            </div>

            <div class="tip-box">
                <h4>💡 Pro Tip</h4>
                <p>Volume Down + Q dabao extra keyboard keys ke liye!</p>
            </div>

            <div class="card">
                <h3>🔤 Basic Commands</h3>
                <table class="cmd-table">
                    <tr><th>Command</th><th>Kya Karta Hai</th></tr>
                    <tr><td>ls</td><td>Files list karo</td></tr>
                    <tr><td>cd folder</td><td>Folder mein jao</td></tr>
                    <tr><td>pwd</td><td>Current path dekho</td></tr>
                    <tr><td>mkdir name</td><td>Naya folder banao</td></tr>
                    <tr><td>rm file</td><td>File delete karo</td></tr>
                    <tr><td>cp a b</td><td>File copy karo</td></tr>
                    <tr><td>mv a b</td><td>File move karo</td></tr>
                    <tr><td>cat file</td><td>File content dekho</td></tr>
                    <tr><td>clear</td><td>Screen saaf karo</td></tr>
                    <tr><td>exit</td><td>Termux band karo</td></tr>
                </table>
            </div>

            <div class="warning-box">
                <h4>⚠️ Warning</h4>
                <p>rm -rf command carefully use karo, ye permanently delete karta hai!</p>
            </div>
        </main>
        <footer class="footer">
            Made with ❤️ by Saddam Khan | 2025
        </footer>
        {MOBILE_JS}
    </body>
    </html>
    """)

# ============== PAGE 4: SHIZUKU SETUP ==============
@app.route('/shizuku-setup')
def shizuku_setup():
    sidebar = SIDEBAR.format(home_active="", profile_active="", basics_active="",
                             shizuku_active="active", commands_active="", tips_active="",
                             packages_active="", contact_active="")
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Shizuku Setup</title>
        {MOBILE_CSS}
    </head>
    <body>
        {sidebar}
        <main class="main-content">
            <h1 class="page-title">⚡ Shizuku Setup</h1>

            <div class="card">
                <h3>📥 Step 1: Download Shizuku</h3>
                <p>Play Store ya GitHub se Shizuku download karo</p>
                <div class="code-block">
                    <code id="shiz1">[shizuku.rikka.app](https://shizuku.rikka.app/)</code>
                </div>
                <button class="copy-btn" onclick="copyCode('shiz1')">📋 Copy</button>
            </div>

            <div class="card">
                <h3>🔧 Step 2: Developer Options Enable</h3>
                <p>Settings → About Phone → Build Number pe 7 baar tap karo</p>
            </div>

            <div class="card">
                <h3>🐛 Step 3: USB Debugging On</h3>
                <p>Settings → Developer Options → USB Debugging ON karo</p>
            </div>

            <div class="card">
                <h3>📲 Step 4: Wireless Debugging (Android 11+)</h3>
                <p>Developer Options mein Wireless Debugging ON karo</p>
            </div>

            <div class="card">
                <h3>🚀 Step 5: Shizuku Start via Wireless</h3>
                <p>Shizuku app open karo. Start via Wireless Debugging option pe tap karo. Pairing notification aayegi. Usmein diye gaye code ko Wireless Debugging settings mein enter karo. Shizuku start ho jayega.</p>
            </div>

            <div class="tip-box">
                <h4>💡 Important Note</h4>
                <p>Har baar phone restart karne par Shizuku ko dobara start karna padega (non-rooted devices ke liye).</p>
            </div>

            <div class="card">
                <h3>💻 Step 6: Termux se Shizuku connect karna (rish)</h3>
                <p>Termux mein rish (Remote Interactive Shell) setup karne ke liye ye commands follow karo:</p>
                <div class="code-block">
                    <code id="shiz2">pkg install curl -y</code>
                </div>
                <button class="copy-btn" onclick="copyCode('shiz2')">📋 Copy</button>
                <div class="code-block">
                    <code id="shiz3">curl -L https://github.com/RikkaApps/Shizuku/releases/latest/download/rish -o $PREFIX/bin/rish</code>
                </div>
                <button class="copy-btn" onclick="copyCode('shiz3')">📋 Copy</button>
                <div class="code-block">
                    <code id="shiz4">chmod +x $PREFIX/bin/rish</code>
                </div>
                <button class="copy-btn" onclick="copyCode('shiz4')">📋 Copy</button>
                <p>Ab aap `rish -c 'command'` use karke ADB commands chala sakte ho, jaise:</p>
                <div class="code-block">
                    <code id="shiz5">rish -c 'cmd package list packages'</code>
                </div>
                <button class="copy-btn" onclick="copyCode('shiz5')">📋 Copy</button>
            </div>

        </main>
        <footer class="footer">
            Made with ❤️ by Saddam Khan | 2025
        </footer>
        {MOBILE_JS}
    </body>
    </html>
    """)

# ============== PAGE 5: USEFUL COMMANDS ==============
@app.route('/useful-commands')
def useful_commands():
    sidebar = SIDEBAR.format(home_active="", profile_active="", basics_active="",
                             shizuku_active="", commands_active="active", tips_active="",
                             packages_active="", contact_active="")
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Useful Commands</title>
        {MOBILE_CSS}
    </head>
    <body>
        {sidebar}
        <main class="main-content">
            <h1 class="page-title">💻 Useful Commands</h1>

            <div class="card">
                <h3>📁 File Management</h3>
                <table class="cmd-table">
                    <tr><th>Command</th><th>Description</th></tr>
                    <tr><td><code>ls -l</code></td><td>Detailed list of files</td></tr>
                    <tr><td><code>cp -r source dest</code></td><td>Copy directory recursively</td></tr>
                    <tr><td><code>find . -name "*.txt"</code></td><td>Find all .txt files in current dir</td></tr>
                    <tr><td><code>grep "text" file.txt</code></td><td>Search for "text" in a file</td></tr>
                    <tr><td><code>head file.txt</code></td><td>Show first 10 lines of file</td></tr>
                    <tr><td><code>tail file.txt</code></td><td>Show last 10 lines of file</td></tr>
                    <tr><td><code>tar -czvf archive.tar.gz folder/</code></td><td>Compress folder to tar.gz</td></tr>
                    <tr><td><code>tar -xzvf archive.tar.gz</code></td><td>Extract tar.gz archive</td></tr>
                </table>
            </div>

            <div class="card">
                <h3>🌐 Network Utilities</h3>
                <table class="cmd-table">
                    <tr><th>Command</th><th>Description</th></tr>
                    <tr><td><code>ping google.com</code></td><td>Check network connectivity</td></tr>
                    <tr><td><code>ifconfig</code></td><td>Display network interfaces (legacy)</td></tr>
                    <tr><td><code>ip addr</code></td><td>Display network interfaces (modern)</td></tr>
                    <tr><td><code>netstat -tuln</code></td><td>List open TCP/UDP ports</td></tr>
                    <tr><td><code>curl -I example.com</code></td><td>Show HTTP headers of a URL</td></tr>
                    <tr><td><code>wget -O newname.zip url/file.zip</code></td><td>Download file with a new name</td></tr>
                    <tr><td><code>ssh user@host</code></td><td>Connect to a remote server via SSH</td></tr>
                </table>
            </div>

            <div class="card">
                <h3>⚙️ System Information</h3>
                <table class="cmd-table">
                    <tr><th>Command</th><th>Description</th></tr>
                    <tr><td><code>df -h</code></td><td>Display disk space usage</td></tr>
                    <tr><td><code>du -sh folder/</code></td><td>Display total size of a folder</td></tr>
                    <tr><td><code>free -m</code></td><td>Display memory usage in MB</td></tr>
                    <tr><td><code>top</code> or <code>htop</code></td><td>Display running processes (htop needs installation: `pkg install htop`)</td></tr>
                    <tr><td><code>uname -a</code></td><td>Print system information</td></tr>
                    <tr><td><code>uptime</code></td><td>Show how long the system has been running</td></tr>
                </table>
            </div>

            <div class="warning-box">
                <h4>⚠️ Caution!</h4>
                <p>Some commands like `rm -rf` can cause permanent data loss. Always double-check before executing commands that modify or delete files.</p>
            </div>
        </main>
        <footer class="footer">
            Made with ❤️ by Saddam Khan | 2025
        </footer>
        {MOBILE_JS}
    </body>
    </html>
    """)

# ============== PAGE 6: TIPS & TRICKS ==============
@app.route('/tips-tricks')
def tips_tricks():
    sidebar = SIDEBAR.format(home_active="", profile_active="", basics_active="",
                             shizuku_active="", commands_active="", tips_active="active",
                             packages_active="", contact_active="")
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Tips & Tricks</title>
        {MOBILE_CSS}
    </head>
    <body>
        {sidebar}
        <main class="main-content">
            <h1 class="page-title">🎯 Tips & Tricks</h1>

            <div class="card">
                <h3>⌨️ Termux Keyboard Shortcuts</h3>
                <p>Termux mein kaam karte waqt productivity badhane ke liye kuch useful shortcuts:</p>
                <table class="cmd-table">
                    <tr><th>Shortcut</th><th>Action</th></tr>
                    <tr><td>Volume Down + Q</td><td>Extra keys (Ctrl, Alt, Esc, arrow keys)</td></tr>
                    <tr><td>Volume Down + K</td><td>Show/hide keyboard</td></tr>
                    <tr><td>Volume Down + V</td><td>Paste text</td></tr>
                    <tr><td>Ctrl + C</td><td>Stop current process</td></tr>
                    <tr><td>Ctrl + Z</td><td>Suspend current process</td></tr>
                    <tr><td>Ctrl + L</td><td>Clear screen</td></tr>
                    <tr><td>Ctrl + D</td><td>Exit Termux session</td></tr>
                </table>
            </div>

            <div class="card">
                <h3>💾 Termux Backup & Restore</h3>
                <p>Apne Termux environment ko backup aur restore kaise karein:</p>
                <div class="code-block">
                    <code id="tip1">termux-backup # Backup current state</code>
                </div>
                <button class="copy-btn" onclick="copyCode('tip1')">📋 Copy</button>
                <div class="code-block">
                    <code id="tip2">termux-restore # Restore from backup</code>
                </div>
                <button class="copy-btn" onclick="copyCode('tip2')">📋 Copy</button>
                <p>Backups `data/data/com.termux/files/home/` mein save hote hain.</p>
            </div>

            <div class="tip-box">
                <h4>💡 Customizing Termux Prompt</h4>
                <p>Apni `bashrc` file edit karke prompt ko customize kar sakte ho. Example: `PS1='\\u@termux:\w\$ '`</p>
            </div>

            <div class="card">
                <h3>🌐 Ngrok Tunneling for Local Server</h3>
                <p>Agar aap Termux mein koi web server chala rahe ho (jaise Python Flask/Django), toh Ngrok se use public internet par expose kar sakte ho:</p>
                <div class="code-block">
                </div>
                <button class="copy-btn" onclick="copyCode('tip3')">📋 Copy</button>
                <div class="code-block">
                </div>
                <button class="copy-btn" onclick="copyCode('tip4')">📋 Copy</button>
                <p>Isse aapko ek public URL milega jisse aap apne local server ko access kar sakte ho.</p>
            </div>

        </main>
        <footer class="footer">
            Made with ❤️ by Saddam Khan | 2025
        </footer>
        {MOBILE_JS}
    </body>
    </html>
    """)

# ============== PAGE 7: BEST PACKAGES ==============
@app.route('/packages')
def packages():
    sidebar = SIDEBAR.format(home_active="", profile_active="", basics_active="",
                             shizuku_active="", commands_active="", tips_active="",
                             packages_active="active", contact_active="")
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Best Packages</title>
        {MOBILE_CSS}
    </head>
    <body>
        {sidebar}
        <main class="main-content">
            <h1 class="page-title">📦 Best Packages</h1>

            <div class="card">
                <h3>📝 Text Editors</h3>
                <table class="cmd-table">
                    <tr><th>Package</th><th>Description</th><th>Install Command</th></tr>
                    <tr><td><code>nano</code></td><td>Simple, user-friendly text editor</td><td><code>pkg install nano</code></td></tr>
                    <tr><td><code>vim</code></td><td>Powerful, highly configurable editor</td><td><code>pkg install vim</code></td></tr>
                    <tr><td><code>micro</code></td><td>Modern, intuitive command-line editor</td><td><code>pkg install micro</code></td></tr>
                </table>
            </div>

            <div class="card">
                <h3>🐍 Programming Languages</h3>
                <table class="cmd-table">
                    <tr><th>Package</th><th>Description</th><th>Install Command</th></tr>
                    <tr><td><code>python</code></td><td>General-purpose programming language</td><td><code>pkg install python</code></td></tr>
                    <tr><td><code>nodejs</code></td><td>JavaScript runtime for server-side</td><td><code>pkg install nodejs</code></td></tr>
                    <tr><td><code>php</code></td><td>Server-side scripting language</td><td><code>pkg install php</code></td></tr>
                    <tr><td><code>golang</code></td><td>Google's compiled language</td><td><code>pkg install golang</code></td></tr>
                </table>
            </div>

            <div class="card">
                <h3>🛠️ Development Tools</h3>
                <table class="cmd-table">
                    <tr><th>Package</th><th>Description</th><th>Install Command</th></tr>
                    <tr><td><code>git</code></td><td>Version control system</td><td><code>pkg install git</code></td></tr>
                    <tr><td><code>clang</code></td><td>C/C++/Objective-C compiler</td><td><code>pkg install clang</code></td></tr>
                    <tr><td><code>make</code></td><td>Build automation tool</td><td><code>pkg install make</code></td></tr>
                    <tr><td><code>openssh</code></td><td>SSH client and server</td><td><code>pkg install openssh</code></td></tr>
                </table>
            </div>

            <div class="card">
                <h3>📡 Networking Tools</h3>
                <table class="cmd-table">
                    <tr><th>Package</th><th>Description</th><th>Install Command</th></tr>
                    <tr><td><code>nmap</code></td><td>Network discovery and security auditing</td><td><code>pkg install nmap</code></td></tr>
                    <tr><td><code>netcat</code> (nc)</td><td>Utility for reading/writing network connections</td><td><code>pkg install netcat</code></td></tr>
                    <tr><td><code>w3m</code></td><td>Text-based web browser</td><td><code>pkg install w3m</code></td></tr>
                    <tr><td><code>aria2</code></td><td>Multi-protocol & multi-source download utility</td><td><code>pkg install aria2</code></td></tr>
                </table>
            </div>

            <div class="card">
                <h3>📦 Utilities</h3>
                <table class="cmd-table">
                    <tr><th>Package</th><th>Description</th><th>Install Command</th></tr>
                    <tr><td><code>htop</code></td><td>Interactive process viewer</td><td><code>pkg install htop</code></td></tr>
                    <tr><td><code>unzip</code>/<code>zip</code></td><td>Archive file utilities</td><td><code>pkg install unzip zip</code></td></tr>
                    <tr><td><code>termux-api</code></td><td>Access Android APIs from Termux</td><td><code>pkg install termux-api</code></td></tr>
                    <tr><td><code>grep</code></td><td>Search text patterns in files</td><td><code>pkg install grep</code></td></tr>
                </table>
            </div>

        </main>
        <footer class="footer">
            Made with ❤️ by Saddam Khan | 2025
        </footer>
        {MOBILE_JS}
    </body>
    </html>
    """)

# ============== PAGE 8: CONTACT ==============
@app.route('/contact')
def contact():
    sidebar = SIDEBAR.format(home_active="", profile_active="", basics_active="",
                             shizuku_active="", commands_active="", tips_active="",
                             packages_active="", contact_active="active")
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Contact Us</title>
        {MOBILE_CSS}
        <style>
            .contact-info-card {{
                background: rgba(255,255,255,0.05);
                border-radius: 15px;
                padding: 20px;
                margin: 15px 0;
                border: 1px solid rgba(0,255,136,0.2);
                backdrop-filter: blur(10px);
            }}
            .contact-info-card .contact-item {{
                background: none;
                padding: 10px 0;
                margin: 0;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .contact-info-card .contact-item:last-child {{
                border-bottom: none;
            }}
            .contact-info-card .contact-item .info-icon {{
                width: 40px;
                height: 40px;
                font-size: 18px;
            }}
            .contact-info-card h3 {{
                text-align: center;
                color: #00ff88;
                margin-bottom: 20px;
                font-size: 20px;
            }}
            .social-media-icons {{
                text-align: center;
                margin-top: 30px;
            }}
            .social-media-icons a {{
                display: inline-block;
                margin: 0 10px;
                color: #00d4ff;
                font-size: 30px;
                transition: transform 0.3s ease;
            }}
            .social-media-icons a:hover {{
                transform: scale(1.2);
                color: #00ff88;
            }}
        </style>
    </head>
    <body>
        {sidebar}
        <main class="main-content">
            <h1 class="page-title">📞 Contact Saddam Khan</h1>

            <div class="contact-info-card">
                <h3>Get in Touch!</h3>
                <div class="contact-item">
                    <div class="info-icon">📧</div>
                    <div class="info-text">
                        <h4>Email</h4>
                        <p>khansaddam93667@gmail.com</p>
                    </div>
                </div>
                <div class="contact-item">
                    <div class="info-icon">📱</div>
                    <div class="info-text">
                        <h4>Phone</h4>
                        <p>+91 88509 75949</p>
                    </div>
                </div>
                <div class="contact-item">
                    <div class="info-icon">📍</div>
                    <div class="info-text">
                        <h4>Location</h4>
                        <p>India</p>
                    </div>
                </div>
            </div>

            <div class="card">
                <h3>💬 Send a Message</h3>
                <p>Feel free to reach out for any queries, suggestions, or collaborations!</p>
                <form action="#" method="POST" style="margin-top: 15px;">
                    <input type="text" placeholder="Your Name" style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #00ff88; background-color: rgba(0,0,0,0.3); color: #fff;">
                    <input type="email" placeholder="Your Email" style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #00ff88; background-color: rgba(0,0,0,0.3); color: #fff;">
                    <textarea placeholder="Your Message" rows="5" style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #00ff88; background-color: rgba(0,0,0,0.3); color: #fff;"></textarea>
                    <button type="submit" class="copy-btn" style="width: 100%;">🚀 Send Message</button>
                </form>
            </div>

            <div class="social-media-icons">
                <a href="#"><i class="fab fa-github"></i></a>
                <a href="#"><i class="fab fa-twitter"></i></a>
                <a href="#"><i class="fab fa-linkedin"></i></a>
            </div>

        </main>
        <footer class="footer">
            Made with ❤️ by Saddam Khan | 2025
        </footer>
        {MOBILE_JS}
    </body>
    </html>
    """)




# Run Flask in a thread so the cell doesn't block


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
