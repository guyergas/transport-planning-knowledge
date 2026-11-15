"""Fetch URL with headless Chromium. Usage: browser_fetch.py URL DEST -> prints JSON line."""
import json, sys, urllib.parse
from playwright.sync_api import sync_playwright
url, dest = sys.argv[1], sys.argv[2]
out = {'url': url}
with sync_playwright() as p:
    b = p.chromium.launch(args=['--disable-blink-features=AutomationControlled'])
    ctx = b.new_context(locale='he-IL', user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36')
    pg = ctx.new_page()
    try:
        is_file = urllib.parse.urlsplit(url).path.lower().endswith(('.pdf', '.zip', '.doc', '.docx', '.xls', '.xlsx'))
        if is_file:
            o = urllib.parse.urlsplit(url)
            pg.goto(f'{o.scheme}://{o.netloc}/', wait_until='domcontentloaded', timeout=60000)
            pg.wait_for_timeout(4000)
            r = ctx.request.get(url, timeout=240000)
            open(dest, 'wb').write(r.body())
            out.update(status=r.status, final_url=r.url, content_type=r.headers.get('content-type', ''))
        else:
            r = pg.goto(url, wait_until='networkidle', timeout=90000)
            pg.wait_for_timeout(3000)
            if r and r.status in (403, 503):  # challenge pages often reload themselves
                pg.wait_for_timeout(8000); r = pg.reload(wait_until='networkidle', timeout=90000)
            open(dest, 'w', encoding='utf-8').write(pg.content())
            out.update(status=r.status if r else 0, final_url=pg.url, content_type='text/html')
        out['redirects'] = int(out.get('final_url', url) != url)
    except Exception as e:
        out.update(status=0, error=repr(e)[:300])
    b.close()
print(json.dumps(out))
