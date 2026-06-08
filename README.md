# MedRefer

An AI-powered medical referral system that analyzes patient medical questions and recommends appropriate medical specialists using LLM models (default: `ollama/gemma4` via LiteLLM).

## Overview

MedRefer uses large language models (powered by LiteLLM) to intelligently interpret patient symptoms and medical questions, then recommends the most appropriate medical specialists. The system validates recommendations against a curated list of 45 medical specialties to ensure accuracy and prevent hallucinations.

## Features

- **AI-Powered Analysis**: Uses LLMs to understand medical questions and symptoms
- **Multi-Provider Support**: Works with any LLM provider supported by LiteLLM (OpenAI, Anthropic, etc.)
- **Specialist Validation**: Validates recommendations against a predefined list of 45 medical specialties
- **Interactive CLI**: Simple command-line interface for continuous use
- **Error Handling**: Graceful error handling for API failures
- **Professional Disclaimers**: Includes disclaimers reminding users to verify recommendations with healthcare professionals

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/csv610/MedRefer.git
   cd MedRefer
   ```

2. **Install dependencies**:
   ```bash
   make install        # production only
   # or
   make install-dev    # with dev/test dependencies
   ```
   Or manually:
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"   # includes test tooling
   ```

3. **Set up Ollama** (default model):

   Install [Ollama](https://ollama.com) and pull the default model:
   ```bash
   ollama pull gemma4
   ```

   For other LLM providers, set the appropriate environment variable:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"        # For OpenAI
   export ANTHROPIC_API_KEY="your-anthropic-api-key"  # For Claude
   export GOOGLE_API_KEY="your-google-api-key"        # For Gemini
   ```

## Usage

### Basic Usage

Run the interactive CLI:
```bash
python medrefer.py
```

Then enter your medical question when prompted:
```
Enter your medical question: I have chest pain and shortness of breath.
Recommended Specialists: Cardiologist, Pulmonologist
```

### Programmatic Usage

```python
from medrefer import MedReferral

# Initialize the referral system
referral = MedReferral()

# Get specialist recommendations
question = "I have severe headaches and blurry vision"
specialists = referral.get_specialist_recommendation(question)
print(f"Recommended Specialists: {specialists}")
```

## Supported Medical Specialties

The system supports 45 medical specialties including:
- Allergist
- Cardiologist
- Dermatologist
- Endocrinologist
- Gastroenterologist
- Neurologist
- Oncologist
- Ophthalmologist
- Orthopedic Surgeon
- Psychiatrist
- Urologist
- And 34 more...

See the complete list in the `medrefer.py` file under the `medical_specialists` frozenset.

## Configuration

### Changing the LLM Model

The default model is **Ollama Gemma4** (`ollama/gemma4`). To use a different LLM model, modify the `model` parameter in the `get_specialist_recommendation` method:

```python
response = litellm.completion(
    model="gpt-4o",  # Use OpenAI instead
    messages=[...],
    max_tokens=100
)
```

Supported models via LiteLLM include:
- Ollama: `ollama/gemma4` (default), `ollama/llama3`, `ollama/mistral`
- OpenAI: `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`
- Google: `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-pro`
- Anthropic: `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- And many more...

### API / Provider Configuration

LiteLLM automatically uses the right auth based on the model prefix:
- Ollama: runs locally (no API key needed)
- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- Google Gemini: `GOOGLE_API_KEY`
- Hugging Face: `HUGGINGFACE_API_KEY`

## Makefile

Commonly used targets (run `make help` for all):

| Target | Description |
|--------|-------------|
| `make test` | Run all tests |
| `make test-coverage` | Run with coverage report |
| `make run` | Start interactive CLI |
| `make lint` | Check Python syntax |
| `make install-dev` | Install all dependencies |
| `make clean` | Remove caches and build artifacts |

## Testing

Run the test suite:
```bash
make test
# or
pytest tests/ -v
```

Run specific tests:
```bash
pytest tests/test_medrefer.py::TestGetSpecialistRecommendation::test_returns_valid_specialists -v
```

Run with coverage:
```bash
pytest tests/ --cov=medrefer --cov-report=html
```

## Architecture

### MedReferral Class

**Attributes:**
- `medical_specialists`: A frozenset containing 45 valid medical specialist types

**Methods:**
- `__init__()`: Initializes the API configuration
- `get_specialist_recommendation(question)`: Analyzes a medical question and returns specialist recommendations

### Flow

1. User provides a medical question
2. LLM analyzes the question with context from examples
3. Response is parsed to extract specialist names
4. Extracted specialists are validated against the allowed list
5. Valid specialists are returned; otherwise, a disclaimer is provided

## Error Handling

The system includes try-except blocks to handle API failures gracefully. If an error occurs, a user-friendly error message is returned instead of crashing the application.

## Important Disclaimers

This tool is designed to assist in finding appropriate specialists based on symptoms. However:
- **Always consult with a qualified healthcare professional** before making medical decisions
- This tool is not a medical diagnosis or treatment recommendation
- Recommendations should be verified by a licensed healthcare provider
- Emergency situations require immediate professional medical attention

## Dependencies

- **litellm**: Unified interface for LLM APIs
- **openai**: OpenAI Python client (automatically installed with litellm)
- Python 3.7+

See `requirements.txt` for exact versions.

## License

MIT

## Contributing

Contributions are welcome! Please ensure:
- All tests pass
- Code follows PEP 8 style guidelines
- New features include appropriate tests

## Support

For issues or questions, please open an issue on GitHub or contact the maintainers.
