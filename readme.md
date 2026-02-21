> **Note:**
> The first time you build the Docker image, Docker Compose will download the Hugging Face RoBERTa sentiment model (`cardiffnlp/twitter-roberta-base-sentiment-latest`). This step can take a few minutes (typically 2–5 minutes depending on your internet speed). Subsequent runs will use the cached model and start much faster.

## Scalability Considerations

**Speech-to-Text (STT) and Text-to-Speech (TTS) Models:**
I use Deepgram for STT (with diarization) and Google TTS for generating audio. For sentiment, I use a RoBERTa model from Hugging Face. Originally, I considered WhisperX (open-source, fast, accurate, supports diarization), but it requires a Hugging Face token and extra setup. In the future, self-hosting WhisperX would let me scale without relying on external APIs.

**Decoupling Compute from I/O:**
Celery lets me scale the API and worker layers independently. The API can handle lots of uploads without blocking, while workers can be added or removed based on queue depth.

**Resource-Aware Worker Pools:**
Some tasks (like running big NLP models) use a lot of memory. In production, I’d tune Celery’s prefetch settings and use separate queues for heavy and light jobs, so one worker doesn’t get overloaded.

**Database & Caching:**
As transcripts grow, I’d use PostgreSQL partitioning to keep queries fast. For TTS, I cache generated audio files—if a snippet was already created, I reuse it. In a bigger setup, this could move to Redis or a CDN.

**Horizontal Scaling & Storage:**
Right now, Docker volumes handle file sharing. For real scale, I’d use object storage (like S3 or GCS) so any worker can access files, even across machines.

**Optimized Model Loading:**
Heavy models are loaded once per worker, not per task, to save memory and speed up processing.

These choices help the system stay fast, reliable, and ready to grow as usage increases.

## Architectural Decisions & Trade-offs


This project is built with FastAPI for its speed and developer-friendly interface. FastAPI lets me handle HTTP requests quickly and makes it easy to build and document APIs.


For heavy-lifting tasks like transcription and speaker diarization, I use Celery. Celery runs these jobs asynchronously, so the app doesn’t block while processing audio. This means users get a fast response, and the actual work happens in the background. Redis is used as the broker and queue for Celery, making task management reliable and fast.


PostgreSQL is my database of choice. It’s robust, handles relational data well, and is easy to work with for storing calls, transcripts, and metadata.


Docker Compose is used to orchestrate all services. I run Celery in a separate container from FastAPI, so each service can be scaled independently. This separation also makes the system more reusable and easier to maintain. For example, if transcription jobs start piling up, I can scale just the Celery workers without touching the API or database containers.

These choices help keep the app responsive, modular, and ready for production workloads.
---


Build and start all services:

```
docker compose up --build
```

To start only FastAPI:

```
docker compose up app
```

To start only Celery:

```
docker compose up celery
```


Once FastAPI is running, visit:

```
http://localhost:8000/docs
```
for interactive API documentation and testing.


Postgres and pgAdmin are included in Docker Compose. Access pgAdmin at:

```
http://localhost:5050
```
Login with:
	- Email: admin@admin.com
	- Password: admin

The database and tables are automatically created when the app service starts. 

---

## Example Usage & Endpoint Testing

### 1. Transcribe Audio

Upload an audio file for transcription (use any local file or sample in `sample_clip/`):

```
curl --location 'http://localhost:8000/transcribe/' \
	--header 'accept: application/json' \
	--form 'file=@"sample_clip/your_audio_file.wav"'
```

Returns 200 and starts a Celery task. Uses Deepgram for transcription (diarization enabled). Add your Deepgram API key in `.env` (see `.env.example`).

### 2. Text-to-Speech (/speak)

Generate speech audio from text:

```
curl --location 'http://localhost:8000/speak/' \
	--header 'Content-Type: application/json' \
	--data '{"text": "Hello, this is a test."}'
```

Returns an audio file for the provided text.

### 3. Coachable Moments (/integration/coachable-moments)

Get detected coachable moments:

```
curl --location 'http://localhost:8000/integration/coachable-moments/' \
	--header 'Content-Type: application/json'
```

Response example:

```
{
	"response": [
		{
			"id": 6,
			"call_id": "809a613b-3a6c-4b85-a7ad-597f44b65dd6",
			"speaker_tag": "Speaker 0",
			"text": "The stale smell of old beer lingers.",
			"start_time": 1.12,
			"end_time": 3.62,
			"sentiment": "negative",
			"is_coachable": true
		}
	]
}
```

### 4. Replay Coachable Moment (/replay)

Use the `id` from the previous response to get the audio snippet:

```
curl --location --request POST 'http://localhost:8000/replay?id=6' \
	--header 'Content-Type: application/json'
```

Returns the audio snippet for that exact coachable moment.

### 5. List Calls (/integration/calls)

Get all calls:

```
curl --location 'http://localhost:8000/integration/calls' \
	--header 'Content-Type: application/json'
```

### 6. Get Transcript Segments (/integration/transcript-segments)

Use the `call_id` to get transcript segments:

```
curl --location 'http://localhost:8000/integration/transcript-segments?call_id=809a613b-3a6c-4b85-a7ad-597f44b65dd6' \
	--header 'Content-Type: application/json'
```
