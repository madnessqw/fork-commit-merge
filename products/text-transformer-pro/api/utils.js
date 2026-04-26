/**
 * Text Transformation Utilities
 * All-in-one text formatting: case conversion, counting, slug generation
 */

function transformText(text, mode) {
  if (!text) return '';

  switch (mode) {
    case 'upper':
      return text.toUpperCase();
    case 'lower':
      return text.toLowerCase();
    case 'title':
      return text.toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
    case 'sentence':
      return text.toLowerCase().replace(/(^.|[.!?]\s+\w)/g, c => c.toUpperCase());
    case 'camel':
      return text.toLowerCase()
        .replace(/[^a-zA-Z0-9]+(.)/g, (_, chr) => chr.toUpperCase());
    case 'pascal':
      return text.toLowerCase()
        .replace(/[^a-zA-Z0-9]+(.)/g, (_, chr) => chr.toUpperCase())
        .replace(/^[a-z]/, c => c.toUpperCase());
    case 'snake':
      return text.toLowerCase().replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_+|_+$/g, '');
    case 'kebab':
      return text.toLowerCase().replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-+|-+$/g, '');
    case 'slug':
      return text.toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-+|-+$/g, '');
    case 'reverse':
      return text.split('').reverse().join('');
    case 'clean':
      return text.replace(/\s+/g, ' ').trim();
    default:
      return text;
  }
}

function analyzeText(text) {
  if (!text) {
    return {
      characters: 0,
      charactersNoSpaces: 0,
      words: 0,
      lines: 0,
      sentences: 0,
      paragraphs: 0,
      readingTime: 0
    };
  }

  const characters = text.length;
  const charactersNoSpaces = text.replace(/\s/g, '').length;
  const words = text.trim().split(/\s+/).filter(w => w.length > 0).length;
  const lines = text.split('\n').length;
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0).length;
  const paragraphs = text.split(/\n\n+/).filter(p => p.trim().length > 0).length;
  const readingTime = Math.ceil(words / 200);

  return {
    characters,
    charactersNoSpaces,
    words,
    lines,
    sentences,
    paragraphs,
    readingTime
  };
}

function generateStats(text) {
  const analysis = analyzeText(text);
  const uniqueWords = new Set((text.toLowerCase().match(/\b\w+\b/g) || [])).size;
  const avgWordLength = analysis.words > 0 ? Math.round(analysis.charactersNoSpaces / analysis.words) : 0;

  return {
    ...analysis,
    uniqueWords,
    avgWordLength
  };
}

module.exports = { transformText, analyzeText, generateStats };
