FROM python:3.11.4


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install the NotionAPI
COPY ./ ./

RUN pip install NotionAPI/dist/NotionAPI-0.1.2-py3-none-any.whl

CMD [ "python", "./src/main.py" ]