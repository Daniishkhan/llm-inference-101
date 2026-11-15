// tutor.js — the tutor panel beside every book in docs/book/. No dependencies, no build step.
// Ported from cpp-101's Week 1 tutor.js, in copy-a-prompt mode only: there is no server and no
// network request. Every action (explain a selection, an analogy, a question, a quiz, a hint rung)
// composes one prompt and copies it to the clipboard, to paste into Claude Code in the terminal of
// this repository, where CLAUDE.md applies. Claude explains and hands out hint rungs; it never
// writes your code.
// Loaded after book.js (both `defer`), so book.js's DOMContentLoaded handler, which builds the top
// bar, is registered first and runs first; this file's handler runs after it.
(function () {
  'use strict';

  // =====================================================================
  // 1. Pure helpers (no DOM). Exported on window.bookTutor for tests.
  // =====================================================================
  function escHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  // where: { front, num: '07', title, section, book: 'the Module 1 book (Measure first)' }
  function contextLine(where) {
    const sec = where.section ? `, section "${where.section}".` : '.';
    const book = where.book ? `, of ${where.book}` : '';
    if (where.front || !where.num) return `I'm reading the front page of ${where.book || 'the book'}${sec}`;
    return `I'm reading chapter ${where.num}, "${where.title}"${book}${sec}`;
  }
  function quoteBlock(q) {
    if (q.code) {
      const body = q.text.replace(/\s+$/, '');
      const fence = /```/.test(body) ? '~~~' : '```';
      return fence + (q.lang || 'python') + '\n' + body + '\n' + fence;
    }
    return q.text.trim().split('\n').map((l) => ('> ' + l).trimEnd()).join('\n');
  }
  const QUIZ = 'ask me three short questions, one at a time, and wait for my answer before the next. Start with the first question only.';
  function composePrompt(kind, p) {
    const head = contextLine(p.where) + '\n\n';
    switch (kind) {
      case 'explain': return head + 'Explain this passage more simply, from first principles:\n\n' + quoteBlock(p.quote);
      case 'analogy': return head + 'Give me an everyday analogy for this passage, and say where the analogy breaks down:\n\n' + quoteBlock(p.quote);
      case 'ask': return head + p.question.trim() + '\n\nAbout this passage:\n\n' + quoteBlock(p.quote);
      case 'quiz': return head + (p.quizChapter ? `Quiz me on chapter ${p.quizChapter}: ` : 'Quiz me on this chapter: ') + QUIZ;
      case 'rung': {
        const n = p.rung, t = p.target;
        let s = head + `Hint ladder, rung ${n} of 4, for the ${t.type} "${t.title}".\n\nThe task as the book states it:\n\n` +
          t.text.trim().split('\n').map((l) => ('> ' + l).trimEnd()).join('\n');
        if (p.attempt && p.attempt.trim()) {
          const a = p.attempt.replace(/\s+$/, '');
          const fence = /```/.test(a) ? '~~~' : '```';
          s += '\n\nMy attempt or error:\n\n' + fence + '\n' + a + '\n' + fence;
        }
        return s + `\n\nThe book folds its own four rungs for this ${t.type} in the chapter above; you ` +
          `may read them there. Give me rung ${n} only, and nothing from a later rung.`;
      }
      default: return head + p.message.trim();
    }
  }

  const api = { escHtml, composePrompt, contextLine, quoteBlock };
  if (typeof window !== 'undefined') window.bookTutor = api;
  if (typeof document === 'undefined') return;      // loaded by a test harness without a DOM

  // =====================================================================
  // 2. Page facts and storage
  // =====================================================================
  const P = window.bookPage || {};
  const BOOK = P.BOOK || window.BOOK || {};
  const BOOK_ID = BOOK.id || 'book';
  const here = P.here || location.pathname.split('/').pop() || 'index.html';
  const CHAPTER = P.chapter || null;
  const IS_CHAPTER = !!P.isChapter;
  const NUM = IS_CHAPTER && typeof P.num === 'function' ? P.num(CHAPTER) : '';
  const BOOK_LABEL = BOOK.brand && BOOK.title ? `the ${BOOK.brand} book (${BOOK.title})` : (BOOK.title ? `the book "${BOOK.title}"` : 'the book');
  // The on/off switch is shared by every book (book.js writes it); conversations and rung counters
  // belong to one book, since every book is served from one origin.
  const K = { on: 'llm101-tutor', chat: 'llm101-tutor-chat:' + BOOK_ID + '/', rungs: 'llm101-tutor-rungs:' + BOOK_ID };
  const MAX_MSGS = 40, PROMPT_MAX = 12000;
  function read(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function write(k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
  function readJSON(k, def) { try { const v = JSON.parse(read(k)); return v == null ? def : v; } catch (e) { return def; } }
  const isOn = () => read(K.on) !== 'off';

  const IS_MAC = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || '');
  const HOSTED = () => document.documentElement.dataset.hosted === 'static';
  const ANCHOR_SEL = 'p, li, pre, h2, h3, td, .callout, blockquote';
  const EXCLUDE = '.tutor-panel, .tutor-sel, .tutor-rung, .tutor-marks, .cb-head, .cb-sub, .topbar, .popover';
  const S = { on: true, open: false, msgs: [], sel: null, selAsk: false, selY: 0, pointerDown: false, rungTarget: null, targets: [], started: false };
  const $ = {};   // DOM references

  const COPY_SVG = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5.5" y="5.5" width="8" height="8" rx="1.8"/><path d="M10.5 5.5V4a1.5 1.5 0 0 0-1.5-1.5H4A1.5 1.5 0 0 0 2.5 4v5A1.5 1.5 0 0 0 4 10.5h1.5"/></svg>';
  const ICON = {
    tutor: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4.2 4h11.6c.9 0 1.7.8 1.7 1.7v7c0 .9-.8 1.7-1.7 1.7H9.6L6 17.2v-2.8H4.2c-.9 0-1.7-.8-1.7-1.7v-7C2.5 4.8 3.3 4 4.2 4z"/><path d="M10 6.6l.75 1.65 1.65.75-1.65.75L10 11.4l-.75-1.65L7.6 9l1.65-.75z" stroke-width="1.2"/></svg>',
    close: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M5.5 5.5l9 9M14.5 5.5l-9 9"/></svg>',
    send: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M10 15.5v-11M5.5 9L10 4.5 14.5 9"/></svg>',
    copy: COPY_SVG,
  };

  // =====================================================================
  // 3. Small DOM helpers
  // =====================================================================
  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function headText(h) {
    const c = h.cloneNode(true);
    c.querySelectorAll('.anchor').forEach((a) => a.remove());
    return c.textContent.replace(/\s+/g, ' ').trim();
  }
  const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
  const isNarrow = () => window.matchMedia('(max-width: 559px)').matches;

  // Clipboard API where the page is a secure context (localhost, https), a hidden textarea otherwise
  // (a page opened from a file). Call it inside the click or key handler: browsers allow a copy only
  // while the reader's gesture lasts.
  function copyText(text) {
    const fallback = () => {
      const ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', '');
      ta.style.position = 'fixed'; ta.style.top = '0'; ta.style.left = '0'; ta.style.opacity = '0'; ta.style.pointerEvents = 'none';
      document.body.appendChild(ta); ta.select();
      let ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      ta.remove();
      return ok;
    };
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text).then(() => true, () => fallback());
    return Promise.resolve(fallback());
  }
  function flashLabel(btn, label, back) {
    const span = btn.querySelector('span') || btn;
    span.textContent = label;
    clearTimeout(btn._t);
    btn._t = setTimeout(() => { span.textContent = back; }, 1400);
  }

  // where am I: chapter, and the nearest h2 before an element or at the top of the viewport
  function mainH2s() { return [...document.querySelectorAll('main > h2')]; }
  function sectionOf(node) {
    let cur = null;
    for (const h of mainH2s()) {
      if (h === node || (h.compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING)) cur = h; else break;
    }
    return cur ? headText(cur) : '';
  }
  function viewportH2() {
    let cur = null;
    for (const h of mainH2s()) { if (h.getBoundingClientRect().top < 160) cur = h; else break; }
    return cur;
  }
  function whereFor(node) {
    return {
      front: !IS_CHAPTER, num: NUM, title: IS_CHAPTER ? CHAPTER.title : '', book: BOOK_LABEL,
      section: node ? sectionOf(node) : (viewportH2() ? headText(viewportH2()) : ''),
    };
  }

  // =====================================================================
  // 4. Stored prompts (one list per page of this book)
  // =====================================================================
  function loadMsgs() {
    const v = readJSON(K.chat + here, []);
    return Array.isArray(v) ? v.filter((m) => m && typeof m.text === 'string') : [];
  }
  function saveMsgs() { write(K.chat + here, JSON.stringify(S.msgs.slice(-MAX_MSGS))); }

  // =====================================================================
  // 5. The panel
  // =====================================================================
  function buildButton() {
    const settings = document.querySelector('.topbar .settings-btn');
    if (!settings) return;
    const b = el('button', 'icon-btn tutor-btn');
    b.type = 'button'; b.title = 'Tutor (A)';
    b.setAttribute('aria-label', 'Tutor'); b.setAttribute('aria-expanded', 'false'); b.setAttribute('aria-controls', 'tutor-panel');
    b.innerHTML = ICON.tutor;
    b.addEventListener('click', (e) => { e.stopPropagation(); togglePanel(); });
    settings.before(b);
    $.btn = b;
  }

  function buildPanel() {
    const p = el('aside', 'tutor-panel');
    p.id = 'tutor-panel';
    p.setAttribute('aria-label', 'Tutor');
    p.innerHTML =
      `<div class="tp-head">` +
        `<div class="tp-titles"><div class="tp-name" role="heading" aria-level="2">Tutor</div><p class="tp-ctx"></p></div>` +
        `<div class="tp-actions">` +
          `<button type="button" class="tp-tbtn" data-act="copy" title="Copy every prompt on this page as Markdown">${ICON.copy}<span>Copy all</span></button>` +
          `<button type="button" class="tp-tbtn" data-act="clear" title="Clear this page's prompts">Clear</button>` +
          `<button type="button" class="icon-btn tp-close" data-act="close" title="Close (Esc)" aria-label="Close the tutor">${ICON.close}</button>` +
        `</div>` +
      `</div>` +
      `<div class="tp-log" role="log" aria-live="polite" aria-relevant="additions"></div>` +
      `<div class="tp-rung" hidden></div>` +
      `<form class="tp-foot">` +
        `<textarea rows="1" maxlength="8000" placeholder="Ask about this chapter…" aria-label="Your question"></textarea>` +
        `<button type="submit" class="tp-send" title="Copy the prompt (Enter)" aria-label="Copy the prompt">${ICON.send}</button>` +
      `</form>`;
    document.body.appendChild(p);
    $.panel = p;
    $.ctx = p.querySelector('.tp-ctx');
    $.log = p.querySelector('.tp-log');
    $.rung = p.querySelector('.tp-rung');
    $.form = p.querySelector('.tp-foot');
    $.input = $.form.querySelector('textarea');
    $.send = $.form.querySelector('.tp-send');
    p.inert = true;

    p.addEventListener('click', (e) => e.stopPropagation());
    p.querySelector('[data-act="close"]').addEventListener('click', () => closePanel());
    p.querySelector('[data-act="copy"]').addEventListener('click', (e) => {
      const b = e.currentTarget;
      copyText(allPromptsMarkdown()).then((ok) => flashLabel(b, ok ? 'Copied' : 'Copy failed', 'Copy all'));
    });
    const clear = p.querySelector('[data-act="clear"]');
    clear.addEventListener('click', () => {
      if (!S.msgs.length) return;
      if (!clear.classList.contains('confirm')) {
        clear.classList.add('confirm'); clear.textContent = 'Clear all?';
        clearTimeout(clear._t);
        clear._t = setTimeout(() => { clear.classList.remove('confirm'); clear.textContent = 'Clear'; }, 3000);
        return;
      }
      clearTimeout(clear._t); clear.classList.remove('confirm'); clear.textContent = 'Clear';
      S.msgs = []; saveMsgs(); renderLog(); placeMarks();
    });

    // composer
    const grow = () => { $.input.style.height = 'auto'; $.input.style.height = Math.min($.input.scrollHeight, 200) + 'px'; syncSend(); };
    $.input.addEventListener('input', grow);
    $.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey && !e.isComposing && e.keyCode !== 229) { e.preventDefault(); submitComposer(); }
    });
    $.form.addEventListener('submit', (e) => { e.preventDefault(); submitComposer(); });
    $.grow = grow;

    $.log.addEventListener('click', onLogClick);
    paintContext();
    syncSend();
  }

  function submitComposer() {
    const text = $.input.value.trim();
    if (!text) return;
    $.input.value = ''; $.grow();
    send('chat', { prompt: composePrompt('chat', { where: whereFor(null), message: text }), say: text });
  }
  function syncSend() { if ($.send) $.send.disabled = !$.input.value.trim(); }

  function paintContext() {
    if (!$.ctx) return;
    const where = IS_CHAPTER ? `Chapter ${NUM} · ${CHAPTER.title}` : 'Front page';
    $.ctx.textContent = `${where} · prompts for Claude Code`;
    $.ctx.title = 'Nothing is sent from this page: each prompt is copied for you to paste into Claude Code.';
  }

  function openPanel(focus) {
    if (!S.on || !$.panel) return;
    if (!S.open) {
      S.open = true;
      $.panel.inert = false;
      $.panel.classList.add('open');
      document.documentElement.dataset.tutorOpen = '';
      if ($.btn) { $.btn.setAttribute('aria-expanded', 'true'); $.btn.classList.add('active'); }
      if (!S.msgs.length) renderLog();                 // starter chips follow the viewport
      scrollLogToEnd();
    }
    if (focus && !isNarrow()) $.input.focus({ preventScroll: true });
  }
  function closePanel() {
    if (!S.open) return;
    S.open = false;
    $.panel.classList.remove('open');
    $.panel.inert = true;
    delete document.documentElement.dataset.tutorOpen;
    if ($.btn) { $.btn.setAttribute('aria-expanded', 'false'); $.btn.classList.remove('active'); }
    if ($.panel.contains(document.activeElement) && $.btn) $.btn.focus({ preventScroll: true });
  }
  function togglePanel(focus) { if (S.open) closePanel(); else openPanel(focus !== false); }

  // ---------- the log: your requests, each with its prompt ----------
  const KIND_LABEL = { explain: 'Explain simpler', analogy: 'Analogy', ask: 'Ask', quiz: 'Quiz', chat: '' };
  function kindLabel(m) {
    if (m.kind === 'rung') return m.target ? `Rung ${m.target.rung} of 4` : 'Hint rung';
    return KIND_LABEL[m.kind] || '';
  }
  function renderLog() {
    if (!$.log) return;
    $.log.textContent = '';
    if (!S.msgs.length) { $.log.appendChild(emptyState()); return; }
    S.msgs.forEach((m, i) => $.log.appendChild(renderMsg(m, i)));
  }

  function emptyState() {
    const box = el('div', 'tp-empty');
    box.appendChild(el('p', 'tp-empty-lede', IS_CHAPTER
      ? 'Ask about anything in this chapter. Or select a sentence or a line of code and choose Explain simpler.'
      : 'Ask how to use the book, or where to begin.'));
    box.appendChild(el('p', 'tp-empty-rule', 'Each question becomes a prompt, copied for you to paste into Claude Code in the terminal of this repository, where CLAUDE.md applies. Claude explains, gives analogies and hands out hint rungs. It never writes your code.'));
    const chips = el('div', 'tp-chips');
    for (const c of starters()) {
      const b = el('button', 'tp-chip', c.label);
      b.type = 'button';
      b.addEventListener('click', () => c.run());
      chips.appendChild(b);
    }
    box.appendChild(chips);
    return box;
  }

  function starters() {
    const chat = (label, message) => ({ label, run: () => send('chat', { prompt: composePrompt('chat', { where: whereFor(null), message: message || label }), say: message || label }) });
    if (!IS_CHAPTER) return [chat('Where should I start?'), chat('How do I use this book?')];
    if (BOOK.drillsPage && here === BOOK.drillsPage) {
      const ch = drillChapter();
      return [
        { label: "I'm stuck on a drill", run: () => {
          const d = nearestDrill();
          $.input.value = d ? `I'm stuck on the drill "${d}". ` : "I'm stuck on a drill: ";
          $.grow(); $.input.focus();
          $.input.setSelectionRange($.input.value.length, $.input.value.length);
        } },
        { label: ch ? `Quiz me on chapter ${ch.n}` : 'Quiz me on a chapter', run: () => {
          const c = drillChapter();
          const what = c ? `${c.n}${c.title ? `, "${c.title}"` : ''}` : '';
          send('quiz', { prompt: composePrompt('quiz', { where: whereFor(null), quizChapter: what }), say: c ? `Quiz me on chapter ${c.n}` : 'Quiz me' });
        } },
      ];
    }
    return [
      { label: 'Quiz me on this chapter', run: () => send('quiz', { prompt: composePrompt('quiz', { where: whereFor(null) }), say: 'Quiz me on this chapter' }) },
      chat('What should I be able to explain now?'),
      chat('Explain the hardest idea here with an analogy'),
    ];
  }
  // On the drills page, a section heading that names a chapter ("Practice for chapter 3") says which.
  function drillChapter() {
    const h = viewportH2() || mainH2s()[0];
    const m = h && headText(h).match(/chapter\s+(\d{1,2})/i);
    if (!m) return null;
    const n = String(parseInt(m[1], 10)).padStart(2, '0');
    const c = (P.chapters || []).find((x) => !x.front && typeof P.num === 'function' && P.num(x) === n);
    return { n, title: c ? c.title : '' };
  }
  function nearestDrill() {
    let cur = null;
    for (const h of document.querySelectorAll('main > h3')) { if (h.getBoundingClientRect().top < 200) cur = h; else break; }
    return cur ? headText(cur) : '';
  }

  function renderMsg(m, i) {
    const box = el('div', 'tm tm-user');
    box.dataset.i = String(i);
    const who = el('div', 'tm-who', 'You');
    const kl = kindLabel(m);
    if (kl) who.appendChild(el('span', 'tm-kind', kl));
    box.appendChild(who);
    if (m.target) box.appendChild(el('div', 'tm-target', m.target.type === 'milestone' ? m.target.title : 'Drill · ' + m.target.title));
    const q = m.anchor ? m.anchor.q : m.quote;
    if (q) {
      const chip = el(m.anchor ? 'button' : 'span', 'tm-quote', '“' + q + (q.length >= 80 ? '…' : '') + '”');
      if (m.anchor) { chip.type = 'button'; chip.title = 'Show this passage in the chapter'; chip.dataset.jump = String(i); }
      box.appendChild(chip);
    }
    if (m.say) box.appendChild(el('div', 'tm-text', m.say));
    if (m.attempt) box.appendChild(el('pre', 'tm-attempt', m.attempt));

    const card = el('div', 'tm-offline');
    card.appendChild(el('div', 'tm-off-title', m.copied ? 'Copied to the clipboard' : 'Prompt ready to copy'));
    card.appendChild(el('pre', 'tm-off-prompt', m.text));
    const row = el('div', 'tm-off-row');
    const b = el('button', 'tp-btn primary'); b.type = 'button'; b.dataset.copyPrompt = String(i);
    b.innerHTML = ICON.copy + '<span>Copy prompt</span>';
    row.appendChild(b);
    card.appendChild(row);
    card.appendChild(el('p', 'tm-off-note', HOSTED()
      ? 'Paste it into Claude Code in the terminal of your clone of this repository, where CLAUDE.md applies.'
      : 'Paste it into Claude Code in the terminal of this repository, where CLAUDE.md applies.'));
    const wrap = el('div', 'tm-pair');
    wrap.dataset.i = String(i);
    wrap.append(box, card);
    return wrap;
  }

  function onLogClick(e) {
    const t = e.target.closest('button');
    if (!t || !$.log.contains(t)) return;
    if (t.dataset.copyPrompt) {
      const m = S.msgs[Number(t.dataset.copyPrompt)];
      if (m) copyText(m.text).then((ok) => flashLabel(t, ok ? 'Copied' : 'Copy failed', 'Copy prompt'));
    } else if (t.dataset.jump) {
      const m = S.msgs[Number(t.dataset.jump)];
      const block = m && m.anchor ? resolveAnchor(m.anchor) : null;
      if (block) {
        if (isNarrow()) closePanel();
        const target = block.closest('.cb') || block;
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        flash(target);
      } else {
        flashLabel(t, 'That passage is no longer on this page', t.textContent);
      }
    }
  }

  // Scroll the log only (scrollIntoView would also scroll the page, sideways too on a phone).
  function scrollLogTo(node) {
    const lr = $.log.getBoundingClientRect(), nr = node.getBoundingClientRect();
    const top = $.log.scrollTop + (nr.top - lr.top) - Math.max(0, (lr.height - nr.height) / 2);
    $.log.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
  }
  function scrollLogToEnd() { if ($.log) $.log.scrollTop = $.log.scrollHeight; }

  function allPromptsMarkdown() {
    const title = IS_CHAPTER ? `Chapter ${NUM}, ${CHAPTER.title}` : "The book's front page";
    let out = `# Tutor prompts: ${title}\n\n`;
    for (const m of S.msgs) out += `**${kindLabel(m) || 'Question'}**:\n\n${m.text}\n\n`;
    return out.trim() + '\n';
  }

  // =====================================================================
  // 6. Composing and copying
  // =====================================================================
  function send(kind, opts) {
    if (!S.on) return;
    let prompt = opts.prompt;
    if (prompt.length > PROMPT_MAX) prompt = prompt.slice(0, PROMPT_MAX - 20) + '\n\n(cut short)';
    const m = { kind, text: prompt, say: opts.say || '', copied: false };
    if (opts.anchor) m.anchor = opts.anchor;
    else if (opts.quote) m.quote = opts.quote;
    if (opts.target) m.target = opts.target;
    if (opts.attempt) m.attempt = opts.attempt;
    S.msgs.push(m);
    if (S.msgs.length > MAX_MSGS) S.msgs = S.msgs.slice(-MAX_MSGS);
    const copying = copyText(prompt);              // inside the reader's click or key press
    if (kind === 'rung' && m.target) bumpRung(m.target);
    openPanel(false);
    saveMsgs(); renderLog(); scrollLogToEnd(); placeMarks();
    copying.then((ok) => {
      m.copied = ok; saveMsgs();
      const i = S.msgs.indexOf(m);
      const old = i >= 0 && $.log.querySelector(`.tm-pair[data-i="${i}"]`);
      if (old) old.replaceWith(renderMsg(m, i));
    });
  }

  // =====================================================================
  // 7. Selection menu
  // =====================================================================
  function buildMenu() {
    const m = el('div', 'tutor-sel');
    m.setAttribute('role', 'toolbar'); m.setAttribute('aria-label', 'Ask the tutor about the selection');
    m.hidden = true;
    m.innerHTML =
      `<div class="ts-row">` +
        `<button type="button" data-sel="explain" title="Explain simpler (${IS_MAC ? '⌘↵' : 'Ctrl+Enter'})">Explain simpler <kbd>${IS_MAC ? '⌘↵' : 'Ctrl↵'}</kbd></button>` +
        `<button type="button" data-sel="analogy">Analogy</button>` +
        `<button type="button" data-sel="ask">Ask…</button>` +
      `</div>` +
      `<form class="ts-ask" hidden><input type="text" maxlength="500" placeholder="Ask about this passage…" aria-label="Your question about the selected text">` +
        `<button type="submit" aria-label="Copy the prompt">${ICON.send}</button></form>`;
    document.body.appendChild(m);
    $.menu = m;
    $.menuAsk = m.querySelector('.ts-ask');
    $.menuInput = $.menuAsk.querySelector('input');
    // keep the page selection alive when a button is pressed
    m.addEventListener('mousedown', (e) => { if (!e.target.closest('input')) e.preventDefault(); });
    m.addEventListener('click', (e) => {
      e.stopPropagation();
      const b = e.target.closest('[data-sel]');
      if (!b || !S.sel) return;
      if (b.dataset.sel === 'ask') {
        S.selAsk = true; S.selY = scrollY;
        m.querySelector('.ts-row').hidden = true;
        $.menuAsk.hidden = false;
        $.menuInput.value = '';
        placeMenu(S.sel.rect);
        $.menuInput.focus({ preventScroll: true });
      } else act(b.dataset.sel, S.sel);
    });
    $.menuAsk.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = $.menuInput.value.trim();
      if (q && S.sel) act('ask', S.sel, q);
    });
  }

  function snapshot() {
    const main = document.querySelector('main');
    const sel = window.getSelection && window.getSelection();
    if (!main || !sel || !sel.rangeCount || sel.isCollapsed) return null;
    const raw = sel.toString();
    const trimmed = raw.trim();
    if (trimmed.length < 2 || trimmed.length > 2000) return null;
    const range = sel.getRangeAt(0);
    const common = range.commonAncestorContainer;
    const ce = common.nodeType === 1 ? common : common.parentElement;
    if (!ce || !main.contains(ce) || ce.closest(EXCLUDE)) return null;
    const sc = range.startContainer;
    const startEl = (sc.nodeType === 1 ? (sc.childNodes[range.startOffset] && sc.childNodes[range.startOffset].nodeType === 1 ? sc.childNodes[range.startOffset] : sc) : sc.parentElement) || ce;
    const pre = ce.closest('pre');
    let lang = 'python';
    if (pre) lang = pre.dataset.lang || (pre.classList.contains('shell') ? 'sh' : pre.classList.contains('output') ? 'text' : 'python');
    if (lang === 'shell' || lang === 'bash') lang = 'sh';
    let block = startEl.closest(ANCHOR_SEL);
    if (block && !main.contains(block)) block = null;
    if (!block) block = ce.closest(ANCHOR_SEL);
    const text = pre ? raw.replace(/^\n+|\s+$/g, '') : trimmed.replace(/[ \t ]+/g, ' ').replace(/ *\n */g, '\n').replace(/\n{3,}/g, '\n\n');
    let anchor = null;
    if (block && main.contains(block)) {
      const i = anchorBlocks().indexOf(block);
      if (i >= 0) anchor = { i, q: norm(text).slice(0, 80) };
    }
    const rects = range.getClientRects();
    let rect = range.getBoundingClientRect();
    if ((!rect.width && !rect.height) && rects.length) rect = rects[0];
    return { text, code: !!pre, lang, anchor, rect, where: whereFor(block || ce) };
  }

  function evaluateSelection() {
    if (!S.on || S.selAsk) return;
    const snap = snapshot();
    if (!snap) { hideMenu(); return; }
    S.sel = snap;
    showMenu(snap.rect);
  }
  function showMenu(rect) {
    $.menu.querySelector('.ts-row').hidden = false;
    $.menuAsk.hidden = true;
    $.menu.hidden = false;
    placeMenu(rect);
  }
  function placeMenu(rect) {
    const m = $.menu;
    m.style.visibility = 'hidden';
    m.style.left = '0px'; m.style.top = '0px';
    const w = m.offsetWidth, h = m.offsetHeight;
    const topbar = (document.querySelector('.topbar') || { offsetHeight: 56 }).offsetHeight;
    const coarse = window.matchMedia('(pointer: coarse)').matches;   // phones put their own menu above
    let top = coarse ? rect.bottom + 10 : rect.top - h - 10;
    if (!coarse && top < topbar + 6) top = rect.bottom + 10;
    if (top + h > innerHeight - 6) top = Math.max(topbar + 6, rect.top - h - 10);
    let left = rect.left + rect.width / 2 - w / 2;
    left = Math.max(8, Math.min(left, innerWidth - w - 8));
    m.style.left = Math.round(left) + 'px';
    m.style.top = Math.round(top) + 'px';
    m.style.visibility = '';
  }
  function hideMenu() {
    if (!$.menu || $.menu.hidden) return;
    $.menu.hidden = true;
    S.selAsk = false;
    if ($.menu.contains(document.activeElement)) document.activeElement.blur();
  }
  const menuVisible = () => $.menu && !$.menu.hidden;

  function act(kind, snap, question) {
    hideMenu();
    S.sel = null;
    const p = { where: snap.where, quote: snap, question };
    send(kind, { prompt: composePrompt(kind, p), say: kind === 'ask' ? question : '', anchor: snap.anchor, quote: norm(snap.text).slice(0, 80) });
    const s = window.getSelection && window.getSelection();
    if (s) s.removeAllRanges();
  }

  function wireSelection() {
    let t = 0;
    document.addEventListener('selectionchange', () => {
      if (!S.on || S.pointerDown || S.selAsk) return;
      clearTimeout(t);
      t = setTimeout(evaluateSelection, 180);
    });
    document.addEventListener('pointerdown', (e) => {
      if ($.menu && $.menu.contains(e.target)) return;
      S.pointerDown = true;
      hideMenu();
    }, true);
    document.addEventListener('pointerup', (e) => {
      if (!S.pointerDown) return;
      S.pointerDown = false;
      if ($.menu && $.menu.contains(e.target)) return;
      setTimeout(evaluateSelection, 10);
    }, true);
    document.addEventListener('pointercancel', () => { S.pointerDown = false; }, true);
    addEventListener('scroll', () => {
      if (!menuVisible()) return;
      if (!S.selAsk || Math.abs(scrollY - S.selY) > 60) hideMenu();
    }, { passive: true });
    addEventListener('resize', () => hideMenu());
  }

  // =====================================================================
  // 8. Margin marks: a dot beside each passage you asked about
  // =====================================================================
  let _blocks = null;
  function anchorBlocks() {
    if (!_blocks) { const main = document.querySelector('main'); _blocks = main ? [...main.querySelectorAll(ANCHOR_SEL)] : []; }
    return _blocks;
  }
  function resolveAnchor(a) {
    const blocks = anchorBlocks();
    const probe = norm(a.q || '').slice(0, 40);
    const b = blocks[a.i];
    if (b && (!probe || norm(b.textContent).includes(probe))) return b;
    if (!probe) return null;
    return blocks.find((x) => norm(x.textContent).includes(probe)) || null;
  }
  function buildMarks() {
    const layer = el('div', 'tutor-marks');
    layer.setAttribute('aria-label', 'Passages you asked the tutor about');
    document.body.appendChild(layer);
    $.marks = layer;
    layer.addEventListener('click', (e) => {
      const b = e.target.closest('.tutor-mark');
      if (!b) return;
      e.stopPropagation();
      openPanel(false);
      const node = $.log.querySelector(`.tm-pair[data-i="${b.dataset.i}"]`);
      if (node) { scrollLogTo(node); flash(node.querySelector('.tm') || node); }
    });
    const main = document.querySelector('main');
    if (main && window.ResizeObserver) new ResizeObserver(() => placeMarks()).observe(main);
    addEventListener('resize', () => placeMarks());
    document.addEventListener('toggle', () => placeMarks(), true);
  }
  let _marksRaf = 0;
  function placeMarks() {
    if (!$.marks || _marksRaf) return;
    _marksRaf = requestAnimationFrame(() => {
      _marksRaf = 0;
      const layer = $.marks, main = document.querySelector('main');
      layer.textContent = '';
      if (!S.on || !main) return;
      const latest = new Map();          // block -> index of the latest request anchored there
      S.msgs.forEach((m, i) => {
        if (!m.anchor) return;
        const b = resolveAnchor(m.anchor);
        if (b) latest.set(b, i);
      });
      if (!latest.size) return;
      const mr = main.getBoundingClientRect();
      const contentLeft = mr.left + parseFloat(getComputedStyle(main).paddingLeft || '0');
      latest.forEach((i, block) => {
        const target = block.closest('.cb') || block;
        const r = target.getBoundingClientRect();
        if (!r.height) return;                         // inside a closed <details>
        const left = Math.min(contentLeft, r.left) - 22 + scrollX;
        const top = r.top + scrollY + Math.min(r.height / 2, 16) - 10;
        const dot = el('button', 'tutor-mark');
        dot.type = 'button'; dot.dataset.i = String(i);
        dot.title = 'You asked the tutor about this passage';
        dot.setAttribute('aria-label', 'Open the tutor at your question about this passage');
        dot.style.left = Math.max(2, left) + 'px'; dot.style.top = top + 'px';
        layer.appendChild(dot);
      });
    });
  }
  function flash(node) {
    node.classList.remove('tutor-flash');
    void node.offsetWidth;
    node.classList.add('tutor-flash');
    setTimeout(() => node.classList.remove('tutor-flash'), 1700);
  }

  // =====================================================================
  // 9. Rung buttons (drills and milestones)
  // =====================================================================
  // The build page (BOOK.buildPage) gets one after each h2 whose text starts "Milestone N"; the
  // drills page (BOOK.drillsPage) one after each h3. The next rung per target is stored and goes up
  // each time a rung prompt is copied; there is no rung 5.
  function rungKey(t) { return here + '#' + t.id; }
  function nextRung(t) {
    const r = readJSON(K.rungs, {});
    const n = parseInt(r && r[rungKey(t)], 10);
    return n >= 1 && n <= 5 ? n : 1;
  }
  function setRung(t, n) {
    const r = readJSON(K.rungs, {}) || {};
    if (n <= 1) delete r[rungKey(t)]; else r[rungKey(t)] = Math.min(5, n);
    write(K.rungs, JSON.stringify(r));
    syncRungButtons();
  }
  function bumpRung(target) {
    const t = S.targets.find((x) => x.id === target.id) || target;
    setRung(t, Math.max(nextRung(t), Math.min(5, (target.rung || 1) + 1)));
  }

  function sectionNodes(head, stopTags) {
    const out = [];
    let n = head.nextElementSibling;
    while (n && !stopTags.includes(n.tagName)) { out.push(n); n = n.nextElementSibling; }
    return out;
  }
  function findTargets() {
    const main = document.querySelector('main');
    if (!main) return [];
    let heads = [];
    if (BOOK.drillsPage && here === BOOK.drillsPage) heads = [...main.querySelectorAll(':scope > h3')].map((h) => ({ h, type: 'drill', stop: ['H1', 'H2', 'H3'] }));
    else if (BOOK.buildPage && here === BOOK.buildPage) heads = [...main.querySelectorAll(':scope > h2')].filter((h) => /^Milestone\s+\d+/i.test(headText(h))).map((h) => ({ h, type: 'milestone', stop: ['H1', 'H2'] }));
    return heads.filter((x) => x.h.id).map(({ h, type, stop }) => {
      const nodes = sectionNodes(h, stop);
      let after = null;
      for (const n of nodes) if (n.matches('details.hint') || n.querySelector('details.hint')) after = n;
      if (!after) after = nodes.length ? nodes[nodes.length - 1] : h;
      if (after.matches('.done-box, .chapter-nav')) after = h;
      const wrap = el('div', 'tutor-rung');
      const btn = el('button', 'tr-btn'); btn.type = 'button';
      const reset = el('button', 'tr-reset', 'reset'); reset.type = 'button'; reset.title = 'Start this hint ladder again from rung 1';
      wrap.append(btn, reset);
      after.after(wrap);
      const t = { id: h.id, title: headText(h), type, head: h, stop, wrap, btn, reset };
      btn.addEventListener('click', () => openRungCard(t));
      reset.addEventListener('click', () => setRung(t, 1));
      return t;
    });
  }
  function syncRungButtons() {
    for (const t of S.targets) {
      const n = nextRung(t);
      if (n > 4) {
        t.btn.textContent = 'No rung 5: reread the chapter, or ask for a review';
        t.btn.disabled = true;
      } else {
        t.btn.textContent = `Copy a prompt for rung ${n} of 4`;
        t.btn.disabled = false;
      }
      t.reset.hidden = n <= 1;
      t.wrap.classList.toggle('spent', n > 4);
    }
    if (S.rungTarget && $.rung && !$.rung.hidden) paintRungCard();
  }

  // The visible statement of the drill or milestone. Every details.answer and every details.hint is
  // removed first. The prompt is shown in the panel before it is pasted, so a folded rung copied
  // into it would be read at once: asking for rung 1 must not put rung 4 on the screen. Claude Code
  // can open the chapter itself. Book chrome (code headers, pills, anchors, our button) goes too.
  function targetText(t) {
    const parts = [];
    for (const n of sectionNodes(t.head, t.stop)) {
      if (n.matches('details.answer, details.hint, .tutor-rung')) continue;
      const c = n.cloneNode(true);
      c.querySelectorAll('details.answer, details.hint, .tutor-rung, .cb-head, .cb-sub, .anchor, .pill, script, style').forEach((x) => x.remove());
      let s;
      if (c.matches('.cb') || c.matches('pre')) s = (c.querySelector('pre') || c).textContent.replace(/\s+$/, '');
      else if (c.matches('ul, ol')) s = [...c.children].map((li) => '- ' + norm(li.textContent)).join('\n');
      else s = norm(c.textContent);
      if (s) parts.push(s);
    }
    let text = parts.join('\n\n');
    if (text.length > 6000) text = text.slice(0, 6000).replace(/\s+\S*$/, '') + ' …';
    return text;
  }

  function openRungCard(t) {
    if (!S.on || nextRung(t) > 4) return;
    S.rungTarget = t;
    paintRungCard();
    $.rung.hidden = false;
    openPanel(false);
    if (!isNarrow()) $.rung.querySelector('textarea').focus({ preventScroll: true });
  }
  function paintRungCard() {
    const t = S.rungTarget, n = nextRung(t);
    const box = $.rung;
    box.textContent = '';
    const head = el('div', 'tr-head');
    head.appendChild(el('span', 'tr-pill', `Rung ${Math.min(n, 4)} of 4`));
    head.appendChild(el('span', 'tr-kind', t.type === 'milestone' ? 'Milestone' : 'Drill'));
    const x = el('button', 'icon-btn tr-x'); x.type = 'button'; x.innerHTML = ICON.close; x.setAttribute('aria-label', 'Cancel'); x.title = 'Cancel';
    x.addEventListener('click', closeRungCard);
    head.appendChild(x);
    box.appendChild(head);
    box.appendChild(el('div', 'tr-title', t.title));
    box.appendChild(el('p', 'tr-note', ['Rung 1 says where to look.', 'Rung 2 gives the idea in words.', 'Rung 3 gives the shape: which data structure, which loop, what to test first.', 'Rung 4 is a worked example on a different problem.'][Math.min(n, 4) - 1]));
    const ta = el('textarea', 'tr-attempt');
    ta.rows = 4; ta.maxLength = 5000; ta.placeholder = 'Paste your code or the traceback (optional)';
    ta.setAttribute('aria-label', 'Your code or the traceback (optional)');
    box.appendChild(ta);
    const row = el('div', 'tr-actions');
    row.appendChild(el('span', 'tr-keys', IS_MAC ? '⌘↵ copies' : 'Ctrl+Enter copies'));
    const go = el('button', 'tp-btn primary', 'Copy prompt'); go.type = 'button';
    row.appendChild(go);
    box.appendChild(row);
    const fire = () => {
      const rung = nextRung(t);
      if (rung > 4) return;
      const attempt = ta.value.replace(/\s+$/, '');
      const target = { id: t.id, title: t.title, type: t.type, rung };
      const prompt = composePrompt('rung', { where: whereFor(t.head), rung, target: { type: t.type, title: t.title, text: targetText(t) }, attempt });
      closeRungCard();
      send('rung', { prompt, target, attempt, say: '' });
    };
    go.addEventListener('click', fire);
    ta.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); fire(); }
    });
  }
  function closeRungCard() { S.rungTarget = null; if ($.rung) { $.rung.hidden = true; $.rung.textContent = ''; } }

  // =====================================================================
  // 10. Keyboard, preferences, start-up
  // =====================================================================
  function wireKeys() {
    // Capture phase, so this runs before book.js's own handler (which closes its popover on Escape).
    window.addEventListener('keydown', (e) => {
      if (!S.on) return;
      const tgt = e.target;
      const typing = !!(tgt && tgt.matches && tgt.matches('input, textarea, select, [contenteditable], [contenteditable] *'));
      const inTutor = !!(tgt && tgt.closest && tgt.closest('.tutor-panel, .tutor-sel'));
      if (e.key === 'Escape') {
        if (menuVisible()) { hideMenu(); e.preventDefault(); return; }
        if (tgt && tgt.closest && tgt.closest('.tp-rung')) { e.preventDefault(); closeRungCard(); $.input.focus({ preventScroll: true }); return; }
        const pop = document.querySelector('.popover');
        if (pop && !pop.hidden) return;                                  // book.js closes its menu first
        if (S.open && (!typing || inTutor)) { e.preventDefault(); closePanel(); }
        return;
      }
      if (e.key === 'Enter' && (e.metaKey || e.ctrlKey) && !e.altKey && !e.shiftKey) {
        if (typing) return;
        const snap = (menuVisible() && !S.selAsk && S.sel) || snapshot();
        if (snap) { e.preventDefault(); act('explain', snap); }
        return;
      }
      if (e.metaKey || e.ctrlKey || e.altKey || typing) return;
      if (e.key === 'a' || e.key === 'A') { e.preventDefault(); togglePanel(true); }
    }, true);
  }

  function applyOn() {
    S.on = isOn();
    document.documentElement.dataset.tutor = S.on ? 'on' : 'off';
    if (!S.on) { closePanel(); hideMenu(); closeRungCard(); }
    placeMarks();
  }

  function init() {
    if (S.started || !document.querySelector('header.topbar')) return;   // book.js did not run: stay out of the way
    S.started = true;
    S.msgs = loadMsgs();
    buildButton();
    buildPanel();
    buildMenu();
    buildMarks();
    S.targets = findTargets();
    syncRungButtons();
    wireSelection();
    wireKeys();
    document.addEventListener('click', (e) => { if (menuVisible() && !$.menu.contains(e.target)) hideMenu(); });
    document.addEventListener('prefs-change', applyOn);
    applyOn();
    renderLog();
    placeMarks();
  }

  // A deferred script runs while readyState is already "interactive" but before DOMContentLoaded, and
  // book.js builds the top bar in its own DOMContentLoaded handler. That handler was registered first
  // (book.js executes first), so it runs before ours. Only start at once if the bar already exists.
  if (document.querySelector('header.topbar')) init();
  else document.addEventListener('DOMContentLoaded', init);
})();
