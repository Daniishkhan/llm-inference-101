// book.js — layout and reading tools for every book in docs/book/. No dependencies.
// One shared script: each book's own facts (title, chapter list, storage key, which page holds the
// build milestones and which the drills) come from window.BOOK, set by that book's book-config.js,
// which the page loads just before this file. Ported from cpp-101's Week 1 book.js.
// Builds: top bar, chapter sidebar, "On this page" outline, code-block headers with copy,
// reading settings (theme, text size, panels), progress tracking and keyboard shortcuts.
// Preferences themselves live in theme.js, which runs before the page paints.
(function () {
  'use strict';

  // ---------- this book (single source of truth for nav + progress: book-config.js) ----------
  // window.BOOK = { id, title, brand, tagline, courseHref, storageKey, buildPage, drillsPage,
  //                 chapters: [{ file, title, n?, part?, label?, front? }] }
  // The entry with front: true is the book's front page (index.html): it has no number, is not
  // counted for progress and gets no card; every other entry is a chapter.
  const BOOK = window.BOOK || {};
  const LIST = Array.isArray(BOOK.chapters) ? BOOK.chapters : [];
  const KEY = BOOK.storageKey || 'llm101-' + (BOOK.id || 'book') + '-done';
  const TITLE = BOOK.title || document.title;
  const here = location.pathname.split('/').pop() || 'index.html';
  const idx = LIST.findIndex((c) => c.file === here);
  const cur = idx >= 0 ? LIST[idx] : null;
  const isChapter = !!cur && !cur.front;
  const COUNTED = LIST.filter((c) => !c.front);
  const T = () => window.bookTheme;
  const isDrawer = () => window.matchMedia('(max-width: 959px)').matches;
  const num = (c) => (c && !c.front ? (c.n != null ? String(c.n) : String(COUNTED.indexOf(c)).padStart(2, '0')) : '');
  const frontFile = (LIST.find((c) => c.front) || { file: 'index.html' }).file;

  const ICON = {
    sidebar: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2.5" y="3.5" width="15" height="13" rx="2.5"/><path d="M7.5 3.5v13"/></svg>',
    outline: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M4 5.5h12M7 10h9M7 14.5h9"/></svg>',
    prev: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4.5L6.5 10l5.5 5.5"/></svg>',
    next: '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M8 4.5l5.5 5.5L8 15.5"/></svg>',
    copy: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="5.5" y="5.5" width="8" height="8" rx="1.8"/><path d="M10.5 5.5V4a1.5 1.5 0 0 0-1.5-1.5H4A1.5 1.5 0 0 0 2.5 4v5A1.5 1.5 0 0 0 4 10.5h1.5"/></svg>',
    check: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3.5 8.5l3 3 6-7"/></svg>',
    out: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4.5l3.5 3.5L3 11.5M8.5 11.5H13"/></svg>',
  };
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  function doneSet() {
    try { return new Set(JSON.parse(localStorage.getItem(KEY) || '[]')); } catch (e) { return new Set(); }
  }
  function saveDone(set) {
    try { localStorage.setItem(KEY, JSON.stringify([...set])); } catch (e) {}
    document.dispatchEvent(new CustomEvent('done-change'));
  }
  function doneCount() { const d = doneSet(); return COUNTED.filter((c) => d.has(c.file)).length; }
  function setBar(holder, n) {
    const fill = holder && holder.querySelector('.bar div');
    if (fill) fill.style.width = (COUNTED.length ? (100 * n / COUNTED.length).toFixed(0) : 0) + '%';
  }

  // ---------- top bar ----------
  function buildTopbar() {
    const bar = document.createElement('header');
    bar.className = 'topbar';
    const prev = LIST[idx - 1], next = LIST[idx + 1];
    const crumb = isChapter ? `<b>${esc(num(cur))}</b> · ${esc(cur.title)}` : '';
    const navBtn = (c, dir) => c
      ? `<a class="icon-btn" href="${esc(c.file)}" title="${dir === 'prev' ? 'Previous' : 'Next'}: ${esc(c.title)} (${dir === 'prev' ? '←' : '→'})" aria-label="${dir === 'prev' ? 'Previous' : 'Next'} chapter">${ICON[dir]}</a>`
      : `<span class="icon-btn" aria-disabled="true">${ICON[dir]}</span>`;
    bar.innerHTML =
      `<button class="icon-btn sidebar-toggle" type="button" title="Show or hide chapters ([)" aria-label="Toggle chapter list">${ICON.sidebar}</button>` +
      `<a class="brand" href="${esc(frontFile)}">` + (BOOK.brand ? `<span class="week">${esc(BOOK.brand)}</span>` : '') + `<span class="full">${esc(TITLE)}</span></a>` +
      `<div class="crumb">${crumb}</div>` +
      (idx >= 0 ? navBtn(prev, 'prev') + navBtn(next, 'next') + '<span class="sep"></span>' : '<span class="spacer"></span>') +
      `<button class="icon-btn toc-toggle" type="button" title="Show or hide the outline (O)" aria-label="Toggle outline">${ICON.outline}</button>` +
      `<button class="icon-btn settings-btn" type="button" title="Reading settings (,)" aria-haspopup="dialog" aria-expanded="false"><span class="aa">Aa</span></button>` +
      `<div class="readbar"></div>`;
    document.body.prepend(bar);
    bar.querySelector('.sidebar-toggle').addEventListener('click', toggleSidebar);
    bar.querySelector('.toc-toggle').addEventListener('click', () => T() && T().setToc(T().getToc() === 'hidden' ? 'shown' : 'hidden'));
    bar.querySelector('.settings-btn').addEventListener('click', (e) => { e.stopPropagation(); togglePopover(); });
    syncToggles();
  }
  function syncToggles() {
    const sb = document.querySelector('.sidebar-toggle'), tc = document.querySelector('.toc-toggle');
    if (!T()) return;
    if (sb) sb.classList.toggle('active', isDrawer() ? document.documentElement.dataset.drawer === 'open' : T().getSidebar() === 'open');
    if (tc) tc.classList.toggle('active', T().getToc() === 'shown');
  }
  function toggleSidebar() {
    if (isDrawer()) {
      const open = document.documentElement.dataset.drawer === 'open';
      setDrawer(!open);
    } else if (T()) {
      T().setSidebar(T().getSidebar() === 'closed' ? 'open' : 'closed');
    }
    syncToggles();
  }
  function setDrawer(open) {
    const root = document.documentElement;
    let bd = document.querySelector('.drawer-backdrop');
    if (open) {
      root.dataset.drawer = 'open';
      if (!bd) { bd = document.createElement('div'); bd.className = 'drawer-backdrop'; bd.addEventListener('click', () => setDrawer(false)); document.body.appendChild(bd); }
    } else {
      delete root.dataset.drawer;
      if (bd) bd.remove();
    }
    syncToggles();
  }

  // reading progress bar + crumb visibility
  function watchScroll() {
    const bar = document.querySelector('.readbar'), crumb = document.querySelector('.crumb'), h1 = document.querySelector('main h1');
    let ticking = false;
    const update = () => {
      ticking = false;
      const max = document.documentElement.scrollHeight - innerHeight;
      if (bar) bar.style.width = (max > 0 ? Math.min(100, 100 * scrollY / max) : 0) + '%';
      if (crumb && h1) crumb.classList.toggle('show', h1.getBoundingClientRect().bottom < 60);
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  // ---------- sidebar ----------
  let sidebarWired = false;
  function buildSidebar() {
    const nav = document.querySelector('nav.sidebar');
    if (!nav) return;
    const done = doneSet();
    const n = doneCount();
    const tagline = BOOK.tagline ? esc(BOOK.tagline) : '';
    let html = `<div class="side-head"><div class="t">${esc(TITLE)}</div>` +
      (tagline ? `<div class="s">${BOOK.courseHref ? `<a href="${esc(BOOK.courseHref)}">${tagline}</a>` : tagline}</div>` : '') +
      `<div class="side-progress">${n} of ${COUNTED.length} done<div class="bar"><div></div></div></div></div><ol>`;
    LIST.forEach((c) => {
      if (c.part) html += `</ol><p class="part">${esc(c.part)}</p><ol>`;
      const cls = [c.file === here ? 'current' : '', done.has(c.file) && !c.front ? 'done' : ''].join(' ').trim();
      html += `<li class="${cls}"><a href="${esc(c.file)}"${c.file === here ? ' aria-current="page"' : ''}><span class="n">${esc(num(c))}</span><span>${esc(c.title)}</span><span class="tick">${ICON.check}</span></a></li>`;
    });
    html += '</ol>';
    const keep = nav.scrollTop;
    nav.innerHTML = html;
    setBar(nav.querySelector('.side-progress'), n);
    nav.scrollTop = keep;
    if (!sidebarWired) {
      sidebarWired = true;
      nav.addEventListener('click', (e) => { if (e.target.closest('a') && isDrawer()) setDrawer(false); });
    }
  }
  function centreCurrentInSidebar() {
    const nav = document.querySelector('nav.sidebar'), li = nav && nav.querySelector('li.current');
    if (li) nav.scrollTop = li.offsetTop - nav.clientHeight / 2 + li.offsetHeight / 2;  // scrolls the sidebar only, never the page
  }

  // ---------- "On this page" outline ----------
  function buildToc() {
    const main = document.querySelector('main');
    const heads = [...document.querySelectorAll('main > h2')];
    if (!main || heads.length < 2) { document.querySelector('.toc-toggle')?.remove(); return; }
    const words = (main.innerText || '').split(/\s+/).length;
    const aside = document.createElement('aside');
    aside.className = 'toc';
    aside.setAttribute('aria-label', 'On this page');
    aside.innerHTML = `<p class="toc-title">On this page</p><p class="meta">About ${Math.max(1, Math.round(words / 230))} min of reading</p><ol>` +
      heads.map((h) => { const c = h.cloneNode(true); c.querySelectorAll('.anchor').forEach((a) => a.remove()); return `<li><a href="#${esc(h.id)}">${esc(c.textContent.trim())}</a></li>`; }).join('') +
      '</ol><div class="toc-actions"><a href="#" class="to-top">↑ Back to top</a>' +
      (isChapter ? `<label><input type="checkbox" class="done-mirror"> Chapter done</label>` : '') + '</div>';
    document.body.appendChild(aside);
    aside.querySelector('.to-top').addEventListener('click', (e) => { e.preventDefault(); scrollTo({ top: 0, behavior: 'smooth' }); history.replaceState(null, '', location.pathname); });
    const links = new Map(heads.map((h) => [h, aside.querySelector(`a[href="#${CSS.escape(h.id)}"]`)]));
    const setActive = () => {
      let at = heads[0];
      for (const h of heads) { if (h.getBoundingClientRect().top < 140) at = h; else break; }
      links.forEach((a, h) => a && a.classList.toggle('active', h === at));
    };
    let ticking = false;
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { ticking = false; setActive(); }); } }, { passive: true });
    setActive();
  }

  // ---------- end of chapter: done toggle + prev/next ----------
  function buildChapterEnd() {
    const main = document.querySelector('main');
    if (!isChapter || !main) return;
    const box = document.createElement('label');
    box.className = 'done-box';
    box.innerHTML = `<input type="checkbox"> <span>Mark this chapter as done. Your progress is saved in this browser.</span>`;
    main.appendChild(box);
    const nav = document.createElement('div');
    nav.className = 'chapter-nav';
    const prev = LIST[idx - 1], next = LIST[idx + 1];
    nav.innerHTML = (prev ? `<a class="prev" href="${esc(prev.file)}"><small>← Previous</small>${esc(prev.title)}</a>` : '') +
                    (next ? `<a class="next" href="${esc(next.file)}"><small>Next →</small>${esc(next.title)}</a>` : `<a class="next" href="${esc(frontFile)}"><small>Back to</small>Contents</a>`);
    main.appendChild(nav);
    const sync = () => {
      const d = doneSet().has(here);
      document.querySelectorAll('.done-box input, .done-mirror').forEach((i) => { i.checked = d; });
      box.classList.toggle('is-done', d);
    };
    document.addEventListener('change', (e) => {
      if (!e.target.matches('.done-box input, .done-mirror')) return;
      const d = doneSet(); if (e.target.checked) d.add(here); else d.delete(here); saveDone(d);
    });
    document.addEventListener('done-change', sync);
    sync();
  }

  // ---------- index page cards ----------
  // <div class="toc-cards" data-auto data-blurb0="…" data-blurb1="…">: one card per chapter, where
  // data-blurbK is the blurb of the K-th chapter after the front page (K from 0).
  // <div class="progress"></div> anywhere on the page shows "N of M marked done".
  function buildIndex() {
    const holder = document.querySelector('.toc-cards[data-auto]');
    const prog = document.querySelector('.progress');
    if (!holder && !prog) return;
    const render = () => {
      const done = doneSet();
      if (holder) {
        holder.innerHTML = COUNTED.map((c, i) => {
          const blurb = holder.dataset[`blurb${i}`] || '';
          return `<a href="${esc(c.file)}" class="${done.has(c.file) ? 'done' : ''}"><span class="n">${esc(c.label || 'Chapter ' + num(c))}</span><h3>${esc(c.title)}</h3><p>${esc(blurb)}</p></a>`;
        }).join('');
      }
      if (prog) {
        const n = doneCount();
        prog.innerHTML = `${n} of ${COUNTED.length} marked done<div class="bar"><div></div></div>`;
        setBar(prog, n);
      }
    };
    render();
    window.addEventListener('storage', (e) => { if (e.key === KEY) render(); });
  }

  // ---------- heading anchors ----------
  // The slug rule, kept identical in tools/book-check.py (slug()): the heading's text, trimmed,
  // lower-cased, every run of characters other than a-z and 0-9 turned into one hyphen, and a
  // hyphen at either end dropped. "Milestone 1: time_calls" -> "milestone-1-time-calls".
  // A heading with its own id keeps it.
  function slug(text) { return text.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, ''); }
  function anchors() {
    document.querySelectorAll('main h2, main h3').forEach((h) => {
      if (h.closest('.toc-cards')) return;
      if (!h.id) h.id = slug(h.textContent);
      const a = document.createElement('a'); a.className = 'anchor'; a.href = '#' + h.id; a.textContent = '#';
      a.setAttribute('aria-label', 'Link to this section');
      h.appendChild(a);
    });
  }

  // ---------- highlighting ----------
  const PY_KW = new Set('False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield'.split(' '));
  const PY_SOFT = new Set(['match', 'case']);   // keywords only at the start of a statement
  const PY_BUILTIN = new Set(('abs aiter all anext any ascii bin bool breakpoint bytearray bytes callable chr classmethod compile complex delattr dict dir divmod enumerate eval exec filter float format frozenset getattr globals hasattr hash help hex id input int isinstance issubclass iter len list locals map max memoryview min next object oct open ord pow print property range repr reversed round set setattr slice sorted staticmethod str sum super tuple type vars zip __import__ ' +
    'BaseException Exception ArithmeticError AssertionError AttributeError EOFError FileNotFoundError ImportError IndexError KeyError KeyboardInterrupt LookupError MemoryError ModuleNotFoundError NameError NotImplemented NotImplementedError OSError OverflowError RecursionError RuntimeError StopIteration SyntaxError SystemExit TimeoutError TypeError UnicodeDecodeError ValueError ZeroDivisionError Ellipsis __name__ __file__').split(' '));
  const isIdStart = (c) => /[A-Za-z_]/.test(c || '');
  const isIdChar = (c) => /[A-Za-z0-9_]/.test(c || '');
  const STR_START = /^(?:[rRbBuUfF]|[rR][bBfF]|[bBfF][rR])?(?:'|")/;

  // End index of the string literal starting at i (at its prefix, if any). Escapes are skipped,
  // even in raw strings (r"\"" is one string); an f-string's {fields} may hold nested strings.
  function stringEnd(src, i) {
    const n = src.length;
    let j = i;
    while (/[rRbBuUfF]/.test(src[j])) j++;
    const isF = /f/i.test(src.slice(i, j));
    const q = src.startsWith(src[j].repeat(3), j) ? src[j].repeat(3) : src[j];
    j += q.length;
    let depth = 0;
    while (j < n) {
      const c = src[j];
      if (depth === 0) {
        if (c === '\\') { j += 2; continue; }
        if (src.startsWith(q, j)) return j + q.length;
        if (q.length === 1 && c === '\n') return j;               // unterminated: stop at the line end
        if (isF && c === '{') { if (src[j + 1] === '{') { j += 2; continue; } depth = 1; }
        j++;
      } else {
        if (c === '{') depth++;
        else if (c === '}') depth--;
        else if (c === '"' || c === "'") { j = stringEnd(src, j); continue; }   // nested string (Python 3.12+)
        else if (c === '\n' && q.length === 1) return j;             // unclosed field: stop at the line end
        j++;
      }
    }
    return n;
  }
  // An f-string: literal parts as strings, each {field} highlighted as Python, its format spec
  // (after a top-level : or !) as part of the string.
  function highlightFString(lit) {
    let out = '', buf = '', i = 0;
    const flush = () => { if (buf) { out += `<span class="hl-str">${esc(buf)}</span>`; buf = ''; } };
    while (i < lit.length) {
      const c = lit[i];
      if (c === '{' && lit[i + 1] === '{') { buf += '{{'; i += 2; continue; }
      if (c !== '{') { buf += c; i++; continue; }
      // a replacement field: find its end and the start of its spec
      let j = i + 1, depth = 1, spec = -1, bracket = 0;
      while (j < lit.length && depth > 0) {
        const d = lit[j];
        if (d === '"' || d === "'") { j = stringEnd(lit, j); continue; }
        if (d === '{') depth++;
        else if (d === '}') { depth--; if (depth === 0) break; }
        else if ('(['.includes(d)) bracket++;
        else if (')]'.includes(d)) bracket--;
        else if (spec < 0 && depth === 1 && bracket === 0 && (d === ':' || d === '!') && lit[j + 1] !== '=') spec = j;
        j++;
      }
      flush();
      const expr = lit.slice(i + 1, spec < 0 ? j : spec);
      out += '{' + highlightPython(expr) + (spec < 0 ? '' : `<span class="hl-str">${esc(lit.slice(spec, j))}</span>`) + (j < lit.length ? '}' : '');
      i = j + 1;
    }
    flush();
    return out;
  }

  function highlightPython(src) {
    let out = '', i = 0, lineStart = true, after = '';   // after: the keyword just seen (def, class)
    const n = src.length;
    while (i < n) {
      const c = src[i];
      if (c === '\n') { out += '\n'; i++; lineStart = true; continue; }
      if ((c === ' ' || c === '\t') && lineStart) { out += c; i++; continue; }
      // comment
      if (c === '#') { let j = src.indexOf('\n', i); if (j < 0) j = n; out += `<span class="hl-cm">${esc(src.slice(i, j))}</span>`; i = j; continue; }
      // decorator, at the start of a line
      if (c === '@' && lineStart && isIdStart(src[i + 1])) {
        let j = i + 1; while (j < n && /[A-Za-z0-9_.]/.test(src[j])) j++;
        out += `<span class="hl-pp">${esc(src.slice(i, j))}</span>`; i = j; lineStart = false; continue;
      }
      const wasLineStart = lineStart;
      lineStart = false;
      // string, with or without a prefix (r, b, f, u, rb, fr ...)
      const m = !isIdChar(src[i - 1]) && STR_START.exec(src.slice(i, i + 4));
      if (m) {
        const j = stringEnd(src, i);
        const lit = src.slice(i, j);
        out += /^[a-z]*f/i.test(m[0]) ? highlightFString(lit) : `<span class="hl-str">${esc(lit)}</span>`;
        i = j; after = ''; continue;
      }
      // number: 42, 3.14, .5, 1_000, 0x1f, 1e-3, 2j
      if ((/[0-9]/.test(c) || (c === '.' && /[0-9]/.test(src[i + 1] || ''))) && !isIdChar(src[i - 1])) {
        let j = i;
        while (j < n && (/[0-9A-Za-z_.]/.test(src[j]) || ((src[j] === '-' || src[j] === '+') && /[eE]/.test(src[j - 1]) && !/^0[xX]/.test(src.slice(i, j))))) j++;
        out += `<span class="hl-num">${esc(src.slice(i, j))}</span>`; i = j; continue;
      }
      // identifier
      if (isIdStart(c)) {
        let j = i; while (j < n && isIdChar(src[j])) j++;
        const w = src.slice(i, j);
        let k = j; while (k < n && src[k] === ' ') k++;
        const attr = src[i - 1] === '.';
        if (after === 'def') out += `<span class="hl-fn">${w}</span>`;
        else if (after === 'class') out += `<span class="hl-ty">${w}</span>`;
        else if (!attr && (PY_KW.has(w) || (wasLineStart && PY_SOFT.has(w) && src[j] === ' ' && !/[=.:,)\]]/.test(src[k] || '')))) out += `<span class="hl-kw">${w}</span>`;
        else if (!attr && PY_BUILTIN.has(w)) out += `<span class="hl-ty">${w}</span>`;
        else if (src[k] === '(') out += `<span class="hl-fn">${w}</span>`;
        else out += esc(w);
        after = w === 'def' || w === 'class' ? w : '';
        i = j; continue;
      }
      if (c !== ' ' && c !== '\t') after = '';
      out += esc(c); i++;
    }
    return out;
  }
  function highlightShell(src) {
    return src.split('\n').map((line) => {
      if (/^\$ /.test(line)) return `<span class="hl-prompt">$ </span>${esc(line.slice(2))}`;
      return `<span class="hl-cm">${esc(line)}</span>`;
    }).join('\n');
  }
  function highlightAll() {
    document.querySelectorAll('pre.code, pre.shell').forEach((pre) => {
      const code = pre.querySelector('code') || pre;
      const lang = pre.dataset.lang || (pre.classList.contains('shell') ? 'shell' : 'python');
      const raw = code.textContent.replace(/\n$/, '');
      if (lang === 'python' || lang === 'py') code.innerHTML = highlightPython(raw);
      else if (lang === 'shell' || lang === 'bash' || lang === 'sh') code.innerHTML = highlightShell(raw);
      else code.textContent = raw;
    });
  }

  // ---------- code blocks: header with language, file name, badge, copy; attach output ----------
  function copyText(pre) {
    const code = pre.querySelector('code') || pre;
    let text = code.textContent;
    if (pre.classList.contains('shell')) text = text.split('\n').filter((l) => /^\$ /.test(l)).map((l) => l.slice(2)).join('\n') || text;
    return text.replace(/\n$/, '');
  }
  function makeHead(lang, title, badge, pre) {
    const head = document.createElement('div');
    head.className = 'cb-head';
    head.innerHTML = `<span class="cb-lang">${esc(lang)}</span>` + (title ? `<span class="cb-title">${esc(title)}</span>` : '') + (badge || '');
    if (pre) {
      const btn = document.createElement('button');
      btn.type = 'button'; btn.className = 'cb-copy'; btn.innerHTML = ICON.copy + '<span>Copy</span>';
      btn.title = pre.classList.contains('shell') ? 'Copy the commands (without the $)' : 'Copy the code';
      btn.addEventListener('click', () => {
        navigator.clipboard.writeText(copyText(pre)).then(() => {
          btn.querySelector('span').textContent = 'Copied'; setTimeout(() => (btn.querySelector('span').textContent = 'Copy'), 1300);
        });
      });
      head.appendChild(btn);
    }
    return head;
  }
  function wrapCodeBlocks() {
    const LANG = { python: 'Python', py: 'Python', shell: 'Shell', bash: 'Shell', sh: 'Shell', text: 'Text', toml: 'TOML', json: 'JSON' };
    document.querySelectorAll('main pre.code, main pre.shell, main pre.output').forEach((pre) => {
      if (pre.parentElement.classList.contains('cb')) return;   // already attached as an output
      const wrap = document.createElement('div');
      pre.before(wrap);
      if (pre.classList.contains('output')) {
        wrap.className = 'cb cb-output';
        wrap.append(makeHead('Out', here === BOOK.drillsPage ? 'Expected output' : 'Output', '', null), pre);
        return;
      }
      const shell = pre.classList.contains('shell');
      const lang = shell ? 'Shell' : (LANG[pre.dataset.lang || 'python'] || pre.dataset.lang);
      const check = pre.dataset.check;
      let badge = '';
      if (check === 'error') badge = '<span class="cb-badge error">Raises an error, on purpose</span>';
      else if (check === 'fragment') badge = '<span class="cb-badge quiet">Excerpt</span>';
      wrap.className = 'cb ' + (shell ? 'cb-shell' : 'cb-code');
      wrap.append(makeHead(lang, shell ? 'Terminal' : (pre.dataset.file || ''), badge, pre), pre);
      // A following <pre class="output"> belongs to this block: show it underneath, in the same card.
      const next = wrap.nextElementSibling;
      if (next && next.matches('pre.output')) {
        const sub = document.createElement('div');
        sub.className = 'cb-sub';
        sub.innerHTML = ICON.out + (check === 'error' ? 'What Python says' : (shell ? 'What you see' : 'Output'));
        wrap.append(sub, next);
      }
    });
  }
  function wrapTables() {
    document.querySelectorAll('main table').forEach((t) => {
      if (t.parentElement.classList.contains('table-wrap')) return;
      const w = document.createElement('div'); w.className = 'table-wrap'; t.before(w); w.appendChild(t);
    });
  }
  function pills() {
    document.querySelectorAll('details.hint > summary, details.answer > summary').forEach((s) => {
      if (s.querySelector('.pill')) return;
      const isHint = s.parentElement.classList.contains('hint');
      const word = isHint ? 'Hint' : 'Answer';
      // A summary that only says "Answer" or "Show the answer" would repeat the pill: give it a plain label instead.
      const m = s.textContent.match(/^\s*(?:show(?: the| me the)?\s+)?(answer|solution|hint)s?\s*[.:]?\s*$/i);
      if (m) s.textContent = isHint ? 'Show a hint' : (m[1].toLowerCase() === 'solution' ? 'Show the solution' : 'Show the answer');
      const p = document.createElement('span');
      p.className = 'pill'; p.textContent = word;
      s.prepend(p);
    });
  }

  // ---------- reading settings popover ----------
  function buildPopover() {
    const pop = document.createElement('div');
    pop.className = 'popover'; pop.hidden = true; pop.setAttribute('role', 'dialog'); pop.setAttribute('aria-label', 'Reading settings');
    document.body.appendChild(pop);
    pop.addEventListener('click', (e) => e.stopPropagation());
    document.addEventListener('click', () => { if (!pop.hidden) togglePopover(false); });
    renderPopover();
    document.addEventListener('prefs-change', () => { renderPopover(); syncToggles(); });
  }
  function renderPopover() {
    const pop = document.querySelector('.popover');
    const t = T();
    if (!pop || !t) return;
    const curTheme = t.get(), size = t.getSize(), tutorOn = getTutor() === 'on';
    pop.innerHTML =
      `<section><h4>Theme</h4><div class="theme-grid">` +
      t.THEMES.map((k) => `<button type="button" class="theme-opt" data-theme-opt="${k}" aria-pressed="${k === curTheme}">` +
        `<span class="sw sw-${k}"></span>` +
        `<span><span class="nm">${t.LABELS[k]}</span><br><span class="ds">${t.NOTES[k]}</span></span></button>`).join('') +
      `</div></section>` +
      `<section><h4>Text size</h4><div class="stepper"><button type="button" data-size="-1" aria-label="Smaller text">A−</button>` +
      `<span class="val">${size}px${size === t.SIZE.def ? ' · default' : ''}</span>` +
      `<button type="button" data-size="1" aria-label="Larger text">A+</button></div></section>` +
      `<section><h4>Layout</h4>` +
      `<label class="switch-row"><span>Chapter list</span><span class="switch"><input type="checkbox" data-pref="sidebar" ${t.getSidebar() === 'open' ? 'checked' : ''}><span></span></span></label>` +
      `<label class="switch-row"><span>On this page outline</span><span class="switch"><input type="checkbox" data-pref="toc" ${t.getToc() === 'shown' ? 'checked' : ''}><span></span></span></label>` +
      `</section>` +
      `<section><h4>Tutor</h4>` +
      `<label class="switch-row"><span>Tutor prompts</span><span class="switch"><input type="checkbox" data-pref="tutor" ${tutorOn ? 'checked' : ''}><span></span></span></label>` +
      `<p class="pop-note">${tutorOn ? 'Composes a question for Claude Code: explanations, analogies, hint rungs. Claude never writes your code.' : 'Off: just the book.'}</p>` +
      `</section>` +
      `<section><h4>Keyboard</h4><div class="keys">` +
      `<kbd>←</kbd><span>Previous chapter</span><kbd>→</kbd><span>Next chapter</span>` +
      `<kbd>[</kbd><span>Show or hide the chapter list</span><kbd>O</kbd><span>Show or hide the outline</span>` +
      `<kbd>T</kbd><span>Next theme</span><kbd>+</kbd><span>Larger text (<kbd>−</kbd> smaller)</span>` +
      (tutorOn ? `<kbd>A</kbd><span>Open or close the tutor</span><kbd>${IS_MAC ? '⌘↵' : 'Ctrl↵'}</kbd><span>Explain the selected text</span>` : '') +
      `<kbd>,</kbd><span>This menu</span><kbd>Esc</kbd><span>Close</span></div></section>`;
    pop.querySelectorAll('[data-theme-opt]').forEach((b) => b.addEventListener('click', () => t.set(b.dataset.themeOpt)));
    pop.querySelectorAll('[data-size]').forEach((b) => b.addEventListener('click', () => t.setSize(t.getSize() + Number(b.dataset.size))));
    pop.querySelector('[data-pref="sidebar"]').addEventListener('change', (e) => { t.setSidebar(e.target.checked ? 'open' : 'closed'); });
    pop.querySelector('[data-pref="toc"]').addEventListener('change', (e) => { t.setToc(e.target.checked ? 'shown' : 'hidden'); });
    pop.querySelector('[data-pref="tutor"]').addEventListener('change', (e) => { setTutor(e.target.checked ? 'on' : 'off'); });
  }
  // The tutor switch (tutor.js does the rest). "off" means just the book: tutor.js hides everything it added.
  const TUTOR_KEY = 'llm101-tutor';
  const IS_MAC = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || '');
  function getTutor() { try { return localStorage.getItem(TUTOR_KEY) === 'off' ? 'off' : 'on'; } catch (e) { return 'on'; } }
  function setTutor(v) {
    try { localStorage.setItem(TUTOR_KEY, v === 'off' ? 'off' : 'on'); } catch (e) {}
    document.dispatchEvent(new CustomEvent('prefs-change'));
  }
  function togglePopover(force) {
    const pop = document.querySelector('.popover'), btn = document.querySelector('.settings-btn');
    if (!pop) return;
    const open = force === undefined ? pop.hidden : force;
    pop.hidden = !open;
    if (btn) btn.setAttribute('aria-expanded', String(open));
    if (open) pop.querySelector('[aria-pressed="true"]')?.focus({ preventScroll: true });
  }

  // ---------- keyboard ----------
  function keys() {
    document.addEventListener('keydown', (e) => {
      if (e.metaKey || e.ctrlKey || e.altKey || e.target.matches('input, textarea, select, [contenteditable]')) return;
      const t = T();
      const prev = LIST[idx - 1], next = LIST[idx + 1];
      switch (e.key) {
        case 'ArrowLeft': if (idx >= 0 && prev) location.href = prev.file; break;
        case 'ArrowRight': if (idx >= 0 && next) location.href = next.file; break;
        case '[': case '\\': toggleSidebar(); break;
        case 'o': case 'O': if (t) t.setToc(t.getToc() === 'hidden' ? 'shown' : 'hidden'); break;
        case 't': case 'T': if (t) t.cycle(); break;
        case '+': case '=': if (t) t.setSize(t.getSize() + 1); break;
        case '-': case '_': if (t) t.setSize(t.getSize() - 1); break;
        case ',': togglePopover(); break;
        case 'Escape': togglePopover(false); setDrawer(false); break;
        default: return;
      }
    });
    window.matchMedia('(max-width: 959px)').addEventListener('change', () => { setDrawer(false); syncToggles(); });
  }

  // Shared with tutor.js (loaded after this file): the book, where we are, and a few helpers.
  // chapter is the current entry of BOOK.chapters (null when this page is not in the list).
  window.bookPage = { BOOK, chapters: LIST, idx, here, chapter: cur, isChapter, num, esc, slug, highlightPython, togglePopover };

  document.addEventListener('DOMContentLoaded', () => {
    highlightAll();
    wrapCodeBlocks();
    wrapTables();
    pills();
    anchors();
    buildTopbar();
    buildSidebar();
    buildIndex();
    buildChapterEnd();
    buildToc();
    buildPopover();
    keys();
    watchScroll();
    centreCurrentInSidebar();
    document.addEventListener('done-change', buildSidebar);
    // Deep links: the sticky top bar must not cover the target heading.
    if (location.hash) { const el = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (el) el.scrollIntoView(); }
  });
})();
