<script>
  import '../app.css';
  import { onMount } from 'svelte';

  let claimText = '';
  let imageFile = null;
  let imagePreviewUrl = null;
  let isDragging = false;
  let isLoading = false;
  let result = null;
  let error = null;
  let isLight = false;
  let activeStep = 0;
  let lang = 'en';

  onMount(() => {
    const saved = localStorage.getItem('sf-theme');
    if (saved === 'light') isLight = true;
    const savedLang = localStorage.getItem('sf-lang');
    if (savedLang === 'kn') lang = 'kn';
  });

  function toggleTheme() {
    isLight = !isLight;
    localStorage.setItem('sf-theme', isLight ? 'light' : 'dark');
  }

  function toggleLang() {
    lang = lang === 'en' ? 'kn' : 'en';
    localStorage.setItem('sf-lang', lang);
  }

  const t = {
    en: {
      heroBadge: 'AI-powered · Karnataka DSEL sources',
      heroTitle1: 'Is that circular',
      heroTitleAccent: 'real?',
      heroSubtitle: 'Got a WhatsApp forward about school closures, exam dates, or fee changes? Paste it below. Satya Finder cross-checks it against Karnataka Education Department sources in seconds.',
      inputLabel: 'Claim or message text',
      placeholder: 'Type a claim or circular... e.g. Schools are closed on Monday due to heavy rain',
      inputHint: 'Ctrl + Enter to check',
      tryExample: 'Try an example',
      orUpload: 'or upload an image',
      dropPrimary: 'Drop a circular image here',
      dropSecondary: 'or click to browse — JPG, PNG, WEBP',
      checkBtn: 'Check this claim',
      checking: 'Analysing claim...',
      remove: 'Remove',
      disclaimer: 'Satya Finder does not make legal or administrative decisions. Always verify with your school or the Karnataka DSEL portal.',
      errorEmpty: 'Enter a claim or upload an image to check.',
      processingMsg: 'Still processing — the result may update. Try again in a moment.',
      flaggedMsg: 'This claim has been flagged for human review. Treat the AI result below as preliminary only.',
      whatWeFound: 'What we found',
      confidence: 'Confidence',
      sourcesChecked: 'Sources checked',
      humanTitle: 'Human review recommended',
      humanText: 'Satya Finder flags and explains — it does not make final decisions. For school closures, exam dates, or fee changes, confirm directly with your school principal or the Karnataka DSEL portal.',
      checkAnother: 'Check another claim',
      footerMain: 'Satya Finder · Karnataka Education Fact Checker · Built for USAII Global AI Hackathon 2026',
      footerSub: 'AI output may be incorrect. Always verify with official sources.',
      hiwBadge: 'Process',
      hiwTitle: 'How it works',
      hiwSubtitle: 'Four steps from rumour to verdict',
      verdictTrue: 'True',
      verdictFalse: 'False',
      verdictMisleading: 'Misleading',
      verdictUnverified: 'Unverified',
      lightLabel: 'Light',
      darkLabel: 'Dark',
      langLabel: 'ಕನ್ನಡ',
      headerTag: 'Karnataka Education · Fact Check',
      samples: [
        'Schools are closed on Monday due to flooding in Bengaluru',
        'PU Board has postponed all exams by two weeks',
        'Karnataka government declared a holiday for all schools tomorrow',
      ],
      hiwSteps: [
        {
          number: '01',
          title: 'Paste or Upload',
          desc: 'Type a claim from a WhatsApp forward, news headline, or school circular — or upload a screenshot or image directly.',
        },
        {
          number: '02',
          title: 'AI Analyses the Claim',
          desc: 'Satya Finder uses a large language model to parse the claim, extract key facts, and identify what needs verification.',
        },
        {
          number: '03',
          title: 'Cross-checked Against DSEL Sources',
          desc: 'The claim is matched against Karnataka DSEL circulars, official notifications, and verified government data in real time.',
        },
        {
          number: '04',
          title: 'Verdict Delivered',
          desc: 'You get a clear verdict — True, False, Misleading, or Unverified — along with a confidence score and source links.',
        },
      ],
    },
    kn: {
      heroBadge: 'AI-ಆಧಾರಿತ · Karnataka DSEL ಮೂಲಗಳು',
      heroTitle1: 'ಆ circular',
      heroTitleAccent: 'ನಿಜವೇ?',
      heroSubtitle: 'ಶಾಲೆ ಮುಚ್ಚುವಿಕೆ, ಪರೀಕ್ಷಾ ದಿನಾಂಕಗಳು ಅಥವಾ ಶುಲ್ಕ ಬದಲಾವಣೆಯ ಬಗ್ಗೆ WhatsApp ಸಂದೇಶ ಬಂದಿದೆಯೇ? ಕೆಳಗೆ ಅಂಟಿಸಿ. Satya Finder ಅದನ್ನು Karnataka ಶಿಕ್ಷಣ ಇಲಾಖೆಯ ಮೂಲಗಳೊಂದಿಗೆ ಕ್ಷಣಾರ್ಧದಲ್ಲಿ ಪರಿಶೀಲಿಸುತ್ತದೆ.',
      inputLabel: 'ಸಂದೇಶ ಅಥವಾ ಹೇಳಿಕೆ ಟೈಪ್ ಮಾಡಿ',
      placeholder: 'ಒಂದು ಸುದ್ದಿ ಅಥವಾ circular ಟೈಪ್ ಮಾಡಿ... ಉದಾ: ಮಳೆಯ ಕಾರಣ ಸೋಮವಾರ ಶಾಲೆಗಳಿಗೆ ರಜೆ',
      inputHint: 'Ctrl + Enter ಒತ್ತಿ ಪರಿಶೀಲಿಸಿ',
      tryExample: 'ಉದಾಹರಣೆ ನೋಡಿ',
      orUpload: 'ಅಥವಾ ಚಿತ್ರ ಅಪ್ಲೋಡ್ ಮಾಡಿ',
      dropPrimary: 'Circular ಚಿತ್ರವನ್ನು ಇಲ್ಲಿ ಬಿಡಿ',
      dropSecondary: 'ಅಥವಾ ಕ್ಲಿಕ್ ಮಾಡಿ — JPG, PNG, WEBP',
      checkBtn: 'ಹೇಳಿಕೆ ಪರಿಶೀಲಿಸಿ',
      checking: 'ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...',
      remove: 'ತೆಗೆದುಹಾಕಿ',
      disclaimer: 'Satya Finder ಕಾನೂನು ಅಥವಾ ಆಡಳಿತಾತ್ಮಕ ನಿರ್ಧಾರಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುವುದಿಲ್ಲ. ಯಾವಾಗಲೂ ನಿಮ್ಮ ಶಾಲೆ ಅಥವಾ Karnataka DSEL ಪೋರ್ಟಲ್ ಮೂಲಕ ದೃಢೀಕರಿಸಿ.',
      errorEmpty: 'ಪರಿಶೀಲಿಸಲು ಹೇಳಿಕೆ ನಮೂದಿಸಿ ಅಥವಾ ಚಿತ್ರ ಅಪ್ಲೋಡ್ ಮಾಡಿ.',
      processingMsg: 'ಇನ್ನೂ ಪ್ರಕ್ರಿಯೆಯಲ್ಲಿದೆ — ಫಲಿತಾಂಶ ಶೀಘ್ರದಲ್ಲೇ ನವೀಕರಣಗೊಳ್ಳಬಹುದು.',
      flaggedMsg: 'ಈ ಹೇಳಿಕೆಯನ್ನು ಮಾನವ ಪರಿಶೀಲನೆಗೆ ಗುರುತಿಸಲಾಗಿದೆ. ಕೆಳಗಿನ AI ಫಲಿತಾಂಶವನ್ನು ಪ್ರಾಥಮಿಕ ಮಾತ್ರ ಎಂದು ಪರಿಗಣಿಸಿ.',
      whatWeFound: 'ನಾವು ಕಂಡುಕೊಂಡದ್ದು',
      confidence: 'ವಿಶ್ವಾಸ ಮಟ್ಟ',
      sourcesChecked: 'ಪರಿಶೀಲಿಸಿದ ಮೂಲಗಳು',
      humanTitle: 'ಮಾನವ ಪರಿಶೀಲನೆ ಶಿಫಾರಸು',
      humanText: 'Satya Finder ಸೂಚಿಸುತ್ತದೆ ಮತ್ತು ವಿವರಿಸುತ್ತದೆ — ಅಂತಿಮ ನಿರ್ಧಾರ ತೆಗೆದುಕೊಳ್ಳುವುದಿಲ್ಲ. ಶಾಲೆ ಮುಚ್ಚುವಿಕೆ, ಪರೀಕ್ಷಾ ದಿನಾಂಕಗಳು ಅಥವಾ ಶುಲ್ಕ ಬದಲಾವಣೆಗಳಿಗೆ, ನೇರವಾಗಿ ನಿಮ್ಮ ಮುಖ್ಯೋಪಾಧ್ಯಾಯರನ್ನು ಅಥವಾ Karnataka DSEL ಪೋರ್ಟಲ್ ಅನ್ನು ಸಂಪರ್ಕಿಸಿ.',
      checkAnother: 'ಮತ್ತೊಂದು ಹೇಳಿಕೆ ಪರಿಶೀಲಿಸಿ',
      footerMain: 'Satya Finder · Karnataka ಶಿಕ್ಷಣ Fact Checker · USAII Global AI Hackathon 2026',
      footerSub: 'AI ಔಟ್‌ಪುಟ್ ತಪ್ಪಾಗಿರಬಹುದು. ಯಾವಾಗಲೂ ಅಧಿಕೃತ ಮೂಲಗಳೊಂದಿಗೆ ಪರಿಶೀಲಿಸಿ.',
      hiwBadge: 'ಪ್ರಕ್ರಿಯೆ',
      hiwTitle: 'ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ',
      hiwSubtitle: 'ಅಫವಾಹದಿಂದ ತೀರ್ಪಿನವರೆಗೆ ನಾಲ್ಕು ಹಂತಗಳು',
      verdictTrue: 'ನಿಜ · True',
      verdictFalse: 'ತಪ್ಪು · False',
      verdictMisleading: 'ತಪ್ಪು ತಿಳಿವಳಿಕೆ · Misleading',
      verdictUnverified: 'ಅನಿಶ್ಚಿತ · Unverified',
      lightLabel: 'Light',
      darkLabel: 'Dark',
      langLabel: 'English',
      headerTag: 'Karnataka ಶಿಕ್ಷಣ · Fact Check',
      samples: [
        'ಮಳೆಯ ಕಾರಣ ಬೆಂಗಳೂರಿನಲ್ಲಿ ಸೋಮವಾರ ಶಾಲೆಗಳಿಗೆ ರಜೆ',
        'PU ಮಂಡಳಿ ಎಲ್ಲಾ ಪರೀಕ್ಷೆಗಳನ್ನು ಎರಡು ವಾರ ಮುಂದೂಡಿದೆ',
        'Karnataka ಸರ್ಕಾರ ನಾಳೆ ಎಲ್ಲಾ ಶಾಲೆಗಳಿಗೆ ರಜೆ ಘೋಷಿಸಿದೆ',
      ],
      hiwSteps: [
        {
          number: '01',
          title: 'ಅಂಟಿಸಿ ಅಥವಾ ಅಪ್ಲೋಡ್ ಮಾಡಿ',
          desc: 'WhatsApp ಸಂದೇಶ, ಸುದ್ದಿ ಶೀರ್ಷಿಕೆ ಅಥವಾ ಶಾಲಾ circular ನಿಂದ ಹೇಳಿಕೆ ಟೈಪ್ ಮಾಡಿ — ಅಥವಾ ನೇರವಾಗಿ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅಥವಾ ಚಿತ್ರ ಅಪ್ಲೋಡ್ ಮಾಡಿ.',
        },
        {
          number: '02',
          title: 'AI ಹೇಳಿಕೆ ವಿಶ್ಲೇಷಿಸುತ್ತದೆ',
          desc: 'Satya Finder ಹೇಳಿಕೆಯನ್ನು ಪಾರ್ಸ್ ಮಾಡಲು, ಪ್ರಮುಖ ಸಂಗತಿಗಳನ್ನು ಹೊರತೆಗೆಯಲು ಮತ್ತು ಏನನ್ನು ಪರಿಶೀಲಿಸಬೇಕೆಂದು ಗುರುತಿಸಲು ದೊಡ್ಡ ಭಾಷಾ ಮಾದರಿಯನ್ನು ಬಳಸುತ್ತದೆ.',
        },
        {
          number: '03',
          title: 'DSEL ಮೂಲಗಳೊಂದಿಗೆ ಪರಿಶೀಲನೆ',
          desc: 'ಹೇಳಿಕೆಯನ್ನು Karnataka DSEL circulars, ಅಧಿಕೃತ ಅಧಿಸೂಚನೆಗಳು ಮತ್ತು ಪರಿಶೀಲಿತ ಸರ್ಕಾರಿ ಡೇಟಾದೊಂದಿಗೆ ತಕ್ಷಣವೇ ಹೋಲಿಸಲಾಗುತ್ತದೆ.',
        },
        {
          number: '04',
          title: 'ತೀರ್ಪು ನೀಡಲಾಗುತ್ತದೆ',
          desc: 'ನಿಮಗೆ ಸ್ಪಷ್ಟ ತೀರ್ಪು ಸಿಗುತ್ತದೆ — ನಿಜ, ತಪ್ಪು, ತಪ್ಪು ತಿಳಿವಳಿಕೆ ಅಥವಾ ಅನಿಶ್ಚಿತ — ವಿಶ್ವಾಸ ಅಂಕ ಮತ್ತು ಮೂಲ ಲಿಂಕ್‌ಗಳೊಂದಿಗೆ.',
        },
      ],
    },
  };

  $: strings = t[lang];

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
      error = strings.errorEmpty;
      return;
    }
    isLoading = true;
    result = null;
    error = null;
    try {
      let imageBase64 = null;
      if (imageFile) imageBase64 = await toBase64(imageFile);
      const payload = { text: claimText.trim() || null, image: imageBase64 || null };
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
      if (data.status === 'failed') throw new Error('The server could not process this claim. Please try again.');
      result = data;
    } catch (err) {
      error = err.message || 'Something went wrong. Please try again.';
    } finally {
      isLoading = false;
    }
  }

  function handleKeydown(event) {
    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) handleCheck();
  }

  function reset() {
    claimText = '';
    removeImage();
    result = null;
    error = null;
  }

  function injectSample(text) {
    claimText = text;
    error = null;
  }

  function getVerdictStyle(verdict) {
    if (!verdict) return {};
    const v = verdict.toLowerCase();
    if (v === 'true') return { bg: 'rgba(22,163,74,0.15)', color: '#4ade80', border: '#16a34a', label: strings.verdictTrue };
    if (v === 'false') return { bg: 'rgba(220,38,38,0.15)', color: '#f87171', border: '#dc2626', label: strings.verdictFalse };
    if (v === 'misleading') return { bg: 'rgba(202,138,4,0.15)', color: '#facc15', border: '#ca8a04', label: strings.verdictMisleading };
    return { bg: 'rgba(99,102,241,0.15)', color: '#a5b4fc', border: '#6366f1', label: strings.verdictUnverified };
  }
</script>

<div class="page" class:light={isLight}>
  <div class="bg-grid"></div>
  <div class="bg-glow-1"></div>
  <div class="bg-glow-2"></div>

  <header class="header">
    <div class="header-inner">
      <div class="logo-block">
        <span class="logo-dot"></span>
        <span class="logo-text">Satya Finder</span>
        <span class="logo-kannada">ಸತ್ಯ ಹುಡುಕಿ</span>
      </div>
      <span class="header-tag">{strings.headerTag}</span>
      <div class="header-controls">
        <button class="theme-toggle" on:click={toggleLang} aria-label="Toggle language">
          {strings.langLabel}
        </button>
        <button class="theme-toggle" on:click={toggleTheme} aria-label="Toggle theme">
          {isLight ? strings.darkLabel : strings.lightLabel}
        </button>
      </div>
    </div>
  </header>

  <main class="main">
    {#if !result}
      <section class="hero">
        <div class="hero-badge">{strings.heroBadge}</div>
        <h1 class="hero-title">
          {strings.heroTitle1} <span class="hero-accent">{strings.heroTitleAccent}</span>
        </h1>
        <p class="hero-subtitle">{strings.heroSubtitle}</p>
      </section>

      <div class="checker-card">
        <div class="card-glow"></div>

        <div class="input-section">
          <label class="input-label" for="claim-input">{strings.inputLabel}</label>
          <textarea
            id="claim-input"
            class="claim-textarea"
            class:kannada-text={lang === 'kn'}
            bind:value={claimText}
            on:keydown={handleKeydown}
            placeholder={strings.placeholder}
            rows="4"
            disabled={isLoading}
          ></textarea>
          <p class="input-hint">{strings.inputHint}</p>
        </div>

        <div class="samples-row">
          <span class="samples-label">{strings.tryExample}</span>
          {#each strings.samples as sample}
            <button class="sample-chip" on:click={() => injectSample(sample)} disabled={isLoading}>
              {sample.length > 42 ? sample.slice(0, 42) + '…' : sample}
            </button>
          {/each}
        </div>

        <div class="divider-row">
          <div class="divider-line"></div>
          <span class="divider-text">{strings.orUpload}</span>
          <div class="divider-line"></div>
        </div>

        <div class="upload-section">
          {#if imagePreviewUrl}
            <div class="image-preview-wrapper">
              <img src={imagePreviewUrl} alt="Uploaded circular" class="image-preview" />
              <button class="remove-image-btn" on:click={removeImage} disabled={isLoading}>{strings.remove}</button>
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
                <div class="drop-icon-ring">
                  <div class="drop-icon-inner"></div>
                </div>
                <p class="drop-zone-primary">{strings.dropPrimary}</p>
                <p class="drop-zone-secondary">{strings.dropSecondary}</p>
              </div>
              <input id="image-upload" type="file" accept="image/*" on:change={handleImageSelect} disabled={isLoading} style="display:none" />
            </label>
          {/if}
        </div>

        {#if error}
          <div class="error-banner" role="alert">{error}</div>
        {/if}

        <button class="check-btn" on:click={handleCheck} disabled={isLoading || (!claimText.trim() && !imageFile)}>
          {#if isLoading}
            <span class="spinner"></span>
            {strings.checking}
          {:else}
            {strings.checkBtn}
          {/if}
        </button>
      </div>

      <div class="disclaimer">{strings.disclaimer}</div>

      <section class="hiw-section">
        <div class="hiw-header">
          <span class="hiw-badge">{strings.hiwBadge}</span>
          <h2 class="hiw-title">{strings.hiwTitle}</h2>
          <p class="hiw-subtitle">{strings.hiwSubtitle}</p>
        </div>

        <div class="hiw-steps">
          {#each strings.hiwSteps as step, i}
            <button
              class="hiw-step"
              class:hiw-step-active={activeStep === i}
              on:click={() => activeStep = i}
              aria-pressed={activeStep === i}
            >
              <div class="hiw-step-left">
                <div class="hiw-step-num" class:hiw-num-active={activeStep === i}>{step.number}</div>
                <div class="hiw-step-connector" class:hiw-connector-last={i === strings.hiwSteps.length - 1}></div>
              </div>
              <div class="hiw-step-body">
                <div class="hiw-step-top">
                  <span class="hiw-step-title">{step.title}</span>
                  <span class="hiw-chevron" class:hiw-chevron-open={activeStep === i}>›</span>
                </div>
                {#if activeStep === i}
                  <p class="hiw-step-desc">{step.desc}</p>
                {/if}
              </div>
            </button>
          {/each}
        </div>
      </section>

    {:else}
      {@const vs = getVerdictStyle(result.verdict)}
      <section class="result-section">
        {#if result.status === 'processing'}
          <div class="processing-banner" role="status">
            <span class="spinner spinner-indigo"></span>
            {strings.processingMsg}
          </div>
        {/if}

        {#if result.flagged_for_review}
          <div class="flagged-banner" role="alert">
            <span class="flagged-dot"></span>
            {strings.flaggedMsg}
          </div>
        {/if}

        <div class="result-card">
          <div class="result-card-glow" style="background:{vs.border}"></div>

          <div class="result-header">
            <div class="verdict-badge" style="background:{vs.bg}; color:{vs.color}; border-color:{vs.border}">
              {vs.label}
            </div>
            {#if result.confidence !== undefined}
              <div class="confidence-block">
                <span class="confidence-label">{strings.confidence}</span>
                <div class="confidence-bar-track">
                  <div class="confidence-bar-fill" style="width:{result.confidence}%; background:{vs.border}"></div>
                </div>
                <span class="confidence-value" style="color:{vs.color}">{result.confidence}%</span>
              </div>
            {/if}
          </div>

          <div class="result-explanation">
            <p class="explanation-label">{strings.whatWeFound}</p>
            <p class="explanation-text">{result.explanation}</p>
          </div>

          {#if result.sources && result.sources.length > 0}
            <div class="sources-block">
              <p class="sources-label">{strings.sourcesChecked}</p>
              <ul class="sources-list">
                {#each result.sources as source}
                  <li>
                    <a href={source} target="_blank" rel="noopener noreferrer" class="source-link">{source}</a>
                  </li>
                {/each}
              </ul>
            </div>
          {/if}

          <div class="human-review-notice">
            <p class="human-review-title">{strings.humanTitle}</p>
            <p class="human-review-text">{strings.humanText}</p>
          </div>
        </div>

        <button class="check-another-btn" on:click={reset}>{strings.checkAnother}</button>
      </section>
    {/if}
  </main>

  <footer class="footer">
    <p>{strings.footerMain}</p>
    <p class="footer-sub">{strings.footerSub}</p>
  </footer>
</div>

<style>
  .page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: #080b14;
    color: #e2e8f0;
    position: relative;
    overflow-x: hidden;
  }

  .bg-grid {
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
  }

  .bg-glow-1 {
    position: fixed;
    top: -180px;
    left: 50%;
    transform: translateX(-60%);
    width: 700px;
    height: 500px;
    background: radial-gradient(ellipse, rgba(99,102,241,0.18) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  .bg-glow-2 {
    position: fixed;
    bottom: -200px;
    right: -100px;
    width: 500px;
    height: 500px;
    background: radial-gradient(ellipse, rgba(139,92,246,0.1) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  .header {
    border-bottom: 1px solid rgba(99,102,241,0.15);
    background: rgba(8,11,20,0.85);
    backdrop-filter: blur(12px);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .header-inner {
    max-width: 760px;
    margin: 0 auto;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .logo-block {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .logo-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #6366f1;
    box-shadow: 0 0 8px #6366f1;
    animation: pulse-dot 2s ease-in-out infinite;
    flex-shrink: 0;
  }

  @keyframes pulse-dot {
    0%, 100% { opacity: 1; box-shadow: 0 0 8px #6366f1; }
    50%       { opacity: 0.5; box-shadow: 0 0 16px #6366f1; }
  }

  .logo-text {
    font-size: 1.2rem;
    font-weight: 700;
    color: #e2e8f0;
    letter-spacing: -0.02em;
  }

  .logo-kannada {
    font-family: 'Noto Sans Kannada', sans-serif;
    font-size: 0.82rem;
    color: #6366f1;
    font-weight: 400;
  }

  .header-tag {
    font-size: 0.72rem;
    font-weight: 600;
    color: #a5b4fc;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    padding: 4px 10px;
    border-radius: 100px;
    letter-spacing: 0.03em;
    white-space: nowrap;
  }

  .header-controls {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
  }

  .theme-toggle {
    font-size: 0.72rem;
    font-weight: 600;
    color: #64748b;
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 100px;
    padding: 5px 14px;
    cursor: pointer;
    transition: background 0.15s, color 0.15s;
    letter-spacing: 0.04em;
    white-space: nowrap;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .theme-toggle:hover {
    background: rgba(99,102,241,0.16);
    color: #a5b4fc;
  }

  .main {
    flex: 1;
    max-width: 760px;
    margin: 0 auto;
    padding: 60px 24px 40px;
    width: 100%;
    position: relative;
    z-index: 1;
  }

  .hero {
    text-align: center;
    margin-bottom: 44px;
  }

  .hero-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #a5b4fc;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 20px;
  }

  .hero-title {
    font-size: 3rem;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 18px;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .hero-accent {
    color: #6366f1;
    position: relative;
  }

  .hero-accent::after {
    content: '';
    position: absolute;
    bottom: 2px;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    border-radius: 2px;
  }

  .hero-subtitle {
    font-size: 1rem;
    color: #cbd5e1;
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.7;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .checker-card {
    background: rgba(15,20,35,0.8);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 24px;
    padding: 36px;
    box-shadow: 0 0 0 1px rgba(99,102,241,0.05), 0 24px 60px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(8px);
  }

  .card-glow {
    position: absolute;
    top: -60px;
    left: 50%;
    transform: translateX(-50%);
    width: 300px;
    height: 120px;
    background: radial-gradient(ellipse, rgba(99,102,241,0.15) 0%, transparent 70%);
    pointer-events: none;
  }

  .input-label {
    display: block;
    font-size: 0.72rem;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 10px;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .claim-textarea {
    width: 100%;
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 14px 16px;
    font-size: 0.97rem;
    color: #f1f5f9;
    background: rgba(8,11,20,0.6);
    resize: vertical;
    transition: border-color 0.2s, box-shadow 0.2s;
    line-height: 1.65;
  }

  .claim-textarea.kannada-text {
    font-family: 'Noto Sans Kannada', sans-serif;
    font-size: 1rem;
    line-height: 1.8;
  }

  .claim-textarea:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
    outline: none;
  }

  .claim-textarea::placeholder {
    color: #64748b;
    font-size: 0.9rem;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .claim-textarea:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .input-hint {
    font-size: 0.72rem;
    color: #64748b;
    margin-top: 6px;
    text-align: right;
  }

  .samples-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-top: 14px;
  }

  .samples-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #94a3b8;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    flex-shrink: 0;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .sample-chip {
    font-size: 0.78rem;
    color: #a5b4fc;
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 100px;
    padding: 5px 12px;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s, color 0.15s;
    text-align: left;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .sample-chip:hover:not(:disabled) {
    background: rgba(99,102,241,0.18);
    border-color: rgba(99,102,241,0.4);
    color: #c7d2fe;
  }

  .sample-chip:disabled {
    opacity: 0.4;
    cursor: not-allowed;
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
    background: rgba(99,102,241,0.12);
  }

  .divider-text {
    font-size: 0.75rem;
    color: #64748b;
    white-space: nowrap;
    font-weight: 500;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .drop-zone {
    display: block;
    border: 1.5px dashed rgba(99,102,241,0.25);
    border-radius: 16px;
    padding: 32px 24px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    background: rgba(8,11,20,0.4);
  }

  .drop-zone:hover {
    border-color: rgba(99,102,241,0.5);
    background: rgba(99,102,241,0.06);
  }

  .drop-zone.dragging {
    border-color: #6366f1;
    background: rgba(99,102,241,0.1);
  }

  .drop-zone-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }

  .drop-icon-ring {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: 1.5px solid rgba(99,102,241,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 4px;
    background: rgba(99,102,241,0.08);
  }

  .drop-icon-inner {
    width: 18px;
    height: 14px;
    border: 1.5px solid #6366f1;
    border-radius: 2px;
    position: relative;
  }

  .drop-icon-inner::before {
    content: '';
    position: absolute;
    bottom: -7px;
    left: 50%;
    transform: translateX(-50%);
    width: 1.5px;
    height: 7px;
    background: #6366f1;
  }

  .drop-icon-inner::after {
    content: '';
    position: absolute;
    bottom: -12px;
    left: 50%;
    transform: translateX(-50%);
    width: 8px;
    height: 1.5px;
    background: #6366f1;
  }

  .drop-zone-primary {
    font-size: 0.92rem;
    font-weight: 600;
    color: #cbd5e1;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .drop-zone-secondary {
    font-size: 0.78rem;
    color: #94a3b8;
  }

  .image-preview-wrapper {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(99,102,241,0.2);
  }

  .image-preview {
    width: 100%;
    max-height: 280px;
    object-fit: contain;
    display: block;
    background: rgba(8,11,20,0.6);
  }

  .remove-image-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(8,11,20,0.85);
    color: #e2e8f0;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 100px;
    border: 1px solid rgba(99,102,241,0.2);
    transition: opacity 0.15s;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .remove-image-btn:hover { opacity: 0.75; }

  .error-banner {
    margin-top: 16px;
    padding: 12px 16px;
    background: rgba(220,38,38,0.1);
    border: 1px solid rgba(220,38,38,0.3);
    border-radius: 10px;
    font-size: 0.88rem;
    color: #f87171;
    font-weight: 500;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .check-btn {
    margin-top: 24px;
    width: 100%;
    padding: 15px 24px;
    background: #6366f1;
    color: #ffffff;
    font-size: 1rem;
    font-weight: 700;
    border-radius: 12px;
    letter-spacing: 0.01em;
    transition: background 0.15s, transform 0.1s, box-shadow 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    position: relative;
    overflow: hidden;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .check-btn::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 60%);
    pointer-events: none;
  }

  .check-btn:hover:not(:disabled) {
    background: #4f46e5;
    box-shadow: 0 0 24px rgba(99,102,241,0.4);
    transform: translateY(-1px);
  }

  .check-btn:active:not(:disabled) { transform: scale(0.99) translateY(0); }
  .check-btn:disabled { opacity: 0.35; cursor: not-allowed; }

  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,0.25);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    flex-shrink: 0;
  }

  .spinner-indigo {
    border-color: rgba(99,102,241,0.2);
    border-top-color: #6366f1;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  .disclaimer {
    margin-top: 20px;
    text-align: center;
    font-size: 0.75rem;
    color: #64748b;
    line-height: 1.5;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .hiw-section {
    margin-top: 64px;
    margin-bottom: 16px;
  }

  .hiw-header {
    text-align: center;
    margin-bottom: 36px;
  }

  .hiw-badge {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a5b4fc;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    padding: 4px 12px;
    border-radius: 100px;
    margin-bottom: 12px;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .hiw-title {
    font-size: 1.9rem;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.03em;
    margin-bottom: 8px;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .hiw-subtitle {
    font-size: 0.92rem;
    color: #94a3b8;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .hiw-steps {
    display: flex;
    flex-direction: column;
  }

  .hiw-step {
    display: flex;
    align-items: flex-start;
    background: transparent;
    border: none;
    cursor: pointer;
    text-align: left;
    padding: 0;
    width: 100%;
  }

  .hiw-step-left {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
    width: 56px;
  }

  .hiw-step-num {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 1.5px solid rgba(99,102,241,0.25);
    background: rgba(99,102,241,0.06);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 800;
    color: #64748b;
    letter-spacing: 0.05em;
    transition: border-color 0.2s, background 0.2s, color 0.2s;
    flex-shrink: 0;
    margin-top: 14px;
  }

  .hiw-num-active {
    border-color: #6366f1;
    background: rgba(99,102,241,0.18);
    color: #a5b4fc;
  }

  .hiw-step-connector {
    width: 1.5px;
    flex: 1;
    min-height: 24px;
    background: rgba(99,102,241,0.15);
  }

  .hiw-connector-last { background: transparent; }

  .hiw-step-body {
    flex: 1;
    padding: 14px 0 14px 16px;
    border-bottom: 1px solid rgba(99,102,241,0.08);
  }

  .hiw-step:last-child .hiw-step-body { border-bottom: none; }

  .hiw-step-top {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .hiw-step-title {
    font-size: 0.97rem;
    font-weight: 700;
    color: #e2e8f0;
    flex: 1;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .hiw-chevron {
    font-size: 1.1rem;
    color: #475569;
    transition: transform 0.2s, color 0.2s;
    display: inline-block;
    line-height: 1;
  }

  .hiw-chevron-open {
    transform: rotate(90deg);
    color: #6366f1;
  }

  .hiw-step-desc {
    margin-top: 10px;
    font-size: 0.9rem;
    color: #cbd5e1;
    line-height: 1.7;
    animation: fadeSlide 0.2s ease;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  @keyframes fadeSlide {
    from { opacity: 0; transform: translateY(-4px); }
    to   { opacity: 1; transform: translateY(0); }
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
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    font-size: 0.88rem;
    color: #a5b4fc;
    font-weight: 500;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .flagged-banner {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 18px;
    background: rgba(202,138,4,0.08);
    border: 1px solid rgba(202,138,4,0.25);
    border-radius: 12px;
    font-size: 0.88rem;
    color: #facc15;
    font-weight: 500;
    line-height: 1.5;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .flagged-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #facc15;
    box-shadow: 0 0 8px #facc15;
    flex-shrink: 0;
    animation: pulse-dot 1.5s ease-in-out infinite;
  }

  .result-card {
    background: rgba(15,20,35,0.85);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 24px 60px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
    gap: 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(8px);
  }

  .result-card-glow {
    position: absolute;
    top: -40px;
    left: 50%;
    transform: translateX(-50%);
    width: 200px;
    height: 80px;
    border-radius: 50%;
    opacity: 0.12;
    filter: blur(24px);
    pointer-events: none;
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
    border: 1px solid;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    align-self: flex-start;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .confidence-block {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .confidence-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    white-space: nowrap;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .confidence-bar-track {
    flex: 1;
    height: 5px;
    background: rgba(255,255,255,0.06);
    border-radius: 100px;
    overflow: hidden;
  }

  .confidence-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
  }

  .confidence-value {
    font-size: 0.88rem;
    font-weight: 800;
    white-space: nowrap;
    min-width: 36px;
    text-align: right;
  }

  .explanation-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .explanation-text {
    font-size: 0.97rem;
    color: #cbd5e1;
    line-height: 1.75;
  }

  .sources-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .sources-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .source-link {
    font-size: 0.82rem;
    color: #6366f1;
    text-decoration: none;
    word-break: break-all;
    font-weight: 500;
    transition: color 0.15s;
  }

  .source-link:hover {
    color: #a5b4fc;
    text-decoration: underline;
  }

  .human-review-notice {
    background: rgba(99,102,241,0.06);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 12px;
    padding: 16px 20px;
  }

  .human-review-title {
    font-size: 0.72rem;
    font-weight: 700;
    color: #6366f1;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .human-review-text {
    font-size: 0.85rem;
    color: #94a3b8;
    line-height: 1.65;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .check-another-btn {
    align-self: center;
    padding: 12px 28px;
    background: transparent;
    color: #6366f1;
    font-size: 0.92rem;
    font-weight: 600;
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px;
    transition: background 0.15s, border-color 0.15s;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .check-another-btn:hover {
    background: rgba(99,102,241,0.08);
    border-color: rgba(99,102,241,0.5);
  }

  .footer {
    border-top: 1px solid rgba(99,102,241,0.08);
    padding: 20px 24px;
    text-align: center;
    position: relative;
    z-index: 1;
  }

  .footer p {
    font-size: 0.72rem;
    color: #475569;
    line-height: 1.6;
    font-family: 'Noto Sans Kannada', 'Inter', sans-serif;
  }

  .footer-sub {
    margin-top: 4px;
    font-style: italic;
  }

  .light {
    background: #f8f9fc;
    color: #0f172a;
  }

  .light .bg-grid {
    background-image:
      linear-gradient(rgba(99,102,241,0.06) 1px, transparent 1px),
      linear-gradient(90deg, rgba(99,102,241,0.06) 1px, transparent 1px);
  }

  .light .bg-glow-1 {
    background: radial-gradient(ellipse, rgba(99,102,241,0.1) 0%, transparent 70%);
  }

  .light .bg-glow-2 {
    background: radial-gradient(ellipse, rgba(139,92,246,0.07) 0%, transparent 70%);
  }

  .light .header {
    background: rgba(248,249,252,0.9);
    border-bottom-color: rgba(99,102,241,0.12);
  }

  .light .logo-text { color: #1e1b4b; }

  .light .header-tag {
    color: #4f46e5;
    background: rgba(99,102,241,0.08);
    border-color: rgba(99,102,241,0.2);
  }

  .light .theme-toggle {
    color: #4f46e5;
    background: rgba(99,102,241,0.06);
    border-color: rgba(99,102,241,0.2);
  }

  .light .theme-toggle:hover {
    background: rgba(99,102,241,0.12);
    color: #4338ca;
  }

  .light .hero-title { color: #0f172a; }
  .light .hero-subtitle { color: #475569; }

  .light .hero-badge {
    color: #4f46e5;
    background: rgba(99,102,241,0.07);
    border-color: rgba(99,102,241,0.15);
  }

  .light .checker-card {
    background: #ffffff;
    border-color: rgba(99,102,241,0.15);
    box-shadow: 0 4px 24px rgba(99,102,241,0.08), 0 1px 4px rgba(0,0,0,0.04);
  }

  .light .input-label { color: #475569; }

  .light .claim-textarea {
    background: #f8f9fc;
    border-color: #e2e8f0;
    color: #0f172a;
  }

  .light .claim-textarea:focus {
    background: #ffffff;
    border-color: #6366f1;
  }

  .light .claim-textarea::placeholder { color: #94a3b8; }
  .light .input-hint { color: #94a3b8; }
  .light .samples-label { color: #94a3b8; }

  .light .sample-chip {
    color: #4f46e5;
    background: rgba(99,102,241,0.06);
    border-color: rgba(99,102,241,0.15);
  }

  .light .sample-chip:hover:not(:disabled) {
    background: rgba(99,102,241,0.12);
    border-color: rgba(99,102,241,0.3);
    color: #4338ca;
  }

  .light .divider-line { background: #e2e8f0; }
  .light .divider-text { color: #94a3b8; }

  .light .drop-zone {
    background: #f8f9fc;
    border-color: #e2e8f0;
  }

  .light .drop-zone:hover {
    border-color: #6366f1;
    background: rgba(99,102,241,0.04);
  }

  .light .drop-zone-primary { color: #475569; }
  .light .drop-zone-secondary { color: #94a3b8; }

  .light .error-banner {
    background: #fef2f2;
    border-color: #fca5a5;
    color: #b91c1c;
  }

  .light .check-btn { background: #4f46e5; }

  .light .check-btn:hover:not(:disabled) {
    background: #4338ca;
    box-shadow: 0 0 20px rgba(99,102,241,0.25);
  }

  .light .disclaimer { color: #94a3b8; }

  .light .processing-banner {
    background: rgba(99,102,241,0.06);
    border-color: rgba(99,102,241,0.15);
    color: #4f46e5;
  }

  .light .flagged-banner {
    background: #fefce8;
    border-color: #fde047;
    color: #92400e;
  }

  .light .flagged-dot {
    background: #ca8a04;
    box-shadow: 0 0 8px #ca8a04;
  }

  .light .result-card {
    background: #ffffff;
    border-color: rgba(99,102,241,0.15);
    box-shadow: 0 4px 24px rgba(99,102,241,0.08), 0 1px 4px rgba(0,0,0,0.04);
  }

  .light .explanation-text { color: #475569; }

  .light .confidence-label,
  .light .explanation-label,
  .light .sources-label { color: #94a3b8; }

  .light .confidence-bar-track { background: #e2e8f0; }
  .light .source-link { color: #4f46e5; }
  .light .source-link:hover { color: #4338ca; }

  .light .human-review-notice {
    background: rgba(99,102,241,0.04);
    border-color: rgba(99,102,241,0.12);
  }

  .light .human-review-title { color: #4f46e5; }
  .light .human-review-text { color: #64748b; }

  .light .check-another-btn {
    color: #4f46e5;
    border-color: rgba(99,102,241,0.25);
  }

  .light .check-another-btn:hover {
    background: rgba(99,102,241,0.06);
    border-color: rgba(99,102,241,0.4);
  }

  .light .footer { border-top-color: #e2e8f0; }
  .light .footer p { color: #94a3b8; }
  .light .remove-image-btn { background: rgba(15,23,42,0.75); }
  .light .image-preview { background: #f1f5f9; }

  .light .hiw-title { color: #0f172a; }
  .light .hiw-subtitle { color: #64748b; }

  .light .hiw-badge {
    color: #4f46e5;
    background: rgba(99,102,241,0.07);
    border-color: rgba(99,102,241,0.15);
  }

  .light .hiw-step-num {
    border-color: rgba(99,102,241,0.2);
    background: rgba(99,102,241,0.05);
    color: #94a3b8;
  }

  .light .hiw-num-active {
    border-color: #6366f1;
    background: rgba(99,102,241,0.1);
    color: #4f46e5;
  }

  .light .hiw-step-connector { background: rgba(99,102,241,0.12); }
  .light .hiw-step-body { border-bottom-color: rgba(99,102,241,0.08); }
  .light .hiw-step-title { color: #0f172a; }
  .light .hiw-step-desc { color: #475569; }
  .light .hiw-chevron { color: #94a3b8; }
  .light .hiw-chevron-open { color: #4f46e5; }

  @media (max-width: 600px) {
    .hero-title { font-size: 2.1rem; }
    .checker-card { padding: 22px 18px; }
    .result-card { padding: 22px 18px; }
    .header-tag { display: none; }
    .samples-row { gap: 6px; }
    .hiw-title { font-size: 1.5rem; }
  }
</style>