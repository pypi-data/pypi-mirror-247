from abc \
    import (
        ABC,
        abstractmethod
)


class Streamable(
    ABC
):
    def __init__(
        self
    ):
        self.done: bool = False
        self.build()

    def __del__(
        self
    ):
        self.cleanup()

    def is_done(
        self
    ) -> bool:
        return self.done

    def set_done(
        self,
        value: bool
    ) -> None:
        self.done = value

    def flag_is_done(
        self
    ) -> None:
        self.set_done(
            True
        )

    @abstractmethod
    def build(
        self
    ):
        raise NotImplemented(
            "Please implement me in class"
        )

    @abstractmethod
    def fetch(
        self
    ):
        raise NotImplemented(
            "Please implement me in class"
        )

    @abstractmethod
    def cleanup(
        self
    ):
        raise NotImplemented(
            "Please implement me in class"
        )

    def call_finish_event(
        self
    ) -> None:
        raise IOError(
            'Stream is finished'
        )
    