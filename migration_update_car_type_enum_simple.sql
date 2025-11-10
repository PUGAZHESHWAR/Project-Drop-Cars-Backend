-- Simple migration script to add new car types to CAR_TYPE_ENUM
-- Run this script on your PostgreSQL database

-- Add new car type values to CAR_TYPE_ENUM
-- Note: If you get an error about enum values already existing, that's okay - they'll be skipped

ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE IF NOT EXISTS 'SEDAN_4_PLUS_1';
ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE IF NOT EXISTS 'NEW_SEDAN_2022_MODEL';
ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE IF NOT EXISTS 'ETIOS_4_PLUS_1';
ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE IF NOT EXISTS 'SUV_6_PLUS_1';
ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE IF NOT EXISTS 'SUV_7_PLUS_1';
ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE IF NOT EXISTS 'INNOVA_6_PLUS_1';
ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE IF NOT EXISTS 'INNOVA_7_PLUS_1';
ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE IF NOT EXISTS 'INNOVA_CRYSTA_6_PLUS_1';
ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE IF NOT EXISTS 'INNOVA_CRYSTA_7_PLUS_1';

-- Note: If your database has old values like 'Hatchback', 'Sedan', 'New Sedan', 'Innova', 'Innova Crysta'
-- and you want to use the new uppercase versions, you'll need to:
-- 1. Update existing data first
-- 2. Then use the alternative approach in migration_update_car_type_enum.sql to recreate the enum


