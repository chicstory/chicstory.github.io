# 🚀 ThePathLab 포털 성능 최적화 히스토리 (PageSpeed Optimization Log)

이 문서는 `ThePathLab` 메인 포털(`chicstory.github.io`)의 웹 성능(PageSpeed Insights, Core Web Vitals) 개선 과정과 적용된 핵심 아키텍처 및 히스토리를 기록한 기술 문서입니다.

---

## 1. 개요 및 최종 달성 목표
- **대상 URL**: `https://chicstory.github.io/`
- **핵심 목표**:
  - 데스크탑: **PageSpeed 95 ~ 100점** (TBT < 50ms)
  - 모바일: **PageSpeed 90점 이상** (FCP < 1.8s, LCP < 2.5s)
  - Dark Tech UI 테마 무결성 유지, GA4(`G-K3PFHN6VW7`) 및 다국어 번역 기능 100% 보존

---

## 2. 주요 병목 이슈 및 단계별 해결 내역

### 🛑 이슈 1: 외부 CDN(jsdelivr) 폰트 타임아웃 (27.2초 대기 현상)
* **현상**:
  - PageSpeed 측정 시 점수가 70~80점대로 급락하거나 봇 응답 대기 시간이 27.2초까지 치솟음.
* **원인**:
  - `https://cdn.jsdelivr.net/gh/orioncactus/pretendard.../pretendard.min.css` 외부 CDN 링크를 참조하고 있었으나, 해외 PageSpeed 분석 봇 및 특정 환경에서 jsdelivr 지연/차단 발생.
* **해결책**:
  - 무거운 외부 CDN 폰트 링크를 완전 제거.
  - OS 내장 시스템 폰트 스택(`-apple-system`, `BlinkMacSystemFont`, `Pretendard`, `Segoe UI`, `Roboto`, `Apple SD Gothic Neo`)을 최우선 폴백으로 적용하여 **폰트 로딩 대기 시간 0초 달성**.

---

### 🛑 이슈 2: Google Translate 위젯 초기 렌더링 블로킹 (128KB 미사용 JS)
* **현상**:
  - 첫 화면 진입 시 구글 번역 스크립트(`translate.google.com/translate_a/element.js`)가 동기 실행되어 메인 스레드를 장시간 점유.
* **해결책**:
  - **On-demand Lazy Load 패턴 적용**:
  - 사용자의 실제 상호작용(`scroll`, `mousemove`, `touchstart`) 또는 언어 버튼 클릭 시에만 번역 스크립트를 동적으로 로드하도록 분리.
  - PageSpeed 측정 봇의 첫 페인트 측정 과정에서 번역 스크립트 오버헤드를 완전 제거.

---

### 🛑 이슈 3: 데스크탑 TBT (270ms) & 모바일 FCP(3.9s)/LCP(6.0s) 지연
* **현상**:
  - 데스크탑에서 Total Blocking Time(TBT)이 270ms 발생.
  - 모바일 저사양 CPU에서 1,300줄 이상의 방대한 CSS 및 전체 DOM 트리를 첫 프레임에 계산하느라 LCP가 지연됨.
* **해결책**:
  1. **`content-visibility: auto` 기반 오프스크린 렌더링 스킵**:
     - 첫 화면(Above the Fold) 바깥의 하단 요소(`.recent-activity-wrap`, `.brand-chips-wrap`, `footer`)에 브라우저 네이티브 지연 렌더링 적용.
     - `content-visibility: auto; contain-intrinsic-size: 0 250px;` 지정으로 뷰포트에 도달하기 전까지 복잡한 스타일/레이아웃 연산을 스킵하여 메인 스레드 부하 해소.
  2. **Hero 텍스트 렌더링 우선순위 강화**:
     - 메인 헤딩(`.hero-title`, `.hero-desc`)에 `text-rendering: optimizeSpeed;`를 부여하여 폰트 렌더링 즉각성 극대화.
  3. **Non-blocking CSS/폰트 분리**:
     - `media="print" onload="this.media='all'"` 기법으로 서브 폰트(JetBrains Mono)와 Bootstrap Icons를 비동기 로드 처리.

---

## 3. 핵심 CSS 최적화 스니펫 요약

```css
/* Hero 영역 초고속 텍스트 페인팅 */
.hero-title, .hero-desc {
    text-rendering: optimizeSpeed;
}

/* 스크롤 하단 컴포넌트 브라우저 연산 스킵 */
.recent-activity-wrap {
    content-visibility: auto;
    contain-intrinsic-size: 0 250px;
}

.brand-chips-wrap {
    content-visibility: auto;
    contain-intrinsic-size: 0 160px;
}

footer {
    content-visibility: auto;
    contain-intrinsic-size: 0 140px;
}
```

---

## 4. 모니터링 및 유지보수 수칙
1. **외부 폰트 CDN 재도입 금지**:
   - CDN 장애 및 해외 봇 타임아웃 방지를 위해 Pretendard 등 웹폰트 CDN을 `<link>`로 직접 불러오지 마십시오.
2. **신규 컴포넌트 추가 시 유의사항**:
   - 첫 화면 아래에 들어가는 무거운 목록이나 위젯은 항상 `content-visibility: auto;`와 적정 `contain-intrinsic-size`를 부여하여 초기 렌더링 속도를 유지하십시오.
