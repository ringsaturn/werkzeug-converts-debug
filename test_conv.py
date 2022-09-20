from unittest import TestCase, main

from werkzeug import routing as r


class TestConverts(TestCase):
    def test_default_converts(self):
        map = r.Map(
            [
                r.Rule("/foo-lng/<float(signed=True):lng>", endpoint="foo-lng"),
                r.Rule("/foo-lat/<float(signed=True):lat>", endpoint="foo-lat"),
                r.Rule(
                    "/foo-lnglat/<float(signed=True):lng>,<float(signed=True):lat>",
                    endpoint="foo-lnglat",
                ),
            ]
        )

        adapter = map.bind("example.co", "/")

        assert adapter.match("/foo-lng/116.12") == ("foo-lng", {"lng": 116.12})
        assert adapter.match("/foo-lat/116.12") == ("foo-lat", {"lat": 116.12})
        assert adapter.match("/foo-lnglat/116.12,116.12") == (
            "foo-lnglat",
            {"lng": 116.12, "lat": 116.12},
        )
        assert adapter.match("/foo-lnglat/116.12,39.34") == (
            "foo-lnglat",
            {"lng": 116.12, "lat": 39.34},
        )
        assert adapter.match("/foo-lnglat/116.12,-39.34") == (
            "foo-lnglat",
            {"lng": 116.12, "lat": -39.34},
        )

    def test_custom_converts(self):
        try:
            from werkzeug.routing.converters import NumberConverter
        except:
            from werkzeug.routing import NumberConverter

        class FloatConverter(NumberConverter):
            """FloatConverter.
            Copy from werkzeug and replace regex.
            """

            regex = r"-?\d+(\.\d+)?"
            num_convert = float
            part_isolating = True

            def __init__(
                self,
                map,
                min=None,
                max=None,
                signed: bool = False,
            ) -> None:
                super().__init__(map, min=min, max=max, signed=signed)  # type: ignore

        map = r.Map(
            [
                r.Rule("/foo-lng/<float(signed=True):lng>", endpoint="foo-lng"),
                r.Rule("/foo-lat/<float(signed=True):lat>", endpoint="foo-lat"),
                r.Rule(
                    "/foo-lnglat/<float(signed=True):lng>,<float(signed=True):lat>",
                    endpoint="foo-lnglat",
                ),
            ],
            converters={"float": FloatConverter},
        )

        adapter = map.bind("example.co", "/")

        assert adapter.match("/foo-lng/116.12") == ("foo-lng", {"lng": 116.12})
        assert adapter.match("/foo-lat/116.12") == ("foo-lat", {"lat": 116.12})
        assert adapter.match("/foo-lnglat/116.12,116.12") == (
            "foo-lnglat",
            {"lng": 116.12, "lat": 116.12},
        )
        assert adapter.match("/foo-lnglat/116.12,39.34") == (
            "foo-lnglat",
            {"lng": 116.12, "lat": 39.34},
        )
        assert adapter.match("/foo-lnglat/116.12,-39.34") == (
            "foo-lnglat",
            {"lng": 116.12, "lat": -39.34},
        )


if __name__ == "__main__":
    main()
