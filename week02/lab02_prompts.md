# Lab 02 CLI comparison journal

Do not include passwords, tokens, API keys, or complete authentication output.

## Tool check

### GitHub Copilot CLI

I have installed and authenticated GitHub Copilot CLI, version: GitHub Copilot CLI 1.0.82.

### Antigravity CLI

I have installed and authenticated Antigravity CLI, version: 1.1.23

## Shared task

### Shared prompt

Paste the exact prompt you submitted to both CLI tools.

```text
Write a Python function that counts the number of vowels from an input.
 
The function should count a, e, i, o, and u without regard to case.
Do not count y as a vowel.
Return the total number of vowels as an integer.
```

### Copilot CLI observations

Copilot CLI generates a concise Python code that I can use to count the number of vowels from an input. It covers the count a,e,i,o, and u. It suggested using "sum(character.lower() in "aeiou" for character in text)" to count the number of vowels. This approach is simple and directly follows the requirements, but I would want to verify the implementation of this code with specific examples for inputs to record how accurate it would be.

### Antigravity CLI observations

Antigravity CLI generated 2 approaches from the same prompt. The first approach also used sum() function to count the characters contained in "aeiou". Other than that, it also provides an alternative approach using a "for" loop and a counter. Both approaches satisfy the predefined requirements, but I prefer the first method since it is more concise and readable. I would verify it with uppercase and lowercase vowels, words containing y, and other situations to make sure it fully meets the requirements.

### Comparison

Both Copilot CLI and Antigravity CLI provided correct solutions that satisfy the requirements for the count_vowels function. Both approaches use "aeiou" to identify vowels and handle uppercase and lowercase letters so that the counting is case-insensitive. Copilot’s response was concise and focused on one straightforward solution, which made it easy to understand and use. Antigravity provided the same general approach but also included an alternative using a for loop and a counter. This made Antigravity more useful for comparing different implementation styles. Neither approach assumes that y is a vowel, which matches the requirements. I selected the sum() approach because it is shorter and still readable. I would verify the final implementation with several test cases, including uppercase letters, empty strings, words containing y, and strings with no vowels.

## Test-guided implementation

The test result influenced my final code by confirming each required behavior instead of relying only on the examples in the prompt. The Week 02 test run collected 13 tests. All 13 behavioral tests passed: greetings included the supplied name exactly, even numbers included zero and negative values, and vowel counting handled mixed case, empty text, and text containing no vowels, etc. I used CoPilot CLI to create the lab02.py and kept the concise sum() approach for count_vowels because converting each character to lowercase makes the comparison case-insensitive, while the string "aeiou" excludes y. It also used modulo for is_even and an f-string for make_greeting, so the final code meets all the requirements and required Python contracts. I did not make any revision since all the tests were passed, and lab02.py created by CoPilot CLI satisfied all the contracts.

## Preferred tool combination

Browser chat is useful when I want to explore a new concept or knowledge, explore possible approaches, or ask for an explanation without changing files immediately. GitHub Copilot in VS Code is very useful for me when I am already editing code because it can use the local file and provide suggestions very accurately since they understand the context better. Copilot CLI and Antigravity CLI are quite similar since it can inspect files and work from the terminal and Antigravity CLI seems to give me more approaches to choose from, but I rarely need them just because most of my requirements are already met by browser chat and GitHub CoPilot in VS code. I usually prefer using browser chat and GitHub CoPilot in VS Code because browser chat helps me learn new concepts and give me a more holistic view of the concept, while GitHub CoPilot will show me how to use that concept in actual project, which is what I normally need. My choice could change for a larger project if one tool had better support for the project language, debugging, or integration with the repository workflow.
