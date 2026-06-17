<script>
  import '../app.css';

  let claimText = '';
  let imageFile = null;
  let imagePreviewUrl = null;
  let isDragging = false;
  let isLoading = false;
  let result = null;
  let error = null;

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

  function handleImageSelect(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      imageFile = file;
      imagePreviewUrl = URL.createObjectURL(file);
      error = null;
    }
  }

  function handleDrop(event) {
    event.preventDefault();
    isDragging = false;
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      imageFile = file;
      imagePreviewUrl = URL.createObjectURL(file);
      error = null;
    }
  }

  function handleDragOver(event) {
    event.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  function removeImage() {
    imageFile = null;
    if (imagePreviewUrl) {
      URL.revokeObjectURL(imagePreviewUrl);
      imagePreviewUrl = null;
    }
  }

  function toBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result.split(',')[1]);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  async function handleCheck() {
    if (!claimText.trim() && !imageFile) {
      error = 'Enter a claim or upload an image to check.';
      return;
    }

    isLoading = true;
    result = null;
    error = null;

    try {
      let imageBase64 = null;
      if (imageFile) {
        imageBase64 = await toBase64(imageFile);
      }

      const payload = {
        text: claimText.trim() || null,
        image: imageBase64 || null
      };

      const response = await fetch(`${BACKEND_URL}/check`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(data.detail || `Server error: ${response.status}`);
      }

      const data = await response.json();
      if (data.status === 'failed') {
        throw new Error('The server could not process this claim. Please try again.');
      }
      result = data;
    } catch (err) {
      error = err.message || 'Something went wrong. Please try again.';
    } finally {
      isLoading = false;
    }
  }

  function handleKeydown(event) {
    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
      handleCheck();
    }
  }

  function reset() {
    claimText = '';
    removeImage();
    result = null;
    error = null;
  }

  function getVerdictStyle(verdict) {
    if (!verdict) return {};
    const v = verdict.toLowerCase();
    if (v === 'true') return { bg: 'var(--green-50)', color: 'var(--green-700)', border: 'var(--green-600)', label: 'ನಿಜ · True' };
    if (v === 'false') return { bg: 'var(--red-50)', color: 'var(--red-700)', border: 'var(--red-600)', label: 'ತಪ್ಪು · False' };
    if (v === 'misleading') return { bg: 'var(--yellow-50)', color: 'var(--yellow-700)', border: 'var(--yellow-600)', label: 'ತಪ್ಪು ತಿಳಿವಳಿಕೆ · Misleading' };
    return { bg: 'var(--indigo-50)', color: 'var(--indigo-700)', border: 'var(--indigo-500)', label: 'ಅನಿಶ್ಚಿತ · Unverified' };
  }
</script>

<div class="page">
  <header class="header">
    <div class="header-inner">
      <div class="logo-block">
        <span class="logo-text">SatyaFinder</span>
        <span class="logo-kannada">ಸತ್ಯ ಹುಡುಕಿ</span>
      </div>
      <span class="header-tag">Karnataka Education · Fact Check</span>
    </div>
  </header>

  <main class="main">
    {#if !result}
      <section class="hero">
        <p class="hero-eyebrow">ಸತ್ಯ ಹುಡುಕಿ — Find the Truth</p>
        <h1 class="hero-title">Is that circular real?</h1>
        <p class="hero-subtitle">
          Paste a claim, forward, or notification from school — or upload a photo of a circular.
          SatyaFinder checks it against Karnataka Education Department sources.
        </p>
      </section>

      <div class="checker-card">
        <div class="input-section">
          <label class="input-label" for="claim-input">Claim or message text</label>
          <textarea
            id="claim-input"
            class="claim-textarea"
            bind:value={claimText}
            on:keydown={handleKeydown}
            placeholder="ಒಂದು ಸುದ್ದಿ ಅಥವಾ circular ಟೈಪ್ ಮಾಡಿ... e.g. Schools are closed on Monday due to heavy rain"
            rows="4"
            disabled={isLoading}
          ></textarea>
          <p class="input-hint">Ctrl + Enter to check</p>
        </div>

        <div class="divider-row">
          <div class="divider-line"></div>
          <span class="divider-text">or upload an image</span>
          <div class="divider-line"></div>
        </div>

        <div class="upload-section">
          {#if imagePreviewUrl}
            <div class="image-preview-wrapper">
              <img src={imagePreviewUrl} alt="Uploaded circular" class="image-preview" />
              <button class="remove-image-btn" on:click={removeImage} disabled={isLoading}>
                Remove
              </button>
            </div>
          {:else}
            <label
              class="drop-zone"
              class:dragging={isDragging}
              on:drop={handleDrop}
              on:dragover={handleDragOver}
              on:dragleave={handleDragLeave}
              for="image-upload"
            >
              <div class="drop-zone-inner">
                <div class="drop-zone-icon-box">
                  <div class="drop-zone-icon"></div>
                </div>
                <p class="drop-zone-primary">Drop a circular image here</p>
                <p class="drop-zone-secondary">or click to browse — JPG, PNG, WEBP</p>
              </div>
              <input
                id="image-upload"
                type="file"
                accept="image/*"
                on:change={handleImageSelect}
                disabled={isLoading}
                style="display:none"
              />
            </label>
          {/if}
        </div>

        {#if error}
          <div class="error-banner" role="alert">
            {error}
          </div>
        {/if}

        <button
          class="check-btn"
          on:click={handleCheck}
          disabled={isLoading || (!claimText.trim() && !imageFile)}
        >
          {#if isLoading}
            <span class="spinner"></span>
            Checking...
          {:else}
            Check this claim
          {/if}
        </button>
      </div>

      <div class="disclaimer">
        SatyaFinder does not make legal or administrative decisions.
        Always verify with your school or the Karnataka DSEL portal.
      </div>

    {:else}
      {@const vs = getVerdictStyle(result.verdict)}
      <section class="result-section">
        {#if result.status === 'processing'}
          <div class="processing-banner" role="status">
            <span class="spinner spinner-dark"></span>
            Still processing — the result may update shortly. Try checking again in a moment.
          </div>
        {/if}

        {#if result.flagged_for_review}
          <div class="flagged-banner" role="alert">
            This claim has been flagged for human review. The AI result below should be treated as preliminary only.
          </div>
        {/if}

        <div class="result-card">
          <div class="result-header">
            <div class="verdict-badge" style="background:{vs.bg}; color:{vs.color}; border-color:{vs.border}">
              {vs.label}
            </div>
            {#if result.confidence !== undefined}
              <div class="confidence-block">
                <span class="confidence-label">Confidence</span>
                <div class="confidence-bar-track">
                  <div
                    class="confidence-bar-fill"
                    style="width:{result.confidence}%; background:{vs.border}"
                  ></div>
                </div>
                <span class="confidence-value">{result.confidence}%</span>
              </div>
            {/if}
          </div>

          <div class="result-explanation">
            <p class="explanation-label">What we found</p>
            <p class="explanation-text">{result.explanation}</p>
          </div>

          {#if result.sources && result.sources.length > 0}
            <div class="sources-block">
              <p class="sources-label">Sources checked</p>
              <ul class="sources-list">
                {#each result.sources as source}
                  <li>
                    <a href={source} target="_blank" rel="noopener noreferrer" class="source-link">
                      {source}
                    </a>
                  </li>
                {/each}
              </ul>
            </div>
          {/if}

          <div class="human-review-notice">
            <p class="human-review-title">Human review recommended</p>
            <p class="human-review-text">
              SatyaFinder flags and explains — it does not make final decisions.
              For school closures, exam dates, or fee changes, confirm directly
              with your school principal or the Karnataka DSEL portal.
            </p>
          </div>
        </div>

        <button class="check-another-btn" on:click={reset}>
          Check another claim
        </button>
      </section>
    {/if}
  </main>

  <footer class="footer">
    <p>SatyaFinder · Karnataka Education Fact Checker · Built for USAII Global AI Hackathon 2026</p>
    <p class="footer-sub">AI output may be incorrect. Always verify with official sources.</p>
  </footer>
</div>

<style>
  .page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: var(--white);
  }

  .header {
    border-bottom: 1px solid var(--gray-200);
    background: var(--white);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .header-inner {
    max-width: 720px;
    margin: 0 auto;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .logo-block {
    display: flex;
    align-items: baseline;
    gap: 10px;
  }

  .logo-text {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--indigo-700);
    letter-spacing: -0.02em;
  }

  .logo-kannada {
    font-family: var(--font-kannada);
    font-size: 0.85rem;
    color: var(--slate-500);
    font-weight: 400;
  }

  .header-tag {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--indigo-600);
    background: var(--indigo-50);
    padding: 4px 10px;
    border-radius: 100px;
    letter-spacing: 0.01em;
  }

  .main {
    flex: 1;
    max-width: 720px;
    margin: 0 auto;
    padding: 60px 24px 40px;
    width: 100%;
  }

  .hero {
    text-align: center;
    margin-bottom: 40px;
  }

  .hero-eyebrow {
    font-family: var(--font-kannada);
    font-size: 0.9rem;
    color: var(--indigo-600);
    font-weight: 600;
    letter-spacing: 0.04em;
    margin-bottom: 12px;
  }

  .hero-title {
    font-size: 2.75rem;
    font-weight: 700;
    color: var(--navy);
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 16px;
  }

  .hero-subtitle {
    font-size: 1.05rem;
    color: var(--slate-600);
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
  }

  .checker-card {
    background: var(--white);
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-xl);
    padding: 32px;
    box-shadow: var(--shadow-lg);
  }

  .input-label {
    display: block;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--slate-700);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 10px;
  }

  .claim-textarea {
    width: 100%;
    border: 1.5px solid var(--gray-200);
    border-radius: var(--radius-md);
    padding: 14px 16px;
    font-size: 1rem;
    color: var(--navy);
    background: var(--off-white);
    resize: vertical;
    transition: border-color 0.15s, box-shadow 0.15s;
    line-height: 1.6;
  }

  .claim-textarea:focus {
    border-color: var(--indigo-500);
    background: var(--white);
    box-shadow: var(--shadow-focus);
  }

  .claim-textarea::placeholder {
    color: var(--gray-400);
    font-family: var(--font-kannada);
    font-size: 0.95rem;
  }

  .claim-textarea:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .input-hint {
    font-size: 0.75rem;
    color: var(--slate-400);
    margin-top: 6px;
    text-align: right;
  }

  .divider-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 24px 0;
  }

  .divider-line {
    flex: 1;
    height: 1px;
    background: var(--gray-200);
  }

  .divider-text {
    font-size: 0.8rem;
    color: var(--slate-400);
    white-space: nowrap;
    font-weight: 500;
  }

  .drop-zone {
    display: block;
    border: 2px dashed var(--gray-200);
    border-radius: var(--radius-lg);
    padding: 36px 24px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
    background: var(--off-white);
  }

  .drop-zone:hover {
    border-color: var(--indigo-500);
    background: var(--indigo-50);
  }

  .drop-zone.dragging {
    border-color: var(--indigo-600);
    background: var(--indigo-50);
  }

  .drop-zone-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }

  .drop-zone-icon-box {
    width: 44px;
    height: 44px;
    border-radius: var(--radius-md);
    background: var(--indigo-100);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 4px;
  }

  .drop-zone-icon {
    width: 20px;
    height: 16px;
    border: 2px solid var(--indigo-600);
    border-radius: 3px;
    position: relative;
  }

  .drop-zone-icon::before {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 2px;
    height: 8px;
    background: var(--indigo-600);
  }

  .drop-zone-icon::after {
    content: '';
    position: absolute;
    bottom: -14px;
    left: 50%;
    transform: translateX(-50%);
    width: 10px;
    height: 2px;
    background: var(--indigo-600);
  }

  .drop-zone-primary {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--slate-700);
  }

  .drop-zone-secondary {
    font-size: 0.8rem;
    color: var(--slate-400);
  }

  .image-preview-wrapper {
    position: relative;
    border-radius: var(--radius-lg);
    overflow: hidden;
    border: 1.5px solid var(--gray-200);
  }

  .image-preview {
    width: 100%;
    max-height: 280px;
    object-fit: contain;
    display: block;
    background: var(--off-white);
  }

  .remove-image-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: var(--navy);
    color: var(--white);
    font-size: 0.75rem;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 100px;
    transition: opacity 0.15s;
  }

  .remove-image-btn:hover {
    opacity: 0.8;
  }

  .error-banner {
    margin-top: 16px;
    padding: 12px 16px;
    background: var(--red-50);
    border: 1px solid var(--red-600);
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    color: var(--red-700);
    font-weight: 500;
  }

  .check-btn {
    margin-top: 24px;
    width: 100%;
    padding: 15px 24px;
    background: var(--indigo-600);
    color: var(--white);
    font-size: 1rem;
    font-weight: 600;
    border-radius: var(--radius-md);
    letter-spacing: 0.01em;
    transition: background 0.15s, transform 0.1s, box-shadow 0.15s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }

  .check-btn:hover:not(:disabled) {
    background: var(--indigo-700);
    box-shadow: var(--shadow-md);
  }

  .check-btn:active:not(:disabled) {
    transform: scale(0.99);
  }

  .check-btn:disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }

  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: var(--white);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    flex-shrink: 0;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .disclaimer {
    margin-top: 20px;
    text-align: center;
    font-size: 0.78rem;
    color: var(--slate-400);
    line-height: 1.5;
  }

  .result-section {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .processing-banner {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    background: var(--indigo-50);
    border: 1px solid var(--indigo-100);
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    color: var(--indigo-700);
    font-weight: 500;
  }

  .spinner-dark {
    border-color: rgba(79,70,229,0.2);
    border-top-color: var(--indigo-600);
  }

  .flagged-banner {
    padding: 14px 18px;
    background: var(--yellow-50);
    border: 1px solid var(--yellow-600);
    border-radius: var(--radius-md);
    font-size: 0.9rem;
    color: var(--yellow-700);
    font-weight: 500;
    line-height: 1.5;
  }

  .result-card {
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-xl);
    padding: 32px;
    box-shadow: var(--shadow-lg);
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .result-header {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .verdict-badge {
    display: inline-flex;
    align-items: center;
    padding: 10px 20px;
    border-radius: 100px;
    border: 1.5px solid;
    font-size: 1rem;
    font-weight: 700;
    font-family: var(--font-kannada);
    letter-spacing: 0.01em;
    align-self: flex-start;
  }

  .confidence-block {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .confidence-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--slate-500);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    white-space: nowrap;
  }

  .confidence-bar-track {
    flex: 1;
    height: 6px;
    background: var(--gray-200);
    border-radius: 100px;
    overflow: hidden;
  }

  .confidence-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.6s ease;
  }

  .confidence-value {
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--slate-700);
    white-space: nowrap;
    min-width: 36px;
    text-align: right;
  }

  .explanation-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--slate-500);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
  }

  .explanation-text {
    font-size: 1rem;
    color: var(--slate-700);
    line-height: 1.7;
  }

  .sources-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--slate-500);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 10px;
  }

  .sources-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .source-link {
    font-size: 0.85rem;
    color: var(--indigo-600);
    text-decoration: none;
    word-break: break-all;
    font-weight: 500;
    transition: color 0.15s;
  }

  .source-link:hover {
    color: var(--indigo-700);
    text-decoration: underline;
  }

  .human-review-notice {
    background: var(--indigo-50);
    border: 1px solid var(--indigo-100);
    border-radius: var(--radius-md);
    padding: 16px 20px;
  }

  .human-review-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--indigo-700);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
  }

  .human-review-text {
    font-size: 0.88rem;
    color: var(--indigo-900);
    line-height: 1.6;
    opacity: 0.85;
  }

  .check-another-btn {
    align-self: center;
    padding: 12px 28px;
    background: var(--white);
    color: var(--indigo-600);
    font-size: 0.95rem;
    font-weight: 600;
    border: 1.5px solid var(--indigo-200);
    border-radius: var(--radius-md);
    transition: background 0.15s, border-color 0.15s;
  }

  .check-another-btn:hover {
    background: var(--indigo-50);
    border-color: var(--indigo-400);
  }

  .footer {
    border-top: 1px solid var(--gray-200);
    padding: 20px 24px;
    text-align: center;
  }

  .footer p {
    font-size: 0.75rem;
    color: var(--slate-400);
    line-height: 1.6;
  }

  .footer-sub {
    margin-top: 4px;
    font-style: italic;
  }

  @media (max-width: 600px) {
    .hero-title {
      font-size: 2rem;
    }

    .checker-card {
      padding: 22px 18px;
    }

    .result-card {
      padding: 22px 18px;
    }

    .header-tag {
      display: none;
    }
  }
</style>
