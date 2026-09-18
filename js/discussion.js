document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('discussion-form');
  const titleInput = document.getElementById('title-input');
  const ageSelect = document.getElementById('age-select');
  const purposeSelect = document.getElementById('purpose-select');
  const resultEl = document.getElementById('result');
  const messageEl = document.getElementById('message');
  const submitBtn = document.getElementById('submit-btn');
  const talkingPointsEl = document.getElementById('talking-points');
  const discussionTopicsEl = document.getElementById('discussion-topics');

  // 도서 정보 페이지에서 넘어온 책 제목을 URL 쿼리스트링으로 자동 채움
  const params = new URLSearchParams(window.location.search);
  const prefillTitle = params.get('title');
  if (prefillTitle) {
    titleInput.value = prefillTitle;
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const title = titleInput.value.trim();
    const ageGroup = ageSelect.value;
    const purpose = purposeSelect.value;

    messageEl.textContent = '';
    resultEl.hidden = true;

    // 실패 처리 ①: 필수값 누락
    if (!title || !ageGroup || !purpose) {
      messageEl.textContent = '필수 항목(책 제목, 연령대, 목적)을 모두 입력/선택해주세요.';
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = '추천 받는 중...';

    try {
      const data = await fetchJSON('/api/discussion-topics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, age_group: ageGroup, purpose }),
      });

      renderList(talkingPointsEl, data.talking_points);
      renderList(discussionTopicsEl, data.discussion_topics);
      resultEl.hidden = false;
    } catch (err) {
      // 실패 처리 ②: API 오류 / 실패 처리 ③: 지연·타임아웃
      messageEl.textContent = err.message;
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = '토론 주제 추천받기';
    }
  });

  function renderList(listEl, items) {
    listEl.innerHTML = '';
    (items || []).forEach((item) => {
      const li = document.createElement('li');
      li.textContent = item;
      listEl.appendChild(li);
    });
  }
});
