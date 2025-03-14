from flask import Flask, request
from queue import Queue
from services.webhook import send_webhook
import threading
import uuid
import os
import time
from version import BUILD_NUMBER  # 🔢 Import the BUILD_NUMBER

MAX_QUEUE_LENGTH = int(os.environ.get('MAX_QUEUE_LENGTH', 0))  # 🚦 Maximum tasks allowed in queue

def create_app():
    app = Flask(__name__)

    # 📥 Create a queue to hold tasks
    task_queue = Queue()
    queue_id = id(task_queue)  # 🔢 Generate a unique queue_id for this worker

    # ⏱️ Function to process tasks from the queue in a separate thread
    def process_queue():
        while True:
            job_id, data, task_func, queue_start_time = task_queue.get()  # 📥 Get task from queue
            queue_time = time.time() - queue_start_time  # ⏳ Calculate time spent in queue
            run_start_time = time.time()  # ⏱️ Start time for processing
            pid = os.getpid()  # 🖥️ Get the PID of the processing thread
            response = task_func()  # 🔄 Execute the task
            run_time = time.time() - run_start_time  # ⏲️ Calculate task run time
            total_time = time.time() - queue_start_time  # ⏳ Total time (queue + run)

            response_data = {
                "endpoint": response[1],
                "code": response[2],
                "id": data.get("id"),
                "job_id": job_id,
                "response": response[0] if response[2] == 200 else None,
                "message": "success" if response[2] == 200 else response[0],
                "pid": pid,
                "queue_id": queue_id,
                "run_time": round(run_time, 3),
                "queue_time": round(queue_time, 3),
                "total_time": round(total_time, 3),
                "queue_length": task_queue.qsize(),
                "build_number": BUILD_NUMBER  # 🏗️ Add build number to response
            }

            send_webhook(data.get("webhook_url"), response_data)  # 🔔 Send result via webhook

            task_queue.task_done()  # ✅ Mark task as done

    # 🧵 Start the queue processing in a separate daemon thread
    threading.Thread(target=process_queue, daemon=True).start()

    # 🚀 Decorator to add tasks to the queue or bypass it
    def queue_task(bypass_queue=False):
        def decorator(f):
            def wrapper(*args, **kwargs):
                job_id = str(uuid.uuid4())  # 🆔 Generate a unique job ID
                data = request.json if request.is_json else {}  # 📥 Get JSON payload
                pid = os.getpid()  # 🖥️ Get PID for non-queued tasks
                start_time = time.time()  # ⏱️ Start time for task execution
                
                if bypass_queue or 'webhook_url' not in data:
                    # ⚡ Process task immediately (bypassing the queue)
                    response = f(job_id=job_id, data=data, *args, **kwargs)
                    run_time = time.time() - start_time  # ⏲️ Calculate run time
                    return {
                        "code": response[2],
                        "id": data.get("id"),
                        "job_id": job_id,
                        "response": response[0] if response[2] == 200 else None,
                        "message": "success" if response[2] == 200 else response[0],
                        "run_time": round(run_time, 3),
                        "queue_time": 0,
                        "total_time": round(run_time, 3),
                        "pid": pid,
                        "queue_id": queue_id,
                        "queue_length": task_queue.qsize(),
                        "build_number": BUILD_NUMBER  # 🏗️ Add build number to response
                    }, response[2]
                else:
                    # 🚦 Check if queue has reached maximum length
                    if MAX_QUEUE_LENGTH > 0 and task_queue.qsize() >= MAX_QUEUE_LENGTH:
                        return {
                            "code": 429,
                            "id": data.get("id"),
                            "job_id": job_id,
                            "message": f"MAX_QUEUE_LENGTH ({MAX_QUEUE_LENGTH}) reached",
                            "pid": pid,
                            "queue_id": queue_id,
                            "queue_length": task_queue.qsize(),
                            "build_number": BUILD_NUMBER  # 🏗️ Add build number to response
                        }, 429
                    
                    # ⏳ Put task into the queue
                    task_queue.put((job_id, data, lambda: f(job_id=job_id, data=data, *args, **kwargs), start_time))
                    
                    return {
                        "code": 202,
                        "id": data.get("id"),
                        "job_id": job_id,
                        "message": "processing",
                        "pid": pid,
                        "queue_id": queue_id,
                        "max_queue_length": MAX_QUEUE_LENGTH if MAX_QUEUE_LENGTH > 0 else "unlimited",
                        "queue_length": task_queue.qsize(),
                        "build_number": BUILD_NUMBER  # 🏗️ Add build number to response
                    }, 202
            return wrapper
        return decorator

    app.queue_task = queue_task  # ⚙️ Attach the queue_task decorator to the app

    # 📥 Import blueprints (API endpoints)
    from routes.media_to_mp3 import convert_bp
    from routes.transcribe_media import transcribe_bp
    from routes.combine_videos import combine_bp
    from routes.audio_mixing import audio_mixing_bp
    from routes.gdrive_upload import gdrive_upload_bp
    from routes.authenticate import auth_bp
    from routes.caption_video import caption_bp 
    from routes.extract_keyframes import extract_keyframes_bp
    from routes.image_to_video import image_to_video_bp
    
    # 🚀 Register blueprints
    app.register_blueprint(convert_bp)
    app.register_blueprint(transcribe_bp)
    app.register_blueprint(combine_bp)
    app.register_blueprint(audio_mixing_bp)
    app.register_blueprint(gdrive_upload_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(caption_bp)
    app.register_blueprint(extract_keyframes_bp)
    app.register_blueprint(image_to_video_bp)
    
    # 📌 Version 1.0 endpoints
    from routes.v1.ffmpeg.ffmpeg_compose import v1_ffmpeg_compose_bp
    from routes.v1.media.media_transcribe import v1_media_transcribe_bp
    from routes.v1.media.transform.media_to_mp3 import v1_media_transform_mp3_bp
    from routes.v1.video.concatenate import v1_video_concatenate_bp
    from routes.v1.video.caption_video import v1_video_caption_bp
    from routes.v1.image.transform.image_to_video import v1_image_transform_video_bp
    from routes.v1.toolkit.test import v1_toolkit_test_bp  # 🔄 (If needed, change 'toolkit' to 'ciberfobia-api')
    from routes.v1.toolkit.authenticate import v1_toolkit_auth_bp  # 🔄 (If needed, change 'toolkit' to 'ciberfobia-api')
    from routes.v1.code.execute.execute_python import v1_code_execute_bp

    app.register_blueprint(v1_ffmpeg_compose_bp)
    app.register_blueprint(v1_media_transcribe_bp)
    app.register_blueprint(v1_media_transform_mp3_bp)
    app.register_blueprint(v1_video_concatenate_bp)
    app.register_blueprint(v1_video_caption_bp)
    app.register_blueprint(v1_image_transform_video_bp)
    app.register_blueprint(v1_toolkit_test_bp)
    app.register_blueprint(v1_toolkit_auth_bp)
    app.register_blueprint(v1_code_execute_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # 🚀 Run the app on port 8080
