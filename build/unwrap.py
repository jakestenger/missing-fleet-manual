import re, io, sys

FENCE  = re.compile(r'^\s*(```|~~~)')
HEAD   = re.compile(r'^\s{0,3}#{1,6}\s')
TABLE  = re.compile(r'^\s*\|')
HR     = re.compile(r'^\s{0,3}([-*_])(\s*\1){2,}\s*$')
LIST   = re.compile(r'^(\s*)([-*+]|\d{1,9}[.)])\s+')
QUOTE  = re.compile(r'^\s*>')
INDENT = re.compile(r'^ {4,}\S')          # indented code block
HARDBR = re.compile(r'\S {2,}$')          # trailing double space = hard break

def quote_body(ln):
    """The content of a blockquote line, with its '>' markers removed."""
    return re.sub(r'^\s*>+\s?', '', ln)

def unwrap(text):
    lines = text.split('\n')
    out, i, n = [], 0, len(lines)

    # frontmatter passthrough
    if lines and lines[0].strip() == '---':
        out.append(lines[0]); i = 1
        while i < n and lines[i].strip() != '---':
            out.append(lines[i]); i += 1
        if i < n:
            out.append(lines[i]); i += 1

    buf = []            # paragraph buffer
    prefix = ''         # list marker / quote marker to keep on the joined line

    def flush():
        nonlocal buf, prefix
        if buf:
            out.append(prefix + ' '.join(s.strip() for s in buf))
            buf, prefix = [], ''

    while i < n:
        ln = lines[i]
        s  = ln.strip()

        if FENCE.match(ln):                      # code fence: copy verbatim
            flush(); out.append(ln); i += 1
            close = FENCE.match(ln).group(1)
            while i < n:
                out.append(lines[i])
                if lines[i].strip().startswith(close): i += 1; break
                i += 1
            continue

        if s.startswith('<!--'):                  # html comment: copy verbatim
            flush()
            while i < n:
                out.append(lines[i])
                if '-->' in lines[i]: i += 1; break
                i += 1
            continue

        if not s:                                 # blank line ends a block
            flush(); out.append(ln); i += 1; continue

        if HEAD.match(ln) or TABLE.match(ln) or HR.match(ln) or INDENT.match(ln):
            flush(); out.append(ln); i += 1; continue

        if HARDBR.search(ln):                     # deliberate hard break: leave block alone
            flush(); out.append(ln); i += 1; continue

        m = LIST.match(ln)
        if m:                                     # new list item
            flush(); prefix = m.group(0); buf = [ln[len(m.group(0)):]]; i += 1; continue

        if QUOTE.match(ln) and FENCE.match(quote_body(ln)):
            # A code fence inside a blockquote. FENCE.match(ln) above misses it, because the
            # line starts with '>', so without this branch the fence and its contents fall
            # through to the blockquote branch and get joined into one unrunnable line. That
            # happened to 8.1's cron_stats query and shipped, because sig() strips '>' markers
            # and so compared the wreckage equal to the original.
            flush()
            close = FENCE.match(quote_body(ln)).group(1)
            out.append(ln); i += 1
            while i < n:
                out.append(lines[i])
                if quote_body(lines[i]).strip().startswith(close): i += 1; break
                i += 1
            continue

        if QUOTE.match(ln):                       # blockquote
            body = quote_body(ln)
            if not body.strip():                  # '>' alone separates quote paragraphs
                flush(); out.append(ln); i += 1; continue
            if prefix.strip().startswith('>'):
                buf.append(body)
            else:
                flush(); prefix = '> '; buf = [body]
            i += 1; continue

        # plain paragraph line, or a continuation of a list item / quote
        if not buf and not prefix:
            prefix = ''
        buf.append(ln); i += 1

    flush()
    return '\n'.join(out)

def sig(t):
    """Signature for verifying the rendered content is unchanged.

    Strips leading blockquote markers, because joining '> a' + '> b' into '> a b'
    legitimately drops a marker while rendering identically. Everything else must match.
    """
    lines = [re.sub(r'^\s*>+\s?', '', l) for l in t.split('\n')]
    return re.sub(r'\s+', ' ', ' '.join(lines)).strip()

if __name__ == '__main__':
    import glob
    files = sys.argv[2:] if len(sys.argv) > 2 else sorted(glob.glob('manual/*/*.md'))
    apply = sys.argv[1] == 'apply'
    changed = mism = 0
    for f in files:
        orig = io.open(f, encoding='utf-8').read()
        new  = unwrap(orig)
        if sig(orig) != sig(new):
            print("  !! SIGNATURE MISMATCH %s" % f); mism += 1; continue
        if new != orig:
            changed += 1
            if apply:
                io.open(f, 'w', encoding='utf-8').write(new)
    print("%s: %d files changed, %d signature mismatches" %
          ('APPLIED' if apply else 'DRY RUN', changed, mism))
