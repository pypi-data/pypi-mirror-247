# TODO: LLMEvalTemplate
evaluation_steps_template = """
You will be given 4 blocks of text labelled "Input", "Actual output", "Expected output", and "Context". Generate 3-4 concise evaluation steps based on the criteria below. Explicitly state to ignore any blocks of text that is not mentioned in the evaluation criteria.

Criteria:
{criteria}

**
IMPORTANT: Please make sure to only return in JSON format, with the "steps" key as a list of strings. No words or explaination is needed.
**

JSON:
"""

evaluation_results_template = """
Evaluation Steps:
{evaluation_steps}

Text:
{text}

Given the evaluation steps, please evaluate the provided Text. Some fields in text might be unavailable and will be labelled "N/A". Only return a JSON with two keys: 1) a `score` key ranging from 0 - 10, with 10 being that it follows the criteria and 0 being that it does not, and 2) a `reason` key, a reason for the given score. Be extra harsh and give as low a score as possible as it designed to penalize.

**
IMPORTANT: Please make sure to only return in JSON format, with the "score" and "reason" key. No words or explaination is needed.
**

JSON:
"""

# TODO: summarization template
closed_end_questions_template = """
Based on the text below, please generate {n} closed-ended questions that can be answered with either a 'yes' or 'no'. Only return a JSON with a 'questions' key, which is a list of strings. The questions have to be STRICTLY closed ended.

Text:
{text}

JSON:
"""

closed_end_answers_template = """
Based on the given text, please provide either a 'yes', 'no', or 'idk' answer to the question presented. Only answer 'idk' IF the the answer cannot be deduced from the given text.

Question:
{question}

Text:
{text}

Answer:
"""


class FaithfulnessTemplate:
    @staticmethod
    def generate_truths(text):
        return f"""Based on the given text, please generate a comphrensive list of undisputed "truths" that can inferred from the provided text. You should NOT incorporate any knowledge you have, and take each truth at face value.

Example text: "Einstein won the noble prize in 1968 for his discovery of the photoelectric effect."
Example truths: ["Einstein won the noble prize for his discovery of the photoelectric effect.", "Einstein won the noble prize in 1968."]

**
IMPORTANT: Please make sure to only return in JSON format, with the "truths" key as a list of strings. No words or explaination is needed.
**

Text:
{text}

JSON:
"""

    @staticmethod
    def generate_verdicts(truths, text):
        return f"""Based on a list of strings, called contexts, please generate a list of JSON objects to indicate whether the given 'actual output' agrees with EACH context. The JSON will have 2 fields: 'verdict' and 'reason'.
The 'verdict' key should STRICTLY be either 'yes', 'no', or 'idk', and states whether the given text agrees with the context. 
The 'reason' is the reason for the verdict. When the answer is 'no' or 'idk', try to provide a correction in the reason.

**
IMPORTANT: Please make sure to only return in JSON format, with the 'verdicts' key as a list of JSON objects.
Example contexts: ["Einstein won the Nobel Prize for his discovery of the photoelectric effect.", "Einstein won the Nobel Prize in 1968."]
Example text: "Einstein won the Nobel Prize in 1969 for his discovery of the photoelectric effect."

Example:
{{
    "verdicts": [
        {{
            "verdict": "yes",
            "reason": "The context states that Einstein won the Nobel Prize for his discovery of the photoelectric effect."
        }},
        {{
            "verdict": "no",
            "reason": "The context states that Einstein won the Nobel Prize in 1968, not 1969."
        }}
    ]  
}}

You should NOT incorporate any prior knowledge you have and take each context at face value. Since you are going to generate a verdict for each context, the number of 'verdicts' SHOULD BE STRICTLY EQUAL to that of contexts.
**

Contexts:
{truths}

Actual Output:
{text}

JSON:
"""

    @staticmethod
    def generate_reason(score, contradiction_reasons):
        return f"""Below is a list of Contradictions. It explains why the 'actual output' does not align with the 'retrieval context'.
Given the faithfulness score, which is a 0-1 score indicating how faithful the `actual output` is the context (higher the better), concisely summarize the contradictions to justify the score. If there are no contradictions, just say something positive with an upbeat tone (but don't overdo it otherwise it gets annoying).

Faithfulness Score:
{score}

Contradictions:
{contradiction_reasons}

Example:
The score is <faithfulness_score> because <your_reason>.

Justification:
"""


class AnswerRelevancyTemplate:
    @staticmethod
    def generate_key_points(answer, retrieval_context):
        return f"""Given the answer text, breakdown and generate a list of key points presented in the answer. In case the answer is ambigious to what it is talking about, you can use the retrieval contexts as additional information for more comphrensive key points. Make the key points concise.

Answer:
{answer}

Retrieval Context:
{retrieval_context}

**
IMPORTANT: Please make sure to only return in JSON format, with the "key_points" key as a list of strings. No words or explaination is needed.
**

JSON:
"""

    @staticmethod
    def generate_verdicts(original_question, key_points):
        return f"""For the provided list of key points, compare each key point with the question. Please generate and list of JSON with two keys: `verdict` and `reason`.
The 'verdict' key should STRICTLY be either a 'yes', 'no', or 'idk'. Answer 'yes' if it makes sense for the key point is relevant as an answer to the question, 'no' if the key point is irrelevant, and 'idk' if it is ambiguous (eg., not directly relevant but could be used as a supporting point to answer the question).
The 'reason' is the reason for the verdict.

**
IMPORTANT: Please make sure to only return in JSON format, with the 'verdicts' key as a list of JSON objects.
Example key points: ["Meditation offers a rich tapestry of benefits that touch upon various aspects of well-being.", "The practice of meditation has been around for centuries, evolving through various cultures and traditions, which underscores its timeless relevance.", "Improved sleep quality is another significant benefit, aiding in overall physical restoration."]

Example:
Question:
What are the primary benefits of meditation?

{{
    "verdicts": [
        {{
            "verdict": "yes",
            "reason": "Addresses the question directly, stating benefits of meditation.",
        }},
        {{
            "verdict": "no",
            "reason": "The historical and cultural origins of meditation is not relevant to the question.",   
        }},
        {{
            "verdict": "yes",
            "reason": "Improved sleep quality is relevant a benefit of meditation.",   
        }}
    ]  
}}

Since you are going to generate a verdict for each question, the number of 'verdicts' SHOULD BE STRICTLY EQUAL to that of `key points`.
**
           
Question:
{original_question}

Key Points:
{key_points}

JSON:
"""

    @staticmethod
    def generate_reason(irrelevant_points, original_question, answer, score):
        return f"""
Given the answer relevancy score, the list of irrelevant points, the list of ambiguous point, and the original question, summarize a CONCISE reason for the score. Explain why it is not higher, but also why it is at its current score.
The irrelevant points represent things in the original answer to the original question that is irrelevant to the question.
If there are nothing irrelevant, just say something positive with an upbeat tone (but don't overdo it otherwise it gets annoying).

Answer Relevancy Score:
{score}

Irrelevant Points:
{irrelevant_points}

Original Question:
{original_question}

Original Answer:
{answer}

Example:
The score is <answer_relevancy_score> because <your_reason>.

Reason:
"""
