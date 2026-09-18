/**
 * 여러 페이지에서 공통으로 쓰는 fetch 헬퍼 + 네비게이션 활성 표시
 */
const DEFAULT_TIMEOUT_MS = 15000;

/**
 * fetch를 감싸서 타임아웃과 에러 메시지를 통일해서 처리한다.
 * 실패 시 항상 사용자에게 보여줄 한글 메시지가 담긴 Error를 던진다.
 */
async function fetchJSON(url, options = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    clearTimeout(timeoutId);

    let data = {};
    try {
      data = await res.json();
    } catch (parseError) {
      data = {};
    }

    if (!res.ok) {
      throw new Error(data.error || '오류가 발생했어요. 잠시 후 다시 시도해주세요.');
    }

    return data;
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error('응답이 지연되고 있어요. 잠시 후 다시 시도해주세요.');
    }
    throw err;
  }
}

function setActiveNav() {
  const path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach((link) => {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });
}

document.addEventListener('DOMContentLoaded', setActiveNav);
