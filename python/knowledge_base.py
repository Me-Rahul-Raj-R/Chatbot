"""
knowledge_base.py - Knowledge Base, Intent Detection, Normalization, and Answer Retrieval
for the Educational Conversational Chatbot.
"""

import re
import difflib
from typing import Dict, Any, Optional, Tuple, List

# ---------- Typo & Contraction Mappings ----------
TYPO_MAP = {
    "pyhton": "python",
    "pyton": "python",
    "javasript": "javascript",
    "javscript": "javascript",
    "htmll": "html",
    "html5": "html",
    "css3": "css",
    "databse": "database",
    "datbase": "database",
    "funciton": "function",
    "funtion": "function",
    "variabel": "variable",
    "varible": "variable",
    "algoritm": "algorithm",
    "algorithem": "algorithm",
    "recurson": "recursion",
    "recursun": "recursion",
    "intewiew": "interview",
    "intervew": "interview",
    "porcess": "process",
    "thred": "thread",
    "oops": "oop",
    "oops.": "oop",
}

CONTRACTIONS = {
    "what's": "what is",
    "whats": "what is",
    "how's": "how is",
    "hows": "how is",
    "where's": "where is",
    "who's": "who is",
    "it's": "it is",
    "its": "it is",
    "can't": "cannot",
    "dont": "do not",
    "don't": "do not",
    "doesn't": "does not",
    "doesnt": "does not",
    "isn't": "is not",
    "isnt": "is not",
    "aren't": "are not",
    "arent": "are not",
    "i'm": "i am",
    "im": "i am",
    "you're": "you are",
    "youre": "you are",
    "tell me about": "explain",
    "can you explain": "explain",
    "could you explain": "explain",
    "what do you know about": "explain",
    "give me details on": "explain",
    "i want to know about": "explain",
    "teach me": "explain",
    "give me python basics": "explain python",
    "python explanation please": "explain python",
    "python meaning": "what is python",
    "what does python mean": "what is python",
    "what is meant by python": "what is python",
    "pillars of oop": "explain oop",
    "pillar of oop": "explain oop",
    "pillars of oops": "explain oop",
    "pillar of oops": "explain oop",
    "4 pillars of oop": "explain oop",
    "four pillars of oop": "explain oop",
    "4 pillars of oops": "explain oop",
    "four pillars of oops": "explain oop",
    "acid property": "explain acid properties",
    "acid properties": "explain acid properties",
    "give an example of": "example",
    "show an example of": "example",
    "show example": "example",
    "code example": "example",
}

# ---------- Normalization Function ----------
def normalize_text(text: str) -> str:
    """
    Internal normalization:
    1. Convert to lowercase.
    2. Expand common contractions & key phrases.
    3. Fix common technical typos.
    4. Remove unnecessary punctuation (, ! ? . ; : " ' ( ) [ ] { } ).
    5. Collapse multiple spaces and trim.
    """
    if not text:
        return ""
    
    norm = text.lower().strip()
    
    # Expand contractions & key phrase shortcuts
    for key, val in CONTRACTIONS.items():
        norm = re.sub(r'\b' + re.escape(key) + r'\b', val, norm)
        
    # Remove punctuation except alphanumeric and spaces
    norm = re.sub(r"[^\w\s]", " ", norm)
    
    # Fix typos
    words = norm.split()
    corrected_words = [TYPO_MAP.get(w, w) for w in words]
    norm = " ".join(corrected_words)
    
    # Collapse multiple spaces
    norm = re.sub(r"\s+", " ", norm).strip()
    return norm

# ---------- Comprehensive Local Knowledge Base ----------

KB_EXACT: Dict[str, str] = {
    # --- Greetings & Casual ---
    "hello": "Hello! I am your educational assistant. How can I help you learn programming, web development, computer science, or SQL today?",
    "hi": "Hi there! Feel free to ask me any question about Python, HTML, CSS, JavaScript, SQL, Data Structures, Git, or Networking!",
    "hey": "Hey! What concept would you like to explore today?",
    "good morning": "Good morning! Ready to learn something new today?",
    "good afternoon": "Good afternoon! How can I assist with your study or coding today?",
    "good evening": "Good evening! What programming or CS topic can I help you with?",
    "how are you": "I am doing great and ready to assist you! How can I help you today?",
    "thank you": "You're very welcome! Let me know if you have any more questions.",
    "thanks": "Glad to help! Feel free to ask any follow-up questions.",
    "okay": "Great! What would you like to learn next?",
    "bye": "Goodbye! Have a wonderful day and happy coding!",
    "goodbye": "Goodbye! Keep practicing and learning!",
    "see you": "See you later! Feel free to come back whenever you have questions.",

    # --- Project Self-Awareness ---
    "what is this chatbot": "This is a Conversational Educational Assistant built using a hybrid architecture (Python standard library backend with optional Gemini AI fallback, HTML5, CSS3, and Vanilla JavaScript).",
    "how does this chatbot work": "It follows a multi-step pipeline:\n1. Input Normalization (cleans spaces, punctuation, typos).\n2. Topic & Intent Classification.\n3. Local Knowledge Base Retrieval (fast, rule-based answers).\n4. Gemini API Fallback (when API key is set and local KB lacks an answer).\n5. Friendly Fallback (polite response listing valid topics when offline).",
    "what technologies are used": "This application uses standard HTML5 for layout, CSS3 for modern styling, Vanilla JavaScript for dynamic interaction, and Python's `http.server` for backend API routing.",
    "why did you build this": "This project was created as a lightweight educational tool to demonstrate chatbot architecture, intent recognition, and clean full-stack web integration without heavy frameworks.",
    "why did you use python": "Python was chosen for the backend because of its clean readable syntax, robust standard libraries (`http.server`, `urllib`, `re`), and ease of maintaining a modular knowledge base.",
    "why did you use javascript": "JavaScript handles asynchronous DOM updates, user input capture, API fetches to `/chat`, and typing indicators in the browser.",
    "what is the role of html": "HTML provides the semantic structure of the chat interface, including headers, chat history window, suggested question buttons, and text input.",
    "what is the role of css": "CSS provides modern styling, visual hierarchy, user/bot message bubble alignment, responsive flexbox layout, and smooth animations.",
    "is this chatbot ai": "It is a hybrid system! It uses rule-based local pattern matching for fast, accurate core technical answers, and can delegate complex open-ended questions to the Google Gemini API when configured.",
    "is this chatgpt": "No, this is a custom educational chatbot project designed for learning web development and programming fundamentals. It is not ChatGPT.",

    # --- General Programming Fundamentals ---
    "what is programming": "Programming is the process of writing instructions (code) for a computer to execute in order to perform specific tasks or solve problems.",
    "what is a programming language": "A programming language is a formal set of rules, syntax, and vocabulary used to instruct computers to perform computations. Examples include Python, JavaScript, C++, and Java.",
    "what is source code": "Source code is human-readable text written in a programming language before it is compiled or interpreted into machine-executable instructions.",
    "what is a program": "A program is a collection of compiled or interpreted instructions executed by a computer to accomplish a specific function (e.g., a web browser or calculator).",
    "what is an algorithm": "An algorithm is a step-by-step procedure or set of rules defined to solve a specific problem or perform a task efficiently.",
    "what is pseudocode": "Pseudocode is an informal, high-level description of an algorithm written in plain language instead of strict programming syntax, used for planning code logic.",
    "what is syntax": "Syntax refers to the set of formal rules governing the structure, spelling, and grammar of valid code statements in a programming language.",
    "what is a variable": "A variable is a named storage location in memory used to hold data values that can be read or modified during program execution. Example in Python: `x = 10`.",
    "what is a constant": "A constant is a value that cannot be altered by the program during execution once it is defined (e.g., `const PI = 3.14` in JS).",
    "what is a data type": "A data type classifies the kind of value a variable holds, determining what operations can be performed on it (e.g., Integer, Float, String, Boolean).",
    "what is an operator": "An operator is a special symbol that tells the compiler/interpreter to perform specific mathematical, logical, or relational operations (e.g., `+`, `-`, `==`, `&&`).",
    "what is an expression": "An expression is a combination of variables, constants, operators, and function calls that evaluates to a single value (e.g., `5 + 3` evaluates to `8`).",
    "what is a statement": "A statement is a complete instruction in code that performs an action (e.g., variable assignment `x = 5`, or print call `print(x)`).",
    "what is a function": "A function is a reusable block of code that accepts inputs (parameters), performs a specific computation, and optionally returns a result.",
    "what is a parameter": "A parameter is a variable defined in a function's definition that acts as a placeholder for values passed into the function.",
    "what is an argument": "An argument is the actual value or expression passed into a function when it is called.",
    "what is a loop": "A loop is a control structure that repeatedly executes a block of code while a specified condition evaluates to true or across a sequence of items.",
    "what is a condition": "A condition is a boolean expression (evaluating to `True` or `False`) used by control structures like `if` statements and loops to direct program flow.",
    "what is an if statement": "An `if` statement executes a block of code only if its associated boolean condition evaluates to `True`.",
    "what is an else statement": "An `else` statement specifies a block of code to run when the preceding `if` condition evaluates to `False`.",
    "what is a nested loop": "A nested loop is a loop inside another loop. The inner loop executes all its iterations for each single iteration of the outer loop.",
    "what is recursion": "Recursion is a programming technique where a function calls itself to solve smaller instances of the same problem until a base condition is met.",
    "what is debugging": "Debugging is the process of identifying, analyzing, and resolving bugs, syntax errors, or logical flaws in software code.",
    "what is an error": "An error is a fault or unexpected condition in a program that prevents it from compiling, running, or producing the intended output.",
    "what is a syntax error": "A syntax error occurs when code violates the grammar or structural rules of the programming language, preventing parsing or compilation.",
    "what is a runtime error": "A runtime error occurs while the program is actively executing (e.g., dividing by zero or accessing an out-of-bounds array index).",
    "what is a logical error": "A logical error occurs when code runs without crashing but produces incorrect or unintended results due to flawed logic.",
    "what is testing": "Testing is the process of evaluating software to verify that it meets requirements and behaves correctly under various conditions.",
    "compiler vs interpreter": "A **Compiler** translates the entire source code into machine code all at once before execution (e.g., C, C++). An **Interpreter** translates and executes source code line-by-line at runtime (e.g., Python, JavaScript).",

    # --- Python Domain ---
    "what is python": "Python is a high-level, interpreted programming language known for its clear, readable syntax, dynamic typing, and massive library ecosystem.",
    "why is python popular": "Python is popular due to its beginner-friendly syntax, versatility across Data Science, Web Development, Automation, and AI, and its vibrant global developer community.",
    "what is python used for": "Python is widely used for Artificial Intelligence, Machine Learning, Data Analysis, Web Development (Django/Flask), Automation scripting, and Scientific Computing.",
    "who uses python": "Python is used by top organizations like Google, NASA, Netflix, Instagram, Spotify, and academic researchers worldwide.",
    "is python easy to learn": "Yes! Python's syntax closely resembles natural English, making it one of the easiest and most readable programming languages for beginners to learn.",
    "what are python features": "Python features include clean syntax, dynamic typing, automatic memory management (garbage collection), extensive standard library support, and cross-platform compatibility.",
    "what are python applications": "Python applications include Web Development, Machine Learning, Data Science, Web Scraping, Game Development, Network Scripting, and Desktop GUIs.",
    "what is a python variable": "In Python, a variable is created the moment you assign a value to a name without declaring an explicit data type. Example:\n```python\nname = 'Alice'\nage = 25\n```",
    "how do i create a variable": "You create a Python variable by typing a name, an equals sign `=`, and a value:\n```python\nx = 10\nmessage = 'Hello World'\n```",
    "what are python data types": "Python's core data types include:\n- **Numeric**: `int`, `float`, `complex`\n- **Sequence**: `str`, `list`, `tuple`, `range`\n- **Mapping**: `dict`\n- **Set**: `set`, `frozenset`\n- **Boolean**: `bool` (`True`/`False`)\n- **NoneType**: `None`",
    "what is int": "`int` represents whole numbers (positive, negative, or zero) without decimals in Python, e.g., `x = 42`.",
    "what is float": "`float` represents real numbers with a decimal point in Python, e.g., `pi = 3.14159`.",
    "what is string": "A string (`str`) in Python is an immutable sequence of Unicode characters surrounded by single or double quotes, e.g., `greeting = 'Hello'`.",
    "what is boolean": "A boolean (`bool`) represents one of two values: `True` or `False`. Used primarily in conditional statements.",
    "what is list": "A list in Python is an ordered, mutable (changeable) collection of elements defined with square brackets, e.g., `fruits = ['apple', 'banana', 'cherry']`.",
    "what is tuple": "A tuple in Python is an ordered, immutable (unchangeable) collection defined with parentheses, e.g., `coordinates = (10.0, 20.0)`.",
    "what is set": "A set in Python is an unordered collection of unique elements defined with curly braces, e.g., `unique_ids = {1, 2, 3}`.",
    "what is dictionary": "A dictionary (`dict`) in Python is an ordered collection of key-value pairs defined with curly braces, e.g., `user = {'name': 'Alice', 'age': 30}`.",
    "what is none": "`None` is a special Python constant used to represent the absence of a value or a null value.",
    "what is type conversion": "Type conversion (or type casting) is the process of converting a variable from one data type to another, e.g., `int('5')` converts string `'5'` to integer `5`.",
    "what is casting": "Casting in Python means manually specifying a data type using constructor functions like `int()`, `float()`, or `str()`. Example: `x = float(5)` gives `5.0`.",
    "what is input": "The `input()` function prompts the user for text entry in the console and returns it as a string. Example: `name = input('Enter your name: ')`.",
    "what is print": "The `print()` function outputs text or values to the console. Example: `print('Hello, Python!')`.",
    "what is if": "The `if` statement evaluates a condition and executes code if the condition is `True`.\n```python\nif score >= 50:\n    print('Pass')\n```",
    "what is elif": "`elif` (short for else if) tests additional conditions if preceding `if` conditions evaluate to `False`.",
    "what is else": "`else` executes a block of code if all preceding `if` and `elif` conditions evaluate to `False`.",
    "what is for loop": "A `for` loop iterates over a sequence (such as a list, tuple, string, or range):\n```python\nfor i in range(3):\n    print(i)\n# Output: 0, 1, 2\n```",
    "what is while loop": "A `while` loop repeatedly executes code as long as its condition remains `True`:\n```python\ncount = 0\nwhile count < 3:\n    print(count)\n    count += 1\n```",
    "what is break": "The `break` statement immediately terminates the innermost loop and resumes execution after the loop.",
    "what is continue": "The `continue` statement skips the rest of the current iteration and jumps to the next iteration of the loop.",
    "what is pass": "The `pass` statement is a null statement used as a placeholder when code is syntactically required but no action is needed.",
    "what is range": "The `range()` function generates an immutable sequence of numbers. Example: `range(1, 5)` yields numbers 1, 2, 3, 4.",
    "how do i define a function": "In Python, functions are defined using the `def` keyword followed by the function name and parentheses:\n```python\ndef greet(name):\n    return f'Hello, {name}!'\n```",
    "what is return": "The `return` statement exits a function and sends back a specified value to the function caller.",
    "what is lambda": "A `lambda` function is a small anonymous single-expression function in Python:\n```python\nsquare = lambda x: x ** 2\nprint(square(4)) # 16\n```",
    "what is a module": "A module is a single Python file (`.py`) containing reusable code, functions, and classes that can be imported into other scripts.",
    "what is a package": "A package is a directory containing multiple Python modules along with an `__init__.py` file.",
    "what is import": "The `import` keyword loads external or standard library modules into your Python script. Example: `import math`.",
    "what is exception handling": "Exception handling in Python allows programs to gracefully catch and handle runtime errors without crashing using `try`, `except`, and `finally` blocks.",
    "what is try": "The `try` block contains code that might raise an exception.",
    "what is except": "The `except` block handles specific exceptions raised within the corresponding `try` block.",
    "what is finally": "The `finally` block executes regardless of whether an exception occurred or was caught in the `try` block.",
    "what is class": "A class is a blueprint or template for creating objects in Object-Oriented Programming, encapsulating data and methods.",
    "what is object": "An object is a specific instance of a class containing concrete state (attributes) and behavior (methods).",
    "what is inheritance": "Inheritance allows a child class to inherit attributes and methods from a parent class, promoting code reuse.",

    # --- Python Lists Deep-Dive ---
    "explain list creation": "Create a list using square brackets `[]` or the `list()` constructor:\n```python\nnumbers = [1, 2, 3, 4]\nempty_list = []\n```",
    "explain list indexing": "Python list elements are indexed starting at 0:\n```python\ncolors = ['red', 'green', 'blue']\nprint(colors[0]) # Output: 'red'\n```",
    "explain negative indexing": "Negative indexing accesses elements starting from the end (-1 is the last element):\n```python\ncolors = ['red', 'green', 'blue']\nprint(colors[-1]) # Output: 'blue'\n```",
    "explain list slicing": "Slicing extracts a sublist using `list[start:stop:step]`:\n```python\nnums = [0, 1, 2, 3, 4]\nprint(nums[1:4]) # Output: [1, 2, 3]\n```",
    "explain append": "`append()` adds a single element to the end of a list:\n```python\nitems = [1, 2]\nitems.append(3) # items is now [1, 2, 3]\n```",
    "explain insert": "`insert(index, element)` places an item at a specific position:\n```python\nitems = ['a', 'c']\nitems.insert(1, 'b') # ['a', 'b', 'c']\n```",
    "explain remove": "`remove(value)` removes the first matching value from the list:\n```python\nitems = ['a', 'b', 'c']\nitems.remove('b') # ['a', 'c']\n```",
    "explain pop": "`pop(index)` removes and returns the item at a given index (defaults to the last item):\n```python\nitems = [10, 20, 30]\nlast = items.pop() # returns 30, items is [10, 20]\n```",
    "explain sort": "`sort()` sorts the list items in-place in ascending order:\n```python\nnums = [3, 1, 4, 2]\nnums.sort() # nums is now [1, 2, 3, 4]\n```",
    "explain reverse": "`reverse()` reverses the order of elements in-place:\n```python\nnums = [1, 2, 3]\nnums.reverse() # [3, 2, 1]\n```",
    "explain len": "`len(collection)` returns the total number of items in a list, string, dictionary, or tuple:\n```python\nprint(len([10, 20, 30])) # Output: 3\n```",
    "explain list iteration": "Iterate through list elements using a `for` loop:\n```python\nfor item in ['apple', 'banana']:\n    print(item)\n```",
    "explain nested lists": "A nested list is a list containing other lists (like a 2D matrix):\n```python\nmatrix = [[1, 2], [3, 4]]\nprint(matrix[0][1]) # Output: 2\n```",
    "explain list comprehension": "List comprehension provides a concise syntax for creating lists from existing iterables:\n```python\nsquares = [x**2 for x in range(5)] # [0, 1, 4, 9, 16]\n```",

    # --- Python Dictionaries Deep-Dive ---
    "explain dictionary creation": "Create a dictionary using curly braces `{}` with key-value pairs:\n```python\nstudent = {'name': 'John', 'age': 20, 'grade': 'A'}\n```",
    "explain keys": "Keys in a dictionary are unique identifiers used to store and access values. They must be immutable types (strings, numbers, tuples).",
    "explain values": "Values in a dictionary are the associated data stored under keys. Values can be of any data type and can be duplicate.",
    "explain key value pairs": "Key-value pairs link a unique key to a specific value: `'name': 'John'`. Access values using key notation: `student['name']`.",
    "explain get": "The `get(key, default)` method returns the value for a key if present, avoiding `KeyError` if the key is missing:\n```python\nprint(student.get('age', 0)) # 20\n```",
    "explain update": "The `update()` method merges another dictionary or key-value pairs into the current dictionary:\n```python\nstudent.update({'age': 21, 'city': 'NY'})\n```",
    "explain keys method": "`dict.keys()` returns a view object containing all keys in the dictionary:\n```python\nfor k in student.keys():\n    print(k)\n```",
    "explain values method": "`dict.values()` returns a view object containing all values in the dictionary.",
    "explain items method": "`dict.items()` returns key-value tuples for iteration:\n```python\nfor key, val in student.items():\n    print(key, '->', val)\n```",
    "explain dictionary iteration": "Iterate over dictionary keys, values, or items using `for key, value in d.items()`.",
    "explain nested dictionaries": "A nested dictionary contains other dictionaries as values:\n```python\nusers = {'user1': {'name': 'Alice'}, 'user2': {'name': 'Bob'}}\n```",

    # --- Python Object-Oriented Programming (OOP) ---
    "explain oop": "Object-Oriented Programming (OOP) is a paradigm based on objects containing data (attributes) and code (methods). The **4 Pillars of OOP** are:\n1. **Encapsulation**: Bundling data and methods into a class.\n2. **Abstraction**: Hiding internal implementation details.\n3. **Inheritance**: Creating child classes from parent classes.\n4. **Polymorphism**: Allowing different objects to respond to the same method call.",
    "what is oop": "Object-Oriented Programming (OOP) is a paradigm based on objects containing data (attributes) and code (methods). The **4 Pillars of OOP** are:\n1. **Encapsulation**: Bundling data and methods into a class.\n2. **Abstraction**: Hiding internal implementation details.\n3. **Inheritance**: Creating child classes from parent classes.\n4. **Polymorphism**: Allowing different objects to respond to the same method call.",
    "pillars of oop": "The **4 Pillars of OOP** are:\n1. **Encapsulation**: Bundling data and methods into a class.\n2. **Abstraction**: Hiding internal complexity and exposing clean interfaces.\n3. **Inheritance**: Inheriting attributes and methods from parent classes.\n4. **Polymorphism**: Using a common interface for entities of different types.",
    "pillar of oop": "The **4 Pillars of OOP** are:\n1. **Encapsulation**: Bundling data and methods into a class.\n2. **Abstraction**: Hiding internal complexity and exposing clean interfaces.\n3. **Inheritance**: Inheriting attributes and methods from parent classes.\n4. **Polymorphism**: Using a common interface for entities of different types.",
    "explain constructor": "A constructor is a special method called automatically when an instance of a class is created. In Python, it is `__init__`.",
    "explain init": "`__init__` is Python's constructor method used to initialize an object's instance variables upon creation:\n```python\nclass Person:\n    def __init__(self, name):\n        self.name = name\n```",
    "explain self": "`self` represents the instance of the class currently being operated on, allowing access to instance attributes and methods.",
    "explain method": "A method is a function defined inside a class that operates on instances of that class.",
    "explain instance variable": "An instance variable is unique to each object instance, defined using `self.variable_name` inside methods.",
    "explain class variable": "A class variable is shared among all instances of a class, defined directly within the class body outside methods.",
    "explain encapsulation": "Encapsulation bundles data (attributes) and methods operating on that data within a class while restricting direct external access to internal implementation details.",
    "explain polymorphism": "Polymorphism allows objects of different classes to respond to the same method call in their own specific way.",
    "explain abstraction": "Abstraction hides complex implementation details and exposes only necessary public interfaces to the user.",

    # --- HTML Domain ---
    "what is html": "HTML (HyperText Markup Language) is the standard markup language used to structure web pages and web applications.",
    "what does html stand for": "HTML stands for **HyperText Markup Language**.",
    "what is an html tag": "An HTML tag is markup syntax enclosed in angle brackets `<tagname>` used to define elements (e.g., `<p>`, `<a>`, `<div>`).",
    "what is an html element": "An HTML element consists of an opening tag, content, and a closing tag (e.g., `<p>Hello World</p>`).",
    "what is an html attribute": "An HTML attribute provides additional properties or configuration to an HTML element (e.g., `href='index.html'` or `class='btn'`).",
    "what is a heading": "HTML headings are created with `<h1>` to `<h6>` tags, where `<h1>` represents the highest priority header and `<h6>` the lowest.",
    "what is a paragraph": "A paragraph element is defined using the `<p>` tag to contain text blocks with automatic margin spacing.",
    "what is a link": "A hyperlink in HTML is created using the `<a>` (anchor) tag with the `href` attribute: `<a href='https://example.com'>Click Here</a>`.",
    "what is an image": "An image is embedded in HTML using the `<img>` tag with `src` (source path) and `alt` (alternate text) attributes: `<img src='pic.jpg' alt='Description'>`.",
    "what is a form": "A web form is created using the `<form>` tag to collect user input through input fields, checkboxes, radio buttons, and submit buttons.",
    "what is a table": "An HTML table structures tabular data using `<table>`, `<tr>` (table row), `<th>` (header cell), and `<td>` (data cell).",
    "what is a list": "HTML supports ordered lists (`<ol>`) for numbered items and unordered lists (`<ul>`) for bullet points, containing list item (`<li>`) tags.",
    "what is ordered list": "An ordered list (`<ol>`) displays items with sequential numbers or letters.",
    "what is unordered list": "An unordered list (`<ul>`) displays items with bullet points.",
    "what is div": "`<div>` is a generic block-level container element used to group HTML elements for styling or layout control.",
    "what is span": "`<span>` is an inline container element used to mark up a part of a text or document for specific inline styling.",
    "what is semantic html": "Semantic HTML uses meaningful structural elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`) rather than generic `<div>` tags to improve accessibility and SEO.",
    "what is header": "The `<header>` tag represents introductory content or navigation links at the top of a page or section.",
    "what is footer": "The `<footer>` tag contains footer content such as copyright information, links, and contact details.",
    "what is nav": "The `<nav>` tag defines a block of major navigation links.",
    "what is section": "The `<section>` tag defines a standalone thematic section within a web document.",
    "what is article": "The `<article>` tag represents a self-contained composition intended to be independently reusable (e.g., blog post or news story).",
    "what is main": "The `<main>` tag specifies the dominant, primary content of the `<body>` of a document.",
    "what is input": "The `<input>` element creates interactive form fields (e.g., `type='text'`, `type='password'`, `type='checkbox'`).",
    "what is button": "The `<button>` tag creates a clickable button used in forms or with JavaScript event handlers.",
    "what is textarea": "The `<textarea>` element defines a multi-line text input control.",
    "what is select": "The `<select>` element creates a drop-down menu containing `<option>` elements.",
    "what is option": "The `<option>` tag defines an selectable item inside a `<select>` drop-down element.",
    "what is label": "The `<label>` element represents a caption for a form control, enhancing usability and screen-reader accessibility.",
    "what is placeholder": "The `placeholder` attribute displays temporary hint text inside an input field before a user types a value.",
    "what is id": "The `id` attribute provides a unique identifier for an HTML element within a document.",
    "what is class attribute": "The `class` attribute assigns one or more CSS class names to an element for styling or JavaScript manipulation.",
    "what is href": "`href` (Hypertext Reference) specifies the target URL destination for an anchor link (`<a>`).",
    "what is src": "`src` (Source) specifies the file path or URL for external media resources like images (`<img>`) or scripts (`<script>`).",
    "what is alt": "`alt` (Alternate Text) provides descriptive text for images if they fail to load, crucial for web accessibility.",
    "explain html document structure": "An HTML5 document starts with `<!DOCTYPE html>`, followed by `<html>`, containing `<head>` (metadata, title, stylesheet links) and `<body>` (visible page content).",

    # --- CSS Domain ---
    "what is css": "CSS (Cascading Style Sheets) is a stylesheet language used to specify the presentation, visual design, layout, and responsiveness of HTML web pages.",
    "what does css stand for": "CSS stands for **Cascading Style Sheets**.",
    "why is css used": "CSS separates content (HTML) from visual presentation, allowing developers to design clean, consistent, and responsive web user interfaces.",
    "what is a css selector": "A CSS selector targets specific HTML elements to apply styling rules (e.g., element, class, or ID selectors).",
    "what is an element selector": "An element selector targets all elements of a given tag name (e.g., `p { color: blue; }`).",
    "what is a class selector": "A class selector targets elements with a specific `class` attribute using a dot prefix (e.g., `.btn { background: green; }`).",
    "what is an id selector": "An ID selector targets a single element with a specific `id` attribute using a hash prefix (e.g., `#main-header { font-size: 24px; }`).",
    "what is the universal selector": "The universal selector (`*`) matches every single HTML element on the page (e.g., `* { box-sizing: border-box; }`).",
    "what is color": "The `color` property sets the text color of an element (e.g., `color: #333;` or `color: rgb(0,0,255);`).",
    "what is background": "The `background` property sets background colors, images, gradients, or repeat behavior for an element.",
    "what is font-size": "`font-size` specifies the size of text (e.g., `16px`, `1.2rem`, or `100%`).",
    "what is font-family": "`font-family` sets the font typeface for text with fallback options (e.g., `font-family: Arial, sans-serif;`).",
    "what is margin": "`margin` clears space *outside* the border of an element, separating it from adjacent elements.",
    "what is padding": "`padding` clears space *inside* the border of an element, between the content and the border.",
    "what is border": "`border` sets the line surrounding an element's padding and content (e.g., `border: 1px solid #ccc;`).",
    "what is width": "`width` sets the horizontal size of an element (e.g., `width: 100%;` or `width: 300px;`).",
    "what is height": "`height` sets the vertical size of an element (e.g., `height: 200px;`).",
    "what is display": "The `display` property determines how an element is rendered in the document layout (e.g., `block`, `inline`, `inline-block`, `flex`, `grid`, `none`).",
    "what is block": "A block element takes up the full available width and starts on a new line (e.g., `<div>`, `<p>`, `<h1>`).",
    "what is inline": "An inline element takes up only as much width as its content requires and does not force a new line (e.g., `<span>`, `<a>`).",
    "what is inline-block": "An `inline-block` element flows inline with surrounding text but accepts custom `width` and `height` properties.",
    "what is flexbox": "Flexbox (Flexible Box Layout) is a 1D CSS layout model designed to distribute space and align items along a single row or column.",
    "what is css grid": "CSS Grid is a powerful 2D layout system that arranges items into custom rows and columns simultaneously.",
    "what is position": "The `position` property determines how an element is located on the page (`static`, `relative`, `absolute`, `fixed`, `sticky`).",
    "what is responsive design": "Responsive web design ensures web pages render beautifully across all screen sizes and devices (desktops, tablets, mobile phones).",
    "what is media query": "A media query (`@media`) applies CSS rules selectively based on device capabilities, such as screen width (e.g., `@media (max-width: 768px)`).",
    "what is hover": "The `:hover` pseudo-class applies styles when the user hovers a mouse cursor over an element.",
    "what is transition": "The `transition` property allows CSS property changes to animate smoothly over a specified duration.",
    "what is box model": "The CSS Box Model describes the rectangular boxes generated for elements, consisting of 4 layers: **Content**, **Padding**, **Border**, and **Margin**.",

    # --- JavaScript Domain ---
    "what is javascript": "JavaScript is a lightweight, dynamic, compiled/interpreted programming language primarily used to add client-side interactivity, logic, and dynamic content to web pages.",
    "why is javascript used": "JavaScript enables interactive features like form validation, smooth animations, DOM manipulation, asynchronous data fetching (`fetch`/AJAX), and full-stack development via Node.js.",
    "what is a variable in javascript": "In JavaScript, variables store data values declared using `let`, `const`, or `var`.",
    "what is let": "`let` declares a block-scoped variable in JavaScript that can be reassigned.",
    "what is const": "`const` declares a block-scoped constant variable in JavaScript that cannot be reassigned after initialization.",
    "what is var": "`var` declares a function-scoped or globally-scoped variable in traditional JavaScript (prone to hoisting issues, `let`/`const` are preferred).",
    "difference between let and var": "`let` is **block-scoped** and cannot be re-declared in the same scope. `var` is **function-scoped** and can be re-declared.",
    "what is an arrow function": "An arrow function is a concise syntax for writing JavaScript functions introduced in ES6:\n```javascript\nconst add = (a, b) => a + b;\n```",
    "what is an array": "An array in JavaScript is an ordered list of values enclosed in square brackets:\n```javascript\nconst colors = ['red', 'green', 'blue'];\n```",
    "what is an object": "An object in JavaScript is a collection of key-value properties enclosed in curly braces:\n```javascript\nconst user = { name: 'Alice', age: 25 };\n```",
    "what is dom": "The DOM (Document Object Model) is a programming interface representing an HTML document as a tree structure of objects that JavaScript can dynamically inspect and modify.",
    "what is an event": "An event is an action or occurrence that happens in the browser (e.g., `click`, `keydown`, `load`, `submit`).",
    "what is event listener": "An `addEventListener` attaches an event handler function to an HTML element without overwriting existing event handlers:\n```javascript\nbtn.addEventListener('click', () => alert('Clicked!'));\n```",
    "what is getelementbyid": "`document.getElementById('id')` retrieves a single HTML element matching the specified unique ID attribute.",
    "what is queryselector": "`document.querySelector('selector')` returns the first element matching a CSS selector string.",
    "what is json": "JSON (JavaScript Object Notation) is a lightweight text-based data format used for storing and exchanging data between client and server.",
    "what is localstorage": "`localStorage` is a Web Storage API that saves key-value data in the browser with no expiration time.",
    "what is sessionstorage": "`sessionStorage` saves data for the duration of the current browser tab session (cleared when tab closes).",
    "what is fetch": "The `fetch()` API provides a modern asynchronous JavaScript interface for making network HTTP requests to servers.",

    # --- SQL & Database Concepts (GeeksforGeeks DBMS Coverage) ---
    "what is sql": "SQL (Structured Query Language) is the standard domain-specific language used for managing and querying Relational Database Management Systems (RDBMS).",
    "what is dbms": "A Database Management System (DBMS) is software that enables users to create, store, organize, retrieve, update, and manage data efficiently in a database while ensuring security and integrity. Examples: MySQL, PostgreSQL, Oracle, SQLite.",
    "what is rdbms": "An RDBMS (Relational Database Management System) stores data in structured tables composed of rows and columns, enforcing relationships using primary and foreign keys. Examples: PostgreSQL, MySQL, MS SQL Server.",
    "what is database": "A database is an organized collection of structured data stored electronically for rapid search, retrieval, and management.",
    "what is table": "A database table is a structured collection of related data organized in horizontal rows (records) and vertical columns (fields).",
    "what is row": "A row (or record) represents a single data entry item inside a database table.",
    "what is column": "A column (or field) represents a specific attribute or data element maintained across table rows.",
    "what is primary key": "A Primary Key is a column (or set of columns) that uniquely identifies each row in a table. It cannot contain `NULL` values and must contain unique values.",
    "what is a primary key": "A Primary Key is a column (or set of columns) that uniquely identifies each row in a table. It cannot contain `NULL` values and must contain unique values.",
    "what is foreign key": "A Foreign Key is a column in one table that references the Primary Key of another table, establishing a referential integrity link between them.",
    "what is a foreign key": "A Foreign Key is a column in one table that references the Primary Key of another table, establishing a referential integrity link between them.",
    "what is unique key": "A Unique Key constraint ensures all values in a column are distinct, but unlike a Primary Key, it allows one `NULL` value.",
    "what is super key": "A Super Key is a set of one or more attributes that collectively identify a tuple/row uniquely within a table relation.",
    "what is candidate key": "A Candidate Key is a minimal super key—a minimal set of attributes that uniquely identifies a row without redundant fields.",
    "what is composite key": "A Composite Key is a primary key made up of two or more columns combined together to uniquely identify a record.",
    "explain acid properties": "The **ACID Properties** ensure database transaction reliability:\n- **Atomicity**: All operations in a transaction succeed or all fail (all-or-nothing).\n- **Consistency**: Database transitions from one valid state to another, preserving constraints.\n- **Isolation**: Concurrent transactions execute independently without interfering with each other.\n- **Durability**: Committed changes persist permanently even after system crashes.",
    "what are acid properties": "The **ACID Properties** ensure database transaction reliability:\n- **Atomicity**: All operations in a transaction succeed or all fail (all-or-nothing).\n- **Consistency**: Database transitions from one valid state to another, preserving constraints.\n- **Isolation**: Concurrent transactions execute independently without interfering with each other.\n- **Durability**: Committed changes persist permanently even after system crashes.",
    "explain ddl": "DDL (Data Definition Language) commands define and alter database schema structure:\n- `CREATE`: Creates tables/databases.\n- `ALTER`: Modifies table structure.\n- `DROP`: Deletes objects permanently.\n- `TRUNCATE`: Removes all records from a table.",
    "what is ddl": "DDL (Data Definition Language) commands define and alter database schema structure:\n- `CREATE`: Creates tables/databases.\n- `ALTER`: Modifies table structure.\n- `DROP`: Deletes objects permanently.\n- `TRUNCATE`: Removes all records from a table.",
    "explain dml": "DML (Data Manipulation Language) commands modify database data:\n- `INSERT`: Adds new records.\n- `UPDATE`: Modifies existing rows.\n- `DELETE`: Removes specified records.",
    "what is dml": "DML (Data Manipulation Language) commands modify database data:\n- `INSERT`: Adds new records.\n- `UPDATE`: Modifies existing rows.\n- `DELETE`: Removes specified records.",
    "explain dcl": "DCL (Data Control Language) commands manage permissions and user rights:\n- `GRANT`: Gives user access permissions.\n- `REVOKE`: Withdraws user permissions.",
    "what is dcl": "DCL (Data Control Language) commands manage permissions and user rights:\n- `GRANT`: Gives user access permissions.\n- `REVOKE`: Withdraws user permissions.",
    "explain tcl": "TCL (Transaction Control Language) commands manage database transactions:\n- `COMMIT`: Saves transaction changes permanently.\n- `ROLLBACK`: Restores database state before transaction.\n- `SAVEPOINT`: Sets a checkpoint within a transaction.",
    "what is tcl": "TCL (Transaction Control Language) commands manage database transactions:\n- `COMMIT`: Saves transaction changes permanently.\n- `ROLLBACK`: Restores database state before transaction.\n- `SAVEPOINT`: Sets a checkpoint within a transaction.",
    "what is er diagram": "An Entity-Relationship (ER) Diagram visually models a database structure using:\n- **Entities** (Rectangles): Real-world objects (e.g., Student, Course).\n- **Attributes** (Ovals): Properties of entities (e.g., Name, ID).\n- **Relationships** (Diamonds): Connections between entities (e.g., Enrolls_In).",
    "what is a view": "A View in SQL is a virtual table based on the result-set of an SQL statement. It does not store physical data itself but provides a dynamic window over actual tables.",
    "what is a trigger": "A Trigger is a stored database procedure that automatically executes (fires) when a specified event (`INSERT`, `UPDATE`, `DELETE`) occurs on a table.",
    "what is a stored procedure": "A Stored Procedure is a prepared batch of SQL statements saved in the database that can be executed repeatedly with input/output parameters.",
    "what is bcnf": "BCNF (Boyce-Codd Normal Form) is a stricter version of 3NF. A table is in BCNF if for every functional dependency $X \\rightarrow Y$, $X$ is a super key.",
    "what is 1nf": "1NF (First Normal Form) requires atomic cell values (no arrays/lists inside cells) and unique records.",
    "what is 2nf": "2NF (Second Normal Form) requires 1NF compliance and no partial functional dependencies (non-key attributes depend on whole primary key).",
    "what is 3nf": "3NF (Third Normal Form) requires 2NF compliance and no transitive functional dependencies (non-key attributes depend *only* on primary key).",
    "what is clustered index": "A Clustered Index alters the physical order of data rows in a table to match the index key order. Each table can have only one clustered index.",
    "what is non clustered index": "A Non-Clustered Index creates a separate structure containing index key values and row pointers to physical table data. A table can have multiple non-clustered indexes.",
    "clustered index vs non clustered index": "Clustered vs Non-Clustered Index:\n- **Clustered Index**: Determines the physical order of data in the table. Only 1 allowed per table. Faster data retrieval.\n- **Non-Clustered Index**: Stores pointers to actual table data in a separate index structure. Multiple allowed per table.",
    "what is functional dependency": "A Functional Dependency ($X \\rightarrow Y$) expresses a constraint where attribute set $X$ uniquely determines attribute set $Y$ in a relation.",
    "what is concurrency control": "Concurrency Control in DBMS ensures simultaneous execution of transactions without data inconsistency or race conditions, using mechanisms like Lock-Based Protocols and Timestamp Ordering.",
    "what is select": "The `SELECT` statement retrieves columns/data from one or more database tables:\n```sql\nSELECT name, age FROM users WHERE age > 18;\n```",
    "what is from": "The `FROM` clause specifies the database table(s) from which to retrieve data.",
    "what is where": "The `WHERE` clause filters table records based on a specified condition.",
    "what is order by": "The `ORDER BY` clause sorts returned query results in ascending (`ASC`) or descending (`DESC`) order.",
    "what is group by": "The `GROUP BY` clause groups rows sharing equal values into summary rows, often used with aggregate functions.",
    "what is having": "The `HAVING` clause filters grouped summary records after `GROUP BY` aggregation (unlike `WHERE` which filters before grouping).",
    "what is limit": "The `LIMIT` clause restricts the maximum number of rows returned by a query.",
    "what is distinct": "The `DISTINCT` keyword eliminates duplicate rows from query results (`SELECT DISTINCT country FROM users;`).",
    "what is insert": "The `INSERT INTO` statement adds new records to a table:\n```sql\nINSERT INTO users (name, age) VALUES ('Alice', 25);\n```",
    "what is update": "The `UPDATE` statement modifies existing records in a table:\n```sql\nUPDATE users SET age = 26 WHERE name = 'Alice';\n```",
    "what is delete": "The `DELETE FROM` statement removes records from a table:\n```sql\nDELETE FROM users WHERE age < 18;\n```",
    "what is create": "The `CREATE TABLE` statement creates a new database table structure.",
    "what is alter": "The `ALTER TABLE` statement modifies an existing table structure (adding, dropping, or renaming columns).",
    "what is drop": "The `DROP TABLE` statement completely deletes a table and all its stored data from the database.",
    "what is join": "A `JOIN` clause combines rows from two or more tables based on a related column between them.",
    "what is inner join": "`INNER JOIN` returns only records that have matching values in both joined tables.",
    "what is left join": "`LEFT JOIN` (or LEFT OUTER JOIN) returns all records from the left table, and matching records from the right table.",
    "what is right join": "`RIGHT JOIN` returns all records from the right table, and matching records from the left table.",
    "what is full join": "`FULL JOIN` (or FULL OUTER JOIN) returns all records when there is a match in either left or right table.",
    "what is aggregate function": "An aggregate function performs a calculation on a set of values and returns a single summary value (e.g., `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).",
    "count": "`COUNT(column)` returns the total number of non-null rows in a column.",
    "sum": "`SUM(column)` calculates the total numerical sum of a column.",
    "avg": "`AVG(column)` calculates the average numerical value of a column.",
    "min": "`MIN(column)` returns the smallest value in a column.",
    "max": "`MAX(column)` returns the largest value in a column.",

    # Database Normalization & Concepts
    "explain normalization": "Database Normalization is the process of organizing table structures to reduce data redundancy and improve data integrity. Main forms:\n- **1NF**: Atomic values, no repeating groups.\n- **2NF**: In 1NF and no partial dependencies.\n- **3NF**: In 2NF and no transitive dependencies.\n- **BCNF**: Strict form of 3NF where all determinants are super keys.",
    "explain first normal form": "1NF requires that table cells hold single atomic values and each record is unique.",
    "explain second normal form": "2NF requires 1NF compliance and that non-key attributes depend on the complete primary key.",
    "explain third normal form": "3NF requires 2NF compliance and that non-key attributes depend *only* on the primary key (no transitive dependencies).",
    "explain data redundancy": "Data Redundancy refers to storing the same piece of data in multiple places unnecessarily, leading to storage waste and update anomalies.",
    "explain data integrity": "Data Integrity ensures data accuracy, consistency, and reliability across database operations.",

    # --- Data Structures & Algorithms ---
    "explain data structure": "A data structure is a specialized format for organizing, processing, retrieving, and storing data efficiently in computer memory.",
    "explain array": "An array is a linear data structure storing elements of the same type in contiguous memory locations accessed by index.",
    "explain linked list": "A linked list is a linear data structure where elements (nodes) contain data and a pointer/reference to the next node in the sequence.",
    "explain stack": "A Stack is a LIFO (Last-In, First-Out) linear data structure supporting `push()` (add) and `pop()` (remove top element) operations.",
    "explain queue": "A Queue is a FIFO (First-In, First-Out) linear data structure supporting `enqueue()` (add at rear) and `dequeue()` (remove from front) operations.",
    "explain tree": "A Tree is a hierarchical non-linear data structure consisting of nodes connected by edges, starting from a root node.",
    "explain graph": "A Graph is a non-linear data structure composed of vertices (nodes) and edges connecting pairs of vertices.",
    "explain hash table": "A Hash Table (or HashMap) stores key-value pairs using a hash function to map keys to bucket indices for average $O(1)$ lookup time.",
    "explain linear search": "Linear search inspects every element in a list sequentially from start to finish until the target element is found ($O(n)$ time).",
    "explain binary search": "Binary search finds a target value in a **sorted** array by repeatedly dividing the search interval in half ($O(\\log n)$ time).",
    "explain sorting": "Sorting rearranges list elements into a specific order (ascending or descending).",
    "explain bubble sort": "Bubble sort repeatedly steps through a list, compares adjacent elements, and swaps them if they are in the wrong order ($O(n^2)$ time).",
    "explain selection sort": "Selection sort repeatedly finds the minimum element from the unsorted portion and moves it to the beginning ($O(n^2)$ time).",
    "explain insertion sort": "Insertion sort builds the sorted array one item at a time by inserting elements into their correct position ($O(n^2)$ time).",
    "explain time complexity": "Time Complexity measures the total execution time or operations required by an algorithm as a function of input size $n$.",
    "explain space complexity": "Space Complexity measures the total memory space required by an algorithm to run as a function of input size $n$.",
    "explain big o notation": "Big O notation mathematically describes the upper bound or worst-case performance growth rate of an algorithm (e.g., $O(1)$, $O(n)$, $O(n^2)$).",

    # --- CS Fundamentals & Operating Systems ---
    "explain operating system": "An Operating System (OS) is core system software that manages hardware resources (CPU, RAM, storage) and provides services for application programs (e.g., Windows, Linux, macOS).",
    "explain process": "A process is an active instance of a running program executing in memory with dedicated resources.",
    "what is a process": "A process is an active instance of a running program executing in memory with dedicated resources.",
    "explain thread": "A thread is the smallest unit of execution within a process. Multiple threads within a process share memory space.",
    "what is a thread": "A thread is the smallest unit of execution within a process. Multiple threads within a process share memory space.",
    "process vs thread": "A **Process** is an independent executing program with its own memory address space. A **Thread** is a lightweight execution path inside a process sharing the parent process's memory.",
    "explain multitasking": "Multitasking allows an OS to execute multiple tasks/processes concurrently by switching the CPU rapidly between them.",
    "explain multiprocessing": "Multiprocessing utilizes two or more physical CPU cores simultaneously to process separate tasks.",
    "explain scheduling": "CPU scheduling is the OS mechanism that determines which process gets CPU execution time and when.",
    "explain memory management": "Memory management tracks every byte of RAM, allocating memory to programs when requested and freeing it when no longer needed.",
    "explain virtual memory": "Virtual memory uses disk storage as an extension of RAM, allowing the OS to execute programs larger than physical memory.",
    "explain ram": "RAM (Random Access Memory) is fast, volatile primary memory used to store active data and running programs.",
    "explain rom": "ROM (Read-Only Memory) is non-volatile memory storing permanent startup instructions (firmware/BIOS).",
    "explain cache": "Cache is small, high-speed memory located near CPU cores to store frequently accessed data for fast retrieval.",
    "explain file system": "A file system controls how data is stored, organized, and retrieved on storage devices (e.g., NTFS, ext4, FAT32).",
    "explain deadlock": "Deadlock is a situation where two or more processes are blocked forever, each waiting for a resource held by the other.",
    "explain concurrency": "Concurrency means executing multiple task sequences in overlapping time periods.",
    "explain synchronization": "Synchronization controls thread access to shared resources to prevent data corruption and race conditions.",

    # --- Computer Networking ---
    "explain computer network": "A computer network is a collection of interconnected devices sharing resources, data, and services.",
    "explain lan": "LAN (Local Area Network) connects devices within a small geographic area like a home, office, or school building.",
    "explain wan": "WAN (Wide Area Network) spans a large geographic region, connecting multiple LANs across cities or countries (e.g., the Internet).",
    "explain man": "MAN (Metropolitan Area Network) covers a city or town area.",
    "explain pan": "PAN (Personal Area Network) connects personal devices in close range (e.g., Bluetooth).",
    "explain ip address": "An IP Address is a unique numerical label assigned to every device connected to a computer network.",
    "explain ipv4": "IPv4 is a 32-bit address format expressed in 4 dot-separated numbers (e.g., `192.168.1.1`).",
    "explain ipv6": "IPv6 is a 128-bit address format expressed in 8 colon-separated hexadecimal groups, created to replace exhausted IPv4 addresses.",
    "explain mac address": "A MAC Address is a unique 48-bit hardware identifier assigned to a network interface card (NIC) by its manufacturer.",
    "explain router": "A router is a network device that forwards data packets between different computer networks.",
    "explain switch": "A switch connects multiple devices together within a single local network (LAN) using MAC addresses.",
    "explain modem": "A modem converts digital signals from a computer into analog signals suitable for transmission over cables/fiber.",
    "explain dns": "DNS (Domain Name System) translates human-readable domain names (e.g., `google.com`) into numerical IP addresses (`142.250.190.46`).",
    "what is dns": "DNS (Domain Name System) translates human-readable domain names (e.g., `google.com`) into numerical IP addresses (`142.250.190.46`).",
    "explain http": "HTTP (Hypertext Transfer Protocol) is the application-level protocol used to transfer web page data across the Web.",
    "explain https": "HTTPS is the secure version of HTTP that encrypts web communication using SSL/TLS.",
    "explain tcp": "TCP (Transmission Control Protocol) is a reliable connection-oriented transport protocol that guarantees ordered, error-checked packet delivery.",
    "explain udp": "UDP (User Datagram Protocol) is a fast, connectionless transport protocol that sends packets without guaranteeing delivery or packet order (used for video streaming and gaming).",
    "explain port": "A port is a 16-bit number identifying a specific process or network service on a device (e.g., HTTP uses port 80, HTTPS uses 443).",
    "explain client": "A client is a device or application (like a web browser) that requests resources or services from a server.",
    "explain server": "A server is a computer or application that listens for incoming client requests and provides data or services in response.",
    "explain request": "An HTTP request is a message sent by a client to a server asking for an action or resource (containing Method, URL, Headers, Body).",
    "explain response": "An HTTP response is the server's reply containing Status Code (e.g., 200 OK, 404 Not Found), Headers, and Content Payload.",
    "explain url": "A URL (Uniform Resource Locator) is a web address specifying the location of a resource on the Internet.",
    "explain api": "An API (Application Programming Interface) defines set rules allowing different software applications to communicate with each other.",
    "explain rest api": "An REST API (Representational State Transfer API) is an architectural style for designing networked web APIs using standard HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) and JSON payloads.",

    # --- Git & GitHub ---
    "explain git": "Git is a distributed version control system that tracks code changes, allows branch merging, and helps developers collaborate on software projects.",
    "explain github": "GitHub is a cloud-based hosting platform for Git repositories, offering collaboration tools, pull requests, and issue tracking.",
    "explain repository": "A repository (repo) is a storage location containing all project files, commits, and revision history.",
    "explain commit": "A commit is a saved snapshot of your project changes in Git along with a descriptive commit message.",
    "explain branch": "An independent line of development in Git, allowing developers to work on new features without affecting main branch code.",
    "explain merge": "Merging combines changes from one branch into another (e.g., merging a feature branch into `main`).",
    "explain clone": "Cloning creates a local copy of a remote Git repository on your machine.",
    "explain pull": "Fetching and merging changes from a remote repository into your local branch (`git pull`).",
    "explain push": "Uploading your local Git commits to a remote repository (`git push`).",
    "explain pull request": "A Pull Request (PR) is a proposal on GitHub to review and merge code changes from your branch into a target repository.",
    "explain gitignore": "A `.gitignore` file specifies intentionally untracked files and directories that Git should ignore (e.g., `__pycache__`, `.env`).",
    "explain readme": "A `README.md` file provides project overview documentation, installation steps, and usage instructions.",
    "explain version control": "Version Control is system software that records changes to code files over time so specific versions can be recalled later.",

    # --- Basic Educational Questions (Math/Logic) ---
    "explain percentages": "A percentage represents a fraction or ratio expressed as a portion out of 100. Formula: `(part / total) * 100`.",
    "explain averages": "The average (mean) is calculated by adding all numbers in a dataset and dividing by the total count of numbers. Example: average of 2, 4, 6 is `(2+4+6)/3 = 4`.",
    "explain ratios": "A ratio compares two quantities showing how many times one value contains another (e.g., 2:3).",
    "explain simple probability": "Probability measures the likelihood of an event occurring: `P(Event) = (Favorable Outcomes) / (Total Possible Outcomes)`.",
    "explain basic statistics": "Statistics involves collecting, analyzing, summarizing, and interpreting numerical data (using metrics like Mean, Median, Mode, and Range).",
    "explain basic logical reasoning": "Logical reasoning applies formal rules of deduction and inference to draw valid conclusions from given premises or conditions.",

    # --- Comparisons ---
    "python vs java": "Python vs Java:\n- **Python**: Dynamic typing, interpreted, concise readable syntax, excellent for Data Science & AI.\n- **Java**: Static typing, compiled to JVM bytecode, verbose syntax, widely used for enterprise backend systems and Android.",
    "html vs css": "HTML vs CSS:\n- **HTML**: Provides the backbone structure and content elements of a web page.\n- **CSS**: Controls the visual presentation, colors, fonts, layout, and responsive design of HTML elements.",
    "html vs javascript": "HTML vs JavaScript:\n- **HTML**: Defines static page elements and content structure.\n- **JavaScript**: Adds dynamic interactivity, logic, event handling, and data fetching to the web page.",
    "sql vs nosql": "SQL vs NoSQL:\n- **SQL**: Relational databases storing structured data in tables with fixed schemas and ACID compliance (e.g., PostgreSQL, MySQL).\n- **NoSQL**: Non-relational databases storing unstructured/semi-structured data in documents, key-value pairs, or graphs (e.g., MongoDB).",
    "list vs tuple": "List vs Tuple in Python:\n- **List**: Mutable (can add/modify/remove items), defined with `[]`, slightly slower.\n- **Tuple**: Immutable (cannot change after creation), defined with `()`, memory efficient and faster.",
    "stack vs queue": "Stack vs Queue:\n- **Stack**: LIFO (Last-In First-Out) data structure; insertion and deletion happen at the top.\n- **Queue**: FIFO (First-In First-Out) data structure; insertion at rear, deletion at front.",
    "primary key vs foreign key": "Primary Key vs Foreign Key:\n- **Primary Key**: Uniquely identifies a record within its own table (cannot be NULL).\n- **Foreign Key**: References a Primary Key in another table to establish relationships between tables.",
    "dbms vs rdbms": "DBMS vs RDBMS:\n- **DBMS**: Manages data stored as files or hierarchies without enforcing table relationships.\n- **RDBMS**: Manages tabular relational data linked by primary/foreign keys with strict referential integrity.",
    "http vs https": "HTTP vs HTTPS:\n- **HTTP**: Transmits data in plain unencrypted text (port 80).\n- **HTTPS**: Encrypts data transmission using SSL/TLS (port 443) for security.",
    "tcp vs udp": "TCP vs UDP:\n- **TCP**: Connection-oriented protocol providing reliable, ordered packet delivery with error checking.\n- **UDP**: Connectionless protocol providing fast packet streaming without delivery guarantees.",
}

# Key topic definitions lookup table for direct single-word or short phrase requests
TOPIC_KEYWORD_MAP = {
    "python": "what is python",
    "html": "what is html",
    "css": "what is css",
    "javascript": "what is javascript",
    "js": "what is javascript",
    "sql": "what is sql",
    "algorithm": "what is an algorithm",
    "process": "what is a process",
    "thread": "what is a thread",
    "dns": "what is dns",
    "ip": "explain ip address",
    "git": "explain git",
    "github": "explain github",
    "loop": "what is a loop",
    "function": "what is a function",
    "variable": "what is a variable",
    "class": "what is class",
    "object": "what is object",
    "inheritance": "what is inheritance",
    "chatbot": "what is this chatbot",
    "recursion": "what is recursion",
    "array": "explain array",
    "stack": "explain stack",
    "queue": "explain queue",
    "database": "what is database",
    "dbms": "what is dbms",
    "rdbms": "what is rdbms",
    "acid": "explain acid properties",
    "bcnf": "what is bcnf",
    "ddl": "explain ddl",
    "dml": "explain dml",
    "dcl": "explain dcl",
    "tcl": "explain tcl",
}

def retrieve_local_answer(message: str, session_context: Optional[dict] = None) -> Optional[Tuple[str, str]]:
    """
    Main local KB match pipeline:
    1. Normalize text (lowercase, contractions, typos, punctuation removal).
    2. Direct match in KB_EXACT.
    3. Topic phrase alias mapping ("explain python", "pillars of oop", "pillar of oops").
    4. Follow-up pronoun resolution using session_context.
    5. Fuzzy match for close spellings.
    """
    norm = normalize_text(message)
    if not norm:
        return None, None

    # 1. Direct exact match in KB_EXACT
    if norm in KB_EXACT:
        return KB_EXACT[norm], norm.split()[-1]

    # 2. Key phrase prefix matching (e.g. "explain python" -> "what is python")
    if norm.startswith("explain "):
        target_topic = norm[8:].strip()
        if target_topic in TOPIC_KEYWORD_MAP:
            mapped_key = TOPIC_KEYWORD_MAP[target_topic]
            if mapped_key in KB_EXACT:
                return KB_EXACT[mapped_key], target_topic

    # 3. Check single topic keyword (e.g. "python", "html", "process", "acid")
    if norm in TOPIC_KEYWORD_MAP:
        mapped_key = TOPIC_KEYWORD_MAP[norm]
        if mapped_key in KB_EXACT:
            return KB_EXACT[mapped_key], norm

    # 4. Check word-boundary matched keys in KB_EXACT
    for key, ans in KB_EXACT.items():
        if len(key) > 4:
            pattern = r'\b' + re.escape(key) + r'\b'
            if re.search(pattern, norm):
                return ans, key.split()[-1]

    # 5. Handle follow-up pronouns ("it", "this", "example", "why is it popular") using session_context
    if session_context and session_context.get("last_topic"):
        last_topic = session_context["last_topic"]
        if any(w in norm for w in ["it", "this", "example", "why", "code", "explain more", "how"]):
            if last_topic in TOPIC_KEYWORD_MAP:
                mapped_key = TOPIC_KEYWORD_MAP[last_topic]
                if mapped_key in KB_EXACT:
                    return KB_EXACT[mapped_key], last_topic

    # 6. Fuzzy match using difflib for near-matches
    best_match = None
    best_score = 0.0
    for key, ans in KB_EXACT.items():
        score = difflib.SequenceMatcher(None, norm, key).ratio()
        if score > 0.75 and score > best_score:
            best_score = score
            best_match = ans

    if best_match:
        return best_match, "general"

    # 7. Check if user is asking for interview questions
    if "interview" in norm:
        return (
            "Here are some common technical interview questions from GeeksforGeeks you can practice:\n"
            "1. 'What are ACID properties in DBMS?'\n"
            "2. 'What is the difference between DDL, DML, DCL, and TCL?'\n"
            "3. 'What is the difference between Primary Key, Foreign Key, and Super Key?'\n"
            "4. 'What are the 4 Pillars of OOP?'\n"
            "5. 'What is BCNF and how is it different from 3NF?'\n"
            "6. 'What is the difference between Clustered and Non-Clustered Index?'\n"
            "Feel free to ask me to explain any of these!",
            "interview"
        )

    return None, None


def get_varied_fallback() -> str:
    """Returns a friendly, polite fallback response listing available topics."""
    return (
        "I don't have a predefined answer for that specific question yet. "
        "However, I am happy to help you with programming and CS topics! "
        "You can ask me about **Python**, **HTML**, **CSS**, **JavaScript**, **DBMS / SQL**, "
        "**ACID Properties**, **OOP Pillars**, **Data Structures**, **Networking**, **Git**, or **Operating Systems**."
    )
