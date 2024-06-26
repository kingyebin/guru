import pandas as pd

# 유효한 장르 목록
valid_genres = [
    "Action", "Platform", "Shooter", "Fighting", "Beat 'em up", "Stealth", "Survival", "Rhythm", 
    "Battle Royale", "Action-adventure", "Survival horror", "Metroidvania", "Adventure", "Text adventures", 
    "Graphic adventures", "Visual novels", "Interactive movie", "Real-time 3D adventures", "Puzzle", 
    "Breakout clone", "Logical", "Physics", "Programming", "Trial-and-error / Exploration", "Hidden object",
    "Reveal the picture", "Tile-matching", "Traditional puzzle", "Puzzle-platform", "Role-playing", 
    "Action RPG", "MMORPG", "Roguelikes", "Tactical RPG", "Sandbox RPG", "First-person party-based RPG", 
    "Monster Tamer", "Simulation", "Construction and management simulation", "Life simulation", 
    "Vehicle simulation", "Strategy", "4X game", "Artillery", "Auto battler (Auto chess)", "MOBA", 
    "RTS", "RTT", "Tower defense", "TBS", "TBT", "Wargame", "Grand strategy wargame", "Sports", "Racing", 
    "Competitive", "Sports-based fighting", "MMO", "Board", "Card", "Casino", "Digital collectible card", 
    "Digital therapeutic video", "Gacha", "Horror", "Idle", "Party", "Photography", "Social deduction", 
    "Trivia", "Typing", "Advergame", "Art", "Casual", "Christian", "Educational", "Esports", "Exergame", 
    "Personalized", "Serious", "Live Interactive", "Sandbox", "Creative", "Open world", "Tycoon"
]

# 한국어 키워드를 유효한 장르로 매핑하는 사전
keyword_mapping = {
    "1인칭": "First-person",
    "2.5D": "2.5D",
    "2D": "2D",
    "2D격투": "2D Fighting",
    "2D플랫포머": "2D Platform",
    "2차대전": "World War II",
    "3D": "3D",
    "3D격투": "3D Fighting",
    "3인칭": "Third-person",
    "80년대": "1980s",
    "90년대": "1990s",
    "MOBA": "MOBA",
    "PvP": "PvP",
    "RTS": "RTS",
    "SF": "Science Fiction",
    "Scrolling": "Scrolling",
    "Static": "Static",
    "VR": "VR",
    "VR전용": "VR Only",
    "가로": "Horizontal",
    "가상생활": "Simulation",
    "가족과함께": "Family Friendly",
    "감성적인": "Emotional",
    "갬블링": "Gambling",
    "거래": "Trading",
    "건설": "Construction",
    "걷기시뮬레이터": "Walking Simulator",
    "격투": "Fighting",
    "경마": "Horse Racing",
    "경영": "Management",
    "경영/타이쿤": "Tycoon",
    "경제": "Economics",
    "고어": "Gore",
    "골프": "Golf",
    "공포": "Horror",
    "귀여운": "Cute",
    "기지건설": "Base Building",
    "기차": "Train",
    "낚시": "Fishing",
    "논리": "Logical",
    "농구": "Basketball",
    "농장시뮬레이션": "Farming Simulation",
    "다양한결말": "Multiple Endings",
    "다채로운": "Colorful",
    "달리기": "Running",
    "당구": "Billiards",
    "댄스": "Dance",
    "던전크롤러": "Dungeon Crawler",
    "덱빌딩": "Deck Building",
    "드라마": "Drama",
    "등각": "Isometric",
    "디펜스": "Defense",
    "라이트건": "Light Gun",
    "랠리/오프로드": "Rally/Off-road",
    "럭비": "Rugby",
    "레슬링": "Wrestling",
    "레이싱": "Racing",
    "레일": "Rail",
    "로그라이크": "Roguelike",
    "로맨스": "Romance",
    "로봇": "Robots",
    "로컬멀티플레이어": "Local Multiplayer",
    "로컬협동": "Local Co-op",
    "롤플레잉": "Role-playing",
    "리니어": "Linear",
    "리듬": "Rhythm",
    "리플레이가치": "Replay Value",
    "릴랙싱": "Relaxing",
    "만화같은": "Cartoon",
    "만화책": "Comic Book",
    "맞추기": "Matching",
    "매직": "Magic",
    "멀티플레이어": "Multiplayer",
    "메트로배니아": "Metroidvania",
    "모드가능": "Moddable",
    "모터사이클": "Motorcycle",
    "모토크로스": "Motocross",
    "무료플레이": "Free to Play",
    "미니게임": "Minigames",
    "미니멀리스트": "Minimalist",
    "미스터리": "Mystery",
    "미식축구": "American Football",
    "민간항공기": "Civil Aviation",
    "배구": "Volleyball",
    "보드": "Board",
    "보드/카드": "Board/Card",
    "복고풍": "Retro",
    "복싱": "Boxing",
    "복싱/마샬아츠": "Boxing/Martial Arts",
    "볼링": "Bowling",
    "분위기있음": "Atmospheric",
    "비선형적": "Nonlinear",
    "비주얼노벨": "Visual Novel",
    "비행": "Flight",
    "빗뎀업": "Beat 'em up",
    "사냥": "Hunting",
    "사육/건설": "Raising/Construction",
    "사이버펑크": "Cyberpunk",
    "상식": "Trivia",
    "샌드박스": "Sandbox",
    "생존": "Survival",
    "서핑/웨이크보드": "Surfing/Wakeboarding",
    "선정적": "Suggestive",
    "선택의중요": "Choice Matters",
    "성인": "Adult",
    "세로": "Vertical",
    "소형우주선": "Small Spaceship",
    "수중": "Underwater",
    "숨은그림찾기": "Hidden Object",
    "슈팅": "Shooter",
    "슛뎀업": "Shoot 'em up",
    "스노우보드": "Snowboarding",
    "스키/스노우보드": "Skiing/Snowboarding",
    "스펙타클파이터": "Spectacle Fighter",
    "스포츠": "Sports",
    "스포츠시뮬레이션": "Sports Simulation",
    "스포츠카": "Sports Car",
    "시간관리": "Time Management",
    "시뮬레이션": "Simulation",
    "실시간": "Real-time",
    "실험적": "Experimental",
    "심리적": "Psychological",
    "심리적공포": "Psychological Horror",
    "싱글플레이어": "Single-player",
    "쌓기": "Stacking",
    "아니메": "Anime",
    "아름다운": "Beautiful",
    "아이스하키": "Ice Hockey",
    "아케이드": "Arcade",
    "앞서해보기": "Early Access",
    "애완동물": "Pet",
    "액션": "Action",
    "액션RPG": "Action RPG",
    "액션로그라이크": "Action Roguelike",
    "액션어드벤처": "Action-adventure",
    "야구": "Baseball",
    "어드벤처": "Adventure",
    "어려움": "Difficult",
    "에듀테인먼트": "Edutainment",
    "에피소드": "Episodic",
    "여성주인공": "Female Protagonist",
    "역사": "History",
    "역사의": "Historical",
    "영원한죽음": "Permadeath",
    "오픈월드": "Open world",
    "온라인협동": "Online Co-op",
    "올드스쿨": "Old School",
    "요리": "Cooking",
    "우주": "Space",
    "운동": "Exercise",
    "운동경기": "Sports Game",
    "운전": "Driving",
    "음악": "Music",
    "응접실": "Parlor",
    "이동수단": "Vehicles",
    "인디": "Indie",
    "인터랙티브무비": "Interactive Movie",
    "인터랙티브픽션": "Interactive Fiction",
    "자동차": "Car",
    "자동차전투": "Car Combat",
    "자본주의": "Capitalism",
    "자연": "Nature",
    "자원관리": "Resource Management",
    "작곡": "Composition",
    "전략": "Strategy",
    "전쟁": "War",
    "전투": "Combat",
    "절차적생성": "Procedural Generation",
    "정부": "Government",
    "제트기": "Jet",
    "중세": "Medieval",
    "직업": "Job",
    "철학적인": "Philosophical",
    "초현대적": "Ultra-modern",
    "총기커스터마이징": "Gun Customization",
    "추상적": "Abstract",
    "축구": "Soccer",
    "카드": "Card",
    "카드배틀": "Card Battle",
    "카트": "Kart",
    "캐릭터커스터마이즈": "Character Customization",
    "캐주얼": "Casual",
    "컨트롤러": "Controller",
    "크래프팅": "Crafting",
    "클리커": "Clicker",
    "타워디펜스": "Tower Defense",
    "타이쿤": "Tycoon",
    "탄막슈팅": "Bullet Hell",
    "탐험": "Exploration",
    "탑다운": "Top-down",
    "택틱스": "Tactics",
    "턴기반전투": "Turn-based Combat",
    "턴기반택틱스": "Turn-based Tactics",
    "턴제": "Turn-based",
    "트럭": "Truck",
    "팀": "Team",
    "파티": "Party",
    "판타지": "Fantasy",
    "퍼즐": "Puzzle",
    "포스트아포칼립스": "Post-apocalyptic",
    "포인트앤클릭": "Point-and-click",
    "폭력": "Violence",
    "풍부한스토리": "Rich Story",
    "플랫포머": "Platform",
    "픽셀그래픽": "Pixel Graphics",
    "핀볼": "Pinball",
    "한국어지원": "Korean Supported",
    "합본": "Compilation",
    "헬리콥터": "Helicopter",
    "현대적": "Modern",
    "현실적": "Realistic",
    "협동": "Co-op",
    "횡스크롤": "Side-scroller",
    "훌륭한사운드트랙": "Great Soundtrack"
}

# CSV 파일 읽기 (인코딩 지정)
file_path = '/Users/AIFFELthon/final/data/null/genre/minimap_genre.csv'
df_before = pd.read_csv(file_path, encoding='utf-8')

# 'Keywords' 열의 값을 한국어 키워드에서 유효한 장르로 변경
def map_keywords(keywords):
    if pd.isna(keywords):
        return 'Miscellaneous'
    keywords_list = keywords.split('#')
    mapped_keywords = [keyword_mapping.get(kw.strip(), "Miscellaneous") for kw in keywords_list if kw.strip()]
    valid_keywords = [kw for kw in mapped_keywords if kw in valid_genres]
    return ', '.join(valid_keywords) if valid_keywords else 'Miscellaneous'

df_after = df_before.copy()
df_after['Keywords'] = df_after['Keywords'].apply(map_keywords)

# 결과를 CSV 파일로 저장 (인코딩 지정)
output_path = '/Users/AIFFELthon/final/data/null/minimap_genre_updated.csv'
df_after.to_csv(output_path, index=False, encoding='utf-8')

output_path