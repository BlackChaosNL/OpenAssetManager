from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" ALTER COLUMN "refresh_token" TYPE TEXT USING "refresh_token"::TEXT;
        ALTER TABLE "token" ALTER COLUMN "access_token" TYPE TEXT USING "access_token"::TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "token" ALTER COLUMN "refresh_token" TYPE VARCHAR(128) USING "refresh_token"::VARCHAR(128);
        ALTER TABLE "token" ALTER COLUMN "access_token" TYPE VARCHAR(128) USING "access_token"::VARCHAR(128);"""
