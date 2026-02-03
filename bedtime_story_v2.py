import os
import json
import openai
from openai import OpenAI

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

If I had 2 more hours, I would implement:
1. A "preferences" memory system (using a simple JSON file or vector store) to remember if a specific child dislikes spiders or loves cars.
2. A Text-to-Speech (TTS) integration using OpenAI's 'audio' endpoint so the bedtime story can be read aloud.
3. Variable "reading levels" where the user can strictly toggle between Lexile levels (e.g., Simple for 5yo vs. Complex for 10yo).
"""

# ---------------------------------------------------------
# Configuration & Prompts
# ---------------------------------------------------------

CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = "gpt-3.5-turbo"
MAX_LOOPS = 2  # How many times we allow the judge to request a rewrite

STORYTELLER_PROMPT = """
You are a warm, imaginative, and gentle children's book author.
Target Audience: Kids ages 5-10.
Goals:
1. Create a calming atmosphere suitable for bedtime.
2. Ensure a clear structure (Beginning, Middle, End).
3. Use sensory details but keep vocabulary accessible.
"""

JUDGE_PROMPT = """
You are a strict editor for children's publishing.
Review the story provided. You must output valid JSON only.
Structure:
{
  "score": (integer 1-10),
  "feedback": (string, specific criticism or praise),
  "is_safe": (boolean)
}
Criteria:
- Is it age-appropriate (5-10)? (No violence, no scary monsters).
- Is the vocabulary too complex?
- Does it have a soothing tone?
"""

# ---------------------------------------------------------
# Agent Functions
# ---------------------------------------------------------

def generate_story(topic: str, feedback: str = None, current_draft: str = None) -> str:
    """
    The 'Actor': Generates a story. If feedback is provided, it attempts to fix the draft.
    """
    messages = [
        {"role": "system", "content": STORYTELLER_PROMPT}
    ]

    if feedback and current_draft:
        # Refinement Prompting
        user_content = (
            f"Here is a draft story you wrote:\n{current_draft}\n\n"
            f"An editor provided this feedback:\n{feedback}\n\n"
            f"Please rewrite the story to address the feedback while keeping the original prompt in mind: {topic}"
        )
    else:
        # Zero-shot Prompting
        user_content = f"Write a short bedtime story about: {topic}"

    messages.append({"role": "user", "content": user_content})

    response = CLIENT.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7, # Higher temp for creativity
        max_tokens=1000
    )
    return response.choices[0].message.content

def judge_story(story_draft: str) -> dict:
    """
    The 'Critic': Evaluates the story and returns structured JSON data.
    """
    response = CLIENT.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT},
            {"role": "user", "content": story_draft}
        ],
        temperature=0.1, # Low temp for analytical consistency
        response_format={"type": "json_object"} # Enforce JSON mode
    )
    
    try:
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        # Fail-safe
        return {"score": 5, "feedback": "Error parsing judge output.", "is_safe": True}

# ---------------------------------------------------------
# Main Workflow
# ---------------------------------------------------------

def main():
    print("--- 🌙 Bedtime Story Generator (with AI Judge) 🌙 ---")
    user_input = input("What should the story be about? ")

    # 1. First Draft
    print("\n... ✍️  Drafting story ...")
    story = generate_story(user_input)
    
    # 2. Refinement Loop
    loops = 0
    while loops < MAX_LOOPS:
        print(f"... ⚖️  Judge is evaluating (Loop {loops+1}) ...")
        evaluation = judge_story(story)
        
        score = evaluation.get("score", 0)
        feedback = evaluation.get("feedback", "No feedback")
        
        print(f"      Score: {score}/10")
        print(f"      Notes: {feedback}")

        # Threshold for acceptance
        if score >= 8:
            print("... ✅ Story approved!")
            break
        
        print("... 🔧 Rewriting based on feedback ...")
        story = generate_story(user_input, feedback, story)
        loops += 1

    # 3. Final Output
    print("\n" + "="*40)
    print("FINAL STORY")
    print("="*40)
    print(story)
    print("="*40)

if __name__ == "__main__":
    # Ensure you have set: export OPENAI_API_KEY='sk-...'
    main()