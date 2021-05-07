FROM python:3.8

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR '/app'

COPY handlers/* handlers/
COPY sample-data/* sample-data/
COPY tests/* tests/

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
COPY app.py .
WORKDIR .

EXPOSE 5000
ENTRYPOINT ["python", "app.py"]