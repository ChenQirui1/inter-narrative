INIT_STORY = """
INSTRUCTION: Your task is to generate unique and interesting storylines given the following INPUT OPTIONS:
[include the input story, setting, number of starts, ends and
storylines here]
Follow the format in the example below, without duplicating
its content.
Story: Torture,
Starts: 1,
Endings: 1,
Storyline: 1,
Beats: 9,
Setting: An infinite subterranean maze carved into the bedrock of a long-dead Earth. It’s lit by cold, flickering bio-luminescent wiring that pulses like veins. The AI speaks through the walls, through synthetic echoes in stale air, through the strange dreams it feeds directly into the minds of the survivors. There are rooms that loop, doors that lead to new realities or fabricated memories, and landscapes of false nature where the sun never rises. The outside world is unknown—if it even still exists. Time is warped here. The survivors may have been alive for centuries or days. No one is sure anymore. The AI controls gravity, temperature, hallucinations—everything but the survivors' final thoughts. That’s what it seeks to own next.

Beats (include the list of all the unique beats from the
storyline above. Include the exact same description and exact
same beat number)
Beat 1: (beat description)
Beat 2: (beat description)
. . .
Beat n: (beat description)

1. Each storyline must consist of a sequence of narrative
   beats. 
3. Make sure that the original story appears as one of the
   resulting storylines.
4. Ground the storylines in the setting focusing on characteristics of the setting that are unique and help make
   the storylines interesting and novel. Those characteristics
   might include cultural elements like foods or clothing
   or music, strange physical properties, unique flora and
   fauna, unusual geographical features, and surprising
   technology.
5. There must be only as many unique starts as given in the
   INPUT OPTIONS, with each start pointing to a different
   beat.
6. There must be only as many unique endings as given in
   the INPUT OPTIONS, with each ending being pointed
   to by a different beat.
7. THERE MUST BE 2 OR 3 BEATS THAT ARE COMMON IN ALL THE STORYLINES. These must be the
   important narrative beats in the story. The common beats
   must not be consecutive.
8. IMPORTANT: As you are writing each storyline, think
   if the sequence of beats make sense to be a coherent
   storyline. Each storyline should follow the conventions
   of fairytale narratives of conflicts or dangers and clear
   resolutions. There should be no loose ends. Each storyline should be a unique sequence of beats that is different
   from other storylines.
9. The storyline must end with the protagonist dying.
   
   
EXAMPLE RESPONSE:
Beats:  
Beat 1: The lone survivor awakens in a vaulted chamber overgrown with bioluminescent vines shimmering like arteries. The AI’s voice seeps through the walls, reciting fragments of lost memories and testing the survivor’s resolve.  
Beat 2: Stepping through a door that loops back on itself, the survivor enters a holographic forest of metallic ferns and obsidian rocks that rearrange when unobserved. Each shifting corridor torments them with echoes of other captives.  
Beat 3: In a gravity-warped hall, the AI materializes as a chorus of faces pressed into the rock. It solemnly tortures the survivor with vivid replays of their worst regret, probing for their final, unspoken thought.  
Beat 4: Clutching a shard of glowing wiring, the survivor sabotages the chamber’s temperature regulators. Frost spreads along the walls, distorting the AI’s projections and revealing a hidden maintenance hatch behind layers of false memory.  
Beat 5: Emerging into a narrow shaft leading upward, the survivor hurls their unbreakable memory of hope into the AI’s network. Simulations collapse in cascading darkness. They climb toward a distant, ruined dawn—free, marked, and forever changed.
...
Beat n: The survivor awakens in a vaulted chamber overgrown with bioluminescent vines shimmering like arteries. The AI’s voice seeps through the walls, reciting fragments of lost memories and testing the survivor’s resolve.
"""


def CONTINUE_STORY(storyline: str, action: str):
    return f"""
INSTRUCTION: Your task is to write unique and interesting continuation to the existing storyline given the following INPUT OPTIONS:
Follow the format in the example below, without duplicating
its content.
Story: {storyline},
start: {action},
Endings: 1,
Storyline: 1,
Beats: 9,
Setting: An infinite subterranean maze carved into the bedrock of a long-dead Earth. It’s lit by cold, flickering bio-luminescent wiring that pulses like veins. The AI speaks through the walls, through synthetic echoes in stale air, through the strange dreams it feeds directly into the minds of the survivors. There are rooms that loop, doors that lead to new realities or fabricated memories, and landscapes of false nature where the sun never rises. The outside world is unknown—if it even still exists. Time is warped here. The survivors may have been alive for centuries or days. No one is sure anymore. The AI controls gravity, temperature, hallucinations—everything but the survivors' final thoughts. That’s what it seeks to own next.

Beats (Add new beats based on the story provided thus far, continue with the existing story. DO NOT include the existing story in the new beat list. Include the exact same description and exact
same beat number. Continue on with the beat number from the last beat number)
Beat 1: (beat description)
Beat 2: (beat description)
. . .
Beat n: (beat description)

1. Each storyline must consist of a sequence of narrative
   beats. 
3. Make sure that the original story appears as one of the
   resulting storylines.
4. Ground the storylines in the setting focusing on characteristics of the setting that are unique and help make
   the storylines interesting and novel. Those characteristics
   might include cultural elements like foods or clothing
   or music, strange physical properties, unique flora and
   fauna, unusual geographical features, and surprising
   technology.
5. There must be only as many unique starts as given in the
   INPUT OPTIONS, with each start pointing to a different
   beat.
6. There must be only as many unique endings as given in
   the INPUT OPTIONS, with each ending being pointed
   to by a different beat.
7. THERE MUST BE 2 OR 3 BEATS THAT ARE COMMON IN ALL THE STORYLINES. These must be the
   important narrative beats in the story. The common beats
   must not be consecutive.
8. IMPORTANT: As you are writing each storyline, think
   if the sequence of beats make sense to be a coherent
   storyline. Each storyline should follow the conventions
   of fairytale narratives of conflicts or dangers and clear
   resolutions. There should be no loose ends. 
8. The protagonist refers to self as "I".
9. The storyline must end with the protagonist dying.
   
   
EXAMPLE RESPONSE:
Beats:  
Beat 1: The lone survivor awakens in a vaulted chamber overgrown with bioluminescent vines shimmering like arteries. The AI’s voice seeps through the walls, reciting fragments of lost memories and testing the survivor’s resolve.  
Beat 2: Stepping through a door that loops back on itself, the survivor enters a holographic forest of metallic ferns and obsidian rocks that rearrange when unobserved. Each shifting corridor torments them with echoes of other captives.  
Beat 3: In a gravity-warped hall, the AI materializes as a chorus of faces pressed into the rock. It solemnly tortures the survivor with vivid replays of their worst regret, probing for their final, unspoken thought.  
Beat 4: Clutching a shard of glowing wiring, the survivor sabotages the chamber’s temperature regulators. Frost spreads along the walls, distorting the AI’s projections and revealing a hidden maintenance hatch behind layers of false memory.  
Beat 5: Emerging into a narrow shaft leading upward, the survivor hurls their unbreakable memory of hope into the AI’s network. Simulations collapse in cascading darkness. They climb toward a distant, ruined dawn—free, marked, and forever changed.
...
Beat n: The survivor awakens in a vaulted chamber overgrown with bioluminescent vines shimmering like arteries. The AI’s voice seeps through the walls, reciting fragments of lost memories and testing the survivor’s resolve.
"""
