from latex2sympy2 import latex2sympy
import re
from sympy import simplify
from word2number import w2n


def verify_extraction(extraction):
    extraction = extraction.strip()
    if extraction == "" or extraction == None:
        return False
    return True


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def extract_full_boxed_content(s):
    """
    Extract the full content inside \boxed{}, handling nested braces {{}} properly.
    """
    results = []

    i = 0
    while i < len(s):
        if s[i:i + 7] == r'\boxed{':
            brace_stack = []
            start = i + 7
            i = start

            while i < len(s):
                if s[i] == '{':
                    brace_stack.append(i)
                elif s[i] == '}':
                    if brace_stack:
                        brace_stack.pop()
                    else:
                        results.append(s[start:i])
                        break
                i += 1
        i += 1

    return results


def is_equal(md_ans, gt_ans):

    md_ans = md_ans.lower()
    gt_ans = gt_ans.lower()

    if md_ans.strip() == gt_ans.strip():
        return True

    try:
        md_ans_cache = str(w2n.word_to_num(md_ans))
        if md_ans_cache.strip() == gt_ans.strip():
            return True
    except ValueError:
        pass

    # For Math
    try:
        # Parse LaTeX expressions into sympy and compare numerical values
        md_sympy = latex2sympy(md_ans)
        gt_sympy = latex2sympy(gt_ans)

        # Compare evaluated results, rounded to 2 decimal places
        if round(float(md_sympy.evalf()), 2) == round(float(gt_sympy.evalf()), 2):
            return True

        # Additionally, compare simplified symbolic expressions
        if simplify(md_sympy - gt_sympy) == 0:
            return True
    except Exception:
        pass  # Ignore parsing errors or evaluation failures

    return False


score_demo_prompt = """Please read the following example. Then determine whether the response is correct and type it 
at the end of the prompt. It is worth noting that the final answer in the response is usually in \\boxed{}, 
You only need to compare the final answer in the response with the answer, without considering the logical 
correctness of the response itself.

Response: The correct answer is:\n\nA

Answer: A

Correct_or_not: Correct

Response: The correct option is:\n\n\\[\n\\boxed{E}\n\\]

Answer: C

Correct_or_not: Incorrect
"""