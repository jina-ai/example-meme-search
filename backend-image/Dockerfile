FROM jinaai/jina:3.2.10-py39-standard

# setup the workspace
COPY . /workspace
WORKDIR /workspace

RUN apt-get update && apt-get install --no-install-recommends -y zlib1g zlib1g-dev git build-essential g++ libjpeg-dev && pip install -r requirements.txt

ENTRYPOINT ["python", "app.py", "-t"]
CMD ["search"]

EXPOSE 65432
