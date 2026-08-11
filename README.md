*This project has been created as part of the 42 curriculum by anasinda.*

# Call-Me-Maybe-Project

## Description

This project implements a function-calling pipeline that converts natural-language prompts into structured JSON function calls. The program reads function definitions and test prompts from the input directory, asks an LLM to select the best function, then generates the arguments with constrained decoding so the final output is always valid JSON.

The implementation targets Qwen/Qwen3-0.6B and uses the attached `llm_sdk` wrapper. The output file contains one object per prompt with the keys `prompt`, `fn_name`, and `args`.

## Instructions

### Requirements

The project is written for Python 3.10+ and uses `uv` for dependency management.

### Installation

Run the following command from the repository root:

```bash
uv sync
```

### Execution

Run the project with the default input files:

```bash
uv run python -m src
```

You can also pass custom paths:

```bash
uv run python -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calling_results.json
```

### Makefile

The repository includes a Makefile with the required project commands:

```bash
make install
make run
make debug
make clean
make lint
```

## Algorithm Explanation

The pipeline works in two stages.

First, the program loads and validates the input files. The function definitions are parsed into Pydantic models, and the prompt file is validated so empty prompts and numeric-only prompts are rejected early with clear errors.

Second, the model performs function selection and parameter extraction using constrained decoding. For function selection, the model is prompted with the available function descriptions and only allowed to emit one of the known function names. For argument extraction, the program generates each value token by token while masking invalid tokens, so the output remains compatible with the declared JSON schema.

This approach avoids relying on the model to spontaneously produce valid JSON. Instead, the output structure is enforced during decoding.

## Design Decisions

- Pydantic is used to validate function definitions, prompt records, and schema contracts.
- The command-line interface reads file paths from terminal arguments instead of hardcoding them.
- Input parsing is centralized in `src/parsing.py` so error handling stays consistent.
- The final result is stored as a list of dictionaries before being written to disk.
- Progress messages are printed after each processed prompt so long runs stay visible.
- The code keeps the output format simple and machine-readable to match the correction page expectations.

## Performance Analysis

The project is designed to be reliable first and fast enough for the evaluation constraints.

- JSON parsing and validation happen once at startup.
- Prompt generation is bounded by a maximum number of decoding steps.
- The output file is written once after all prompts are processed.
- The current implementation prioritizes correctness and recoverability over aggressive batching or caching.

In practice, the main performance cost is model inference, not file parsing. The constrained decoding logic reduces invalid generations and avoids repeated retries.

## Challenges Faced

- Making the project work as a proper Python module required fixing package-relative imports.
- The input data needed stricter validation so malformed definitions and prompts fail with clear messages instead of crashing.
- Keeping the code compatible with flake8 and mypy required reflowing long prompt strings and adding explicit type annotations.
- The output schema had to stay stable while the internal processing pipeline evolved.

## Testing Strategy

The implementation was validated with a mix of static checks and direct runtime checks.

- `uv run flake8 src`
- `uv run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`
- `python -m src --help`
- Direct parser checks for empty prompts, empty function metadata, and numeric-only input files

These checks confirmed that invalid input is rejected cleanly and that the package entry point still works.

## Example Usage

Run the default pipeline:

```bash
uv run python -m src
```

Run with explicit file paths:

```bash
uv run python -m src \
	--functions_definition data/input/functions_definition.json \
	--input data/input/function_calling_tests.json \
	--output data/output/function_calling_results.json
```

The generated file will be written to the chosen output path as a JSON array.

## Resources

- Python argparse documentation
- Python json documentation
- Pydantic documentation
- Qwen model documentation for Qwen/Qwen3-0.6B
- JSON specification and RFC 8259
- 42 project subject and correction page provided with the assignment

### AI Usage

AI was used to help with code refactoring, input validation design, README drafting, and line-length cleanup. The final implementation and validation were reviewed in the repository, and the project logic was kept understandable and editable without depending on generated code as a black box.
