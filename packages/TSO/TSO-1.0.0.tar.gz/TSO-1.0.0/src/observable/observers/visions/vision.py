from observers.visions.streams \
    import Streamable


class Vision:
    def __init__(
        self,
        stream: Streamable | None = None
    ) -> None:
        self.stream: None | Streamable = stream

    def __del__(
        self
    ) -> None:
        pass

    def get_stream(
        self
    ) -> Streamable | None:
        return self.stream

    def set_stream(
        self,
        stream: Streamable | None = None
    ) -> None:
        self.stream = stream

    def is_stream_empty(
        self
    ) -> bool:
        return self.stream is None

