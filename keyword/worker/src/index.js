/**
 * ThePathLab Keyword & Blog Diagnostic Worker
 * - Search Ad API (/keywordstool)
 * - NAVER API HUB Blog Search (/search/v1/blog)
 * - NAVER API HUB Search Trend (/search-trend/v1/search)
 * - Naver Blog RSS (rss.blog.naver.com)
 */

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400',
};

function jsonResponse(data, status = 200, cacheSeconds = 0) {
  const headers = {
    ...CORS_HEADERS,
    'Content-Type': 'application/json; charset=utf-8',
  };
  if (cacheSeconds > 0) {
    headers['Cache-Control'] = `public, max-age=${cacheSeconds}`;
  }
  return new Response(JSON.stringify(data), { status, headers });
}

function getSearchCreds(env) {
  return {
    id: env.NAVER_NCP_CLIENT_ID || env.NAVER_OPEN_CLIENT_ID || '',
    secret: env.NAVER_NCP_CLIENT_SECRET || env.NAVER_OPEN_CLIENT_SECRET || '',
  };
}

async function createSearchAdSignature(timestamp, method, uri, secretKey) {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    encoder.encode(secretKey),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const message = `${timestamp}.${method}.${uri}`;
  const signatureBuffer = await crypto.subtle.sign('HMAC', key, encoder.encode(message));
  const bytes = new Uint8Array(signatureBuffer);
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

function parseCount(val) {
  if (typeof val === 'number') return val;
  if (typeof val === 'string') {
    if (val.includes('<')) return 5;
    const num = parseInt(val.replace(/,/g, ''), 10);
    return Number.isNaN(num) ? 0 : num;
  }
  return 0;
}

function parseFloatSafe(val) {
  const num = parseFloat(val);
  return Number.isFinite(num) ? num : 0;
}

async function fetchNaverBlogSearch(query, env, display = 10, sort = 'sim') {
  const { id, secret } = getSearchCreds(env);
  const url = `https://naverapihub.apigw.ntruss.com/search/v1/blog?query=${encodeURIComponent(query)}&display=${display}&start=1&sort=${sort}&format=json`;
  const res = await fetch(url, {
    headers: {
      'X-NCP-APIGW-API-KEY-ID': id,
      'X-NCP-APIGW-API-KEY': secret,
    },
  });
  if (!res.ok) {
    throw new Error(`NAVER API HUB error (${res.status})`);
  }
  return res.json();
}

async function fetchSearchTrend(keyword, env, gender = '', ages = []) {
  const { id, secret } = getSearchCreds(env);
  const now = new Date();
  const endDate = now.toISOString().slice(0, 10);
  const startObj = new Date(now.getFullYear() - 1, now.getMonth(), 1);
  const startDate = startObj.toISOString().slice(0, 10);

  const body = {
    startDate,
    endDate,
    timeUnit: 'month',
    keywordGroups: [{ groupName: keyword, keywords: [keyword] }],
  };
  if (gender === 'm' || gender === 'f') body.gender = gender;
  if (Array.isArray(ages) && ages.length > 0) body.ages = ages;

  const res = await fetch('https://naverapihub.apigw.ntruss.com/search-trend/v1/search', {
    method: 'POST',
    headers: {
      'X-NCP-APIGW-API-KEY-ID': id,
      'X-NCP-APIGW-API-KEY': secret,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    throw new Error(`Search Trend API error (${res.status})`);
  }
  const data = await res.json();
  return data?.results?.[0]?.data || [];
}

async function fetchAutocomplete(query) {
  const url = `https://ac.search.naver.com/nx/ac?q=${encodeURIComponent(query)}&st=100&r_format=json&r_enc=UTF-8`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0' },
  });
  if (!res.ok) return [];
  const data = await res.json();
  const list = data?.items?.[0] || [];
  return list.map((item) => item[0]).filter(Boolean).slice(0, 10);
}

function stripHtml(str) {
  return (str || '')
    .replace(/<[^>]*>/g, '')
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .trim();
}

function parseRssItems(xmlText, limit = 15) {
  const items = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/g;
  let match;
  while ((match = itemRegex.exec(xmlText)) !== null && items.length < limit) {
    const block = match[1];
    const titleMatch = /<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>|<title>([\s\S]*?)<\/title>/.exec(block);
    const linkMatch = /<link>([\s\S]*?)<\/link>/.exec(block);
    const dateMatch = /<pubDate>([\s\S]*?)<\/pubDate>/.exec(block);
    const title = stripHtml(titleMatch?.[1] || titleMatch?.[2] || '');
    const link = (linkMatch?.[1] || '').trim();
    const pubDate = (dateMatch?.[1] || '').trim();
    if (title && link) {
      items.push({ title, link, pubDate });
    }
  }
  return items;
}

function analyzeTopDifficulty(items, totalDocs) {
  const now = Date.now();
  const dayMs = 86400000;
  let recent3mCount = 0;
  let old1yCount = 0;
  let titleLenSum = 0;

  items.forEach((item) => {
    const title = stripHtml(item.title);
    titleLenSum += title.length;
    const pd = item.postdate || '';
    if (/^\d{8}$/.test(pd)) {
      const y = Number(pd.slice(0, 4));
      const m = Number(pd.slice(4, 6)) - 1;
      const d = Number(pd.slice(6, 8));
      const diffDays = (now - new Date(y, m, d).getTime()) / dayMs;
      if (diffDays <= 90) recent3mCount += 1;
      if (diffDays >= 365) old1yCount += 1;
    }
  });

  const topCount = items.length;
  const avgTitleLen = topCount > 0 ? Math.round(titleLenSum / topCount) : 0;
  let level = '보통';
  if (old1yCount >= 5) level = '쉬움 (노후 글 다수)';
  else if (recent3mCount >= 6) level = '치열 (최신 글 위주)';

  return { totalDocs, topCount, recent3mCount, old1yCount, avgTitleLen, level };
}

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const creds = getSearchCreds(env);

    if (url.pathname === '/' || url.pathname === '/api/health') {
      return jsonResponse({
        status: 'ok',
        service: 'ThePathLab Keyword & Blog Diagnostic Worker',
        configured: {
          searchAd: Boolean(env.NAVER_AD_API_KEY && env.NAVER_AD_SECRET_KEY && env.NAVER_AD_CUSTOMER_ID),
          searchApi: Boolean(creds.id && creds.secret),
        },
      });
    }

    const cache = caches.default;
    const cacheKey = new Request(url.toString(), request);
    const cached = await cache.match(cacheKey);
    if (cached) return cached;

    try {
      // 1. Keyword Discovery
      if (url.pathname === '/api/keywords') {
        const q = (url.searchParams.get('q') || '').trim();
        if (!q) return jsonResponse({ error: '키워드를 입력해 주세요.' }, 400);
        if (!env.NAVER_AD_API_KEY || !env.NAVER_AD_SECRET_KEY || !env.NAVER_AD_CUSTOMER_ID) {
          return jsonResponse({ error: '검색광고 API 키가 Worker Secret에 설정되지 않았습니다.' }, 500);
        }
        if (!creds.id || !creds.secret) {
          return jsonResponse({ error: 'NAVER API HUB 키가 Worker Secret에 설정되지 않았습니다.' }, 500);
        }

        const hintKeywords = q.replace(/\s+/g, '');
        const uri = '/keywordstool';
        const timestamp = Date.now().toString();
        const signature = await createSearchAdSignature(timestamp, 'GET', uri, env.NAVER_AD_SECRET_KEY);

        const [adRes, autocomplete] = await Promise.all([
          fetch(`https://api.searchad.naver.com${uri}?hintKeywords=${encodeURIComponent(hintKeywords)}&showDetail=1`, {
            headers: {
              'X-Timestamp': timestamp,
              'X-API-KEY': env.NAVER_AD_API_KEY,
              'X-Customer': env.NAVER_AD_CUSTOMER_ID,
              'X-Signature': signature,
            },
          }),
          fetchAutocomplete(q),
        ]);

        if (!adRes.ok) {
          const errText = await adRes.text();
          return jsonResponse({ error: `검색광고 API 오류 (${adRes.status}): ${errText}` }, 502);
        }

        const adData = await adRes.json();
        const rawList = (adData.keywordList || []).slice(0, 15);

        const enriched = await Promise.all(
          rawList.map(async (item) => {
            const pc = parseCount(item.monthlyPcQcCnt);
            const mobile = parseCount(item.monthlyMobileQcCnt);
            const totalSearch = pc + mobile;
            let blogDocs = 0;
            try {
              const blogRes = await fetchNaverBlogSearch(item.relKeyword, env, 1, 'sim');
              blogDocs = blogRes.total || 0;
            } catch {
              blogDocs = 0;
            }
            const competition = totalSearch > 0 ? Number((blogDocs / totalSearch).toFixed(2)) : 999;
            return {
              keyword: item.relKeyword,
              pc,
              mobile,
              totalSearch,
              blogDocs,
              competition,
              compIdx: item.compIdx || '-',
              ctrPc: parseFloatSafe(item.monthlyAvePcCtr),
              ctrMo: parseFloatSafe(item.monthlyAveMobileCtr),
              clkPc: parseFloatSafe(item.monthlyAvePcClkCnt),
              clkMo: parseFloatSafe(item.monthlyAveMobileClkCnt),
              plAvgDepth: parseCount(item.plAvgDepth),
            };
          })
        );

        const response = jsonResponse({ query: q, autocomplete, keywords: enriched }, 200, 43200);
        ctx.waitUntil(cache.put(cacheKey, response.clone()));
        return response;
      }

      // 1-B. Keyword Deep-Dive Detail (Trend + Top10 Difficulty)
      if (url.pathname === '/api/keyword-detail') {
        const q = (url.searchParams.get('q') || '').trim();
        const gender = (url.searchParams.get('gender') || '').trim();
        const agesRaw = (url.searchParams.get('ages') || '').trim();
        const ages = agesRaw ? agesRaw.split(',').filter(Boolean) : [];
        if (!q) return jsonResponse({ error: '키워드를 입력해 주세요.' }, 400);
        if (!creds.id || !creds.secret) {
          return jsonResponse({ error: 'NAVER API HUB 키가 Worker Secret에 설정되지 않았습니다.' }, 500);
        }

        const [trend, blogRes] = await Promise.all([
          fetchSearchTrend(q, env, gender, ages),
          fetchNaverBlogSearch(q, env, 10, 'sim'),
        ]);

        const items = blogRes.items || [];
        const difficulty = analyzeTopDifficulty(items, blogRes.total || 0);
        const topPosts = items.slice(0, 5).map((item, idx) => ({
          rank: idx + 1,
          title: stripHtml(item.title),
          link: item.link,
          postdate: item.postdate || '',
        }));
        const response = jsonResponse({
          query: q,
          filters: { gender, ages },
          trend,
          difficulty,
          topPosts,
        }, 200, 21600);
        ctx.waitUntil(cache.put(cacheKey, response.clone()));
        return response;
      }

      // 2. Top Blog Rank Check
      if (url.pathname === '/api/rank') {
        const q = (url.searchParams.get('q') || '').trim();
        const blogId = (url.searchParams.get('blogId') || '').trim().toLowerCase();
        if (!q) return jsonResponse({ error: '키워드를 입력해 주세요.' }, 400);
        if (!creds.id || !creds.secret) {
          return jsonResponse({ error: 'NAVER API HUB 키가 Worker Secret에 설정되지 않았습니다.' }, 500);
        }

        const blogRes = await fetchNaverBlogSearch(q, env, 30, 'sim');
        let myRank = null;
        const items = (blogRes.items || []).map((item, idx) => {
          const rank = idx + 1;
          const isMine = blogId ? (item.bloggerlink || '').toLowerCase().includes(`blog.naver.com/${blogId}`) : false;
          if (isMine && myRank === null) myRank = rank;
          return {
            rank,
            title: stripHtml(item.title),
            link: item.link,
            bloggername: item.bloggername,
            bloggerlink: item.bloggerlink,
            postdate: item.postdate,
            isMine,
          };
        });

        const response = jsonResponse({
          query: q,
          blogId: blogId || null,
          totalDocs: blogRes.total || 0,
          myRank,
          items,
        }, 200, 3600);
        ctx.waitUntil(cache.put(cacheKey, response.clone()));
        return response;
      }

      // 3. Blog Post Omission Check
      if (url.pathname === '/api/omission') {
        const blogId = (url.searchParams.get('blogId') || '').trim().toLowerCase();
        if (!blogId || !/^[a-z0-9_-]+$/.test(blogId)) {
          return jsonResponse({ error: '올바른 네이버 블로그 ID를 입력해 주세요.' }, 400);
        }
        if (!creds.id || !creds.secret) {
          return jsonResponse({ error: 'NAVER API HUB 키가 Worker Secret에 설정되지 않았습니다.' }, 500);
        }

        const rssRes = await fetch(`https://rss.blog.naver.com/${encodeURIComponent(blogId)}.xml`, {
          headers: { 'User-Agent': 'Mozilla/5.0' },
        });
        if (!rssRes.ok) {
          return jsonResponse({ error: `블로그 RSS를 불러올 수 없습니다 (${rssRes.status}). 비공개 블로그이거나 ID를 확인해 주세요.` }, 404);
        }

        const xmlText = await rssRes.text();
        const rssItems = parseRssItems(xmlText, 15);
        if (rssItems.length === 0) {
          return jsonResponse({ error: 'RSS에서 최근 글을 찾지 못했습니다.' }, 404);
        }

        const results = await Promise.all(
          rssItems.map(async (post) => {
            try {
              const searchRes = await fetchNaverBlogSearch(post.title, env, 10, 'sim');
              const found = (searchRes.items || []).some((it) =>
                (it.bloggerlink || '').toLowerCase().includes(`blog.naver.com/${blogId}`)
              );
              return { ...post, status: found ? 'OK' : 'BAD' };
            } catch {
              return { ...post, status: 'ERROR' };
            }
          })
        );

        const okCount = results.filter((r) => r.status === 'OK').length;
        const badCount = results.filter((r) => r.status === 'BAD').length;

        const response = jsonResponse({
          blogId,
          checkedCount: results.length,
          okCount,
          badCount,
          posts: results,
        }, 200, 1800);
        ctx.waitUntil(cache.put(cacheKey, response.clone()));
        return response;
      }

      return jsonResponse({ error: 'Not Found' }, 404);
    } catch (err) {
      return jsonResponse({ error: err.message || 'Internal Server Error' }, 500);
    }
  },
};
