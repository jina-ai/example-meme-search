FROM jinaai/jina:2.6.2-py39-standard

# setup the workspace
COPY . /workspace
WORKDIR /workspace

RUN apt-get update && apt-get install --no-install-recommends -y zlib1g zlib1g-dev git build-essential g++ libjpeg-dev && pip install -r requirements.txt

EXPOSE 8510

ENTRYPOINT ["streamlit"]
CMD ["run", "frontend.py"]
