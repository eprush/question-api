# The 1 stage: Assembly
FROM python:3.13 AS builder

# Create a working directory /src for the source code and /venv for the virtual environment
WORKDIR /src/

COPY pyproject.toml .
COPY pdm.lock .

# Manually create a virtual environment in /venv and install dependencies
RUN python -m venv /venv \
    && . /venv/bin/activate \
    && pip install pdm \
    && pdm install

# The 2 stage: Final
FROM python:3.13

# Working directory for the application /src
WORKDIR /src/

# Copy the installed virtual environment from the first stage into /venv
COPY --from=builder /venv /venv

# Copy the rest of the application files into /src
COPY . .

# Set environment variables to activate the virtual environment and add PYTHONPATH
ENV VIRTUAL_ENV=/venv
ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH="/src"

WORKDIR /src/

# Expose the necessary port
EXPOSE 8080

# Run the application
CMD ["sh", "-c", "alembic upgrade head && python main.py"]