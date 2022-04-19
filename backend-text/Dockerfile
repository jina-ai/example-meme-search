FROM jinaai/jina:3.2.9-py39-standard

# setup the workspace
COPY . /workspace
WORKDIR /workspace

RUN apt-get update && apt-get install --no-install-recommends -y git build-essential g++

ENTRYPOINT ["python", "app.py", "-t"]
CMD ["search"]

EXPOSE 45679
