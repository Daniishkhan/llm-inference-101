// book-config.js — this book's facts, read by ../assets/book.js and ../assets/tutor.js.
// Loaded (defer) just before book.js. The chapter list is the single source of truth for the
// sidebar, prev and next, the contents cards and progress. `part` starts a group in the sidebar.
window.BOOK = {
  id: '02-tokenizer',
  title: 'Tokenizer',
  brand: 'Module 2',
  tagline: 'Module 2 of 20 · LLM inference in Python',
  courseHref: '../index.html',
  storageKey: 'llm101-02-tokenizer-done',
  buildPage: '08-build-the-tokenizer.html',
  drillsPage: '07-drills.html',
  chapters: [
    { file: 'index.html', title: 'Contents', front: true },
    { file: '00-start-here.html', n: '00', title: 'Start here', part: 'Orientation' },
    { file: '01-bytes-and-utf8.html', n: '01', title: 'Bytes and UTF-8', part: 'From text to tokens' },
    { file: '02-pairs-and-merges.html', n: '02', title: 'Pairs and merges' },
    { file: '03-encoding-by-rank.html', n: '03', title: 'Encoding by rank' },
    { file: '04-gpt2s-tokenizer.html', n: '04', title: "GPT-2's tokenizer", part: 'The real thing' },
    { file: '05-heaps-and-linked-lists.html', n: '05', title: 'Heaps and linked lists' },
    { file: '06-tokens-as-cost.html', n: '06', title: 'Tokens as cost' },
    { file: '07-drills.html', n: '07', title: 'Drills', part: 'Practice' },
    { file: '08-build-the-tokenizer.html', n: '08', title: 'Build the tokenizer', part: 'The build' },
    { file: '09-appendix.html', n: '09', title: 'Appendix', part: 'Reference' },
  ],
};
