# -*- coding: utf-8 -*-
"""
ThePathLab Radar Builder (v3.0)
- 🏆 1부 리그: PLM100 (PathLab Moat 100 - 철옹성 독점 해자 100선)
- 🌱 2부 리그: PLV100 (PathLab Venture 100 - 텐배거 벤처 100선)
- 📈 11월 1일 (11월 2일 첫 거래일) 1,000 pt 베이스 지수 산출 및 S&P 500 비교
- ⏰ 매일 미국 장 마감 후 자동 갱신
"""

import sys
import os
import json
import datetime
import urllib.request
from concurrent.futures import ThreadPoolExecutor

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 유니버스 불러오기
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from universe_plm100 import PLM100_WATCHLIST
from universe_plv100 import PLV100_WATCHLIST

BASE_DATE = "2026-11-02"

def compute_rsi(closes, period=14):
    if len(closes) < period + 1:
        return 50.0
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100.0 - (100.0 / (1.0 + rs)), 1)

def fetch_ticker_data(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1mo"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            result = data['chart']['result'][0]
            meta = result['meta']
            price = meta.get('regularMarketPrice')
            high52 = meta.get('fiftyTwoWeekHigh')
            low52 = meta.get('fiftyTwoWeekLow')
            
            timestamps = result.get('timestamp', [])
            quotes = result.get('indicators', {}).get('quote', [{}])[0]
            closes = quotes.get('close', [])
            
            # 날짜별 종가
            date_closes = {}
            valid_closes = []
            for ts, c in zip(timestamps, closes):
                if c is not None:
                    dt = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    date_closes[dt] = c
                    valid_closes.append(c)
            
            # RSI
            rsi = compute_rsi(valid_closes) if valid_closes else 50.0
            
            # 52주 위치
            from_low_pct = round(((price - low52) / low52) * 100, 1) if low52 else 0.0
            from_high_pct = round(((price - high52) / high52) * 100, 1) if high52 else 0.0
            range_pct = round(((price - low52) / (high52 - low52)) * 100, 1) if (high52 and low52 and high52 != low52) else 50.0
            
            # 11월 2일 기준가
            # 만약 11월 2일 데이터가 휴장 등으로 없으면 가장 가까운 첫 영업일 종가
            base_price = date_closes.get(BASE_DATE)
            if not base_price and date_closes:
                sorted_dates = sorted(date_closes.keys())
                for sd in sorted_dates:
                    if sd >= BASE_DATE:
                        base_price = date_closes[sd]
                        break
                if not base_price:
                    base_price = date_closes[sorted_dates[0]]
            
            return {
                "status": "OK",
                "price": round(price, 2) if price else 0.0,
                "base_price": round(base_price, 2) if base_price else round(price, 2),
                "high52": round(high52, 2) if high52 else 0.0,
                "low52": round(low52, 2) if low52 else 0.0,
                "from_low_pct": from_low_pct,
                "from_high_pct": from_high_pct,
                "range_pct": range_pct,
                "rsi": rsi,
                "daily_history": date_closes
            }
    except Exception as e:
        print(f"[{ticker}] Fetch failed: {e}")
        return {"status": "FAIL", "price": 0.0, "rsi": 50.0, "daily_history": {}}

def process_universe(watchlist, max_workers=12):
    results = {}
    tickers = list(watchlist.keys())
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_ticker_data, t): t for t in tickers}
        for future in futures:
            t = futures[future]
            try:
                res = future.result()
                results[t] = res
            except Exception as e:
                results[t] = {"status": "FAIL", "price": 0.0, "rsi": 50.0, "daily_history": {}}
    return results

def main():
    print("🚀 ThePathLab Radar Builder (v3.0) Starting...")
    print(f"PLM100: {len(PLM100_WATCHLIST)} tickers | PLV100: {len(PLV100_WATCHLIST)} tickers")
    
    # 1. 시세 수집
    print("Fetching PLM100 (1부 리그)...")
    plm_data = process_universe(PLM100_WATCHLIST)
    
    print("Fetching PLV100 (2부 리그)...")
    plv_data = process_universe(PLV100_WATCHLIST)
    
    print("Fetching Benchmark SPY (S&P 500)...")
    spy_data = fetch_ticker_data("SPY")
    
    # 2. 거래일 리스트 추출 (11월 2일 이후)
    all_dates = set(spy_data.get("daily_history", {}).keys())
    for d in plm_data.values():
        all_dates.update(d.get("daily_history", {}).keys())
    for d in plv_data.values():
        all_dates.update(d.get("daily_history", {}).keys())
        
    trading_dates = sorted([d for d in all_dates if d >= BASE_DATE])
    print(f"Trading dates since {BASE_DATE}: {trading_dates}")
    
    # 3. 일별 지수 포인트(1,000pt 베이스) 계산
    history = []
    spy_base = spy_data.get("base_price", spy_data.get("price", 1.0))
    if not spy_base: spy_base = 1.0
    
    for dt in trading_dates:
        # PLM100 평균 수익률
        plm_ratios = []
        for t, d in plm_data.items():
            dh = d.get("daily_history", {})
            b_p = d.get("base_price", 0)
            p_t = dh.get(dt)
            if p_t and b_p and b_p > 0:
                plm_ratios.append(p_t / b_p)
        plm_idx = round(1000.0 * (sum(plm_ratios) / len(plm_ratios)), 2) if plm_ratios else 1000.0
        
        # PLV100 평균 수익률
        plv_ratios = []
        for t, d in plv_data.items():
            dh = d.get("daily_history", {})
            b_p = d.get("base_price", 0)
            p_t = dh.get(dt)
            if p_t and b_p and b_p > 0:
                plv_ratios.append(p_t / b_p)
        plv_idx = round(1000.0 * (sum(plv_ratios) / len(plv_ratios)), 2) if plv_ratios else 1000.0
        
        # SPY 지수
        spy_t = spy_data.get("daily_history", {}).get(dt, spy_base)
        spy_idx = round(1000.0 * (spy_t / spy_base), 2)
        
        history.append({
            "date": dt,
            "plm100": plm_idx,
            "plv100": plv_idx,
            "spy": spy_idx
        })
        
    latest_hist = history[-1] if history else {"plm100": 1000.0, "plv100": 1000.0, "spy": 1000.0}
    
    # 4. 종목별 카드 데이터 정제
    def build_items(watchlist, raw_data, league_type):
        items = []
        for t, meta in watchlist.items():
            d = raw_data.get(t, {})
            price = d.get("price", 0.0)
            base_p = d.get("base_price", price)
            ret_from_base = round(((price - base_p) / base_p) * 100, 2) if (base_p and base_p > 0) else 0.0
            
            items.append({
                "ticker": t,
                "name": meta.get("name", t),
                "country": meta.get("country", "US"),
                "sector": meta.get("sector", ""),
                "category": meta.get("category", league_type),
                "league": league_type,
                "price": price,
                "base_price": base_p,
                "high52": d.get("high52", 0.0),
                "low52": d.get("low52", 0.0),
                "return_pct": ret_from_base,
                "from_high_pct": d.get("from_high_pct", 0.0),
                "from_low_pct": d.get("from_low_pct", 0.0),
                "range_pct": d.get("range_pct", 50.0),
                "rsi": d.get("rsi", 50.0),
                "thesis": meta.get("thesis", ""),
                "if_best": meta.get("if_best", ""),
                "if_worst": meta.get("if_worst", ""),
                "kill_switch": meta.get("kill_switch", "")
            })
        return items

    plm_items = build_items(PLM100_WATCHLIST, plm_data, "PLM")
    plv_items = build_items(PLV100_WATCHLIST, plv_data, "PLV")
    
    # 정렬: 기본적으로 고점 대비 낙폭 순(기회 포착)
    plm_items.sort(key=lambda x: x["from_high_pct"])
    plv_items.sort(key=lambda x: x["from_high_pct"])
    
    # 5. 최종 데이터셋 생성
    now_str = datetime.datetime.now().strftime("%Y년 %m월 %d일 %H:%M")
    payload = {
        "updated": now_str,
        "base_date": BASE_DATE,
        "beta_status": {
            "is_beta": True,
            "period": "2026.11.01 ~ 2026.12.31",
            "official_launch": "2027.01.02",
            "notice": "현재 시스템은 2027년 1월 2일 공식 승강제 출범을 앞둔 Beta 시범 운용 모드입니다."
        },
        "indices": {
            "plm100": {
                "name": "PLM100 (1부 독점 해자)",
                "current": latest_hist["plm100"],
                "return_pct": round(((latest_hist["plm100"] - 1000.0) / 1000.0) * 100, 2),
                "base": 1000.0
            },
            "plv100": {
                "name": "PLV100 (2부 텐배거 벤처)",
                "current": latest_hist["plv100"],
                "return_pct": round(((latest_hist["plv100"] - 1000.0) / 1000.0) * 100, 2),
                "base": 1000.0
            },
            "spy": {
                "name": "S&P 500 (SPY 벤치마크)",
                "current": latest_hist["spy"],
                "return_pct": round(((latest_hist["spy"] - 1000.0) / 1000.0) * 100, 2),
                "base": 1000.0
            }
        },
        "history": history,
        "counts": {
            "plm100": len(plm_items),
            "plv100": len(plv_items)
        },
        "plm100_items": plm_items,
        "plv100_items": plv_items
    }
    
    output_path = os.path.join(CURRENT_DIR, "radar_data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        
    print(f"\n🎉 Successfully updated radar_data.json!")
    print(f"PLM100 Index: {latest_hist['plm100']} pt ({payload['indices']['plm100']['return_pct']}%)")
    print(f"PLV100 Index: {latest_hist['plv100']} pt ({payload['indices']['plv100']['return_pct']}%)")
    print(f"SPY Benchmark: {latest_hist['spy']} pt ({payload['indices']['spy']['return_pct']}%)")
    print(f"Items: PLM={len(plm_items)} | PLV={len(plv_items)}")

if __name__ == "__main__":
    main()
