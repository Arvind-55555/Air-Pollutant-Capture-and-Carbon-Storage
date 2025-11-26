FROM python:3.11-slim
WORKDIR /agents
COPY agents /agents
RUN pip install --no-cache-dir requests
CMD ["python", "agent_runner.py"]
