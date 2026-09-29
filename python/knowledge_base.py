"""
knowledge_base.py - Master Rule-Based Knowledge Engine for Conversational Chatbot.
Provides comprehensive coverage for OOP, HTML, CSS, JavaScript, Python, Java, SQL, and CS Fundamentals.
Includes robust input normalization, phrase alias mapping, topic detection, and follow-up context tracking.
"""

import re
import difflib
from typing import Dict, Any, Optional, Tuple, List

# ---------- Typo & Keyword Correction Dictionary ----------
TYPO_MAP = {
    "pyhton": "python",
    "pyton": "python",
    "javasript": "javascript",
    "javscript": "javascript",
    "js": "javascript",
    "htmll": "html",
    "htlm": "html",
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
    "intewiew": "interview",
    "intervew": "interview",
    "porcess": "process",
    "thred": "thread",
    "oops": "oop",
    "oops.": "oop",
    "jvaa": "java",
}

# ---------- Contraction & Phrase Shortcuts ----------
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
    "difference between": "vs",
    "different from": "vs",
    "differentiate": "vs",
    "compare": "vs",
}

# ---------- Input Normalization ----------
def normalize_text(text: str) -> str:
    """
    Internal normalization:
    1. Lowercase text.
    2. Expand contractions and key phrases.
    3. Replace common technical typos.
    4. Remove punctuation except spaces and letters/digits.
    5. Collapse repeated spaces and trim.
    """
    if not text:
        return ""
    
    norm = text.lower().strip()
    
    # Expand contractions and phrases
    for key, val in CONTRACTIONS.items():
        norm = re.sub(r'\b' + re.escape(key) + r'\b', val, norm)
        
    # Remove punctuation
    norm = re.sub(r"[^\w\s]", " ", norm)
    
    # Correct typos
    words = norm.split()
    corrected_words = [TYPO_MAP.get(w, w) for w in words]
    norm = " ".join(corrected_words)
    
    # Collapse spaces
    norm = re.sub(r"\s+", " ", norm).strip()
    return norm


# ---------- CANONICAL KNOWLEDGE BASE ----------
# Organized as { concept_id: answer_text }

CANONICAL_ANSWERS: Dict[str, str] = {
    # --- Greetings & Casual ---
    "greeting_hello": "Hello! I am your educational chatbot assistant. Ask me anything about Python, Java, HTML, CSS, JavaScript, OOP, SQL, or Computer Science concepts!",
    "greeting_hi": "Hi there! I am ready to help you prepare for technical interviews and learn programming fundamentals.",
    "greeting_thanks": "You're very welcome! Feel free to ask any follow-up questions.",
    "greeting_bye": "Goodbye! Have a great day and happy coding!",
    "greeting_how_are_you": "I'm doing great! Ready to help you learn programming and interview topics.",

    # --- Project Self-Awareness ---
    "chatbot_self_info": "This is a Conversational Educational Assistant built using standard HTML5, CSS3, Vanilla JavaScript, and a rule-based Python backend. It uses curated pattern matching to deliver fast, accurate explanations without external AI services.",

    # --- OOP KNOWLEDGE DOMAIN ---
    "oop_definition": "Object-Oriented Programming (OOP) is a programming paradigm based on the concept of 'objects' containing data (attributes) and code (methods). The **4 Pillars of OOP** are:\n1. **Encapsulation**: Bundling data and methods into a single class.\n2. **Abstraction**: Exposing essential features while hiding internal complexity.\n3. **Inheritance**: Creating new child classes from existing parent classes for code reuse.\n4. **Polymorphism**: Allowing different objects to respond to the same method call in their own specific way.",
    
    "procedural_vs_oop": "Procedural Programming vs Object-Oriented Programming (OOP):\n- **Procedural**: Focuses on functions and step-by-step procedures operating on global/shared data (e.g., C, Pascal).\n- **OOP**: Focuses on objects encapsulating both data and methods, offering higher modularity, reusability, and access control.",

    "class_concept": "A **Class** is a blueprint or template that defines the attributes (data) and methods (behavior) that objects created from it will possess.",

    "object_concept": "An **Object** is a concrete instance of a class that holds actual values for attributes and can execute methods defined by its class.",

    "class_vs_object": "Class vs Object:\n- **Class**: The abstract blueprint or template (e.g., `Car` definition).\n- **Object**: A real instance created from that blueprint with specific state (e.g., `my_tesla = Car('Red', 'Model 3')`).",

    "attributes_vs_methods": "Attributes vs Methods:\n- **Attributes**: Variables stored inside an object representing its state or properties (e.g., `color`, `speed`).\n- **Methods**: Functions defined within a class that operate on an object's data (e.g., `drive()`, `brake()`).",

    "encapsulation": "Encapsulation is the OOP principle of bundling data (attributes) and methods that operate on that data inside a single unit (class), while restricting direct access to internal details using access modifiers.",

    "data_hiding": "Data Hiding is the practice of concealing internal object states (e.g., using `private` fields in Java or `__private` naming in Python) so external code cannot mutate attributes directly.",

    "encapsulation_vs_abstraction": "Encapsulation vs Abstraction:\n- **Encapsulation**: Hides data within an object to protect internal state (focuses on *how* data is secured).\n- **Abstraction**: Hides implementation complexity to expose simple interfaces (focuses on *what* an object does).",

    "abstraction": "Abstraction is the OOP pillar that hides complex background implementation details and exposes only essential interfaces to the user (e.g., pressing a car accelerator without knowing engine fuel dynamics).",

    "inheritance": "Inheritance allows a new class (child/derived) to acquire properties and behaviors from an existing class (parent/base), promoting code reusability.",

    "inheritance_types": "Common Inheritance Types:\n- **Single**: One child inherits from one parent.\n- **Multilevel**: A child inherits from a parent which inherits from a grandparent.\n- **Multiple**: A child inherits from multiple parent classes (Supported in Python, but restricted in Java using interfaces).\n- **Hierarchical**: Multiple child classes inherit from a single parent.\n- **Hybrid**: A combination of two or more inheritance types.",

    "polymorphism": "Polymorphism ('many forms') allows objects of different classes to be treated as instances of a common superclass, responding to the same method call according to their specific implementations.",

    "overloading_vs_overriding": "Method Overloading vs Method Overriding:\n- **Method Overloading**: Multiple methods in the *same class* share the same name but have different parameter signatures (Compile-Time Polymorphism).\n- **Method Overriding**: A child class provides a specific implementation of a method already defined in its *parent class* (Runtime Polymorphism).",

    "interface_vs_abstract_class": "Interface vs Abstract Class:\n- **Interface**: Defines a pure contract of abstract methods with no state (all methods implicitly public/abstract).\n- **Abstract Class**: Can contain both abstract methods and concrete methods with instance variables.",

    "association_aggregation_composition": "Association, Aggregation, and Composition:\n- **Association**: General relationship between two independent objects.\n- **Aggregation**: 'Has-A' weak relationship where child objects can exist independently of the parent (e.g., Department and Teachers).\n- **Composition**: 'Has-A' strong relationship where child objects cannot exist if the parent is destroyed (e.g., House and Rooms).",

    "is_a_vs_has_a": "IS-A vs HAS-A Relationship:\n- **IS-A**: Based on Inheritance (e.g., `Dog` IS-A `Animal`).\n- **HAS-A**: Based on Composition/Aggregation (e.g., `Car` HAS-A `Engine`).",

    # --- PYTHON KNOWLEDGE DOMAIN ---
    "python_definition": "Python is a high-level, interpreted, dynamically-typed programming language known for its clean, readable syntax and massive ecosystem supporting Web Dev, Data Science, AI, and Automation.",

    "python_features": "Key Python Features:\n1. **Readable Syntax**: Resembles pseudo-code/English.\n2. **Interpreted**: Code is executed line-by-line.\n3. **Dynamically Typed**: Variable types are determined at runtime.\n4. **Extensive Standard Library**: Includes built-in math, file handling, and regex packages.",

    "python_popular": "Python is popular due to its beginner-friendly readability, versatility across AI, Machine Learning, Web Backend (Django/Flask), Data Analysis, and large supportive developer community.",

    "python_execution": "Python is an **Interpreted** language. Source code (`.py`) is compiled into bytecode (`.pyc`) by the Python interpreter and executed line-by-line by the Python Virtual Machine (PVM).",

    "python_indentation": "Python uses **Indentation** (whitespace) to define code blocks (loops, functions, classes) instead of curly braces `{}`. Proper indentation is mandatory to avoid `IndentationError`.",

    "python_dynamic_typing": "Dynamic Typing means you do not declare variable types explicitly in Python; the interpreter determines the data type dynamically at runtime based on assigned values (`x = 10` is an integer).",

    "python_datatypes": "Core Python Data Types:\n- **Numeric**: `int`, `float`, `complex`\n- **Sequence**: `str`, `list`, `tuple`, `range`\n- **Mapping**: `dict`\n- **Set**: `set`, `frozenset`\n- **Boolean**: `bool` (`True`/`False`)\n- **NoneType**: `None`",

    "python_mutability": "Mutable vs Immutable Objects in Python:\n- **Mutable**: Values can be changed after creation (`list`, `dict`, `set`).\n- **Immutable**: Values cannot be changed once created (`int`, `float`, `str`, `tuple`, `frozenset`).",

    "python_list": "A **List** in Python is an ordered, mutable sequence defined with square brackets: `fruits = ['apple', 'banana', 'cherry']`.",

    "python_tuple": "A **Tuple** in Python is an ordered, immutable sequence defined with parentheses: `point = (10, 20)`.",

    "python_list_vs_tuple": "List vs Tuple in Python:\n- **List**: Mutable (can append/modify), defined with `[]`, slightly higher memory footprint.\n- **Tuple**: Immutable (cannot modify after creation), defined with `()`, faster and memory efficient.",

    "python_set": "A **Set** in Python is an unordered collection of unique, immutable elements defined with curly braces: `ids = {1, 2, 3}`.",

    "python_dict": "A **Dictionary** in Python is an ordered collection of key-value pairs: `person = {'name': 'Alice', 'age': 25}`.",

    "python_list_comprehension": "List Comprehension provides a concise syntax for creating lists from iterables: `squares = [x**2 for x in range(5)]`.",

    "python_args_kwargs": "*args and **kwargs in Python:\n- `*args`: Passes a variable number of positional arguments as a tuple.\n- `**kwargs`: Passes a variable number of keyword arguments as a dictionary.",

    "python_lambda": "A **Lambda** is an anonymous single-expression function in Python: `add = lambda a, b: a + b`.",

    "python_exceptions": "Exception Handling in Python uses `try` (risky code), `except` (error handling), `else` (runs if no exception), and `finally` (always runs):",

    "python_is_vs_equals": "`is` vs `==` in Python:\n- `==`: Checks if two variables have equal **values**.\n- `is`: Checks if two variables point to the exact same **memory object identity**.",

    # --- JAVA KNOWLEDGE DOMAIN ---
    "java_definition": "Java is an object-oriented, class-based, statically-typed programming language designed to be platform-independent ('Write Once, Run Anywhere').",

    "java_platform_independent": "Java is platform-independent because Java source code (`.java`) is compiled by `javac` into bytecode (`.class`), which runs on any operating system equipped with a **Java Virtual Machine (JVM)**.",

    "java_jdk_jre_jvm": "JDK vs JRE vs JVM:\n- **JVM (Java Virtual Machine)**: Executes Java bytecode line-by-line on target OS.\n- **JRE (Java Runtime Environment)**: Contains JVM + core runtime libraries needed to *run* Java apps.\n- **JDK (Java Development Kit)**: Contains JRE + development tools (`javac`, debugger) needed to *write* Java apps.",

    "java_access_modifiers": "Java Access Modifiers:\n- `public`: Accessible anywhere.\n- `private`: Accessible only within the same class.\n- `protected`: Accessible in the same package and subclasses.\n- `default`: Accessible only within the same package.",

    "java_string_stringbuilder": "String vs StringBuilder vs StringBuffer in Java:\n- `String`: Immutable sequence of characters.\n- `StringBuilder`: Mutable and fast, but not thread-safe.\n- `StringBuffer`: Mutable and thread-safe (synchronized).",

    "java_exceptions": "Checked vs Unchecked Exceptions in Java:\n- **Checked Exceptions**: Verified at compile-time (e.g., `IOException`, `SQLException`); must be handled with `try-catch` or `throws`.\n- **Unchecked Exceptions**: Occur at runtime (e.g., `NullPointerException`, `ArrayIndexOutOfBoundsException`).",

    "java_collections": "Java Collections Framework core interfaces:\n- **List**: Ordered collection with duplicates allowed (`ArrayList`, `LinkedList`).\n- **Set**: Unordered collection with unique elements (`HashSet`, `TreeSet`).\n- **Map**: Key-value pairs (`HashMap`, `TreeMap`).",

    # --- HTML KNOWLEDGE DOMAIN ---
    "html_definition": "HTML (HyperText Markup Language) is the standard markup language used to structure and present content on web pages.",

    "html_not_programming": "HTML is a **Markup Language**, not a programming language, because it structures page content using tags rather than executing logic, loops, or algorithms.",

    "html5": "HTML5 is the latest HTML standard introducing native multimedia elements (`<audio>`, `<video>`), dynamic graphic elements (`<canvas>`, `<svg>`), and semantic structural tags (`<header>`, `<nav>`, `<article>`).",

    "html_tag_vs_element": "HTML Tag vs Element vs Attribute:\n- **Tag**: Bracketed keyword opening/closing markup (e.g., `<p>`).\n- **Element**: Opening tag + content + closing tag (e.g., `<p>Hello</p>`).\n- **Attribute**: Additional configuration inside an opening tag (e.g., `<img src='pic.jpg'>`).",

    "html_semantic": "Semantic HTML uses structural tags with clear meaning (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`) to improve code readability, accessibility, and SEO.",

    "html_div_vs_span": "div vs span in HTML:\n- `<div>`: Block-level element that starts on a new line and occupies full width.\n- `<span>`: Inline element that wraps inline text without breaking layout.",

    "html_block_vs_inline": "Block vs Inline Elements in HTML:\n- **Block**: Occupies 100% width, starts on a new line (`<div>`, `<p>`, `<h1>`, `<form>`).\n- **Inline**: Occupies only content width, stays on same line (`<span>`, `<a>`, `<img>`, `<b>`).",

    # --- CSS KNOWLEDGE DOMAIN ---
    "css_definition": "CSS (Cascading Style Sheets) is a stylesheet language used to specify visual styling, layout formatting, colors, fonts, and responsiveness for HTML web pages.",

    "css_types": "3 Ways to Apply CSS:\n1. **Inline**: Using `style` attribute directly on element (`<h1 style='color:red;'>`).\n2. **Internal**: Using `<style>` block in HTML `<head>`.\n3. **External**: Linking separate `.css` file via `<link rel='stylesheet' href='style.css'>` (Best Practice).",

    "css_box_model": "The CSS Box Model consists of 4 layers surrounding content:\n1. **Content**: Text or images.\n2. **Padding**: Transparent space *inside* border.\n3. **Border**: Border line around padding.\n4. **Margin**: Transparent space *outside* border.",

    "css_margin_vs_padding": "Margin vs Padding:\n- **Margin**: Space *outside* the border of an element.\n- **Padding**: Space *inside* the border, between content and border.",

    "css_flexbox_vs_grid": "Flexbox vs CSS Grid:\n- **Flexbox**: 1D layout system designed for aligning items along a single row or column.\n- **CSS Grid**: 2D layout system designed for complex multi-row and multi-column grid layouts.",

    "css_positioning": "CSS Position Property:\n- `static`: Default flow positioning.\n- `relative`: Positioned relative to its normal place.\n- `absolute`: Positioned relative to nearest non-static ancestor.\n- `fixed`: Positioned relative to viewport (stays fixed on scroll).\n- `sticky`: Toggles between relative and fixed based on scroll position.",

    # --- JAVASCRIPT KNOWLEDGE DOMAIN ---
    "js_definition": "JavaScript is a lightweight, dynamic, multi-paradigm scripting language used to create interactive, dynamic web applications.",

    "js_var_let_const": "var vs let vs const in JavaScript:\n- `var`: Function-scoped, hoisted, re-assignable, re-declarable.\n- `let`: Block-scoped, re-assignable, cannot be re-declared in same scope.\n- `const`: Block-scoped, immutable assignment (cannot be reassigned).",

    "js_equality": "== vs === in JavaScript:\n- `==` (Abstract Equality): Compares values *after* implicit type coercion (`'5' == 5` is `true`).\n- `===` (Strict Equality): Compares both **value and data type** (`'5' === 5` is `false`).",

    "js_hoisting": "Hoisting is JavaScript's default behavior of moving variable and function declarations to the top of their containing scope during compilation.",

    "js_closures": "A Closure is a function bundled together with references to its surrounding lexical environment, allowing an inner function to access variables from an outer function even after the outer function has returned.",

    "js_dom": "The DOM (Document Object Model) is a tree-structure programming interface representing an HTML document so JavaScript can dynamically access, modify, and style elements.",

    "js_async_promises": "Asynchronous JavaScript (Promises & async/await):\n- **Promises**: Objects representing eventual completion/failure of an async operation.\n- **async/await**: Syntactic sugar over Promises allowing asynchronous code to be written sequentially.",

    # --- COMPARISON MATRIX ---
    "java_vs_javascript": "Java vs JavaScript:\n- **Java**: Statically-typed compiled language running on JVM, used for enterprise backends and Android.\n- **JavaScript**: Dynamically-typed scripting language running in browsers/Node.js, used for web interactivity.",

    "python_vs_java": "Python vs Java:\n- **Python**: Dynamic typing, concise readable syntax, rapid prototyping, popular for AI & Data Science.\n- **Java**: Static typing, verbose syntax, compiled to bytecode, popular for enterprise scale and Android.",

    "html_vs_css": "HTML vs CSS:\n- **HTML**: Provides the structural content and backbone of a web page.\n- **CSS**: Provides visual presentation, colors, layout, and styling.",
}

# ---------- PHRASE ALIAS MAPPING ----------
# Maps patterns and keyword variations to canonical concept keys

ALIAS_RULES: List[Tuple[List[str], str]] = [
    # OOP & Pillars
    (["oop", "oops", "object oriented programming", "pillars of oop", "pillar of oop", "4 pillars"], "oop_definition"),
    (["procedural vs oop", "difference between procedural and oop", "procedural programming vs oop"], "procedural_vs_oop"),
    (["class", "what is class", "class in oop"], "class_concept"),
    (["object", "what is object", "object in oop"], "object_concept"),
    (["class vs object", "difference between class and object", "object vs class"], "class_vs_object"),
    (["attributes vs methods", "attribute vs method"], "attributes_vs_methods"),
    (["encapsulation", "what is encapsulation"], "encapsulation"),
    (["data hiding", "what is data hiding"], "data_hiding"),
    (["encapsulation vs abstraction", "abstraction vs encapsulation"], "encapsulation_vs_abstraction"),
    (["abstraction", "what is abstraction"], "abstraction"),
    (["inheritance", "what is inheritance"], "inheritance"),
    (["types of inheritance", "inheritance types", "single inheritance", "multilevel inheritance"], "inheritance_types"),
    (["polymorphism", "what is polymorphism"], "polymorphism"),
    (["overloading vs overriding", "method overloading vs method overriding", "overriding vs overloading"], "overloading_vs_overriding"),
    (["interface vs abstract class", "abstract class vs interface"], "interface_vs_abstract_class"),
    (["association aggregation composition", "aggregation vs composition", "composition vs aggregation"], "association_aggregation_composition"),
    (["is a vs has a", "has a vs is a"], "is_a_vs_has_a"),

    # Python
    (["python", "what is python", "explain python", "python language"], "python_definition"),
    (["python features", "features of python", "characteristics of python"], "python_features"),
    (["why python", "why is python popular", "advantages of python", "python advantages"], "python_popular"),
    (["python execution", "is python interpreted", "how python executes"], "python_execution"),
    (["indentation", "python indentation", "why indentation in python"], "python_indentation"),
    (["dynamic typing", "what is dynamic typing"], "python_dynamic_typing"),
    (["python datatypes", "datatypes in python", "python data types"], "python_datatypes"),
    (["mutable vs immutable", "immutable vs mutable"], "python_mutability"),
    (["python list", "list in python", "what is list"], "python_list"),
    (["python tuple", "tuple in python", "what is tuple"], "python_tuple"),
    (["list vs tuple", "tuple vs list"], "python_list_vs_tuple"),
    (["python set", "set in python"], "python_set"),
    (["python dictionary", "dictionary in python", "dict in python"], "python_dict"),
    (["list comprehension", "explain list comprehension"], "python_list_comprehension"),
    (["args kwargs", "args and kwargs", "*args", "**kwargs"], "python_args_kwargs"),
    (["lambda", "lambda python", "python lambda"], "python_lambda"),
    (["exception handling in python", "python try except"], "python_exceptions"),
    (["is vs ==", "== vs is python", "is vs equals"], "python_is_vs_equals"),

    # Java
    (["java", "what is java", "explain java"], "java_definition"),
    (["platform independent", "why java platform independent", "java platform independence"], "java_platform_independent"),
    (["jdk jre jvm", "jvm vs jre vs jdk", "difference between jdk jre jvm"], "java_jdk_jre_jvm"),
    (["access modifiers in java", "java access modifiers", "public private protected"], "java_access_modifiers"),
    (["string vs stringbuilder", "stringbuilder vs stringbuffer"], "java_string_stringbuilder"),
    (["checked vs unchecked exception", "java checked exception"], "java_exceptions"),
    (["java collections", "collections framework in java"], "java_collections"),

    # HTML
    (["html", "what is html", "explain html"], "html_definition"),
    (["is html programming language", "is html a programming language"], "html_not_programming"),
    (["html5", "what is html5", "html vs html5"], "html5"),
    (["html tag vs element", "tag vs element"], "html_tag_vs_element"),
    (["semantic html", "what is semantic html"], "html_semantic"),
    (["div vs span", "span vs div"], "html_div_vs_span"),
    (["block vs inline", "inline vs block"], "html_block_vs_inline"),

    # CSS
    (["css", "what is css", "explain css"], "css_definition"),
    (["types of css", "inline internal external css"], "css_types"),
    (["css box model", "box model in css", "box model"], "css_box_model"),
    (["margin vs padding", "padding vs margin"], "css_margin_vs_padding"),
    (["flexbox vs grid", "grid vs flexbox"], "css_flexbox_vs_grid"),
    (["css position", "positioning in css", "relative vs absolute"], "css_positioning"),

    # JavaScript
    (["javascript", "what is javascript", "explain javascript"], "js_definition"),
    (["var let const", "let vs var", "var vs let", "let vs const"], "js_var_let_const"),
    (["== vs ===", "=== vs =="], "js_equality"),
    (["hoisting", "what is hoisting"], "js_hoisting"),
    (["closure", "closures", "what is closure"], "js_closures"),
    (["dom", "what is dom", "dom in js"], "js_dom"),
    (["async await", "promises in js", "js async promises"], "js_async_promises"),

    # Comparisons
    (["java vs javascript", "javascript vs java"], "java_vs_javascript"),
    (["python vs java", "java vs python"], "python_vs_java"),
    (["html vs css", "css vs html"], "html_vs_css"),
]


# ---------- MATCHING & RETRIEVAL ENGINE ----------

def retrieve_local_answer(message: str, session_context: Optional[dict] = None) -> Optional[Tuple[str, str]]:
    """
    Rule-based matching pipeline:
    1. Normalize input string.
    2. Check exact matches & alias rules.
    3. Handle follow-ups using session context.
    4. Return (answer_string, topic_key).
    """
    norm = normalize_text(message)
    if not norm:
        return None, None

    # Check for direct greeting or chatbot self info
    if norm in ["hello", "hi", "hey", "greetings"]:
        return CANONICAL_ANSWERS["greeting_hello"], "greeting"
    if norm in ["bye", "goodbye", "see you"]:
        return CANONICAL_ANSWERS["greeting_bye"], "goodbye"
    if norm in ["thanks", "thank you", "thx"]:
        return CANONICAL_ANSWERS["greeting_thanks"], "thanks"
    if norm in ["how are you", "how r u"]:
        return CANONICAL_ANSWERS["greeting_how_are_you"], "greeting"
    if any(p in norm for p in ["what is this chatbot", "how does this chatbot work", "technologies used"]):
        return CANONICAL_ANSWERS["chatbot_self_info"], "chatbot"

    # Alias pattern matching
    for keywords, concept_key in ALIAS_RULES:
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, norm):
                if concept_key in CANONICAL_ANSWERS:
                    return CANONICAL_ANSWERS[concept_key], concept_key

    # Check follow-up context
    if session_context and session_context.get("last_topic"):
        last_topic = session_context["last_topic"]
        if any(w in norm for w in ["advantages", "benefits", "example", "why", "code", "explain more", "difference"]):
            if last_topic in CANONICAL_ANSWERS:
                return CANONICAL_ANSWERS[last_topic], last_topic

    # Fuzzy match threshold
    best_match_key = None
    best_score = 0.0
    for keywords, concept_key in ALIAS_RULES:
        for kw in keywords:
            score = difflib.SequenceMatcher(None, norm, kw).ratio()
            if score > 0.80 and score > best_score:
                best_score = score
                best_match_key = concept_key

    if best_match_key and best_match_key in CANONICAL_ANSWERS:
        return CANONICAL_ANSWERS[best_match_key], best_match_key

    return None, None


def get_varied_fallback() -> str:
    """Returns polite fallback listing available topics."""
    return (
        "I don't have a predefined answer for that specific question yet. "
        "However, I can help you with **Python**, **Java**, **HTML**, **CSS**, **JavaScript**, "
        "**OOP (4 Pillars)**, **SQL / DBMS**, **Data Structures**, or **Operating Systems** concepts!"
    )
