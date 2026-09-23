import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
readme_path = os.path.join(repo_root, 'README.md')

with open(readme_path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\r\n', '\n')

# 1. Russian Credits Section
credits_ru = """### 13. 🤝 Благодарности (Credits) (RU)

Выражаем искреннюю благодарность разработчикам и исследователям сообщества, чей труд, экспертиза и открытые наработки внесли ключевой вклад в создание и совершенствование комбайна:

* 🌟 **ItzDFPlayer** — за фундаментальные исследования структуры системных оверлеев камеры, реверс-инжиниринг XML-манифестов `device_features` и модификаций приложений камеры MIUI / HyperOS.
* 🌟 **HolyBear** — за разработку и оптимизацию продвинутых профилей обработки изображений, устранение артефактов и глубокий анализ библиотек постобработки.
* 🌟 **amitkattal** — за выдающийся вклад в разблокировку полного разрешения 50Мп / 200Мп Ultra RAW, реверс-инжиниринг драйверов Qualcomm CamX и тонкую настройку калибровок сенсоров.
* 🌟 **GeorgeKiarie** — за создание легендарного алгоритмического мода **George Video MOD** (разблокировка записи видео в разрешении 8K со всех оптических модулей, 4K120fps и байпас агрессивного шумоподавления ArcSoft).

---

"""

# 2. English Credits Section
credits_en = """### 13. 🤝 Credits & Acknowledgements (EN)

We express our heartfelt appreciation and gratitude to the outstanding community developers and researchers whose dedication, expertise, and open research made this project possible:

* 🌟 **ItzDFPlayer** — for foundational architectural research into camera systemless overlays, `device_features` manifest structuring, and MIUI / HyperOS camera package modifications.
* 🌟 **HolyBear** — for pioneering custom image processing profiles, artifact mitigation algorithms, and in-depth analysis of processing pipelines.
* 🌟 **amitkattal** — for groundbreaking work on unlocking 50MP / 200MP full-resolution Ultra RAW capture, Qualcomm CamX driver reverse engineering, and sensor tuning.
* 🌟 **GeorgeKiarie** — for the legendary **George Video MOD** algorithms (unlocking 8K recording across all camera lenses, 4K120fps high-frame-rate capture, and bypassing ArcSoft video noise reduction smearing).

---

"""

# Update RU Navigation
nav_item_ru = '12. [Сообщество, обратная связь и Telegram](#12-сообщество-обратная-связь-и-telegram-ru)'
new_nav_item_ru = nav_item_ru + '\n13. [Благодарности (Credits)](#13-благодарности-credits-ru)'
if nav_item_ru in text:
    text = text.replace(nav_item_ru, new_nav_item_ru, 1)
    print("[OK] RU Navigation updated with Credits")

# Update EN Navigation
nav_item_en = '12. [Community, Feedback & Telegram Channel](#12-community-feedback--telegram-channel-en)'
new_nav_item_en = nav_item_en + '\n13. [Credits & Acknowledgements](#13-credits--acknowledgements-en)'
if nav_item_en in text:
    text = text.replace(nav_item_en, new_nav_item_en, 1)
    print("[OK] EN Navigation updated with Credits")

# Insert RU Credits before English section header
en_header_marker = '<a name="-english"></a>'
if en_header_marker in text:
    text = text.replace(en_header_marker, credits_ru + en_header_marker, 1)
    print("[OK] RU Credits section inserted before English section")
else:
    print("[FAIL] en_header_marker not found")

# Insert EN Credits at the end of the file
text = text.rstrip() + "\n\n" + credits_en
print("[OK] EN Credits section appended at the end")

# Clean any residual author strings in tables / headers
text = text.replace("borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)", "borndead")
text = text.replace("borndead (feat. amitkattal & GeorgeKiarie)", "borndead")
text = text.replace("borndead (feat. itzdfplayer & GeorgeKiarie)", "borndead")
text = text.replace("borndead (feat. Qualcomm CamX & Xiaomi AISP Team)", "borndead")

with open(readme_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print("\n=== README.md UPDATED WITH CREDITS & ACKNOWLEDGEMENTS ===")
