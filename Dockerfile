FROM python

RUN mkdir -p /usr/my_app

WORKDIR /usr/my_app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "/bin/sh", "-c", "python data_harvest/harvest.py" ]
