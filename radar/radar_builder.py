import urllib.request
import json
import os
import datetime

# 🎯 종목 레이더 감시 풀 (전 종목 EPS > 0 흑자 검증 및 물리적 해자 보유)
WATCHLIST = {
    # [식량 / 농업 / 비료]
    "ADM": {
        "name": "아처 대니얼스 미들랜드",
        "sector": "🌾 식량 / 곡물 1위",
        "tag": "곡물 메이저",
        "category": "food",
        "thesis": "전 세계 곡물 운송선, 사일로 창고, 가공 플랜트 독점",
        "special_issue": "영양 부문 내부 회계 조사 노이즈로 주가 급락 후 펀더멘털 바닥 확인 중",
        "if_best": "기상이변 속 곡물 유통 마진 폭증 + 회계 노이즈 해소 ➔ 주가 $85+ 회복",
        "if_worst": "미 법무부의 대규모 회계 분식 기소 및 과징금",
        "kill_switch": "전사적 회계 부정 확정 시"
    },
    "BG": {
        "name": "번지 글로벌 (Bunge)",
        "sector": "🌾 식량 / 대두 가공 1위",
        "tag": "저P/E 9배",
        "category": "food",
        "thesis": "Viterra 합병으로 세계 최대 곡물/대두 가공 거인으로 등극",
        "special_issue": "곡물 가격 안정화 국면에서 Fwd P/E 8~9배 수준의 단단한 안전마진",
        "if_best": "Viterra 합병 시너지로 연 FCF 20억 달러+ 창출 ➔ 밸류 리레이팅",
        "if_worst": "합병 승인 각국 규제당국 불허",
        "kill_switch": "핵심국 독점 규제로 합병 최종 무산 시"
    },
    "CF": {
        "name": "CF 인더스트리즈",
        "sector": "⚡ 질소 비료 독점",
        "tag": "P/FCF 7배",
        "category": "food",
        "thesis": "미국 저렴한 셰일가스로 질소 비료 생산, 유럽/러시아 원가 압살",
        "special_issue": "P/FCF 7~8배의 강력한 현금 창출력. 대규모 자사주 소각 지속",
        "if_best": "유럽 천연가스 불안 + 비료 부족 ➔ 판가 급등 및 대규모 특별배당",
        "if_worst": "미국 천연가스 가격 급등으로 마진 축소",
        "kill_switch": "미국 헨리허브 가스 가격 $6+ 지속 시"
    },
    "NTR": {
        "name": "뉴트리엔 (Nutrien)",
        "sector": "🌱 칼륨 비료 1위",
        "tag": "필수 영양소",
        "category": "food",
        "thesis": "캐나다 기반 전 세계 1위 칼륨(Potash) 독점 공급자",
        "special_issue": "농산물 가격 약세로 52주 신저가 부근 바닥 다지기",
        "if_best": "글로벌 곡물 파종 확대 ➔ 칼륨 수요 폭발 및 주가 40%+ 반등",
        "if_worst": "러시아·벨라루스 칼륨 덤핑 지속",
        "kill_switch": "칼륨 판가가 생산 원가 이하로 급락 시"
    },
    "DE": {
        "name": "디어 앤 컴퍼니",
        "sector": "🚜 스마트 농기계 1위",
        "tag": "정밀 농업",
        "category": "food",
        "thesis": "전 세계 1위 트랙터 독점 및 AI 자율주행 정밀농업 선도자",
        "special_issue": "고금리로 농부들의 트랙터 교체 주기 일시 둔화 ➔ 사이클 바닥권",
        "if_best": "금리 인하 + 농산물 가격 반등 ➔ 신규 자율주행 트랙터 업그레이드 사이클",
        "if_worst": "고금리 장기화로 농가 부채 위기",
        "kill_switch": "정밀농업 구독 매출 역성장 시"
    },

    # [폐기물 / 철도 / 실물 인프라]
    "WM": {
        "name": "웨이스트 매니지먼트",
        "sector": "🗑️ 매립지 토지 독점",
        "tag": "북미 1위",
        "category": "infra",
        "thesis": "신규 인허가 불가한 북미 최대 매립지 영지 독점 + 매립가스 발전",
        "special_issue": "쓰레기 반입 수수료 인상으로 인플레이션 자동 전가. 안정적 FCF",
        "if_best": "매립가스(RNG) 전력 판매 고성장 ➔ 배당 및 자사주 확대",
        "if_worst": "환경 규제 강화로 매립지 사후 관리 비용 급증",
        "kill_switch": "영업현금흐름(OCF) 마진율 5%p 이상 하락 시"
    },
    "RSG": {
        "name": "리퍼블릭 서비스",
        "sector": "🗑️ 폐기물 과점 2위",
        "tag": "물가연동 가격력",
        "category": "infra",
        "thesis": "북미 2위 폐기물 처리 과점. 장기 계약 기반 안정적 이익",
        "special_issue": "지자체 장기 수거 계약으로 경기 침체 무풍지대",
        "if_best": "자원 재활용 및 환경 인프라 인수로 연 10%+ EPS 성장",
        "if_worst": "유가 폭등으로 수거 트럭 유류비 급증",
        "kill_switch": "자유현금흐름 적자 전환 시"
    },
    "CLH": {
        "name": "클린 하버즈",
        "sector": "☣️ 특수 유해폐기물 1위",
        "tag": "초고마진 소각",
        "category": "infra",
        "thesis": "반도체·화학·정유 공장 유해 폐기물 소각 및 정화 인프라 독점",
        "special_issue": "미국 제조업 리쇼어링으로 산업 폐기물 처리 수요 증가",
        "if_best": "미국 내 반도체/배터리 팹 가동 ➔ 고마진 특수 처리 폭증",
        "if_worst": "미국 제조업 리쇼어링 지연",
        "kill_switch": "산업 서비스 부문 마진 급락 시"
    },
    "UNP": {
        "name": "유니언 퍼시픽",
        "sector": "🚂 미국 서부 철도 독점",
        "tag": "대륙의 혈관",
        "category": "infra",
        "thesis": "트럭 대비 운송비 1/4. 미국 서부·중부 물류 인프라 독점",
        "special_issue": "곡물, 화학물질, 공산품 컨테이너 운송의 영구적 해자",
        "if_best": "니어쇼어링(멕시코 수입) 물동량 급증 ➔ 배당 증액 랠리",
        "if_worst": "철도 노조 파업 및 경기 침체 물동량 감소",
        "kill_switch": "영업비율(OR) 65% 이상으로 악화 지속 시"
    },
    "CSX": {
        "name": "CSX 코퍼레이션",
        "sector": "🚂 미국 동부 철도 독점",
        "tag": "원정수송 해자",
        "category": "infra",
        "thesis": "뉴욕 대도시 쓰레기 원정 수송(Trash Train) 및 동부 공업지대 철도 독점",
        "special_issue": "대체 불가한 동부 철로망 기반 높은 영업이익률",
        "if_best": "동부 전력망 석탄/가스 발전 원자재 수송 증가",
        "if_worst": "동부 항만 물동량 급감",
        "kill_switch": "분기 순이익 적자 전환 시"
    },
    "NUE": {
        "name": "뉴코어 (Nucor)",
        "sector": "🔩 전기로 철강 1위",
        "tag": "50년 배당귀족",
        "category": "infra",
        "thesis": "미국 최대 전기로 고철 재활용 철강사. 저렴한 전기 원가 우위",
        "special_issue": "50년 연속 배당 증액. 무차입급 건전한 대차대조표",
        "if_best": "미국 인프라 재건법(IIJA) 착공 본격화 ➔ 봉형강/후판 수요 폭발",
        "if_worst": "글로벌 철강 수요 침체 및 판가 급락",
        "kill_switch": "가동률 60% 붕괴 시"
    },

    # [원자력 / 전력망 / 에너지]
    "CCJ": {
        "name": "카메코 (Cameco)",
        "sector": "☢️ 우라늄 채굴 1위",
        "tag": "원전 연료 독점",
        "category": "power",
        "thesis": "서방 1위 고품위 우라늄 광산 및 웨스팅하우스 지분 보유",
        "special_issue": "원전 르네상스와 빅테크 AI 데이터센터 전력 계약 수혜",
        "if_best": "우라늄 장기 계약가 파운드당 $100+ 안착 ➔ 마진 폭발",
        "if_worst": "원전 중대 사고 발생으로 글로벌 원전 정책 후퇴",
        "kill_switch": "우라늄 스팟 가격 $40 이하 급락 시"
    },
    "BWXT": {
        "name": "BWX 테크놀로지스",
        "sector": "☢️ 해군 원자로 / SMR",
        "tag": "국방 원자력",
        "category": "power",
        "thesis": "미 해군 핵잠수함/항공모함 원자로 독점 + 상용 SMR 부품 독점",
        "special_issue": "미 해군 버지니아/컬럼비아급 잠수함 건조 증가 및 SMR 상용화",
        "if_best": "미 국방부 원자력 예산 증액 + 소형 SMR 수주 가시화",
        "if_worst": "미 해군 잠수함 건조 지연",
        "kill_switch": "정부 국방 계약 취소 시"
    },
    "ETN": {
        "name": "이튼 (Eaton)",
        "sector": "⚡ 변압기 / 배전 1위",
        "tag": "전력망 심장",
        "category": "power",
        "thesis": "미국 노후 전력망 50년 교체 주기 + AI 데이터센터 전력 장비 독점",
        "special_issue": "변압기 수주 잔고 2~3년 누적. 조정 시 분할 매수 적합",
        "if_best": "전력망 슈퍼사이클 10년 지속 ➔ EPS 연 20% 성장",
        "if_worst": "빅테크 데이터센터 투자 축소",
        "kill_switch": "수주-출하 비율(Book-to-Bill) 1.0 미만 하락 시"
    },
    "PWR": {
        "name": "콴타 서비시즈",
        "sector": "⚡ 송전탑 / 그리드 시공",
        "tag": "인프라 시공 1위",
        "category": "power",
        "thesis": "미국 1위 전력망·송전탑 전문 엔지니어링 및 시공 인력 독점",
        "special_issue": "신재생 전력망 연계 및 초고압 송전탑 시공 수요 폭발",
        "if_best": "미 연방정부 송전망 인허가 가속 ➔ 대형 프로젝트 수주 폭발",
        "if_worst": "주정부 간 송전선 통과 인허가 갈등 장기화",
        "kill_switch": "백로그(수주잔고) 순감소 시"
    },

    # [자원 광산 / 심해 에너지]
    "BHP": {
        "name": "BHP 그룹",
        "sector": "⛏️ 글로벌 광산 1위",
        "tag": "남반구 자원요새",
        "category": "ocean",
        "thesis": "호주 본토 중심 철광석, 구리, 칼륨 생산 세계 1위 광산 거인",
        "special_issue": "배당수익률 5%+의 강력한 현금 흐름. 신냉전 안전 자원 기지",
        "if_best": "구리 수요 폭증 + 얀센 칼륨 광산 상업 가동 ➔ 이익 점프",
        "if_worst": "중국 철강 소비 침체로 철광석 가격 급락",
        "kill_switch": "배당 컷 또는 구리/철광석 동반 폭락 시"
    },
    "FCX": {
        "name": "프리포트 맥모란",
        "sector": "🥉 상장 구리 1위",
        "tag": "AI 전력 구리",
        "category": "ocean",
        "thesis": "전력망, AI 데이터센터, 전기차에 필수적인 구리 광산 1위",
        "special_issue": "구리 공급 부족 속 인도네시아 그라스버그 광산 마진 견조",
        "if_best": "구리 파운드당 $5+ 돌파 ➔ 연간 잉여현금흐름 폭발",
        "if_worst": "인도네시아 정부 수출 규제 갈등",
        "kill_switch": "구리 가격 $3 이하 하락 시"
    },
    "RIG": {
        "name": "트랜스오션",
        "sector": "🌊 초심해 시추선 1위",
        "tag": "공급절벽 수혜",
        "category": "ocean",
        "thesis": "지상 셰일 고갈에 따른 가이아나/브라질 심해 시추 독점 공급자",
        "special_issue": "시추선 공급 절벽으로 일일 용선료 $50만 돌파. 주가 바닥권",
        "if_best": "유가 $80+ 유지 ➔ 수주 백로그 매출 전환 ➔ 100%+ 랠리",
        "if_worst": "글로벌 경기 침체로 유가 $50 이하 폭락",
        "kill_switch": "WTI 유가 $55 이하 6개월 지속 시"
    },
    "VAL": {
        "name": "발라리스 (Valaris)",
        "sector": "🌊 해양 시추선 2위",
        "tag": "무차입 시추선사",
        "category": "ocean",
        "thesis": "파산 구조조정으로 부채 털어낸 깨끗한 대차대조표의 해양 시추 기업",
        "special_issue": "수주 잔고 순차적 매출 전환으로 FCF 급증 국면",
        "if_best": "해양 플로터 가동률 95% 돌파 ➔ 주가 전고점 회복",
        "if_worst": "오프쇼어 프로젝트 지연",
        "kill_switch": "수주 잔고 순감소 2분기 연속 발생 시"
    },
    "OII": {
        "name": "오셔니어링",
        "sector": "🤖 심해 로봇(ROV) 독점",
        "tag": "해저 작업 1위",
        "category": "ocean",
        "thesis": "수심 3,000m 작업 무인 원격 로봇팔(ROV) 글로벌 1위 독점사",
        "special_issue": "해저 광케이블 매설, 심해 유전 보수, 미 해군 무인 잠수정 수주",
        "if_best": "해저 인프라 투자 폭증 ➔ 영업이익률 20% 돌파",
        "if_worst": "심해 탐사 CAPEX 동결",
        "kill_switch": "ROV 가동률 50% 붕괴 시"
    },

    # [우주 방산 / 지상국 관제]
    "KTOS": {
        "name": "크라토스 (Kratos)",
        "sector": "📡 위성 지상 관제 독점",
        "tag": "지상국 80%",
        "category": "defense",
        "thesis": "전 세계 위성 80%가 경유하는 지상국 관제 소프트웨어 독점",
        "special_issue": "미 우주군 차세대 관제 시스템 수주 및 무인 전투기 사업",
        "if_best": "미 우주군 예산 급증 + 상용 저궤도 위성 지상국 수주 폭발",
        "if_worst": "정부 국방 예산 일시 삭감",
        "kill_switch": "우주 부문 매출 역성장 시"
    },
    "LHX": {
        "name": "L3해리스 (L3Harris)",
        "sector": "🛡️ 방산 통신 / 전자전 1위",
        "tag": "군용 전술통신",
        "category": "defense",
        "thesis": "미 국방부 전술 라디오, 군용 위성 통신, 전자전 시스템 독점",
        "special_issue": "에어로젯 로켓다인 인수로 미사일 로켓 모터 생산 내재화",
        "if_best": "신냉전 미사일/위성 통신 주문 폭주 ➔ FCF 30억 달러 달성",
        "if_worst": "인수 관련 부채 상환 지연",
        "kill_switch": "영업이익률 10% 미만 하락 시"
    },

    # [헬스케어 / 소프트웨어 / 소비재 턴어라운드]
    "CI": {
        "name": "시그나 (The Cigna Group)",
        "sector": "🏥 헬스케어 / PBM 요새",
        "tag": "현금 요새",
        "category": "health",
        "thesis": "미국 3대 처방약 급여관리(PBM) 및 기업 건강보험 과점",
        "special_issue": "휴마나 인수 철회 후 남는 현금 전액 자사주 소각. P/E 10배 바닥권",
        "if_best": "가치주 피난처 부각 ➔ P/E 15배 리레이팅 ($380+)",
        "if_worst": "미 의회의 초당적 PBM 마진 규제 입법 통과",
        "kill_switch": "PBM 수수료 모델 금지 연방법 통과 시"
    },
    "PRVA": {
        "name": "프리비아 헬스",
        "sector": "🩺 가치기반 1차의료",
        "tag": "무차입 순현금",
        "category": "health",
        "thesis": "의사들을 네트워크로 묶어 의료비 절감분을 인센티브로 공유",
        "special_issue": "52주 최저가 부근 바닥. 무차입 순현금으로 고령화 메디케어 수혜",
        "if_best": "메디케어 환자 유입 폭증 ➔ EPS 연 20% 성장 ➔ 주가 $30+ 회복",
        "if_worst": "정부 메디케어 어드밴티지 보조금 삭감",
        "kill_switch": "분기 EBITDA 적자 전환 시"
    },
    "DOX": {
        "name": "암독스 (Amdocs)",
        "sector": "📞 통신사 과금 독점",
        "tag": "Fwd P/E 7.1배",
        "category": "health",
        "thesis": "글로벌 주요 통신사 빌링 소프트웨어 전환 비용 극상 독점",
        "special_issue": "Fwd P/E 7.1배, P/FCF 9.6배의 탄탄한 현금흐름과 자사주 매입",
        "if_best": "통신사 5G/클라우드 전환 수주 지속 ➔ 멀티플 정상화",
        "if_worst": "통신사들의 자체 인하우스 빌링 전환 시도",
        "kill_switch": "핵심 고객사 계약 해지 시"
    },
    "PATH": {
        "name": "유아이패스 (UiPath)",
        "sector": "💻 RPA 사무자동화",
        "tag": "순현금 10억$",
        "category": "health",
        "thesis": "글로벌 1위 RPA 기업. 에이전틱 자동화로 진화 중",
        "special_issue": "AI 대체 공포로 주가 폭락. 순현금 10억 달러+ 보유로 망할 위험 0",
        "if_best": "에이전틱 AI 워크플로우 안착 ➔ 주가 100% 턴어라운드",
        "if_worst": "거대 LLM이 RPA 없이 화면 완벽 조작",
        "kill_switch": "분기 ARR 순감소 또는 순현금 적자 시"
    },
    "NKE": {
        "name": "나이키 (Nike)",
        "sector": "👟 스포츠 퍼포먼스",
        "tag": "P/E 10년 최저",
        "category": "health",
        "thesis": "알파플라이 마라톤 기술 독점 + 32년 순혈 CEO 엘리엇 힐 복귀",
        "special_issue": "중국 리스크 선반영으로 주가 반토막 바닥. 러닝 퍼포먼스 복원 가속",
        "if_best": "홀세일 유통망 복원 및 신규 러닝 라인업 호조 ➔ 주가 50%+ 회복",
        "if_worst": "중국 시장 점유율 추가 하락",
        "kill_switch": "매출총이익률 40% 붕괴 시"
    },
    "GEHC": {
        "name": "GE 헬스케어 (GE HealthCare)",
        "sector": "🏥 영상진단(MRI/CT) 1위",
        "tag": "저P/E 14배",
        "category": "health",
        "thesis": "전 세계 MRI, CT, 초음파 영상진단 장비 및 조영제 글로벌 3대 독점사",
        "special_issue": "중국 병원 장비 발주 지연으로 52주 저점 턱밑(+12.4%) 바닥권. P/E 14배 수준의 역사적 저평가",
        "if_best": "글로벌 병원 진단장비 교체 주기 도래 + AI 진단 소프트웨어 구독 매출 성장 ➔ 주가 $90+ 회복",
        "if_worst": "중국 의료장비 국산화 대체 가속",
        "kill_switch": "분기 수주(Book-to-Bill) 0.9 미만 2분기 지속 시"
    },
    "ASTH": {
        "name": "아스트라나 헬스 (Astrana Health)",
        "sector": "🩺 로컬 의사 MSO 1위",
        "tag": "흑자 MSO",
        "category": "health",
        "thesis": "로컬 1차 진료 의사들의 청구/행정/EHR 대행 및 가치기반의료(VBC) 수수료 독점",
        "special_issue": "프로스펙트 헬스 대형 M&A 인수 비용으로 고점 대비 -32.5% 조정. 통합 완료 시 FCF 급증 잠재력",
        "if_best": "M&A 네트워크 통합 완료 ➔ 캘리포니아/텍사스 커버리지 확장 및 EPS 연 25% 점프",
        "if_worst": "피인수 병원/클리닉의 부실 의료비 손실 전이",
        "kill_switch": "영업이익 적자 전환 또는 부채 상환 불능 이슈 발생 시"
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
    print(f"Collecting radar data for {len(WATCHLIST)} stocks...")
    stock_items = []
    
    for ticker, meta in WATCHLIST.items():
        data = fetch_stock_data(ticker)
        stock_items.append({
            "ticker": ticker,
            "meta": meta,
            "data": data
        })

    # 52주 최저가에 가장 가까운 순(오름차순) 자동 정렬
    stock_items.sort(key=lambda x: x["data"].get("from_low_pct", 999) if x["data"].get("status") == "OK" else 999)

    now_dt = datetime.datetime.now()
    updated_str = now_dt.strftime("%Y년 %m월 %d일 %H:%M")

    out_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(out_dir, "radar_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"updated": updated_str, "items": stock_items}, f, ensure_ascii=False, indent=2)

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
            <div class="{card_class}" id="card-{t}" data-category="{m['category']}">
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
                    <div class="issue-title"><i class="bi bi-lightning-charge-fill text-gold"></i> 특수 상황 & 핵심 촉매</div>
                    <div class="issue-desc">{m['special_issue']}</div>
                </div>

                <div class="scenario-accordion">
                    <details>
                        <summary><i class="bi bi-diagram-3"></i> 시나리오 및 손절선 보기</summary>
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
    <title>종목 레이더 | 52주 신저가 & 특수 상황 모니터링 - ThePathLab</title>
    <meta name="description" content="ThePathLab 종목 레이더: 식량 안보, 폐기물 인프라, 원자력, 철도, 심해 시추 등 물리적 해자 독점 기업의 52주 최저가 및 특수 이슈 실시간 감시 대시보드">
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

    <header class="hero-wrap">
        <div class="hero-badge">
            <i class="bi bi-radar"></i> ThePathLab Stock Radar
        </div>
        <h1 class="hero-title">종목 레이더</h1>
        <p class="hero-desc">
            식량 안보, 폐기물 처리, 원자력, 철도, 심해 시추 등 대체 불가능한 물리적 해자를 가진 기업들의 52주 최저가 근접도 및 특수 상황(Special Situation) 실시간 감시 대시보드입니다.
        </p>
        <div class="meta-bar">
            <div class="meta-item">
                <i class="bi bi-clock-history"></i> 갱신 기준: <strong>{updated_str}</strong>
            </div>
            <div class="meta-item">
                <i class="bi bi-fire text-gold"></i> 현재 바닥 사정권: <strong>{bottom_count}개 종목</strong>
            </div>
            <div class="meta-item">
                <i class="bi bi-sort-down text-gold"></i> 정렬: <strong>52주 최저가 근접순</strong>
            </div>
        </div>
    </header>

    <div class="filter-bar">
        <button class="filter-btn active" onclick="filterCategory('all')">전체보기 ({len(stock_items)})</button>
        <button class="filter-btn" onclick="filterCategory('alert')">🔥 바닥 사정권</button>
        <button class="filter-btn" onclick="filterCategory('food')">🌾 식량/비료</button>
        <button class="filter-btn" onclick="filterCategory('infra')">🏭 폐기물/인프라</button>
        <button class="filter-btn" onclick="filterCategory('power')">⚡ 전력/원자력</button>
        <button class="filter-btn" onclick="filterCategory('ocean')">🌊 심해/자원</button>
        <button class="filter-btn" onclick="filterCategory('defense')">📡 방산/우주</button>
        <button class="filter-btn" onclick="filterCategory('health')">🏥 헬스케어/기타</button>
    </div>

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
                }} else {{
                    const cCat = card.getAttribute('data-category');
                    card.style.display = (cCat === cat) ? 'block' : 'none';
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

    print(f"Stock Radar dashboard built successfully at: {html_path}")

if __name__ == "__main__":
    build_radar()
