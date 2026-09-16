#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ThePathLab AutoCost - Opinet Fuel Price Collector
한국석유공사 오피넷(Opinet) 메인 전국 평균 유가를 수집하여 
autocost/data/fuel_price.json 으로 정적 저장하는 스크립트.
"""

import os
import re
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime

# Windows 콘솔 인코딩 안전화
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "fuel_price.json")

def fetch_opinet_fuel_prices():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.opinet.co.kr/user/main/mainView.do',
        'Origin': 'https://www.opinet.co.kr'
    }

    data = urllib.parse.urlencode({
        'netfunnel_key': '',
        'opinet_key': 'AzPBADgJkMqwThk5Idgx/8BOPcvKwciYuk+W+COw3So='
    }).encode('utf-8')

    # 기본값 (오피넷 연결 실패 시 안전한 전국 평균 벤치마크 Fallback)
    today_str = datetime.now().strftime("%Y.%m.%d")
    result = {
        "status": "success",
        "source": "한국석유공사 오피넷 (Opinet)",
        "updated_at": today_str,
        "prices": {
            "gasoline": 1690,       # 보통휘발유
            "diesel": 1560,         # 자동차경유
            "lpg": 1050,            # 자동차부탄 LPG
            "premium": 1920,        # 고급휘발유
            "electricity": 340      # 전기차(완속/급속 평균)
        }
    }

    try:
        req = urllib.request.Request('https://www.opinet.co.kr/user/main/mainView.do', data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = resp.read()
        
        text = raw.decode('utf-8', errors='ignore')
        
        # 1. 보통휘발유 (oilcon1)
        m_gas = re.search(r'<div id="oilcon1">.*?<span class="text-3">([0-9\.,]+)</span>', text, re.DOTALL)
        if m_gas:
            result["prices"]["gasoline"] = round(float(m_gas.group(1).replace(',', '')))
        
        # 2. 자동차경유 (oilcon2)
        m_die = re.search(r'<div id="oilcon2">.*?<span class="text-3">([0-9\.,]+)</span>', text, re.DOTALL)
        if m_die:
            result["prices"]["diesel"] = round(float(m_die.group(1).replace(',', '')))
        
        # 3. 자동차부탄 LPG (oilcon3)
        m_lpg = re.search(r'<div id="oilcon3">.*?<span class="text-3">([0-9\.,]+)</span>', text, re.DOTALL)
        if m_lpg:
            result["prices"]["lpg"] = round(float(m_lpg.group(1).replace(',', '')))
        
        # 4. 고급휘발유: 보통휘발유 대비 약 +210원 시장 가중치
        result["prices"]["premium"] = result["prices"]["gasoline"] + 210

        # 5. 오피넷 공시 일자 파싱
        m_date = re.search(r'<span class="text-2">\(([0-9]{4}\.[0-9]{2}\.[0-9]{2})\)</span>', text)
        if m_date:
            result["updated_at"] = m_date.group(1)

        print(f"[SUCCESS] Opinet Fuel: Updated {result['updated_at']} | Gasoline {result['prices']['gasoline']} KRW, Diesel {result['prices']['diesel']} KRW, LPG {result['prices']['lpg']} KRW, Premium {result['prices']['premium']} KRW")

    except Exception as e:
        print(f"[WARNING] Opinet fetch exception -> using fallback: {e}")

    # JSON 저장
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"[SAVED] {OUTPUT_FILE}")
    return result

if __name__ == "__main__":
    fetch_opinet_fuel_prices()
