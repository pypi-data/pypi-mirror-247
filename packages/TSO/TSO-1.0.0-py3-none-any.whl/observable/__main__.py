from framework \
    import ApplicationFramework


def main():
    framework = ApplicationFramework()

    framework.initialise()
    framework.execution()
    framework.garbage_collection()


entry_point: str = '__main__'

if __name__ == entry_point:
    main()
