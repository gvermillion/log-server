import socketserver
import logging
import struct
import pickle
import datetime


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    log_filename = '/workspaces/codespaces-jupyter/notebooks/server.log'

    def handle(self):
        with open(self.log_filename, "a") as log_file:
            while True:
                # Read the length of the incoming log record
                chunk = self.connection.recv(4)
                if len(chunk) < 4:
                    break
                slen = struct.unpack('>L', chunk)[0]

                # Read the log record data based on the length
                chunk = self.connection.recv(slen)
                while len(chunk) < slen:
                    chunk += self.connection.recv(slen - len(chunk))

                # Unpickle the data and create a log record
                obj = self.unPickle(chunk)
                record = logging.makeLogRecord(obj)

                # Write the log message to the file
                log_file.write(self.format_record(record) + "\n")
                log_file.flush()

    def unPickle(self, data):
        return pickle.loads(data)

    def format_record(self, record):
        log_time: str = (
            datetime
            .datetime
            .fromtimestamp(
                record.created
            )
            .strftime('%Y-%m-%d %H:%M:%S')
        )
        msg = f"[{log_time} {record.filename}:{record.lineno}] {record.levelname}: {record.getMessage()}"
        print(msg)
        return msg

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = socketserver.TCPServer(('127.0.0.1', 9981), LogRecordStreamHandler)
    open(LogRecordStreamHandler.log_filename, 'a').close()
    print("Starting TCP log server...")
    server.serve_forever()
