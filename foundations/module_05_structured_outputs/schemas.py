from pydantic import BaseModel, Field

class SnowFlakeMetadata(BaseModel):
    """"Structured output returned by the LLM."""
    server: str = Field(description="Snowflake server hostname")
    warehouse: str = Field(description="Snowflake warehouse")
    database : str = Field(description="Snowflake database")
    database_schema: str | None = Field(default=None,
                               description="Databse Schema if present")
    table_name: str | None = Field(default=None,
                               description="Snowflake table name if present")
    role: str| None = Field(default=None,
                            description="Snowflake role if preesent")
    