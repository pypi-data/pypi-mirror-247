from observers \
    import Observer


class ApplicationFramework:
    def __init__(
        self
    ) -> None:
        self.observer = None

    def __del__(
        self
    ) -> None:
        pass
    
    def initialise(
        self
    ) -> None:
        pass

    def execution(
        self
    ) -> None:
        pass

    def garbage_collection(
        self
    ) -> None:
        pass

    def is_observer_empty(
        self
    ) -> bool:
        return self.observer is None

    def get_observer(
        self
    ) -> Observer:
        if self.is_observer_empty():
            self.set_observer(
                Observer()
            )

        return self.observer

    def set_observer(
        self,
        obj: Observer
    ) -> None:
        self.observer = obj
