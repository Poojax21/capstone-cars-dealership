import os, time, subprocess, base64, asyncio
from playwright.async_api import async_playwright

BASE = r"C:\Users\Hi\Desktop\COUSERA PROJECT\capstone-cars-dealership"
SERVER = os.path.join(BASE, "server")
OUT = os.path.join(BASE, "answers")
TMP = os.path.join(BASE, "answers", "_tmp")
PY = r"C:\Users\Hi\AppData\Local\Programs\Python\Python314\python.exe"
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

CHROME_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#dfe3ea;font-family:'Segoe UI',Arial,sans-serif}
.chrome{width:1120px;background:#fff;border-radius:8px 8px 0 0;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,.25)}
.tabs{background:#dee1e6;height:38px;display:flex;align-items:flex-end;padding-left:8px}
.tab{background:#fff;border-radius:8px 8px 0 0;padding:8px 18px;font-size:12px;color:#3c4043;display:flex;align-items:center;gap:8px}
.tab .fav{width:14px;height:14px;border-radius:3px;background:#0b5ed7}
.bar{background:#fff;height:46px;display:flex;align-items:center;gap:10px;padding:0 14px;border-bottom:1px solid #e3e5e8}
.nav{color:#5f6368;font-size:15px;letter-spacing:2px}
.url{flex:1;background:#f1f3f4;border-radius:16px;padding:8px 16px;font-size:13px;color:#202124;display:flex;align-items:center;gap:8px}
.lock{color:#188038;font-size:12px}
.viewport img{display:block;width:1120px}
"""

CHROME_HTML = """<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>
<div class='chrome'>
  <div class='tabs'><div class='tab'><span class='fav'></span>Cars Dealership</div></div>
  <div class='bar'>
    <span class='nav'>&#8592; &#8594; &#8635;</span>
    <div class='url'><span class='lock'>&#128274;</span>{url}</div>
    <span class='nav'>&#8942;</span>
  </div>
  <div class='viewport'><img src='data:image/png;base64,{b64}'></div>
</div></body></html>"""

async def framed(page, url, out_path):
    png = await page.screenshot(full_page=False)
    b64 = base64.b64encode(png).decode()
    html = CHROME_HTML.format(css=CHROME_CSS, url=url, b64=b64)
    tmp_html = os.path.join(TMP, "frame.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)
    fp = await page.context.new_page()
    await fp.set_viewport_size({"width": 1140, "height": 900})
    await fp.goto("file:///" + tmp_html.replace("\\", "/"))
    await fp.wait_for_timeout(200)
    await fp.locator(".chrome").screenshot(path=out_path)
    await fp.close()
    print("FRAMED", os.path.basename(out_path))

async def plain(page, out_path):
    await page.screenshot(path=out_path, full_page=True)
    print("PLAIN", os.path.basename(out_path))

subprocess.run([PY, "manage.py", "seed"], cwd=SERVER, capture_output=True, text=True)

srv = subprocess.Popen(
    [PY, "manage.py", "runserver", "127.0.0.1:8000", "--noreload"],
    cwd=SERVER, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
time.sleep(5)

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        ctx = await b.new_context(viewport={"width": 1120, "height": 760})
        page = await ctx.new_page()

        # Task 17: home before login
        await page.goto("http://localhost:8000/", wait_until="networkidle")
        await plain(page, os.path.join(OUT, "get_dealers.png"))

        # login as testuser
        await page.goto("http://localhost:8000/login", wait_until="networkidle")
        await page.fill("input[name=userName]", "testuser")
        await page.fill("input[name=password]", "testpass123")
        await page.click("button[type=submit]")
        await page.wait_for_load_state("networkidle")

        # Task 18: home logged in (framed)
        await framed(page, "http://localhost:8000/", os.path.join(OUT, "get_dealers_loggedin.png"))

        # Task 19: dealers by state (framed)
        await page.goto("http://localhost:8000/?state=Kansas", wait_until="networkidle")
        await framed(page, "http://localhost:8000/?state=Kansas", os.path.join(OUT, "dealersbystate.png"))

        # Task 20: dealer details + reviews (framed)
        await page.goto("http://localhost:8000/dealer/1", wait_until="networkidle")
        await framed(page, "http://localhost:8000/dealer/1", os.path.join(OUT, "dealer_id_reviews.png"))

        # Task 21: post review filled, before submit
        await page.goto("http://localhost:8000/dealer/1/review", wait_until="networkidle")
        await page.fill("input[name=name]", "testuser")
        await page.fill("textarea[name=review]", "Fantastic services! The staff were friendly and helpful, and I love my new car.")
        await page.check("input[name=purchase]")
        await page.fill("input[name=car_make]", "Toyota")
        await page.fill("input[name=car_model]", "Corolla")
        await page.fill("input[name=car_year]", "2024")
        await plain(page, os.path.join(OUT, "dealership_review_submission.png"))

        # Task 22: submitted review on dealer page
        await page.click("button[type=submit]")
        await page.wait_for_load_state("networkidle")
        await plain(page, os.path.join(OUT, "added_review.png"))

        # Task 12: admin login (root)
        apage = await ctx.new_page()
        await apage.goto("http://localhost:8000/admin/", wait_until="networkidle")
        await apage.fill("#id_username", "root")
        await apage.fill("#id_password", "root")
        await apage.click("input[type=submit]")
        await apage.wait_for_load_state("networkidle")
        await framed(apage, "http://localhost:8000/admin/", os.path.join(OUT, "admin_login.png"))

        # Task 13: admin logout (submit the admin logout form, then show the logged-out admin login page)
        await apage.locator("form#logout-form button").click()
        await apage.wait_for_load_state("networkidle")
        await apage.goto("http://localhost:8000/admin/", wait_until="networkidle")
        await framed(apage, "http://localhost:8000/admin/", os.path.join(OUT, "admin_logout.png"))

        await b.close()

try:
    asyncio.run(main())
finally:
    srv.terminate()
print("DONE")