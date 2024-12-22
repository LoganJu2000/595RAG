import openai
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = (
    "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"
)
client = OpenAI()


def check_answer_equivalence(question, answer1, answer2, model="gpt-4o-mini"):
    """
    判定两个答案是否等价，基于 GPT 模型的输出。

    :param question: 问题
    :param answer1: 第一个答案
    :param answer2: 第二个答案
    :param model: 使用的 GPT 模型，默认为 gpt-4o-mini
    :return: 是否等价（True 或 False）
    """
    prompt = f"""
    Are the following two answers to the given question equivalent? Do not consider whether the answers are right or wrong, but only whether they are equivalent. Directly state \u201dYes\u201d or \u201dNo\u201d.

    Question: {question}
    Answer 1: {answer1}
    Answer 2: {answer2}

    Are the two answers equivalent?"""
    messages = [
        {"role": "system", "content": f"You are an expert at common sense."},
        {"role": "user", "content": prompt},
    ]
    try:
        response = client.chat.completions.create(model=model, messages=messages)
        output = response.choices[0].message.content.strip()
        if output.lower() == "yes":
            return True
        elif output.lower() == "no":
            return False
        else:
            raise ValueError(f"Unexpected model output: {output}")
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    question = "Which title was conferred to Anna Muzychuk in 2007?"
    answer1 = "Anna Muzychuk was conferred the title of International Master (IM) in 2007. She earned the title by scoring three norms in rapid chess tournaments."
    answer2 = "International Master"

    result = check_answer_equivalence(question, answer1, answer2)
    if result is not None:
        print(f"答案是否等价: {'是' if result else '否'}")
