# Hippocratic_Assessment
A self-correcting bedtime story generator powered by OpenAI. Features an iterative 'Actor-Critic' architecture where a Judge agent automatically critiques and refines content for quality and safety.

## System Architecture

```mermaid
graph TD
    User([User Request]) --> Input{Input Handler}
    Input -->|Topic & Age| Storyteller[Storyteller Agent]
    
    subgraph "Quality Control Loop"
        Storyteller -->|Draft Story| Judge[Judge Agent]
        Judge -->|Critique & Score| Decision{Pass Score > 7?}
        Decision -- No (Feedback) --> Refine[Refinement Step]
        Refine -->|Improved Context| Storyteller
        Decision -- Yes --> Finalizer[Final Polish]
    end
    
    Finalizer --> Output([Final Story])
    
    style Storyteller fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style Judge fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    style Decision fill:#ffebee,stroke:#c62828,stroke-width:2px
```

## 🚀 How to Run

### 1. Prerequisites
* Python 3.8 or higher
* An OpenAI API Key

### 2. Setup
Clone the repo and install the required library:
```bash
pip install openai
