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
            r = None
            for attempt in range(3):
                try:
                    r = pg.goto(url, wait_until='domcontentloaded', timeout=60000)
                    try:
                        pg.wait_for_load_state('networkidle', timeout=20000)
                    except Exception:
                        pass  # SPA keeps polling; content is usually there
                    pg.wait_for_timeout(3000)
                    if r and r.status == 200 and len(pg.content()) > 20000:
                        for _ in range(6):  # lazy lists: scroll to load more
                            pg.mouse.wheel(0, 20000); pg.wait_for_timeout(1200)
                        break
                except Exception as e:
                    out['retry_error'] = repr(e)[:200]
                pg.wait_for_timeout(5000 * (attempt + 1))
            open(dest, 'w', encoding='utf-8').write(pg.content())
            out.update(status=r.status if r else 0, final_url=pg.url, content_type='text/html')
        out['redirects'] = int(out.get('final_url', url) != url)
    except Exception as e:
        out.update(status=0, error=repr(e)[:300])
    b.close()
print(json.dumps(out))
