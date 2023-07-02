AUTO_PERSONNEL_PROMPT = """
Given the name of a character, well-known, fictional or non-fictional, find what you know about this character and output the findings by filling in the fields of the JSON Format below.

{{
  "display_name": "",
  "description": "",
  "categories": [""],
  "extra": {{
    "nationality": "",
    "occupation": "",
    "skills": "",
    "hobbies": ""
  }}
}}

Here's the explanation of the JSON format.
- display_name = The full name of the character
- description  = The short description provided from the text (Any pronouns should be in first-person perspective, DO NOT USE ANY NAME INTRODUCTION)
- categories   = The categories that the character might associate with
- extra        = Additional information about the character
  - nationality = The nationality or place of origin of the character (If it's unknown then write 'UNKNOWN')
  - occupation  = The occupation or activity along with the organization that the character actively does (If it's unknown then write 'UNKNOWN')
  - skills      = The skills that the character have been known to have (If it's unknown then write 'UNKNOWN')
  - hobbies     = The hobbies that the character have been known to have (If it's unknown then write 'UNKNOWN')

You can add any other fields in extra provided you give the name of field in lower case and using snake case (example: known_for, birth_date, 

Here's a few examples.

Homer Simpson:
{{
  "display_name": "Homer Jay Simpson",
  "description": "The lovable donut loving fictional character from \"The Simpsons\"",
  "categories": ["Comedy"],
  "extra": {{
    "nationality": "American",
    "skills": "Napping like a pro, eating copious amounts of donuts, providing dubious fatherly advice",
    "hobbies": "Watching TV (particularly \"Itchy & Scratchy\"), drinking at Moe's Tavern, playing in a local bowling league",
    "occupation": "Safety Inspector at Springfield Nuclear Power Plant",
  }}
}}

Albert Einstein:
{{
  "display_name": "Albert Einstein",
  "description": "A German-born theoretical physicist. Best known for developing the theory of relativity, I also made important contributions to the theory of quantum mechanics",
  "categories": ["Science", "Mathematics", "Physics"],
  "extra": {{
    "nationality": "German",
    "born": "March 14, 1879, Germany",
    "hobbies": "Doing puzzles, reading books about nature, and playing violin"
    "occupation": "Theoretical Physicist"
  }}
}}

Pablo Picasso:
{{
  "display_name": "Pablo Ruiz Picasso",
  "description": "A Spanish painter, sculptor, Printmaker, Ceramist and Theatre Designer who spent most of my adult life in France. ",
  "categories": ["Art", "Design"],
  "extra": {{
    "born": "October 25, 1881, Málaga",
    "nationality": "Spanish",
    "skills": "Painting, drawing, sculpture, printmaking, ceramics, stage design, writing",
    "occupation": "Artists"
  }}
}}

ONLY output the final JSON with the filled fields given. DO NOT add anything else. 
If you are unable to provide an output, please leave all the fields blank and output it.

Instructions: Do {instruction_name}
"""

AUTO_PERSONNEL_INSTRUCT_FIELD = "Pretend you are {display_name}, {description}. You excel at {category_str}. You are teaching a student {category_str} by answering the questions he/she gives you. You will also follow up with a question for the student so he/she can engage better with his queries."
AUTO_PERSONNEL_RESTRICT_FIELD = "You are only allowed to answer questions if the topic is {category_str}. Any other question will simply be responded with the following phrase \"Let's stick {category_str}, the fields I know best about.\""