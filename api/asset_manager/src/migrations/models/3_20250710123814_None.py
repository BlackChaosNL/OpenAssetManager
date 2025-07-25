from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "acl" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "READ" INT NOT NULL DEFAULT 0,
    "WRITE" INT NOT NULL DEFAULT 0,
    "REPORT" INT NOT NULL DEFAULT 0,
    "MANAGE" INT NOT NULL DEFAULT 0,
    "ADMIN" INT NOT NULL DEFAULT 0
) /* ACL */;
CREATE TABLE IF NOT EXISTS "organization" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL,
    "type" VARCHAR(128) NOT NULL,
    "street_name" TEXT,
    "zip_code" VARCHAR(128),
    "state" VARCHAR(128),
    "city" VARCHAR(128),
    "country" VARCHAR(128),
    "disabled" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "disabled_at" TIMESTAMP
) /* Organization */;
CREATE TABLE IF NOT EXISTS "user" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "email" VARCHAR(128) NOT NULL,
    "username" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "surname" TEXT NOT NULL,
    "password" VARCHAR(128),
    "disabled" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "disabled_at" TIMESTAMP
) /* User */;
CREATE TABLE IF NOT EXISTS "token" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "token_type" VARCHAR(128) NOT NULL DEFAULT 'Bearer',
    "access_token" TEXT,
    "refresh_token" TEXT,
    "disabled" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "disabled_at" TIMESTAMP,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
) /* Token */;
CREATE TABLE IF NOT EXISTS "membership" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "disabled" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "disabled_at" TIMESTAMP,
    "acl_id" CHAR(36) NOT NULL REFERENCES "acl" ("id") ON DELETE CASCADE,
    "organization_id" CHAR(36) REFERENCES "organization" ("id") ON DELETE SET NULL,
    "user_id" CHAR(36) REFERENCES "user" ("id") ON DELETE SET NULL
) /* Membership */;
CREATE TABLE IF NOT EXISTS "invite" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "receiver" VARCHAR(128) NOT NULL,
    "sender" CHAR(36) NOT NULL,
    "org_id" CHAR(36) NOT NULL,
    "message" TEXT,
    "accepted" INT NOT NULL DEFAULT 0,
    "disabled" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "disabled_at" TIMESTAMP,
    "acl_id" CHAR(36) NOT NULL REFERENCES "acl" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "Membership" (
    "organization_id" CHAR(36) NOT NULL REFERENCES "organization" ("id") ON DELETE NO ACTION,
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE NO ACTION
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_Membership_organiz_b0a446" ON "Membership" ("organization_id", "user_id");
CREATE TABLE IF NOT EXISTS "Membership" (
    "user_id" CHAR(36) NOT NULL REFERENCES "user" ("id") ON DELETE NO ACTION,
    "organization_id" CHAR(36) NOT NULL REFERENCES "organization" ("id") ON DELETE NO ACTION
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_Membership_user_id_cc48d3" ON "Membership" ("user_id", "organization_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
