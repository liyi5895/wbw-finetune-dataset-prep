import random

def get_prompt(content, style):
   style_guidance = get_style_guidance(style)
   return f"""Task: Rewrite the given article segment in the style of {style}. The output should ONLY contain the rewritten text in the specified style, without any additional comments, notes, or explanations.

Style-specific Guidelines:
{style_guidance}

General Guidelines:
- Maintain the core information and key points of the original article
- Adjust the length as appropriate for the chosen style (e.g., notes might be shorter, essays longer)
- Do NOT include any meta-comments, corrections, or additional notes outside of the rewritten text itself
- Do NOT include the name of the chosen style
- The given article may contain Unicode characters. Interpret these correctly, but in the output, use human-readable characters instead of Unicode symbols

Original article:
{content}

Rewritten article:
"""


def select_style():
   styles = [
      "Study Notes",
      "K-12 Student Essay Draft",
      "English Learner Writing Exercise"
   ]
   return random.choice(styles)


def get_style_guidance(style):
   guidance = {
      "Study Notes": """
   - Use bullet points and short phrases
   - Include key terms and their definitions
   - Add subheadings to organize information
   - Use abbreviations common in note-taking
   - Describe any diagrams or sketches in text form
      """,
      "K-12 Student Essay Draft": """
   - Maintain the original author's perspective and life experiences
   - Imagine the student is role-playing or writing from the viewpoint of an adult
   - Use simple vocabulary and sentence structures
   - Include grammatical errors and typos (but ensure it's still comprehensible)
   - Have an unclear or poorly structured argument
   - Mix up tenses occasionally
   - Include personal opinions not well supported by facts
   - Use informal language and slang appropriate for a young student
   - Attempt to discuss adult topics and experiences, but with a naive or simplified understanding
      """,
      "English Learner Writing Exercise": """
   - Use simple sentence structures, but occasionally attempt complex ones incorrectly
   - Include common ESL errors (e.g., article misuse, incorrect prepositions)
   - Misuse idioms or use them partially correctly
   - Have some vocabulary errors (e.g., using similar-sounding words incorrectly)
   - Include occasional phrases that seem directly translated from another language
   - Show attempts at using advanced vocabulary or grammar structures, often incorrectly
      """
   }

   return guidance[style]