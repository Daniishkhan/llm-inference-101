// book-config.js — this book's facts, read by ../assets/book.js and ../assets/tutor.js.
// Loaded (defer) just before book.js. The chapter list is the single source of truth for the
// sidebar, prev and next, the contents cards and progress. `part` starts a group in the sidebar.
window.BOOK = {
  id: '01-measure',
  title: 'Measure first',
  brand: 'Module 1',
  tagline: 'Module 1 of 20 · LLM inference in Python',
  courseHref: '../index.html',
  storageKey: 'llm101-01-measure-done',
  buildPage: '08-build-the-harness.html',
  drillsPage: '07-drills.html',
  chapters: [
    { file: 'index.html', title: 'Contents', front: true },
    { file: '00-start-here.html', n: '00', title: 'Start here', part: 'Orientation' },
    { file: '01-two-clocks.html', n: '01', title: 'Two clocks', part: 'Timing and its spread' },
    { file: '02-tails-and-percentiles.html', n: '02', title: 'Tails and percentiles' },
    { file: '03-partition-and-select.html', n: '03', title: 'Partition and select' },
    { file: '04-pictures-in-the-terminal.html', n: '04', title: 'Pictures in the terminal', part: 'Showing and explaining' },
    { file: '05-where-the-time-goes.html', n: '05', title: 'Where the time goes' },
    { file: '06-boxes-and-arrays.html', n: '06', title: 'Boxes and arrays' },
    { file: '07-drills.html', n: '07', title: 'Drills', part: 'Practice' },
    { file: '08-build-the-harness.html', n: '08', title: 'Build the harness', part: 'The build' },
    { file: '09-appendix.html', n: '09', title: 'Appendix', part: 'Reference' },
  ],
};
