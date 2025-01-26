import grpc
from proto import text_service_pb2, text_service_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:32768') as channel:
        stub = text_service_pb2_grpc.TextServiceStub(channel)
        text = input("Enter text: ")
        response = stub.ProcessText(text_service_pb2.TextRequest(text=text))
        print("Received processed text: " + response.processed_text)

if __name__ == '__main__':
    run()