"""Build RSS 2.0 feeds for Pinterest auto-publish from social/queue.json (one feed per board)."""
import json, sys, os, html, datetime
root = sys.argv[1]
q = json.load(open(os.path.join(root, 'social', 'queue.json'), encoding='utf-8'))
BOARDS = {
    'jars-kitchen': ('Ceramic Jars & Kitchen Storage', {'jars', 'moon', 'art', 'kitchen', 'bottles'}),
    'dinnerware': ('Ceramic Dinnerware & Serveware', {'dining', 'salad', 'handi', 'serve', 'horeca'}),
    'vases-decor': ('Ceramic Vases & Home Décor', {'decor', 'bath'}),
    'planters': ('Ceramic Planters', {'planters'}),
    'mugs-gifts': ('Ceramic Mugs & Gifts', {'mugs', 'gift'}),
}
TAIL = 'Ceramics made in India by Clyra Ceramics. Bulk orders, gifting and worldwide shipping. WhatsApp +91 79838 95342 · clyraceramics.in'
start = datetime.datetime(2026, 11, 7, tzinfo=datetime.timezone.utc)
e = lambda s: html.escape(s or '', quote=True)
for slug, (title, cats) in BOARDS.items():
    items = [p for p in q['posts'] if p.get('cat') in cats]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">', '<channel>',
           f'<title>{e(title)} | Clyra Ceramics</title>', '<link>https://clyraceramics.in/</link>',
           f'<description>{e(title)} from Clyra Ceramics, hand-painted in India.</description>', '<language>en</language>']
    for i, p in enumerate(items):
        name = p['n'].replace(' · ', ' – ')
        parts = [name + '.']
        if p.get('code'): parts.append(f"Code {p['code']}.")
        if p.get('d'): parts.append(p['d'])
        if p.get('f'): parts.append(' · '.join(p['f']) + '.')
        if p.get('finish') == 'Hand-painted': parts.append('Hand-painted.')
        desc = ' '.join(parts + [TAIL])
        img = q['base'] + 'post/' + p['key'] + '.jpg'
        link = f"https://clyraceramics.in/?pin={p['key']}#products"
        date = (start - datetime.timedelta(minutes=i)).strftime('%a, %d %b %Y %H:%M:%S +0000')
        out += ['<item>', f'<title>{e(name)}</title>', f'<link>{e(link)}</link>', f'<guid isPermaLink="false">clyra-{e(p["key"])}</guid>',
                f'<description>{e(desc)}</description>', f'<pubDate>{date}</pubDate>',
                f'<enclosure url="{e(img)}" type="image/jpeg" length="0"/>', f'<media:content url="{e(img)}" medium="image" type="image/jpeg"/>', '</item>']
    out += ['</channel>', '</rss>']
    open(os.path.join(root, 'pinterest', slug + '.xml'), 'w', encoding='utf-8').write('\n'.join(out))
    print(slug, len(items))
