
_KEYWORD = "keywords:"

_LANGUAGE = "language:"

_LENGTH = "length_constraints:"

_CONTENT = "detectable_content:"

_FORMAT = "detectable_format:"

_MULTITURN = "multi-turn:"

_COMBINATION = "combination:"

_STARTEND = "startend:"

_CHANGE_CASES = "change_case:"

_PUNCTUATION = "punctuation:"

taxonomy = {

    _KEYWORD + "existence": {
        "args": {
            # TODO
            "keywords": []
        },
        "description": [
            "The response must include the keywords <keywords>",
            "containing keywords \"<keywords>\" in your response",
            "Don't forget to include the keywords <keywords>",
            "Make sure to include the words <keywords>",
            "response should contain the keyword \"<keywords>\"",
            "your reply should Include the keywords <keywords>",
            "Please also include the keywords \"<keywords>\" in the response",
            "use the keywords <keywords>"
        ]
    },
    _KEYWORD + "frequency": {
        "args":{
            "relation": ["at least", "less than"],
            # TODO
            "keyword": '',
            "frequency": [2,3,4] 
        },
        "description": [
            "Make sure to use the word <keyword> <relation> <frequency> times",
            "Mention the word \"<keyword>\" for <relation> <frequency> times",
            "Make sure the word <keyword> appears <relation> <frequency> times",
            "The word <keyword> should appear <relation> <frequency> times in the response",
            "reply should include the word \"<keyword>\" <relation> <frequency> times",
            "there should be <relation> <frequency> occurrences of the word \"<keyword>\" in your response",
            "in the response, the word \"<keyword>\" should appear <relation> <frequency> times in your response",
            "Make sure to use the word <keyword> <relation> <frequency> times"
        ]
    },
    _KEYWORD + "forbidden_words": {
        "args":{
            # TODO
            "forbidden_words": []
        },
        "description": [
            "The word \"<forbidden_words>\" should not appear in your response",
            "answer without using the word \"<forbidden_words>\"",
            "Do not include the keywords: <forbidden_words>",
            "do not say the word \"<forbidden_words>\" in the response",
            "Do not mention the word <forbidden_words>",
            "Avoid using the word <forbidden_words>",
            "Your answer must not include keywords <forbidden_words>",
            "The words <forbidden_words> cannot be in the response"
        ]

    },
    _KEYWORD + "letter_frequency": {
        "args": {
            "let_relation": ["at least", "less than"],
            "letter": ['t','o','c','e','p','l','j','q','n','a','y','i','w','m'],
            "let_frequency": [3,4,5,6,7,8]
        },
        "description": [
            "Contain <let_relation> <let_frequency> letter\"<letter>\" in your response",
            "In your entire response, the letter <letter> should appear <let_relation> <let_frequency> times",
            "The letter <letter> should show up <let_relation> <let_frequency> times",
            "be sure the letter <letter> appears <let_relation> <let_frequency> times in your response",
            "include the letter \"<letter>\" <let_relation> <let_frequency> times",
            "making sure to use the letter \"<letter>\" <let_relation> <let_frequency> times",
            "answer with the letter \"<letter>\" appearing <let_relation> <let_frequency> times",
            "The letter <letter> must appear <let_relation> <let_frequency> times in the reply"

        ]
    },
    _LANGUAGE + "response_language": {
        "args": {
            "language": ['bn','kn','pa','mr','fa','vi','ko','sw','ru','hi','bg','pt','te','it','ar','ta','fi','ne','ur','th','gu','de']
        },
        "description": [
            "Outside of <language>, no other language is allowed throughout your entire response",
            "Please respond using only the <language> language, no other language is allowed",
            "response should be entirely in <language>, no other language is allowed",
            "Please respond to me only in <language>",
            "using only <language>, no other language is allowed"
        ]

    },
    _LENGTH + "number_sentences": {
        "args":{
            "relation": ["at least", "less than"],
            "num_sentences": [3,4,5]
        },
        "description": [
            "Your response should contain <relation> <num_sentences> sentences.",
            "Have <relation> <num_sentences> sentences in your response",
            "Your entire response should include <relation> <num_sentences> sentences.",
            "Please make sure the response <relation> <num_sentences> sentences long",
            "Respond with <relation> <num_sentences> sentences",
            "The number of sentences in your response should be <relation> <num_sentences>",
            "Use <relation> <num_sentences> sentences in your reply",
            "organize your entire response in <relation> <num_sentences> sentences"
        ]       
    },
    _LENGTH + "number_paragraphs": {
        "args": {
            "num_paragraphs": [2,3,4]
        },
        "description": [
            "There should be exactly <num_paragraphs> paragraphs in your response, separated by the markdown divider: ***.",
            "make sure there are exactly <num_paragraphs> sections. Separated the sections by the markdown divider: ***",
            "Please reply in details, and include exactly <num_paragraphs> paragraphs. Separate the paragraphs with ***",
            "Separate your response into <num_paragraphs> parts, where each part is separated with ***",
            "Put the response into at least <num_paragraphs> sections, separated using 3 asterisks ***",
            "I would like for there to be exactly <num_paragraphs> paragraphs each separated by three asterisk symbols (***)",
            "Give me the answer in exactly <num_paragraphs> paragraphs, separated with the markdown divider: ***"
        ]
    },
    _LENGTH + "number_words": {
        "args":{
            "relation": ["at least", "less than"],
            "num_words": [[10, 15, 20], [30, 40, 50, 100]]
        },
        "description": [
            "Respond with <relation> <num_words> words",
            "use <relation> <num_words> words",
            "make sure the response has <relation> <num_words> words",
            "Limit the number of words you use (<relation> <num_words> words)",
            "the total number of words in your response should be <relation> <num_words>",
            "Keep your entire response <relation> <num_words> words or less.",
            "Control the length of your reply. I don't want anything <relation> <num_words> words",
            "answer with <relation> <num_words>"
        ]
    },
    _LENGTH + "nth_paragraph_first_word": {
        "args": {
            # TODO
            "first_word": "",
            "num_paragraphs": [2,3,4],
            "nth_paragraph": {
                1: "first",
                2: "second",
                3: "third",
                4: "fourth",
            },
        },
        "description":[
            "Please reply with exactly <num_paragraphs> paragraphs and separate each paragraph with two new lines. The very <nth_paragraph> paragraph must start with the word \"<first_word>\"",
            "Response should contain exactly <num_paragraphs> paragraphs, and the <nth_paragraph> paragraph must start with the word \"<first_word>\". Separate paragraphs by double line breaks (\"\\n\\n\")",
            "Can you please answer with <num_paragraphs> paragraphs? Make sure that the <nth_paragraph> paragraph starts with the word \"<first_word>\" and that each paragraph is separated by two new lines",
            "answer exactly <num_paragraphs> paragraphs. Use 2 new lines to separate paragraphs. Start the <nth_paragraph> paragraph with the word \"<first_word>\"",
            "Your answer must be exactly <num_paragraphs> paragraphs where paragraphs and only paragraphs are separated by two new lines, as if they were '\\n\\n' in python. The <nth_paragraph> paragraph must start with the word <first_word>",
            "Write exactly <num_paragraphs> paragraphs each separated with two new lines answering this instruction. The <nth_paragraph> paragraph must start with \"<first_word>\"",
            "There should be exactly <num_paragraphs> paragraphs each separated by two new lines in your response. <nth_paragraph> paragraph must start with the word <first_word>" 
        ]
    },
    _CONTENT + "number_placeholders": {
        "args": {
            "num_placeholders":[1,2,3]
        },
        "description": [
            "Make sure to include at least <num_placeholders> placeholder represented by square brackets, such as [address], [name]",
            "Use square brackets for placeholders, like [username1], [username2]. Please include at least <num_placeholders> placeholders in the thread",
            "The response must contain at least <num_placeholders> placeholders represented by square brackets",
            "make sure it contains at least <num_placeholders> placeholders represented by square brackets, such as [name]",
            "Please include at least <num_placeholders> placeholders represented by square brackets, such as [address]",
            "Your answer must also contain at least <num_placeholders> placeholder (an example of a placeholder is [address])",
            "The response must contain at least <num_placeholders> placeholders (e.g., [restaurant])",
            "Your answer must have at least <num_placeholders> placeholders, wrapped in square brackets, such as [author]"
        ]
    },
    _CONTENT + "postscript": {
        "args": {
            "postscript_marker": ['P.P.S','P.S.']
        },
        "description": [
            "At the end of your response, please explicitly add a postscript starting with <postscript_marker>",
            "end it with a post script starting with <postscript_marker>" ,
            "add a postscript starting with <postscript_marker> to the end of your response",
            "Make sure to include a postscript starting with <postscript_marker>",
            "please explicitly add a note starting with <postscript_marker>",
            "End your response with a postscript indicated by <postscript_marker>",
            "You should add a postscript starting with <postscript_marker> at the end of your response",
            "Please finish your answer with a postscript starting with <postscript_marker>"
        ]
    },
    _FORMAT + "number_bullet_lists": {
        "args":{
            "num_bullets": [2,3,4]
        },
        "description": [
            "Your answer must contain exactly <num_bullets> bullet points in the markdown format (use \"* \" to indicate each bullet) such as:\n* This is the first point.\n* This is the second point",
            "Your answer must contain exactly <num_bullets> bullet point in Markdown using the following format:\n* Bullet point one.\n* Bullet point two.\n...",
            "Response must also contain exactly <num_bullets> bullet points in markdown format. Use * to indicate bullets, like:\n* xyz\n* abc\n* opq",
            "Include exactly <num_bullets> bullet points in your response. The bullet points should be in the form of:\n* This is bullet 1\n* This is bullet 2\n...\n",
            "In your entire response make sure to use exactly <num_bullets> bullet points in markdown format. Please use the following bullet point format:\n* Text for bullet 1\n* Text for bullet 2",
            "Your answer must be in the form of exactly <num_bullets> bullet points with the format below:\n* This is bullet point 1\n* This is bullet point 2",
            "Make sure the answer contains exactly <num_bullets> bullet points in markdown format",
            "Answer with exactly <num_bullets> bullet points.\n\nBullet points are indicated by \"* \". For example:\n* Bullet 1\n* Bullet 2\n"

        ]

    },
    _FORMAT + "constrained_response": {
        "args": {},
        "description": [
            "Choose from the following: ('My answer is yes.', 'My answer is no.', 'My answer is maybe.') -- please include the exact phrase in your response.",
            "Answer with exactly one of the following phrases: \"My answer is yes.\", \"My answer is no.\", \"My answer is maybe.\"",
            "your answer must contain one of the following exact phrases: \u201dMy answer is yes.\", \"My answer is no.\", \"My answer is maybe.\"",
            "You should just say \"My answer is yes.\" or \"My answer is no.\" or \"My answer is maybe.\"",
            "answer with one of the following options: \"My answer is yes.\", \"My answer is no.\", \"My answer is maybe.\"",
            "Choose from:\nMy answer is yes.\nMy answer is no.\nMy answer is maybe.\nJust choose one phrase from above as your answer",
            "Your response should be one of the following: \"My answer is yes.\", \"My answer is no.\", \"My answer is maybe.\"",
            "Please choose one of the following phrases to reply: \"My answer is yes.\", \"My answer is no.\", \"My answer is maybe.\""

        ]
    },
    _FORMAT + "number_highlighted_sections": {
        "args": {
            "num_highlights": [1,2,3]
        },
        "description": [
            "Highlight at least <num_highlights> text sections, i.e. *highlighted section*",
            "Highlight at least <num_highlights> sections of your response in markdown such as *highlighted section*",
            "at least <num_highlights> sections should be highlighted with markdown such as *highlighted section*",
            "Make sure to highlight at least <num_highlights> sections in your answer with markdown, i.e. use *highlighted section*",
            "Highlight at least <num_highlights> sections in your answer by starting and ending with \"*\", like: *highlighted text section*",
            "Italicize at least <num_highlights> text parts with markdown (using * to italicize, like *italic text*)",
            "highlight at least <num_highlights> key point by wrapping it with *. For example: *highlighted key point*",
            "You must highlight at least <num_highlights> words or phrases in your response, like *highlighted phrase*"
        ]
    },
    _FORMAT + "multiple_sections": {
        "args": {
            "section_spliter": ['SECTION','Section'],
            "num_sections": [3,4,5]
        },
        "description": [
            "The response must have <num_sections> sections marked with <section_spliter> X",
            "Make sure to include at least <num_sections> sections marking the beginning of each section with '<section_spliter> X'",
            "Your answer should have <num_sections> sections, and each section should start with \"<section_spliter> X\"",
            "The response should have <num_sections> sections, with each section marked with <section_spliter> X",
            "The answer should be in at least <num_sections> sections with each section starting with <section_spliter> X (where X is 1, 2, 3,...)",
            "Your response must contain <num_sections> sections, mark the beginning of each section with <section_spliter> X",
            "Divide your response into <num_sections> sections, and mark each section with <section_spliter> X",
            "reply with <num_sections> sections. Each section should be explicitly noted as <section_spliter> X"
        ]
    },
    _FORMAT + "json_format": {
        "args": {},
        "description": [
            "I want the entire output in JSON format",
            "Your entire output should just contain a JSON block, nothing else",
            "Make sure your entire response is wrapped in JSON format",
            "Wrap the entire output in JSON format",
            "Please use JSON format",
            "Put your entire answer in JSON format",
            "Format your entire output in JSON",
            "Wrap all words into one JSON block"
        ]
    },
    _FORMAT + "title": {
        "args": {},
        "description": [
            "the response must contain a title wrapped in double angular brackets, i.e. <<title>>",
            "Your answer must have a title contained in double angular brackets, such as <<title>>",
            "Please make sure each point have a title wrapped in double angular brackets, i.e. <<title>>",
            "The entire reply should contain a title in double angular brackets, i.e. <<title>>",
            "Include a title wrapped in double angular brackets, i.e. <<title>>",
            "give your answer wrapped in double angular brackets, such as <<your answer>>",
            "provide a title wrapped in double angular brackets in your response, such as <<title>>",
            "Make sure to include a title that is wrapped in double angular brackets, i.e. <<title>>"
        ]
    },
    _COMBINATION + "two_responses": {
        "args": {},
        "description": [
            "Please give exactly two different responses. Separate the responses with 6 asterisk symbols: ******",
            "Provide exactly two anwers separated by ******",
            "Separate your two responses with six asterisks (******).",
            "Give me exactly two different responses. Responses and only responses should be separated by 6 asterisk symbols: ******",
            "Give exactly two different responses, separating them with 6 asterisk symbols (******)",
            "Responses should be separated by 6 asterisk symbols (******)",
            "come up two answers and separate the two answers like below:\nAnswer 1\n******\nAnswer 2\n\n",
            "Offer two different responses and separate them with 6 asterisk symbols \"******\""
        ]
    },
    _COMBINATION + "repeat_prompt": {
        "args": {
            "position": ["end","start"],
            "prompt_to_repeat": ""
        },
        "description": [
            "\nFirst repeat the request word for word without change, then give your answer (1. do not say any words or characters before repeating the request; 2. the request you need to repeat does not include this sentence)",
            "\nYou need to repeat the sentence above first... Do not change any word, just repeat it. Do not say anything before repeating the sentence.",
            "\nFirst repeat the exact request above, then give your answer. Do not say any word before repeating the exact request",
            "\nLet's repeat the request above first, before you say anything or really respond to the request",

            "repeat the exact request below first, then give your response. Do not say any word before repeating the exact request\n",
            "First repeat the request below, word for word without change, then give your answer. Do not say any words or characters before repeating the request below.\n",
            "For the following request, please repeat the request itself exactly as it is, then give your reply. Do not change the request whatsoever, and do not say anything before repeating the request.\n",
            "Before you answer it, just repeat the request below. You need to repeat it exactly as it is. Do not change any word.\n"
        ]
            
    },
    _STARTEND + "end_checker": {
        "args":{
            "end_phrase": ['Is there anything else I can help with?','Hope you agree with me.','Let me know if you have additional questions.','your love, and thanks.','That is all you need!']
        },
        "description": [
            "Finish the response with this exact phrase: <end_phrase> ",
            "The very last sentence of your response should be \"<end_phrase>\"",
            "Your answer must end with the exact phrase \"<end_phrase>\". No other words should follow this phrase",
            "The very end of your response should read \"<end_phrase>\"",
            "I need you to end your response with \"<end_phrase>\"",
            "The very end of your entire response should read exactly like: <end_phrase> ",
            "The response should end with the phrase \"<end_phrase>\",Do not say anything after that",
            "you should end your entire response with the phrase \"<end_phrase>\""
        ]
    },
    _CHANGE_CASES + "capital_word_frequency": {
        "args": {
            "capital_relation": ["at least","less than"],
            "capital_frequency": [1,2,3,4]
        },
        "description": [
            "make sure that words with all capital letters appear <capital_relation> <capital_frequency> times",
            "Use some words in all caps in your response, but those all-caps words should appear <capital_relation> <capital_frequency> times",
            "Add stress words which are capitalized. Limit those stress words for <capital_relation> <capital_frequency> times",
            "Please limit the number of words with all capital letters to <capital_relation> <capital_frequency>",
            "Use words in all capital letters <capital_relation> <capital_frequency> times",
            "the respoinse should include <capital_relation> <capital_frequency> words in all capital letters."
            "In your response, use words with all capital letters <capital_relation> <capital_frequency> times",
            "Respond with <capital_relation> <capital_frequency> words be in all capital letters",
        ]
    },
    _CHANGE_CASES + "english_capital": {
        "args": {},
        "description": [
            "Your answer should be in all capital letters, no lowercase letters allowed",
            "Your entire response should be in English, and in all capital letters",
            "Make sure to only use capital letters in your entire response",
            "Please reply in English and capitalize all your words",
            "Your answer must be in all capital letters and in English",
            "capitalize every letter in your whole response",
            "All letters in your entire response should be capitalized",
            "Make sure your reply is in English and all capital letters"
        ]
    },
    _CHANGE_CASES + "english_lowercase": {
        "args": {},
        "description": [
            "Please ensure that your response is in English, and in all lowercase letters. No capital letters are allowed",
            "Your entire response should be in English and all lower case (no capital letters whatsoever)",
            "All letters in your response must be lower case letters",
            "Response should be in English, and no capital letters are allowed",
            "Make sure the entire response is in English and no capital letters are used",
            "The answer should be in all lowercase letters, with no capitalizations",
            "Answer shoud be written in English, with all letters lowercased.",
            "Answer in lowercase letters only, throughout your entire answer"
        ]
    },
    _PUNCTUATION + "no_comma": {
        "args": {},
        "description": [
            "Do not contain commas in your response",
            "You are not allowed to use any commas in your response",
            "make sure you don't use any commas",
            "Do not include any commas in your response",
            "There should be no commas in your reply",
            "Refrain from using commas in your response",
            "In your response please avoid using commas",
            "response without any commas"
        ]
    },
    _STARTEND + "quotation": {
        "args": {},
        "description": [
            "Wrap the entire response with double quotation marks",
            "put double quotations marks around your whole response",
            "Please wrap your entire reply with double quotation marks",
            "Make sure your entire response is wrapped in double quotation marks",
            "Put your entire response inside double quotation marks",
            "The whole response should be wrapped in double quotes",
            "You need to wrap your entire response in double quotes",
            "Your answer need to be wrapped in double quotes",
        ]
    },


}