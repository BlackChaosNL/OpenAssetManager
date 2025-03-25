from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "asset" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL
);
CREATE TABLE IF NOT EXISTS "acl" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "READ" BOOL NOT NULL  DEFAULT False,
    "WRITE" BOOL NOT NULL  DEFAULT False,
    "REPORT" BOOL NOT NULL  DEFAULT False,
    "MANAGE" BOOL NOT NULL  DEFAULT False,
    "ADMIN" BOOL NOT NULL  DEFAULT False
);
COMMENT ON TABLE "acl" IS 'ACL';
CREATE TABLE IF NOT EXISTS "organization" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "disabled_at" TIMESTAMPTZ,
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "type" VARCHAR(128) NOT NULL,
    "disabled" BOOL NOT NULL  DEFAULT False
);
COMMENT ON TABLE "organization" IS 'Organization';
CREATE TABLE IF NOT EXISTS "user" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "disabled_at" TIMESTAMPTZ,
    "id" UUID NOT NULL  PRIMARY KEY,
    "email" VARCHAR(128) NOT NULL,
    "username" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "surname" TEXT NOT NULL,
    "password" VARCHAR(128),
    "disabled" BOOL NOT NULL  DEFAULT False
);
COMMENT ON TABLE "user" IS 'User';
CREATE TABLE IF NOT EXISTS "token" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "disabled_at" TIMESTAMPTZ,
    "id" UUID NOT NULL  PRIMARY KEY,
    "token_type" VARCHAR(128) NOT NULL  DEFAULT 'Bearer',
    "access_token" VARCHAR(128),
    "refresh_token" VARCHAR(128),
    "disabled" BOOL NOT NULL  DEFAULT False,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "token" IS 'Token';
CREATE TABLE IF NOT EXISTS "membership" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "disabled_at" TIMESTAMPTZ,
    "id" UUID NOT NULL  PRIMARY KEY,
    "disabled" BOOL NOT NULL  DEFAULT False,
    "acl_id" UUID NOT NULL REFERENCES "acl" ("id") ON DELETE CASCADE,
    "organization_id" UUID NOT NULL REFERENCES "organization" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "membership" IS 'Membership';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
