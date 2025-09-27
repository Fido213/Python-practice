from playwright.sync_api import sync_playwright, TimeoutError
import requests
from bs4 import BeautifulSoup
import time
import json

# event id = submit
# submit = confirm


def detect_login_security(page):
    """ run 7 security checks as to know what the scrapper is dealing with
      and print the results"""

    print("\n=== Security Feature Checks ===")

    # 1. SSO Redirect
    if "cas" in page.url or "saml" in page.url or "openid" in page.url:
        print("🔐 SSO redirect in use (CAS/SAML/OpenID)")
    else:
        print("✅ No external SSO detected in final URL")

    # 2. Hidden Tokens
    hidden_inputs = page.query_selector_all("input[type='hidden']")
    hidden_names = [i.get_attribute("name") for i in hidden_inputs]
    if any("execution" in (name or "") for name in hidden_names):
        print("✅ CAS execution token found")
    else:
        print("⚠️ No CAS execution token found")

    # 3. PIN prompt (PRONOTE)
    if page.query_selector("input[type=password][maxlength='4']"):
        print("🔐 PIN code required (2FA)")
    else:
        print("✅ No PIN required")

    # 4. CAPTCHA
    if (
        page.query_selector("iframe[src*='recaptcha']")
        or "captcha" in page.content().lower()
    ):
        print("⚠️ CAPTCHA present")
    else:
        print("✅ No CAPTCHA detected")

    # 5. Device registration
    if "appareil de confiance" in page.content().lower():
        print("📱 Device registration prompt detected")
    else:
        print("✅ No device registration prompt")

    # 6. Login result
    content = page.content().lower()
    if "sg.do" in page.url:
        print("✅ Logged in successfully (redirected to dashboard)")
    elif "erreur" in content or "incorrect" in content:
        print("❌ Login failed (credentials or block)")
    else:
        print("⚠️ Unknown login state")

    # 7. Session cookies
    cookies = page.context.cookies()
    if any(c["name"].startswith("JSESSIONID") for c in cookies):
        print("✅ Active session cookie present")
    else:
        print("⚠️ No session cookie found")


with sync_playwright() as p:
    noteslist = []  # list to store notes
    browser = p.chromium.launch(headless=False)
    # assign launching a chrome browser (not headless so gui) to browser
    context = browser.new_context()
    # incognito context for new session
    page = context.new_page()
    # new page in the incognito context
    # what we just did is:
    # A: Launch a chrome browser with a gui
    # B: Create an incognito session in that browser
    # C: Open a new tab "page" in that incognito session
    # Go to login page via skolengo url
    page.goto(
        "https://cas1.skolengo.com/login?service=https%3A%2F%2Flfc.skolengo.com%2Fsg.do%3FPROC%3DIDENTIFICATION_FRONT"
    )
    # wait for the form fields to be present as to avoid typing too early
    page.wait_for_selector("input#username", timeout=5000)
    page.wait_for_selector("input#password", timeout=5000)
    # Use fill which triggers the usual events, fill is also faster than type
    page.fill("input#username", "farid.el_achkar")
    page.fill("input#password", "Fortnite@2020_2021")
    # make sure submit is ready and click, then wait for redirect
    page.press("input#password", "Enter")
    try:
        page.wait_for_url("**/sg.do*", timeout=10000)
        page.wait_for_load_state("networkidle")
        # these 2 lines basically means "wait until fully loaded or timeout
        # after 10s"
        # this is to avoid running detection checks too early and getting
        # false negatives
        # aswell as avoiding cascading errors due to this
        # this also allows gracefull exits and flagging of timeout issues
    except TimeoutError:
        print("⚠️ Redirect to dashboard did not occur within timeout")
    # Run detection checks
    detect_login_security(page)
    page.goto("https://3010002s.index-education.net/pronote/")
    page.click('#GInterface\\.Instances\\[0\\]\\.Instances\\[1\\]_Combo2:has-text("Notes")')
    time.sleep(1)  # wait for the dropdown to open
    page.click('div.label-submenu:has-text("Mes notes")')
# now that we launched the browser and are logged in, we now need to scrape
# the html info
# since the html info is provided by the js, we use beautiful soup alongside
# playwright
# since playwright simulatees an actual browser and hence received the fully
# rendered html
# and scrape it from there, with beautiful soup in lxml mode for speedy parsing
# and beautiful soups ease of use.
    time.sleep(2)  # wait for the notes page to load
    note_items = page.locator("div.liste-cellule-focusable")  # all notes
    count = note_items.count()  # how many notes are there
    print(count)  # debugging purposes
    # now that we have the amount of notes, we can run a loop:
    for note in range(count):
        note_items.nth(note).click()  # .nth to select the note and click
        # basically, when we do this line "page.locator" it returns a list
        # of all the elements in that page that matches
        # so .nth basically iterates through our list of notes, and since
        # its index base, we can just use the loop variable and do .click
        # to click on each note
        time.sleep(2)  # wait for the note to load
        html = page.inner_html('section#GInterface\\.Instances\\[2\\]_detail')
        # get the html of the note details section using inner_html, so that we
        # can parse it with beautiful soup
        soup = BeautifulSoup(html, "lxml")
        # parse the html with beautiful soup in lxml mode for speed
        title = soup.select_one("h2.ie-titre").get_text(strip=True)
        # gets title from html div
        date = soup.select_one("p.ie-texte").get_text(strip=True)
        # gets date from html div
        print(f"Title: {title}\nDate: {date}")  # debugging
        details = {
            dt.get_text(strip=True): dd.get_text(strip=True)
            for dt, dd in zip(soup.select("dt"), soup.select("dd"))
        }
        # this is a dictionary comprehension that creates a dictionary from
        # the dt and dd elements in the html
        noteslist.append(
            {
                "title": title,
                "date": date,
                "details": details,
            }
        )  # append the note to the list of notes in dictionary format
        time.sleep(1)  # wait a bit before going to the next note
    # after the loop is done, we can save the notes to a json file
        print(title)  # print the notes for debugging purposes
    with open("Project4webscraper/notes.json", "w", encoding="utf-8") as f:
        json.dump(noteslist, f, ensure_ascii=False, indent=4)
        # refer back to previous projects for json dump parameters
# great, now that we have a working notes scrapper, we can move on to
# assignments, for this we will need to, on the notes page, click the menu bar
# and then click on assignments, and then repeat the same process as above
# after that we can move onto the contenu du cours (course contents) sections
# which is in the same manu as assignments, so we should be able to just
# switch to that tab, now a pretty annoying problem is the way the assignments
# and course contents are loaded, they are rendered in a scrollable div
# with the course subject (eg, maths, french, etc) as clickable tabs on the
# left side, and the contents (be it assignments or course contents) on the
# right side, the annoying part being the fact that its loaded in a scrollable
# format, with a basic layout template of: date, subject, teacher, next to
# teacher
# hours, and then below that the actual content, which can be text, images,
# etc... Now our main hurdle is actually loading them all in a clean fashion
# aswell as handling images and scrolling
# we will use page.evaluate for the scrolling thingi
# after translating the html code from chatgpt to js, we can do:
    # first we go to the assignments page
    page.click('#GInterface\\.Instances\\[0\\]\\.Instances\\[1\\]_Combo1:has-text("Cahier")')
    time.sleep(1)  # wait for the dropdown to open
    page.click('div.label-submenu:has-text("Contenu et ressources")')
    time.sleep(1)  # wait for the assignments page to load
    # now we can run the js code to scrape the assignments
    # this js code is the same for course contents, so we can reuse it later
    class_content = page.evaluate("""() => {
    const days = [];
    document.querySelectorAll("ul.liste-date > li").forEach(dayLi => {
        const date = dayLi.querySelector("h2.ie-titre-gros")?.innerText.trim() || "";
        const tasks = [];

        dayLi.querySelectorAll("li[tabindex]").forEach(taskLi => {
        const item = taskLi.querySelector("div.conteneur-item");
        if (!item) return;

        const subject = item.querySelector(".entete-element .titre-matiere")?.innerText.trim() || "";
        const teacher = item.querySelector(".ie-sous-titre")?.innerText.trim() || "";
        const hours = item.querySelector(".ie-titre-petit")?.innerText.trim() || "";
        const title = item.querySelector(".conteneur-descriptif .titre-matiere")?.innerText.trim() || "";

        // ✅ Correct selector for descriptions
        const descContainer = item.querySelector("div.descriptif.tiny-view");
        let description = "";
        if (descContainer) {
            description = descContainer.innerText.trim();
        }

        tasks.push({ subject, teacher, hours, title, description });
        });

        if (date || tasks.length) days.push({ date, tasks });
    });
    return days;
    }""")
    # print(class_content)  # print the content for debugging purposes
    with open("Project4webscraper/assignments.json", "w", encoding="utf-8") as f:
        json.dump(class_content, f, ensure_ascii=False, indent=4)
        # save the assignments to a json file
    browser.close()  # close the browser when done
