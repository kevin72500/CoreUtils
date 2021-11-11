from python:3.6.4
RUN mkdir /app;
copy bladeTest/* /app/
workdir /app
RUN pip install pip --upgrade; pip install -r requirements.txt -i https://pypi.douban.com/simple --no-cache-dir
CMD ["python","versionSuggestion.py"]
