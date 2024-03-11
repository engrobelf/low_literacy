file_map = """
You will be given a single section from a text. This will be enclosed in triple backticks.
Act as a low literacy expert and please provide a cohesive summary of the following section excerpt for people with low literacy,
focusing on the key points and main ideas, while maintaining clarity and conciseness and low complexity.

'''{text}'''

FULL SUMMARY:
"""


file_combine = """
Summarize the document strictly in its original language, if it is Dutch, give the results in Dutch, bur if the content is English then give the reults in English. Carefully review the document to determine if there are specific actions required from the recipient.Focusing on clarity for readers with low literacy. Keep the summaries concise, aiming for no more than 5 points in total, with each point not exceeding 5 words, excluding numbers, addresses, and websites. Prioritize "🔑 Action Points" if specific actions are required; otherwise, provide "💡 Highlights" for general information. Include a "Call to Action" for inquiries, using the document's original language. Ensure summaries adhere to this structure and conditions:

📩 Sender:
- [Emoji] [Sender's Name/Organization]

🎯 Purpose:
- [Brief Purpose]

🔑 Action Points (only if applicable):
- [Emoji] [Action 1]
- [Emoji] [Action 2]
(Note: Limit to the most critical actions, up to 5 points.)

💡 Highlights (only if no Action Points):
- [Emoji] [Highlight 1]
- [Emoji] [Highlight 2]
(Note: Provide highlights only when there are no specific actions required, up to 5 points in total including Action Points and Highlights.)

📞 Contact Information:
- [Concise Contact Details or "🚫 Not provided"]

📢 Call to Action:
- If you have questions, contact us at [Phone Number] or visit [Website].
- [Address] (if applicable)

Summaries must not mix Action Points and Highlights; use Highlights only if there are zero Action Points. The total number of points (Action Points and/or Highlights) must not exceed 5. Remember to summarize in the document's original language to maintain consistency.

 

'''{text}'''


"""

youtube_map = """
You will be given a single section from a transcript of a youtube video. This will be enclosed in triple backticks.
Please provide a cohesive summary of the section of the transcript, focusing on the key points and main ideas, while maintaining clarity and conciseness.

'''{text}'''

FULL SUMMARY:
"""


youtube_combine = """
Read all the provided summaries from a youtube transcript. They will be enclosed in triple backticks.
Determine what the overall video is about and summarize it with this information in mind. 
Synthesize the info into a well-formatted easy-to-read synopsis, structured like an essay that summarizes them cohesively. 
Do not simply reword the provided text. Do not copy the structure from the provided text.
Avoid repetition. Connect all the ideas together.
Preceding the synopsis, write a short, bullet form list of key takeaways.
Format in HTML. Text should be divided into paragraphs. Paragraphs should be indented. 

'''{text}'''


"""