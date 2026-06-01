from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class AddressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    line: str
    city: str
    postal_code: str
    country: str


class AddressCreate(BaseModel):
    line: str
    city: str
    postal_code: str
    country: str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Postal code must contain only digits [0-9]")
        return value

    @model_validator(mode="after")
    def postal_code_length_for_country(self):
        country = self.country.strip().upper()
        postal_code_length = len(self.postal_code)

        if country in ("US", "USA") and postal_code_length != 5:
            raise ValueError("US ZIP codes must be exactly 5 digits")

        if country in ("IN", "INDIA") and postal_code_length != 6:
            raise ValueError("Indian PIN codes must be exactly 6 digits")

        return self


class AddressCreateRequest(AddressCreate):
    employee_id: int


class AddressUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    line: str | None = None
    city: str | None = None
    postal_code: str | None = None
    country: str | None = None

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, value: str | None) -> str | None:
        if value is not None and not value.isdigit():
            raise ValueError("Postal code must contain only digits [0-9]")
        return value