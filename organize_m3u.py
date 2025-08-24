import re

# ==== CONFIG ====
input_file = "/Users/nickismithey/Downloads/us.m3u"
output_file = "/Users/nickismithey/Downloads/us_cleaned.m3u"

# ==== PREMIUM CHANNELS (full list with aliases) ====
premium_channels = [
    "FX", "AMC", "TNT", "NBC", "NBC HD", "Syfy", "Disney", "Disney Channel", "Disney XD",
    "Disney Junior", "Nickelodeon", "TeenNick", "ABC", "CBS", "CNN", "Fox News", "MSNBC",
    "BBC", "ESPN", "ESPN2", "HBO", "HBO HD", "Showtime", "Showtime HD", "Starz", "Starz HD",
    "Cinemax", "Cinemax HD", "Cartoon Network", "TBS", "USA Network", "Hallmark Channel",
    "Discovery Channel", "Nat Geo", "National Geographic", "History Channel", "FXM",
    "FX Movie Channel", "Freeform", "Lifetime", "PBS", "PBS Kids", "CNBC", "Bloomberg TV",
    "HGTV", "Food Network", "Travel Channel", "Animal Planet", "A&E", "Bravo", "E!", "Comedy Central",
    "Paramount Network"
]

# ==== LOW-QUALITY/NICHE KEYWORDS ====
low_quality_keywords = {
    "Shopping": ["shopping", "teleshopping", "home & garden", "QVC", "HSN"],
    "Infomercials": ["infomercial"],
    "Radio/Music": ["radio", "music"],
    "Hunting/Fishing": ["hunting", "fishing"],
    "Religious": ["religion", "faith", "church", "spiritual"],
    "Weather": ["weather"],
    "Obscure/Foreign": ["foreign", "regional"]
}

# ==== OTHER DECENT CATEGORIES ====
other_categories_keywords = {
    "Sports": ["Sports", "ESPN2", "Fox Sports", "NBC Sports", "CBS Sports", "Golf Channel", "NFL Network"],
    "Kids": ["Boomerang", "Cartoonito", "Nick Jr.", "Disney Junior", "PBS Kids"],
    "Local": ["Local", "ABC", "CBS", "NBC", "FOX", "MyNetworkTV"],
    "Entertainment": ["E!", "Bravo", "FXM", "TBS", "Lifetime", "Hallmark Channel", "Freeform", "Comedy Central"],
    "Educational": ["Discovery", "Nat Geo", "History", "PBS", "Smithsonian"],
    "Lifestyle": ["HGTV", "Food Network", "Travel Channel", "Lifetime", "Hallmark"],
    "Cultural": ["Arte", "NHK", "Cultural", "Educational"],
    "Regional": ["Regional", "Local"]
}

# ==== FUNCTION TO CATEGORIZE ====
def categorize_channel(name):
    name_lower = name.lower()
    for premium in premium_channels:
        if premium.lower() in name_lower:
            return "Premium"
    for category, keywords in low_quality_keywords.items():
        for keyword in keywords:
            if keyword.lower() in name_lower:
                return f"Low-quality/Niche - {category}"
    for category, keywords in other_categories_keywords.items():
        for keyword in keywords:
            if keyword.lower() in name_lower:
                return category
    return "Other Decent"

# ==== READ M3U ====
with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# ==== INIT SECTIONS ====
sections = {"Premium": []}
# add all other decent categories
for cat in other_categories_keywords.keys():
    sections[cat] = []
# add low-quality niche categories dynamically
for cat in low_quality_keywords.keys():
    sections[f"Low-quality/Niche - {cat}"] = []
sections["Other Decent"] = []

# ==== REMOVE DUPLICATES ====
seen_urls = set()

# ==== PARSE FILE ====
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("#EXTINF:"):
        match = re.search(r',(.+)', line)
        if match:
            channel_name = match.group(1).strip()
            category = categorize_channel(channel_name)
            # get URL
            if i + 1 < len(lines):
                url_line = lines[i+1].strip()
                if url_line in seen_urls:
                    i += 2
                    continue
                seen_urls.add(url_line)
                sections[category].append(line + "\n")
                sections[category].append(url_line + "\n")
        i += 2
    else:
        i += 1

# ==== SORT AND WRITE OUTPUT ====
with open(output_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n")
    # Premium first
    f.write("#=== PREMIUM CHANNELS ===\n")
    f.writelines(sorted(sections["Premium"]))
    f.write(f"#=== Total Premium Channels: {len(sections['Premium'])//2} ===\n\n")
    # Other decent categories
    for cat in other_categories_keywords.keys():
        f.write(f"#=== {cat.upper()} ===\n")
        f.writelines(sorted(sections[cat]))
        f.write(f"#=== Total {cat} Channels: {len(sections[cat])//2} ===\n\n")
    # Other Decent
    f.write("#=== OTHER DECENT ===\n")
    f.writelines(sorted(sections["Other Decent"]))
    f.write(f"#=== Total Other Decent Channels: {len(sections['Other Decent'])//2} ===\n\n")
    # Low-quality/Niche
    for cat in low_quality_keywords.keys():
        section_name = f"Low-quality/Niche - {cat}"
        f.write(f"#=== {section_name.upper()} ===\n")
        f.writelines(sorted(sections[section_name]))
        f.write(f"#=== Total {cat} Channels: {len(sections[section_name])//2} ===\n\n")
    # TV guide placeholder
    f.write("#=== TV GUIDE PLACEHOLDER ===\n")
    f.write("# This section can be filled with IPTVX-compatible guide info if needed.\n")

print(f"✅ Done! Cleaned and fully categorized M3U saved to: {output_file}")