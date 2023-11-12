FROM tensorflow/tensorflow

WORKDIR /app_backend

RUN pip install fastapi==0.103.2
RUN pip install uvicorn==0.23.2
RUN pip install pytest==7.4.2

RUN pip install gensim==4.3.2
RUN pip install scikit-learn==1.3.1


COPY /app_backend .


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
