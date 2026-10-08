from parser import parser as iperf_parser


class TestSuite:
    def test_iperf3_client_connection(self, client):
        result, error = client

        assert not error, f"Клієнт повернув помилку підключення: {error}"

        result_list = iperf_parser(result)
        assert result_list, "Парсер не знайшов жодного інтервалу у виводі iperf3"

        for value in result_list:
            assert value['Transfer'] > 2, (
                f"Interval {value['Interval']}: Transfer {value['Transfer']} "
                f"не перевищує 2 MBytes"
            )
            assert value['Bitrate'] > 20, (
                f"Interval {value['Interval']}: Bitrate {value['Bitrate']} "
                f"не перевищує 20 Mbits/sec"
            )
