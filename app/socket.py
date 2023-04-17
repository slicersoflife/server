from flask_socketio import emit, SocketIO


def add_events(socket: SocketIO):
    @socket.on("call")
    def handle_call(json):
        emit("call", {"callerId": json.get("callerId"), "rtcMessage": json.get("rtcMessage")}, to=json.get("calleeId"))

    @socket.on("answer")
    def handle_answer(json):
        emit("answer", {"calleeId": json.get("calleeId"), "rtcMessage": json.get("rtcMessage")},
             to=json.get("callerId"))

    @socket.on("ICECandidate")
    def handle_candidate(json):
        emit("ICECandidate", {"sender": json.get("sender"), "rtcMessage": json.get("rtcMessage")},
             to=json.get("receiver"))
