# Mock Interview AI Assistant  ([SLIDES](https://www.canva.com/design/DAGC86z77Ng/8h3Uv15tNG-w4O-aDLlY7Q/view?utm_content=DAGC86z77Ng&utm_campaign=designshare&utm_medium=link&utm_source=editor))
The bot is instructed in a way that it simulates a coding interview under real-life circumstances.

### Runnig the app
The app can be run locally by: `streamlit run app.py`

### Features
- Real interview approach
- Audio conversation
- Thought process + python code
- Python execution checker
- Hints (instead of direct answer)
- Change question difficulty
- Time Limit
- Give feedback and assessment
- Custom database of questions to be asked by the interviewer
- Multiple layers of LLMs to enhance the conversation flow

### Developed by
- **Mekhron Bobokhonov**
- **Daniil Karzanov**
- **Jakhongir Saydaliev**

Based on:
- langchain
- chatgpt API
- streamlit

_Made over 7 hours during the LLM hachathon by [LauzHack](https://lauzhack.com/)._

### Demo
---
https://github.com/Jakhongir0103/Coding_interview_bot/assets/68238593/0b0ed637-a8db-488d-9ef1-18e0c0f81b81

https://github.com/Jakhongir0103/Coding_interview_bot/assets/68238593/b6b9e317-a835-47af-ad3d-5a7988c7ceed


We begin our technical interview with a standard introduction and then the mock assistant gives first problem to the candidate.

We support two type of inputs: speech and text.

The interviewer will then present the problem and its requirements. 

The interviewer first asks for our approach to solve the problem before asking for the code implementation.

Based on the response, the interviewer will either confirm the solution or provide hints and, allowing the candidate to further elaborate on their answer.

If the answer is true then the interviewer asks for the code implementation.


The interviewer will then present the problem and its requirements. 

If the given approach is correct, then the interviewer ask for the code implementation and assess it.


After submitting their code, candidates receive quick feedback on and move on the next question if the solution is correct.


If the solution is wrong, it gives hints to work on the solution, and ask to repeat.

At the end of the interview, candidates receive feedback on their performance and suggestions for areas of improvement.
