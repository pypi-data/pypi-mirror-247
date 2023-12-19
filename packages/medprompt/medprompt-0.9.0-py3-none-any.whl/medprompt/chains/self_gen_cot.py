from kink import di
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from .. import MedPrompter
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
med_prompter = MedPrompter()

SELF_GENERATED_COT_TEMPLATE = """
## Question: {{question}}
## Answer : {{answer}}
Given the above question and answer, generate a chain of thought explanation for the answer.
First, start with the model generated chain of thought explanation.
End the chain of though explanation with:
Therefore, the answer is {{answer}}.
"""


self_gen_cot_llm = di["self_gen_cot_llm"]

class SelfGenCot(BaseModel):
    question: str = Field(..., title="Question", description="The question to generate a chain of thought for.")
    answer: str = Field(..., title="Answer", description="The answer to generate a chain of thought for.")

def get_runnable(**kwargs):
    """Get the runnable chain."""
    _cot = RunnablePassthrough.assign(
        question = lambda x: x["question"],
        answer = lambda x: x["answer"],
        ) | self_gen_cot_llm | StrOutputParser()
    chain = _cot.with_types(SelfGenCot)
    return chain