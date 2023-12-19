import queue
from concurrent.futures import ThreadPoolExecutor
import threading
import grpc
import json
from google.protobuf.json_format import MessageToJson
from . import asr_pb2 
from . import asr_pb2_grpc


class GrpcClient:
    def __init__(
        self,
        url,
        token,
        req_id,
        nbest=1,
        continuous_decoding=True,
        on_start=None,
        on_sentence_changed=None,
        on_sentence_end=None,
        on_completed=None,
        on_error=None
    ):
        # configs
        self.url = url
        self.req_id = req_id
        self.nbest = nbest
        self.continuous_decoding = continuous_decoding
        # callbacks
        self.on_start = on_start
        self.on_sentence_changed = on_sentence_changed
        self.on_sentence_end = on_sentence_end
        self.on_completed = on_completed
        self.on_error = on_error
        # service
        self.executor = ThreadPoolExecutor()
        self.data_queue = queue.Queue()
        self.channel = grpc.insecure_channel(self.url)
        self.stub = asr_pb2_grpc.ASRStub(self.channel)
        # state
        self._recognize_finished = threading.Event()

        if self.continuous_decoding:
            response_iterator = self.stub.RealTimeSpeechRecognition(
                self.generate_request(),
                metadata=((("authorization", token),) if token is not None else None)
            )
        else:
            response_iterator = self.stub.OneSentenceSpeechRecognition(
                self.generate_request(),
                metadata=((("authorization", token),) if token is not None else None)
            )
        executor = ThreadPoolExecutor()
        consumer_future = executor.submit(self.response_watcher, response_iterator)

    def send(self, data):
        self.data_queue.put(data)
    
    def stop(self):
        self.data_queue.put(None)
        self._recognize_finished.wait()
        if not self._recognize_finished.is_set():
            if self.on_error:
                self.on_error(f"[Req {self.req_id}] Recognition does not stop after 30 seconds...")

    def close(self):
        self.channel.close()

    def generate_request(self):
        if self.on_start is not None:
            self.on_start(f"[Req {self.req_id}] Recognition started")

        # first send config
        request = asr_pb2.Request()
        request.decode_config.req_id = self.req_id
        request.decode_config.nbest = self.nbest
        yield request

        # then send data
        while True:
            try:
                request = asr_pb2.Request()
                data = self.data_queue.get(timeout=30.0)
            except Exception as e:
                if self.on_error is not None:
                    self.on_error(f"[Req {self.req_id}] No data input for more than 30 seconds...")
                break

            if data is None:
                break
            request.audio_data = data
            yield request

    def response_watcher(self, response_iterator):
        try:
            for response in response_iterator:
                if response.header.status == asr_pb2.Response.Status.OK:
                    if response.header.type == asr_pb2.Response.Type.SENTENCE_CHANGED:
                        result = json.loads(MessageToJson(response))['payload']['result']
                        if self.on_sentence_changed is not None:
                            self.on_sentence_changed(f"[Req {self.req_id}] Sentence changed", result=result)
                    elif response.header.type == asr_pb2.Response.Type.SENTENCE_END:
                        result = json.loads(MessageToJson(response))['payload']['result']
                        if self.on_sentence_end is not None:
                            self.on_sentence_end(f"[Req {self.req_id}] Sentence end", result=result)
                    if response.header.type == asr_pb2.Response.Type.COMPLETED:
                        if self.on_completed is not None:
                            self.on_completed(f"[Req {self.req_id}] Recognize completed")
                        break
                else:
                    if self.on_error is not None:
                        self.on_error(f"[Req {self.req_id}] Server returns error.")
        except Exception as e:
            if self.on_error is not None:
                self.on_error(f"[Req {self.req_id}] Recognize error: {str(e)}")
        self._recognize_finished.set()


class OneSentenceClient(GrpcClient):
    def __init__(
        self,
        url,
        token,
        req_id,
        nbest=1,
        on_start=None,
        on_sentence_changed=None,
        on_sentence_end=None,
        on_completed=None,
        on_error=None
    ):
        super().__init__(
            url,
            token,
            req_id,
            nbest=nbest,
            continuous_decoding=False,
            on_start=on_start,
            on_sentence_changed=on_sentence_changed,
            on_sentence_end=on_sentence_end,
            on_completed=on_completed,
            on_error=on_error
        )


class RealTimeClient(GrpcClient):
    def __init__(
        self,
        url,
        token,
        req_id,
        nbest=1,
        on_start=None,
        on_sentence_changed=None,
        on_sentence_end=None,
        on_completed=None,
        on_error=None
    ):
        super().__init__(
            url,
            token,
            req_id,
            nbest=nbest,
            continuous_decoding=True,
            on_start=on_start,
            on_sentence_changed=on_sentence_changed,
            on_sentence_end=on_sentence_end,
            on_completed=on_completed,
            on_error=on_error
        )
