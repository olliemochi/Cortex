################################################################################
# Cortex CLI - Command-line Interface
# Organization: AetherAssembly
# License: MIT
# 
# Production-ready Docker image for Cortex CLI
################################################################################

FROM python:3.11-slim

WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy CLI files
COPY cli/cortex_cli.py .
COPY cli/commands ./commands
COPY cli/completions ./completions

# Install minimal dependencies for CLI
RUN pip install --no-cache-dir \
    click==8.1.8 \
    rich==13.7.0 \
    tabulate==0.9.0 \
    requests==2.32.5

# Set the CLI script as entrypoint
RUN chmod +x cortex_cli.py

ENTRYPOINT ["python", "cortex_cli.py"]
CMD ["--help"]
