import grpc
from concurrent import futures
from ml_service import MlService
from proto import text_service_pb2, text_service_pb2_grpc


class TextService(text_service_pb2_grpc.TextServiceServicer):
  def __init__(self, model):
    self.model = model
    super().__init__()


  def ProcessText(self, request, context):
    text = request.text
    result = self.model.predict(text)
    return text_service_pb2.TextResponse(processed_text=result)

def serve():
  # train model first
  ml_service = MlService()
  ml_service.train()

  # setup server
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  text_service_pb2_grpc.add_TextServiceServicer_to_server(TextService(ml_service), server)
  server.add_insecure_port('[::]:50051')
  print("Server started on port 50051...")
  server.start()
  server.wait_for_termination()


if __name__ == '__main__':
  serve()