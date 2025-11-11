-- Migration script to update CAR_TYPE_ENUM with new car types
-- Run this script on your PostgreSQL database

-- Note: PostgreSQL allows adding values to existing enums, but the order matters
-- If you get an error, you may need to recreate the enum type (see alternative approach below)

-- Add new car type values to CAR_TYPE_ENUM
DO $$ 
BEGIN
    -- Add new values if they don't exist
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'SEDAN_4_PLUS_1' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'CAR_TYPE_ENUM')) THEN
        ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE 'SEDAN_4_PLUS_1';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'NEW_SEDAN_2022_MODEL' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'CAR_TYPE_ENUM')) THEN
        ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE 'NEW_SEDAN_2022_MODEL';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'ETIOS_4_PLUS_1' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'CAR_TYPE_ENUM')) THEN
        ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE 'ETIOS_4_PLUS_1';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'SUV_6_PLUS_1' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'CAR_TYPE_ENUM')) THEN
        ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE 'SUV_6_PLUS_1';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'SUV_7_PLUS_1' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'CAR_TYPE_ENUM')) THEN
        ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE 'SUV_7_PLUS_1';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'INNOVA_6_PLUS_1' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'CAR_TYPE_ENUM')) THEN
        ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE 'INNOVA_6_PLUS_1';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'INNOVA_7_PLUS_1' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'CAR_TYPE_ENUM')) THEN
        ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE 'INNOVA_7_PLUS_1';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'INNOVA_CRYSTA_6_PLUS_1' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'CAR_TYPE_ENUM')) THEN
        ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE 'INNOVA_CRYSTA_6_PLUS_1';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM pg_enum WHERE enumlabel = 'INNOVA_CRYSTA_7_PLUS_1' AND enumtypid = (SELECT oid FROM pg_type WHERE typname = 'CAR_TYPE_ENUM')) THEN
        ALTER TYPE "CAR_TYPE_ENUM" ADD VALUE 'INNOVA_CRYSTA_7_PLUS_1';
    END IF;
    
    -- Update HATCHBACK if it exists as 'Hatchback' (old value)
    -- Note: You cannot change enum values, only add new ones
    -- If HATCHBACK needs to be changed from 'Hatchback' to 'HATCHBACK', 
    -- you'll need to use the alternative approach below
    
END $$;

-- Alternative approach if the above doesn't work (recreate enum type):
-- This approach requires more steps and should be done carefully in production
/*
-- Step 1: Create a new enum type with all values
CREATE TYPE "CAR_TYPE_ENUM_NEW" AS ENUM (
    'HATCHBACK',
    'SEDAN_4_PLUS_1',
    'NEW_SEDAN_2022_MODEL',
    'ETIOS_4_PLUS_1',
    'SUV',
    'SUV_6_PLUS_1',
    'SUV_7_PLUS_1',
    'INNOVA',
    'INNOVA_6_PLUS_1',
    'INNOVA_7_PLUS_1',
    'INNOVA_CRYSTA',
    'INNOVA_CRYSTA_6_PLUS_1',
    'INNOVA_CRYSTA_7_PLUS_1'
);

-- Step 2: Update all columns to use the new enum
ALTER TABLE new_orders ALTER COLUMN car_type TYPE "CAR_TYPE_ENUM_NEW" USING car_type::text::"CAR_TYPE_ENUM_NEW";
ALTER TABLE orders ALTER COLUMN car_type TYPE "CAR_TYPE_ENUM_NEW" USING car_type::text::"CAR_TYPE_ENUM_NEW";
ALTER TABLE hourly_rental ALTER COLUMN car_type TYPE "CAR_TYPE_ENUM_NEW" USING car_type::text::"CAR_TYPE_ENUM_NEW";

-- Step 3: Drop old enum and rename new one
DROP TYPE "CAR_TYPE_ENUM";
ALTER TYPE "CAR_TYPE_ENUM_NEW" RENAME TO "CAR_TYPE_ENUM";
*/


