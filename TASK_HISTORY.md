# 📜 ThePathLab Main Portal (chicstory.github.io) Task & Architecture History

ThePathLab 메인 포털 허브 및 공통 네비게이션, SEO, 차량 유지비 계산기(autocost) 개발 히스토리입니다.

> 루트 전체 마스터 히스토리는 [루트 TASK_HISTORY.md](../TASK_HISTORY.md)를 참조하십시오.

## [2026-09-30] 미국 1억 파이프라인 52주 신저가 & 특수 상황 모니터링 레이더 대시보드 구축 및 새벽 무인 자동화 배포
- **1. 요청사항**: 
  - 터미널이나 로컬 환경이 아닌, 아침에 눈떠서 스마트폰으로 `thapathlab.com`에서 원클릭으로 미국 시장 핵심 종목의 52주 최저가 근접도와 특수 상황(Special Situation)을 모니터링할 수 있는 전용 웹 대시보드 요청.
- **2. 솔루션 & 구현**:
  - **전용 웹 레이더 페이지 신설 (`chicstory.github.io/radar/`)**:
    - `radar_builder.py`: 야후 파이낸스 실시간 시세를 수집해 52주 최저가 대비 위치, 고점 대비 하락률, 시각적 52주 레인지 프로그레스 바, 특수 이슈, IF 시나리오(Best/Worst/킬스위치)를 담은 모바일 최적화 Dark Tech UI 대시보드(`radar/index.html`) 및 경량 API(`radar/radar_data.json`) 0초 빌더 구현.
    - 52주 최저가에 가장 가까운 순(오름차순)으로 자동 정렬하여 현재 가장 바닥에 패대기쳐진 종목(NKE +1.9%, PRVA +2.9%, CI +13.7%, DOX +15.3% 등)이 최상단에 노출되도록 설계.
  - **포털 네비게이션 및 퀵허브 연동**:
    - `index.html` 글로벌 내비게이션 바, 모바일 드로어, 상단 Quick Hub Anchor Bar(6열 확장)에 '미국 1억 레이더' 다이렉트 점프 칩 추가.
  - **새벽 무인 배치 파이프라인 연계**:
    - `thepathlab/auto_daily_briefing.bat` 및 `run_briefing.bat`의 포털 배포 단계에 `radar_builder.py` 실행 및 `git add radar/`를 포함시켜 매일 새벽 브리핑과 함께 365일 무인 자동 업데이트 완료.
- **3. 결과 & 검증**:
  - `https://thapathlab.com/radar/` 실시간 배포 완료 (`8bc1ecc`).
  - 모바일(360px) 가로 스크롤 제로, GA4 추적 태그 유지 및 콘솔 에러 제로 검증.
- **4. 주요 합의 사항**:
  - 매일 아침 눈떠서 스마트폰으로 `thapathlab.com/radar/`만 열면 바닥 사정권 종목과 특수 이슈를 즉시 파악 가능.
  - 13개 핵심 종목(PRVA, NKE, CI, DOX, PATH, ADM, CF, NTR, RIG, VAL, OII, DE, ETN) 중심의 바벨 포지션 감시 유지.

---

## [2026-09-29] 네이버 블로그 홈페이지형 1단 위젯 5종 구축, 배포 및 블로그 연동 로드맵 수립
- **1. 요청사항**:
  - 네이버 블로그 메인/프롤로그에 3대 핵심 사이트(thapathlab.com, runanalyz.com, bookinquiry.com) 및 계산기 연동 요청.
  - 상단 가로형 배너(홈페이지형 블로그) 구조 전환 및 블로그 테마/스킨 리프레시.
- **2. 솔루션 & 구현**:
  - **네이버 블로그 1단 레이아웃 전환**: 상단에 가로 5칸 위젯 배치가 가능한 1단 레이아웃 확립.
  - **레티나 고화질 카드 배너 5종 생성 및 배포**:
    - `generate_widgets.py` 스크립트를 통해 가로 340×210px(렌더링 170×105px) 다크 테크 카드 배너 5종 생성.
    - `chicstory.github.io/widgets/` 경로에 배포 (`banner_thepathlab.png`, `banner_runanalyz.png`, `banner_bookinquiry.png`, `banner_autocost.png`, `banner_hub.png`).
    - 네이버 블로그 구형 스킨의 높이 잘림(overflow:hidden) 방지를 위한 `style="display:block !important; height:105px !important;"` 완벽 보정 코드 제공.
  - **네이버 블로그 5대 카테고리 체계 정립**:
    - `독서노트` (주 1회, 원제 어그로 해체 + BookInquiry 4대 질문), `매일루틴` (RunAnalyz 러닝 마일리지 캡처 및 생각 정렬), `1단계 탈출일기` (`1단계 재정일기`, `캐시플로 - 철거 현장 스토리`, `지출관리`).
  - **4대 기기 Syncthing 풀 메시 연동 구조 확립**: 데스크탑, 노트북, 스마트폰, 태블릿 간 `00_Inbox/raw` 실시간 메모 동기화 및 `.stignore` 충돌 방지 가이드 제공.
- **3. 결과 & 검증**:
  - 커밋 `c298677` 푸시 완료 (`https://thapathlab.com/widgets/banner_thepathlab.png` 등 200 OK 실시간 서빙).
- **4. 주요 합의 사항**:
  - 네이버 블로그 위젯은 외부 이미지 직접링크와 `style="display:block !important; height:105px !important;"` 인라인 강제 스타일을 표준으로 유지.
  - 다음 세션 우선 작업: ① BookInquiry 초경량 한글화(i18n), ② 네이버 블로그 캐시플로 첫 글(AEO 3줄 결론 + 사진 3곳 가이드).

---

## [2026-09-25] [GEO/AEO] 메인 포털 통합 llms.txt 배포 및 'n대 금속' 용어 일원화
- **1. 요청사항**: 
  - 생성형 AI 검색(Perplexity, ChatGPT, Gemini) 대응을 위한 포털 마스터 `llms.txt` 표준 구축.
  - '7대 금속' 등 가변적인 숫자 표현을 제거하고 '금속 원자재 & 스크랩'으로 일원화.
- **2. 솔루션 & 구현**:
  - `chicstory.github.io/llms.txt`: 포털 산하 5대 핵심 프로젝트(Metals, RunAnalyz, Engines, AutoIssue, AutoCost)를 체계적으로 요약한 마크다운 사이트맵 생성.
  - `chicstory.github.io/about.html`: '7대 금속 원자재' 문구를 '금속 원자재 & 스크랩'으로 교정.
- **3. 결과 & 검증**:
  - `https://chicstory.github.io/llms.txt` 및 `https://thapathlab.com/llms.txt`로 AI 크롤러 0초 다이렉트 접근 지원.

---

## [2026-09-18] [SEO & AI 봇] Google-Extended & 주요 생성형 AI 크롤러 robots.txt 명시적 허용 배포

- **1. 요청사항**: 
  - 제미나이가 `runanalyz.com`과 `thapathlab.com`에 대해 구글 AI 학습 봇(`Google-Extended`) 접근이 차단되어 있다고 오판하는 문제 원인 조사.
  - Cloudflare 및 서버 측 크롤러 차단 여부 검증 및 robots.txt 보완 요청.
- **2. 솔루션 & 구현**:
  - **정밀 원인 규명**:
    1. 두 도메인 모두 Cloudflare DNS Only(회색 구름) 모드로 GitHub Pages IP로 직접 라우팅되고 있어 Cloudflare WAF/Bot 규칙에 의한 차단이 아님을 증명.
    2. curl 테스트 결과 `Google-Extended`, `GoogleOther`, `Googlebot` 모두 HTTP 200 정상 응답.
    3. `Google-Extended`는 실제 방문 크롤러가 아니라 robots.txt 전용 학습 거부 토큰(Standalone token)이며, 제미나이의 접근 불가 답변은 LLM의 전형적인 학습 토큰 혼동(할루시네이션)임을 설명.
  - **robots.txt 명시적 선언 보완**:
    - `chicstory.github.io/robots.txt` 및 `shoef/runanalyz/robots.txt`, `shoef/robots.txt`에 Google Search & AI 크롤러(`Googlebot`, `Google-Extended`, `GoogleOther`)와 주요 LLM(`GPTBot`, `OAI-SearchBot`, `ClaudeBot`) 명시적 `Allow: /` 블록 추가.
    - 변경된 `robots.txt` 파일만 명시적 스테이징 후 커밋 및 푸시.
- **3. 결과 & 검증**:
  - `chicstory.github.io` 커밋: `00ad1f6`
  - `runanalyz` 커밋: `036653d`
  - 배포 라이브 검증: `https://thapathlab.com/robots.txt` 실시간 200 OK 및 신규 AI 크롤러 허용 블록 반영 확인.
- **4. 주요 합의 사항**:
  - 향후 신규 서브도메인이나 사이트 생성 시 `robots.txt`에는 `User-agent: *`뿐 아니라 `Googlebot`, `Google-Extended`, `GoogleOther` 등의 명시적 허용 블록을 기본 템플릿으로 포함한다.


## [2026-09-16] 메인 포털 극단적 다이어트(심플 타이틀, 4대 허브 퀵 앵커칩, 컨텐츠 중심 카드화 및 모바일 오버플로우 방지)
- **1. 요청사항**:
  - 장황한 수식어 타이틀("실무자를 위한 원자재 시세 & 모빌리티 데이터 랩" 등)을 전면 제거하고 직관적으로 브랜딩.
  - 가로 스크롤을 유발하던 라이브 펄스바 대신, 클릭 시 0초 즉시 점프하는 4대 허브 퀵 앵커 칩(`quick-hub-bar`) 탑재.
  - 세세한 문장형 설명 대신, 사용자가 찾는 컨텐츠 명칭(XX계산기, 일일금속시세, 엔진백과, 리콜속보)을 전면에 단도직입적으로 박아둘 것.
  - 모바일 화면에서 텍스트가 밀려 화면 밖으로 오버플로우되거나 레이아웃이 깨지는 현상 전수 점검 및 차단.
- **2. 솔루션 & 구현**:
  - **헤더 타이틀 초슬림화 (`chicstory.github.io/index.html`)**:
    - 장황한 문장형 카피를 삭제하고, `ThePathLab` 메인 타이틀 + 한줄 핵심 카테고리(`원자재 시세 · 자동차 결함·리콜 · 운용 유지비 계산기 · 파워트레인 백과`)로 극단적 다이어트.
  - **4대 허브 퀵 앵커칩 (`quick-hub-bar`) 신설**:
    - `live-pulse-bar` 제거 후 반응형 4열 앵커 바 구축:
      `[ 🪙 일일 금속시세·계산기 ]` `[ 🚨 자동차 결함·리콜 ]` `[ 💸 유지비·보험 계산기 ]` `[ 🚗 엔진 전수 백과 ]`
    - 모바일에서는 2x2 그리드로 자동 전환되어 가로 스크롤/오버플로우 0% 차단.
  - **컨텐츠·기능 중심 쿼드 카드 개편**:
    - 카드 1: **일일 금속 시세 & 스크랩·폐촉매 계산기** (`🪙 9대 금속 일일 시세표`, `⚡ 1초 스크랩 계산기`, `🚗 폐촉매 실무 견적기`)
    - 카드 2: **자동차 데일리 결함·리콜 속보** (`🚨 데일리 리콜 속보`, `🇺🇸 미국 NHTSA 선제 공고`, `🔍 10대 제조사별 필터`)
    - 카드 3: **자동차 유지비 & 보험료 계산기** (`⛽ 오피넷 실시간 유류비`, `🛡️ 내 차 자차가액·보험료`, `🚘 국산·수입 13종 비교`)
    - 카드 4: **엔진 전수 백과 & 제조사별 스펙표** (`📊 9대사 전수 스펙표`, `📈 실측 다이노 출력 곡선`, `💬 차주 정비 꿀팁 메모장`)
  - **모바일 오버플로우 방지 미디어 쿼리 보강**:
    - 480px 이하 초소형 화면에서 폰트, 카드 패딩, 칩 크기를 축소하여 가로 스크롤 없이 데스크톱과 모바일 모두 1화면 최적화.
- **3. 결과 & 검증**:
  - `chicstory.github.io`: 커밋 `e9aee84` 푸시 완료.
  - CSS 정적 분석: 8개 nowrap 규칙 중 오버플로우 유발 요소(과거 pulse bar 등) 완전 제거 확인.
- **4. 주요 합의 사항**:
  - 메인 포털에서는 "설명문"보다 사용자가 누를 수 있는 "컨텐츠와 기능 명칭"을 우선 노출하며, 복잡한 장식보다는 0초 접근성을 최우선 원칙으로 삼는다.


## [2026-09-16] 메인 포털 UX 대폭 다이어트(히어로 경량화, 라이브 펄스바, 4대 허브 쿼드 카드) 및 전 레포 GNB/햄버거 메뉴 AutoCost 전수 동기화
- **1. 요청사항**:
  - `thapathlab.com` 첫 진입 시 무슨 사이트인지 한눈에 안 들어오고 장황한 수식어("INTELLIGENCE ARCHIVE", "산업 자원 시세 & 자동차 테크 인텔리전스" 등)가 스크롤을 가로막는 문제 해결.
  - 데스크톱 1화면(Above the Fold)에서 4대 핵심 서비스를 한눈에 파악하고 즉시 클릭/이동할 수 있도록 히어로 다이어트 및 인터랙티브 UI 개편.
  - 상단 메뉴(GNB)와 햄버거 메뉴(드로어)에 신규 허브 `autocost`(유지비·보험)가 각 서브 페이지별로 나타났다 안 나타났다 하는 불일치 문제 전수 점검 및 100% 통일.
- **2. 솔루션 & 구현**:
  - **메인 포털 히어로 다이어트 & 실시간 라이브 펄스 바 (`chicstory.github.io/index.html`)**:
    - 장황한 타이틀과 거대 여백을 대폭 축소(`padding: 2.2rem 0 1.2rem`, 폰트 크기 최적화)하고 직관적인 "실무자를 위한 원자재 시세 & 모빌리티 데이터 랩"으로 핵심 가치 정의.
    - 상단 `live-pulse-bar` 신설: ⛽ 오피넷 전국 휘발유/경유 실시간 유가, 🪙 LME 9대 금속 & 환율, 🚨 국토부·NHTSA 리콜 속보, 🚗 280개 파워트레인 제원·다이노 한줄 라이브 티커 탑재.
    - **4대 서비스 쿼드-대시보드 카드화**:
      1) `Metals`: 9대 금속 원자재·스크랩 허브 (LME 시세, 1초 계산기, 폐촉매 견적기)
      2) `AutoIssue`: 자동차 데일리 이슈 허브 (국토부 리콜, NHTSA 선제 공고, 10대 제조사)
      3) `AutoCost`: 자동차 순수 유지비 & 자차가액·보험료 (오피넷 실시간 유가, 올해 자차기준가액, 국산/수입 13종)
      4) `Engines`: 제조사별 전수 스펙표 & 280개 엔진 백과 (9대사 전수 스펙 비교, 실측 다이노, 차주 정비 메모장)
      - 데스크톱 2x2 반응형 그리드 및 퀵 액션 칩을 배치하여 1화면에서 탐색 완료 가능.
  - **워크스페이스 전 레포 GNB & 햄버거 드로어 AutoCost 전수 동기화 (총 417개 HTML)**:
    - 표준 7대 GNB 링크(`포털 홈`, `자동차 데일리 이슈`, `유지비·보험`, `금속 원자재·스크랩`, `제조사별 스펙표`, `엔진 전수 백과`, `이용 가이드`) 확립.
    - `autoissue/index.html`: GNB 및 드로어에 `autocost` 링크 추가 및 푸시 (`65fd165`).
    - `chicstory.github.io`: `about.html`, `contact.html`, `privacy.html` GNB 및 드로어 동기화 및 푸시 (`bf3faad`).
    - `engines`: 루트 10개 파일(`index.html`, 9대 제조사 스펙표) 및 하위 396개 상세 엔진 페이지 전수에 `autoissue`와 `autocost` 링크 일괄 동기화 및 푸시 (`4454dc6`).
    - 전수 검증 스크립트 실행 결과 Missing 0건 달성.
  - **보안 및 규정 준수**:
    - GEMINI.md 지침에 따라 `git add .` 배제 및 대상 파일 명시적 스테이징 준수.
    - GA4 (`G-K3PFHN6VW7`) 및 AdSense (`ca-pub-1876940323402065`) 태그 100% 무결성 유지.
- **3. 결과 & 검증**:
  - `chicstory.github.io`: 커밋 `bf3faad` 푸시 완료.
  - `autoissue`: 커밋 `65fd165` 푸시 완료.
  - `engines`: 커밋 `4454dc6` 푸시 완료.
  - 워크스페이스 내 417개 전체 HTML 대상 `autocost` 누락 여부 전수 스캔: 누락 0건 (100% 통일).
- **4. 주요 합의 사항**:
  - 향후 신규 서비스 허브 추가 시 메인 포털 카드뿐만 아니라 `autoissue`, `engines`, `metals`, 서브 안내 페이지(`about`, `privacy`, `contact`)의 GNB와 햄버거 드로어까지 원스톱으로 동기화하는 자동화 배치 또는 일괄 스크립트를 표준 절차로 활용한다.

