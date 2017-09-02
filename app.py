import json
import os
import traceback
import uuid
import asyncio
import logging
import queue
import signal
import concurrent
from flask import Flask, abort, make_response, jsonify, request
from task import TaskGenerateText
from threading import Timer


logging.basicConfig(level="INFO", format="%(name)s : %(levelname)s : %(message)s")


YANDEX_KEY = os.getenv('YANDEX_KEY')
app = Flask(__name__)
q = queue.PriorityQueue()

loop = asyncio.get_event_loop()
executor = concurrent.futures.ThreadPoolExecutor(1)


@app.route('/play', methods=['POST'])
def play():
    req = request.json
    if not req or not 'text' in req:
        return jsonify({'error': 'Not text'}), 503

    try:
        q.put_nowait(TaskGenerateText(req.get('priority', 1), req, YANDEX_KEY))
        logging.info('Add task with: %s' % req)
        return jsonify({'message': 'Add task with: %s' % req,
                        'queue_size': q.qsize(),
                        }), 200
    except Exception as e:
        logging.exception("Error by generate response for method play!")
        return jsonify({'error': traceback.format_exc()}), 503

def shutdown_server(*args):
    try:
        loop.stop()
        executor.shutdown(wait=True)
        loop.close()

        func_ = request.environ.get('werkzeug.server.shutdown')
        func_()
    except Exception as e:
        logging.exception("Error by shutdown server!")
    finally:
        os._exit(1)

@app.route('/kill', methods=['GET', 'POST'])
def kill():
    Timer(0.5, shutdown_server).start()
    return jsonify({'message': 'Start shutdown server'}), 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found method'}), 404)

async def run_tasks():
    while loop.is_running():
        await asyncio.sleep(0.1)
        while not q.empty():
            task = q.get()
            task.play()
            q.task_done()
            logging.info('Play task with: %s' % task.data)
            logging.info('Queue size: %s' % q.qsize())

if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, shutdown_server)
        signal.signal(signal.SIGTERM, shutdown_server)

        loop.create_task(run_tasks())
        loop.run_in_executor(executor, loop.run_forever)

        app.run("0.0.0.0", os.getenv('APP_PORT') or 5000, threaded=True, debug=True)
    except Exception as e:
        logging.exception("Error by up server!")
    finally:
        shutdown_server()
