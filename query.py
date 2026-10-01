"""Task 3: Grounded scheme verification & dialect tuning.

Converts ambiguous, colloquial rural speech into high-precision government-portal
search queries, detects the interaction language, and scores source URLs so the
LLM prompt and the UI can prefer official .gov.in evidence over SEO spam.
"""

import re
from typing import Dict, List, Tuple
from urllib.parse import urlparse

SCHEME_HINTS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    (
        "Pradhan Mantri Matru Vandana Yojana PMMVY maternity benefit",
        (
            "pregnan", "pregnant", "கர்ப்ப", "கர்ப்பிண", "गर्भवती", "prasoot", "san Gestan",
            "baby", "குழந்தை", "shishu", "maternity", "matru", "maa", "delivery", "expecting",
            "months pregnant", "anc", "hospital", "delivery benefit",
            # bn / as / gu / kn / ml / pa / or / te / ur
            "গর্ভবতী", "প্রসূতি", "সন্তান", "গর্ৱপত", "গৰ্ভৱতী", "গৰোদৰ",
            "ગર્ભવતિ", "સન્તાન", "ಗರ್ಭವತಿ", "ഗർഭവതിയായി", "സന്താനം",
            "ਗਰਭਵਤੀ", "ਸੁਖੀ", "ଗର୍ଭବତୀ", "ଶିଶୁ", "అంగరేషి", "పుత్తురు",
        ),
    ),
    (
        "Lakhpati Didi scheme women self help group SHG loan interest subvention",
        (
            "silai", "sewing", "tailor", "வணிகம்", "தையல்", "व्यवसाय", "dudh", "dairy",
            "poultry", "k poultry", "business", "loan", "கடன்", "ஆதாரம்", "self help",
            "shg", "group", "மேல்நிலை", "income", "வருமானம்", "silk", "mudi", "small business",
            "shop", "venture", "enterprise", "start my", "income support",
            "সেলাই", "ব্যবসা", "স্বনির্ভর", "સીલાઈ", "વ્યવસાય", "ಸಿಲೈ", "ವ್ಯಾಪಾರ",
            "തുട്ട", "സംഘടന", "ਸਿਲਾਈ", "ਕਾਰੋਬਾਰ", "ସେଲାଇ", "ବ୍ୟବସାୟ", "అలవైని",
            "گیس", "کاروبار", "dudh", "పాల", "میں نے",
        ),
    ),
    (
        "PM Ujjwala Yojana LPG connection subsidy",
        (
            "gas", "indane", "lpg", "பாரிவா", "இலங்கை", "cylinder", "சிலிண்டர்", "रसोई",
            "cooking gas", "ගල් ඉන්දන්", "गैस", "ગેસ", "ಅನ್ಯ ವಾಟ", "വാതക", "ਗੈਸ",
            "ଗ୍ୟାସ", "ਗੈਸ", "సిలిండర్",
        ),
    ),
    (
        "PM Mudra Yojana women enterprise loan",
        ("mudra", "முதுரா", "मुद्रा", "micro loan", "microlone", "micro loan"),
    ),
    (
        "National Scholarship Portal post matric scholarship girls",
        (
            "scholarship", "10th", "12th", "பள்ளி", "கல்வி", "विद्या", "education", "padachanam",
            "படிப்பு", "studies", "study", "further studies", "higher education", "college", "பால்கல்வி",
            "girl", "passed 10th", "board exam",
            "పড়াশোনা", "স্কলারশিপ", "মেয়ে", "দশম", "વિદ્યા", "દસમી", "શિક્ષણ",
            "ವಿದ್ಯಾರ್ಥಿ", "ಹತ್ತನ", "ತರಗತಿ", "ಶಿಕ್ಷಣ", "ಮಗು", "ಪಠನ",
            "പഠനം", "മകൾ", "പത്താം", "ക്ലാസ്", "സഹായം",
            "ਧੰਨ", "ਬੇਟੀ", "ਪੜ੍ਹਾਈ", "ਕਲਾਸ", "ਮਦਦ",
            "ପଠନ", "ଝିଅ", "ଦଶମ", "ସାହାଯ୍ୟ", "କଲାସ",
            "పదో", "తరగతి", "కూతురు", "సహాయం", "బెట్టి", "విద్య",
            "दसवीं", "पढ़ाई", "दशम", "बेटी", "विद्या", "पढ़ना",
            "मुलीला", "दहाड्या", "परीक्षा", "शाला", "अभ्यास", "पुढे", "आगे", "मिळेल",
        ),
    ),
    (
        "Pradhan Mantri Fasal Bima Yojana Kisan welfare and Kisan Credit Card",
        (
            "farmer", "விவசாய", "किसान", "crop", "பயிர்", "Fasal", "Fasal Bima",
            "kethi", "krishi", "chasha", "sethi", "zameen", "ಕೃಷಿ", "കാര്ഷിക", "ਖੇਤੀ",
        ),
    ),
    (
        "Sukanya Samriddhi Yojana girl child savings",
        (
            "daughter", "மகள்", "बेटी", "girl child", "savings", "சேமிப்பு", "बालिका",
            "putri", "ghonghor", "gongor", "মেয়ে", "દીકરી", "ಮಗು", "മകൾ", "ਬੇਟੀ",
            "ଝିଅ", "కూతురు",
        ),
    ),
)

SPOKEN_FILLER = re.compile(
    r"\b(please|kindly|maa|akka|didi|amma|appa|naan|na|aku|me|naaku|meri|enakku|evuru|"
    r"i want|i need|can i|do i|will government|a government|plz|sister|akhya|indru|vandi|"
    r"amaru|unga|kannu|konjam|naal|naalai|ke liye|liye|meri|merA|maja|magalu|vachitam|"
    r"mi|meko|maarte|maja|m\'aa|m\'e|mue|savad|sakhi|akka|akka)\b",
    re.I,
)

# Word-ish characters: Latin plus every Indic/Arabic block we support.
WORD_CHARS = (
    r"\w\s\u0600-\u06FF\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F\u0A80-\u0AFF"
    r"\u0B00-\u0B7F\u0B80-\u0BFF\u0C00-\u0CFF\u0D00-\u0D7F"
)

# Unicode script blocks: (low, high) -> language code
SCRIPT_RANGES: Dict[str, Tuple[str, str]] = {
    "ta": ("\u0b80", "\u0bff"),
    "te": ("\u0c00", "\u0c7f"),
    "hi": ("\u0900", "\u097f"),
}

ROMAN_HINTS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    (
        "en",
        (
            "government", "scheme", "apply", "benefit", "please", "daughter", "study", "studies",
            "school", "money", "loan", "gas", "preg", "help", "card", "bank", "job", "work",
            "i want", "i need", "can i", "give me", "myself", "her", "wife",
        ),
    ),
    (
        "hi",
        (
            "sarkar", "paisa", "kaise", "kaisay", "bharat", "yoga", "didi", "gaon", "khet",
            "padhai", "sarkari", "kya", "mujhe", "hai", "nahi", "didi", "bahu", "chahiye",
        ),
    ),
    (
        "ta",
        (
            "angadi", "panchayat", "anangal", "thuna", "katchi", "theertha", "selvam", "thittu",
            "naal", "akka", "naan", "unga", "eppo", "konjam", "vachi", "padichu",
        ),
    ),
    (
        "te",
        (
            "grameen", "panchayati", "yuddham", "arogyam", "didi", "nistyam", "akka", "meekata",
            "kavali", "undhi", "kada", "cheppaledi", "sari",
        ),
    ),
)

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
}

OFFICIAL_SUFFIXES = (".gov.in", ".nic.in", ".nhs.net", ".rbi.org.in", ".india.gov.in")
BLOCKED_TOKENS = (
    "loanbazaar",
    "bajaj",
    "advertisement",
    "affiliate",
    "creditcard",
    "mutualfund",
    "policybazaar",
    "bankoffer",
    "chitfund",
    "aggregator",
)


def detect_language(text: str) -> str:
    """Return an English language name; auto-detects script first, then romanised hints."""
    found = []
    for name, (low, high) in SCRIPT_RANGES.items():
        if any(low <= ch <= high for ch in text):
            found.append(name)

    if found:
        return LANGUAGE_NAMES[found[0]]

    lowered = f" {text.lower()} "
    best: Tuple[int, str] = (0, "en")
    for code, hints in ROMAN_HINTS:
        score = sum(1 for hint in hints if hint in lowered)
        if score > best[0]:
            best = (score, code)
    return LANGUAGE_NAMES[best[1]]


def official_url_score(url: str) -> int:
    """1 = official government domain, 0 = third party / blocked."""
    if not url:
        return 0
    host = (urlparse(url).hostname or url).lower()
    if any(token in host for token in BLOCKED_TOKENS):
        return 0
    if any(host.endswith(suffix) for suffix in OFFICIAL_SUFFIXES):
        return 1
    return 0


def filter_sources(sources: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Keep official sources first; third-party sources are demoted, never silently dropped."""
    official = [s for s in sources if official_url_score(s.get("url", "")) == 1]
    other = [s for s in sources if official_url_score(s.get("url", "")) == 0]
    return official + other


def _clean(text: str) -> str:
    cleaned = SPOKEN_FILLER.sub(" ", text or "")
    cleaned = re.sub(r"[^" + WORD_CHARS + r"]+", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def build_search_query(user_raw_speech: str, language: str) -> str:
    """Turn a loose spoken sentence into a precise government-portal search string."""
    raw = (user_raw_speech or "").strip()
    lowered = raw.lower()
    cleaned = _clean(raw)

    matched: List[str] = []
    for hint, keywords in SCHEME_HINTS:
        if any(keyword in lowered for keyword in keywords):
            matched.append(hint)
    if not matched:
        matched = [f"government welfare scheme for women {cleaned}"]

    state = "India"
    if any(token in lowered for token in ("tamil", "தமிழ்", "தமிழக", "தமில்நாடு", "chennai", "coimbatore", "madurai")):
        state = "Tamil Nadu"
    elif any(token in lowered for token in ("andhra", "తెలంగాణ", "telangana", "hyd", "vijayawada")):
        state = "Telangana"
    elif any(token in lowered for token in ("karnataka", "ಕರ್ನಾಟ", "bengaluru", "bangalore", "mysore")):
        state = "Karnataka"
    elif any(token in lowered for token in ("maharashtra", "महाराष्ट्र", "महाराष्ट्र", "pune", "mumbai")):
        state = "Maharashtra"
    elif any(token in lowered for token in ("kerala", "കേരള", "kochi", "thiruvananthapuram")):
        state = "Kerala"
    elif any(token in lowered for token in ("west bengal", "পশ্চিমবঙ্গ", "bengal", "kolkata")):
        state = "West Bengal"
    elif any(token in lowered for token in ("gujarat", "ગુજરાત", "ahmedabad", "surat")):
        state = "Gujarat"
    elif any(token in lowered for token in ("punjab", "ਪੰਜਾਬ", "ਪੰਜਾਬ", "ludhiana", "amritsar")):
        state = "Punjab"
    elif any(token in lowered for token in ("odisha", "ଓଡ଼ିଶା", "ଓଡ଼ିଆ", "orissa", "bhubaneswar", "cuttack")):
        state = "Odisha"
    elif any(token in lowered for token in ("assam", "অসম", "অসমীয়া", "guwahati", "ডিব্ৰুগড়")):
        state = "Assam"
    elif any(token in lowered for token in ("uttar pradesh", "उत्तर प्रदेश", "UP ", "varanasi", "lucknow")):
        state = "Uttar Pradesh"
    elif any(token in lowered for token in ("rajasthan", "राजस्थान", "jaipur")):
        state = "Rajasthan"
    elif any(token in lowered for token in ("madhya pradesh", "मध्य प्रदेश", "bhopal", "indore")):
        state = "Madhya Pradesh"

    primary = matched[0]
    parts = [primary, "eligibility", f"{state}"]
    parts.extend(matched[1:2])
    parts.extend(["benefit amount", "required documents", "myscheme.gov.in"])
    return " ".join(p for p in parts if p).strip()


if __name__ == "__main__":  # manual smoke test
    import sys

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

    cases = [
        "I am 5 months pregnant, will government give money?",
        "நான் ஐந்து மாத கர்ப்பிணி, மருத்துவமனைக்கு அரசு பணம் தருமா?",
        "I want loan to start tailoring shop",
        "मेरी बेटी 10th पास है, आगे की पढ़ाई के लिए सरकारी मदद मिलेगी?",
        "mujhe silai ka kaam shuru karna hai, koi sarkari madad milegi?",
        "My daughter finished 10th grade, is there government help for her further studies?",
        "I need money for my small tailoring shop in Tamil Nadu",
        "gas cylinder kahan se milega",
        "আমার মেয়ে দশম শ্রেণী পাশ করেছে, সরকারি সাহায্য আছে?",
        "माझ्या मुलीला दहाड्या पाश झाली आहे, सरकारी मदत मिळेल का?",
        "ਮੇਰੀ ਬੇਟੀ ਦਸਵੀਂ ਪਾਸ ਹੈ, ਸਰਕਾਰੀ ਮਦਦ ਮਿਲੇਗੀ?",
        "আমি গর্ভবতী, সরকারি টাকা দেবে?",
        "ನನ್ನ ಮಗು ಹತ್ತನ ತರಗತಿ ಮುಗಿಸಿದ್ದಾ, ಸರ್ಕಾರಿ ಸಹಾಯ ಇದೆ?",
        "എന്റെ മകളുണ്ട് പത്താം ക്ലാസ് കഴിഞ്ഞു, സർക്കാർ സഹായം ലഭിക്കുമോ?",
        "મારી દીકરી દસમી પાસ થઈ છે, સરકારી મદદ મળશે?",
        "ମୋ ଝିଅ ଦଶମ ପାସ କରିଛି, ସରକାରୀ ସାହାଯ୍ୟ ମିଳିବ?",
        "ਮੇਰੀ ਬੇਟੀ ਦਸਵੀਂ ਪਾਸ ਹੈ, ਸਰਕਾਰੀ ਮਦਦ ਮਿਲੇਗੀ?",
        "మా కూతురు పదో తరగతి పూర్తి చేసింది, ప్రభుత్వ సహాయం ఉందా?",
        "मेरी बेटी दसवीं पास है, सरकारी मदद मिलेगी?",
        "मेरा बेटी दसवीं पास बा, सरकारी मदद मिली?",
    ]
    for case in cases:
        lang = detect_language(case)
        print(f"[{lang}] {case}\n  -> {build_search_query(case, lang)}\n")
