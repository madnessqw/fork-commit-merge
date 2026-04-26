// Git Diff Visualizer API - Process endpoint
// Handles diff visualization requests

module.exports = async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { diff, mode = 'side-by-side', format = 'html' } = req.body;

    if (!diff) {
      return res.status(400).json({ error: 'No diff provided' });
    }

    // Parse the diff
    const parsedDiff = parseDiff(diff);

    // Generate output based on mode
    let result;
    if (mode === 'side-by-side') {
      result = generateSideBySide(parsedDiff);
    } else if (mode === 'inline') {
      result = generateInline(parsedDiff);
    } else if (mode === 'unified') {
      result = generateUnified(parsedDiff);
    } else {
      return res.status(400).json({ error: 'Invalid mode. Use side-by-side, inline, or unified' });
    }

    // Export as patch if requested
    if (format === 'patch') {
      return res.status(200).json({
        patch: generatePatch(parsedDiff),
        stats: getDiffStats(parsedDiff)
      });
    }

    return res.status(200).json({
      result,
      stats: getDiffStats(parsedDiff),
      mode,
      files: parsedDiff.map(f => f.filename)
    });

  } catch (error) {
    console.error('Diff processing error:', error);
    return res.status(500).json({ error: 'Failed to process diff', message: error.message });
  }
};

function parseDiff(diffText) {
  const files = [];
  const lines = diffText.split('\n');
  let currentFile = null;
  let currentHunk = null;

  for (const line of lines) {
    // File header: diff --git a/filename b/filename
    const gitDiffMatch = line.match(/^diff --git a\/(.+) b\/.+$/);
    if (gitDiffMatch) {
      if (currentFile) files.push(currentFile);
      currentFile = {
        filename: gitDiffMatch[1],
        oldFile: null,
        newFile: null,
        hunks: []
      };
      currentHunk = null;
      continue;
    }

    // Old file: --- a/filename
    const oldFileMatch = line.match(/^--- a\/(.+)$/);
    if (oldFileMatch && currentFile) {
      currentFile.oldFile = oldFileMatch[1];
      continue;
    }

    // New file: +++ b/filename
    const newFileMatch = line.match(/^\+\+\+ b\/(.+)$/);
    if (newFileMatch && currentFile) {
      currentFile.newFile = newFileMatch[1];
      continue;
    }

    // Hunk header: @@ -start,count +start,count @@
    const hunkMatch = line.match(/^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$/);
    if (hunkMatch && currentFile) {
      currentHunk = {
        oldStart: parseInt(hunkMatch[1]),
        oldCount: parseInt(hunkMatch[2] || 1),
        newStart: parseInt(hunkMatch[3]),
        newCount: parseInt(hunkMatch[4] || 1),
        header: hunkMatch[5] || '',
        lines: []
      };
      currentFile.hunks.push(currentHunk);
      continue;
    }

    // Line content
    if (currentHunk) {
      if (line.startsWith('+')) {
        currentHunk.lines.push({ type: 'added', content: line.slice(1) });
      } else if (line.startsWith('-')) {
        currentHunk.lines.push({ type: 'removed', content: line.slice(1) });
      } else if (line.startsWith('\\')) {
        currentHunk.lines.push({ type: 'no-newline', content: line });
      } else if (line.startsWith(' ')) {
        currentHunk.lines.push({ type: 'context', content: line.slice(1) });
      } else if (line === '') {
        currentHunk.lines.push({ type: 'context', content: '' });
      }
    }
  }

  if (currentFile) files.push(currentFile);
  return files;
}

function generateSideBySide(parsedDiff) {
  return parsedDiff.map(file => {
    const hunks = file.hunks.map(hunk => {
      const oldLines = [];
      const newLines = [];
      let oldLineNum = hunk.oldStart;
      let newLineNum = hunk.newStart;

      for (const line of hunk.lines) {
        if (line.type === 'context') {
          oldLines.push({ num: oldLineNum++, content: line.content, type: 'context' });
          newLines.push({ num: newLineNum++, content: line.content, type: 'context' });
        } else if (line.type === 'removed') {
          oldLines.push({ num: oldLineNum++, content: line.content, type: 'removed' });
        } else if (line.type === 'added') {
          newLines.push({ num: newLineNum++, content: line.content, type: 'added' });
        }
      }

      // Pad arrays to same length
      const maxLen = Math.max(oldLines.length, newLines.length);
      while (oldLines.length < maxLen) oldLines.push({ num: '', content: '', type: 'empty' });
      while (newLines.length < maxLen) newLines.push({ num: '', content: '', type: 'empty' });

      return { header: hunk.header, oldLines, newLines };
    });

    return { filename: file.filename, hunks };
  });
}

function generateInline(parsedDiff) {
  return parsedDiff.map(file => {
    const hunks = file.hunks.map(hunk => {
      const lines = [];
      let oldLineNum = hunk.oldStart;
      let newLineNum = hunk.newStart;

      for (const line of hunk.lines) {
        if (line.type === 'context') {
          lines.push({
            oldNum: oldLineNum++,
            newNum: newLineNum++,
            content: line.content,
            type: 'context'
          });
        } else if (line.type === 'removed') {
          lines.push({
            oldNum: oldLineNum++,
            newNum: '',
            content: line.content,
            type: 'removed'
          });
        } else if (line.type === 'added') {
          lines.push({
            oldNum: '',
            newNum: newLineNum++,
            content: line.content,
            type: 'added'
          });
        }
      }

      return { header: hunk.header, lines };
    });

    return { filename: file.filename, hunks };
  });
}

function generateUnified(parsedDiff) {
  // Similar to inline but with @@ markers
  return generateInline(parsedDiff);
}

function generatePatch(parsedDiff) {
  return parsedDiff.map(file => {
    const hunks = file.hunks.map(h => {
      const lines = h.lines.map(l => {
        if (l.type === 'added') return '+' + l.content;
        if (l.type === 'removed') return '-' + l.content;
        if (l.type === 'context') return ' ' + l.content;
        return l.content;
      }).join('\n');
      return `@@ -${h.oldStart},${h.oldCount} +${h.newStart},${h.newCount} @@${h.header}\n${lines}`;
    }).join('\n');

    return `--- a/${file.oldFile || file.filename}\n+++ b/${file.newFile || file.filename}\n${hunks}`;
  }).join('\n\n');
}

function getDiffStats(parsedDiff) {
  let additions = 0;
  let deletions = 0;
  let changes = 0;

  for (const file of parsedDiff) {
    for (const hunk of file.hunks) {
      for (const line of hunk.lines) {
        if (line.type === 'added') additions++;
        if (line.type === 'removed') deletions++;
      }
    }
  }

  changes = parsedDiff.length;

  return { additions, deletions, changes };
}
