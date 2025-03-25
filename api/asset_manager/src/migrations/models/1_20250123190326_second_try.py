from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "asset" ADD "disabled_at" TIMESTAMPTZ;
        ALTER TABLE "asset" ADD "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "asset" ADD "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "asset" DROP COLUMN "disabled_at";
        ALTER TABLE "asset" DROP COLUMN "modified_at";
        ALTER TABLE "asset" DROP COLUMN "created_at";"""
