def execute():
    def decorator(cls):
        class DecoratedClass(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def run(self):
                if hasattr(self, "test_arg"):
                    print("Running MyClass with arg={} and test_arg={}".format(self.arg, self.test_arg))
                else:
                    print("Running MyClass with arg={}".format(self.arg))

        instance = DecoratedClass(1)
        instance.run()
        return DecoratedClass

    return decorator


def test_data(test_arg=None):
    def decorator(cls):
        class DecoratedClass(cls):
            def __init__(self, *args, **kwargs):
                self.test_arg = test_arg
                super().__init__(*args, **kwargs)

        return DecoratedClass

    return decorator


@execute()
@test_data("A")
class MyClass:
    def __init__(self, arg):
        self.arg = arg

