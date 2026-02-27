# Evaluation Framework

## Overview

The evaluation framework provides comprehensive metrics to assess RAG system performance across retrieval quality, generation quality, and efficiency.

## Metrics

### Retrieval Metrics

**Recall** (`retrieval_recall.py`)
- Measures: What fraction of relevant documents were retrieved?
- Formula: `|retrieved ∩ relevant| / |relevant|`
- Score: 0-1 (higher is better)
- Use case: Assessing retriever effectiveness

**Precision**
- Measures: What fraction of retrieved documents are relevant?
- Formula: `|retrieved ∩ relevant| / |retrieved|`
- Score: 0-1 (higher is better)
- Use case: Avoiding irrelevant context

### Generation Metrics

**Faithfulness** (`faithfulness.py`)
- Measures: How closely does the answer adhere to provided context?
- Approach: NLI-based entailment checking
- Score: 0-1 (higher is better)
- Use case: Preventing hallucinations

**Relevance**
- Measures: How well does the answer address the query?
- Approach: Semantic similarity between answer and query
- Score: 0-1 (higher is better)
- Use case: Answer quality assurance

### System Metrics

**Latency** (`latency.py`)
- Measures: End-to-end response time
- Unit: Milliseconds
- Threshold: < 2000ms (configurable)
- Use case: Performance monitoring

**Throughput**
- Measures: Queries processed per second
- Unit: QPS
- Use case: Capacity planning

## Datasets

### Golden Datasets (`evaluation/datasets/`)
- Format: Query-Document pairs with ground truth relevance labels
- Structure: JSON/CSV with fields:
  - `query`: User question
  - `relevant_docs`: List of document IDs
  - `expected_answer`: Ground truth response
- Usage: Held-out test set for evaluation

### Custom Datasets
Add your evaluation datasets to `data/evaluation/`:
```
data/evaluation/
├── dataset_v1.json
├── dataset_v2.json
└── human_annotations.csv
```

## Quality Thresholds

Configured in `ci/thresholds.yaml`:

```yaml
thresholds:
  faithfulness:
    min: 0.75
  retrieval_recall:
    min: 0.80
  latency:
    max: 2000
```

## Running Evaluation

### Programmatic

```python
from evaluation.evaluator import Evaluator

evaluator = Evaluator(metrics=['faithfulness', 'retrieval_recall', 'latency'])
results = evaluator.evaluate(predictions)
```

### Pipeline

```bash
python -m pipelines.run_evaluation \
  --dataset data/evaluation/test.json \
  --output results/eval_2026_01_13.json
```

### CI/CD

Evaluation runs automatically on push to `main`:
```bash
# See .github/workflows/evaluation.yml
```

## Interpretation Guide

| Metric | Score | Interpretation |
|--------|-------|-----------------|
| Faithfulness | > 0.85 | Excellent - minimal hallucination |
| Faithfulness | 0.70-0.85 | Good - acceptable hallucination rate |
| Faithfulness | < 0.70 | Poor - high hallucination |
| Recall | > 0.85 | Excellent - finding most relevant docs |
| Recall | 0.70-0.85 | Good - missing some relevant docs |
| Recall | < 0.70 | Poor - missing many relevant docs |
| Latency | < 500ms | Excellent - real-time capable |
| Latency | 500-2000ms | Good - acceptable for most uses |
| Latency | > 2000ms | Poor - too slow for interactive use |

## Adding Custom Metrics

1. Create metric file in `evaluation/metrics/custom_metric.py`
2. Implement metric function with signature:
   ```python
   def compute_metric(predictions: list[dict], golden: list[dict]) -> float:
       """Compute metric score."""
       pass
   ```
3. Register in `evaluator.py`
4. Add to `thresholds.yaml` if needed

## Reporting

Generate evaluation reports:

```python
from evaluation.reports import generate_report

report = generate_report(results, output_path="results/report.html")
```

Reports include:
- Metric summaries
- Threshold compliance
- Failure case analysis
- Trend charts (if historical data available)
