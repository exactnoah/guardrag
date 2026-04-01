from deepeval.models import OllamaModel
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric

from logger import eval_log_entry

OLLAMA_MODEL = "mistral:7b"

def get_judge_model():
    return OllamaModel(
        model=OLLAMA_MODEL,
        base_url="http://localhost:11434"
    )

def get_metrics(judge_model):
    return [
        FaithfulnessMetric(model=judge_model),
        AnswerRelevancyMetric(model=judge_model),
    ]

def run_evaluation(question, answer, retrieved_docs, print_fn):
    def output(message):
        print_fn(message)
        eval_log_entry(message)
    
    judge_model = get_judge_model()
    metrics = get_metrics(judge_model)

    testcase = LLMTestCase(
        input=question,
        actual_output=answer,
        retrieval_context=[doc.content for doc in retrieved_docs]
    )

    output("\n\nRe-Evaluating Answer...")
    results = evaluate(test_cases=[testcase], metrics=metrics)
    metrics_data = results.test_results[0].metrics_data
    answer_valid = True

    if metrics_data[0].score < 0.75:
        output("\nLikely Hallucinations detected. Please try again with a more specific question or after adding relevant files.")
        output(f"Reasoning: {metrics_data[0].reason}")
        answer_valid = False

    if metrics_data[1].score < 0.75:
        output("\nGenerated Answer may not be relevant to asked question. Please try again with a more specific question or after adding relevant files.")
        output(f"Reasoning: {metrics_data[1].reason}")
        answer_valid = False

    if answer_valid:
        output("\n--- Evaluation Results ---")
        for metric in metrics_data:
            output(f"{metric.name}: {metric.score:.2f}")
            output(f"Reasoning: {metric.reason}")