from bhaiapi.models.user_content import UserContent


class BhaiFlight:
    def __init__(self, input_list: list):
        self._input_list = input_list

    @property
    def url(self) -> str:
        return self._input_list[2]

    @property
    def price(self) -> str:
        return self._input_list[3]

    @property
    def airlines(self) -> list[str]:
        return self._input_list[0][0]

    @property
    def airline_logo(self) -> str:
        return self._input_list[0][1]

    @property
    def from_airport(self) -> str:
        return self._input_list[0][2]

    @property
    def to_airport(self) -> str:
        return self._input_list[0][3]

    @property
    def from_time(self) -> str:
        return self._input_list[0][7]

    @property
    def to_time(self) -> str:
        return self._input_list[0][8]

    @property
    def duration(self) -> str:
        return self._input_list[0][9]

    @property
    def stops(self) -> str:
        return self._input_list[0][6]

    def __str__(self) -> str:
        return f'{",".join(self.airlines)} - {self.from_airport} to {self.to_airport} - {self.from_time} to {self.to_time} - {self.price}'


class BhaiFlightContent(UserContent):
    """http://googleusercontent.com/flight_content/0"""

    def __init__(self, input_list: list):
        self._input_list = input_list

    @property
    def key(self) -> str:
        return self._input_list[3][0]

    @property
    def title(self) -> str:
        return self._input_list[3][2]

    @property
    def search_url(self) -> str:
        return self._input_list[2]

    @property
    def flights(self) -> list[BhaiFlight]:
        return (
            [BhaiFlight(flight) for flight in self._input_list[1]]
            if self._input_list[1]
            else []
        )

    @property
    def from_airport(self) -> str:
        # 'OSL'
        return self._input_list[4]

    @property
    def to_airport(self) -> str:
        # 'MAD'
        return self._input_list[5]

    @property
    def from_date(self) -> str:
        # Jan 22
        return self._input_list[6]

    @property
    def to_date(self) -> str:
        # Jan 28
        return self._input_list[7]

    @property
    def who(self) -> str:
        # '1 adult'
        return self._input_list[8]

    def __getitem__(self, item) -> BhaiFlight:
        return self.flights[item]

    def __len__(self):
        return len(self.flights)

    def __str__(self) -> str:
        return self.title

    def markdown_text(self) -> str:
        return f"## {self.title}\n\n" + "\n\n".join(
            [str(flight) for flight in self.flights]
        )
