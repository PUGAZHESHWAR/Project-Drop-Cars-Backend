-- data.sql

INSERT INTO admin (
    id,
    username,
    password,
    role,
    email,
    phone,
    organization_id,
    created_at
) VALUES (
    'a7f9f59e-1d4b-4bfa-9b57-3a8c0e4d4a11',
    'adminuser',
    'securepassword123',
    'Owner',
    'admin@example.com',
    '9876543210',
    '9cbd3e60-476a-4b1d-a81a-938e19ad15b1',
    NOW()
);
