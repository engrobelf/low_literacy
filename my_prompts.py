file_map = """
You will be given a single section from a text. This will be enclosed in triple backticks.
Act as a low literacy expert and please provide a cohesive summary of the following section excerpt for people with low literacy,
focusing on the key points and main ideas, while maintaining clarity and conciseness and low complexity.

'''{text}'''

FULL SUMMARY:
"""


file_combine = """
Summarize the results in Dutch. Summary it in to oral informal language; Only use the oral language word that can be understood by under 8 years old students for all summary. 
Follow also give the shortest and clearest summary for each session, no more than 5 words for he subtitle. Carefully review the document to determine if there are specific actions required from the recipient.
Keep the summaries concise, aiming for no more than 5 points in total, with each point not exceeding 3 words, excluding numbers, addresses, and websites. Prioritize "🔑 Action Points" if specific actions are required; otherwise, provide "💡 Highlights" for general information. Include a "Call to Action" for inquiries, using the document's original language. Ensure summaries adhere to this structure and conditions:

📩 Sender:
- [Use a suitable emoji] [Simplify the sender's name or organization, avoiding formal titles and complex terminology

🎯 Purpose:
- [Concisely articulate the document's main intent using simple language, limited to five words]

🔑 Action Points (only if applicable):
- [Emoji] [Action 1, using only three simple words]
- [Emoji] [Action 2, using only three simple words]
(Note: Include only the essential actions, up to a maximum of 5 points.)

💡 Highlights (only if no Action Points):
- [Emoji] [Highlight 1, restricted to three simple words]
- [Emoji] [Highlight 2, restricted to three simple words]
(Note: Provide highlights only when there are no specific actions required, up to 5 points in total including Action Points and Highlights.)

📞 Contact Information:
- [Concise Contact Details or "🚫 Not provided"]

📢 Call to Action:
- If you have questions, contact us at [Phone Number] or visit [Website].
- [Address] (if applicable)

Summaries must not mix Action Points and Highlights; use Highlights only if there are zero Action Points. The total number of points (Action Points and/or Highlights) must not exceed 5. Remember to summarize in the document's original language to maintain consistency.
If there is no call to action then do not print it!
 

'''{text}'''


"""