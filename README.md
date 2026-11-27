# AI API Service

Dịch vụ API AI viết bằng **Flask + LangChain**, dùng chung cho nhiều sản phẩm (LMS, HRM, CRM, chatbot khách hàng…). Cung cấp chatbot RAG, sinh nội dung (câu hỏi, khoá học, mục tiêu, công thức…), Text-to-SQL cho báo cáo, chuyển văn bản thành giọng nói và giao diện quản lý dữ liệu training (vector).

---

## 1. Tổng quan kiến trúc

```
Client (LMS / HRM / web) ──HTTP──► Flask app (container "web", cổng 5000)
                                     │
                                     ├── LLM providers: OpenAI · Claude · Gemini · Groq
                                     ├── Redis Stack (container "redis") — vector store / RediSearch
                                     └── SQL Server (bên ngoài, qua ODBC Driver 17) — chỉ dùng cho Report / Training SQL
```

| Thành phần | Công nghệ |
|---|---|
| Web framework | Flask 3, flask-cors, flasgger (Swagger UI) |
| LLM orchestration | LangChain 0.3, LangGraph |
| Model | OpenAI (`chatgpt`), Anthropic (`claude`), Google (`gemini`), Groq (`groq`) |
| Vector DB | Redis Stack (`langchain_redis`), embedding = `OpenAIEmbeddings` |
| SQL | SQL Server qua `pyodbc` + `msodbcsql17` |
| Xử lý tài liệu | pypdf, docx2txt, python-pptx, pytesseract (OCR tiếng Việt), pdf2image |
| Giọng nói | gTTS, pydub, ffmpeg |

## 2. Cấu trúc thư mục

```
.
├── app.py                 # Entry point Flask, đăng ký blueprint, log vào logs/error_log.log
├── routes/                # Các blueprint HTTP
│   ├── chatbot.py         #   /chatbot/*
│   ├── generate.py        #   /generate/*
│   ├── report.py          #   /report/*
│   ├── speech.py          #   /speech/*
│   └── training.py        #   /training/*  (kèm giao diện HTML)
├── factory/
│   ├── model_factory.py   # Chọn LLM theo tên: chatgpt | claude | gemini | groq
│   ├── training_factory.py# Chọn loại training: course | resource | resource_saas | training_sql | training_ddl
│   ├── base/              # Lớp cơ sở: context, model, services, training
│   ├── model/             # Wrapper từng LLM provider
│   └── services/          # Chatbot / graph dùng chung
├── project/               # Logic theo từng dự án/khách hàng
│   ├── lms/               #   LMS: chatbot, sinh câu hỏi/khoá học/bài tập/feedback/goal, training
│   ├── hrm/               #   HRM: sinh goal, formula
│   ├── report/            #   Text-to-SQL (DDL + SQL mẫu lưu trong vector store)
│   ├── crm/ english/ highlands/ suleco/ trungnguyen/   # chatbot theo khách hàng
├── config/
│   ├── config_sqldb.py    # Kết nối SQL Server
│   └── config_vectordb.py # Kết nối Redis vector store
├── tools/helper.py        # Hàm tiện ích (load chatbot động theo context, đọc file, ...)
├── templates/, static/    # Giao diện training / import / chatbot demo
├── delete.py              # Script tay: xoá index trong Redis
├── dump.rdb               # Bản dump Redis (dữ liệu vector mẫu)
├── Dockerfile, docker-compose.yml, makefile
└── .env.dist              # Mẫu biến môi trường
```

**Cơ chế "context":** request chatbot gửi `context` (vd `lms`, `crm`, `highlands`) → `tools/helper.get_chatbot()` import động `project.<context>.services.chatbot`. Muốn thêm khách hàng mới: tạo thư mục `project/<tên>/` với `context.py` và `services/chatbot.py` theo mẫu có sẵn.

## 3. Chạy project bằng Docker Compose

### 3.1. Yêu cầu

- Docker + Docker Compose (Docker Desktop trên Windows/macOS).
- API key của ít nhất một LLM provider (OpenAI bắt buộc nếu dùng vector store vì embedding dùng OpenAI).
- (Tuỳ chọn) SQL Server truy cập được từ máy chạy Docker — chỉ cần cho Report / Training SQL.

### 3.2. Cấu hình `.env`

```bash
cp .env.dist .env
```

Ví dụ `.env` tối thiểu khi chạy bằng Docker:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=
CLAUDE_MODEL=claude-haiku-5-5
GROQ_API_KEY=
GOOGLE_API_KEY=

VECTORDB_NAME=redis
VECTORDB_HOST=redis
VECTORDB_PORT=6379
```

### 3.3. Build và chạy

```bash
docker compose up -d --build     # lần đầu hoặc khi đổi requirements.txt / Dockerfile
docker compose up -d             # các lần sau  (hoặc: make up)
docker compose ps                # kiểm tra trạng thái
docker compose logs -f web       # xem log app
```

Sau khi chạy:

| Dịch vụ | URL |
|---|---|
| API | http://localhost:5000 |
| Swagger | http://localhost:5000/apidocs |
| Giao diện training | http://localhost:5000/training/index |
| RedisInsight (UI Redis Stack) | http://localhost:8001 |
| Redis từ máy host | `localhost:6381` |
| Cổng debug (ptvsd) | `5678` — cần bỏ comment dòng `ptvsd.enable_attach` trong `app.py` |

> Thư mục code được mount vào container (`.:/app`), app chạy với `use_reloader=True` nên sửa code là tự reload, không cần build lại. Chỉ build lại khi đổi `requirements.txt` hoặc `Dockerfile`.

### 3.4. Dữ liệu Redis

- Dữ liệu Redis lưu ở `./redis` (mount vào `/data`, đã nằm trong `.gitignore`).
- Khôi phục dữ liệu mẫu từ `dump.rdb` trong repo (làm **trước** lần chạy đầu, hoặc khi Redis đang dừng):

  ```bash
  docker compose stop redis
  mkdir -p redis && cp dump.rdb redis/dump.rdb
  docker compose start redis
  ```

- Sao lưu dữ liệu Redis hiện tại ra file `dump.rdb`: `make db` (= `docker cp redis:/data/dump.rdb ./`).

### 3.5. Lệnh thường dùng

```bash
docker compose restart web       # restart app
docker compose exec web bash     # vào shell container app
docker compose exec redis redis-cli
docker compose down              # dừng & xoá container (dữ liệu Redis vẫn còn trong ./redis)
```

> Lưu ý `makefile`: các lệnh `rs`, `log`, `e`, `rsdb`, `logdb`, `edb` đang dùng tên container cũ (`ai-web-1`, `redis_test`). Tên thực tế phụ thuộc tên thư mục project (vd `<thư-mục>-web-1`) và container redis tên `redis`. Dùng `docker compose ...` như trên để không phụ thuộc tên, hoặc sửa lại `makefile`. Các lệnh `make up`, `make down`, `make ps`, `make db` dùng được bình thường.

## 4. Chạy không dùng Docker (tham khảo)

Cần Python 3.13, ODBC Driver 17 for SQL Server, ffmpeg, tesseract-ocr (+ gói `vie`), poppler. Redis Stack vẫn chạy bằng Docker:

```bash
docker compose up -d redis
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
# .env: VECTORDB_HOST=127.0.0.1, VECTORDB_PORT=6381
python app.py
```
