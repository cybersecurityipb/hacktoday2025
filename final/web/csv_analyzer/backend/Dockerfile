FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
RUN mkdir -p /app/uploads
RUN echo "hacktoday{bayangin_lu_bukan_seorang_web_main_tapi_karena_para_player_web_ganiat_lu_terpaksa_buat_soal-(woi p @ardhani, tolong yang solp tag beliau sambil bilang parah di dc hektod)}" > /flag-$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 16).txt
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]