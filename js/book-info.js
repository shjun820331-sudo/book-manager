document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('book-info-form');
  const titleInput = document.getElementById('title-input');
  const resultEl = document.getElementById('result');
  const messageEl = document.getElementById('message');
  const submitBtn = document.getElementById('submit-btn');
  const authorIntroEl = document.getElementById('author-intro');
  const summaryEl = document.getElementById('summary');
  const goDiscussionBtn = document.getElementById('go-discussion-btn');

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const title = titleInput.value.trim();
    messageEl.textContent = '';
    resultEl.hidden = true;
    goDiscussionBtn.hidden = true;

    // 실패 처리 ①: 빈 입력
    if (!title) {
      messageEl.textContent = '책 제목을 입력해주세요.';
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = '조회 중...';

    try {
      const data = await fetchJSON('/api/book-info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      });

      authorIntroEl.textContent = data.author_intro;
      summaryEl.textContent = data.summary;
      resultEl.hidden = false;

      goDiscussionBtn.hidden = false;
      goDiscussionBtn.onclick = () => {
        window.location.href = `discussion.html?title=${encodeURIComponent(title)}`;
      };
    } catch (err) {
      // 실패 처리 ②: API 오류 / 실패 처리 ③: 지연·타임아웃 (fetchJSON에서 메시지 통일)
      messageEl.textContent = err.message;
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = '조회하기';
    }
  });
});
