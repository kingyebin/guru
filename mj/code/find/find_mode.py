import pandas as pd

df_mode = pd.read_csv('/Users/AIFFELthon/final/data/tag_list.csv')


# Updated list of modes provided by the user
modes = [
    "Single player", "Multiplayer", "Co-operative", "Split screen", "Massively Multiplayer Online", "MMO", 
    "Battle Royale", "PvP", "Player vs Player", "PvE", "Player vs Environment", "Team-based", "Campaign", 
    "Sandbox", "Survival", "Roguelike", "Simulation", "Competitive", "Turn-based", "RTS", "Arcade", 
    "Educational", "VR", "AR", "Story", "Time Trial", "Endless", "Freeroam", "Creative", "Adventure", 
    "Spectator", "Practice", "Hardcore", "Looter Shooter", "Boss Rush", "Escort Mission", "Horde", 
    "Stealth", "Puzzle", "Construction", "Role-Playing", "Capture the Flag", "King of the Hill", 
    "Deathmatch", "Conquest", "Breakthrough", "Hazard Zone", "Portal", "Battle Royale", "Creative Mode", 
    "Save the World", "Lego Fortnite", "Training", "Firing Range", "Defense", "Capture Point", "Zombie", 
    "Search", "Destroy", "Team Deathmatch", "Gun", "Headquarters", "Hardpoint", "Demolition", "Infection"
]

# Extend the function to handle specific patterns for Single player and Multiplayer
def find_modes_advanced(tag):
    tag_lower = tag.lower()
    present_modes = []
    
    # Single player patterns
    single_player_patterns = [
        r'\b1 player\b', r'\b1-player\b', r'\b1-player-hangman-game\b'
    ]
    
    # Multiplayer patterns
    multiplayer_patterns = [
        r'\b1 - 9 players \(Alternating\)\b', r'\b1 to 4 Players\b', r'\b1-2-players\b', r'\b1-4 player\b',
        r'\b1-4-players\b', r'\b1-8 players\b', r'\b1-v-1\b', r'\b1-vs-1\b', r'\b1-vs-100\b', r'\b2 or 4 players\b',
        r'\b2 players\b', r'\b2-4 player multiplayer\b', r'\b2-4-player\b', r'\b2-4-players\b'
    ]
    
    # Both Single player and Multiplayer
    single_multiplayer_patterns = [r'\b1–2 player\b']
    
    # Check for exact matches in modes list
    for mode in modes:
        if re.search(r'\b' + re.escape(mode) + r'\b', tag_lower, re.IGNORECASE):
            present_modes.append(mode)
    
    # Check for single player patterns
    for pattern in single_player_patterns:
        if re.search(pattern, tag_lower):
            present_modes.append("Single player")
            break
    
    # Check for multiplayer patterns
    for pattern in multiplayer_patterns:
        if re.search(pattern, tag_lower):
            present_modes.append("Multiplayer")
            break
    
    # Check for both single player and multiplayer patterns
    for pattern in single_multiplayer_patterns:
        if re.search(pattern, tag_lower):
            present_modes.append("Single player")
            present_modes.append("Multiplayer")
            break
    
    # Remove duplicates and sort the modes
    present_modes = sorted(set(present_modes))
    
    return '||'.join(present_modes) if present_modes else None


# Convert 'Unique Tags' column to string to handle NaN values and avoid AttributeError
df_mode['Unique Tags'] = df_mode['Unique Tags'].str.replace('-', ', ')

# Apply the function again to create a new column 'Modes_Present'
df_mode['Modes_Present'] = df_mode['Unique Tags'].apply(find_modes_advanced)

# Display the updated dataframe
df_mode.head()