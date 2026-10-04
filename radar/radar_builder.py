import urllib.request
import json
import os
import datetime
import sys

# Windows 콘솔 인코딩 호환
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 🎯 종목 레이더 감시 풀 (전 종목 EPS > 0 흑자 검증 및 독점적 해자 보유)
WATCHLIST = {
    # ==========================================
    # 💻 [테크 / AI 반도체 / 엔터프라이즈 SaaS]
    # ==========================================
    "NVDA": {
        "name": "엔비디아 (NVIDIA)",
        "sector": "💻 AI 가속기 & CUDA 독점",
        "tag": "AI 황제",
        "category": "tech",
        "thesis": "전 세계 AI 가속기 시장 90%+ 장악 및 CUDA 소프트웨어 생태계 락인",
        "special_issue": "블랙웰 아키텍처 본격 양산 국면. 빅테크 CAPEX 지속 속 밸류에이션(Fwd P/E 15배, PEG 0.23) 안전마진 확보",
        "if_best": "블랙웰 울트라 공급 폭증 + 추론용 수요 폭발 ➔ 전고점 돌파 랠리",
        "if_worst": "빅테크 AI 데이터센터 투자(CAPEX) 급격한 동결 및 공급망 차질",
        "kill_switch": "데이터센터 부문 분기 매출 전분기 대비 15% 이상 역성장 시"
    },
    "AVGO": {
        "name": "브로드컴 (Broadcom)",
        "sector": "💻 커스텀 AI ASIC & 스위칭",
        "tag": "ASIC 1등",
        "category": "tech",
        "thesis": "구글 TPU, 메타 MTIA 맞춤형 AI 칩 설계 1위 + 토마호크 통신 스위칭 독점",
        "special_issue": "VMware 구독 모델 전환으로 FCF 폭발. Fwd P/E 18.4배, PEG 0.28 저평가 구간",
        "if_best": "빅테크 자체 ASIC 채택률 50%+ 돌파 ➔ 연 FCF 300억 달러+ 창출",
        "if_worst": "VMware 핵심 대기업 고객사 오픈소스 이탈 가속",
        "kill_switch": "반도체 솔루션 영업이익률 30% 붕괴 시"
    },
    "SNPS": {
        "name": "시놉시스 (Synopsys)",
        "sector": "🧠 반도체 설계 EDA 툴 1위",
        "tag": "설계 소프트웨어",
        "category": "tech",
        "thesis": "2nm/3nm 칩 설계 시 절대 대체 불가한 전자설계자동화(EDA) 글로벌 과점",
        "special_issue": "앤시스(Ansys) 대형 인수로 시뮬레이션 통합. 최근 기술주 조정으로 매력적 밸류 도달",
        "if_best": "AI 칩 설계 붐으로 EDA 라이선스 계약 단가 폭증 ➔ 전고점 회복 (+30%)",
        "if_worst": "각국 반독점 규제 당국의 앤시스 합병 불허",
        "kill_switch": "분기 반복 라이선스 매출(ARR) 순감소 시"
    },
    "CDNS": {
        "name": "케이던스 (Cadence)",
        "sector": "🧠 반도체 EDA 소프트웨어 과점",
        "tag": "반도체 필수재",
        "category": "tech",
        "thesis": "시놉시스와 함께 전 세계 칩 설계를 양분하는 과점 소프트웨어 제국",
        "special_issue": "자율주행, AI, 모바일 칩 복잡도 증가로 R&D 필수 소프트웨어 락인 심화",
        "if_best": "파운드리 2나노 공정 전환 가속 ➔ EDA 툴 사용료 30% 인상 반영",
        "if_worst": "글로벌 팹리스 스타트업들의 R&D 예산 삭감",
        "kill_switch": "영업현금흐름(OCF) 마진 30% 미만 하락 시"
    },
    "KLAC": {
        "name": "KLA 코퍼레이션",
        "sector": "🔬 나노 미세 수율/계측 독점",
        "tag": "영업마진 40%",
        "category": "tech",
        "thesis": "웨이퍼 표면 미세 결함 및 광학 계측 글로벌 1위 독점 (대체재 0개)",
        "special_issue": "HBM 적층 및 파운드리 초미세 공정 수율을 잡기 위해 장비 발주 필수 지속",
        "if_best": "글로벌 파운드리 2나노 경쟁 심화 ➔ 계측 장비 수주 잔고 사상 최대",
        "if_worst": "대중국 첨단 반도체 장비 수출 통제 전면 확대",
        "kill_switch": "분기 영업이익률 30% 이하로 급락 시"
    },
    "AMAT": {
        "name": "어플라이드 머티어리얼즈",
        "sector": "⚙️ 반도체 전공정 장비 1위",
        "tag": "장비 제국",
        "category": "tech",
        "thesis": "증착, 식각, 이온주입 등 반도체 제조 전공정 세계 최대 포트폴리오 보유",
        "special_issue": "GAA(게이트올어라운드) 및 후면전력공급(BSPDN) 전환기 핵심 수혜",
        "if_best": "글로벌 반도체 팹 신설(IIJA/유럽) 본격 가동 ➔ 사상 최대 실적 비트",
        "if_worst": "글로벌 팹 완공 지연 및 장비 입고 연기",
        "kill_switch": "수주-출하 비율(Book-to-Bill) 0.90 미만 2분기 지속 시"
    },
    "INTU": {
        "name": "인튜이트 (Intuit)",
        "sector": "📊 세무 & 회계 SaaS 독점",
        "tag": "Fwd P/E 10배 바닥",
        "category": "tech",
        "thesis": "미국 개인 세무 신고(터보택스) + 3천만 중소기업 회계 장부(퀵북스) 100% 독점",
        "special_issue": "현재 Fwd P/E 10.7배, PEG 0.50 수준의 극단적 저평가 안전마진 타점",
        "if_best": "퀵북스 AI 자동장부 기능 안착 + 중소기업 ARPU 15% 상승 ➔ 주가 $400+ 복귀",
        "if_worst": "미 국세청(IRS)의 직접 무료 세무 신고(Direct File) 전면 의무화",
        "kill_switch": "터보택스 유료 이용자 수 10% 이상 순감소 시"
    },
    "ADBE": {
        "name": "어도비 (Adobe)",
        "sector": "🎨 크리에이티브 클라우드 독점",
        "tag": "AI 공포 과매도",
        "category": "tech",
        "thesis": "포토샵, 일러스트레이터, 프리미어 등 디지털 디자인 표준 툴 영구 락인",
        "special_issue": "생성형 AI 위협론 공포로 고점 대비 -40% 폭락. Fwd P/E 8.6배, PEG 0.58 바닥권",
        "if_best": "파이어플라이(Firefly) AI 엔터프라이즈 구독 폭증 ➔ P/E 20배 복귀 (+40% 익절)",
        "if_worst": "Canva, Midjourney 등 신생 AI 툴로 기업 고객 대량 이탈",
        "kill_switch": "기업용 디지털 미디어 ARR 순감소 공시 시"
    },
    "NOW": {
        "name": "서비스나우 (ServiceNow)",
        "sector": "🏢 전사 IT 워크플로우 1위",
        "tag": "포춘 500 필수 SaaS",
        "category": "tech",
        "thesis": "포춘 500대 기업 85%가 사용하는 IT 헬프데스크 및 업무 자동화 중앙 플랫폼",
        "special_issue": "AI 에이전트 도입으로 기업 생산성 혁신 주도. 갱신율(Renewal Rate) 98% 경이적 락인",
        "if_best": "엔터프라이즈 AI 플랫폼 계약 폭증 ➔ 연간 FCF 40억 달러+ 돌파",
        "if_worst": "빅테크(MS, Salesforce)와의 업무 영역 침범 경쟁 격화",
        "kill_switch": "순매출 유지율(NRR) 115% 미만 붕괴 시"
    },
    "COHR": {
        "name": "코히런트 (Coherent)",
        "sector": "⚡ AI 데이터센터 광트랜시버 1위",
        "tag": "800G 광통신 독점",
        "category": "tech",
        "thesis": "AI 클러스터 초고속 데이터 전송용 800G/1.6T 광트랜시버 핵심 부품 독점",
        "special_issue": "구리선 한계로 광통신 전환 필수화. PEG 0.48 수준의 고성장 대비 저평가",
        "if_best": "엔비디아/구글 차세대 광통신 모듈 독점 공급 ➔ 실적 서프라이즈 랠리",
        "if_worst": "경쟁사(Lumentum 등)의 저가 광트랜시버 시장 침투",
        "kill_switch": "광통신 부문 분기 수주잔고 순감소 시"
    },
    "FSLR": {
        "name": "퍼스트 솔라 (First Solar)",
        "sector": "☀️ 미국 대형 박막 태양광 독점",
        "tag": "IRA 수혜 저P/E 7배",
        "category": "tech",
        "thesis": "중국 실리콘 태양광 대신 미국 내 100% 제조되는 카드뮴-텔루라이드(CdTe) 박막 모듈 독점",
        "special_issue": "2027~2028년까지 수주 백로그 완판. Fwd P/E 7.5배, PEG 0.27 극단적 저평가",
        "if_best": "빅테크 데이터센터 전력 자가공급 태양광 대형 수주 ➔ 밸류 리레이팅 (+50%)",
        "if_worst": "미국 대선 이후 IRA 세액공제(45X) 폐지 또는 대폭 축소",
        "kill_switch": "IRA 제조 보조금 전면 폐지 입법 통과 시"
    },

    # ==========================================
    # 🏭 [산업재 / 데이터센터 냉각 / 필수 부품 / 톨게이트]
    # ==========================================
    "FIX": {
        "name": "컴포트 시스템즈 (Comfort Systems)",
        "sector": "❄️ AI 데이터센터 냉각/MEP 1위",
        "tag": "데이터센터 수혜 대장",
        "category": "infra",
        "thesis": "빅테크 AI 데이터센터의 액체냉각, HVAC 공조 및 모듈러 MEP 시공 압도적 1위",
        "special_issue": "수주 잔고 사상 최대 경신. 5년 EPS 성장률 47.8%, PEG 0.78 고성장 알짜",
        "if_best": "차세대 액체냉각 단가 인상 + 메가 데이터센터 착공 폭증 ➔ 전고점 돌파 (+30%)",
        "if_worst": "빅테크 AI 데이터센터 설비투자(CAPEX) 급격한 동결",
        "kill_switch": "수주-출하 비율(Book-to-Bill) 1.0 미만 2분기 연속 붕괴 시"
    },
    "HWM": {
        "name": "하우멧 에어로스페이스",
        "sector": "✈️ 제트엔진 터빈 블레이드 독점",
        "tag": "P/S 10배 괴물",
        "category": "infra",
        "thesis": "보잉/에어버스 제트엔진의 초고온 합금 터빈 블레이드 및 항공기 패스너 1등 독점",
        "special_issue": "민항기 인도 지연 해소 및 엔진 부품 교체 수요 폭증. 5년 EPS 성장률 50.8%",
        "if_best": "항공기 제작사 인도량 정상화 + 방산 전투기 엔진 수주 ➔ 마진 추가 확대",
        "if_worst": "티타늄 등 핵심 항공우주 원자재 공급망 단절",
        "kill_switch": "엔진 부문 영업이익률 20% 미만 하락 시"
    },
    "HEI": {
        "name": "하이코 (HEICO)",
        "sector": "✈️ FAA 승인 대체부품(PMA) 독점",
        "tag": "버핏 스타일 복리",
        "category": "infra",
        "thesis": "순정품 대비 30~50% 저렴한 FAA 승인 항공기 대체 부품 독점 공급자",
        "special_issue": "항공사들의 비용 절감 필수 파트너. 지난 30년간 연평균 복리 20%+ 우상향",
        "if_best": "글로벌 항공 여객 수요 증가 속 대체 부품 침투율 40% 돌파 ➔ 실적 점프",
        "if_worst": "PMA 대체 부품의 중대 품질 결함 이슈 발생",
        "kill_switch": "FAA의 핵심 부품 PMA 인가 취소 시"
    },
    "CPRT": {
        "name": "코파트 (Copart)",
        "sector": "🚗 전손차/사고차 경매 독점",
        "tag": "영업마진 40%",
        "category": "infra",
        "thesis": "미국 보험사고 전손 차량 온라인 경매 1위 독점 + 대도시 주변 토지 야드 인허가 해자",
        "special_issue": "차량 첨단화로 수리비 급증 ➔ 전손 처리율 상승 수혜. Fwd P/E 15.4배 밸류 매력",
        "if_best": "글로벌 바이어 네트워크 확대 속 수수료 인상 ➔ FCF 15억 달러+ 달성",
        "if_worst": "자동차 사고율의 구조적 급감 (자율주행 급진적 보급)",
        "kill_switch": "전손차 출품 대수 2분기 연속 10% 이상 감소 시"
    },
    "ULS": {
        "name": "UL 솔루션스 (UL Solutions)",
        "sector": "🏷️ 전자기기 안전규격 100% 독점",
        "tag": "UL 마크 통행세",
        "category": "infra",
        "thesis": "전 세계 전자기기, 배터리, 건축 자재에 찍히는 'UL 마크' 안전인증 독점 톨게이트",
        "special_issue": "EV 배터리, 신재생, AI 데이터센터 기기 안전 인증 필수화로 안정적 성장",
        "if_best": "글로벌 신제품 출시 붐 속 시험인증 수수료 매출 연 15% 성장",
        "if_worst": "유럽 CE 등 경쟁 인증 규격의 미국 시장 잠식",
        "kill_switch": "인증 부문 영업이익률 15% 미만 하락 시"
    },
    "CTAS": {
        "name": "신타스 (Cintas)",
        "sector": "👔 기업 유니폼 렌탈/세탁 1위",
        "tag": "트럭망 네트워크",
        "category": "infra",
        "thesis": "미국 기업 유니폼 렌탈 및 사업장 안전용품 배송 트럭망 독점",
        "special_issue": "고객 유지율 95%+의 무차입 현금흐름 제국. 경기 둔화기에도 가격 전가력 유지",
        "if_best": "신규 헬스케어/서비스업 유니폼 고객 침투 ➔ 40년 연속 배당 증액 랠리",
        "if_worst": "미국 실업률 급등으로 사업장 근무자 수 급감",
        "kill_switch": "유기적 매출 성장률 마이너스 전환 시"
    },
    "WM": {
        "name": "웨이스트 매니지먼트",
        "sector": "🗑️ 매립지 토지 독점",
        "tag": "북미 1위 인프라",
        "category": "infra",
        "thesis": "신규 인허가 불가한 북미 최대 매립지 영지 독점 + 매립가스 발전",
        "special_issue": "쓰레기 반입 수수료 인상으로 인플레이션 자동 전가. 안정적 FCF 창출",
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
    "XYL": {
        "name": "자일럼 (Xylem)",
        "sector": "💧 글로벌 수처리 펌프 1위",
        "tag": "상하수도 독점",
        "category": "infra",
        "thesis": "전 세계 상하수도, 해수담수화, 반도체 초순수 공급용 초고압 펌프·스마트 밸브 1위",
        "special_issue": "고금리 지자체 예산 집행 지연으로 고점 대비 -34% 급락 후 52주 바닥권 다지기",
        "if_best": "담수화 플랜트 + 반도체/AI 데이터센터 초순수 수주 본격화 ➔ 주가 $140+ 회복",
        "if_worst": "글로벌 경기 침체로 각국 지자체 인프라 개보수 예산 삭감",
        "kill_switch": "분기 수주잔고(Backlog) 순감소 2분기 연속 지속 시"
    },
    "ECL": {
        "name": "이콜랩 (Ecolab)",
        "sector": "💧 산업용 정수/멸균 1위",
        "tag": "빌게이츠 1대 주주",
        "category": "infra",
        "thesis": "전 세계 반도체 팹, 공장, 병원에서 물을 정화하고 재활용하는 특수 케미컬·소프트웨어 독점",
        "special_issue": "수자원 고갈 시대 필수 방어벽. 영업마진 꾸준히 개선 중",
        "if_best": "데이터센터 수냉식 냉각수 정수 및 공장 폐수 무방류(ZLD) 수요 폭증 ➔ 전고점 돌파",
        "if_worst": "원자재(기초화학) 가격 폭등으로 제조 마진 일시 축소",
        "kill_switch": "영업이익률 5%p 이상 급락 시"
    },
    "VMC": {
        "name": "벌컨 머티리얼즈",
        "sector": "🪨 골재/채석장 인허가 독점",
        "tag": "대체 불가 광산",
        "category": "infra",
        "thesis": "도로/건축용 모래·자갈 채석장 독점 (인허가 규제로 신규 채석장 개설 불가)",
        "special_issue": "무거운 골재 특성상 운송 반경 80km 내 지역 독점권 보유. 판가 매년 인상",
        "if_best": "미국 인프라 재건 및 공장 건설 붐 ➔ 골재 판가 10%+ 인상 전가",
        "if_worst": "건설 착공 급감으로 출하량 감소",
        "kill_switch": "골재 판매 톤당 마진 하락 전환 시"
    },
    "GNTX": {
        "name": "젠텍스 (Gentex)",
        "sector": "🪞 스마트 ECM 룸미러 90% 독점",
        "tag": "부품사 마진 20%",
        "category": "infra",
        "thesis": "글로벌 프리미엄 자동차 눈부심 방지(ECM) 및 디지털 룸미러 90% 독점",
        "special_issue": "부품사임에도 무차입 순현금 및 20%대 영업이익률. Fwd P/E 13배 저평가",
        "if_best": "자율주행용 실내 카메라/바이오센서 미러 채택 확대 ➔ 대당 매출 30% 증가",
        "if_worst": "완성차 업체들의 저가 일반 거울 다운그레이드",
        "kill_switch": "매출총이익률 30% 붕괴 시"
    },

    # ==========================================
    # 🏥 [헬스케어 / 100% 독점 치료제 & 수술실 지배자]
    # ==========================================
    "VRTX": {
        "name": "버텍스 파마슈티컬",
        "sector": "🧬 낭포성 섬유증 100% 독점",
        "tag": "순이익률 40%",
        "category": "health",
        "thesis": "치명적 유전병인 낭포성 섬유증(CF) 치료제 시장 전 세계 100% 독점",
        "special_issue": "대체재 0개. 비마약성 진통제(Suzetrigine) 승인 대기 속 FCF 복리 누적",
        "if_best": "비마약성 진통제 FDA 승인 잭팟 ➔ 주가 전고점 돌파 (+30%)",
        "if_worst": "경쟁사의 CF 복제약/대체 신약 임상 3상 성공 공시",
        "kill_switch": "경쟁사 낭포성 섬유증 대체 치료제 승인 시"
    },
    "ISRG": {
        "name": "인튜이티브 서지컬",
        "sector": "🦾 다빈치 수술 로봇 1등 독점",
        "tag": "면도날 모델",
        "category": "health",
        "thesis": "글로벌 복강경 수술 로봇 독점. 매출의 70%가 일회용 수술 도구 반복 매출",
        "special_issue": "최신 다빈치 5(DV5) 교체 사이클 본격화. 의사들의 기술 락인 극강",
        "if_best": "다빈치 5 병원 도입 가속 + 수술 건수 15%+ 성장 ➔ 사상 최고가 경신",
        "if_worst": "병원들의 의료장비 자본지출(CAPEX) 급격한 긴축",
        "kill_switch": "분기 수술 건수(Procedure Growth) 8% 미만 하락 시"
    },
    "IDXX": {
        "name": "아이덱스 랩스 (IDEXX)",
        "sector": "🐕 동물병원 진단 장비/시약 1위",
        "tag": "반려동물 비급여",
        "category": "health",
        "thesis": "전 세계 동물병원 임상 진단 장비 및 진단 시약 압도적 1위 독점",
        "special_issue": "정부 의료보험 통제 없는 비급여 반려동물 헬스케어의 영구적 캐시카우",
        "if_best": "글로벌 동물병원 진단 장비 설치 기반 확대 ➔ 고마진 시약 매출 폭증",
        "if_worst": "반려동물 입양 감소 및 진료 건수 감소",
        "kill_switch": "시약/소모품 반복 매출 성장률 5% 미만 둔화 시"
    },
    "WST": {
        "name": "웨스트 파마슈티컬",
        "sector": "💉 바이오 주사기 고무마개 70% 독점",
        "tag": "필수 패키징",
        "category": "health",
        "thesis": "바이오의약품, 인슐린, GLP-1 비만치료제 바이알 주사기 특수 고무마개 독점",
        "special_issue": "GLP-1 비만치료제 펜 주사기 수요 폭발의 숨은 병목이자 최대 수혜주",
        "if_best": "GLP-1 생산량 2배 확대 ➔ 고마진 특수 코팅 마개 출하량 폭증",
        "if_worst": "빅파마들의 재고 조정 장기화",
        "kill_switch": "고마진 프록스(HVP) 제품 비중 하락 시"
    },
    "RMD": {
        "name": "레스메드 (ResMed)",
        "sector": "💨 수면무호흡증 양압기(CPAP) 1위",
        "tag": "필립스 리콜 수혜",
        "category": "health",
        "thesis": "수면무호흡증 치료용 양압기 및 호흡기 마스크 글로벌 1위 독점사",
        "special_issue": "비만약 공포로 과매도 후 펀더멘털 증명하며 강력한 반등세 지속",
        "if_best": "GLP-1 복용자들의 수면무호흡 진단율 증가 ➔ 양압기 수요 동반 증가",
        "if_worst": "필립스의 양압기 시장 전면 재진입 및 가격 인하",
        "kill_switch": "시장 점유율 10%p 이상 잠식 시"
    },
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
    "DECK": {
        "name": "덱커스 (Deckers Outdoor)",
        "sector": "👟 호카(HOKA) + 어그(UGG) 챔피언",
        "tag": "Fwd P/E 9.5배 극단가치",
        "category": "health",
        "thesis": "나이키 점유율을 흡수하는 프리미엄 러닝화 호카 및 라이프스타일 어그 보유",
        "special_issue": "현재 Fwd P/E 9.5배 수준의 압도적 안전마진. 무차입 건전 대차대조표",
        "if_best": "호카 글로벌 유통망 확장 + 직영 D2C 마진 확대 ➔ 전고점 돌파 (+35%)",
        "if_worst": "러닝화 트렌드 급변으로 호카 브랜드 피로도 노출",
        "kill_switch": "호카 브랜드 매출 성장률 10% 미만 급랭 시"
    },
    "ROOT": {
        "name": "루트 (Root, Inc.)",
        "sector": "🚗 텔레매틱스 인슈어테크",
        "tag": "스페셜 시츄에이션",
        "category": "health",
        "thesis": "카바나(CVNA) 독점 제휴로 마케팅비(CAC) 0원화 + Low Float 수급 탄성",
        "special_issue": "흑자 전환 후 카바나 판매량 연동 성장. 고점 대비 과매도 구간",
        "if_best": "카바나 임베디드 판매 호조 + 숏스퀴즈 ➔ 주가 $65~$70 수직 반등",
        "if_worst": "카바나 판매 둔화 및 손해율(MLR) 악화로 분기 적자 재발",
        "kill_switch": "카바나 제휴 해지 공시 또는 합산손해율 105% 초과 시"
    },

    # ==========================================
    # ⚡ [원자력 / 전력망 / 셰일 로열티 / 에너지]
    # ==========================================
    "CEG": {
        "name": "컨스텔레이션 에너지",
        "sector": "☢️ 미국 1위 원자력 발전 독점",
        "tag": "MSFT 20년 PPA 독점",
        "category": "power",
        "thesis": "미국 최대 무탄소 원전 가동사 (마이크로소프트 20년 전력구매계약 독점)",
        "special_issue": "빅테크 AI 데이터센터 전력 쇼티지의 최대 수혜주. PEG 0.90 고성장",
        "if_best": "추가 원자로 재가동 및 빅테크 20년 장기 PPA 추가 수주 ➔ 사상 최고가",
        "if_worst": "노후 원자로 중대 결함 또는 FERC의 전력망 직결 규제",
        "kill_switch": "FERC의 데이터센터 원전 전력망 직결 영구 금지 판결 시"
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
    "VNOM": {
        "name": "바이퍼 에너지 (Viper)",
        "sector": "🛢️ 셰일 시추비 0원 로열티 독점",
        "tag": "석유계 비자카드",
        "category": "power",
        "thesis": "시추 비용 부담 0원으로 퍼미안 분지 원유 생산량의 15~25% 로열티만 현금 징수",
        "special_issue": "P/FCF 9.7배, 부채비율 0.2미만. 유가 하락에도 파산 리스크 0",
        "if_best": "유가 $80+ 회귀 + 시추량 증가 ➔ 배당 및 자사주 소각 극대화 (+30%)",
        "if_worst": "OPEC+ 치킨게임 장기화로 유가 $50 이하 폭락",
        "kill_switch": "모회사(다이아몬드백)의 퍼미안 시추 리그 50% 이상 철수 시"
    },
    "WHD": {
        "name": "선인장 (Cactus)",
        "sector": "🛢️ 유전 웰헤드 안전장비 독점",
        "tag": "5년 EPS 27% 성장",
        "category": "power",
        "thesis": "셰일 유전 시추 시 폭발을 방지하는 안전 웰헤드(Wellhead) 시장 1위 독점",
        "special_issue": "무차입 대차대조표에 Fwd P/E 17배 수준의 견고한 펀더멘털",
        "if_best": "미국 셰일 가동 리그 수 반등 ➔ 웰헤드 출하량 및 마진 급증",
        "if_worst": "원유 시추 활동 급격한 침체",
        "kill_switch": "분기 FCF 적자 전환 시"
    },
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

    # ==========================================
    # 🏛️ [금융 / 자본시장 무차입 톨게이트]
    # ==========================================
    "CBOE": {
        "name": "Cboe 글로벌 마켓",
        "sector": "🏛️ 공포지수(VIX) & 옵션 독점",
        "tag": "폭락장 헤지 자산",
        "category": "finance",
        "thesis": "공포지수(VIX) 선물 및 S&P 500 지수 옵션(SPX) 독점 톨게이트",
        "special_issue": "대출 부실 리스크 0원. 시장 폭락 시 변동성 수수료 폭발 수혜",
        "if_best": "매크로 충격으로 VIX 폭등 ➔ 사상 최대 거래 수수료 창출 (+35%)",
        "if_worst": "초장기 저변동성 평화 장세 지속으로 옵션 거래량 감소",
        "kill_switch": "경쟁 거래소의 대체 변동성 상품 시장 점유율 20% 잠식 시"
    },
    "CME": {
        "name": "CME 그룹",
        "sector": "🏛️ 세계 1위 파생상품 거래소",
        "tag": "원자재/금리 선물",
        "category": "finance",
        "thesis": "원유, 금, 국채, 통화, 농산물 글로벌 1위 선물/옵션 거래소 독점",
        "special_issue": "영업이익률 60%에 달하는 현금인출기. 변동성 장세마다 배당 증액",
        "if_best": "금리 변동성 및 원자재 슈퍼사이클 ➔ 계약 거래량 사상 최대",
        "if_worst": "장외(OTC) 거래 플랫폼으로의 기관 자금 이탈",
        "kill_switch": "평균 일일 거래량(ADV) 15% 이상 지속 감소 시"
    },
    "TW": {
        "name": "트레이드웹 (Tradeweb)",
        "sector": "🏛️ 미국 국채 전자거래 1위",
        "tag": "채권 핀테크",
        "category": "finance",
        "thesis": "글로벌 기관 투자자들의 미국 국채, 모기지 채권 전자 거래 1등 플랫폼",
        "special_issue": "미국 재정적자로 국채 발행량 폭증 ➔ 거래 수수료 매출 자동 수혜",
        "if_best": "채권 시장 전자화 침투율 60% 돌파 ➔ 연 20% 고성장 지속",
        "if_worst": "채권 시장 유동성 고갈 및 발행량 급감",
        "kill_switch": "분기 거래 수수료 마진 5%p 이상 하락 시"
    },
    "BLK": {
        "name": "블랙록 (BlackRock)",
        "sector": "🏛️ 세계 1위 자산운용 & 알라딘",
        "tag": "10조 달러 거인",
        "category": "finance",
        "thesis": "10조 달러 iShares ETF 수수료 + 금융기관 필수 리스크관리 SaaS(알라딘)",
        "special_issue": "글로벌 패시브 자금 유입과 사모 자산(Private Credit) 확장 가속",
        "if_best": "글로벌 증시 랠리 속 AUM 12조 달러 돌파 ➔ 수수료 레버리지 폭발",
        "if_worst": "글로벌 금융위기로 인한 AUM 급감 및 운용보수 하락",
        "kill_switch": "분기 순유입 자금(Net Flows) 순유출 전환 시"
    },

    # ==========================================
    # 🌊 [자원 / 광산 / 심해 에너지]
    # ==========================================
    "RGLD": {
        "name": "로열 골드 (Royal Gold)",
        "sector": "⛏️ 금광 로열티/스트리밍 1위",
        "tag": "마진 50% 금 SaaS",
        "category": "ocean",
        "thesis": "직접 땅 파지 않고 광산 개발 자금 대주고 금 생산량 5~10% 영구 수취",
        "special_issue": "곡괭이/인건비 부담 0원. 금값 상승 시 영업마진 50%+ 복리 향유",
        "if_best": "금 온스당 $3,000+ 돌파 ➔ 잉여현금흐름 폭발 및 배당 증액",
        "if_worst": "핵심 로열티 계약 광산의 지정학적 국유화 또는 폐광",
        "kill_switch": "핵심 광산 생산 중단 또는 금 가격 $1,800 이하 급락 시"
    },
    "SCCO": {
        "name": "서던 코퍼 (Southern Copper)",
        "sector": "🥉 세계 최저 원가 구리 독점",
        "tag": "순이익률 40%",
        "category": "ocean",
        "thesis": "부산물(몰리브덴/은) 크레딧으로 파운드당 구리 생산 원가가 글로벌 최저 수준",
        "special_issue": "AI 데이터센터 및 전력망 구리 쇼티지의 최대 수혜자. 엔비디아급 순이익률",
        "if_best": "구리 파운드당 $5+ 안착 ➔ 주당 배당금 사상 최대 지급",
        "if_worst": "페루/멕시코 정부의 광산 특별세 인상 또는 파업",
        "kill_switch": "구리 현물 가격 파운드당 $3.20 이하 급락 시"
    },
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

    # ==========================================
    # 🌾 [식량 / 중독성 소비재 / 필수 유통]
    # ==========================================
    "MNST": {
        "name": "몬스터 베버리지",
        "sector": "⚡ 에너지 음료 제국",
        "tag": "음료계의 SaaS",
        "category": "food",
        "thesis": "공장 소유 없이 코카콜라 글로벌 배송망에 원액만 얹어 무차입 마진 30% 창출",
        "special_issue": "Z세대 충성도 극강. 밸류에이션 조정 시 강력한 자사주 매입 하방 지지",
        "if_best": "글로벌 신흥국 시장 점유율 40% 돌파 ➔ 30년 복리 우상향 재현",
        "if_worst": "카페인 음료 규제 및 신흥 에너지 음료(셀시어스 등) 추격",
        "kill_switch": "글로벌 매출총이익률 50% 붕괴 시"
    },
    "COCO": {
        "name": "비타 코코 (The Vita Coco)",
        "sector": "🥥 코코넛 워터 독점 1위",
        "tag": "점유율 50%+",
        "category": "food",
        "thesis": "미국 코코넛 워터 시장 점유율 50%+ 1등 독점. 무차입 클린 대차대조표",
        "special_issue": "건강 음료 트렌드와 칵테일 믹서 수요로 고성장. Fwd P/E 18배",
        "if_best": "원자재(해상운임) 안정화 속 유럽/아시아 수출 폭증 ➔ 전고점 돌파",
        "if_worst": "글로벌 컨테이너 해상 운임 폭등으로 운송 마진 잠식",
        "kill_switch": "코코넛 워터 시장 점유율 40% 미만 하락 시"
    },
    "CASY": {
        "name": "케이시스 (Casey's)",
        "sector": "🍕 시골 읍내 독점 편의점",
        "tag": "미국 5대 피자 체인",
        "category": "food",
        "thesis": "미국 중서부 인구 5천 명 이하 시골 마을의 유일한 피자집+주유소+편의점",
        "special_issue": "시골 상권 독점으로 경기 불황 무풍지대. FCF 재투자로 매장 확장 지속",
        "if_best": "M&A 편의점 인수 통합 + 즉석식품 마진 확대 ➔ EPS 연 15% 성장",
        "if_worst": "농촌 지역 인구 급감 및 가솔린 마진 축소",
        "kill_switch": "동일매장 매출 성장률(SSSG) 마이너스 전환 시"
    },
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

    # ==========================================
    # 🛡️ [우주 방산 / 지상국 관제 / 전술 통신]
    # ==========================================
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
        "sector": "🛡️ 방산 통신 / 로켓 모터 1위",
        "tag": "군용 전술통신",
        "category": "defense",
        "thesis": "미 국방부 전술 라디오 및 에어로젯 로켓다인 미사일 로켓 모터 독점",
        "special_issue": "신냉전 국방비 증액 속 FCF 25억 달러+ 창출 궤도 안착",
        "if_best": "전술 통신 + 고체 로켓 모터 주문 폭주 ➔ 주가 전고점 돌파",
        "if_worst": "로켓 모터 생산 지연에 따른 납기 페널티",
        "kill_switch": "영업이익률 10% 미만 하락 시"
    }
}

# 14일 RSI 순수 파이썬 계산 함수
def compute_rsi(closes, period=14):
    valid = [c for c in closes if c is not None]
    if len(valid) < period + 1:
        return 50.0
    gains = []
    losses = []
    for i in range(1, period + 1):
        diff = valid[i] - valid[i - 1]
        if diff >= 0:
            gains.append(diff)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(-diff)
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    for i in range(period + 1, len(valid)):
        diff = valid[i] - valid[i - 1]
        gain = max(0.0, diff)
        loss = max(0.0, -diff)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))

def fetch_stock_data(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1y"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            meta = data['chart']['result'][0]['meta']
            price = meta.get('regularMarketPrice')
            high52 = meta.get('fiftyTwoWeekHigh')
            low52 = meta.get('fiftyTwoWeekLow')
            
            closes = data['chart']['result'][0].get('indicators', {}).get('quote', [{}])[0].get('close', [])
            rsi_val = compute_rsi(closes) if closes else 50.0

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
                "rsi": rsi_val,
                "status": "OK"
            }
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)}

def build_radar():
    print(f"🚀 Collecting radar & swing data for {len(WATCHLIST)} stocks...")
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

    # ==========================================
    # 📊 섹터별 평균 벤치마크 지표 계산
    # ==========================================
    category_names = {
        "tech": "💻 테크/AI",
        "infra": "🏭 산업/인프라",
        "health": "🏥 헬스케어",
        "power": "⚡ 전력/에너지",
        "finance": "🏛️ 금융/거래소",
        "ocean": "🌊 자원/광산",
        "food": "🌾 식량/소비재",
        "defense": "🛡️ 방산/우주"
    }

    sector_stats = {}
    for cat_key, cat_name in category_names.items():
        cat_items = [it for it in stock_items if it["meta"]["category"] == cat_key and it["data"].get("status") == "OK"]
        if cat_items:
            avg_high_drop = sum(it["data"]["from_high_pct"] for it in cat_items) / len(cat_items)
            avg_low_gain = sum(it["data"]["from_low_pct"] for it in cat_items) / len(cat_items)
            avg_rsi = sum(it["data"]["rsi"] for it in cat_items) / len(cat_items)
            cat_bottom = sum(1 for it in cat_items if it["data"]["from_low_pct"] <= 15.0 or it["data"]["from_high_pct"] <= -35.0 or it["data"]["rsi"] <= 35.0)
            sector_stats[cat_key] = {
                "name": cat_name,
                "count": len(cat_items),
                "avg_high_drop": avg_high_drop,
                "avg_low_gain": avg_low_gain,
                "avg_rsi": avg_rsi,
                "bottom_count": cat_bottom
            }

    out_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(out_dir, "radar_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "updated": updated_str,
            "sector_benchmarks": sector_stats,
            "items": stock_items
        }, f, ensure_ascii=False, indent=2)

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
            rsi = d["rsi"]
            rp = max(0, min(100, d["range_pct"]))
            
            # 바닥 사정권 조건: 저점 +15% 이내 or 고점 -35% 이상 폭락 or RSI 35 이하
            is_bottom = (fl_pct <= 15.0) or (fh_pct <= -35.0) or (rsi <= 35.0)
            
            if is_bottom:
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

            # RSI 뱃지
            rsi_badge = ""
            if rsi <= 35.0:
                rsi_badge = f'<span class="rsi-badge rsi-oversold"><i class="bi bi-lightning-fill"></i> RSI {rsi:.0f} 과매도</span>'
            elif rsi >= 70.0:
                rsi_badge = f'<span class="rsi-badge rsi-overbought">RSI {rsi:.0f} 과열</span>'
            else:
                rsi_badge = f'<span class="rsi-badge">RSI {rsi:.0f}</span>'

            cards_html += f"""
            <div class="{card_class}" id="card-{t}" data-category="{m['category']}" data-bottom="{'true' if is_bottom else 'false'}">
                <div class="card-header">
                    <div class="card-title-wrap">
                        <div class="card-ticker-row">
                            <span class="ticker-badge">{t}</span>
                            <span class="tag-badge">{m['tag']}</span>
                            {rsi_badge}
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
                        <span style="color: {fh_color}; font-weight:700;">고점대비 {fh_pct:+.1f}%</span>
                        <span>52주 최고 {high_str}</span>
                    </div>
                    <div class="range-track">
                        <div class="range-fill" style="width: {rp:.1f}%;"></div>
                        <div class="range-pin" style="left: {rp:.1f}%;"></div>
                    </div>
                </div>

                <div class="issue-box">
                    <div class="issue-title"><i class="bi bi-shield-lock-fill text-gold"></i> 독점 해자 & 특수 상황</div>
                    <div class="issue-desc">{m['special_issue']}</div>
                </div>

                <div class="scenario-accordion">
                    <details>
                        <summary><i class="bi bi-diagram-3"></i> 스윙 IF 시나리오 & 킬스위치 보기</summary>
                        <div class="scenario-details">
                            <div class="sc-item sc-best">
                                <strong>🌟 Best (익절 타깃):</strong> {m['if_best']}
                            </div>
                            <div class="sc-item sc-worst">
                                <strong>💥 Worst (위험 요인):</strong> {m['if_worst']}
                            </div>
                            <div class="sc-item sc-kill">
                                <strong>🚨 킬스위치 (기계적 손절):</strong> {m['kill_switch']}
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

    # 섹터 벤치마크 카드 HTML 렌더링
    benchmarks_html = ""
    for c_key, c_val in sector_stats.items():
        drop_color = "#f43f5e" if c_val['avg_high_drop'] <= -20 else "#fb7185"
        benchmarks_html += f"""
        <div class="sec-bench-card" onclick="filterCategory('{c_key}')">
            <div class="sec-bench-header">
                <span class="sec-bench-name">{c_val['name']}</span>
                <span class="sec-bench-count">{c_val['count']}종목</span>
            </div>
            <div class="sec-bench-row">
                <span class="sec-bench-lbl">고점대비 평균</span>
                <span class="sec-bench-val" style="color: {drop_color};">{c_val['avg_high_drop']:+.1f}%</span>
            </div>
            <div class="sec-bench-row">
                <span class="sec-bench-lbl">평균 RSI</span>
                <span class="sec-bench-val">{c_val['avg_rsi']:.0f}</span>
            </div>
            <div class="sec-bench-badge">
                {'🔥 바닥 ' + str(c_val['bottom_count']) + '개' if c_val['bottom_count'] > 0 else '안정권'}
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
    <title>종목 레이더 & 스윙 IF 시나리오 | ThePathLab</title>
    <meta name="description" content="ThePathLab 종목 레이더: 8대 섹터 고마진 독점 해자 기업들의 52주 신저가, RSI 과매도 눌림목 포착 및 스윙 IF 시나리오 실시간 감시 대시보드">
    <link rel="canonical" href="https://chicstory.github.io/radar/">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap" rel="stylesheet">
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
            max-width: 1200px;
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
            max-width: 1200px;
            margin: 2rem auto 1.2rem;
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
            font-size: 1.95rem;
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
            max-width: 820px;
            word-break: keep-all;
        }}
        .meta-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
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

        /* 섹터 벤치마크 그리드 */
        .benchmarks-wrap {{
            max-width: 1200px;
            margin: 0 auto 1.5rem;
            padding: 0 1.25rem;
        }}
        .benchmarks-title {{
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-sub);
            margin-bottom: 0.6rem;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .benchmarks-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(135px, 1fr));
            gap: 8px;
        }}
        .sec-bench-card {{
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 8px 10px;
            cursor: pointer;
            transition: all 0.18s ease;
        }}
        .sec-bench-card:hover {{
            background: rgba(30, 41, 59, 0.9);
            border-color: var(--cyan);
            transform: translateY(-2px);
        }}
        .sec-bench-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 4px;
        }}
        .sec-bench-name {{
            font-size: 0.8rem;
            font-weight: 700;
            color: #fff;
        }}
        .sec-bench-count {{
            font-size: 0.7rem;
            color: var(--text-dim);
            font-family: 'JetBrains Mono', monospace;
        }}
        .sec-bench-row {{
            display: flex;
            justify-content: space-between;
            font-size: 0.72rem;
            color: var(--text-sub);
            margin-bottom: 2px;
            font-family: 'JetBrains Mono', monospace;
        }}
        .sec-bench-val {{ font-weight: 700; }}
        .sec-bench-badge {{
            font-size: 0.68rem;
            font-weight: 700;
            color: var(--gold);
            text-align: right;
            margin-top: 2px;
        }}

        .filter-bar {{
            max-width: 1200px;
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
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: var(--cyan);
            color: #070a12;
            border-color: var(--cyan);
            font-weight: 700;
        }}

        .radar-grid {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.25rem;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
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
            margin-bottom: 0.85rem;
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
        .rsi-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--text-sub);
            background: rgba(255, 255, 255, 0.06);
            padding: 2px 6px;
            border-radius: 4px;
        }}
        .rsi-oversold {{
            color: #fb7185;
            background: rgba(244, 63, 94, 0.18);
            border: 1px solid rgba(244, 63, 94, 0.35);
        }}
        .rsi-overbought {{
            color: #fde047;
            background: rgba(255, 184, 0, 0.18);
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
            margin-bottom: 0.85rem;
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
            border: 1px solid rgba(255, 184, 0, 0.2);
            border-radius: 10px;
            padding: 9px 12px;
            margin-bottom: 0.85rem;
        }}
        .issue-title {{
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--gold);
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        .issue-desc {{
            font-size: 0.83rem;
            color: #e2e8f0;
            line-height: 1.45;
            word-break: keep-all;
        }}

        .scenario-accordion {{
            margin-bottom: 0.85rem;
        }}
        .scenario-accordion details {{
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            overflow: hidden;
        }}
        .scenario-accordion summary {{
            padding: 8px 10px;
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--cyan);
            cursor: pointer;
            user-select: none;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .scenario-accordion summary:hover {{
            background: rgba(0, 242, 254, 0.08);
        }}
        .scenario-details {{
            padding: 8px 10px 10px;
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-size: 0.78rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .sc-item {{
            padding: 5px 8px;
            border-radius: 6px;
            line-height: 1.4;
            word-break: keep-all;
        }}
        .sc-best {{
            background: rgba(16, 185, 129, 0.1);
            color: #6ee7b7;
            border-left: 3px solid var(--green);
        }}
        .sc-worst {{
            background: rgba(244, 63, 94, 0.1);
            color: #fda4af;
            border-left: 3px solid var(--red);
        }}
        .sc-kill {{
            background: rgba(255, 184, 0, 0.1);
            color: #fde047;
            border-left: 3px solid var(--gold);
        }}

        .card-footer-actions {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            padding-top: 0.6rem;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }}
        .thesis-text {{
            font-size: 0.77rem;
            color: var(--text-dim);
            line-height: 1.35;
            word-break: keep-all;
        }}
        .chart-btn {{
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--cyan);
            background: rgba(0, 242, 254, 0.08);
            border: 1px solid rgba(0, 242, 254, 0.3);
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
            .hero-title {{ font-size: 1.55rem; }}
            .card-header {{ flex-direction: column; gap: 8px; }}
            .card-price-wrap {{ text-align: left; }}
            .thesis-text {{ display: none; }}
            .benchmarks-grid {{ grid-template-columns: repeat(2, 1fr); }}
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
            <i class="bi bi-radar"></i> ThePathLab Stock & Swing Radar
        </div>
        <h1 class="hero-title">종목 레이더 & 스윙 IF 시나리오</h1>
        <p class="hero-desc">
            8대 섹터 고마진 독점 해자 기업들의 52주 신저가 근접도, 14일 RSI 과매도 눌림목 포착 및 사전 정의된 스윙 IF 시나리오(Best / Worst / 🚨 킬스위치) 실시간 감시 대시보드입니다.
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

    <section class="benchmarks-wrap">
        <div class="benchmarks-title">
            <i class="bi bi-bar-chart-fill text-gold"></i> 섹터별 평균 벤치마크 현황 (카드를 클릭하면 해당 섹터로 필터링)
        </div>
        <div class="benchmarks-grid">
            {benchmarks_html}
        </div>
    </section>

    <div class="filter-bar">
        <button class="filter-btn active" onclick="filterCategory('all')">전체 ({len(stock_items)})</button>
        <button class="filter-btn" onclick="filterCategory('alert')">🔥 바닥 사정권 ({bottom_count})</button>
        <button class="filter-btn" onclick="filterCategory('tech')">💻 테크/AI</button>
        <button class="filter-btn" onclick="filterCategory('infra')">🏭 산업/냉각/인프라</button>
        <button class="filter-btn" onclick="filterCategory('health')">🏥 헬스케어</button>
        <button class="filter-btn" onclick="filterCategory('power')">⚡ 전력/에너지</button>
        <button class="filter-btn" onclick="filterCategory('finance')">🏛️ 금융/거래소</button>
        <button class="filter-btn" onclick="filterCategory('ocean')">🌊 자원/광산</button>
        <button class="filter-btn" onclick="filterCategory('food')">🌾 식량/소비재</button>
        <button class="filter-btn" onclick="filterCategory('defense')">🛡️ 방산/우주</button>
    </div>

    <main class="radar-grid" id="stockGrid">
        {cards_html}
    </main>

    <script>
        function filterCategory(cat) {{
            const buttons = document.querySelectorAll('.filter-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            // 해당 버튼 활성화
            buttons.forEach(btn => {{
                if (btn.getAttribute('onclick').includes("'" + cat + "'")) {{
                    btn.classList.add('active');
                }}
            }});

            const cards = document.querySelectorAll('.radar-card');
            cards.forEach(card => {{
                if (cat === 'all') {{
                    card.style.display = 'block';
                }} else if (cat === 'alert') {{
                    card.style.display = (card.getAttribute('data-bottom') === 'true') ? 'block' : 'none';
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

    print(f"✅ Stock Radar dashboard built successfully with {len(stock_items)} tickers at: {html_path}")

if __name__ == "__main__":
    build_radar()
