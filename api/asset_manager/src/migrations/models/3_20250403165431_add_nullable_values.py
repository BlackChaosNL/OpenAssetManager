from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "organization" ADD "street_name" TEXT;
        ALTER TABLE "organization" ADD "country" VARCHAR(128);
        ALTER TABLE "organization" ADD "zip_code" VARCHAR(128);
        ALTER TABLE "organization" ADD "city" VARCHAR(128);
        ALTER TABLE "organization" ADD "state" VARCHAR(128);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "organization" DROP COLUMN "street_name";
        ALTER TABLE "organization" DROP COLUMN "country";
        ALTER TABLE "organization" DROP COLUMN "zip_code";
        ALTER TABLE "organization" DROP COLUMN "city";
        ALTER TABLE "organization" DROP COLUMN "state";"""
