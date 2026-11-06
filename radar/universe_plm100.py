# -*- coding: utf-8 -*-
"""
🏆 ThePathLab PLM100 (PathLab Moat 100)
1부 리그: 전 세계에서 가장 안전하고 현금을 뿜어내는 '철옹성 독점 해자' 100대 기업
기준: EPS > 0 흑자, 무차입 순현금(D/E < 1), OPM > 15%, 대체 불가 톨게이트
"""

PLM100_WATCHLIST = {
    # ==========================================
    # 💻 [AI 반도체 / 인프라 / 소프트웨어 톨게이트] (15)
    # ==========================================
    "NVDA": {
        "name": "엔비디아 (NVIDIA)", "country": "US", "sector": "💻 AI 가속기 & CUDA 독점", "category": "tech",
        "thesis": "전 세계 AI 가속기 시장 90%+ 장악 및 CUDA 소프트웨어 생태계 락인",
        "if_best": "블랙웰 울트라 공급 폭증 + 추론용 수요 폭발 ➔ 전고점 돌파 랠리",
        "if_worst": "빅테크 AI 데이터센터 투자(CAPEX) 급격한 동결",
        "kill_switch": "데이터센터 분기 매출 전분기 대비 15% 이상 역성장 시"
    },
    "AVGO": {
        "name": "브로드컴 (Broadcom)", "country": "US", "sector": "💻 커스텀 AI ASIC & 스위칭", "category": "tech",
        "thesis": "구글 TPU, 메타 MTIA 맞춤형 AI 칩 설계 1위 + 토마호크 통신 스위칭 독점",
        "if_best": "빅테크 자체 ASIC 채택률 50%+ 돌파 ➔ 연 FCF 300억 달러+ 창출",
        "if_worst": "VMware 대기업 고객사 오픈소스 이탈 가속",
        "kill_switch": "반도체 솔루션 영업이익률 30% 붕괴 시"
    },
    "000660.KS": {
        "name": "SK하이닉스", "country": "KR", "sector": "🧠 HBM3E/HBM4 메모리 독점", "category": "tech",
        "thesis": "엔비디아 블랙웰 HBM3E 독점 공급망, MR-MUF 패키징 기술 격차로 OPM 30%+",
        "if_best": "HBM4 조기 양산 및 차세대 AI 서버 탑재량 2배 증가 ➔ 사상 최대 영업이익",
        "if_worst": "경쟁사(삼성/마이크론)의 HBM3E 공급 퀄테스트 통과로 단가 인하 압박",
        "kill_switch": "HBM 부문 분기 영업이익률 20% 미만으로 급락 시"
    },
    "ASML": {
        "name": "ASML 홀딩", "country": "NL", "sector": "🔬 EUV 초미세 노광장비 100% 독점", "category": "tech",
        "thesis": "2나노 이하 첨단 반도체 양산 시 절대 대체 불가능한 EUV 장비 전 세계 유일 공급자",
        "if_best": "글로벌 파운드리 2나노 경쟁 본격화 ➔ High-NA EUV 수주잔고 사상 최대",
        "if_worst": "미국의 대중국 레거시 DUV 장비 수출 규제 추가 강화",
        "kill_switch": "분기 신규 수주(Net Bookings) 2분기 연속 40% 이상 급감 시"
    },
    "SNPS": {
        "name": "시놉시스 (Synopsys)", "country": "US", "sector": "🧠 반도체 설계 EDA 툴 1위", "category": "tech",
        "thesis": "2nm/3nm 칩 설계 시 절대 대체 불가한 전자설계자동화(EDA) 글로벌 과점",
        "if_best": "AI 칩 설계 붐으로 EDA 라이선스 계약 단가 폭증 ➔ 전고점 회복",
        "if_worst": "각국 반독점 규제 당국의 앤시스 합병 불허",
        "kill_switch": "분기 반복 라이선스 매출(ARR) 순감소 시"
    },
    "CDNS": {
        "name": "케이던스 (Cadence)", "country": "US", "sector": "🧠 반도체 EDA 소프트웨어 과점", "category": "tech",
        "thesis": "시놉시스와 함께 전 세계 칩 설계를 양분하는 과점 소프트웨어 제국",
        "if_best": "파운드리 2나노 공정 전환 가속 ➔ EDA 툴 사용료 30% 인상 반영",
        "if_worst": "글로벌 팹리스 스타트업들의 R&D 예산 삭감",
        "kill_switch": "영업현금흐름(OCF) 마진 30% 미만 하락 시"
    },
    "KLAC": {
        "name": "KLA 코퍼레이션", "country": "US", "sector": "🔬 나노 미세 수율/계측 독점", "category": "tech",
        "thesis": "웨이퍼 표면 미세 결함 및 광학 계측 글로벌 1위 독점 (영업마진 40%)",
        "if_best": "파운드리 2나노 경쟁 심화 ➔ 계측 장비 수주 잔고 사상 최대",
        "if_worst": "대중국 첨단 반도체 장비 수출 통제 전면 확대",
        "kill_switch": "분기 영업이익률 30% 이하로 급락 시"
    },
    "AMAT": {
        "name": "어플라이드 머티어리얼즈", "country": "US", "sector": "⚙️ 반도체 전공정 장비 1위", "category": "tech",
        "thesis": "증착, 식각, 이온주입 등 반도체 제조 전공정 세계 최대 포트폴리오 보유",
        "if_best": "글로벌 반도체 팹 신설(IIJA) 본격 가동 ➔ 사상 최대 실적 비트",
        "if_worst": "글로벌 팹 완공 지연 및 장비 입고 연기",
        "kill_switch": "수주-출하 비율(Book-to-Bill) 0.90 미만 2분기 지속 시"
    },
    "058470.KQ": {
        "name": "리노공업", "country": "KR", "sector": "🔬 반도체 테스트 소켓 1위 독점", "category": "tech",
        "thesis": "글로벌 빅테크 맞춤형 AI/모바일 칩 R&D 테스트 핀/소켓 독점. 영업이익률 40%+, 무차입 순현금",
        "if_best": "온디바이스 AI 칩 종류 폭증으로 테스트 핀 수요 폭발 ➔ 영업마진 45% 돌파",
        "if_worst": "스마트폰 교체 주기 장기화로 모바일 부문 수주 일시 둔화",
        "kill_switch": "영업이익률 30% 미만 붕괴 시"
    },
    "6861.T": {
        "name": "키엔스 (Keyence)", "country": "JP", "sector": "🤖 공장자동화 스마트센서 1위", "category": "tech",
        "thesis": "글로벌 스마트팩토리 광학 센서/바코드/계측 독점. 영업이익률 50%+, 무차입 순현금 수조 원",
        "if_best": "글로벌 제조 리쇼어링 및 무인 자동화 붐 ➔ 사상 최대 분기 영업익",
        "if_worst": "글로벌 제조업 CAPEX 동결",
        "kill_switch": "영업이익률 40% 미만 하락 시"
    },
    "6146.T": {
        "name": "디스코 (Disco Corp)", "country": "JP", "sector": "⚙️ 반도체 웨이퍼 절삭/연마 80% 독점", "category": "tech",
        "thesis": "HBM 적층 및 차세대 패키징 필수인 웨이퍼 다이싱/그라인딩 글로벌 70~80% 독점",
        "if_best": "HBM 고단 적층 가속화로 그라인딩/슬라이싱 장비 및 소모품 휠 매출 폭증",
        "if_worst": "반도체 패키징 투자 사이클 일시적 둔화",
        "kill_switch": "장비 수주잔고 전년비 20% 이상 역성장 시"
    },
    "4063.T": {
        "name": "신에츠화학 (Shin-Etsu)", "country": "JP", "sector": "🧪 반도체 실리콘 웨이퍼 1위", "category": "tech",
        "thesis": "300mm 고품질 실리콘 웨이퍼 및 포토레지스트 글로벌 1위. 30년 무차입 흑자 제국",
        "if_best": "AI 칩 양산 붐으로 프리미엄 에피택셜 웨이퍼 공급 부족 ➔ 판가 20% 인상",
        "if_worst": "PVC 화학 시황 부진 장기화",
        "kill_switch": "반도체 소재 부문 영업이익률 20% 미만 하락 시"
    },
    "INTU": {
        "name": "인튜이트 (Intuit)", "country": "US", "sector": "📊 세무 & 회계 SaaS 독점", "category": "tech",
        "thesis": "미국 개인 세무 신고(터보택스) + 3천만 중소기업 회계(퀵북스) 법적 신고 락인",
        "if_best": "퀵북스 AI 자동장부 기능 안착 + ARPU 15% 상승 ➔ 밸류 리레이팅",
        "if_worst": "미 국세청(IRS)의 직접 무료 세무 신고(Direct File) 전면 의무화",
        "kill_switch": "터보택스 유료 이용자 수 10% 이상 순감소 시"
    },
    "NOW": {
        "name": "서비스나우 (ServiceNow)", "country": "US", "sector": "🏢 전사 IT 워크플로우 1위", "category": "tech",
        "thesis": "포춘 500대 기업 85%가 사용하는 IT 헬프데스크 및 업무 자동화 중앙 플랫폼 (갱신율 98%)",
        "if_best": "엔터프라이즈 AI 에이전트 도입 폭증 ➔ 연 FCF 40억 달러 돌파",
        "if_worst": "빅테크(MS, Salesforce)와의 업무 영역 침범 경쟁 격화",
        "kill_switch": "순매출 유지율(NRR) 115% 미만 붕괴 시"
    },
    "COHR": {
        "name": "코히런트 (Coherent)", "country": "US", "sector": "⚡ AI 데이터센터 광트랜시버 1위", "category": "tech",
        "thesis": "AI 클러스터 초고속 데이터 전송용 800G/1.6T 광트랜시버 핵심 부품 독점",
        "if_best": "빅테크 차세대 AI 클러스터 광통신 모듈 독점 공급 ➔ 실적 서프라이즈",
        "if_worst": "경쟁사 저가 모듈 시장 침투",
        "kill_switch": "광통신 부문 분기 수주잔고 순감소 시"
    },

    # ==========================================
    # 🏭 [산업재 / 실물 인프라 / 오프라인 독점] (20)
    # ==========================================
    "AOS": {
        "name": "A.O. 스미스 (A.O. Smith)", "country": "US", "sector": "🚿 북미 온수기/보일러 1위 독점", "category": "infra",
        "thesis": "북미 온수기 시장 점유율 1위. 온수기는 고장 시 24시간 내 무조건 교체해야 하는 대체 불가 필수재",
        "if_best": "미국 노후 주택 배관 리모델링 붐 + 친환경 히트펌프 온수기 교체 가속",
        "if_worst": "미국 상업용 부동산 착공 절벽",
        "kill_switch": "영업이익률 14% 미만 붕괴 시"
    },
    "GGG": {
        "name": "그라코 (Graco Inc.)", "country": "US", "sector": "⚙️ 산업용 정밀 도장/유체 제어 1위", "category": "infra",
        "thesis": "특수 도료, 접착제, 실런트 정밀 분사 장비 글로벌 1위. 영업이익률 28~30%, 무차입 복리 머신",
        "if_best": "배터리/태양광 조립용 정밀 디스펜싱 장비 매출 폭발 ➔ 전고점 돌파",
        "if_worst": "글로벌 자동차 조립 라인 증설 전면 중단",
        "kill_switch": "영업이익률 20% 미만으로 급락 시"
    },
    "SNA": {
        "name": "스냅온 (Snap-on)", "country": "US", "sector": "🔧 북미 프리미엄 정비공구 1위 독점", "category": "infra",
        "thesis": "카센터 전속 밴(Van) 트럭 방문 순회 판매망으로 영지 독점. 북미 정비사들의 에르메스",
        "if_best": "차량 노후화로 미국 평균 차령 12.6년 돌파 ➔ 정비공구 및 진단기기 교체 주기 가속",
        "if_worst": "정비사 신규 유입 급감 및 저가 공구 침투",
        "kill_switch": "영업현금흐름(OCF) 마진 15% 미만 하락 시"
    },
    "JKHY": {
        "name": "잭 헨리 (Jack Henry)", "country": "US", "sector": "🏦 지방은행 코어뱅킹 시스템 독점", "category": "infra",
        "thesis": "미국 1,000개 지방은행/신협의 전산 척추 코어뱅킹 장악. 계약 갱신율 99%, 20년간 못 바꾸는 락인",
        "if_best": "지방은행들의 디지털 뱅킹 클라우드 전환 수수료 매출 폭증 ➔ 연 10%+ 복리 랠리",
        "if_worst": "지방은행 대규모 연쇄 파산",
        "kill_switch": "핵심 코어 소프트웨어 ARR 순감소 시"
    },
    "FIX": {
        "name": "컴포트 시스템즈 (Comfort Systems)", "country": "US", "sector": "❄️ AI 데이터센터 냉각/MEP 1위", "category": "infra",
        "thesis": "빅테크 AI 데이터센터의 액체냉각, HVAC 공조 및 모듈러 MEP 시공 압도적 1위",
        "if_best": "차세대 액체냉각 단가 인상 + 메가 데이터센터 착공 폭증 ➔ 전고점 돌파",
        "if_worst": "빅테크 AI 데이터센터 설비투자(CAPEX) 동결",
        "kill_switch": "수주-출하 비율(Book-to-Bill) 1.0 미만 2분기 연속 붕괴 시"
    },
    "HWM": {
        "name": "하우멧 에어로스페이스", "country": "US", "sector": "✈️ 제트엔진 터빈 블레이드 독점", "category": "infra",
        "thesis": "보잉/에어버스 제트엔진의 초고온 합금 터빈 블레이드 및 항공기 패스너 1등 독점",
        "if_best": "항공기 제작사 인도량 정상화 + 방산 전투기 엔진 수주 ➔ 마진 추가 확대",
        "if_worst": "티타늄 등 핵심 항공우주 원자재 공급망 단절",
        "kill_switch": "엔진 부문 영업이익률 20% 미만 하락 시"
    },
    "HEI": {
        "name": "하이코 (HEICO)", "country": "US", "sector": "✈️ FAA 승인 대체부품(PMA) 독점", "category": "infra",
        "thesis": "순정품 대비 30~50% 저렴한 FAA 승인 항공기 대체 부품 독점 공급자 (30년 복리 20%+)",
        "if_best": "글로벌 항공 여객 수요 증가 속 대체 부품 침투율 40% 돌파 ➔ 실적 점프",
        "if_worst": "PMA 대체 부품의 중대 품질 결함 이슈 발생",
        "kill_switch": "FAA의 핵심 부품 PMA 인가 취소 시"
    },
    "CPRT": {
        "name": "코파트 (Copart)", "country": "US", "sector": "🚗 전손차/사고차 경매 독점", "category": "infra",
        "thesis": "미국 보험사고 전손 차량 온라인 경매 1위 독점 + 대도시 주변 토지 야드 인허가 해자 (마진 40%)",
        "if_best": "차량 첨단화로 수리비 급증 ➔ 전손 처리율 상승 수혜",
        "if_worst": "자동차 사고율의 구조적 급감 (자율주행)",
        "kill_switch": "전손차 출품 대수 2분기 연속 10% 이상 감소 시"
    },
    "ULS": {
        "name": "UL 솔루션스 (UL Solutions)", "country": "US", "sector": "🏷️ 전자기기 안전규격 100% 독점", "category": "infra",
        "thesis": "전 세계 전자기기, 배터리, 건축 자재에 찍히는 'UL 마크' 안전인증 독점 톨게이트",
        "if_best": "EV 배터리, 신재생, AI 데이터센터 기기 안전 인증 필수화 ➔ 수수료 15% 성장",
        "if_worst": "유럽 CE 등 경쟁 인증 규격의 미국 시장 잠식",
        "kill_switch": "인증 부문 영업이익률 15% 미만 하락 시"
    },
    "CTAS": {
        "name": "신타스 (Cintas)", "country": "US", "sector": "👔 기업 유니폼 렌탈/세탁 1위", "category": "infra",
        "thesis": "미국 기업 유니폼 렌탈 및 사업장 안전용품 배송 트럭망 독점 (고객유지율 95%+)",
        "if_best": "신규 헬스케어/서비스업 유니폼 고객 침투 ➔ 40년 연속 배당 증액 랠리",
        "if_worst": "미국 실업률 급등으로 사업장 근무자 수 급감",
        "kill_switch": "유기적 매출 성장률 마이너스 전환 시"
    },
    "WM": {
        "name": "웨이스트 매니지먼트", "country": "US", "sector": "🗑️ 매립지 토지 독점", "category": "infra",
        "thesis": "신규 인허가 불가한 북미 최대 매립지 영지 독점 + 매립가스 발전 (물가연동 가격력)",
        "if_best": "매립가스(RNG) 전력 판매 고성장 ➔ 배당 및 자사주 확대",
        "if_worst": "환경 규제 강화로 매립지 사후 관리 비용 급증",
        "kill_switch": "영업현금흐름(OCF) 마진율 5%p 이상 하락 시"
    },
    "RSG": {
        "name": "리퍼블릭 서비스", "country": "US", "sector": "🗑️ 폐기물 과점 2위", "category": "infra",
        "thesis": "북미 2위 폐기물 처리 과점. 지자체 장기 수거 계약 기반 경기 침체 무풍지대",
        "if_best": "자원 재활용 및 환경 인프라 인수로 연 10%+ EPS 성장",
        "if_worst": "유가 폭등으로 수거 트럭 유류비 급증",
        "kill_switch": "자유현금흐름 적자 전환 시"
    },
    "CLH": {
        "name": "클린 하버즈", "country": "US", "sector": "☣️ 특수 유해폐기물 1위", "category": "infra",
        "thesis": "반도체·화학 공장 유해 폐기물 소각 및 정화 인프라 독점 (초고마진 소각로 해자)",
        "if_best": "미국 제조업 리쇼어링으로 산업 폐기물 처리 수요 급증 ➔ 판가 20% 인상",
        "if_worst": "주요 소각 시설 안전 사고로 가동 중단",
        "kill_switch": "EBITDA 마진 15% 미만 하락 시"
    },
    "MWA": {
        "name": "뮬러 워터 (Mueller Water)", "country": "US", "sector": "🚰 북미 상수도 밸브/소화전 독점", "category": "infra",
        "thesis": "미국 상수도 인프라의 밸브, 소화전, 배관 제어 독점 공급자. 미국 노후 수도관 교체 필수재",
        "if_best": "미 연방 인프라법(IIJA) 예산 집행 본격화 ➔ 배관 부품 수주 폭발",
        "if_worst": "원자재(고철/구리) 원가 급등 및 지자체 발주 지연",
        "kill_switch": "영업이익률 10% 미만 붕괴 시"
    },
    "WMS": {
        "name": "어드밴스드 드레인지", "country": "US", "sector": "🌧️ 친환경 플라스틱 우수관 독점", "category": "infra",
        "thesis": "콘크리트 배관 대비 가볍고 부식 없는 열가소성 골판 우수관 북미 1위 독점 (재활용 플라스틱 해자)",
        "if_best": "홍수/기후변화 방재 인프라 법안 통과 ➔ 대형 데이터센터 우수관 독점 납품",
        "if_worst": "미국 주택 착공 건수 급감",
        "kill_switch": "FCF 적자 전환 시"
    },
    "UNP": {
        "name": "유니언 퍼시픽", "country": "US", "sector": "🚂 미국 서부 철도 독점", "category": "infra",
        "thesis": "트럭 대비 운송비 1/4. 미국 서부·중부 물류 인프라 영구 독점 (대체 불가 선로망)",
        "if_best": "곡물, 화학물질, 공산품 컨테이너 운송량 사상 최대 ➔ 영업비율(OR) 55% 달성",
        "if_worst": "철도 노조 파업 장기화",
        "kill_switch": "영업비율(OR) 68% 이상으로 수익성 악화 시"
    },
    "CSX": {
        "name": "CSX 코퍼레이션", "country": "US", "sector": "🚂 미국 동부 철도 독점", "category": "infra",
        "thesis": "뉴욕 대도시 쓰레기 전정 수송(Trash Train) 및 동부 공업지대 철도 독점망",
        "if_best": "동부 항만 물동량 내륙 연계 철송 수수료 인상 ➔ FCF 20억 달러+ 창출",
        "if_worst": "석탄 운송 수요 구조적 소멸",
        "kill_switch": "분기 운송 볼륨(Volume) 10% 이상 지속 감소 시"
    },
    "NUE": {
        "name": "뉴코어 (Nucor)", "country": "US", "sector": "🔩 전기로 철강 1위 (50년 배당귀족)", "category": "infra",
        "thesis": "미국 최대 전기로 고철 재활용 철강사. 저렴한 전기 원가 우위 + 무차입급 건전성",
        "if_best": "미국 인프라 재건 및 방산 장갑강 수요 폭증 ➔ 스프레드 사상 최대",
        "if_worst": "글로벌 철강 덤핑 공급 과잉",
        "kill_switch": "50년 연속 배당 증액 삭감 공시 시"
    },
    "XYL": {
        "name": "자일럼 (Xylem Inc.)", "country": "US", "sector": "💧 글로벌 수처리 펌프/스마트 밸브 1위", "category": "infra",
        "thesis": "전 세계 상하수도, 해수담수화, 반도체 초순수 공급용 초고압 펌프·스마트 밸브 1등",
        "if_best": "글로벌 기후 위기로 지자체 수처리 현대화 발주 ➔ 수주잔고 사상 최대",
        "if_worst": "유럽 경기 침체로 산업용 펌프 발주 연기",
        "kill_switch": "영업이익률 10% 미만 하락 시"
    },
    "ECL": {
        "name": "이콜랩 (Ecolab)", "country": "US", "sector": "🧪 산업용 정수/멸균 케미컬 1위", "category": "infra",
        "thesis": "반도체 팹, 식품 공장, 병원에서 물을 정화하고 재활용하는 특수 케미컬 락인 (빌 게이츠 최대주주)",
        "if_best": "AI 데이터센터 수냉식 쿨링 타워 수처리 케미컬 독점 납품 ➔ 고성장 랠리",
        "if_worst": "원자재 화학 원가 급등",
        "kill_switch": "자유현금흐름(FCF) 마진 10% 미만 하락 시"
    },

    # ==========================================
    # 🏥 [독점 헬스케어 / 의약품 유통 / 필수 의료기기] (15)
    # ==========================================
    "MCK": {
        "name": "맥케슨 (McKesson)", "country": "US", "sector": "🏥 미국 1위 의약품 유통 톨게이트", "category": "health",
        "thesis": "미국 3대 의약품 유통 과점 1위 (연 매출 $111B+). 종양학/바이오 전문의약품 독점 유통망, P/FCF 16배",
        "if_best": "바이오시밀러 및 GLP-1 비만치료제 유통 물량 폭증 ➔ 연간 EPS 가이던스 연속 상향",
        "if_worst": "PBM 및 약가 인하 정부 규제 리스크",
        "kill_switch": "분기 잉여현금흐름(FCF) 적자 전환 시"
    },
    "VRTX": {
        "name": "버텍스 파마슈티컬", "country": "US", "sector": "🧬 낭포성 섬유증 100% 독점", "category": "health",
        "thesis": "유전성 희귀질환 낭포성 섬유증(CF) 치료제 시장 100% 영구 독점 + CRISPR 유전자 치료제",
        "if_best": "비마약성 진통제(수제트리고) FDA 블록버스터 승인 ➔ 연 매출 30% 점프",
        "if_worst": "비마약성 진통제 임상 부작용 또는 약가 규제",
        "kill_switch": "CF 치료제 글로벌 처방 환자 수 순감소 시"
    },
    "ISRG": {
        "name": "인튜이티브 서지컬", "country": "US", "sector": "🦾 다빈치 수술 로봇 1등 독점", "category": "health",
        "thesis": "전 세계 수술용 로봇 시장 80%+ 장악. 수술할 때마다 팔리는 소모품 기구(Instruments) 락인",
        "if_best": "다빈치 5세대 글로벌 병원 교체 설치 폭증 ➔ 연간 시술 건수 25% 성장",
        "if_worst": "병원들의 고가 의료 장비 CAPEX 예산 삭감",
        "kill_switch": "연간 수술 건수(Procedure Growth) 5% 미만 둔화 시"
    },
    "IDXX": {
        "name": "아이덱스 랩스 (IDEXX)", "country": "US", "sector": "🐕 동물병원 진단 장비/시약 1위", "category": "health",
        "thesis": "전 세계 동물병원 혈액/소변 진단 장비 및 소모품 시약 독점 (반려동물 가족화 수혜)",
        "if_best": "동물 암 조기진단 신규 키트 글로벌 병원 보급 ➔ 장비당 소모품 매출 20% 증가",
        "if_worst": "경기 침체로 반려동물 동물병원 방문 횟수 급감",
        "kill_switch": "반복 매출(Recurring Revenue) 비중 75% 미만 붕괴 시"
    },
    "WST": {
        "name": "웨스트 파마슈티컬", "country": "US", "sector": "💉 바이오 주사기 고무마개 70% 독점", "category": "health",
        "thesis": "바이오 의약품 바이알 병마개 및 엘라스토머 고무 패킹 글로벌 70% 독점 (대체재 0개)",
        "if_best": "GLP-1 비만치료제 펜 주사기 전용 고무 부품 발주 폭발 ➔ 전고점 회복",
        "if_worst": "고객사들의 코로나 백신 병마개 재고 소진 지연",
        "kill_switch": "고마진 HVP(고가 부품) 매출 비중 역성장 시"
    },
    "RMD": {
        "name": "레스메드 (ResMed)", "country": "US", "sector": "💨 수면무호흡증 양압기(CPAP) 1위", "category": "health",
        "thesis": "전 세계 수면무호흡증 치료용 양압기 및 클라우드 수면 모니터링 1위 과점",
        "if_best": "비만약 복용자들의 수면 질 관심 증대 속 CPAP 처방 병행 ➔ 실적 서프라이즈",
        "if_worst": "GLP-1 약물로 수면무호흡증 완치 환자 대량 발생",
        "kill_switch": "분기 디바이스 매출 전년비 10% 이상 감소 시"
    },
    "CI": {
        "name": "시그나 (The Cigna Group)", "country": "US", "sector": "🏥 헬스케어 / PBM 요새", "category": "health",
        "thesis": "미국 3대 처방약 급여관리(PBM) 에버스노스 및 기업 건강보험 과점 (연 FCF 80억 달러+)",
        "if_best": "휴마나 인수 철회 후 남는 현금 전액 자사주 소각 ➔ EPS 폭발적 증가",
        "if_worst": "미 FTC의 PBM 리베이트 구조 강제 해체",
        "kill_switch": "PBM 부문 영업이익 20% 이상 급감 시"
    },
    "214150.KQ": {
        "name": "클래시스", "country": "KR", "sector": "✨ 피부미용 소모품 톨게이트 1위", "category": "health",
        "thesis": "슈링크/볼뉴머 피부 리프팅 장비 보급 후 시술할 때마다 카트리지 소모품 통행세 독점 (영업마진 50%)",
        "if_best": "미국/브라질/일본 수출 폭발 및 소모품 매출 비중 60% 돌파 ➔ 사상 최대 실적",
        "if_worst": "저가 모방 기기 난립으로 소모품 단가 인하",
        "kill_switch": "영업이익률 35% 미만 하락 시"
    },
    "GEHC": {
        "name": "GE 헬스케어", "country": "US", "sector": "🩻 영상진단(MRI/CT) 1위 과점", "category": "health",
        "thesis": "전 세계 MRI, CT, 초음파 영상진단 장비 및 조영제 글로벌 3대 독점 (P/E 14배 안전마진)",
        "if_best": "AI 영상 판독 솔루션 탑재 신형 MRI 교체 붐 ➔ 마진율 18% 진입",
        "if_worst": "중국 병원 의료장비 반부패 조사로 발주 지연 장기화",
        "kill_switch": "영업현금흐름(OCF) 적자 전환 시"
    },
    "EXEL": {
        "name": "엑셀릭시스 (Exelixis)", "country": "US", "sector": "💊 표적항암제 독점 FCF 머신", "category": "health",
        "thesis": "신장암/간암 표적치료제 카보메틱스 특허 독점. 바이오텍 중 드물게 무차입에 연 FCF 수억 달러 창출",
        "if_best": "카보메틱스 병용요법 적응증 추가 승인 ➔ 연 매출 20% 성장",
        "if_worst": "핵심 특허 조기 만료 분쟁 패소",
        "kill_switch": "카보메틱스 분기 매출 역성장 전환 시"
    },
    "PRVA": {
        "name": "프리비아 헬스 (Privia)", "country": "US", "sector": "🩺 가치기반 1차의료 MSO 1위", "category": "health",
        "thesis": "개원의들을 네트워크로 묶어 진료비 절감분을 인센티브로 공유하는 무차입 순현금 플랫폼",
        "if_best": "고령화 메디케어 수혜 속 참여 의사 수 연 20% 증가 ➔ FCF 폭증",
        "if_worst": "CMS(미 연방의료보험청) 인센티브 지급 기준 강화",
        "kill_switch": "네트워크 참여 의사 수 순감소 시"
    },
    "LNTH": {
        "name": "란테우스 (Lantheus)", "country": "US", "sector": "☢️ 전립선암 방사성의약품 독점", "category": "health",
        "thesis": "전립선암 진단용 방사성의약품 필라리파이(Pylarify) 시장 1위 독점. 고마진 현금 창출",
        "if_best": "PSMA 치료용 방사성 신약 파이프라인 상용화 ➔ 밸류 리레이팅",
        "if_worst": "경쟁 방사성 진단제 시장 진입으로 점유율 하락",
        "kill_switch": "필라리파이 분기 매출 15% 이상 역성장 시"
    },
    "NBIX": {
        "name": "뉴로크린 바이오사이언스", "country": "US", "sector": "🧠 신경계 희귀질환 치료제 독점", "category": "health",
        "thesis": "지연성 운동이상증 치료제 잉그레자(Ingrezza) 독점 판매. 무부채에 연 FCF 5억 달러+",
        "if_best": "선천성 부신과다형성증 신약 크린델리 승인 및 처방 급증",
        "if_worst": "잉그레자 특허 소송 리스크",
        "kill_switch": "영업현금흐름 적자 전환 시"
    },
    "REGN": {
        "name": "리제네론 (Regeneron)", "country": "US", "sector": "👁️ 안과 황반변성 & 아토피 1위", "category": "health",
        "thesis": "아일리아(황반변성) 및 듀피젠트(아토피/천식) 글로벌 블록버스터 보유. 무차입 순현금 $10B+",
        "if_best": "듀피젠트 만성폐쇄성폐질환(COPD) 적응증 추가 ➔ 연 매출 300억 달러 진입",
        "if_worst": "아일리아 바이오시밀러 저가 공세",
        "kill_switch": "분기 순이익 20% 이상 급감 시"
    },
    "BMRN": {
        "name": "바이오마린 (BioMarin)", "country": "US", "sector": "🧬 희귀 유전질환 효소치료제 독점", "category": "health",
        "thesis": "소아 왜소증 치료제 복스조고(Voxzogo) 및 희귀 대사질환 효소 대체 치료제 글로벌 독점",
        "if_best": "복스조고 처방 연령 확대 ➔ 연 매출 30억 달러 조기 달성",
        "if_worst": "경쟁 유전자 치료제 등장으로 효소 대체제 수요 감소",
        "kill_switch": "복스조고 분기 처방 건수 정체 시"
    },

    # ==========================================
    # ⚡ [원전 / 전력망 / 자원 / 에너지 독점] (15)
    # ==========================================
    "CCJ": {
        "name": "카메코 (Cameco)", "country": "CA", "sector": "☢️ 우라늄 채굴 1위 독점", "category": "power",
        "thesis": "서방 1위 고품위 우라늄 광산 및 웨스팅하우스 지분 보유 (원전 르네상스 필수재)",
        "if_best": "빅테크 AI 데이터센터 SMR 전력 계약 폭발 ➔ 우라늄 장기 계약가 $100+ 돌파",
        "if_worst": "원전 중대 사고 발생으로 원자력 정책 후퇴",
        "kill_switch": "우라늄 현물가 파운드당 $50 미만 붕괴 시"
    },
    "BWXT": {
        "name": "BWX 테크놀로지스", "country": "US", "sector": "☢️ 해군 원자로 / 소형모듈원전(SMR)", "category": "power",
        "thesis": "미 해군 원자력 잠수함/항공모함 원자로 100% 독점 제작 + 상용 SMR 핵심 부품",
        "if_best": "미 해군 버지니아급 잠수함 건조 속도 가속 + 지상용 SMR 인허가 완료",
        "if_worst": "국방부 원자력 잠수함 발주 지연",
        "kill_switch": "원자로 제작 부문 영업이익률 12% 미만 붕괴 시"
    },
    "ETN": {
        "name": "이튼 (Eaton)", "country": "US", "sector": "⚡ 변압기 / 배전 솔루션 1위", "category": "power",
        "thesis": "미국 노후 전력망 50년 교체 주기 + AI 데이터센터 전력 장비 독점 수혜",
        "if_best": "초고압 변압기 공급 부족 심화 ➔ 납기 4년, 단가 30% 인상 반영",
        "if_worst": "원자재(구리, 방향성 전기강판) 공급 단절",
        "kill_switch": "전력 부문 수주잔고 순감소 전환 시"
    },
    "PWR": {
        "name": "콴타 서비시즈 (Quanta)", "country": "US", "sector": "⚡ 송배전망 송전탑 시공 1위", "category": "power",
        "thesis": "북미 최대 전력망 송전탑, 재생에너지 연계 변전소 전문 시공 압도적 1위",
        "if_best": "대규모 송전선로 건설 프로젝트 수주 폭증 ➔ 연 15%+ EPS 성장",
        "if_worst": "숙련 송전 전기공 인력난으로 공기 지연",
        "kill_switch": "총 수주잔고(Backlog) 전년비 감소 시"
    },
    "CEG": {
        "name": "콘스텔레이션 에너지", "country": "US", "sector": "☢️ 미국 최대 원자력 발전소", "category": "power",
        "thesis": "미국 1위 무탄소 원전 발전사. MS 스리마일 아일랜드 20년 PPA 독점 전력 계약",
        "if_best": "빅테크 추가 PPA 계약 체결 ➔ 프리미엄 전력 단가 2배 확정",
        "if_worst": "연방에너지규제위원회(FERC)의 원전-데이터센터 직결 송전 불허",
        "kill_switch": "FERC의 빅테크 원전 직결 송전 전면 금지 시"
    },
    "VMC": {
        "name": "벌칸 머티리얼즈", "country": "US", "sector": "🪨 골재(자갈/모래) 지역 독점 1위", "category": "power",
        "thesis": "도로/공장 기초 원자재 골재 1위. 무게로 인해 50마일 밖 수송 불가한 영구 지역 독점",
        "if_best": "인프라법 착공 폭증으로 골재 가격 연 12% 인상 ➔ 마진 극대화",
        "if_worst": "주택 착공 급감으로 단기 출하량 감소",
        "kill_switch": "골재 톤당 현금 총마진(Gross Profit per ton) 감소 시"
    },
    "FSLR": {
        "name": "퍼스트 솔라", "country": "US", "sector": "☀️ 박막 태양광 모듈 독점", "category": "power",
        "thesis": "미국 내 100% 제조 박막 태양광 독점. 2028년까지 수주 백로그 완판, Fwd P/E 7배 바닥",
        "if_best": "빅테크 데이터센터 자가발전 태양광 대형 수주 ➔ 밸류 리레이팅 (+50%)",
        "if_worst": "미 의회의 IRA 세액공제(45X) 폐지 또는 대폭 축소",
        "kill_switch": "IRA 제조 보조금 전면 폐지 입법 통과 시"
    },
    "VNOM": {
        "name": "바이퍼 에너지 (Viper)", "country": "US", "sector": "🛢️ 셰일 광물 로열티 무차입 톨게이트", "category": "power",
        "thesis": "시추 비용 부담 0. 다이아몬드백 석유 채굴 매출의 20%를 통행세로 걷는 순현금 제국",
        "if_best": "퍼미안 분지 시추 효율 증대 ➔ 배당수익률 연 8%+ 폭발",
        "if_worst": "국제 유가 배럴당 $50 미만 급락",
        "kill_switch": "순환 배당수익률 4% 미만 하락 시"
    },
    "WHD": {
        "name": "선인장 (Cactus Inc.)", "country": "US", "sector": "🌵 유정 웰헤드 압력제어 1위", "category": "power",
        "thesis": "셰일 유정 굴착 시 필수인 웰헤드 안전 밸브 1등 독점. P/FCF 10배, 영업마진 30%",
        "if_best": "중동 및 해상 시추 신제품 공급 확대 ➔ 실적 서프라이즈",
        "if_worst": "미국 내 가동 리그(Rig) 수 20% 이상 급감",
        "kill_switch": "분기 영업이익률 20% 미만 하락 시"
    },
    "EOG": {
        "name": "EOG 리소스", "country": "US", "sector": "🛢️ 프리미엄 셰일 오일 FCF 머신", "category": "power",
        "thesis": "배럴당 $40 이하 손익분기점을 가진 미국 최고 효율 셰일 기업. 부채비율 10%대, 무차입 현금 부자",
        "if_best": "천연가스 수출 인프라 가동 + 유가 안정 ➔ 특별 배당 및 자사주 10% 소각",
        "if_worst": "연방 토지 시추 규제 강화",
        "kill_switch": "연간 잉여현금흐름 적자 전환 시"
    },
    "SCCO": {
        "name": "서던 코퍼 (Southern Copper)", "country": "US", "sector": "🥉 글로벌 구리 광산 최저원가 1위", "category": "power",
        "thesis": "전기차, 전력망, AI 데이터센터 필수재 구리. 부산물 몰리브덴 채굴로 세계 최저 생산원가 해자",
        "if_best": "글로벌 구리 공급 부족으로 구리 가격 파운드당 $5.5 돌파 ➔ 배당 폭발",
        "if_worst": "페루/멕시코 광산 파업 및 국유화 세금 인상",
        "kill_switch": "구리 파운드당 현금 원가 급등으로 마진 20% 붕괴 시"
    },
    "FCX": {
        "name": "프리포트 맥모란", "country": "US", "sector": "🥉 세계 최대 상장 구리 광산", "category": "power",
        "thesis": "인도네시아 그라스버그 메가 광산 보유. 전력망 확대에 따른 구리 수요 영구 락인",
        "if_best": "구리 쇼티지 심화 속 배당 및 자사주 소각 확대 ➔ 전고점 돌파",
        "if_worst": "인도네시아 제련소 화재 등 가동 중단",
        "kill_switch": "분기 OCF 50% 이상 급감 시"
    },
    "BHP": {
        "name": "BHP 그룹", "country": "AU", "sector": "⛏️ 세계 최대 광산 제국 (철광석/구리)", "category": "power",
        "thesis": "호주 저원가 철광석 및 칠레 대형 구리 광산 독점. 무차입급 대차대조표와 막대한 현금흐름",
        "if_best": "글로벌 전력망 인프라 투자로 구리 부문 이익 비중 50% 돌파",
        "if_worst": "중국 조강 생산량 급감으로 철광석 가격 폭락",
        "kill_switch": "연간 배당수익률 3% 미만 축소 시"
    },
    "RGLD": {
        "name": "로열 골드 (Royal Gold)", "country": "US", "sector": "👑 금 광산 로열티 톨게이트 1위", "category": "power",
        "thesis": "광산 인건비, 채굴 비용 인플레이션 부담 0. 순수하게 금 매출의 일정 %를 걷는 순현금 제국",
        "if_best": "금값 온스당 $2,800+ 돌파 속 무차입 현금흐름 40% 증가 ➔ 배당귀족 랠리",
        "if_worst": "주요 계약 광산의 조업 영구 정지",
        "kill_switch": "로열티 편입 광산 수 순감소 시"
    },
    "RIG": {
        "name": "트랜스오션 (Transocean)", "country": "US", "sector": "🌊 심해 시추선(드릴십) 독점", "category": "power",
        "thesis": "수심 3,000m 초심해 7세대 고사양 드릴십 과점. 신규 건조 불가로 용선료 하루 50만 달러 돌파",
        "if_best": "브라질/가이아나 심해 유전 개발 붐 ➔ 100% 가동률 속 백로그 $100억 돌파",
        "if_worst": "유가 폭락으로 심해 시추 프로젝트 취소",
        "kill_switch": "평균 용선료(Dayrate) 30만 달러 미만으로 급락 시"
    },

    # ==========================================
    # 💳 [금융 거래소 / 결제망 / 데이터 톨게이트] (15)
    # ==========================================
    "V": {
        "name": "비자 (Visa)", "country": "US", "sector": "💳 글로벌 결제망 1위 톨게이트", "category": "finance",
        "thesis": "전 세계 40억 장 카드 결제 승인 통행세 독점. 영업이익률 55%의 인류 역사상 최강 비즈니스 모델",
        "if_best": "해외 여행 결제 볼륨 두 자릿수 성장 + B2B 기업 송금망 장악 ➔ 사상 최고가 경신",
        "if_worst": "미 법무부(DOJ)의 직불카드 반독점 소송 패소",
        "kill_switch": "연간 결제 처리 건수(Processed Transactions) 역성장 시"
    },
    "MA": {
        "name": "마스터카드 (Mastercard)", "country": "US", "sector": "💳 글로벌 결제망 듀오폴리 2위", "category": "finance",
        "thesis": "비자와 함께 글로벌 소비 결제 통행세 과점. 부가서비스(보안, 사기방지) 고성장",
        "if_best": "국경 간 거래(Cross-border) 수수료 급증 ➔ 연 15%+ EPS 성장 지속",
        "if_worst": "각국 정부의 신용카드 수수료 상한제 강제 도입",
        "kill_switch": "영업이익률 45% 미만 붕괴 시"
    },
    "CBOE": {
        "name": "Cboe 글로벌 마켓", "country": "US", "sector": "📈 변동성 지수(VIX) 및 옵션 독점", "category": "finance",
        "thesis": "VIX 지수 옵션 및 S&P 500 제로데이(0DTE) 옵션 거래 독점 거래소 (변동성 장세 최대 수혜)",
        "if_best": "미국 증시 변동성 폭발로 파생상품 일평균 거래량(ADV) 사상 최대 ➔ 수수료 잔치",
        "if_worst": "증시 초장기 저변동성 박스권 진입",
        "kill_switch": "독점 S&P500 옵션 거래량 30% 이상 급감 시"
    },
    "CME": {
        "name": "CME 그룹", "country": "US", "sector": "🌾 세계 최대 파생상품 거래소", "category": "finance",
        "thesis": "미 국채 금리, 원유, 농산물 선물 거래 독점 거래소. 금리 불확실성 시기 헤지 거래량 폭증",
        "if_best": "지정학적 리스크 + 금리 인하 경로 베팅으로 일일 거래 대금 사상 최대",
        "if_worst": "경쟁 대체 거래소(FMX 등)의 국채 선물 점유율 잠식",
        "kill_switch": "금리 선물 시장 점유율 85% 미만 하락 시"
    },
    "TW": {
        "name": "트레이드웹 (Tradeweb)", "country": "US", "sector": "💻 채권 전자거래 플랫폼 1위", "category": "finance",
        "thesis": "글로벌 기관투자가들의 국채, 회사채 장외거래를 전자거래로 전환 독점 (마진 50%+)",
        "if_best": "글로벌 국채 전자화 침투율 50% 돌파 ➔ 거래 수수료 폭발",
        "if_worst": "채권 거래 시장 유동성 급랭",
        "kill_switch": "평균 수수료율(Fee per million) 2분기 연속 하락 시"
    },
    "BLK": {
        "name": "블랙록 (BlackRock)", "country": "US", "sector": "🏛️ 세계 1위 자산운용 & 알라딘 SaaS", "category": "finance",
        "thesis": "운용자산 $11조 돌파 + 월가 전 금융기관이 리스크 관리에 쓰는 알라딘(Aladdin) 소프트웨어 독점",
        "if_best": "비트코인 현물 ETF 및 인프라 사모펀드 자금 유입 폭발 ➔ AUM 사상 최대",
        "if_worst": "글로벌 금융위기 발 자산가치 폭락",
        "kill_switch": "분기 순자금 유출(Net Outflow) 발생 시"
    },
    "TROW": {
        "name": "T. 로우 프라이스", "country": "US", "sector": "💼 무차입 37년 배당귀족 자산운용", "category": "finance",
        "thesis": "부채비율 0%, 37년 연속 배당 증액. 퇴직연금(401k) 타깃데이트펀드(TDF) 1위 독점망",
        "if_best": "미국 퇴직연금 자금 지속 유입 + 증시 반등 ➔ P/E 15배 밸류 리레이팅",
        "if_worst": "패시브 인덱스 ETF로의 자금 유출 가속",
        "kill_switch": "37년 배당 삭감 또는 동결 공시 시"
    },
    "FDS": {
        "name": "팩트셋 (FactSet)", "country": "US", "sector": "📊 월가 금융 데이터 터미널 듀오폴리", "category": "finance",
        "thesis": "블룸버그와 함께 글로벌 자산운용사, IB 필수 분석 터미널 과점. 갱신율 95%+ 영구 락인",
        "if_best": "AI 금융 분석 툴 탑재로 시트당 단가 15% 인상 반영",
        "if_worst": "월가 금융권 대규모 구조조정 및 시트 해지",
        "kill_switch": "연간 반복 매출(ASV) 마이너스 전환 시"
    },
    "CSU.TO": {
        "name": "컨스텔레이션 소프트웨어", "country": "CA", "sector": "🏢 수직시장 SaaS M&A 복리 제국", "category": "finance",
        "thesis": "북미 틈새 독점 소프트웨어 500개 인수 통합. 지난 15년간 30배 상승, FCF 재투자 영구 기관",
        "if_best": "대형 VMS 소프트웨어 기업 저가 인수 성공 ➔ 연 복리 25% FCF 창출 지속",
        "if_worst": "인수 대상 기업 고갈 및 밸류에이션 과열",
        "kill_switch": "인수 후 투하자본이익률(ROIC) 15% 미만 하락 시"
    },
    "INFY": {
        "name": "인포시스 (Infosys)", "country": "IN", "sector": "💻 인도 1위 IT 아웃소싱 톨게이트", "category": "finance",
        "thesis": "포춘 500대 글로벌 기업 전산망 아웃소싱 1위. 무차입, 높은 FCF 창출 및 안정적 배당",
        "if_best": "엔터프라이즈 AI 시스템 구축 프로젝트 대형 수주 ➔ 달러 매출 15% 성장",
        "if_worst": "미국/유럽 기업들의 IT 컨설팅 예산 삭감",
        "kill_switch": "영업이익률 18% 미만 하락 시"
    },
    "EVR": {
        "name": "에버코어 (Evercore)", "country": "US", "sector": "🤝 글로벌 M&A 부티크 자문 1위", "category": "finance",
        "thesis": "자기자본 투자 리스크 없이 순수 기업 M&A 및 구조조정 자문 수수료만 챙기는 고마진 모델",
        "if_best": "글로벌 빅딜 M&A 사이클 부활 ➔ 자문 수수료 사상 최대 비트",
        "if_worst": "고금리 지속으로 기업 인수합병 시장 동결",
        "kill_switch": "분기 영업적자 발생 시"
    },
    "SEIC": {
        "name": "SEI 인베스트먼트", "country": "US", "sector": "💼 프라이빗 뱅킹 자산관리 솔루션", "category": "finance",
        "thesis": "글로벌 PB, 패밀리오피스 백오피스 처리 전산망 1위. 무부채 현금 부자 톨게이트",
        "if_best": "글로벌 고액자산가 자금 유입 속 수수료율 인상",
        "if_worst": "고객사 전산 시스템 자체 구축 이탈",
        "kill_switch": "순이익률 15% 미만 하락 시"
    },
    "RJF": {
        "name": "레이몬드 제임스", "country": "US", "sector": "🏦 독립계 WM 자산관리 네트워크 1위", "category": "finance",
        "thesis": "미국 독립 자산관리사(FA) 네트워크 1위. 안정적 예대마진 및 수수료 기반 보수적 포트폴리오",
        "if_best": "월가 대형사 이탈 FA 대거 영입 ➔ 관리 자산(AUM) 사상 최대",
        "if_worst": "상업용 부동산 대출 부실화",
        "kill_switch": "대손충당금 급증으로 분기 적자 시"
    },
    "ROOT": {
        "name": "루트 (Root, Inc.)", "country": "US", "sector": "🚗 텔레매틱스 인슈어테크 흑자전환", "category": "finance",
        "thesis": "카바나(CVNA) 제휴로 마케팅비(CAC) 0원화 + 운전습관 데이터 기반 손해율 극적 개선",
        "if_best": "흑자 전환 후 전국 침투율 2배 확대 ➔ S&P 500 편입 랠리",
        "if_worst": "자동차 사고율 급증으로 손해율 80% 돌파",
        "kill_switch": "합산비율(Combined Ratio) 105% 초과 지속 시"
    },
    "DECK": {
        "name": "덱커스 (Deckers Outdoor)", "country": "US", "sector": "👟 호카(HOKA) + 어그(UGG) 챔피언", "category": "finance",
        "thesis": "러닝화 패러다임을 바꾼 호카(HOKA)와 겨울 필수재 어그(UGG) 보유. 무차입 순현금, P/E 11배 바닥",
        "if_best": "호카 글로벌 시장(유럽/아시아) 침투율 30% 돌파 ➔ 영업마진 23% 지속",
        "if_worst": "나이키의 러닝화 반격 및 온러닝과의 출혈 경쟁",
        "kill_switch": "호카 분기 매출 성장률 10% 미만으로 급락 시"
    },

    # ==========================================
    # 🧂 [음식료 / 생활필수재 / 장인 소비재] (10)
    # ==========================================
    "MKC": {
        "name": "맥코믹 (McCormick & Co.)", "country": "US", "sector": "🧂 글로벌 1위 향신료/소스 독점", "category": "food",
        "thesis": "전 세계 향신료, 머스타드(French's), 핫소스(Cholula) 독점 + 글로벌 프랜차이즈 B2B 주방 장악 (37년 배당귀족)",
        "if_best": "원가 안정 + 핫소스/시즈닝 글로벌 판매 회복 ➔ P/E 20배 리레이팅 (+45%)",
        "if_worst": "저가 PB 상품으로의 소비자 영구 이탈",
        "kill_switch": "영업이익률 12% 미만 붕괴 또는 37년 배당 삭감 시"
    },
    "003230.KS": {
        "name": "삼양식품", "country": "KR", "sector": "🍜 불닭볶음면 글로벌 K-푸드 독점", "category": "food",
        "thesis": "전 세계 매운맛 라면 시장의 컬트적 독점 브랜드. 수출 비중 80%+, 영업이익률 18~20% 글로벌 1위",
        "if_best": "밀양 2공장 완공으로 미국/유럽 월마트 입점 물량 2배 확대 ➔ 사상 최대 실적",
        "if_worst": "해외 각국의 라면 나트륨/위생 비관세 장벽 도입",
        "kill_switch": "분기 해외 수출액 역성장 전환 시"
    },
    "271560.KS": {
        "name": "오리온", "country": "KR", "sector": "🥧 초코파이 글로벌 제과 1위", "category": "food",
        "thesis": "중국, 베트남, 러시아 파이/스낵 시장 압도적 1위 독점. 영업이익률 16%, 부채비율 30%대 순현금 제국",
        "if_best": "인도 법인 본격 가동 + 바이오 신사업 안착 ➔ 밸류에이션 P/E 18배 복귀",
        "if_worst": "지정학적 갈등으로 러시아/중국 법인 자산 동결",
        "kill_switch": "영업이익률 12% 미만 하락 시"
    },
    "7309.T": {
        "name": "시마노 (Shimano)", "country": "JP", "sector": "🚲 전 세계 자전거 구동계 70%+ 독점", "category": "food",
        "thesis": "고급 로드/산악 자전거 변속기, 브레이크 70%+ 영구 독점. 무차입 순현금 자산 수조 원",
        "if_best": "유럽 전기자전거(E-Bike) 모터/구동계 점유율 1위 장악 ➔ 실적 턴어라운드",
        "if_worst": "코로나 특수 이후 글로벌 자전거 완제품 재고 소진 지연",
        "kill_switch": "영업이익률 10% 미만 하락 시"
    },
    "MNST": {
        "name": "몬스터 베버리지", "country": "US", "sector": "⚡ 글로벌 에너지 드링크 1위", "category": "food",
        "thesis": "레드불과 함께 에너지 음료 시장 양분. 코카콜라 글로벌 병입 유통망 독점 활용 (영업마진 28%)",
        "if_best": "무설탕 라인업 및 신흥국(인도/동남아) 판매 폭증 ➔ EPS 연 15% 성장",
        "if_worst": "고카페인 음료 청소년 판매 규제 법안",
        "kill_switch": "에너지 음료 시장 점유율 3%p 이상 순감소 시"
    },
    "COCO": {
        "name": "비타 코코 (The Vita Coco)", "country": "US", "sector": "🥥 북미 코코넛워터 1위 독점", "category": "food",
        "thesis": "북미 코코넛 워터 시장 점유율 50%+ 독점. 무차입, 음료 업계 최고의 FCF 전환율",
        "if_best": "스포츠 음료 및 칵테일 믹서 시장 침투 ➔ 연 20%+ 매출 성장",
        "if_worst": "동남아 코코넛 원자재 작황 악화 및 해상 운임 폭등",
        "kill_switch": "총마진(Gross Margin) 30% 미만 붕괴 시"
    },
    "CASY": {
        "name": "케이시스 제너럴 (Casey's)", "country": "US", "sector": "🍕 미국 시골 도로 피자/편의점 독점", "category": "food",
        "thesis": "인구 5,000명 이하 미국 중서부 시골 도로의 유일한 식당이자 주유소. 25년 연속 배당 증액",
        "if_best": "자체 수제 피자 마진 확대 + 경쟁 영세 주유소 인수 합병 ➔ 두 자릿수 EPS 복리 성장",
        "if_worst": "전기차 보급 급증으로 시골 주유소 방문객 급감",
        "kill_switch": "동일 점포 매출 성장률(SSSG) 마이너스 전환 시"
    },
    "ADM": {
        "name": "아처 대니얼스 미들랜드", "country": "US", "sector": "🌾 세계 4대 곡물 메이저 독점 (ABCD)", "category": "food",
        "thesis": "전 세계 곡물 운송선, 사일로 창고, 농산물 가공 인프라 독점 (50년 연속 배당귀족)",
        "if_best": "글로벌 식량 안보 위기 속 곡물 가공 스프레드 확대 ➔ P/E 15배 복귀",
        "if_worst": "영양 부문 회계 조사 리스크 장기화",
        "kill_switch": "50년 배당 삭감 또는 이익 적자 전환 시"
    },
    "CF": {
        "name": "CF 인더스트리즈", "country": "US", "sector": "🌱 질소 비료 북미 1위 독점", "category": "food",
        "thesis": "미국 저렴한 셰일가스로 질소 비료 생산. 유럽/러시아 대비 압도적 원가 우위, P/FCF 8배",
        "if_best": "글로벌 식량 파종 면적 확대로 비료 가격 폭등 ➔ 자사주 15% 일괄 소각",
        "if_worst": "미국 천연가스 가격 폭등으로 제조원가 상승",
        "kill_switch": "분기 FCF 적자 전환 시"
    },
    "DE": {
        "name": "디어 앤 컴퍼니 (John Deere)", "country": "US", "sector": "🚜 스마트 농기계 1위 독점", "category": "food",
        "thesis": "전 세계 1위 트랙터 독점 및 AI 자율주행 정밀농업 선도. 대체 불가한 농업 인프라",
        "if_best": "농기계 자율주행 구독 소프트웨어 매출 확대 ➔ 영업이익률 22% 돌파",
        "if_worst": "농산물 가격 급락으로 농부들의 트랙터 교체 연기",
        "kill_switch": "농업 장비 부문 매출 20% 이상 급감 시"
    },

    # ==========================================
    # 🛡️ [우주 방산 / 통신 톨게이트] (10)
    # ==========================================
    "KTOS": {
        "name": "크라토스 (Kratos)", "country": "US", "sector": "🛰️ 위성 지상 관제 소프트웨어 1위", "category": "defense",
        "thesis": "전 세계 인공위성 80%가 경유하는 지상국 오픈스페이스(OpenSpace) 소프트웨어 독점",
        "if_best": "미 우주군 차세대 지상 관제 시스템 및 발키리 무인 스텔스기 양산 수주",
        "if_worst": "미 국방부 무인기 예산 삭감",
        "kill_switch": "우주 지상국 부문 매출 역성장 시"
    },
    "LHX": {
        "name": "L3해리스 (L3Harris)", "country": "US", "sector": "📡 방산 전술통신 / 전자전 1위", "category": "defense",
        "thesis": "미 국방부 전술 무전기, 군용 위성 통신, 로켓 모터(에어로젯) 1위 독점 톨게이트",
        "if_best": "글로벌 전자전 장비 및 미사일 로켓 모터 수주잔고 사상 최대 경신",
        "if_worst": "에어로젯 합병 후 부채 상환 지연",
        "kill_switch": "분기 잉여현금흐름 적자 전환 시"
    },
    "NOC": {
        "name": "노스롭 그루먼", "country": "US", "sector": "🦅 B-21 차세대 스텔스 폭격기 독점", "category": "defense",
        "thesis": "미 공군 B-21 레이더 스텔스 폭격기 100% 독점 생산 및 핵 억제력 대륙간탄도미사일(ICBM)",
        "if_best": "B-21 조기 실전 배치 + 동맹국 수주 ➔ 안정적 코스트플러스 마진 확보",
        "if_worst": "미 국방부 고정가 계약 초과 비용 발생",
        "kill_switch": "항공 부문 영업이익률 6% 미만 붕괴 시"
    },
    "GD": {
        "name": "제너럴 다이내믹스", "country": "US", "sector": "⚓ 원자력 잠수함 & 걸프스트림 제트기", "category": "defense",
        "thesis": "미 해군 버지니아/컬럼비아급 핵잠수함 독점 건조 + 초고마진 걸프스트림 비즈니스 제트기",
        "if_best": "신형 G700 제트기 인도 폭증 + 핵잠수함 조기 인도 인센티브 획득",
        "if_worst": "잠수함 건조 숙련 조선 인력난 장기화",
        "kill_switch": "해양 부문 영업이익률 5% 미만 하락 시"
    },
    "EME": {
        "name": "EMCOR 그룹", "country": "US", "sector": "⚡ 첨단 팹/데이터센터 특수 전기 시공 1위", "category": "defense",
        "thesis": "반도체 클린룸, 제약 공장, AI 데이터센터 특수 전기·기계 시공 1위 (수주 백로그 사상 최대)",
        "if_best": "첨단 팹 착공 폭증 속 시공 단가 인상 ➔ 연 EPS 25% 성장",
        "if_worst": "글로벌 메가 팹 완공 연기",
        "kill_switch": "수주잔고 2분기 연속 감소 시"
    },
    "IESC": {
        "name": "IES 홀딩스", "country": "US", "sector": "🔌 데이터센터 전력 배선/인프라 1위", "category": "defense",
        "thesis": "빅테크 하이퍼스케일 데이터센터 전력망 내부 배선 및 주거용 전기 시공 1등 고성장주",
        "if_best": "데이터센터 부문 매출 50% 성장 ➔ 전고점 탈환 (+100%)",
        "if_worst": "미국 주택 경기 침체로 주거 부문 마진 악화",
        "kill_switch": "통합 영업이익률 8% 미만 하락 시"
    },
    "DOX": {
        "name": "암독스 (Amdocs)", "country": "US", "sector": "📱 글로벌 통신사 과금/빌링 1위 독점", "category": "defense",
        "thesis": "AT&T, T모바일 등 전 세계 주요 통신사의 빌링 결제 소프트웨어 독점 (전환 비용 극상, Fwd P/E 7배)",
        "if_best": "5G/클라우드 빌링 전환 가속 ➔ 연 FCF 7억 달러+ 창출 및 대규모 자사주 소각",
        "if_worst": "핵심 통신 고객사의 자체 전산 개발",
        "kill_switch": "분기 반복 매출(12개월 수주잔고) 순감소 시"
    },
    "ZBRA": {
        "name": "제브라 테크놀로지스", "country": "US", "sector": "🏷️ 산업용 바코드/RFID 스캐너 독점", "category": "defense",
        "thesis": "아마존, 페덱스, 월마트 물류센터 필수재인 바코드 스캐너, 산업용 모바일 컴퓨터 글로벌 1위",
        "if_best": "글로벌 전자상거래 물류 자동화 투자 재개 ➔ 영업이익 40% 회복",
        "if_worst": "물류 기업들의 모바일 기기 교체 연기",
        "kill_switch": "영업이익률 12% 미만 붕괴 시"
    },
    "YOU": {
        "name": "클리어 시큐어 (Clear Secure)", "country": "US", "sector": "🛫 공항 생체인식 패스트트랙 독점", "category": "defense",
        "thesis": "미국 주요 공항 보안검색대 생체인식 패스트트랙(CLEAR) 독점 운영. 멤버십 구독 기반 FCF 제국",
        "if_best": "공항 외 경기장, 의료기관 본인인증 침투 ➔ 잉여현금흐름 연 30% 성장",
        "if_worst": "TSA(미 교통안전청)의 자체 무료 생체인식 전면 보급",
        "kill_switch": "활성 회원 수(Active Members) 순감소 시"
    },
    "ZWS": {
        "name": "전 엘케이 (Zurn Elkay)", "country": "US", "sector": "🚰 상업용 식수대/음수대 1위 독점", "category": "defense",
        "thesis": "미국 학교, 병원, 공항에 설치되는 필터 식수대(Elkay) 및 상업용 절수 배관 독점 톨게이트",
        "if_best": "미국 공립학교 납/유해물질 정화 식수대 교체 의무화 법안 ➔ 독점 수주",
        "if_worst": "상업용 건축 신축 허가 급감",
        "kill_switch": "자유현금흐름(FCF) 적자 전환 시"
    }
}
