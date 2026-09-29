import urllib.request
import json
import os
import datetime

# 13개 핵심 종목 및 시나리오 정의
WATCHLIST = {
    "PRVA": {
        "name": "프리비아 헬스 (Privia Health)",
        "sector": "🩺 가치기반 1차의료",
        "tag": "무차입 헬스케어",
        "thesis": "의사들을 네트워크로 묶어 의료비 절감분을 인센티브로 공유하는 가치기반 의료 플랫폼",
        "special_issue": "52주 최저가 바로 턱밑(+2.9%). 무차입 순현금 구조로 고령화 메디케어 시대 구조적 수혜주",
        "if_best": "메디케어 환자 유입 폭증 ➔ EPS 연 20% 고성장 ➔ 주가 $30+ 회복 (+50%)",
        "if_worst": "미 정부의 메디케어 어드밴티지 보조금 삭감으로 의사 인센티브 축소",
        "kill_switch": "분기 EBITDA 적자 전환 또는 파트너 의사 수 순감소 시"
    },
    "NKE": {
        "name": "나이키 (Nike)",
        "sector": "👟 스포츠 퍼포먼스",
        "tag": "10년 래 최저 P/E",
        "thesis": "알파플라이·베이퍼플라이 마라톤 기술 독점 + 32년 순혈 CEO 엘리엇 힐 복귀",
        "special_issue": "중국 경기 침체와 애국소비(궈차오) 악재가 주가에 극단적 선반영(-53% 폭락). 엘리엇 힐의 러닝 본질 복귀 가속",
        "if_best": "홀세일 유통망 복원 및 신규 러닝 라인업 호조 ➔ 주가 $55~$60대 회복 (+60%)",
        "if_worst": "중국 시장 매출 추가 역성장 및 안타/리닝에 시장 점유율 영구 상실",
        "kill_switch": "분기 매출총이익률(Gross Margin) 40% 붕괴 또는 배당 컷 시"
    },
    "CI": {
        "name": "시그나 (The Cigna Group)",
        "sector": "🏥 헬스케어 / PBM",
        "tag": "현금 요새",
        "thesis": "미국 3대 처방약 급여관리(PBM) 및 기업 건강보험 과점 사업자",
        "special_issue": "휴마나(HUM) 인수 무리수 철회 후 남는 현금 전액 자사주 소각 선언. P/E 10배 바닥권",
        "if_best": "AI 버블 발작 시 가치주 피난처 부각 ➔ P/E 15배 리레이팅 ($380+, +40%)",
        "if_worst": "미 의회의 초당적 PBM 마진 규제 입법 통과",
        "kill_switch": "PBM 수수료 모델을 금지하는 연방법 확정 시"
    },
    "DOX": {
        "name": "암독스 (Amdocs)",
        "sector": "📞 통신사 과금 독점",
        "tag": "Fwd P/E 7.1배",
        "thesis": "AT&T, 버라이즌, T-모바일 등 글로벌 통신사 빌링/과금 소프트웨어 전환 비용 극상 독점",
        "special_issue": "Fwd P/E 7.1배, P/FCF 9.6배의 경이로운 현금 창출력. 매년 공격적 자사주 매입",
        "if_best": "통신사 5G/클라우드 전환 수주 지속 ➔ 멀티플 정상화 ($80+, +40%)",
        "if_worst": "주요 통신사들의 자체 인하우스 빌링 시스템 전환 시도",
        "kill_switch": "핵심 고객사(AT&T 등)의 계약 해지 또는 매출 역성장 2분기 지속 시"
    },
    "PATH": {
        "name": "유아이패스 (UiPath)",
        "sector": "💻 RPA 사무자동화",
        "tag": "순현금 10억$",
        "thesis": "글로벌 1위 RPA 기업. 단순 매크로를 넘어 대기업용 에이전틱 자동화로 진화",
        "special_issue": "AI 대체 공포로 $12대 바닥 폭락. 하지만 부채 0원 + 순현금 10억 달러 보유로 망할 위험 0, M&A 피인수 1순위",
        "if_best": "에이전틱 AI 워크플로우 안착 ➔ 주가 100% 턴어라운드 ($25+)",
        "if_worst": "거대 LLM(오픈AI, MS)이 RPA 없이 화면을 완벽 조작하여 해자 소멸",
        "kill_switch": "분기 ARR(연간반복매출) 순감소 또는 순현금 적자 전환 시"
    },
    "ADM": {
        "name": "아처 대니얼스 미들랜드 (ADM)",
        "sector": "🌾 식량 주권 / 곡물 1위",
        "tag": "글로벌 ABCD 메이저",
        "thesis": "전 세계 곡물 운송선, 사일로 창고, 가공 플랜트를 독점한 100년 식량 안보 요새",
        "special_issue": "연초 영양 부문 회계 조사 노이즈로 주가 반토막 후 내부 감사 종결 및 펀더멘털 바닥 확인 중",
        "if_best": "기상이변 속 곡물 유통 마진 폭증 + 회계 노이즈 완전 해소 ➔ 주가 $85+ 회복",
        "if_worst": "미 법무부의 대규모 회계 분식 기소 및 천문학적 벌금",
        "kill_switch": "전사적 회계 부정 확정 또는 곡물 유통 시장 점유율 급락 시"
    },
    "CF": {
        "name": "CF 인더스트리즈 (CF Industries)",
        "sector": "⚡ 질소 비료 독점",
        "tag": "P/FCF 7~8배",
        "thesis": "미국 셰일가스로 질소 비료 생산, 비싼 가스를 쓰는 유럽/러시아 원가 압살",
        "special_issue": "P/FCF 7~8배의 미친 현금 창출력. 대규모 자사주 소각 지속 및 글로벌 식량 안보 필수재",
        "if_best": "유럽 천연가스 불안 + 비료 부족 ➔ 판가 급등 및 대규모 특별배당",
        "if_worst": "미국 Henry Hub 천연가스 가격의 구조적 급등으로 원가 마진 축소",
        "kill_switch": "미국 천연가스 가격이 $6/MMBtu 이상 6개월 지속 시"
    },
    "NTR": {
        "name": "뉴트리엔 (Nutrien)",
        "sector": "🌱 칼륨 비료 1위",
        "tag": "글로벌 필수 영양소",
        "thesis": "캐나다 기반 전 세계 1위 칼륨(Potash) 독점 공급자",
        "special_issue": "농산물 가격 약세로 52주 신저가 부근 바닥 다지기. 글로벌 식량 안보 필수 인프라",
        "if_best": "글로벌 곡물 파종 면적 확대 ➔ 칼륨 수요 폭발 및 주가 50%+ 반등",
        "if_worst": "러시아·벨라루스 칼륨의 글로벌 우회 덤핑 수출 지속",
        "kill_switch": "칼륨 톤당 가격이 생산 원가 이하로 급락 시"
    },
    "RIG": {
        "name": "트랜스오션 (Transocean)",
        "sector": "🌊 초심해 시추선 1위",
        "tag": "공급 절벽 르네상스",
        "thesis": "셰일 유전 고갈에 따른 브라질/가이아나 심해 시추 독점 공급자",
        "special_issue": "지난 10년간 신규 건조 전무로 물리적 시추선 공급 동결. 일일 용선료 $50만 돌파",
        "if_best": "유가 $80+ 속 초심해 프로젝트 폭증 ➔ 수주 백로그 폭발 ➔ 100%+ 랠리",
        "if_worst": "글로벌 경기 침체로 유가 $50 이하 급락 및 오일 메이저 시추 중단",
        "kill_switch": "WTI 유가 $55 이하 6개월 지속 시"
    },
    "VAL": {
        "name": "발라리스 (Valaris)",
        "sector": "🌊 해양 시추선 2위",
        "tag": "무부채 시추선사",
        "thesis": "파산 구조조정으로 부채를 100% 털어낸 깨끗한 대차대조표의 해양 시추 과점 기업",
        "special_issue": "수주 잔고 순차적 매출 전환으로 FCF 급증 국면. 강력한 자사주 매입 집행",
        "if_best": "해양 플로터 가동률 95% 돌파 ➔ 주가 전고점 돌파 ($120+, +50%)",
        "if_worst": "오프쇼어 프로젝트 지연 및 유가 하락",
        "kill_switch": "수주 잔고(Backlog) 순감소 2분기 연속 발생 시"
    },
    "OII": {
        "name": "오셔니어링 (Oceaneering)",
        "sector": "🤖 심해 로봇(ROV) 독점",
        "tag": "해저의 곡괭이",
        "thesis": "수심 3,000m 심해 원격 로봇팔(ROV) 점유율 1위 독점사",
        "special_issue": "해저 광케이블 매설, 심해 유전 보수, 미 해군 무인 잠수정(UUV) 수주 3중 수혜",
        "if_best": "해저 데이터센터 및 해저 통신망 인프라 투자 폭증 ➔ 영업이익률 20% 돌파",
        "if_worst": "심해 설비투자 동결",
        "kill_switch": "ROV 가동률 50% 붕괴 시"
    },
    "DE": {
        "name": "디어 앤 컴퍼니 (John Deere)",
        "sector": "🚜 스마트 농기계 1위",
        "tag": "농업계의 테슬라",
        "thesis": "전 세계 1위 트랙터 독점 및 AI 자율주행 정밀농업 선도자",
        "special_issue": "고금리로 농부들의 트랙터 교체 주기 일시 둔화 ➔ 사이클 바닥 다지는 중",
        "if_best": "금리 인하 + 농산물 가격 반등 ➔ 신규 자율주행 트랙터 업그레이드 사이클 개막",
        "if_worst": "고금리 장기화로 농가 부채 위기",
        "kill_switch": "정밀농업 구독 매출 역성장 시"
    },
    "ETN": {
        "name": "이튼 (Eaton)",
        "sector": "⚡ 변압기 / 배전 독점",
        "tag": "20% 공격수 코어",
        "thesis": "AI 데이터센터 + 미국 노후 전력망 50년 교체 주기의 핵심 심장",
        "special_issue": "변압기 납기가 2~3년 밀려 있을 정도로 초호황. AI 버블 논란으로 조정 시마다 분할 매수 적합",
        "if_best": "전력망 슈퍼사이클 10년 지속 ➔ 백로그 매출 전환으로 EPS 연 20% 성장",
        "if_worst": "미국 제조업 리쇼어링 전면 중단 및 빅테크 CAPEX 축소",
        "kill_switch": "전력 부문 수주-출하 비율(Book-to-Bill) 1.0 미만 하락 시"
    }
}

def fetch_stock_data(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1y"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            meta = data['chart']['result'][0]['meta']
            price = meta.get('regularMarketPrice')
            high52 = meta.get('fiftyTwoWeekHigh')
            low52 = meta.get('fiftyTwoWeekLow')
            
            from_low_pct = ((price - low52) / low52) * 100 if low52 else 0
            from_high_pct = ((price - high52) / high52) * 100 if high52 else 0
            
            # 52주 레인지 백분율 (0% = 최저가, 100% = 최고가)
            range_pct = ((price - low52) / (high52 - low52)) * 100 if (high52 and low52 and high52 != low52) else 50
            
            return {
                "price": price,
                "high52": high52,
                "low52": low52,
                "from_low_pct": from_low_pct,
                "from_high_pct": from_high_pct,
                "range_pct": range_pct,
                "status": "OK"
            }
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)}

def build_radar():
    print("Collecting US stock market radar data...")
    stock_items = []
    
    for ticker, meta in WATCHLIST.items():
        data = fetch_stock_data(ticker)
        stock_items.append({
            "ticker": ticker,
            "meta": meta,
            "data": data
        })

    # 정렬: 52주 최저가에 가장 가까운 순(from_low_pct 오름차순)으로 자동 정렬!
    # 즉, 지금 당장 바닥 사정권인 종목이 무조건 최상단에 노출됨!
    stock_items.sort(key=lambda x: x["data"].get("from_low_pct", 999) if x["data"].get("status") == "OK" else 999)

    now_dt = datetime.datetime.now()
    updated_str = now_dt.strftime("%Y년 %m월 %d일 %H:%M")
    date_iso = now_dt.strftime("%Y-%m-%d")

    # JSON 저장 (API 역할)
    out_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(out_dir, "radar_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"updated": updated_str, "items": stock_items}, f, ensure_ascii=False, indent=2)

    # HTML 템플릿 생성 (ThePathLab Dark Tech 테마 & 완벽 반응형)
    cards_html = ""
    bottom_count = 0

    for item in stock_items:
        t = item["ticker"]
        m = item["meta"]
        d = item["data"]
        
        if d.get("status") == "OK":
            p = f"${d['price']:.2f}"
            low_str = f"${d['low52']:.2f}"
            high_str = f"${d['high52']:.2f}"
            fl_pct = d["from_low_pct"]
            fh_pct = d["from_high_pct"]
            rp = max(0, min(100, d["range_pct"]))
            
            # 상태 배지 판단
            if fl_pct <= 15.0 or fh_pct <= -35.0:
                status_badge = '<span class="status-badge alert-fire"><i class="bi bi-fire"></i> 바닥 사정권</span>'
                card_class = "radar-card alert-border"
                bottom_count += 1
            elif fl_pct <= 30.0:
                status_badge = '<span class="status-badge alert-warn"><i class="bi bi-eye"></i> 분할 관심</span>'
                card_class = "radar-card warn-border"
            else:
                status_badge = '<span class="status-badge alert-hold"><i class="bi bi-check2-circle"></i> 관찰 유지</span>'
                card_class = "radar-card normal-border"
                
            fl_color = "#10b981" if fl_pct <= 15 else "#38bdf8"
            fh_color = "#f43f5e" if fh_pct <= -30 else "#94a3b8"

            cards_html += f"""
            <div class="{card_class}" id="card-{t}">
                <div class="card-header">
                    <div class="card-title-wrap">
                        <div class="card-ticker-row">
                            <span class="ticker-badge">{t}</span>
                            <span class="tag-badge">{m['tag']}</span>
                            {status_badge}
                        </div>
                        <h3 class="card-name">{m['name']}</h3>
                        <span class="card-sector">{m['sector']}</span>
                    </div>
                    <div class="card-price-wrap">
                        <div class="current-price">{p}</div>
                        <div class="price-fl" style="color: {fl_color};">
                            <i class="bi bi-arrow-up-right"></i> 저점대비 +{fl_pct:.1f}%
                        </div>
                    </div>
                </div>

                <div class="range-box">
                    <div class="range-labels">
                        <span>52주 최저 {low_str}</span>
                        <span style="color: {fh_color};">고점대비 {fh_pct:+.1f}%</span>
                        <span>52주 최고 {high_str}</span>
                    </div>
                    <div class="range-track">
                        <div class="range-fill" style="width: {rp:.1f}%;"></div>
                        <div class="range-pin" style="left: {rp:.1f}%;"></div>
                    </div>
                </div>

                <div class="issue-box">
                    <div class="issue-title"><i class="bi bi-lightning-charge-fill text-gold"></i> 🚨 특수 상황 & 핵심 촉매</div>
                    <div class="issue-desc">{m['special_issue']}</div>
                </div>

                <div class="scenario-accordion">
                    <details>
                        <summary><i class="bi bi-diagram-3"></i> IF 시나리오 & 손절선 펼치기</summary>
                        <div class="scenario-details">
                            <div class="sc-item sc-best">
                                <strong>🌟 Best:</strong> {m['if_best']}
                            </div>
                            <div class="sc-item sc-worst">
                                <strong>💥 Worst:</strong> {m['if_worst']}
                            </div>
                            <div class="sc-item sc-kill">
                                <strong>🚨 킬스위치 (손절):</strong> {m['kill_switch']}
                            </div>
                        </div>
                    </details>
                </div>

                <div class="card-footer-actions">
                    <span class="thesis-text">{m['thesis']}</span>
                    <a href="https://finance.yahoo.com/quote/{t}" target="_blank" rel="noopener" class="chart-btn">
                        차트 <i class="bi bi-box-arrow-up-right"></i>
                    </a>
                </div>
            </div>
            """

    html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-K3PFHN6VW7"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-K3PFHN6VW7');
    </script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>미국 1억 레이더 | 52주 신저가 & 특수 상황 모니터링 - ThePathLab</title>
    <meta name="description" content="ThePathLab US 100M Radar: 식량 안보, 심해 시추, 무차입 헬스케어, 전력망 교체 핵심 13개 독점 기업의 52주 최저가 및 특수 이슈 실시간 아침 브리핑">
    <link rel="canonical" href="https://thapathlab.com/radar/">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

    <style>
        :root {{
            --bg-body: #070a12;
            --bg-card: rgba(15, 23, 42, 0.75);
            --bg-card-hover: rgba(30, 41, 59, 0.9);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(0, 242, 254, 0.4);
            --cyan: #00f2fe;
            --blue: #38bdf8;
            --gold: #ffb800;
            --red: #f43f5e;
            --green: #10b981;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --text-dim: #64748b;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-body);
            color: var(--text-main);
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            padding-bottom: 5rem;
        }}

        /* Header Navigation */
        .radar-nav {{
            position: sticky;
            top: 0;
            z-index: 1000;
            background: rgba(7, 10, 18, 0.92);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-subtle);
            padding: 0.75rem 1.25rem;
        }}
        .nav-inner {{
            max-width: 1100px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .brand-link {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #ffffff;
            text-decoration: none;
            font-weight: 800;
            font-size: 1.1rem;
        }}
        .brand-link i {{ color: var(--cyan); }}
        .nav-back {{
            color: var(--text-sub);
            text-decoration: none;
            font-size: 0.88rem;
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 5px 10px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
            transition: all 0.2s;
        }}
        .nav-back:hover {{
            color: #fff;
            background: rgba(0, 242, 254, 0.15);
        }}

        /* Hero Banner */
        .hero-wrap {{
            max-width: 1100px;
            margin: 2rem auto 1.5rem;
            padding: 0 1.25rem;
        }}
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--cyan);
            background: rgba(0, 242, 254, 0.1);
            border: 1px solid rgba(0, 242, 254, 0.25);
            padding: 4px 10px;
            border-radius: 20px;
            margin-bottom: 0.75rem;
        }}
        .hero-title {{
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #ffffff 40%, var(--cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-desc {{
            color: var(--text-sub);
            font-size: 0.95rem;
            max-width: 780px;
            word-break: keep-all;
        }}
        .meta-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            margin-top: 1rem;
            font-size: 0.85rem;
            color: var(--text-dim);
        }}
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .meta-item strong {{ color: var(--gold); }}

        /* Filter Chips */
        .filter-bar {{
            max-width: 1100px;
            margin: 0 auto 1.5rem;
            padding: 0 1.25rem;
            display: flex;
            gap: 8px;
            overflow-x: auto;
            scrollbar-width: none;
        }}
        .filter-btn {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-subtle);
            color: var(--text-sub);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.84rem;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }}
        .filter-btn.active {{
            background: rgba(0, 242, 254, 0.15);
            border-color: var(--cyan);
            color: var(--cyan);
            font-weight: 700;
        }}

        /* Radar Card Grid */
        .radar-grid {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 1.25rem;
            display: grid;
            grid-template-columns: 1fr;
            gap: 1.25rem;
        }}

        .radar-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 1.35rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(8px);
        }}
        .radar-card:hover {{
            background: var(--bg-card-hover);
            transform: translateY(-2px);
            border-color: var(--border-glow);
        }}
        .radar-card.alert-border {{
            border-left: 4px solid var(--red);
            background: linear-gradient(135deg, rgba(244, 63, 94, 0.08) 0%, rgba(15, 23, 42, 0.8) 40%);
        }}
        .radar-card.warn-border {{
            border-left: 4px solid var(--gold);
        }}
        .radar-card.normal-border {{
            border-left: 4px solid var(--blue);
        }}

        /* Card Header */
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        .card-ticker-row {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 6px;
        }}
        .ticker-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.15rem;
            font-weight: 800;
            color: #ffffff;
            background: rgba(255, 255, 255, 0.1);
            padding: 2px 8px;
            border-radius: 6px;
        }}
        .tag-badge {{
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--cyan);
            background: rgba(0, 242, 254, 0.1);
            padding: 2px 7px;
            border-radius: 4px;
        }}
        .status-badge {{
            font-size: 0.75rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}
        .alert-fire {{
            background: rgba(244, 63, 94, 0.2);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.4);
        }}
        .alert-warn {{
            background: rgba(255, 184, 0, 0.2);
            color: #fde047;
            border: 1px solid rgba(255, 184, 0, 0.4);
        }}
        .alert-hold {{
            background: rgba(56, 189, 248, 0.15);
            color: #7dd3fc;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }}

        .card-name {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #f1f5f9;
            margin-bottom: 2px;
        }}
        .card-sector {{
            font-size: 0.8rem;
            color: var(--text-dim);
        }}

        .card-price-wrap {{
            text-align: right;
            flex-shrink: 0;
        }}
        .current-price {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.45rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.5px;
        }}
        .price-fl {{
            font-size: 0.8rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* 52w Range Box */
        .range-box {{
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 10px 12px;
            margin-bottom: 1rem;
        }}
        .range-labels {{
            display: flex;
            justify-content: space-between;
            font-size: 0.74rem;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-dim);
            margin-bottom: 6px;
        }}
        .range-track {{
            position: relative;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: visible;
        }}
        .range-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--green) 0%, var(--cyan) 50%, var(--gold) 100%);
            border-radius: 4px;
        }}
        .range-pin {{
            position: absolute;
            top: -4px;
            width: 14px;
            height: 14px;
            background: #ffffff;
            border: 2.5px solid var(--cyan);
            border-radius: 50%;
            transform: translateX(-50%);
            box-shadow: 0 0 8px rgba(0, 242, 254, 0.8);
        }}

        /* Issue Box */
        .issue-box {{
            background: rgba(255, 184, 0, 0.06);
            border: 1px solid rgba(255, 184, 0, 0.18);
            border-radius: 10px;
            padding: 10px 12px;
            margin-bottom: 0.85rem;
        }}
        .issue-title {{
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--gold);
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .text-gold {{ color: var(--gold); }}
        .issue-desc {{
            font-size: 0.86rem;
            color: #cbd5e1;
            line-height: 1.45;
            word-break: keep-all;
        }}

        /* Scenario Accordion */
        .scenario-accordion details {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 8px 12px;
            font-size: 0.82rem;
            margin-bottom: 0.85rem;
        }}
        .scenario-accordion summary {{
            cursor: pointer;
            font-weight: 600;
            color: var(--blue);
            outline: none;
            user-select: none;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .scenario-details {{
            margin-top: 8px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            padding-top: 8px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            color: var(--text-sub);
        }}
        .sc-best strong {{ color: var(--green); }}
        .sc-worst strong {{ color: var(--gold); }}
        .sc-kill strong {{ color: var(--red); }}

        /* Card Footer */
        .card-footer-actions {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .thesis-text {{
            font-size: 0.78rem;
            color: var(--text-dim);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 75%;
        }}
        .chart-btn {{
            font-size: 0.8rem;
            font-weight: 600;
            color: #ffffff;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--border-subtle);
            padding: 4px 10px;
            border-radius: 6px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: all 0.15s;
            flex-shrink: 0;
        }}
        .chart-btn:hover {{
            background: var(--cyan);
            color: #000;
            border-color: var(--cyan);
        }}

        @media (max-width: 640px) {{
            .hero-title {{ font-size: 1.5rem; }}
            .card-header {{ flex-direction: column; gap: 8px; }}
            .card-price-wrap {{ text-align: left; }}
            .thesis-text {{ display: none; }}
        }}
    </style>
</head>
<body>

    <!-- Unified Navigation Bar -->
    <nav class="radar-nav">
        <div class="nav-inner">
            <a href="/" class="brand-link">
                <i class="bi bi-shield-check"></i> ThePathLab
            </a>
            <a href="/" class="nav-back">
                <i class="bi bi-arrow-left"></i> 포털 메인으로
            </a>
        </div>
    </nav>

    <!-- Hero Header -->
    <header class="hero-wrap">
        <div class="hero-badge">
            <i class="bi bi-radar"></i> US 100M Cashflow Radar
        </div>
        <h1 class="hero-title">미국 1억 파이프라인 레이더</h1>
        <p class="hero-desc">
            식량 안보(곡물/비료), 심해 자원, 무차입 헬스케어, 전력망 물리적 인프라 등 
            <strong>"망할 수 없는 미국의 실물 독점 요새"</strong> 13개 종목의 52주 최저가 근접도 및 특수 상황(Special Situation) 실시간 감시 대시보드입니다.
        </p>
        <div class="meta-bar">
            <div class="meta-item">
                <i class="bi bi-clock-history"></i> 갱신 기준: <strong>{updated_str}</strong>
            </div>
            <div class="meta-item">
                <i class="bi bi-fire text-gold"></i> 현재 바닥 사정권: <strong>{bottom_count}개 종목</strong>
            </div>
            <div class="meta-item">
                <i class="bi bi-sort-down text-gold"></i> 정렬: <strong>52주 최저가 근접순 (오름차순)</strong>
            </div>
        </div>
    </header>

    <!-- Category Filters -->
    <div class="filter-bar">
        <button class="filter-btn active" onclick="filterCategory('all')">전체보기 (13)</button>
        <button class="filter-btn" onclick="filterCategory('alert')">🔥 바닥 사정권</button>
        <button class="filter-btn" onclick="filterCategory('health')">🏥 헬스케어/RPA</button>
        <button class="filter-btn" onclick="filterCategory('food')">🌾 식량/비료</button>
        <button class="filter-btn" onclick="filterCategory('ocean')">🌊 심해 에너지</button>
        <button class="filter-btn" onclick="filterCategory('power')">⚡ 전력 인프라</button>
    </div>

    <!-- Stock Cards Grid -->
    <main class="radar-grid" id="stockGrid">
        {cards_html}
    </main>

    <script>
        function filterCategory(cat) {{
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            const cards = document.querySelectorAll('.radar-card');
            cards.forEach(card => {{
                if (cat === 'all') {{
                    card.style.display = 'block';
                }} else if (cat === 'alert') {{
                    card.style.display = card.classList.contains('alert-border') ? 'block' : 'none';
                }} else if (cat === 'health') {{
                    const id = card.id;
                    card.style.display = (id === 'card-PRVA' || id === 'card-CI' || id === 'card-DOX' || id === 'card-PATH') ? 'block' : 'none';
                }} else if (cat === 'food') {{
                    const id = card.id;
                    card.style.display = (id === 'card-ADM' || id === 'card-CF' || id === 'card-NTR' || id === 'card-DE') ? 'block' : 'none';
                }} else if (cat === 'ocean') {{
                    const id = card.id;
                    card.style.display = (id === 'card-RIG' || id === 'card-VAL' || id === 'card-OII') ? 'block' : 'none';
                }} else if (cat === 'power') {{
                    const id = card.id;
                    card.style.display = (id === 'card-ETN') ? 'block' : 'none';
                }}
            }});
        }}
    </script>
</body>
</html>
    """

    html_path = os.path.join(out_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"US Radar web dashboard successfully built at: {html_path}")

if __name__ == "__main__":
    build_radar()
