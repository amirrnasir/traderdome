import streamlit as st
import requests
import time
from datetime import datetime, timedelta
import random
import json
import os
import pandas as pd
import base64
import altair as alt

# Password protection
password = st.text_input("Enter password:", type="password")
if password != "traderdome2026":
    st.stop()

# Page config
st.set_page_config(page_title="TraderDome: Meme Coins", layout="wide", initial_sidebar_state="collapsed")

# CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&family=Black+Ops+One&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        color: #e0e0e0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Suppress Streamlit rerun page flash */
    .stApp > div { transition: none !important; }
    .block-container { transition: none !important; }

    .main-title {
        font-family: 'Black Ops One', cursive;
        font-size: 4.5rem;
        text-align: center;
        background: linear-gradient(45deg, #ff0000, #ff7700, #ffff00, #00ff00, #0099ff, #6600ff, #ff0000);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-battle 4s ease infinite;
        text-shadow: 0 0 60px rgba(255, 0, 0, 0.5);
        margin-bottom: 0.5rem;
        letter-spacing: 0.15em;
    }

    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #ffaa00;
        margin-bottom: 1rem;
        font-weight: 600;
        letter-spacing: 0.1em;
    }

    @keyframes gradient-battle {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Gory welcome banner */
    .gory-welcome {
        background: linear-gradient(135deg, rgba(180,0,0,0.2), rgba(100,0,0,0.3), rgba(180,0,0,0.2));
        border: 2px solid #cc0000;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 0.8rem;
        text-align: center;
        font-size: 1rem;
        color: #ffaaaa;
        line-height: 1.6;
    }
    .gory-welcome .gory-title {
        font-family: 'Black Ops One', cursive;
        font-size: 1.6rem;
        color: #ff4444;
        letter-spacing: 0.1em;
        margin-bottom: 0.4rem;
        text-shadow: 0 0 15px rgba(255,50,50,0.6);
    }

    /* Disclaimer banner */
    .disclaimer-banner {
        background: linear-gradient(135deg, rgba(0, 180, 100, 0.08), rgba(0, 120, 200, 0.08));
        border: 1px solid #336644;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 1rem;
        font-size: 0.88rem;
        line-height: 1.5;
        color: #99bb99;
    }

    .team-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 900;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .llama-header {
        background: linear-gradient(135deg, #00ff88 0%, #00cc66 100%);
        color: #0a0e27;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.6);
    }
    .mistral-header {
        background: linear-gradient(135deg, #00ccff 0%, #0088ff 100%);
        color: #0a0e27;
        box-shadow: 0 0 30px rgba(0, 204, 255, 0.6);
    }

    .bot-card {
        background: rgba(26, 31, 58, 0.95);
        border: 2px solid;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        position: relative;
    }
    .llama-card { border-color: #00ff88; border-left: 6px solid #00ff88; }
    .mistral-card { border-color: #00ccff; border-left: 6px solid #00ccff; }

    /* Danger zone — static highlight, no pulsing animation (prevents page-wide flicker) */
    .danger-zone {
        border-color: #ff3333 !important;
        border-left-color: #ff3333 !important;
        background: rgba(255, 0, 0, 0.08) !important;
        box-shadow: 0 0 12px rgba(255, 0, 0, 0.4);
    }

    .elimination-warning {
        color: #ff4444;
        font-weight: 700;
    }

    .trade-feed {
        background: rgba(10, 14, 39, 0.9);
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        max-height: 460px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.82rem;
    }
    .trade-item {
        padding: 0.35rem;
        margin-bottom: 0.25rem;
        border-left: 3px solid;
        padding-left: 0.7rem;
    }
    .trade-buy { border-left-color: #00ff88; }
    .trade-sell { border-left-color: #ff6b6b; }

    .stat-box {
        background: rgba(26, 31, 58, 0.9);
        border: 2px solid #444;
        border-radius: 8px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        margin: 0.4rem 0;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* House Fees box */
    .taste-box {
        background: linear-gradient(135deg, rgba(180,80,0,0.25), rgba(100,40,0,0.25));
        border: 2px solid #cc5500;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }

    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.6rem;
    }

    /* Photo styles */
    .bot-photo-thumb {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        object-fit: cover;
        vertical-align: middle;
        display: inline-block;
    }
    .fighter-photo-large {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        display: block;
        margin: 0 auto;
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));
    }

    /* Arena */
    .arena-box {
        background: linear-gradient(135deg, rgba(255,50,0,0.25), rgba(255,150,0,0.15));
        border: 3px solid #ff6600;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
    }
    .arena-title {
        font-size: 1.4rem;
        font-weight: 900;
        color: #ffaa00;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px rgba(255,170,0,0.8);
    }
    .fighter-row {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
        gap: 2.5rem;
        position: relative;
    }
    .fighter-box { text-align: center; flex: 0 1 auto; position: relative; }
    .fighter-left { position: relative; }
    .fighter-right { position: relative; }
    .fighter-icon-big {
        font-size: 5rem;
        display: inline-block;
        position: relative;
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));
    }

    /* ===== ALTERNATING PUNCH ANIMATIONS (10s cycle, 5s per side) ===== */
    .fighter-left .fighter-icon-big {
        animation: fighter1-hit 10s ease-in-out infinite;
    }
    @keyframes fighter1-hit {
        0%, 25%, 50%, 100% { transform: rotate(0deg) scale(1) translateX(0); filter: brightness(1); }
        12%  { transform: rotate(12deg) scale(0.95) translateX(10px); }
        15%  { transform: rotate(15deg) scale(0.92) translateX(14px); filter: brightness(0.7); }
        18%  { transform: rotate(10deg) scale(0.95) translateX(7px); }
    }
    .fighter-right .fighter-icon-big {
        animation: fighter2-hit 10s ease-in-out infinite;
        animation-delay: 5s;
    }
    @keyframes fighter2-hit {
        0%, 25%, 50%, 100% { transform: rotate(0deg) scale(1) translateX(0); filter: brightness(1); }
        12%  { transform: rotate(-12deg) scale(0.95) translateX(-10px); }
        15%  { transform: rotate(-15deg) scale(0.92) translateX(-14px); filter: brightness(0.7); }
        18%  { transform: rotate(-10deg) scale(0.95) translateX(-7px); }
    }
    /* Left punch → hits fighter 1 */
    .punch-fist-left {
        position: absolute; top: 50%; left: -20px;
        font-size: 3.5rem; pointer-events: none;
        filter: drop-shadow(0 0 10px rgba(255,200,0,0.6));
        animation: fist-punch-left 10s ease-in-out infinite;
    }
    @keyframes fist-punch-left {
        0%, 25%, 50%, 100% { transform: translateY(-50%) translateX(-130px) rotate(35deg) scaleX(-1) scale(1); opacity: 0; }
        10% { transform: translateY(-50%) translateX(-65px) rotate(20deg) scaleX(-1) scale(1.1); opacity: 1; }
        15% { transform: translateY(-50%) translateX(-10px) rotate(5deg) scaleX(-1) scale(1.3); opacity: 1; filter: brightness(1.5); }
        18% { transform: translateY(-50%) translateX(-22px) rotate(-5deg) scaleX(-1) scale(1.2); opacity: 0.8; }
    }
    .impact-flash-left {
        position: absolute; top: 50%; left: -30px;
        font-size: 2.5rem; pointer-events: none;
        animation: impact-burst-left 10s ease-in-out infinite;
    }
    @keyframes impact-burst-left {
        0%, 14%, 25%, 100% { opacity: 0; transform: translateY(-50%) scale(0.3); }
        15% { opacity: 1; transform: translateY(-50%) scale(2) rotate(-25deg); }
        17% { opacity: 0.5; transform: translateY(-50%) scale(1.5) rotate(-18deg); }
        20% { opacity: 0; }
    }
    /* Right punch → hits fighter 2 */
    .punch-fist-right {
        position: absolute; top: 50%; right: -20px;
        font-size: 3.5rem; pointer-events: none;
        filter: drop-shadow(0 0 10px rgba(255,200,0,0.6));
        animation: fist-punch-right 10s ease-in-out infinite;
        animation-delay: 5s;
    }
    @keyframes fist-punch-right {
        0%, 25%, 50%, 100% { transform: translateY(-50%) translateX(130px) rotate(-35deg) scale(1); opacity: 0; }
        10% { transform: translateY(-50%) translateX(65px) rotate(-20deg) scale(1.1); opacity: 1; }
        15% { transform: translateY(-50%) translateX(10px) rotate(-5deg) scale(1.3); opacity: 1; filter: brightness(1.5); }
        18% { transform: translateY(-50%) translateX(22px) rotate(5deg) scale(1.2); opacity: 0.8; }
    }
    .impact-flash-right {
        position: absolute; top: 50%; right: -30px;
        font-size: 2.5rem; pointer-events: none;
        animation: impact-burst-right 10s ease-in-out infinite;
        animation-delay: 5s;
    }
    @keyframes impact-burst-right {
        0%, 14%, 25%, 100% { opacity: 0; transform: translateY(-50%) scale(0.3); }
        15% { opacity: 1; transform: translateY(-50%) scale(2) rotate(25deg); }
        17% { opacity: 0.5; transform: translateY(-50%) scale(1.5) rotate(18deg); }
        20% { opacity: 0; }
    }
    .vs-big {
        font-size: 2rem; color: #ff6600; font-weight: 900;
        text-shadow: 0 0 10px rgba(255,100,0,0.6); opacity: 0.7;
    }
    .health-bar-container {
        width: 140px; height: 18px;
        background: rgba(0,0,0,0.5); border: 2px solid #fff;
        border-radius: 10px; margin: 0.4rem auto; overflow: hidden;
    }
    .health-bar-fill { height: 100%; transition: width 0.3s ease; }
    .fighter-name-big { font-size: 1.1rem; font-weight: 700; margin: 0.4rem 0; }
    .fighter-value-big { font-size: 1rem; font-weight: 600; color: #fff; }

    .tooltip-term { border-bottom: 2px dotted #ffaa00; cursor: help; }
    .tooltip-term:hover { color: #ffaa00; }
</style>
""", unsafe_allow_html=True)

# ─── Constants ───────────────────────────────────────────────────────────────
DEFAULT_TRADING_FEE = 0.003

# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_bullishness(risk_level):
    risk_map = {
        "ultra_conservative": "🐂",
        "conservative": "🐂🐂",
        "moderate": "🐂🐂🐂",
        "aggressive": "🐂🐂🐂🐂",
        "ultra_aggressive": "🐂🐂🐂🐂🐂"
    }
    return risk_map.get(risk_level, "🐂🐂🐂")


def get_bot_icon_html(bot, size="small"):
    photos = st.session_state.get('bot_photos', {})
    bot_id = bot['id']
    if bot_id in photos and photos[bot_id] is not None:
        b64 = base64.b64encode(photos[bot_id]).decode()
        if size == "large":
            return f'<img src="data:image/jpeg;base64,{b64}" class="fighter-icon-big fighter-photo-large">'
        else:
            return f'<img src="data:image/jpeg;base64,{b64}" class="bot-photo-thumb">'
    else:
        if size == "large":
            return f'<span class="fighter-icon-big">{bot["icon"]}</span>'
        else:
            return f'<span style="font-size:1.3rem;vertical-align:middle;">{bot["icon"]}</span>'


def make_chart(values, color='#00ff88'):
    """Altair line chart with auto-centering y-axis for small changes."""
    if len(values) < 2:
        return None
    y_min = min(values)
    y_max = max(values)
    span = max(y_max - y_min, 0.01)
    pad = span * 0.25          # 25% padding so small changes look dramatic
    domain = [max(0, y_min - pad), y_max + pad]

    df = pd.DataFrame({'i': range(len(values)), 'v': values})
    chart = alt.Chart(df).mark_line(
        color=color, strokeWidth=2, interpolate='monotone'
    ).encode(
        x=alt.X('i:Q', title='', axis=alt.Axis(labels=False, ticks=False, grid=False)),
        y=alt.Y('v:Q',
                scale=alt.Scale(domain=domain, zero=False, nice=False),
                title='Portfolio Value ($)',
                axis=alt.Axis(format='$,.2f', labelColor='#aaa',
                              titleColor='#aaa', gridColor='#2a2a4a',
                              tickCount=5))
    ).properties(height=220, background='transparent'
    ).configure_view(strokeWidth=0, fill='transparent'
    ).configure_axis(gridColor='#2a2a4a', labelColor='#aaa', titleColor='#aaa')
    return chart


# ─── Early session state (before main init block) ────────────────────────────
if 'starting_capital' not in st.session_state:
    st.session_state.starting_capital = 100.0
if 'data_mode' not in st.session_state:
    st.session_state.data_mode = 'historical'
if 'bot_photos' not in st.session_state:
    st.session_state.bot_photos = {}
if 'last_realtime_fetch' not in st.session_state:
    st.session_state.last_realtime_fetch = None
if 'total_fees_collected' not in st.session_state:
    st.session_state.total_fees_collected = 0.0

# ─── Main init (runs once) ────────────────────────────────────────────────────
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.running = False
    st.session_state.trade_count = 0
    st.session_state.last_update = None
    st.session_state.start_time = datetime.now()
    st.session_state.last_elimination = datetime.now()
    st.session_state.eliminated_count = 0
    st.session_state.trade_feed = []

    st.session_state.coin_list = [
        "dogecoin", "shiba-inu", "pepe", "bonk", "floki",
        "dogwifhat", "brett", "popcat", "mog-coin", "meme",
        "cat-in-a-dogs-world", "book-of-meme", "dogs-2", "ponke", "myro",
        "wen-4", "smog", "maneki", "gigachad", "degen-base"
    ]
    st.session_state.coin_emojis = {
        "dogecoin": "🐕", "shiba-inu": "🐕", "pepe": "🐸", "bonk": "🔨", "floki": "🐕",
        "dogwifhat": "🐶", "brett": "🎭", "popcat": "🐱", "mog-coin": "😺", "meme": "🎪",
        "cat-in-a-dogs-world": "🐱", "book-of-meme": "📖", "dogs-2": "🐕", "ponke": "🦧", "myro": "🐕",
        "wen-4": "🗓️", "smog": "💨", "maneki": "🐈", "gigachad": "💪", "degen-base": "🎲"
    }

    historical_file = "historical_prices.json"
    with open(historical_file, 'r') as f:
        st.session_state.historical_data = json.load(f)

    st.session_state.time_cursor = 0
    st.session_state.playback_speed = 50
    st.session_state.virtual_time = None
    st.session_state.hall_of_shame = []
    st.session_state.trading_fee = DEFAULT_TRADING_FEE
    st.session_state.latest_elimination = None
    st.session_state.current_leader = None
    st.session_state.price_history = {coin: [] for coin in st.session_state.coin_list}
    st.session_state.prices = {}

    strategies = {
        1: {"risk": "ultra_conservative", "desc": "Safe & Steady",      "trade_freq": 300, "position_size": 0.10, "stop_loss": 0.05, "take_profit": 0.10, "momentum_threshold": 0.03},
        2: {"risk": "conservative",       "desc": "Cautious Trader",    "trade_freq": 180, "position_size": 0.20, "stop_loss": 0.08, "take_profit": 0.15, "momentum_threshold": 0.02},
        3: {"risk": "moderate",           "desc": "Balanced Fighter",   "trade_freq": 120, "position_size": 0.35, "stop_loss": 0.12, "take_profit": 0.20, "momentum_threshold": 0.015},
        4: {"risk": "aggressive",         "desc": "Bold Warrior",       "trade_freq": 60,  "position_size": 0.50, "stop_loss": 0.15, "take_profit": 0.30, "momentum_threshold": 0.01},
        5: {"risk": "ultra_aggressive",   "desc": "YOLO Champion",      "trade_freq": 30,  "position_size": 0.80, "stop_loss": 0.20, "take_profit": 0.50, "momentum_threshold": 0.005},
    }

    llama_bots_data = [
        {"icon": "🦙", "name": "Cuddles"}, {"icon": "🐪", "name": "Snuggles"},
        {"icon": "🦒", "name": "Bouncer"}, {"icon": "🦘", "name": "Thunder"},
        {"icon": "🦬", "name": "Rocket"}
    ]
    mistral_bots_data = [
        {"icon": "🥷", "name": "Frost"}, {"icon": "🗡️", "name": "Steel"},
        {"icon": "⚔️", "name": "Shadow"}, {"icon": "🎯", "name": "Blaze"},
        {"icon": "⚡", "name": "Storm"}
    ]

    st.session_state.bots = []
    num_traders = st.session_state.get('num_traders', 5)
    sc = st.session_state.starting_capital

    for i in range(1, num_traders + 1):
        for team, bots_data, id_prefix, model in [
            ("llama",   llama_bots_data,   "L", "llama"),
            ("mistral", mistral_bots_data, "M", "mistral"),
        ]:
            bot_data = bots_data[min(i-1, len(bots_data)-1)]
            custom_key = f"{team}_{i}"
            if 'custom_trader_configs' in st.session_state and custom_key in st.session_state.custom_trader_configs:
                cfg = st.session_state.custom_trader_configs[custom_key]
                sd = cfg['data']
                strategy = {
                    "risk": sd['risk'], "desc": cfg['style'],
                    "trade_freq": sd['freq'], "position_size": sd['position']/100,
                    "stop_loss": sd['stop']/100, "take_profit": sd['profit']/100,
                    "momentum_threshold": 0.02
                }
                name = cfg['name']
            else:
                strategy = strategies[min(i, 5)]
                name = bot_data['name']

            st.session_state.bots.append({
                "id": f"{id_prefix}{i}",
                "name": f"{bot_data['icon']} {name}",
                "icon": bot_data['icon'],
                "model": model,
                "strategy": strategy,
                "cash": sc,
                "holdings": {},
                "portfolio_value": sc,
                "history": [sc],
                "next_trade_time": datetime.now() + timedelta(seconds=random.uniform(0, 30)),
                "last_action": "🟡 Waiting...",
                "trades_made": 0,
                "wins": 0,
                "losses": 0,
                "fees_paid": 0.0,
                "entry_prices": {},
                "in_danger": False,
                "birth_time": datetime.now()
            })

# ─── Price fetching ───────────────────────────────────────────────────────────

def fetch_prices():
    """Advance the historical cursor by playback_speed // 10 points per cycle."""
    try:
        speed   = st.session_state.playback_speed
        advance = max(1, speed // 10)          # speed=10→1pt, 50→5pts, 100→10pts
        cursor  = st.session_state.time_cursor
        historical = st.session_state.historical_data
        first_coin = list(historical.keys())[0]

        data_len = len(historical[first_coin])
        cursor = cursor % data_len  # safety wrap in case of stale state

        prices = {}
        for coin in st.session_state.coin_list:
            if coin in historical and cursor < len(historical[coin]):
                timestamp, price = historical[coin][cursor]
                prices[coin] = price
                if st.session_state.virtual_time is None:
                    st.session_state.virtual_time = datetime.fromtimestamp(timestamp / 1000)

        # Advance cursor, wrapping around so data loops forever
        new_cursor = (cursor + advance) % data_len
        st.session_state.time_cursor = new_cursor
        ts = historical[first_coin][new_cursor][0]
        st.session_state.virtual_time = datetime.fromtimestamp(ts / 1000)

        return prices if prices else None
    except Exception as e:
        print(f"Historical fetch error: {e}")
        return None


def fetch_prices_realtime():
    try:
        coin_ids = ",".join(st.session_state.coin_list)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_ids}&vs_currencies=usd"
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        prices = {c: data[c]['usd'] for c in st.session_state.coin_list if c in data and 'usd' in data[c]}
        return prices if prices else None
    except Exception as e:
        print(f"Real-time fetch error: {e}")
        return None


# ─── Trading logic ────────────────────────────────────────────────────────────

def calculate_momentum(coin, lookback=3):
    history = st.session_state.price_history.get(coin, [])
    if len(history) < 2:
        return random.uniform(-0.02, 0.02)
    recent = history[-min(lookback, len(history)):]
    return (recent[-1] - recent[0]) / recent[0] if recent[0] != 0 else 0.0


def get_bot_decision(bot):
    now = datetime.now()
    if now < bot['next_trade_time']:
        return {"action": "hold", "coin": "", "amount": 0}

    strategy = bot['strategy']

    for coin, amount in list(bot['holdings'].items()):
        if coin in st.session_state.prices and coin in bot['entry_prices']:
            change = (st.session_state.prices[coin] - bot['entry_prices'][coin]) / bot['entry_prices'][coin]
            if change <= -strategy['stop_loss']:
                return {"action": "sell", "coin": coin, "amount": "all", "reason": "🛑 STOP-LOSS"}
            if change >= strategy['take_profit']:
                return {"action": "sell", "coin": coin, "amount": "all", "reason": "💰 TAKE-PROFIT"}

    danger_mult = 2.0 if bot['in_danger'] else 1.0
    coins = list(st.session_state.prices.keys())
    if not coins:
        return {"action": "hold", "coin": "", "amount": 0}

    force = random.random() < (0.3 * danger_mult)
    momentum = {c: calculate_momentum(c) for c in coins}
    best_buy  = max(momentum.items(), key=lambda x: x[1])

    if best_buy[1] > strategy['momentum_threshold'] or (force and bot['cash'] > 1.0):
        pos = bot['cash'] * strategy['position_size'] * danger_mult
        if pos > 1.0:
            reason = f"📈 MOM+{best_buy[1]*100:.1f}%" if best_buy[1] > strategy['momentum_threshold'] else "🎲 OPP"
            return {"action": "buy", "coin": best_buy[0], "amount": pos, "reason": reason}

    for coin in bot['holdings']:
        if coin in momentum and momentum[coin] < -strategy['momentum_threshold'] * 0.5:
            return {"action": "sell", "coin": coin, "amount": "all", "reason": f"📉 MOM{momentum[coin]*100:.1f}%"}

    return {"action": "hold", "coin": "", "amount": 0}


def execute_trade(bot, decision):
    """Execute trade and track fees so House Fees accumulates correctly."""
    action = decision.get('action', 'hold')
    coin   = decision.get('coin', '').lower()
    amount = decision.get('amount', 0)
    reason = decision.get('reason', '')

    if action == "hold":
        return "💤 Hold"
    if coin not in st.session_state.prices:
        return "❌ Invalid coin"

    price = st.session_state.prices[coin]
    fee_rate = st.session_state.trading_fee

    if action == "buy":
        if amount == "all":
            amount = bot['cash']
        amount = min(float(amount), bot['cash'])
        if amount < 0.50:
            return "❌ Insufficient"

        fee = amount * fee_rate                    # fee is deducted from buy amount
        bot['cash'] -= amount
        coin_amount = (amount - fee) / price
        bot['holdings'][coin] = bot['holdings'].get(coin, 0) + coin_amount
        bot['entry_prices'][coin] = price
        bot['trades_made'] += 1
        bot['fees_paid'] = bot.get('fees_paid', 0.0) + fee
        st.session_state.total_fees_collected += fee
        log_trade(bot, 'BUY', coin, amount, price, reason)
        return f"✅ BUY ${amount:.2f} {coin.upper()[:4]} {reason}"

    elif action == "sell":
        if coin not in bot['holdings'] or bot['holdings'][coin] == 0:
            return f"❌ No {coin.upper()[:4]}"
        coin_amount = bot['holdings'][coin] if amount == "all" else min(float(amount), bot['holdings'][coin])
        gross = coin_amount * price
        fee   = gross * fee_rate
        net   = gross - fee
        bot['cash'] += net
        bot['holdings'][coin] -= coin_amount
        if coin in bot['entry_prices']:
            if price > bot['entry_prices'][coin]:
                bot['wins'] += 1
            else:
                bot['losses'] += 1
        if bot['holdings'][coin] < 0.000001:
            del bot['holdings'][coin]
            bot['entry_prices'].pop(coin, None)
        bot['trades_made'] += 1
        bot['fees_paid'] = bot.get('fees_paid', 0.0) + fee
        st.session_state.total_fees_collected += fee
        log_trade(bot, 'SELL', coin, gross, price, reason)
        return f"✅ SELL ${gross:.2f} {coin.upper()[:4]} {reason}"

    return "❌ Invalid"


def log_trade(bot, action, coin, amount, price, reason):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.trade_feed.insert(0, {
        'log': f"[{ts}] {bot['name']} {action} ${amount:.2f} {coin.upper()[:4]} @ ${price:.6f} {reason}",
        'action': action,
        'bot_model': bot['model']
    })
    if len(st.session_state.trade_feed) > 50:
        st.session_state.trade_feed = st.session_state.trade_feed[:50]


def update_portfolio_values():
    for bot in st.session_state.bots:
        hv = sum(bot['holdings'].get(c, 0) * st.session_state.prices.get(c, 0) for c in bot['holdings'])
        bot['portfolio_value'] = bot['cash'] + hv
        bot['history'].append(bot['portfolio_value'])
        if len(bot['history']) > 500:
            bot['history'] = bot['history'][-500:]


def check_elimination():
    now = datetime.now()
    elapsed = (now - st.session_state.last_elimination).total_seconds()
    interval_secs = st.session_state.get('elimination_interval', 10) * 60

    if elapsed < interval_secs:
        return False

    sorted_bots = sorted(st.session_state.bots, key=lambda b: b['portfolio_value'])
    worst = sorted_bots[0]
    best  = sorted_bots[-1]
    sc    = st.session_state.get('starting_capital', 100.0)
    snum  = int(worst['id'][1])

    lifespan = (now - worst['birth_time']).total_seconds() / 3600
    wr = (worst['wins'] / max(worst['wins'] + worst['losses'], 1)) * 100

    # Accumulate eliminated bot's unpaid fees into global tally (already counted live)
    shame_entry = {
        "name": worst['name'], "model": worst['model'],
        "final_value": worst['portfolio_value'],
        "pnl": worst['portfolio_value'] - sc,
        "trades": worst['trades_made'], "win_rate": wr,
        "lifespan": lifespan,
        "eliminated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "replaced_by": None, "trained_by": best['name']
    }
    st.session_state.bots.remove(worst)

    icons_map = {
        "llama":   ["🦙", "🐪", "🦒", "🦘", "🦬"],
        "mistral": ["🥷", "🗡️", "⚔️", "🎯", "⚡"],
    }
    names_pool = ["Nova","Spark","Flash","Ace","Phoenix","Blaze","Dash","Volt",
                  "Phantom","Titan","Viper","Hawk","Dragon","Cobra","Ronin","Shinobi"]
    icon    = icons_map[worst['model']][snum - 1]
    new_name = f"{icon} {random.choice(names_pool)}"

    base_strategies = {
        1: {"risk": "ultra_conservative", "desc": "Safe & Steady",    "trade_freq": 300, "position_size": 0.10, "stop_loss": 0.05, "take_profit": 0.10, "momentum_threshold": 0.03},
        2: {"risk": "conservative",       "desc": "Cautious Trader",  "trade_freq": 180, "position_size": 0.20, "stop_loss": 0.08, "take_profit": 0.15, "momentum_threshold": 0.02},
        3: {"risk": "moderate",           "desc": "Balanced Fighter", "trade_freq": 120, "position_size": 0.35, "stop_loss": 0.12, "take_profit": 0.20, "momentum_threshold": 0.015},
        4: {"risk": "aggressive",         "desc": "Bold Warrior",     "trade_freq": 60,  "position_size": 0.50, "stop_loss": 0.15, "take_profit": 0.30, "momentum_threshold": 0.01},
        5: {"risk": "ultra_aggressive",   "desc": "YOLO Champion",    "trade_freq": 30,  "position_size": 0.80, "stop_loss": 0.20, "take_profit": 0.50, "momentum_threshold": 0.005},
    }
    base = base_strategies[snum]
    champ = best['strategy']
    learned = {
        "risk":  base["risk"],
        "desc":  base["desc"] + " 🎓",
        "trade_freq":         int(champ["trade_freq"]*0.7         + base["trade_freq"]*0.3),
        "position_size":      champ["position_size"]*0.7          + base["position_size"]*0.3,
        "stop_loss":          champ["stop_loss"]*0.7              + base["stop_loss"]*0.3,
        "take_profit":        champ["take_profit"]*0.7            + base["take_profit"]*0.3,
        "momentum_threshold": champ["momentum_threshold"]*0.7     + base["momentum_threshold"]*0.3,
    }

    new_bot = {
        "id": worst['id'], "name": new_name, "icon": icon, "model": worst['model'],
        "strategy": learned, "cash": sc, "holdings": {}, "portfolio_value": sc,
        "history": [sc],
        "next_trade_time": datetime.now() + timedelta(seconds=random.uniform(0, 30)),
        "last_action": "🟢 NEW BOT!", "trades_made": 0,
        "wins": 0, "losses": 0, "fees_paid": 0.0,
        "entry_prices": {}, "in_danger": False, "birth_time": datetime.now()
    }
    st.session_state.bots.append(new_bot)
    st.session_state.last_elimination = now
    st.session_state.eliminated_count += 1

    st.session_state.latest_elimination = analyze_bot_strategy(worst, is_winner=False)
    st.session_state.current_leader     = analyze_bot_strategy(best,  is_winner=True)

    shame_entry["replaced_by"] = new_name
    st.session_state.hall_of_shame.insert(0, shame_entry)
    st.session_state.trade_feed.insert(0, {
        'log': f"💀 ELIMINATED: {shame_entry['name']} (${shame_entry['final_value']:.2f}) → {new_name} trained by {best['name']}!",
        'action': 'ELIMINATE', 'bot_model': worst['model']
    })
    return True


def mark_danger_zone():
    sb = sorted(st.session_state.bots, key=lambda b: b['portfolio_value'])
    for bot in st.session_state.bots:
        bot['in_danger'] = bot in sb[:3]


def trading_cycle():
    prices = fetch_prices_realtime() if st.session_state.data_mode == 'realtime' else fetch_prices()
    if prices is None:
        return False

    st.session_state.prices = prices
    for coin, price in prices.items():
        st.session_state.price_history.setdefault(coin, []).append(price)
        if len(st.session_state.price_history[coin]) > 100:
            st.session_state.price_history[coin] = st.session_state.price_history[coin][-100:]

    mark_danger_zone()
    now = datetime.now()
    for bot in st.session_state.bots:
        dec = get_bot_decision(bot)
        bot['last_action'] = execute_trade(bot, dec)
        if dec['action'] != 'hold':
            delay = bot['strategy']['trade_freq'] * random.uniform(0.8, 1.2)
            if bot['in_danger']:
                delay *= 0.5
            bot['next_trade_time'] = now + timedelta(seconds=delay)

    update_portfolio_values()
    try:
        check_elimination()
    except Exception as e:
        print(f"Elimination error (non-fatal): {e}")
    st.session_state.trade_count += 1
    st.session_state.last_update = datetime.now()
    return True


def format_pnl(pnl, pnl_pct):
    if pnl > 0.01:
        return f"🟢 ${pnl:+.2f} ({pnl_pct:+.1f}%)"
    elif pnl < -0.01:
        return f"🔴 ${pnl:+.2f} ({pnl_pct:+.1f}%)"
    return f"🟡 ${pnl:+.2f} ({pnl_pct:+.1f}%)"


def analyze_bot_strategy(bot, is_winner=True):
    sc = st.session_state.get('starting_capital', 100.0)
    pnl = bot['portfolio_value'] - sc
    pnl_pct = (pnl / sc) * 100
    wr = (bot['wins'] / max(bot['wins'] + bot['losses'], 1)) * 100
    age = (datetime.now() - bot['birth_time']).total_seconds() / 3600
    s = bot['strategy']
    a = {
        'bot_name': bot['name'], 'final_value': bot['portfolio_value'],
        'pnl': pnl, 'pnl_pct': pnl_pct,
        'trades': bot['trades_made'], 'wins': bot['wins'], 'losses': bot['losses'],
        'win_rate': wr, 'age': age,
        'position_size': s.get('position_size', 0)*100,
        'stop_loss':     s.get('stop_loss', 0)*100,
        'take_profit':   s.get('take_profit', 0)*100,
        'trade_freq':    s.get('trade_freq', 0),
        'risk_level':    s.get('risk', 'unknown'),
    }
    if is_winner:
        a['summary'] = f"🏆 {bot['name']} dominated with {s['desc']} approach"
        a['key_points'] = [
            f"✓ {a['position_size']:.0f}% position sizing captured major moves",
            f"✓ {a['stop_loss']:.0f}% stop-loss protected capital",
            f"✓ {a['win_rate']:.0f}% win rate shows strong execution",
            f"✓ {a['trades']} trades over {age:.1f}h = active management",
        ]
        a['lesson'] = f"💡 WINNING: {'Aggressive sizing works WITH high win rate!' if a['position_size']>50 and a['win_rate']>60 else 'Consistency beats heroics!'}"
    else:
        a['summary'] = f"💀 {bot['name']} eliminated using {s['desc']} strategy"
        a['key_points'] = [
            f"✗ {a['position_size']:.0f}% position sizing {'too small' if a['position_size']<30 else 'too large for win rate'}",
            f"✗ {a['stop_loss']:.0f}% stop-loss {'cut winners early' if a['stop_loss']<10 else 'allowed big losses'}",
            f"✗ {a['win_rate']:.0f}% win rate",
            f"✗ {a['trades']} trades over {age:.1f}h",
        ]
        a['lesson'] = f"⚠️ LOSING: {'Too conservative, missed moves!' if a['position_size']<20 else 'Review your edge before sizing up!'}"
    return a


def display_strategy_analysis(a):
    c = "#00ff88" if a['pnl'] > 0 else "#ff6666"
    bc = "rgba(0,255,136,0.3)" if a['pnl'] > 0 else "rgba(255,102,102,0.3)"
    st.markdown(f"""
    <div style="background:rgba(26,31,58,0.95);border:2px solid {bc};border-radius:10px;padding:1.2rem;margin:0.8rem 0;">
        <h3 style="color:{c};margin-top:0;">{a['summary']}</h3>
        <div>Final: ${a['final_value']:.2f} ({a['pnl']:+.2f} / {a['pnl_pct']:+.1f}%)</div>
        <div style="margin:0.8rem 0;">
            Position: {a['position_size']:.0f}% | Stop: {a['stop_loss']:.0f}% | Profit: {a['take_profit']:.0f}%
            | Freq: ~{a['trade_freq']//60}min | Risk: {a['risk_level'].replace('_',' ').title()}
        </div>
        <div>{'<br>'.join(a['key_points'])}</div>
        <div style="background:rgba(255,170,0,0.1);padding:0.8rem;border-radius:5px;border-left:4px solid #ffaa00;margin-top:0.8rem;">
            {a['lesson']}
        </div>
    </div>
    """, unsafe_allow_html=True)


TRADING_TERMS = {
    "Stop-Loss": "A preset price where you automatically sell to limit losses.",
    "Take-Profit": "A target price where you automatically sell to lock in gains.",
    "Position Size": "How much of your portfolio you invest in one trade.",
    "Win Rate": "Percentage of profitable trades.",
    "Trading Fee": "Cost charged per trade (buy OR sell). Fees reduce profits!",
    "Round-Trip Cost": "Total fee for buying THEN selling.",
}

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ CUSTOMIZE YOUR BATTLE")
    st.markdown("**Build your AI trading team!**")
    st.markdown("---")

    if 'num_traders' not in st.session_state:
        st.session_state.num_traders = 5
    if 'custom_trader_configs' not in st.session_state:
        st.session_state.custom_trader_configs = {}
    if 'advanced_mode' not in st.session_state:
        st.session_state.advanced_mode = False

    st.session_state.advanced_mode = st.checkbox("🎓 Advanced Mode", value=st.session_state.advanced_mode)
    st.caption("✅ Advanced styles" if st.session_state.advanced_mode else "📚 Beginner styles")
    st.markdown("---")

    st.markdown("**📊 Traders Per Team**")
    st.session_state.num_traders = st.slider("Traders per team", 1, 5, st.session_state.num_traders)
    st.caption(f"Total: {st.session_state.num_traders * 2} traders")
    st.markdown("---")

    if st.session_state.advanced_mode:
        trading_styles = {
            "Ultra Conservative 🛡️": {"risk": "ultra_conservative", "position": 10, "stop": 5,  "profit": 10, "freq": 300},
            "Conservative 🔒":        {"risk": "conservative",       "position": 20, "stop": 8,  "profit": 15, "freq": 180},
            "Balanced ⚖️":            {"risk": "moderate",           "position": 35, "stop": 12, "profit": 20, "freq": 120},
            "Aggressive":             {"risk": "aggressive",         "position": 50, "stop": 15, "profit": 30, "freq": 60},
            "Ultra Aggressive 🚀":    {"risk": "ultra_aggressive",   "position": 80, "stop": 20, "profit": 50, "freq": 30},
        }
    else:
        trading_styles = {
            "🛡️ Safe Player":    {"risk": "ultra_conservative", "position": 10, "stop": 5,  "profit": 10, "freq": 300},
            "🔒 Careful Trader": {"risk": "conservative",       "position": 20, "stop": 8,  "profit": 15, "freq": 180},
            "⚖️ Balanced":       {"risk": "moderate",           "position": 35, "stop": 12, "profit": 20, "freq": 120},
            "Risk Taker":        {"risk": "aggressive",         "position": 50, "stop": 15, "profit": 30, "freq": 60},
            "🚀 All-In Gambler": {"risk": "ultra_aggressive",   "position": 80, "stop": 20, "profit": 50, "freq": 30},
        }

    for team_label, id_prefix in [("🦙 LLAMA TEAM", "L"), ("🥷 MISTRAL TEAM", "M")]:
        st.markdown(f"### {team_label}")
        for i in range(1, st.session_state.num_traders + 1):
            key = f"{'llama' if id_prefix=='L' else 'mistral'}_{i}"
            with st.expander(f"Trader #{i}", expanded=False):
                default_name = f"{'Llama' if id_prefix=='L' else 'Mistral'}-{i}"
                name = st.text_input("Name",
                    value=st.session_state.custom_trader_configs.get(key, {}).get('name', default_name),
                    key=f"name_{key}", max_chars=15)
                opts = list(trading_styles.keys())
                def_style = opts[min(i-1, len(opts)-1)]
                saved = st.session_state.custom_trader_configs.get(key, {}).get('style', def_style)
                if saved not in opts:
                    saved = def_style
                style = st.selectbox("Trading Style", opts,
                    index=opts.index(saved), key=f"style_{key}")
                sd = trading_styles[style]
                st.caption(f"💰 {sd['position']}% | 🛑 {sd['stop']}% | 🎯 {sd['profit']}%")
                st.session_state.custom_trader_configs[key] = {'name': name, 'style': style, 'data': sd}

                photo = st.file_uploader("📷 Bot photo", type=['jpg','jpeg','png'],
                    key=f"photo_{key}", help="Replaces the emoji icon everywhere")
                bot_id = f"{id_prefix}{i}"
                if photo is not None:
                    st.session_state.bot_photos[bot_id] = photo.read()
                    st.success("Photo saved!")
                elif bot_id in st.session_state.bot_photos:
                    st.caption("📷 Custom photo active")
                    if st.button("Remove photo", key=f"rm_{key}"):
                        del st.session_state.bot_photos[bot_id]
                        st.rerun()
        st.markdown("---")

    if st.button("🔄 Reset to Defaults"):
        st.session_state.num_traders = 5
        st.session_state.custom_trader_configs = {}
        st.session_state.advanced_mode = False
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN UI
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<h1 class="main-title">⚔️ TRADERDOME: MEME COINS 🔨</h1>', unsafe_allow_html=True)

# ── Gory welcome (fun/violent theme FIRST) ────────────────────────────────────
st.markdown("""
<div class="gory-welcome">
    <div class="gory-title">☠️ 💀 ⚔️ &nbsp; Welcome to the TraderDome &nbsp; ⚔️ 💀 ☠️</div>
    🩸 Ten AI bots enter. Only one can reign supreme. They clash, bleed value, and face brutal elimination
    when performance falls short. Bots are wiped, replaced, and trained from the corpse of the champion.
    There is <strong>no mercy</strong> in the Dome — only charts, carnage, and cold hard crypto. 🪓💥🔥
</div>
""", unsafe_allow_html=True)

# ── Disclaimer (after the gore) ───────────────────────────────────────────────
st.markdown("""
<div class="disclaimer-banner">
    🛡️ <strong>Safe Practice Zone:</strong> This is fake money — experiment freely, learn how markets move,
    and have fun without risking a real dollar. Only invest what you can afford to lose when trading for real.
    This is not financial advice — it's your playground. Enjoy!
</div>
""", unsafe_allow_html=True)

# ── Data source / Starting capital / Coming soon ──────────────────────────────
top_col1, top_col2, top_col3 = st.columns([2, 2, 2])

with top_col1:
    st.markdown("**📡 Data Source**")
    new_mode = st.radio("datasrc", ["Historical Data", "Real-Time Data"],
        index=0 if st.session_state.data_mode == 'historical' else 1,
        horizontal=True, label_visibility="collapsed")
    st.session_state.data_mode = 'historical' if new_mode == "Historical Data" else 'realtime'
    if st.session_state.data_mode == 'realtime':
        st.warning("⚠️ Real-time mode: live CoinGecko data. 60s+ minimum between cycles.")

with top_col2:
    st.markdown("**💵 Starting Capital Per Bot**")
    cap_locked = st.session_state.get('running', False)
    new_cap = st.number_input("Capital", min_value=10.0, max_value=10000.0,
        value=float(st.session_state.starting_capital), step=10.0, format="%.0f",
        disabled=cap_locked, label_visibility="collapsed",
        help="Starting cash per bot. Use Reset Simulation to apply changes.")
    st.markdown(f"**${new_cap:,.0f}** per bot")
    if not cap_locked:
        st.session_state.starting_capital = new_cap
    if not cap_locked and st.session_state.get('trade_count', 0) > 0:
        if st.button("🔄 Reset Simulation", help="Clears bots and history"):
            for k in ['initialized','running','trade_count','last_update','start_time',
                      'last_elimination','eliminated_count','trade_feed','bots','prices',
                      'price_history','hall_of_shame','latest_elimination','current_leader',
                      'time_cursor','virtual_time','total_fees_collected','last_realtime_fetch']:
                st.session_state.pop(k, None)
            st.session_state.total_fees_collected = 0.0
            st.rerun()

with top_col3:
    st.markdown("**🔮 Coming Next**")
    st.button("🏦 401(k) Simulator — Coming Soon!", disabled=True,
        use_container_width=True,
        help="Multi-asset portfolio trading with stocks, bonds, ETFs, and treasuries.")
    st.caption("Stocks · Bonds · ETFs · Treasuries")

st.markdown("---")

# ── Subtitle / mode info ──────────────────────────────────────────────────────
if st.session_state.get('virtual_time'):
    vt = st.session_state.virtual_time.strftime('%Y-%m-%d %H:%M')
    if st.session_state.data_mode == 'realtime':
        st.markdown(f'<div class="subtitle">🌐 REAL-TIME MODE | 🦙 LLAMA vs MISTRAL 🥷 | 📅 {vt}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="subtitle">⏰ TIME MACHINE | 🦙 LLAMA vs MISTRAL 🥷 | 📅 {vt} | ⚡ {st.session_state.playback_speed}x</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="subtitle">🦙 LLAMA AI TRADERS vs MISTRAL AI TRADERS 🥷 | READY TO LAUNCH</div>', unsafe_allow_html=True)

st.success("🎮 **CUSTOMIZE YOUR BATTLE!** ← Open the sidebar (top-left **>**) to configure traders, names, styles, and bot photos!")

# ── Controls ──────────────────────────────────────────────────────────────────
ctrl1, ctrl2, ctrl3 = st.columns([2, 2, 2])

with ctrl1:
    if st.session_state.data_mode == 'historical':
        st.markdown("**⚡ Playback Speed**")
        st.caption("Higher = more data points per cycle + faster refresh")
        new_speed = st.slider("spd", 1, 100, st.session_state.playback_speed,
            label_visibility="collapsed",
            help="Speed 10 → advance 1pt/cycle. Speed 50 → 5pts. Speed 100 → 10pts.")
        st.session_state.playback_speed = new_speed
        adv = max(1, new_speed // 10)
        slp = round(max(0.15, 0.6 - new_speed * 0.004), 2)
        st.caption(f"Advancing {adv} data point(s)/cycle | ~{slp}s refresh")
    else:
        st.markdown("**⏱️ Cycle Speed (Real-Time)**")
        st.info("60s minimum enforced by API")

with ctrl2:
    st.markdown("**💰 Trading Fee %**")
    st.caption("Deducted from every buy AND sell")
    new_fee = st.slider("fee", 0.0, 1.0, st.session_state.trading_fee * 100,
        step=0.05, label_visibility="collapsed",
        help="Fee is deducted from each transaction. Higher fee = more House Fees.") / 100
    st.session_state.trading_fee = new_fee
    st.caption(f"{new_fee*100:.2f}% per trade | {new_fee*200:.2f}% round-trip")

with ctrl3:
    st.markdown("**⏱️ Elimination Interval**")
    st.caption("Real clock time between bot eliminations")
    if 'elimination_interval' not in st.session_state:
        st.session_state.elimination_interval = 10
    elim_opts   = [1, 2, 5, 10, 15, 30, 60, 120, 180, 360, 720, 1440]
    elim_labels = ["1m","2m","5m","10m","15m","30m","1h","2h","3h","6h","12h","24h"]
    cur_idx = min(range(len(elim_opts)), key=lambda i: abs(elim_opts[i] - st.session_state.elimination_interval))
    new_idx = st.select_slider("elim", options=range(len(elim_opts)), value=cur_idx,
        format_func=lambda x: elim_labels[x], label_visibility="collapsed")
    st.session_state.elimination_interval = elim_opts[new_idx]

st.markdown("---")

# ── Control panel + key metrics ───────────────────────────────────────────────
cp1, cp2, cp3, cp4, cp5 = st.columns([2, 2, 2, 2, 2])

with cp1:
    btn_label = "🚀 START" if not st.session_state.running else "⏸️ PAUSE"
    if st.button(btn_label, use_container_width=True, type="primary"):
        st.session_state.running = not st.session_state.running

with cp2:
    st.metric("⚡ Trade Cycles", st.session_state.trade_count)

with cp3:
    elapsed_e = (datetime.now() - st.session_state.last_elimination).total_seconds()
    remaining = max(0, st.session_state.get('elimination_interval', 10) * 60 - elapsed_e)
    st.metric("💀 Next Elimination", f"{int(remaining//60)}m {int(remaining%60)}s")

with cp4:
    st.metric("Eliminations", st.session_state.eliminated_count)

with cp5:
    if st.session_state.data_mode == 'realtime':
        st.metric("🕐 Mode", "🌐 LIVE")
    elif st.session_state.historical_data and st.session_state.coin_list:
        fc = st.session_state.coin_list[0]
        if fc in st.session_state.historical_data:
            hist = st.session_state.historical_data[fc]
            sd = datetime.fromtimestamp(hist[0][0]/1000).strftime('%b %d')
            ed = datetime.fromtimestamp(hist[-1][0]/1000).strftime('%b %d %Y')
            st.metric("🕐 Mode", "⏰ TIME MACHINE")
            st.caption(f"📅 {sd}–{ed}")

# ── Team scores + House Fees ──────────────────────────────────────────────────
st.markdown("---")
llama_total   = sum(b['portfolio_value'] for b in st.session_state.bots if b['model'] == 'llama')
mistral_total = sum(b['portfolio_value'] for b in st.session_state.bots if b['model'] == 'mistral')
total_taste   = st.session_state.get('total_fees_collected', 0.0)

sc1, sc2, sc3, sc4 = st.columns([1, 1, 1, 1])

with sc1:
    st.markdown(f"""
    <div class="stat-box" style="border-color:#00ff88;">
        <div class="stat-label">🦙 Llama Team</div>
        <div class="stat-value" style="color:#00ff88;">${llama_total:.2f}</div>
    </div>""", unsafe_allow_html=True)

with sc2:
    winner = "🦙 LLAMA LEADS!" if llama_total > mistral_total else "🥷 MISTRAL LEADS!" if mistral_total > llama_total else "⚔️ TIE!"
    lead   = abs(llama_total - mistral_total)
    st.markdown(f"""
    <div class="stat-box" style="border-color:#ffaa00;">
        <div class="stat-label">Battle Status</div>
        <div class="stat-value" style="color:#ffaa00;font-size:1.5rem;">{winner}</div>
        <div class="stat-label">Lead: ${lead:.2f}</div>
    </div>""", unsafe_allow_html=True)

with sc3:
    st.markdown(f"""
    <div class="stat-box" style="border-color:#00ccff;">
        <div class="stat-label">🥷 Mistral Team</div>
        <div class="stat-value" style="color:#00ccff;">${mistral_total:.2f}</div>
    </div>""", unsafe_allow_html=True)

with sc4:
    st.markdown(f"""
    <div class="taste-box">
        <div class="stat-label" style="color:#ff9944;">🏦 House Fees</div>
        <div class="stat-value" style="color:#ff6600;font-size:1.8rem;">${total_taste:.2f}</div>
        <div class="stat-label">Total fees collected from all bots</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Strategy analysis ─────────────────────────────────────────────────────────
if st.session_state.latest_elimination or st.session_state.current_leader:
    st.markdown("### 📚 STRATEGY ANALYSIS & LESSONS")
    ac1, ac2 = st.columns(2)
    with ac1:
        if st.session_state.current_leader:
            st.markdown("#### 🏆 CURRENT CHAMPION")
            display_strategy_analysis(st.session_state.current_leader)
    with ac2:
        if st.session_state.latest_elimination:
            st.markdown("#### 💀 LATEST ELIMINATION")
            display_strategy_analysis(st.session_state.latest_elimination)
    st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
#  BATTLE ARENA + FEED  (side by side, equal weight)
# ═══════════════════════════════════════════════════════════════════════════════
arena_col, feed_col = st.columns([3, 2])

with arena_col:
    if len(st.session_state.bots) >= 2:
        sb = sorted(st.session_state.bots, key=lambda b: b['portfolio_value'], reverse=True)
        f1, f2 = sb[0], sb[1]
        sc_val = st.session_state.get('starting_capital', 100.0)
        f1_hp  = min(100, max(0, (f1['portfolio_value'] / sc_val) * 100))
        f2_hp  = min(100, max(0, (f2['portfolio_value'] / sc_val) * 100))
        lead   = f1['portfolio_value'] - f2['portfolio_value']
        f1_c   = '#00ff88' if f1['model'] == 'llama' else '#00ccff'
        f2_c   = '#00ff88' if f2['model'] == 'llama' else '#00ccff'
        f1_icon = get_bot_icon_html(f1, "large")
        f2_icon = get_bot_icon_html(f2, "large")

        st.markdown(f"""
<div class="arena-box">
<div class="arena-title">⚔️ CHAMPIONSHIP BATTLE ⚔️</div>
<div class="fighter-row">

<div class="fighter-box fighter-left">
  <div style="font-size:1.3rem;font-weight:900;color:#ffd700;margin-bottom:0.4rem;">🥇 1ST PLACE</div>
  <div class="punch-fist-left">👊</div>
  <div class="impact-flash-left">💥</div>
  {f1_icon}
  <div class="fighter-name-big" style="color:{f1_c};">{f1['name']}</div>
  <div class="health-bar-container">
    <div class="health-bar-fill" style="width:{f1_hp}%;background:{f1_c};"></div>
  </div>
  <div class="fighter-value-big">${f1['portfolio_value']:.2f}</div>
</div>

<div class="fighter-box"><div class="vs-big">VS</div></div>

<div class="fighter-box fighter-right">
  <div style="font-size:1.3rem;font-weight:900;color:#c0c0c0;margin-bottom:0.4rem;">🥈 2ND PLACE</div>
  <div class="punch-fist-right">👊</div>
  <div class="impact-flash-right">💥</div>
  {f2_icon}
  <div class="fighter-name-big" style="color:{f2_c};">{f2['name']}</div>
  <div class="health-bar-container">
    <div class="health-bar-fill" style="width:{f2_hp}%;background:{f2_c};"></div>
  </div>
  <div class="fighter-value-big">${f2['portfolio_value']:.2f}</div>
</div>

</div>
<div style="font-size:0.95rem;color:#ffaa00;font-weight:600;">Lead: ${lead:.2f}</div>
</div>
""", unsafe_allow_html=True)

with feed_col:
    st.markdown("### 📡 BATTLE FEED")
    feed_html = '<div class="trade-feed">'
    for trade in st.session_state.trade_feed[:35]:
        cls = 'trade-buy' if trade['action'] == 'BUY' else 'trade-sell' if trade['action'] == 'SELL' else ''
        feed_html += f'<div class="trade-item {cls}">{trade["log"]}</div>'
    feed_html += '</div>'
    st.markdown(feed_html, unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
#  LEADERBOARD  (full width)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""### 🏆 WARRIOR LEADERBOARD
<p style='font-size:0.88rem;color:#aaa;margin-top:-0.4rem;'>
Ranked by Portfolio Value &nbsp;•&nbsp; Bullishness = risk level (🐂 conservative → 🐂🐂🐂🐂🐂 ultra-aggressive)
</p>""", unsafe_allow_html=True)

sc_val = st.session_state.get('starting_capital', 100.0)
sorted_bots = sorted(st.session_state.bots, key=lambda b: b['portfolio_value'], reverse=True)
lb_data = []
for i, bot in enumerate(sorted_bots):
    pnl     = bot['portfolio_value'] - sc_val
    pnl_pct = (pnl / sc_val) * 100
    age     = (datetime.now() - bot['birth_time']).total_seconds() / 3600
    wr      = (bot['wins'] / max(bot['wins'] + bot['losses'], 1)) * 100
    lb_data.append({
        "Rank":        f"{i+1} {'💀' if bot['in_danger'] else ''}",
        "Team":        "🦙" if bot['model'] == 'llama' else "🥷",
        "Bot":         bot['name'],
        "Bullishness": get_bullishness(bot['strategy'].get('risk', 'moderate')),
        "Cash":        f"${bot['cash']:.2f}",
        "Portfolio":   f"${bot['portfolio_value']:.2f}",
        "P&L":         format_pnl(pnl, pnl_pct),
        "Fees Paid":   f"${bot.get('fees_paid',0):.2f}",
        "Trades":      bot['trades_made'],
        "Win%":        f"{wr:.0f}%",
        "Age":         f"{age:.1f}h",
    })
st.dataframe(lb_data, use_container_width=True, hide_index=True, height=380)

# ═══════════════════════════════════════════════════════════════════════════════
#  PERFORMANCE CHARTS  (Altair, auto-centering y-axis)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("### 📈 TEAM PERFORMANCE BATTLE")
ch1, ch2 = st.columns(2)

def build_aggregate(bots_list):
    if not bots_list or len(bots_list[0]['history']) < 2:
        return []
    n = max(len(b['history']) for b in bots_list)
    return [sum(b['history'][i] if i < len(b['history']) else b['history'][-1]
                for b in bots_list)
            for i in range(n)]

with ch1:
    st.markdown("#### 🦙 Llama AI Traders")
    lb = [b for b in st.session_state.bots if b['model'] == 'llama']
    agg = build_aggregate(lb)
    if agg:
        chart = make_chart(agg, '#00ff88')
        if chart:
            st.altair_chart(chart, use_container_width=True)

with ch2:
    st.markdown("#### 🥷 Mistral AI Traders")
    mb = [b for b in st.session_state.bots if b['model'] == 'mistral']
    agg = build_aggregate(mb)
    if agg:
        chart = make_chart(agg, '#00ccff')
        if chart:
            st.altair_chart(chart, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  AI TRADER DETAILS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("### 🤖 AI TRADER DETAILS")

td1, td2 = st.columns(2)
llama_sorted   = sorted([b for b in st.session_state.bots if b['model']=='llama'],   key=lambda x: int(x['id'][1]))
mistral_sorted = sorted([b for b in st.session_state.bots if b['model']=='mistral'], key=lambda x: int(x['id'][1]))

for col, bots_list, card_cls, hdr_cls, hdr_txt in [
    (td1, llama_sorted,   "llama-card",   "llama-header",   "🦙 LLAMA AI TRADERS"),
    (td2, mistral_sorted, "mistral-card", "mistral-header", "🥷 MISTRAL AI TRADERS"),
]:
    with col:
        st.markdown(f'<div class="team-header {hdr_cls}">{hdr_txt}</div>', unsafe_allow_html=True)
        for bot in bots_list:
            pnl     = bot['portfolio_value'] - sc_val
            pnl_pct = (pnl / sc_val) * 100
            pnl_d   = format_pnl(pnl, pnl_pct)
            age     = (datetime.now() - bot['birth_time']).total_seconds() / 3600
            wr      = (bot['wins'] / max(bot['wins'] + bot['losses'], 1)) * 100
            holdings_str = " ".join(
                f"{st.session_state.coin_emojis.get(c,'🪙')} {a:.2f}"
                for c, a in list(bot['holdings'].items())[:5]
            ) or "None"
            dclass = " danger-zone" if bot['in_danger'] else ""
            dtxt   = '<br><span class="elimination-warning">⚠️ DANGER ZONE ⚠️</span>' if bot['in_danger'] else ""
            icon_html = get_bot_icon_html(bot, "small")
            fees_d = bot.get('fees_paid', 0.0)

            st.markdown(f"""
            <div class="bot-card {card_cls}{dclass}">
                <strong>{icon_html} {bot['name']}</strong> — {bot['strategy']['desc']}{dtxt}<br>
                💰 Cash: ${bot['cash']:.2f} | 📊 Portfolio: ${bot['portfolio_value']:.2f} | {pnl_d}<br>
                🪙 Holdings: {holdings_str}<br>
                📈 Trades: {bot['trades_made']} | Win: {wr:.0f}% | Fees: ${fees_d:.2f} | Age: {age:.1f}h<br>
                ⚡ Last: {bot.get('last_action','Waiting...')}
            </div>
            """, unsafe_allow_html=True)

# ─── Trading Glossary ─────────────────────────────────────────────────────────
with st.expander("📚 TRADING GLOSSARY — Learn by Doing!", expanded=False):
    st.markdown("### 🎓 Interactive Trading Concepts")
    st.markdown("---")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "💰 Position Size", "🛑 Stop-Loss & Take-Profit",
        "💸 Trading Fees", "📊 Win Rate", "📈 DCA", "🎲 Risk/Reward"
    ])
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            port = st.number_input("Portfolio ($)", 100, 10000, 1000, 100, key="g_port")
            pct  = st.slider("Position %", 10, 100, 35, 5, key="g_pct")
        with c2:
            val = port * pct / 100
            st.metric("Invested", f"${val:.2f}")
            st.metric("Remaining", f"${port-val:.2f}")
            st.progress(pct/100)
        st.info(f"💡 {pct}% position = ${val:.2f} in this trade.")
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            bp   = st.number_input("Buy Price ($)", 0.001, 100.0, 1.0, 0.01, key="g_bp")
            slp  = st.slider("Stop-Loss %", 5, 30, 10, 5, key="g_sl")
            tpp  = st.slider("Take-Profit %", 10, 100, 20, 10, key="g_tp")
        with c2:
            st.error(f"🛑 Stop at ${bp*(1-slp/100):.3f} (−{slp}%)")
            st.success(f"🎯 Profit at ${bp*(1+tpp/100):.3f} (+{tpp}%)")
    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            amt = st.number_input("Trade ($)", 10, 10000, 100, 10, key="g_amt")
            fp  = st.slider("Fee %", 0.1, 1.0, 0.3, 0.1, key="g_fp")
        with c2:
            fee = amt * fp / 100
            st.metric("Buy Fee",  f"${fee:.2f}")
            st.metric("Sell Fee", f"${fee:.2f}")
            st.metric("Round-Trip", f"${fee*2:.2f}", delta=f"-{fp*2:.1f}%")
        st.warning(f"⚠️ Need >{fp*2:.1f}% profit just to break even!")
    with tab4:
        c1, c2 = st.columns(2)
        with c1:
            w = st.number_input("Wins",   0, 100, 7, 1, key="g_w")
            l = st.number_input("Losses", 0, 100, 3, 1, key="g_l")
        with c2:
            tot = w + l
            if tot > 0:
                wr = w/tot*100
                st.metric("Win Rate", f"{wr:.1f}%")
                st.progress(wr/100)
                st.success("🎉 Excellent!") if wr >= 60 else (st.info("👍 Above breakeven") if wr >= 50 else st.warning("📉 Needs work"))
    with tab5:
        c1, c2 = st.columns(2)
        with c1:
            inv = st.number_input("Per Period ($)", 10, 1000, 100, 10, key="g_inv")
            per = st.slider("Periods", 1, 24, 12, 1, key="g_per")
            ap  = st.number_input("Avg Price ($)", 0.01, 100.0, 1.0, 0.01, key="g_ap")
        with c2:
            tot_inv  = inv * per
            tot_coin = tot_inv / ap
            st.metric("Total Invested", f"${tot_inv:.2f}")
            st.metric("Coins Bought",   f"{tot_coin:.2f}")
            np_ = st.slider("New Price", ap*0.5, ap*2, ap, 0.01, key="g_np")
            st.metric("Portfolio Value", f"${tot_coin*np_:.2f}", delta=f"{tot_coin*np_-tot_inv:+.2f}")
    with tab6:
        c1, c2 = st.columns(2)
        with c1:
            en = st.number_input("Entry ($)", 0.01, 100.0, 1.0, 0.01, key="g_en")
            st_ = st.number_input("Stop ($)", 0.01, en, en*0.9, 0.01, key="g_st")
            tg = st.number_input("Target ($)", en, 200.0, en*1.2, 0.01, key="g_tg")
        with c2:
            risk_v = en - st_; rew_v = tg - en
            if risk_v > 0:
                ratio = rew_v / risk_v
                st.metric("Risk", f"${risk_v:.2f}")
                st.metric("Reward", f"${rew_v:.2f}")
                st.metric("R/R Ratio", f"1:{ratio:.1f}")
                st.success("🎉 Great!") if ratio >= 3 else (st.info("👍 OK") if ratio >= 2 else st.warning("⚠️ Low"))

    st.markdown("---")
    st.markdown("### 📖 Key Terms")
    t1, t2, t3 = st.tabs(["📊 Core Concepts", "🐂🐻 Market Terms", "💼 Advanced"])
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**🐂 Bullishness (Risk Levels)**")
            for emoji, label in [("🐂","Ultra Conservative (10%)"),("🐂🐂","Conservative (20%)"),
                                   ("🐂🐂🐂","Balanced (35%)"),("🐂🐂🐂🐂","Aggressive (50%)"),
                                   ("🐂🐂🐂🐂🐂","Ultra Aggressive (80%)")]:
                st.caption(f"{emoji} = {label}")
        with c2:
            for term, defn in [("**💼 Portfolio**","Total value: cash + assets"),
                                ("**📈 P&L**","Profit & Loss from trading"),
                                ("**🎯 Position Size**","% of portfolio per trade"),
                                ("**🌊 Momentum**","Price trending direction")]:
                st.markdown(term); st.caption(defn)
    with t2:
        c1, c2 = st.columns(2)
        with c1:
            for term, defn in [("**🐂 Bull Market**","Prices rising, optimism"),
                                ("**🐻 Bear Market**","Prices falling, pessimism"),
                                ("**📊 Market Cap**","Price × Total Supply"),
                                ("**😱 FOMO**","Fear Of Missing Out")]:
                st.markdown(term); st.caption(defn)
        with c2:
            for term, defn in [("**🛡️ Support**","Price floor where buyers step in"),
                                ("**🚧 Resistance**","Price ceiling sellers defend"),
                                ("**📈 Volume**","Amount traded — high = strong move"),
                                ("**☠️ Danger Zone**","Bottom 3 facing elimination")]:
                st.markdown(term); st.caption(defn)
    with t3:
        c1, c2 = st.columns(2)
        with c1:
            for term, defn in [("**💵 DCA**","Invest fixed amount regularly"),
                                ("**🎯 Risk/Reward**","Aim 1:2 or better"),
                                ("**🌈 Diversification**","Spread across assets"),
                                ("**📊 Technical Analysis**","Study chart patterns")]:
                st.markdown(term); st.caption(defn)
        with c2:
            for term, defn in [("**📰 Fundamental Analysis**","Study project value"),
                                ("**⚖️ Asset Allocation**","How you divide portfolio"),
                                ("**📉 Drawdown**","Peak-to-trough decline"),
                                ("**🔄 Rebalancing**","Restore target allocation")]:
                st.markdown(term); st.caption(defn)

# ─── Hall of Shame ────────────────────────────────────────────────────────────
st.markdown("---")
if st.session_state.hall_of_shame:
    st.markdown("### 💀 HALL OF SHAME 💀")
    st.markdown("<p style='text-align:center;color:#ff6666;'>Fallen Traders — Never Forget</p>", unsafe_allow_html=True)
    shame_rows = []
    for e in st.session_state.hall_of_shame[:20]:
        pnl_d = f"🟢 ${e['pnl']:+.2f}" if e['pnl'] > 0 else f"🔴 ${e['pnl']:+.2f}"
        shame_rows.append({
            "Team": "🦙" if e['model']=='llama' else "🥷",
            "Bot": e['name'],
            "Final": f"${e['final_value']:.2f}",
            "P&L": pnl_d,
            "Trades": e['trades'],
            "Win%": f"{e['win_rate']:.0f}%",
            "Lifespan": f"{e['lifespan']:.1f}h",
            "Replaced By": e['replaced_by'],
            "Trained By": e['trained_by'],
        })
    st.dataframe(shame_rows, use_container_width=True, hide_index=True, height=280)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
fee_pct = st.session_state.trading_fee * 100
st.markdown(f"""
<div style="text-align:center;color:#555;padding:0.8rem;font-size:0.88rem;">
    ⚙️ <strong>TraderDome: Meme Coins</strong> — Educational simulation, not financial advice<br>
    💰 Fee: {fee_pct:.2f}%/trade ({fee_pct*2:.2f}% round-trip) |
    💀 Elimination every {st.session_state.get('elimination_interval',10)}min |
    💵 ${st.session_state.starting_capital:.0f}/bot starting capital |
    🏦 House Fees: ${st.session_state.get('total_fees_collected',0):.2f}
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  AUTO-REFRESH  — st.rerun() is ALWAYS called so the loop never dies
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.running:
    if st.session_state.data_mode == 'realtime':
        last = st.session_state.last_realtime_fetch
        elapsed_rt = (datetime.now() - last).total_seconds() if last else 999
        if elapsed_rt >= 60:
            try:
                ok = trading_cycle()
                if ok:
                    st.session_state.last_realtime_fetch = datetime.now()
                else:
                    time.sleep(28)   # rate-limit back-off
            except Exception as _e:
                print(f"Realtime cycle error: {_e}")
            time.sleep(2)
        else:
            st.info(f"🌐 Real-time: next fetch in **{int(60-elapsed_rt)}s**")
            time.sleep(1)
        st.rerun()
    else:
        # Sleep scales with playback speed; changes take effect immediately
        sleep_secs = max(0.15, 0.6 - st.session_state.playback_speed * 0.004)
        try:
            trading_cycle()
        except Exception as _e:
            print(f"Trading cycle error: {_e}")
        time.sleep(sleep_secs)
        st.rerun()
