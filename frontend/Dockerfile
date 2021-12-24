FROM python:3.9-bullseye

# setup the workspace
COPY . /workspace
WORKDIR /workspace

RUN pip install -r requirements.txt

EXPOSE 8510

ENTRYPOINT ["streamlit"]
CMD ["run", "frontend.py"]
