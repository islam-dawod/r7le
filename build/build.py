# -*- coding: utf-8 -*-
"""
R7LE.COM static site generator.
Generates the full Arabic (RTL), mobile-first public website described in the
project brief (R7LE_Complete_Website_Instructions_Iraq.pdf).

Run:  python build/build.py
Output is written to the repository root (one folder per route + /assets).
"""
import os
import pathlib
import datetime
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODAY = "13 أكتوبر 2026"
YEAR = datetime.date.today().year

SITE = {
    "brand_ar": "رحلة",
    "brand_latin": "R7LE",
    "domain": "r7le.com",
    "base_url": "https://r7le.com",
    # Placeholders — must be confirmed by the project owner (Section 16).
    "entity": "[الكيان القانوني المشغّل — قيد التأكيد]",
    "reg_no": "[رقم التسجيل — قيد التأكيد]",
    "address": "[العنوان المسجّل — قيد التأكيد]",
    "whatsapp": "+964 [رقم الدعم — قيد التأكيد]",
    "whatsapp_link": "#",
    "email": "support@r7le.com",
    "hours": "[ساعات العمل الفعلية — قيد التأكيد]",
}

# route -> (nav label or None, <title>, meta description)
NAV = [
    ("/", "الرئيسية"),
    ("/usa/", "أمريكا"),
    ("/canada/", "كندا"),
    ("/australia/", "أستراليا"),
    ("/services/", "الخدمات"),
    ("/howitworks/", "كيف نعمل"),
    ("/faq/", "الأسئلة"),
    ("/blog/", "المدونة"),
    ("/contact/", "تواصل"),
]

FOOTER_LEGAL = [
    ("/aboutus/", "من نحن"),
    ("/terms/", "الشروط والأحكام"),
    ("/privacypolicy/", "سياسة الخصوصية"),
    ("/refundpolicy/", "سياسة الاسترداد"),
    ("/disclaimer/", "إخلاء المسؤولية"),
]

DISCLOSURE = (
    "رحلة R7LE علامة تجارية لخدمات خاصة ومحددة في المساعدة الإدارية وتجهيز "
    "وتنظيم المستندات. نحن لسنا سفارة أو قنصلية أو جهة حكومية، ولسنا تابعين "
    "لسلطات الهجرة الأمريكية أو الكندية أو الأسترالية. يمكن للعملاء استخدام "
    "القنوات الحكومية الرسمية مباشرة دون شراء خدماتنا. لا تضمن خدماتنا قبول "
    "أي تأشيرة أو سرعة قرارها، وتبقى القرارات النهائية بيد الجهات المختصة."
)


def rel_prefix(path):
    """Relative path back to site root from a route like /usa/ -> ../"""
    depth = len([p for p in path.strip("/").split("/") if p])
    return "../" * depth if depth else "./"


def icon(name):
    p = {
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
        "close": '<path d="M6 6l12 12M18 6L6 18"/>',
        "wa": '<path d="M12 3a9 9 0 0 0-7.7 13.6L3 21l4.5-1.2A9 9 0 1 0 12 3z"/><path d="M8.5 8.8c.2-.5.4-.5.6-.5h.5c.2 0 .4 0 .6.5l.7 1.6c.1.2 0 .4-.1.6l-.4.5c-.1.2-.2.3 0 .6.3.5.8 1.1 1.4 1.5.6.4.9.5 1.1.4l.5-.4c.2-.2.4-.2.6-.1l1.5.8c.3.1.4.3.4.5 0 .5-.5 1.3-1 1.5-.5.2-1.6.3-3.3-.6-2-1-3.3-3-3.4-3.2-.1-.2-.9-1.3-.9-2.4 0-1.1.6-1.6.8-1.8z"/>',
        "check": '<path d="M20 6L9 17l-5-5"/>',
        "x": '<path d="M18 6L6 18M6 6l12 12"/>',
        "doc": '<path d="M7 3h7l5 5v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M14 3v5h5"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/>',
        "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-2 6a3 3 0 0 0 6 0L7 7m12 0l-2 6a3 3 0 0 0 6 0l-2-6"/>',
        "flag": '<path d="M5 21V4m0 0h11l-2 4 2 4H5"/>',
        "steps": '<path d="M4 6h16M4 12h10M4 18h6"/>',
        "card": '<path d="M3 7h18v10H3zM3 11h18"/>',
        "user": '<path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0"/>',
        "lock": '<path d="M6 10V8a6 6 0 0 1 12 0v2M5 10h14v10H5z"/>',
        "chat": '<path d="M4 5h16v11H9l-5 4V5z"/>',
        "globe": '<path d="M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
        "arrow": '<path d="M19 12H5m7-7l-7 7 7 7"/>',
        "pin": '<path d="M12 21s7-6 7-11a7 7 0 1 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        "mail": '<path d="M3 5h18v14H3zM3 6l9 7 9-7"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    }[name]
    return (f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{p}</svg>')


def logo(rp, mono=False):
    cls = "logo logo--mono" if mono else "logo"
    return (f'<a class="{cls}" href="{rp}index.html" aria-label="رحلة re7le — الصفحة الرئيسية">'
            f'<span class="logo__mark">'
            f'<img src="{rp}assets/img/logo-mark.png" alt="" width="44" height="44" loading="eager" decoding="async">'
            f'</span>'
            f'<span class="logo__txt"><b>رحلة</b><i>re7le</i></span></a>')


def head(title, desc, path, rp, extra=""):
    canonical = SITE["base_url"] + path
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ar_IQ">
<meta property="og:site_name" content="رحلة R7LE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['base_url']}/assets/img/logo-full.png">
<link rel="icon" href="{rp}assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="{rp}assets/img/favicon-64.png" sizes="64x64" type="image/png">
<link rel="apple-touch-icon" href="{rp}assets/img/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rp}assets/css/styles.css">
{extra}</head>
<body>
<a class="skip" href="#main">تخطَّ إلى المحتوى</a>"""


def topbar(rp):
    return f"""<div class="topbar">
  <div class="wrap topbar__row">
    <div class="topbar__contacts">
      <a href="{SITE['whatsapp_link']}" rel="nofollow">{icon('wa')}<span>{SITE['whatsapp']}</span></a>
      <a href="mailto:{SITE['email']}">{icon('mail')}<span dir="ltr">{SITE['email']}</span></a>
      <span class="topbar__hours">{icon('clock')} {SITE['hours']}</span>
    </div>
    <div class="topbar__note">{icon('shield')} خدمات خاصة مستقلة — لسنا جهة حكومية</div>
  </div>
</div>"""


def header(path, rp):
    links = ""
    for route, label in NAV:
        active = ' aria-current="page"' if route == path else ""
        href = rp + "index.html" if route == "/" else rp + route.strip("/") + "/index.html"
        links += f'<li><a href="{href}"{active}>{label}</a></li>'
    return topbar(rp) + f"""<header class="site-head">
  <div class="wrap site-head__row">
    {logo(rp)}
    <nav class="nav" aria-label="التنقل الرئيسي">
      <ul class="nav__list">{links}</ul>
    </nav>
    <div class="site-head__cta">
      <a class="btn btn--wa" href="{SITE['whatsapp_link']}" rel="nofollow">{icon('wa')}<span>تواصل ويانا</span></a>
      <a class="btn btn--primary" href="{rp}services/index.html">ابدأ طلب الخدمة</a>
    </div>
    <button class="nav-toggle" aria-label="القائمة" aria-expanded="false" aria-controls="mobile-nav">
      {icon('menu')}
    </button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="قائمة الجوال" hidden>
    <ul>{links}</ul>
    <div class="mobile-nav__cta">
      <a class="btn btn--wa btn--block" href="{SITE['whatsapp_link']}" rel="nofollow">{icon('wa')}<span>تواصل ويانا على واتساب</span></a>
      <a class="btn btn--primary btn--block" href="{rp}services/index.html">ابدأ طلب الخدمة</a>
    </div>
  </nav>
</header>"""


def disclosure_bar():
    return f"""<div class="disclosure" role="note">
  <div class="wrap disclosure__row">
    {icon('shield')}
    <p>{DISCLOSURE}</p>
  </div>
</div>"""


def footer(rp):
    nav_cols = ""
    dest = ''.join(
        f'<li><a href="{rp}{r.strip("/")}/index.html">{l}</a></li>'
        for r, l in [("/usa/", "أمريكا — B1/B2"), ("/canada/", "كندا — زيارة"),
                     ("/australia/", "أستراليا — Subclass 600")])
    pages = ''.join(
        f'<li><a href="{rp}{r.strip("/")}/index.html">{l}</a></li>'
        for r, l in [("/services/", "الخدمات والأسعار"), ("/howitworks/", "كيف نعمل"),
                     ("/faq/", "الأسئلة الشائعة"), ("/blog/", "المدونة"),
                     ("/client/", "حساب العميل"), ("/contact/", "تواصل معنا")])
    legal = ''.join(
        f'<li><a href="{rp}{r.strip("/")}/index.html">{l}</a></li>' for r, l in FOOTER_LEGAL)
    ribbon = ''.join(
        f'<li>{icon(i)}<span>{t}</span></li>' for i, t in [
            ("shield", "اتصال مشفّر HTTPS/TLS"),
            ("lock", "خصوصية وحماية بيانات"),
            ("card", "رسوم حكومية منفصلة ومعلنة"),
            ("scale", "إفصاح واضح وعدم ارتباط حكومي")])
    return f"""<footer class="site-foot">
  <div class="site-foot__ribbon"><div class="wrap"><ul>{ribbon}</ul></div></div>
  <div class="wrap site-foot__grid">
    <div class="site-foot__brand">
      {logo(rp, mono=True)}
      <p>منصّة مستقلة موجّهة للعراقيين، تقدّم خدمات خاصة في المساعدة الإدارية وتجهيز
         وتنظيم مستندات طلب التأشيرة لوجهات أمريكا وكندا وأستراليا — بأسعار معلنة
         وشروط واضحة.</p>
      <p class="site-foot__entity">الجهة المشغّلة: {SITE['entity']}<br>
         رقم التسجيل: {SITE['reg_no']}</p>
    </div>
    <div class="site-foot__col"><h3>الوجهات</h3><ul>{dest}</ul></div>
    <div class="site-foot__col"><h3>الموقع</h3><ul>{pages}</ul></div>
    <div class="site-foot__col"><h3>القانوني</h3><ul>{legal}</ul></div>
  </div>
  <div class="wrap site-foot__note">
    <p>{DISCLOSURE}</p>
  </div>
  <div class="wrap site-foot__bottom">
    <p>© {YEAR} رحلة R7LE — جميع الحقوق محفوظة.</p>
    <p>لسنا جهة حكومية ولا نضمن أي قرار تأشيرة.</p>
  </div>
</footer>
<script src="{rp}assets/js/main.js" defer></script>
</body>
</html>"""


def page(path, title, desc, body, extra_head="", extra_foot=""):
    rp = rel_prefix(path)
    html = (head(title, desc, path, rp, extra_head)
            + header(path, rp)
            + disclosure_bar()
            + '<main id="main">' + body + '</main>'
            + extra_foot
            + footer(rp))
    out_dir = ROOT if path == "/" else ROOT / path.strip("/")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    return rp


# ---------- Reusable content blocks ----------

def hero_block(rp):
    return f"""
<section class="hero hero--framed">
  <div class="wrap">
    <figure class="hero__frame">
      <img class="hero__bg" src="{rp}assets/img/photos/hero.jpg" width="1448" height="1086"
           fetchpriority="high"
           alt="وجهات أمريكا وكندا وأستراليا — معالم سيدني وتورنتو ونيويورك مع جوازات سفر">
      <span class="hero__overlay" aria-hidden="true"></span>
      <div class="hero__content">
        <span class="eyebrow eyebrow--light">{icon('globe')} خدمات تجهيز مستندات السفر</span>
        <h1>رحلتك تبدأ من هنا</h1>
        <p class="lead">خدمات خاصة لتجهيز وتنظيم مستندات تأشيرة الزيارة لأمريكا وكندا
           وأستراليا — بخطوات واضحة وأسعار معلنة ودعم بالعربية.</p>
        <div class="hero__cta">
          <a class="btn btn--primary btn--lg" href="{rp}services/index.html">ابدأ طلب الخدمة</a>
          <a class="btn btn--light btn--lg" href="#destinations">استكشف الوجهات {icon('arrow')}</a>
        </div>
      </div>
    </figure>
  </div>
</section>"""


def shead(kicker, title, sub=""):
    s = f'<p>{sub}</p>' if sub else ""
    return (f'<div class="section__head"><span class="kicker">{kicker}</span>'
            f'<h2>{title}</h2>{s}</div>')


def trust_strip():
    items = [("shield", "لسنا جهة حكومية", "مقدّم خدمة خاص ومستقل"),
             ("card", "أسعار معلنة", "رسوم الشركة منفصلة عن الحكومية"),
             ("lock", "دفع وبيانات آمنة", "تشفير HTTPS/TLS وخصوصية"),
             ("chat", "دعم بالعربية", "تواصل ويانا بكل وضوح")]
    li = ''.join(
        f'<li>{icon(i)}<div><b>{t}</b><span>{d}</span></div></li>' for i, t, d in items)
    return f"""
<section class="trust-strip" aria-label="ضمانات الخدمة">
  <div class="wrap"><ul>{li}</ul></div>
</section>"""


def whyus_block():
    cards = [
        ("scale", "شفافية حقيقية",
         "نوضّح حدود الخدمة، والرسوم الحكومية المنفصلة، وسياسة الاسترداد قبل أي دفع."),
        ("doc", "مخرجات محدّدة",
         "كل خدمة تذكر بدقة ما ستستلمه (Deliverables) وما لا تشمله — بلا وعود مبهمة."),
        ("shield", "أمان وخصوصية",
         "تشفير للملفات الحساسة، صلاحيات أقل امتياز، وجمع البيانات على مراحل."),
        ("globe", "مخصّص للعراقيين",
         "محتوى ولهجة وخطوات موجّهة للسوق العراقي، ودعم كامل باللغة العربية."),
    ]
    c = ''.join(
        f'<article class="value"><span class="value__ic">{icon(i)}</span>'
        f'<h3>{t}</h3><p>{d}</p></article>' for i, t, d in cards)
    return f"""
<section class="section">
  <div class="wrap">
    {shead("لماذا رحلة re7le", "سبب يجعل اختيارك مطمئنًا",
           "نبني الثقة بالوضوح لا بالوعود — خدمات حقيقية بحدود معلومة.")}
    <div class="grid grid--4 values">{c}</div>
  </div>
</section>"""


def destinations_block(rp):
    cards = [
        ("usa", "أمريكا — الولايات المتحدة", "تمثال الحرية في نيويورك",
         "تخطط لزيارة أمريكا؟ تعرّف على خدماتنا الإدارية المتعلقة بتجهيز مستندات "
         "تأشيرة الزيارة B1/B2 وخدمات المساعدة في بيانات النماذج المتاحة."),
        ("canada", "كندا", "أفق مدينة تورنتو الكندية",
         "تفكر تزور الأهل أو تسافر للسياحة؟ نستعرض متطلبات الزيارة وخدمات تجهيز "
         "المستندات المتاحة، مع مقالات معلوماتية عن البرامج المختلفة."),
        ("australia", "أستراليا", "ميناء سيدني — دار الأوبرا وجسر الميناء في أستراليا",
         "اكتشف متطلبات الزيارة إلى أستراليا وخيارات الدعم الإداري الخاصة بمستندات "
         "تأشيرة الزيارة Subclass 600 ذات الصلة بالعراقيين."),
    ]
    html = ""
    for slug, title, alt, text in cards:
        html += f"""
    <article class="dest-card">
      <a class="dest-card__img" href="{rp}{slug}/index.html" tabindex="-1" aria-hidden="true">
        <img src="{rp}assets/img/photos/{slug}.jpg" alt="{alt}" width="820" height="512" loading="lazy">
        <span class="dest-card__tag">{icon('pin')} {title}</span>
      </a>
      <div class="dest-card__body">
        <h3>{title}</h3>
        <p>{text}</p>
        <a class="link-arrow" href="{rp}{slug}/index.html">تفاصيل الوجهة والخدمات {icon('arrow')}</a>
      </div>
    </article>"""
    return f"""
<section class="section" id="destinations">
  <div class="wrap">
    {shead("وجهاتنا", "اختر وجهتك",
           "ثلاث صفحات مستقلة لكل وجهة، تشرح الخدمات المتاحة وحدودها بوضوح قبل أي طلب.")}
    <div class="grid grid--3">{html}
    </div>
  </div>
</section>"""


def howitworks_block():
    steps = [
        ("اختر الوجهة والخدمة", "اقرأ ما تشمل الخدمة وما لا تشمل قبل البدء."),
        ("املأ المعلومات الأولية", "بيانات تواصل أساسية بدون طلب مستندات حساسة في أول خطوة."),
        ("راجع السعر وأكّد الطلب", "تظهر رسوم الشركة والرسوم الحكومية بصورة منفصلة."),
        ("تابع التنفيذ", "نوفّر قائمة مستندات وتحديثات عن تقدّم عمل فريقنا."),
    ]
    items = ""
    for i, (t, d) in enumerate(steps, 1):
        items += f"""
      <li class="step">
        <span class="step__num">{i}</span>
        <div><h3>{t}</h3><p>{d}</p></div>
      </li>"""
    return f"""
<section class="section section--alt">
  <div class="wrap">
    {shead("آلية العمل", "كيف نعمل؟",
           "تجربة بسيطة للعميل العراقي: من اختيار الوجهة حتى تسليم ملف الخدمة.")}
    <ol class="steps">{items}
    </ol>
  </div>
</section>"""


def promises_block():
    allowed = ["أسعار ورسوم معلنة ومنفصلة", "قائمة واضحة بما تشمل الخدمة وما لا تشمل",
               "دعم إداري لتجهيز وتنظيم المستندات", "حساب عميل آمن لمتابعة الطلب"]
    not_allowed = ["«فيزتك مضمونة»", "«موافقة مضمونة 100٪»", "«نطلع لك التأشيرة»",
                   "«نحجز الموعد الرسمي فورًا»"]
    a = ''.join(f"<li>{icon('check')}<span>{x}</span></li>" for x in allowed)
    n = ''.join(f"<li>{icon('x')}<span>{x}</span></li>" for x in not_allowed)
    return f"""
<section class="section">
  <div class="wrap">
    {shead("التزامنا", "نلتزم بالوضوح",
           "فصل واضح بين المساعدة الإدارية والمعلومات، وبين أي وعود لا تسيطر عليها الشركة.")}
    <div class="grid grid--2">
      <div class="panel panel--ok">
        <h3>{icon('check')} ما نقدّمه</h3>
        <ul class="ticklist">{a}</ul>
      </div>
      <div class="panel panel--no">
        <h3>{icon('x')} ما لا نقوله أبدًا</h3>
        <ul class="ticklist ticklist--no">{n}</ul>
      </div>
    </div>
  </div>
</section>"""


def cta_block(rp):
    return f"""
<section class="cta">
  <div class="wrap cta__inner">
    <div>
      <h2>عندك سؤال؟ فريقنا يجاوبك</h2>
      <p>تواصل ويانا على واتساب أو ابدأ طلب الخدمة مباشرة — بدون مستندات حساسة في أول خطوة.</p>
    </div>
    <div class="cta__btns">
      <a class="btn btn--wa btn--lg" href="{SITE['whatsapp_link']}" rel="nofollow">{icon('wa')}<span>تواصل ويانا على واتساب</span></a>
      <a class="btn btn--light btn--lg" href="{rp}services/index.html">شوف الخدمات والأسعار</a>
    </div>
  </div>
</section>"""


def page_hero(title, subtitle, kicker=""):
    k = f'<span class="eyebrow">{kicker}</span>' if kicker else ""
    return f"""
<section class="page-hero">
  <div class="wrap">
    {k}
    <h1>{title}</h1>
    <p class="lead">{subtitle}</p>
  </div>
</section>"""


def breadcrumb(items, rp):
    lis = ""
    for i, (href, label) in enumerate(items):
        last = i == len(items) - 1
        if last:
            lis += f'<li aria-current="page">{label}</li>'
        else:
            target = rp + "index.html" if href == "/" else rp + href.strip("/") + "/index.html"
            lis += f'<li><a href="{target}">{label}</a></li>'
    return f'<nav class="crumbs" aria-label="مسار التصفح"><div class="wrap"><ol>{lis}</ol></div></nav>'


# ---------- Packages data (tourism/visit only) ----------
# Prices shown in Iraqi Dinar (IQD). These are the company service fee only;
# government fees are separate. Amounts are converted/rounded and must be
# confirmed by the project owner before launch (Section 16).

def iqd(n):
    return f"{n:,}"


PACKAGES = {
    "أمريكا": [
        {
            "sku": "USA-B1B2", "price": 710000, "duration": "~5 أيام عمل (لا تشمل معالجة السلطات)",
            "badge": "الأكثر طلبًا",
            "name": "تجهيز وتقديم طلب تأشيرة الزيارة B1/B2",
            "desc": "مراجعة وتجهيز المستندات المطلوبة، والمساعدة في إعداد الطلب وشرح خطوات "
                    "التقديم، وتقديم الطلب بعد موافقتك على بياناته النهائية.",
            "deliver": ["مراجعة وتجهيز مستندات الطلب", "المساعدة في بيانات النموذج DS-160",
                        "تقديم الطلب بعد موافقتك"],
            "incl": ["تجهيز وتنظيم المستندات", "شرح خطوات التقديم"],
            "excl": ["ضمان القبول أو الموعد أو مدة المعالجة", "الرسوم الحكومية"],
        },
    ],
    "كندا": [
        {
            "sku": "CA-VISIT", "price": 710000, "duration": "5–7 أيام عمل",
            "badge": "الأكثر طلبًا",
            "name": "تجهيز مستندات تأشيرة الزيارة إلى كندا",
            "desc": "تجهيز وتنظيم المستندات الداعمة لطلب الزيارة، مع إعداد مسودات غرض السفر "
                    "وخطة الرحلة بناءً على بياناتك.",
            "deliver": ["قائمة مستندات الزيارة", "مسودة غرض السفر وخطة الرحلة",
                        "مراجعة اكتمال الملف إداريًا"],
            "incl": ["تجهيز وتنظيم مستندات الزيارة", "إعداد المسودات الوصفية"],
            "excl": ["نصيحة هجرة فردية", "الرسوم الحكومية", "تمثيل بلا صفة مخوّلة"],
        },
    ],
    "أستراليا": [
        {
            "sku": "AU-SC600", "price": 1430000, "duration": "حسب الطلب",
            "badge": "الأكثر طلبًا",
            "name": "باقة تأشيرة الزيارة — Subclass 600",
            "desc": "مساعدة إدارية في تجهيز وتنظيم مستندات طلب تأشيرة الزيارة، من تعبئة "
                    "النماذج حتى التحضير للمقابلة، مع متابعة إدارية.",
            "deliver": ["تنظيم مستندات Subclass 600", "المساعدة في تعبئة النماذج",
                        "تحضير إجرائي للمقابلة ومتابعة"],
            "incl": ["تجهيز وتنظيم المستندات", "نقل المعلومات وإدخال البيانات إداريًا"],
            "excl": ["صفة مهنية غير مخوّلة", "ضمان نتيجة الطلب", "الرسوم الحكومية"],
        },
    ],
}


def package_card(p, dest, rp):
    deliver = ''.join(f"<li>{icon('check')}<span>{x}</span></li>" for x in p["deliver"])
    incl = ''.join(f"<li>{icon('check')}<span>{x}</span></li>" for x in p["incl"])
    excl = ''.join(f"<li>{icon('x')}<span>{x}</span></li>" for x in p["excl"])
    badge = (f'<span class="svc__badge">{p["badge"]}</span>' if p.get("badge") else "")
    return f"""
    <article class="svc">
      <div class="svc__head">
        <span class="svc__tags"><span class="chip">{dest}</span>{badge}</span>
        <span class="sku">SKU: {p['sku']}</span>
      </div>
      <h3>{p['name']}</h3>
      <p class="svc__desc">{p['desc']}</p>
      <div class="svc__priceline">
        <span class="svc__amount">{iqd(p['price'])}</span><span class="svc__cur">د.ع</span>
      </div>
      <p class="svc__meta">{icon('clock')} مدة التنفيذ: {p['duration']}</p>
      <div class="svc__block">
        <h4>ما ستستلمه (Deliverables)</h4>
        <ul class="ticklist">{deliver}</ul>
      </div>
      <div class="svc__cols">
        <div><h4>تشمل الباقة</h4><ul class="ticklist">{incl}</ul></div>
        <div><h4>لا تشمل</h4><ul class="ticklist ticklist--no">{excl}</ul></div>
      </div>
      <p class="svc__price">{icon('card')} رسوم الخدمة فقط — الرسوم الحكومية منفصلة وتُدفع
         للجهات المختصة مباشرةً.</p>
      <p class="svc__note">يبدأ التنفيذ بعد تأكيد الدفع والتحقق منه. المدة تقديرية ولا تضمن
         قبول التأشيرة أو مدة قرار الجهة المختصة.</p>
      <div class="svc__cta">
        <a class="btn btn--primary btn--block"
           href="{rp}client/index.html?dest={quote(dest)}&pkg={quote(p['name'])}#order">ابدأ طلب الباقة</a>
      </div>
    </article>"""


# =================================================================
# PAGE BUILDERS
# =================================================================

def build_home():
    rp = rel_prefix("/")
    body = (hero_block(rp) + trust_strip() + destinations_block(rp)
            + whyus_block() + howitworks_block() + promises_block() + cta_block(rp))
    page("/", "رحلة R7LE | خدمات تجهيز مستندات السفر لأمريكا وكندا وأستراليا",
         "منصّة عراقية مستقلة لخدمات المساعدة الإدارية وتجهيز مستندات طلب تأشيرة الزيارة "
         "لأمريكا وكندا وأستراليا، بأسعار معلنة وشروط واضحة ودعم بالعربية.", body)


def destination_body(rp, slug, title, kicker, intro, services_filter, sections):
    crumb = breadcrumb([("/", "الرئيسية"), (f"/{slug}/", title)], rp)
    pkgs = PACKAGES.get(services_filter, [])
    svc = ''.join(package_card(p, services_filter, rp) for p in pkgs)
    svc_wrap = (f'<div class="pkg-single">{svc}</div>' if len(pkgs) == 1
                else f'<div class="grid grid--2">{svc}</div>')
    sec_html = ""
    for h, items in sections:
        li = ''.join(f"<li>{icon('check')}<span>{x}</span></li>" for x in items)
        sec_html += f"""
    <div class="prose-card">
      <h2>{h}</h2>
      <ul class="ticklist">{li}</ul>
    </div>"""
    alts = {"usa": "تمثال الحرية في نيويورك", "canada": "أفق مدينة تورنتو الكندية",
            "australia": "ميناء سيدني — دار الأوبرا وجسر الميناء في أستراليا"}
    banner = f"""
<figure class="banner">
  <img src="{rp}assets/img/photos/{slug}.jpg" alt="{alts.get(slug, title)}" width="820" height="512" loading="eager">
</figure>"""
    return (crumb + page_hero(title, intro, kicker) + banner
            + f"""
<section class="section">
  <div class="wrap">
    {shead("الباقات والأسعار", "باقات التأشيرة السياحية",
           "الأسعار بالدينار العراقي وتمثّل رسوم الخدمة فقط؛ الرسوم الحكومية منفصلة. "
           "كل باقة توضّح ما تشمل وما لا تشمل والمخرجات.")}
    {svc_wrap}
  </div>
</section>
<section class="section section--alt">
  <div class="wrap grid grid--2">{sec_html}</div>
</section>"""
            + cta_block(rp))


def build_usa():
    rp = rel_prefix("/usa/")
    body = destination_body(
        rp, "usa", "أمريكا — الولايات المتحدة", "وجهة · USA",
        "خدمات إدارية لتجهيز وتنظيم مستندات تأشيرة الزيارة B1/B2، مع فصل واضح بين الدعم "
        "الإداري والاستشارة القانونية.",
        "أمريكا",
        [("ما نساعد فيه", ["تجهيز مستندات B1/B2", "مساعدة إدارية في بيانات DS-160",
                           "تحضير إجرائي للمقابلة والتحقق من المواعيد ضمن المسموح"]),
         ("ما لا نقوم به", ["ضمان المواعيد أو نتائج الطلب",
                            "تقييم أهلية أو اختيار مسار هجرة بناءً على حالة الشخص",
                            "صياغة حجج قانونية أو تمثيل رسمي"])])
    page("/usa/", "تأشيرة أمريكا B1/B2 للعراقيين | تجهيز المستندات — رحلة R7LE",
         "خدمات رحلة R7LE الإدارية لتجهيز مستندات تأشيرة الزيارة الأمريكية B1/B2 للعراقيين، "
         "مع أسعار ورسوم معلنة وشروط واضحة.", body)


def build_canada():
    rp = rel_prefix("/canada/")
    body = destination_body(
        rp, "canada", "كندا", "وجهة · Canada",
        "خدمات تنظيم مستندات الزيارة السياحية والعائلية، ومراجعة اكتمال الملف الإداري، "
        "ومقالات معلوماتية عن البرامج المختلفة.",
        "كندا",
        [("ما نساعد فيه", ["تنظيم مستندات زيارة سياحية أو عائلية",
                           "مراجعة اكتمال الملف الإداري", "مقالات معلوماتية عن البرامج"]),
         ("قيود مهمة", ["لا نقدّم نصيحة هجرة فردية",
                        "لا تمثيل مدفوع بلا صفة مخوّلة",
                        "التمثيل في شؤون الهجرة مقيّد بالممثلين المخوّلين لدى الجهات الكندية"])])
    page("/canada/", "زيارة كندا للعراقيين | تنظيم مستندات الزيارة — رحلة R7LE",
         "خدمات رحلة R7LE لتنظيم مستندات زيارة كندا السياحية والعائلية للعراقيين، "
         "مع توضيح الفرق بين المتطلبات الحكومية ورسوم الخدمة الخاصة.", body)


def build_australia():
    rp = rel_prefix("/australia/")
    body = destination_body(
        rp, "australia", "أستراليا", "وجهة · Australia",
        "خدمات تنظيم مستندات تأشيرة الزيارة Subclass 600 ذات الصلة بالعراقيين، ونقل "
        "المعلومات وإدخال البيانات إداريًا حيث يكون ذلك مشروعًا.",
        "أستراليا",
        [("ما نساعد فيه", ["تنظيم مستندات تأشيرة الزيارة Subclass 600",
                           "فحص حدود وأهلية «immigrationassistance»",
                           "نقل المعلومات وإدخال البيانات إداريًا ضمن المسموح"]),
         ("قيود مهمة", ["يتطلب تقديم «immigrationassistance» اتخاذ صفة مهنية مناسبة",
                        "نلتزم بالقوانين والإرشادات الرسمية الأسترالية",
                        "لا ضمان لنتيجة الطلب"])])
    page("/australia/", "تأشيرة أستراليا Subclass 600 للعراقيين — رحلة R7LE",
         "خدمات رحلة R7LE لتنظيم مستندات تأشيرة الزيارة الأسترالية Subclass 600 "
         "للعراقيين، مع أسعار ورسوم معلنة.", body)


def build_services():
    rp = rel_prefix("/services/")
    crumb = breadcrumb([("/", "الرئيسية"), ("/services/", "الخدمات")], rp)
    dest_slug = {"أمريكا": "usa", "كندا": "canada", "أستراليا": "australia"}
    groups = ""
    for dest, pkgs in PACKAGES.items():
        cards_g = ''.join(package_card(p, dest, rp) for p in pkgs)
        wrap_g = (f'<div class="pkg-single">{cards_g}</div>' if len(pkgs) == 1
                  else f'<div class="grid grid--2">{cards_g}</div>')
        groups += f"""
<section class="section pkg-group">
  <div class="wrap">
    {shead("باقات " + dest, "باقات تأشيرة الزيارة — " + dest)}
    {wrap_g}
    <p class="center"><a class="link-arrow" href="{rp}{dest_slug[dest]}/index.html">تفاصيل وجهة {dest} {icon('arrow')}</a></p>
  </div>
</section>"""
    body = (crumb + page_hero(
        "الباقات والأسعار", "باقات التأشيرة السياحية لأمريكا وكندا وأستراليا. الأسعار "
        "بالدينار العراقي وتمثّل رسوم الخدمة فقط؛ الرسوم الحكومية منفصلة وتُدفع للجهات "
        "المختصة. الأسعار قابلة للتعديل قبل الاعتماد النهائي.",
        "كتالوج · Packages")
            + groups
            + cta_block(rp))
    page("/services/", "الخدمات والأسعار | تجهيز مستندات السفر — رحلة R7LE",
         "كتالوج خدمات رحلة R7LE لتجهيز مستندات الزيارة لأمريكا وكندا وأستراليا، "
         "مع المخرجات والأسعار والرسوم المنفصلة والشروط.", body)


def build_howitworks():
    rp = rel_prefix("/howitworks/")
    crumb = breadcrumb([("/", "الرئيسية"), ("/howitworks/", "كيف نعمل")], rp)
    flow = [
        ("اختر الوجهة والخدمة", "أمريكا / كندا / أستراليا، واقرأ ما تشمل الخدمة وما لا تشمل."),
        ("املأ المعلومات الأولية", "بيانات تواصل أساسية بدون طلب مستندات حساسة في أول خطوة."),
        ("راجع السعر وأكّد الطلب", "تظهر رسوم الشركة والرسوم الحكومية بصورة منفصلة."),
        ("ادفع عبر مزوّد معتمد", "يُنشأ الطلب فقط بعد التحقق الخادمي من حالة الدفع."),
        ("استلم رقمًا مرجعيًا", "ثم تظهر قائمة المستندات المطلوبة لاحقًا داخل حسابك."),
        ("تابع التنفيذ والتسليم", "تحديثات عن تقدّم العمل حتى تسليم ملف الخدمة وإغلاق الطلب."),
    ]
    steps = ""
    for i, (t, d) in enumerate(flow, 1):
        steps += f"""<li class="step"><span class="step__num">{i}</span>
          <div><h3>{t}</h3><p>{d}</p></div></li>"""
    states = ["New", "AwaitingPayment", "Paid", "AwaitingDocuments",
              "InAdministrativeReview", "AdditionalDocumentsRequired",
              "Prepared", "Delivered", "Completed"]
    st = ''.join(f'<li>{s}</li>' for s in states)
    body = (crumb + page_hero(
        "كيف نعمل؟", "الخطوات الفعلية من إرسال الطلب حتى تسليم ملف الخدمة، مع التعامل الآمن "
        "مع حالات التأخّر أو الفشل.", "رحلة العميل · Flow")
            + f"""
<figure class="banner">
  <img src="{rp}assets/img/photos/appointment.jpg" width="900" height="600" loading="eager"
       alt="حجز موعد وتجهيز الطلب عبر الحاسوب">
</figure>
<section class="section">
  <div class="wrap"><ol class="steps steps--lg">{steps}</ol></div>
</section>
<section class="section section--alt">
  <div class="wrap">
    <div class="section__head"><h2>حالات الطلب المعتمدة</h2>
      <p>تخصّ تنفيذ عمل رحلة R7LE فقط، ولا يجوز تسميتها «EmbassyProcessing» أو
      «VisaApproved» دون مصدر رسمي موثوق وآلية مصرّح بها.</p></div>
    <ol class="states">{st}</ol>
    <p class="muted">بالإضافة إلى حالات مستقلة:
       <span class="chip chip--sm">Cancelled</span>
       <span class="chip chip--sm">RefundRequested</span>
       <span class="chip chip--sm">Refunded</span></p>
  </div>
</section>"""
            + cta_block(rp))
    page("/howitworks/", "كيف نعمل | خطوات طلب الخدمة — رحلة R7LE",
         "خطوات العمل في رحلة R7LE: اختيار الوجهة والخدمة، الدفع عبر مزوّد معتمد، إنشاء "
         "الطلب بعد التحقق، ثم المتابعة والتسليم، مع حالات الطلب المعتمدة.", body)


def build_faq():
    rp = rel_prefix("/faq/")
    crumb = breadcrumb([("/", "الرئيسية"), ("/faq/", "الأسئلة الشائعة")], rp)
    qa = [
        ("هل رحلة R7LE جهة حكومية أو سفارة؟",
         "لا. رحلة R7LE علامة تجارية لخدمات خاصة في المساعدة الإدارية وتجهيز وتنظيم "
         "المستندات. لسنا سفارة أو قنصلية أو جهة حكومية، ولسنا تابعين لسلطات الهجرة. "
         "ويمكن للعملاء استخدام القنوات الحكومية الرسمية مباشرة دون شراء خدماتنا."),
        ("هل تضمنون الحصول على التأشيرة؟",
         "لا نضمن قبول أي تأشيرة أو سرعة قرارها. القرارات النهائية بيد الجهات المختصة، "
         "وخدمتنا إدارية لتجهيز وتنظيم المستندات فقط."),
        ("كيف تظهر الأسعار والرسوم؟",
         "تُعرض رسوم الشركة بصورة منفصلة عن الرسوم الحكومية قبل تأكيد الدفع، بلا رسوم "
         "مخفية، مع توضيح العملة والمبلغ وسياسة الاسترداد."),
        ("هل تطلبون جواز السفر من أول خطوة؟",
         "لا. نجمع البيانات على مراحل، ولا نطالب برفع الجواز قبل أن يصبح ذلك ضروريًا "
         "للخدمة. في أول خطوة نطلب بيانات تواصل أساسية فقط."),
        ("ما طرق الدفع المتاحة؟",
         "الدفع عبر مزوّد معتمد يقبل نشاط الشركة وطرق الدفع المتاحة فعليًا في العراق. "
         "لا نعرض شعارات وسائل دفع غير مفعّلة، ولا نخزّن بيانات البطاقة على خادم الموقع."),
        ("هل يمكنني متابعة طلبي؟",
         "نعم، عبر حساب العميل الآمن: عرض الطلبات والفواتير، رفع المستندات المطلوبة، "
         "وسجل رسائل خاص بكل طلب، وتنزيل النسخ النهائية وفق سياسة الاحتفاظ."),
        ("هل يمكنني طلب استرداد؟",
         "نعم وفق سياسة الاسترداد المعلنة، حسب حالة التنفيذ وشروط كل خدمة. راجع صفحة "
         "سياسة الاسترداد للتفاصيل."),
        ("هل تستطيعون التقديم بدل الشخص رسميًا لدى الجهات الحكومية؟",
         "التقديم الحكومي الرسمي المباشر متاح للعميل دون شراء خدمتنا. أي تمثيل رسمي "
         "يتطلب صفة مخوّلة ومراجعة قانونية؛ وبدون ذلك نقدّم دعمًا إداريًا فقط."),
    ]
    acc = ""
    for i, (q, a) in enumerate(qa):
        acc += f"""
      <div class="acc">
        <button class="acc__btn" aria-expanded="false" aria-controls="a{i}">
          <span>{q}</span><span class="acc__ic" aria-hidden="true">+</span>
        </button>
        <div class="acc__panel" id="a{i}" hidden><p>{a}</p></div>
      </div>"""
    body = (crumb + page_hero(
        "الأسئلة الشائعة", "إجابات مباشرة عن أكثر ما يسأل عنه العراقيون — بشفافية وبلا وعود.",
        "FAQ")
            + f"""<section class="section"><div class="wrap narrow">{acc}</div></section>"""
            + cta_block(rp))
    page("/faq/", "الأسئلة الشائعة | رحلة R7LE",
         "أسئلة شائعة عن خدمات رحلة R7LE الإدارية: الأسعار، الدفع، المستندات، الاسترداد، "
         "وحدود الخدمة — بشفافية وبدون ضمانات.", body)


def build_blog():
    rp = rel_prefix("/blog/")
    crumb = breadcrumb([("/", "الرئيسية"), ("/blog/", "المدونة")], rp)
    posts = [
        ("تأشيرة أمريكا للعراقيين: الخطوات الرسمية والوثائق",
         "الخطوات الرسمية والوثائق، ومتى تحتاج للخدمة الإدارية.", "أمريكا", "usa"),
        ("زيارة كندا للعراقيين: الفرق بين المتطلبات الحكومية ورسوم الخدمة",
         "توضيح الفرق بين المتطلبات الحكومية الرسمية ورسوم الخدمة الخاصة.", "كندا", "canada"),
        ("أستراليا Subclass 600: المستندات والخطوات الرسمية",
         "الوثائق والخطوات الرسمية ذات الصلة بالعراقيين.", "أستراليا", "australia"),
        ("هل يستطيع حامل جواز عراقي التقديم من دولة إقامته؟",
         "معلومات بحسب الإجراء المعتمد ومصدره الرسمي.", "معلومات", "travel"),
        ("كيف تجهّز أوراق العائلة أو القاصرين للسفر؟",
         "مع رابط التعليمات الحكومية الحديثة.", "معلومات", "appointment"),
    ]
    cards = ""
    for t, d, cat, img in posts:
        cards += f"""
      <article class="post">
        <div class="post__img"><img src="{rp}assets/img/photos/{img}.jpg" alt="" width="820" height="512" loading="lazy">
          <span class="chip chip--sm">{cat}</span></div>
        <div class="post__body">
          <h3>{t}</h3>
          <p>{d}</p>
          <p class="post__meta">{icon('clock')} آخر مراجعة: {TODAY} · المصادر رسمية</p>
          <span class="link-arrow link-arrow--muted">قريبًا {icon('arrow')}</span>
        </div>
      </article>"""
    body = (crumb + page_hero(
        "المدونة", "مقالات معلوماتية مخصّصة للعراقيين — كل مقال يتضمّن تاريخ آخر مراجعة "
        "ومصادر رسمية، مع إيضاح أن الإجراءات والرسوم قابلة للتغيير.", "محتوى · Blog")
            + f"""<section class="section"><div class="wrap">
      <div class="grid grid--3">{cards}</div>
      <p class="muted center">المقالات قيد الإعداد ضمن المرحلة الثانية من خطة التنفيذ.</p>
      </div></section>""")
    page("/blog/", "المدونة | معلومات السفر والتأشيرات للعراقيين — رحلة R7LE",
         "مقالات رحلة R7LE المعلوماتية للعراقيين عن تأشيرات أمريكا وكندا وأستراليا، "
         "موثّقة بمصادر رسمية وتاريخ مراجعة.", body)


def build_client():
    rp = rel_prefix("/client/")
    crumb = breadcrumb([("/", "الرئيسية"), ("/client/", "حساب العميل")], rp)
    body = (crumb + page_hero(
        "ابدأ طلب الباقة", "املأ بياناتك الأساسية لبدء الطلب — بدون تسجيل دخول ولا مستندات "
        "حساسة في هذه الخطوة. تظهر الرسوم منفصلة قبل الدفع.",
        "طلب الخدمة")
            + f"""
<section class="section">
  <div class="wrap narrow">
    <div class="formcard" id="order">
      <h2>{icon('doc')} بيانات الطلب</h2>
      <div class="order-summary" id="order-summary" hidden>
        <span class="order-summary__label">الباقة المختارة</span>
        <strong id="order-pkg"></strong>
        <span class="chip" id="order-dest"></span>
      </div>
      <form class="form" onsubmit="return false">
        <input type="hidden" id="order-dest-input" name="dest">
        <input type="hidden" id="order-pkg-input" name="pkg">
        <label>الاسم الكامل <input type="text" placeholder="الاسم الثلاثي" required></label>
        <div class="form__row">
          <label>رقم الهاتف
            <input type="tel" inputmode="tel" dir="ltr" placeholder="+964 7XX XXX XXXX" required></label>
          <label>المحافظة (اختياري)
            <input type="text" placeholder="مثال: بغداد"></label>
        </div>
        <label>البريد الإلكتروني (اختياري)
          <input type="email" dir="ltr" autocomplete="email" placeholder="name@email.com"></label>
        <label class="check"><input type="checkbox" required>
          <span>أوافق على <a href="{rp}terms/index.html">الشروط</a> و<a href="{rp}privacypolicy/index.html">الخصوصية</a>.</span></label>
        <button class="btn btn--primary btn--block" type="submit">متابعة لمراجعة السعر</button>
        <p class="muted sm">لا نطلب تسجيل دخول في هذه الخطوة. بعد تأكيد الطلب يُنشأ لك رقم
           مرجعي لمتابعته ورفع المستندات لاحقًا.</p>
      </form>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap">
    {shead("بعد الطلب", "ماذا يحدث بعد إرسال طلبك؟")}
    <div class="grid grid--3">
      <div class="feature">{icon('doc')}<h3>رقم مرجعي وفاتورة</h3>
        <p>يُنشأ رقم مرجعي للطلب، وتُعرض الطلبات والفواتير والإيصالات لمتابعتها.</p></div>
      <div class="feature">{icon('shield')}<h3>رفع آمن للمستندات</h3>
        <p>قائمة المستندات المطلوبة مع رفع آمن لاحقًا، وتوضيح ما ينقص منك.</p></div>
      <div class="feature">{icon('chat')}<h3>سجل رسائل لكل طلب</h3>
        <p>متابعة واضحة دون إظهار بيانات داخلية، مع المسؤول عن المتابعة.</p></div>
    </div>
  </div>
</section>""")
    page("/client/", "ابدأ طلب الباقة | رحلة R7LE",
         "ابدأ طلب باقة تجهيز مستندات التأشيرة من رحلة R7LE ببيانات أساسية بدون تسجيل دخول، "
         "مع إنشاء رقم مرجعي لمتابعة الطلب ورفع المستندات لاحقًا.", body)


def build_aboutus():
    rp = rel_prefix("/aboutus/")
    crumb = breadcrumb([("/", "الرئيسية"), ("/aboutus/", "من نحن")], rp)
    rows = [
        ("العلامة التجارية", "رحلة R7LE"),
        ("الكيان المشغّل المسجَّل فعليًا", SITE["entity"]),
        ("رقم التسجيل", SITE["reg_no"]),
        ("العنوان الحقيقي", SITE["address"]),
        ("نطاق الخدمة", "مساعدة إدارية وتجهيز وتنظيم مستندات السفر — أمريكا وكندا وأستراليا"),
        ("وسائل التواصل", f"{SITE['email']} · واتساب: {SITE['whatsapp']}"),
    ]
    tr = ''.join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
    body = (crumb + page_hero(
        "من نحن", "رحلة re7le مقدّم خدمات خاص ومستقل، يقدّم مساعدة إدارية وتجهيزًا وتنظيمًا "
        "للمستندات — دون أي صفة حكومية.", "About")
            + f"""
<figure class="banner"><img src="{rp}assets/img/photos/travel.jpg" width="1100" height="1000"
   alt="جواز سفر ونافذة طائرة — رمز لرحلة السفر" loading="eager"></figure>
<section class="section">
  <div class="wrap narrow">
    <div class="prose">
      <p>نعمل على تبسيط تجربة العراقي الراغب في السفر، عبر خدمات واضحة المعالم في تجهيز
         وتنظيم مستندات طلب التأشيرة، بأسعار معلنة وشروط مكتوبة. التقديم الحكومي الرسمي
         المباشر متاح للجميع دون شراء خدماتنا.</p>
    </div>
    <table class="spec">{tr}</table>
    <div class="callout">{icon('scale')}
      <p>الحقول المعلّمة بـ«قيد التأكيد» تُثبّت من قِبل مالك المشروع قبل الإطلاق،
      بما يتوافق مع هوية الكيان المشغّل الحقيقي (القسم 16 من وثيقة المواصفات).</p></div>
  </div>
</section>""")
    page("/aboutus/", "من نحن | رحلة R7LE",
         "تعرّف على رحلة R7LE: مقدّم خدمات خاص ومستقل للمساعدة الإدارية وتجهيز مستندات "
         "السفر، مع بيانات الكيان المشغّل ووسائل التواصل.", body)


def build_contact():
    rp = rel_prefix("/contact/")
    crumb = breadcrumb([("/", "الرئيسية"), ("/contact/", "تواصل")], rp)
    body = (crumb + page_hero(
        "تواصل ويانا", "فريقنا يجاوبك. للأسئلة العامة أو بدء طلب خدمة — بدون مشاركة "
        "مستندات حساسة في أول تواصل.", "Contact")
            + f"""
<section class="section">
  <div class="wrap grid grid--2 grid--top">
    <div class="contact-info">
      <a class="contact-tile" href="{SITE['whatsapp_link']}" rel="nofollow">{icon('wa')}
        <div><b>واتساب</b><span>{SITE['whatsapp']}</span></div></a>
      <a class="contact-tile" href="mailto:{SITE['email']}">{icon('mail')}
        <div><b>البريد الإلكتروني</b><span>{SITE['email']}</span></div></a>
      <div class="contact-tile">{icon('clock')}
        <div><b>ساعات العمل</b><span>{SITE['hours']}</span></div></div>
      <div class="contact-tile">{icon('pin')}
        <div><b>الجهة المشغّلة</b><span>{SITE['entity']}</span></div></div>
    </div>
    <div class="formcard">
      <h2>{icon('chat')} أرسل رسالة</h2>
      <form class="form" onsubmit="return false">
        <label>الاسم <input type="text" required></label>
        <label>البريد أو الهاتف <input type="text" dir="ltr" required></label>
        <label>رسالتك <textarea rows="4" required></textarea></label>
        <button class="btn btn--primary btn--block" type="submit">إرسال</button>
        <p class="muted sm">بإرسالك توافق على <a href="{rp}privacypolicy/index.html">سياسة الخصوصية</a>.</p>
      </form>
    </div>
  </div>
</section>""")
    page("/contact/", "تواصل معنا | رحلة R7LE",
         "تواصل مع فريق رحلة R7LE عبر واتساب أو البريد الإلكتروني لبدء طلب خدمة أو "
         "للاستفسارات العامة.", body)


def legal_page(path, title, desc, kicker, intro, sections):
    rp = rel_prefix(path)
    slug = path.strip("/")
    label = {"terms": "الشروط والأحكام", "privacypolicy": "سياسة الخصوصية",
             "refundpolicy": "سياسة الاسترداد", "disclaimer": "إخلاء المسؤولية"}[slug]
    crumb = breadcrumb([("/", "الرئيسية"), (path, label)], rp)
    sec = ""
    for h, paras in sections:
        body_html = ""
        for p in paras:
            if isinstance(p, list):
                body_html += "<ul class='ticklist'>" + ''.join(
                    f"<li>{icon('check')}<span>{x}</span></li>" for x in p) + "</ul>"
            else:
                body_html += f"<p>{p}</p>"
        sec += f"<section class='legal__sec'><h2>{h}</h2>{body_html}</section>"
    body = (crumb + page_hero(title, intro, kicker)
            + f"""<div class="section"><div class="wrap narrow legal">
      <p class="legal__updated">{icon('clock')} آخر تحديث: {TODAY}</p>
      {sec}
      <div class="callout">{icon('shield')}<p>{DISCLOSURE}</p></div>
    </div></div>""")
    page(path, f"{title} | رحلة R7LE", desc, body)


def build_legal():
    legal_page(
        "/terms/", "الشروط والأحكام",
        "شروط وأحكام استخدام خدمات رحلة R7LE الإدارية لتجهيز مستندات السفر.",
        "قانوني · Terms",
        "تحكم هذه الشروط العلاقة التعاقدية بين العميل ورحلة R7LE عند طلب أي خدمة.",
        [("التعاقد والخدمة المتفق عليها",
          ["تحدّد كل بطاقة خدمة نطاقها ومخرجاتها وسعرها وشروطها قبل الطلب، وتمثّل الأساس "
           "المتفق عليه عند تأكيد الدفع."]),
         ("مسؤولية العميل عن صحة البيانات",
          ["يتحمّل العميل مسؤولية صحة ودقّة البيانات والمستندات المقدَّمة، وأي قرار نهائي "
           "يبقى بيد الجهات الرسمية المختصة."]),
         ("حدود تنفيذ الخدمة وحقوق الأطراف",
          ["خدماتنا إدارية لتجهيز وتنظيم المستندات، ولا تشمل ضمان المواعيد أو نتائج الطلب، "
           "ولا تقديم استشارة أو تمثيل يتطلب صفة مخوّلة.",
           "المدد الإدارية تقديرية ولا تضمن مدة قرار السفارة."]),
         ("المنازعات",
          ["تُسوّى الخلافات وفق الآلية المبيّنة في الاتفاقية والقانون الواجب التطبيق."])])

    legal_page(
        "/privacypolicy/", "سياسة الخصوصية",
        "كيف تجمع رحلة R7LE البيانات وتعالجها وتحميها، وحقوقك تجاه بياناتك.",
        "قانوني · Privacy",
        "نلتزم بحماية بياناتك وجمعها على مراحل، وعدم طلب مستندات حساسة قبل الحاجة.",
        [("فئات البيانات وأسس المعالجة",
          ["نجمع بيانات التواصل الأساسية أولًا، ثم المستندات المطلوبة للخدمة على مراحل، "
           "لأغراض محدّدة ومشروعة فقط."]),
         ("المشاركة والمعالِجون والتخزين",
          ["لا نرسل أرقام الجوازات أو محتوى النماذج الحساسة إلى أدوات التحليلات أو الإعلانات.",
           "يُختبر أي نقل دولي للبيانات أو مشاركة مع مزوّد أو استضافة أو أدوات تحليل قبل "
           "التفعيل، وفق القوانين الواجبة."]),
         ("التخزين والحذف وأمن البيانات",
          ["تُشفّر الملفات والمعلومات الحساسة عند الحفظ، مع نسخ احتياطية مشفّرة وصلاحيات "
           "أقل امتياز (Least Privilege) ومنع الروابط الدائمة للتنزيل."]),
         ("حقوقك",
          [["الوصول إلى بياناتك وتصحيحها", "طلب الحذف وفق سياسة الاحتفاظ",
            "الاستفسار عن الخصوصية وإدارة الموافقات", f"التواصل عبر {SITE['email']}"]])])

    legal_page(
        "/refundpolicy/", "سياسة الاسترداد",
        "شروط الاسترداد والتأجيل والاستثناءات لخدمات رحلة R7LE.",
        "قانوني · Refund",
        "تُعرض الأسعار وحدود الاسترداد والمصاريف الخارجية قبل الدفع — بلا رسوم مخفية.",
        [("المواعيد والخدمات المنفّذة جزئيًا",
          ["يعتمد الاسترداد على حالة التنفيذ وقت الطلب وشروط كل خدمة؛ قد تُخصم قيمة الأعمال "
           "المنفّذة فعليًا والمصاريف الخارجية غير المستردّة."]),
         ("حالات الإلغاء وطريقة تقديم الطلب",
          ["يُقدَّم طلب الاسترداد عبر حساب العميل وفق الشروط، وتُسوّى المدفوعات والمبالغ "
           "المستردة وربطها بالمعرّفات المالية."]),
         ("استثناءات محدّدة ومشروعة",
          ["الرسوم الرسمية المدفوعة للجهات الحكومية عبر قنواتها قد لا تكون قابلة للاسترداد "
           "من خلالنا بحسب الإجراء الفعلي."])])

    legal_page(
        "/disclaimer/", "إخلاء المسؤولية",
        "صفة رحلة R7LE كمقدّم خدمة خاص، وعدم الارتباط الحكومي، وعدم ضمان التأشيرة.",
        "قانوني · Disclaimer",
        "إفصاح مستقل يظهر على صفحات الخدمات والدفع.",
        [("صفة مقدّم الخدمة الخاصة",
          ["رحلة R7LE مقدّم خدمات خاص ومستقل، وليست جهة حكومية أو سفارة أو قنصلية، "
           "وليست تابعة لسلطات الهجرة الأمريكية أو الكندية أو الأسترالية."]),
         ("عدم الارتباط الحكومي وعدم ضمان التأشيرة",
          ["التقديم الحكومي الرسمي المباشر متاح دون شراء خدماتنا.",
           "لا نضمن قبول أي تأشيرة أو سرعة قرارها؛ تبقى القرارات النهائية بيد الجهات المختصة."]),
         ("روابط الجهات الرسمية",
          ["نوصي بالرجوع إلى المصادر الحكومية الرسمية للتحقق من الإجراءات والرسوم الحديثة، "
           "فهي قابلة للتغيير."])])


def build_404():
    rp = "./"
    body = (f"""
<section class="page-hero"><div class="wrap">
  <span class="eyebrow">خطأ 404</span>
  <h1>الصفحة غير موجودة</h1>
  <p class="lead">يبدو أن الرابط غير صحيح أو أن الصفحة نُقلت.</p>
  <p><a class="btn btn--primary btn--lg" href="{rp}index.html">العودة للرئيسية</a></p>
</div></section>""")
    html = (head("الصفحة غير موجودة | رحلة R7LE", "الصفحة غير موجودة.", "/404.html", rp)
            + header("/404.html", rp) + disclosure_bar()
            + '<main id="main">' + body + '</main>' + footer(rp))
    (ROOT / "404.html").write_text(html, encoding="utf-8")


# ---------- assets ----------
def write_assets():
    (ROOT / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (ROOT / "assets" / "js").mkdir(parents=True, exist_ok=True)
    (ROOT / "assets" / "img").mkdir(parents=True, exist_ok=True)
    (ROOT / "assets" / "css" / "styles.css").write_text(CSS, encoding="utf-8")
    (ROOT / "assets" / "js" / "main.js").write_text(JS, encoding="utf-8")
    (ROOT / "assets" / "img" / "favicon.svg").write_text(FAVICON, encoding="utf-8")


def write_seo():
    routes = ["/", "/usa/", "/canada/", "/australia/", "/services/", "/howitworks/",
              "/faq/", "/blog/", "/client/", "/aboutus/", "/contact/", "/terms/",
              "/privacypolicy/", "/refundpolicy/", "/disclaimer/"]
    urls = ""
    for r in routes:
        urls += (f"  <url><loc>{SITE['base_url']}{r}</loc>"
                 f"<changefreq>weekly</changefreq>"
                 f"<priority>{'1.0' if r == '/' else '0.7'}</priority></url>\n")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + urls + "</urlset>\n")
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    robots = (f"User-agent: *\nAllow: /\n\nSitemap: {SITE['base_url']}/sitemap.xml\n")
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    # GitHub Pages: no Jekyll processing
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">'
           '<rect width="40" height="40" rx="9" fill="#0E6E7D"/>'
           '<path d="M20 9l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L20 29.5 14.4 32l1.1-6.2L11 21.4l6.2-.9L20 9z" fill="#F2A516"/>'
           '</svg>\n')


# CSS kept as a plain string (no f-string) to avoid brace escaping.
CSS = r""":root{
  --ink:#0B1F2A; --ink-2:#1E3340; --muted:#5E7180; --line:#E3E9ED;
  --bg:#F6F8F9; --card:#FFFFFF;
  --primary:#0E6E7D; --primary-d:#0A5560; --primary-l:#E6F1F2;
  --accent:#F2A516; --accent-d:#C9820A;
  --ok:#128A6B; --ok-bg:#E6F4EF; --no:#C0392B; --no-bg:#FBECEA;
  --wa:#25D366; --wa-d:#1DA851;
  --r:14px; --r-sm:10px; --shadow:0 10px 30px rgba(11,31,42,.08);
  --shadow-sm:0 4px 14px rgba(11,31,42,.06);
  --wrap:1160px; --font:"Tajawal",system-ui,"Segoe UI",Arial,sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:var(--font);color:var(--ink);background:var(--bg);
  line-height:1.75;font-size:17px;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{line-height:1.3;margin:0 0 .4em;color:var(--ink);font-weight:800}
h1{font-size:clamp(1.9rem,5vw,3rem)}
h2{font-size:clamp(1.5rem,3.5vw,2.1rem)}
h3{font-size:1.2rem}
p{margin:0 0 1rem}
a{color:var(--primary-d);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%;display:block}
ul{margin:0;padding:0;list-style:none}
.wrap{width:100%;max-width:var(--wrap);margin-inline:auto;padding-inline:16px}
.narrow{max-width:820px}
.ic{width:1.25em;height:1.25em;flex:none;vertical-align:middle}
.muted{color:var(--muted)}
.sm{font-size:.9rem}
.center{text-align:center}
.skip{position:absolute;right:-999px;top:0;background:var(--primary);color:#fff;
  padding:10px 16px;z-index:200;border-radius:0 0 8px 8px}
.skip:focus{right:16px}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px;border-radius:6px}

/* buttons */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;
  font-family:inherit;font-weight:700;font-size:1rem;padding:.72rem 1.3rem;
  border-radius:var(--r-sm);border:1.5px solid transparent;cursor:pointer;
  transition:.18s;white-space:nowrap;text-decoration:none}
.btn:hover{text-decoration:none;transform:translateY(-1px)}
.btn--lg{padding:.9rem 1.7rem;font-size:1.05rem}
.btn--block{width:100%}
.btn--primary{background:var(--primary);color:#fff}
.btn--primary:hover{background:var(--primary-d);color:#fff}
.btn--ghost{background:transparent;color:var(--primary-d);border-color:var(--line)}
.btn--ghost:hover{border-color:var(--primary);background:var(--primary-l)}
.btn--light{background:#fff;color:var(--primary-d)}
.btn--light:hover{background:#eef4f5;color:var(--primary-d)}
.btn--wa{background:var(--wa);color:#07301c}
.btn--wa:hover{background:var(--wa-d);color:#fff}

/* header */
.site-head{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.92);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.site-head__row{display:flex;align-items:center;gap:1rem;min-height:68px}
.logo{display:inline-flex;align-items:center;gap:.55rem;font-weight:800;color:var(--ink)}
.logo:hover{text-decoration:none}
.logo__mark{width:46px;height:46px;flex:none;display:inline-flex;border-radius:11px;
  overflow:hidden;background:#fff}
.logo__mark img{width:100%;height:100%;object-fit:contain;display:block}
.logo__txt{display:flex;flex-direction:column;line-height:1}
.logo__txt b{font-size:1.25rem}
.logo__txt i{font-style:normal;font-size:.74rem;letter-spacing:.16em;color:var(--accent-d);font-weight:700;text-transform:lowercase}
.logo--mono{color:#fff}
.logo--mono .logo__mark{box-shadow:0 0 0 1px rgba(255,255,255,.18)}
.logo--mono .logo__txt i{color:var(--accent)}
.nav{margin-inline-start:auto}
.nav__list{display:flex;gap:.3rem}
.nav__list a{display:block;padding:.5rem .7rem;border-radius:8px;color:var(--ink-2);
  font-weight:500;font-size:.98rem}
.nav__list a:hover{background:var(--primary-l);color:var(--primary-d);text-decoration:none}
.nav__list a[aria-current]{color:var(--primary-d);background:var(--primary-l);font-weight:700}
.site-head__cta{display:flex;gap:.5rem;align-items:center}
.site-head__cta .btn{padding:.55rem 1rem;font-size:.95rem}
.nav-toggle{display:none;background:none;border:1px solid var(--line);border-radius:10px;
  width:46px;height:46px;color:var(--ink);cursor:pointer;align-items:center;justify-content:center}
.nav-toggle .ic{width:26px;height:26px}
.mobile-nav{border-bottom:1px solid var(--line);background:#fff;padding:.5rem 16px 1rem}
.mobile-nav ul{display:flex;flex-direction:column}
.mobile-nav a{display:block;padding:.85rem .4rem;border-bottom:1px solid var(--line);
  font-weight:600;color:var(--ink-2)}
.mobile-nav a[aria-current]{color:var(--primary-d)}
.mobile-nav__cta{display:flex;flex-direction:column;gap:.6rem;margin-top:1rem}

/* disclosure */
.disclosure{background:#07323a;color:#cfe6e8}
.disclosure__row{display:flex;gap:.7rem;align-items:flex-start;padding-block:.6rem}
.disclosure .ic{color:var(--accent);margin-top:.15rem}
.disclosure p{margin:0;font-size:.82rem;line-height:1.6}

/* hero */
.hero{background:
  radial-gradient(1200px 500px at 85% -10%,rgba(14,110,125,.14),transparent),
  linear-gradient(180deg,#fff, var(--bg))}
.hero__inner{display:grid;grid-template-columns:1.1fr .9fr;gap:2.5rem;align-items:center;
  padding-block:clamp(2.5rem,6vw,5rem)}
/* full-bleed background hero: image first, content over it */
/* framed hero: full image shown as a block on white; text overlaid */
.hero--framed{background:#fff;padding-block:clamp(1.6rem,4vw,3rem)}
.hero--framed::before{content:none}
.hero__frame{position:relative;max-width:1060px;margin-inline:auto;border-radius:22px;
  overflow:hidden;box-shadow:0 24px 60px rgba(11,31,42,.16)}
.hero__bg{display:block;width:100%;height:auto}
.hero__overlay{position:absolute;inset:0;z-index:1;background:
  linear-gradient(to left,rgba(5,22,27,.84),rgba(5,22,27,.46) 48%,rgba(5,22,27,.14))}
.hero__content{position:absolute;inset-block:0;inset-inline-start:0;z-index:2;color:#fff;
  width:min(480px,56%);display:flex;flex-direction:column;justify-content:center;
  align-items:flex-start;text-align:start;padding:clamp(1.4rem,3vw,2.6rem)}
.hero__content .hero__cta{justify-content:flex-start}
.hero__content h1{color:#fff;text-shadow:0 2px 22px rgba(0,0,0,.45)}
.hero__content .lead{color:#e9f2f3;text-shadow:0 1px 12px rgba(0,0,0,.4)}
.eyebrow--light{background:rgba(255,255,255,.18);color:#fff;border:1px solid rgba(255,255,255,.32)}
.eyebrow--light .ic{color:#fff}
.btn--light{border-color:var(--line)}
.eyebrow{display:inline-flex;align-items:center;gap:.4rem;background:var(--primary-l);
  color:var(--primary-d);font-weight:700;font-size:.85rem;padding:.4rem .8rem;border-radius:999px;
  margin-bottom:1rem}
.lead{font-size:1.12rem;color:var(--ink-2);max-width:52ch}
.hero__cta{display:flex;gap:.8rem;flex-wrap:wrap;margin:1.4rem 0}
.hero__badges{display:flex;flex-wrap:wrap;gap:.5rem 1.3rem;margin-top:.6rem}
.hero__badges li{display:flex;gap:.4rem;align-items:center;color:var(--ink-2);font-weight:600;font-size:.95rem}
.hero__badges .ic{color:var(--ok)}
.hero__media{position:relative}
.hero__media>img{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;
  border-radius:20px;box-shadow:var(--shadow)}
.hero__ticket{position:absolute;inset-inline-start:-14px;bottom:24px;background:rgba(255,255,255,.96);
  backdrop-filter:blur(6px);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);
  padding:.9rem 1.1rem;min-width:240px}
.hero__ticket-head{display:flex;justify-content:space-between;align-items:center;gap:.6rem;
  font-weight:800;color:var(--primary-d);margin-bottom:.6rem}
.hero__ticket-head .ic{color:var(--accent-d)}
.hero__ticket-route{display:flex;justify-content:space-between;align-items:center;gap:.6rem}
.hero__ticket-route b{display:block;font-size:1rem}
.hero__ticket-route small{color:var(--muted);font-size:.78rem}
.hero__plane{color:var(--primary);transform:scaleX(-1)}
.hero__plane .ic{width:1.5em;height:1.5em}

/* banner figure */
.banner{margin:0;padding:1.6rem 16px 0}
.banner img{display:block;width:100%;max-width:var(--wrap);margin-inline:auto;height:auto;
  aspect-ratio:16/7;object-fit:cover;border-radius:var(--r);box-shadow:var(--shadow-sm)}

/* sections */
.section{padding-block:clamp(2.5rem,5vw,4.2rem)}
.section--alt{background:#fff;border-block:1px solid var(--line)}
.section__head{text-align:center;max-width:62ch;margin:0 auto 2.2rem}
.section__head p{color:var(--muted);font-size:1.05rem}
.grid{display:grid;gap:1.3rem}
.grid--2{grid-template-columns:repeat(2,1fr)}
.grid--3{grid-template-columns:repeat(3,1fr)}
.grid--top{align-items:start}

/* destination cards */
.dest-card{background:var(--card);border:1px solid var(--line);border-radius:var(--r);
  overflow:hidden;box-shadow:var(--shadow-sm);transition:.2s;display:flex;flex-direction:column}
.dest-card:hover{box-shadow:var(--shadow);transform:translateY(-3px);border-color:#cfe0e2}
.dest-card__img{position:relative;display:block;aspect-ratio:820/420;overflow:hidden}
.dest-card__img img{width:100%;height:100%;object-fit:cover;transition:transform .4s}
.dest-card:hover .dest-card__img img{transform:scale(1.05)}
.dest-card__tag{position:absolute;inset-inline-start:12px;bottom:12px;display:inline-flex;
  align-items:center;gap:.35rem;background:rgba(7,35,42,.82);color:#fff;font-weight:700;
  font-size:.85rem;padding:.35rem .75rem;border-radius:999px;backdrop-filter:blur(4px)}
.dest-card__tag .ic{color:var(--accent);width:1.1em;height:1.1em}
.dest-card__body{padding:1.4rem 1.5rem 1.6rem}
.dest-card__body h3{margin:0 0 .5rem}
.link-arrow{display:inline-flex;align-items:center;gap:.35rem;font-weight:700;color:var(--primary-d)}
.link-arrow .ic{width:1.1em;height:1.1em;transform:scaleX(-1)}
.link-arrow--muted{color:var(--muted);cursor:default}

/* steps */
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:1.2rem;counter-reset:s}
.steps--lg{grid-template-columns:repeat(3,1fr)}
.step{background:var(--card);border:1px solid var(--line);border-radius:var(--r);
  padding:1.4rem;display:flex;gap:.9rem;align-items:flex-start;box-shadow:var(--shadow-sm)}
.step__num{flex:none;width:38px;height:38px;border-radius:50%;background:var(--primary);
  color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center}
.step h3{font-size:1.05rem;margin:0 0 .25rem}
.step p{margin:0;color:var(--muted);font-size:.95rem}

/* panels */
.panel{border-radius:var(--r);padding:1.6rem;border:1px solid var(--line);background:#fff}
.panel h3{display:flex;align-items:center;gap:.5rem}
.panel--ok{background:var(--ok-bg);border-color:#c9e7dd}
.panel--ok h3{color:var(--ok)}
.panel--no{background:var(--no-bg);border-color:#f2cfc9}
.panel--no h3{color:var(--no)}
.ticklist{display:flex;flex-direction:column;gap:.6rem}
.ticklist li{display:flex;gap:.55rem;align-items:flex-start}
.ticklist .ic{color:var(--ok);margin-top:.15rem}
.ticklist--no .ic{color:var(--no)}

/* cta banner */
.cta{background:linear-gradient(120deg,var(--primary-d),var(--primary));color:#fff}
.cta__inner{display:flex;align-items:center;justify-content:space-between;gap:1.5rem;
  padding-block:clamp(2rem,4vw,3rem);flex-wrap:wrap}
.cta h2{color:#fff}
.cta p{color:#d8ecee;margin:0;max-width:48ch}
.cta__btns{display:flex;gap:.8rem;flex-wrap:wrap}

/* page hero */
.page-hero{background:linear-gradient(180deg,#fff,var(--bg));padding-block:clamp(2rem,5vw,3.6rem);
  border-bottom:1px solid var(--line)}
.page-hero .lead{max-width:70ch}
.crumbs{background:#fff;border-bottom:1px solid var(--line)}
.crumbs ol{display:flex;flex-wrap:wrap;gap:.4rem;padding-block:.7rem;font-size:.88rem;color:var(--muted)}
.crumbs li::after{content:"‹";margin-inline-start:.4rem;color:var(--line)}
.crumbs li:last-child::after{content:""}
.crumbs a{color:var(--muted)}
.crumbs li[aria-current]{color:var(--primary-d);font-weight:700}

/* service cards */
.svc{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:1.6rem;
  box-shadow:var(--shadow-sm);display:flex;flex-direction:column}
.svc__head{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem}
.chip{background:var(--primary-l);color:var(--primary-d);font-weight:700;font-size:.82rem;
  padding:.3rem .7rem;border-radius:999px}
.chip--sm{font-size:.74rem;padding:.2rem .6rem;display:inline-block}
.sku{font-size:.74rem;color:var(--muted);font-family:ui-monospace,monospace;direction:ltr}
.svc__desc{color:var(--ink-2)}
.svc__block h4,.svc__cols h4{font-size:.92rem;color:var(--primary-d);margin:.6rem 0 .5rem;
  text-transform:uppercase;letter-spacing:.03em}
.svc__cols{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:.4rem 0}
.svc__price{background:var(--accent);color:#3a2600;font-weight:700;border-radius:var(--r-sm);
  padding:.7rem .9rem;display:flex;gap:.5rem;align-items:flex-start;font-size:.88rem}
.svc__price .ic{color:#3a2600}
.svc__note{font-size:.82rem;color:var(--muted)}
.svc__cta{display:flex;flex-direction:column;gap:.5rem;margin-top:auto;padding-top:.6rem}
/* package extras */
.svc__tags{display:flex;gap:.4rem;align-items:center}
.svc__badge{background:var(--accent);color:#3a2600;font-weight:800;font-size:.72rem;
  padding:.22rem .6rem;border-radius:999px}
.svc__priceline{display:flex;align-items:baseline;gap:.35rem;margin:.4rem 0 .2rem}
.svc__amount{font-size:1.9rem;font-weight:800;color:var(--primary-d);line-height:1;direction:ltr}
.svc__cur{font-weight:700;color:var(--muted);font-size:1rem}
.svc__meta{display:flex;gap:.4rem;align-items:center;color:var(--muted);font-size:.85rem;margin:.1rem 0 .4rem}
.svc__meta .ic{color:var(--primary);width:1.1em;height:1.1em}
.pkg-group+.pkg-group{padding-top:0}
.pkg-single{max-width:560px;margin-inline:auto}

/* numbered list */
.numlist{counter-reset:n;display:grid;gap:.8rem;max-width:860px;margin-inline:auto}
.numlist li{display:flex;gap:.8rem;background:#fff;border:1px solid var(--line);
  border-radius:var(--r-sm);padding:1rem 1.2rem;align-items:flex-start}
.numlist .num{flex:none;width:30px;height:30px;border-radius:8px;background:var(--primary-l);
  color:var(--primary-d);font-weight:800;display:flex;align-items:center;justify-content:center;font-size:.9rem}
.callout{display:flex;gap:.8rem;background:#07323a;color:#d8ecee;border-radius:var(--r);
  padding:1.3rem 1.4rem;margin-top:1.6rem;align-items:flex-start}
.callout .ic{color:var(--accent);flex:none;margin-top:.15rem;width:1.6em;height:1.6em}
.callout p{margin:0;font-size:.95rem}
.callout b{color:#fff}

/* states */
.states{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;direction:ltr}
.states li{background:#fff;border:1px solid var(--line);border-radius:999px;padding:.45rem 1rem;
  font-family:ui-monospace,monospace;font-size:.82rem;color:var(--ink-2);position:relative}
.states li:not(:last-child)::after{content:"→";margin-inline-start:.6rem;color:var(--primary)}

/* prose */
.prose-card{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:1.6rem;
  box-shadow:var(--shadow-sm)}
.prose p{font-size:1.05rem;color:var(--ink-2)}
.spec{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);
  border-radius:var(--r);overflow:hidden;margin:1.4rem 0}
.spec th,.spec td{padding:.9rem 1rem;text-align:start;border-bottom:1px solid var(--line);vertical-align:top}
.spec th{background:var(--primary-l);color:var(--primary-d);width:42%;font-weight:700}
.spec tr:last-child th,.spec tr:last-child td{border-bottom:0}

/* posts / features */
.post{background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;
  box-shadow:var(--shadow-sm);display:flex;flex-direction:column}
.post__img{position:relative;aspect-ratio:820/460;overflow:hidden}
.post__img img{width:100%;height:100%;object-fit:cover}
.post__img .chip--sm{position:absolute;inset-inline-start:12px;top:12px;background:rgba(7,35,42,.82);
  color:#fff;backdrop-filter:blur(4px)}
.post__body{padding:1.3rem 1.4rem;display:flex;flex-direction:column;gap:.5rem}
.post h3{margin:.2rem 0;font-size:1.1rem}
.post__meta{font-size:.8rem;color:var(--muted);display:flex;gap:.4rem;align-items:center;margin:0}
.feature{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:1.5rem;
  box-shadow:var(--shadow-sm)}
.feature .ic{color:var(--primary);width:1.9em;height:1.9em;margin-bottom:.5rem}

/* forms */
.formcard{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:1.7rem;
  box-shadow:var(--shadow-sm)}
.formcard h2{display:flex;align-items:center;gap:.5rem;font-size:1.3rem}
.formcard h2 .ic{color:var(--primary)}
.form{display:flex;flex-direction:column;gap:.9rem}
.form label{display:flex;flex-direction:column;gap:.35rem;font-weight:600;font-size:.95rem}
.form input,.form select,.form textarea{font-family:inherit;font-size:1rem;padding:.7rem .85rem;
  border:1.5px solid var(--line);border-radius:var(--r-sm);background:#fff;color:var(--ink);font-weight:500}
.form input:focus,.form select:focus,.form textarea:focus{border-color:var(--primary);outline:none;
  box-shadow:0 0 0 3px var(--primary-l)}
.form__row{display:grid;grid-template-columns:1fr 1fr;gap:.9rem}
.check{flex-direction:row!important;align-items:flex-start;gap:.55rem;font-weight:500}
.check input{width:20px;height:20px;margin-top:.15rem}
.order-summary{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;background:var(--primary-l);
  border:1px solid #cfe0e2;border-radius:var(--r-sm);padding:.8rem 1rem;margin-bottom:1rem}
.order-summary__label{color:var(--muted);font-size:.85rem}
.order-summary strong{color:var(--primary-d);font-size:1.02rem}

/* contact */
.contact-info{display:flex;flex-direction:column;gap:.8rem}
.contact-tile{display:flex;gap:.9rem;align-items:center;background:#fff;border:1px solid var(--line);
  border-radius:var(--r);padding:1.1rem 1.3rem;color:var(--ink)}
.contact-tile:hover{text-decoration:none;border-color:var(--primary)}
.contact-tile .ic{color:var(--primary);width:1.8em;height:1.8em}
.contact-tile b{display:block}.contact-tile span{color:var(--muted);direction:ltr;unicode-bidi:plaintext}

/* legal */
.legal__updated{display:inline-flex;gap:.4rem;align-items:center;color:var(--muted);font-size:.88rem;
  background:#fff;border:1px solid var(--line);padding:.4rem .9rem;border-radius:999px}
.legal__sec{margin:1.6rem 0}
.legal__sec h2{font-size:1.3rem}
.legal p,.legal li{color:var(--ink-2)}

/* accordion */
.acc{background:#fff;border:1px solid var(--line);border-radius:var(--r-sm);margin-bottom:.7rem;overflow:hidden}
.acc__btn{width:100%;display:flex;justify-content:space-between;align-items:center;gap:1rem;
  background:none;border:0;padding:1.1rem 1.3rem;font-family:inherit;font-size:1.05rem;font-weight:700;
  color:var(--ink);cursor:pointer;text-align:start}
.acc__btn:hover{background:var(--primary-l)}
.acc__ic{font-size:1.5rem;color:var(--primary);flex:none;line-height:1}
.acc__btn[aria-expanded="true"]{color:var(--primary-d)}
.acc__panel{padding:0 1.3rem 1.2rem}
.acc__panel p{margin:0;color:var(--ink-2)}

/* footer */
.site-foot{background:#07232a;color:#b9d0d3;padding-top:3rem}
.site-foot__grid{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:2rem;padding-bottom:2rem}
.site-foot__brand p{font-size:.92rem;color:#9fbabd;max-width:40ch}
.site-foot__entity{font-size:.82rem;color:#7f9ca0}
.site-foot__col h3{color:#fff;font-size:1rem;margin-bottom:1rem}
.site-foot__col a{color:#b9d0d3;font-size:.92rem;display:block;padding:.3rem 0}
.site-foot__col a:hover{color:#fff}
.site-foot__note{border-top:1px solid rgba(255,255,255,.12);padding-top:1.3rem}
.site-foot__note p{font-size:.78rem;color:#88a4a8;margin:0}
.site-foot__bottom{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;
  padding-block:1.3rem;border-top:1px solid rgba(255,255,255,.12);margin-top:1.3rem;
  font-size:.82rem;color:#88a4a8}
.site-foot__bottom p{margin:0}

/* ===== premium polish ===== */
/* top utility bar */
.topbar{background:var(--ink);color:#c7d6da;font-size:.82rem}
.topbar__row{display:flex;align-items:center;justify-content:space-between;gap:1rem;
  min-height:40px;flex-wrap:wrap}
.topbar__contacts{display:flex;align-items:center;gap:1.2rem;flex-wrap:wrap}
.topbar__contacts a,.topbar__hours{display:inline-flex;align-items:center;gap:.4rem;color:#c7d6da}
.topbar__contacts a:hover{color:#fff;text-decoration:none}
.topbar__contacts .ic{color:var(--accent);width:1.05em;height:1.05em}
.topbar__note{display:inline-flex;align-items:center;gap:.4rem;color:#9fbabd}
.topbar__note .ic{color:var(--accent);width:1.05em;height:1.05em}

/* refined heading kicker */
.kicker{display:inline-block;color:var(--accent-d);font-weight:800;font-size:.8rem;
  letter-spacing:.14em;text-transform:uppercase;margin-bottom:.6rem}
.section__head .kicker::before{content:"";display:inline-block;width:22px;height:2px;
  background:var(--accent);vertical-align:middle;margin-inline-end:.5rem}
.section__head .kicker::after{content:"";display:inline-block;width:22px;height:2px;
  background:var(--accent);vertical-align:middle;margin-inline-start:.5rem}

/* refined header + primary button */
.site-head.is-scrolled{box-shadow:0 6px 24px rgba(11,31,42,.08)}
.btn--primary{background:linear-gradient(180deg,var(--primary),var(--primary-d));
  box-shadow:0 6px 16px rgba(14,110,125,.28)}
.btn--primary:hover{box-shadow:0 10px 22px rgba(14,110,125,.34)}
.hero{position:relative}
.hero::before{content:"";position:absolute;inset:0;pointer-events:none;
  background-image:radial-gradient(rgba(14,110,125,.07) 1px,transparent 1px);
  background-size:22px 22px;mask-image:linear-gradient(180deg,#000,transparent 70%)}
.hero__inner{position:relative}

/* trust strip under hero */
.trust-strip{background:#fff;border-bottom:1px solid var(--line)}
.trust-strip ul{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--line)}
.trust-strip li{display:flex;gap:.7rem;align-items:center;background:#fff;padding:1.1rem 1.2rem}
.trust-strip .ic{color:var(--primary);width:1.7em;height:1.7em;flex:none}
.trust-strip b{display:block;font-size:.98rem}
.trust-strip span{color:var(--muted);font-size:.82rem}

/* value cards (why us) */
.grid--4{grid-template-columns:repeat(4,1fr)}
.value{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:1.6rem;
  box-shadow:var(--shadow-sm);transition:.2s;position:relative;overflow:hidden}
.value::before{content:"";position:absolute;inset-inline-start:0;top:0;width:100%;height:4px;
  background:linear-gradient(90deg,var(--primary),var(--accent));opacity:0;transition:.2s}
.value:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:#cfe0e2}
.value:hover::before{opacity:1}
.value__ic{display:inline-flex;align-items:center;justify-content:center;width:52px;height:52px;
  border-radius:14px;background:var(--primary-l);color:var(--primary-d);margin-bottom:1rem}
.value__ic .ic{width:1.6em;height:1.6em}
.value h3{font-size:1.1rem}
.value p{color:var(--muted);font-size:.95rem;margin:0}

/* footer trust ribbon */
.site-foot{padding-top:0}
.site-foot__ribbon{background:#061c22;border-bottom:1px solid rgba(255,255,255,.08)}
.site-foot__ribbon ul{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;padding-block:1.2rem}
.site-foot__ribbon li{display:flex;gap:.55rem;align-items:center;color:#aec6ca;font-size:.86rem;
  font-weight:600}
.site-foot__ribbon .ic{color:var(--accent);width:1.3em;height:1.3em;flex:none}
.site-foot__grid{padding-top:2.6rem}

/* responsive */
@media(max-width:960px){
  .nav,.site-head__cta{display:none}
  .nav-toggle{display:inline-flex}
  .hero__inner{grid-template-columns:1fr;gap:1.8rem}
  .hero__media{order:-1;max-width:520px}
  .banner img{aspect-ratio:16/9}
  .grid--3,.grid--4{grid-template-columns:repeat(2,1fr)}
  .steps,.steps--lg{grid-template-columns:repeat(2,1fr)}
  .site-foot__grid,.site-foot__ribbon ul{grid-template-columns:1fr 1fr}
  .trust-strip ul{grid-template-columns:repeat(2,1fr)}
  .topbar__note{display:none}
}
@media(max-width:640px){
  body{font-size:16px}
  .grid--2,.grid--3,.grid--4,.steps,.steps--lg,.svc__cols,.form__row{grid-template-columns:1fr}
  .cta__inner{flex-direction:column;align-items:flex-start}
  .site-foot__grid,.site-foot__ribbon ul{grid-template-columns:1fr}
  .trust-strip ul{grid-template-columns:1fr 1fr}
  .site-foot__bottom{flex-direction:column;gap:.3rem}
  .topbar__hours{display:none}
  .topbar__row{justify-content:center}
  .hero__frame{overflow:visible;box-shadow:none}
  .hero__bg{border-radius:16px;box-shadow:var(--shadow-sm)}
  .hero__overlay{display:none}
  .hero__content{position:static;width:auto;color:var(--ink);padding:1.3rem 0 0}
  .hero__content h1{color:var(--ink);text-shadow:none}
  .hero__content .lead{color:var(--ink-2);text-shadow:none}
  .eyebrow--light{background:var(--primary-l);color:var(--primary-d);border-color:transparent}
  .eyebrow--light .ic{color:var(--primary-d)}
  .hero--framed .hero__cta .btn{flex:1 1 auto}
}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto;transition:none!important}}
"""

JS = r"""// R7LE — interactions: mobile nav + FAQ accordion
(function () {
  "use strict";
  var toggle = document.querySelector(".nav-toggle");
  var mnav = document.getElementById("mobile-nav");
  if (toggle && mnav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      mnav.hidden = open;
    });
    mnav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        toggle.setAttribute("aria-expanded", "false");
        mnav.hidden = true;
      });
    });
  }
  var head = document.querySelector(".site-head");
  if (head) {
    var onScroll = function () {
      head.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
  document.querySelectorAll(".acc__btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      btn.setAttribute("aria-expanded", String(!open));
      if (panel) panel.hidden = open;
      var icn = btn.querySelector(".acc__ic");
      if (icn) icn.textContent = open ? "+" : "–";
    });
  });

  // Prefill the order summary from ?dest=&pkg= (auto destination, no login)
  var box = document.getElementById("order-summary");
  if (box) {
    var params = new URLSearchParams(location.search);
    var dest = params.get("dest");
    var pkg = params.get("pkg");
    if (dest || pkg) {
      var pkgEl = document.getElementById("order-pkg");
      var destEl = document.getElementById("order-dest");
      if (pkgEl) pkgEl.textContent = pkg || "باقة";
      if (destEl) { if (dest) destEl.textContent = dest; else destEl.hidden = true; }
      var di = document.getElementById("order-dest-input");
      var pi = document.getElementById("order-pkg-input");
      if (di) di.value = dest || "";
      if (pi) pi.value = pkg || "";
      box.hidden = false;
    }
  }
})();
"""


def main():
    write_assets()
    build_home()
    build_usa()
    build_canada()
    build_australia()
    build_services()
    build_howitworks()
    build_faq()
    build_blog()
    build_client()
    build_aboutus()
    build_contact()
    build_legal()
    build_404()
    write_seo()
    print("Build complete.")


if __name__ == "__main__":
    main()
