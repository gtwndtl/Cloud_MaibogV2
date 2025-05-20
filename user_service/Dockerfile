# ใช้ official Python image
FROM python:3.10-slim

# ตั้ง working directory
WORKDIR /app

# คัดลอก requirements.txt และติดตั้ง dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดแอปทั้งหมด
COPY . .

# expose port
EXPOSE 5001

# รันแอป
CMD ["python", "app.py"]
