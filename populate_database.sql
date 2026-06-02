USE otj;

-- Insert users
INSERT INTO
    `users` (
        `user_id`,
        `username`,
        `password_hash`,
        `email`,
        `first_name`,
        `last_name`,
        `location`,
        `description`,
        `profile_image`,
        `role`,
        `status`,
        `created_at`,
        `email_public`,
        `name_public`,
        `profile_public`,
        `places_public`,
        `likes_public`,
        `comments_public`,
        `achievement_count`
    )
VALUES
    (
        1,
        'john_doe',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'john.doe@example.com',
        'John',
        'Doe',
        'Auckland',
        'Admin of the system',
        '/static/uploads/1_profile.jpg',
        'admin',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        FALSE,
        TRUE,
        FALSE,
        TRUE,
        FALSE,
        5
    ),
    (
        2,
        'jane_smith',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'jane.smith@example.com',
        'Jane',
        'Smith',
        'Wellington',
        'System administrator',
        NULL,
        'admin',
        'active',
        CURRENT_TIMESTAMP,
        FALSE,
        TRUE,
        FALSE,
        TRUE,
        FALSE,
        TRUE,
        5
    ),
    (
        3,
        'bob_jones',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'bob.jones@example.com',
        'Bob',
        'Jones',
        'Christchurch',
        'Handles user management',
        '/static/uploads/3_profile.jpg',
        'admin',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        5
    ),
    (
        4,
        'alice_williams',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'alice.williams@example.com',
        'Alice',
        'Williams',
        'Hamilton',
        'Content editor',
        NULL,
        'editor',
        'active',
        CURRENT_TIMESTAMP,
        FALSE,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        4
    ),
    (
        5,
        'mike_brown',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'mike.brown@example.com',
        'Mike',
        'Brown',
        'Tauranga',
        'Editor for travel content',
        '/static/uploads/5_profile.jpg',
        'editor',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        FALSE,
        FALSE,
        FALSE,
        TRUE,
        TRUE,
        4
    ),
    (
        6,
        'susan_davis',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'susan.davis@example.com',
        'Susan',
        'Davis',
        'Napier',
        'Editor for event content',
        NULL,
        'editor',
        'active',
        CURRENT_TIMESTAMP,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        FALSE,
        4
    ),
    (
        7,
        'karen_miller',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'karen.miller@example.com',
        'Karen',
        'Miller',
        'Dunedin',
        'Editor for location content',
        NULL,
        'editor',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        FALSE,
        FALSE,
        4
    ),
    (
        8,
        'james_wilson',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'james.wilson@example.com',
        'James',
        'Wilson',
        'Palmerston North',
        'Editor for user stories',
        NULL,
        'editor',
        'active',
        CURRENT_TIMESTAMP,
        FALSE,
        TRUE,
        FALSE,
        TRUE,
        TRUE,
        TRUE,
        4
    ),
    (
        9,
        'tom_moore',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'tom.moore@example.com',
        'Tom',
        'Moore',
        'Rotorua',
        'Travel enthusiast',
        NULL,
        'editor',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        FALSE,
        TRUE,
        FALSE,
        TRUE,
        TRUE,
        4
    ),
    (
        10,
        'emma_taylor',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'emma.taylor@example.com',
        'Emma',
        'Taylor',
        'Nelson',
        'Adventure seeker',
        '/static/uploads/10_profile.jpg',
        'moderator',
        'active',
        CURRENT_TIMESTAMP,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        FALSE,
        TRUE,
        4
    ),
    (
        11,
        'lucas_anderson',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'lucas.anderson@example.com',
        'Lucas',
        'Anderson',
        'New Plymouth',
        'Backpacker',
        NULL,
        'moderator',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        4
    ),
    (
        12,
        'olivia_thomas',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'olivia.thomas@example.com',
        'Olivia',
        'Thomas',
        'Whangarei',
        'Nature lover',
        '/static/uploads/12_profile.jpg',
        'supporttech',
        'active',
        CURRENT_TIMESTAMP,
        FALSE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        FALSE,
        4
    ),
    (
        13,
        'liam_jackson',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'liam.jackson@example.com',
        'Liam',
        'Jackson',
        'Invercargill',
        'Cultural explorer',
        NULL,
        'supporttech',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        FALSE,
        FALSE,
        TRUE,
        4
    ),
    (
        14,
        'ava_white',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'ava.white@example.com',
        'Ava',
        'White',
        'Gisborne',
        'City traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        FALSE,
        FALSE,
        TRUE,
        TRUE,
        TRUE,
        FALSE,
        4
    ),
    (
        15,
        'noah_harris',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'noah.harris@example.com',
        'Noah',
        'Harris',
        'Queenstown',
        'Beach lover',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        FALSE,
        FALSE,
        TRUE,
        FALSE,
        TRUE,
        4
    ),
    (
        16,
        'isabella_martin',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'isabella.martin@example.com',
        'Isabella',
        'Martin',
        'Blenheim',
        'Mountain climber',
        '/static/uploads/16_profile.jpg',
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        TRUE,
        4
    ),
    (
        17,
        'mason_lee',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'mason.lee@example.com',
        'Mason',
        'Lee',
        'Timaru',
        'Desert explorer',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        4
    ),
    (
        18,
        'sophia_clark',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'sophia.clark@example.com',
        'Sophia',
        'Clark',
        'Taupo',
        'Foodie traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        FALSE,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        4
    ),
    (
        19,
        'ben_lewis',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'ben.lewis@example.com',
        'Ben',
        'Lewis',
        'Palmerston North',
        'Wildlife enthusiast',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        FALSE,
        FALSE,
        TRUE,
        TRUE,
        0
    ),
    (
        20,
        'charlotte_robinson',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'charlotte.robinson@example.com',
        'Charlotte',
        'Robinson',
        'Hastings',
        'Cultural traveler',
        '/static/uploads/20_profile.jpg',
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        FALSE,
        0
    ),
    (
        21,
        'william_wright',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'william.wright@example.com',
        'William',
        'Wright',
        'Whanganui',
        'Adventure traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        0
    ),
    (
        22,
        'mia_hall',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'mia.hall@example.com',
        'Mia',
        'Hall',
        'Masterton',
        'Nature traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        FALSE,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        0
    ),
    (
        23,
        'elijah_allen',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'elijah.allen@example.com',
        'Elijah',
        'Allen',
        'Oamaru',
        'City explorer',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        24,
        'ava_young',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'ava.young@example.com',
        'Ava',
        'Young',
        'Ashburton',
        'Beach explorer',
        '/static/uploads/24_profile.jpg',
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        25,
        'james_kim',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'james.kim@example.com',
        'James',
        'Kim',
        'Greymouth',
        'Mountain explorer',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        26,
        'sophia_lee',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'sophia.lee@example.com',
        'Sophia',
        'Lee',
        'Kaikoura',
        'Desert traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        27,
        'liam_harris',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'liam.harris@example.com',
        'Liam',
        'Harris',
        'Motueka',
        'Food traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        28,
        'olivia_james',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'olivia.james@example.com',
        'Olivia',
        'James',
        'Tokoroa',
        'Wildlife traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        29,
        'noah_martin',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'noah.martin@example.com',
        'Noah',
        'Martin',
        'Wairoa',
        'Cultural traveler',
        '/static/uploads/29_profile.jpg',
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        30,
        'charlotte_thompson',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'charlotte.thompson@example.com',
        'Charlotte',
        'Thompson',
        'Hokitika',
        'Adventure traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        31,
        'ben_johnson',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'ben.johnson@example.com',
        'Ben',
        'Johnson',
        'Westport',
        'Nature traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        32,
        'mia_smith',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'mia.smith@example.com',
        'Mia',
        'Smith',
        'Motueka',
        'City traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        33,
        'elijah_brown',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'elijah.brown@example.com',
        'Elijah',
        'Brown',
        'Oamaru',
        'Beach traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        0
    ),
    (
        34,
        'ava_jones',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'ava.jones@example.com',
        'Ava',
        'Jones',
        'Ashburton',
        'Mountain traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        0
    ),
    (
        35,
        'james_Foster',
        '$2b$12$6JOidtBf4q.pyN.3.u4k9.IcEKYqFe2EFVo5Opi.zCnsns568a/6u',
        'james.foster@example.com',
        'James',
        'Foster',
        'Greymouth',
        'Desert traveler',
        NULL,
        'traveller',
        'active',
        CURRENT_TIMESTAMP,
        TRUE,
        TRUE,
        FALSE,
        TRUE,
        TRUE,
        TRUE,
        0
    );

-- Insert journeys
INSERT INTO
    `journeys` (
        `journey_id`,
        `user_id`,
        `title`,
        `description`,
        `start_date`,
        `status`,
        `is_hidden`,
        `created_at`,
        `photo`
    )
VALUES
    (
        1,
        1,
        'Exploring New York',
        'A journey through the streets of New York',
        '2023-01-01',
        'published',
        FALSE,
        '2025-01-05 10:15:00',
        NULL
    ),
    (
        2,
        2,
        'California Adventure',
        'Exploring the beautiful state of California',
        '2023-02-01',
        'published',
        FALSE,
        '2025-01-10 14:30:00',
        NULL
    ),
    (
        3,
        3,
        'Chicago Landmarks',
        'Visiting famous landmarks in Chicago',
        '2023-03-01',
        'published',
        FALSE,
        '2025-01-15 09:45:00',
        NULL
    ),
    (
        4,
        4,
        'San Francisco Tour',
        'A tour of San Francisco',
        '2023-04-01',
        'public',
        FALSE,
        '2025-01-20 11:00:00',
        NULL
    ),
    (
        5,
        5,
        'Seattle Sights',
        'Discovering the sights of Seattle',
        '2023-05-01',
        'public',
        FALSE,
        '2025-01-25 16:20:00',
        NULL
    ),
    (
        6,
        6,
        'Austin Music Scene',
        'Exploring the music scene in Austin',
        '2023-06-01',
        'public',
        FALSE,
        '2025-01-30 08:10:00',
        NULL
    ),
    (
        7,
        7,
        'Denver Mountains',
        'Hiking in the mountains of Denver',
        '2023-07-01',
        'public',
        FALSE,
        '2025-02-05 13:35:00',
        NULL
    ),
    (
        8,
        8,
        'Boston History',
        'A historical tour of Boston',
        '2023-08-01',
        'public',
        FALSE,
        '2025-02-10 17:50:00',
        NULL
    ),
    (
        9,
        9,
        'Miami Beaches',
        'Relaxing on the beaches of Miami',
        '2023-09-01',
        'public',
        FALSE,
        '2025-02-15 12:25:00',
        NULL
    ),
    (
        10,
        10,
        'Orlando Theme Parks',
        'Visiting theme parks in Orlando',
        '2023-10-01',
        'public',
        FALSE,
        '2025-02-20 15:40:00',
        NULL
    ),
    (
        11,
        11,
        'Auckland City Tour',
        'Exploring the city of Auckland',
        '2023-11-01',
        'public',
        FALSE,
        '2025-02-25 10:05:00',
        NULL
    ),
    (
        12,
        12,
        'Wellington Cultural Experience',
        'Discovering the culture of Wellington',
        '2023-12-01',
        'public',
        FALSE,
        '2025-03-01 14:50:00',
        'journey_photo_1.jpg'
    ),
    (
        13,
        13,
        'Christchurch Adventure',
        'An adventure in Christchurch',
        '2023-01-15',
        'public',
        FALSE,
        '2025-01-03 09:00:00',
        'journey_photo_2.jpg'
    ),
    (
        14,
        14,
        'Sydney Harbour',
        'Visiting the Sydney Harbour',
        '2023-02-15',
        'public',
        FALSE,
        '2025-01-08 11:30:00',
        'journey_photo_3.jpg'
    ),
    (
        15,
        15,
        'Great Barrier Reef',
        'Exploring the Great Barrier Reef',
        '2023-03-15',
        'public',
        FALSE,
        '2025-01-13 14:00:00',
        'journey_photo_4.jpg'
    ),
    (
        16,
        16,
        'Tokyo City Lights',
        'Experiencing the lights of Tokyo',
        '2023-04-15',
        'public',
        FALSE,
        '2025-01-18 16:45:00',
        'journey_photo_5.jpg'
    ),
    (
        17,
        17,
        'Paris Landmarks',
        'Visiting famous landmarks in Paris',
        '2023-05-15',
        'public',
        FALSE,
        '2025-01-23 09:15:00',
        NULL
    ),
    (
        18,
        18,
        'London Historical Tour',
        'A historical tour of London',
        '2023-06-15',
        'public',
        FALSE,
        '2025-01-28 12:30:00',
        NULL
    ),
    (
        19,
        1,
        'Rome Ancient Sites',
        'Exploring ancient sites in Rome',
        '2023-07-15',
        'public',
        FALSE,
        '2025-02-02 15:00:00',
        NULL
    ),
    (
        20,
        2,
        'Berlin Wall Tour',
        'A tour of the Berlin Wall',
        '2023-08-15',
        'public',
        FALSE,
        '2025-02-07 17:20:00',
        NULL
    ),
    (
        21,
        1,
        'Mountain Retreat',
        'A private journey to the mountains',
        '2023-09-01',
        'private',
        FALSE,
        '2025-02-12 10:40:00',
        NULL
    ),
    (
        22,
        2,
        'Beach Getaway',
        'A private journey to the beach',
        '2023-10-01',
        'private',
        FALSE,
        '2025-02-17 13:55:00',
        NULL
    ),
    (
        23,
        3,
        'Secret Hideaway',
        'A hidden journey to a secret location',
        '2023-11-01',
        'private',
        TRUE,
        '2025-02-22 16:10:00',
        NULL
    ),
    (
        24,
        4,
        'Mystery Adventure',
        'Another hidden journey to a secret location',
        '2023-12-01',
        'private',
        TRUE,
        '2025-02-27 09:25:00',
        NULL
    ),
    (
        25,
        5,
        'Countryside Escape',
        'A private journey to the countryside',
        '2023-09-15',
        'private',
        FALSE,
        '2025-01-04 11:50:00',
        NULL
    ),
    (
        26,
        6,
        'Urban Exploration',
        'A private journey to the city',
        '2023-10-15',
        'private',
        FALSE,
        '2025-01-09 14:05:00',
        NULL
    ),
    (
        27,
        7,
        'Desert Expedition',
        'A private journey to the desert',
        '2023-11-15',
        'private',
        FALSE,
        '2025-01-14 16:20:00',
        NULL
    ),
    (
        28,
        8,
        'Forest Adventure',
        'A private journey to the forest',
        '2023-12-15',
        'private',
        FALSE,
        '2025-01-19 09:35:00',
        NULL
    ),
    (
        29,
        9,
        'Island Retreat',
        'A private journey to the island',
        '2023-01-20',
        'private',
        FALSE,
        '2025-01-24 11:50:00',
        NULL
    ),
    (
        30,
        10,
        'Cultural Journey',
        'A private journey to a cultural site',
        '2023-02-20',
        'private',
        FALSE,
        '2025-01-29 14:05:00',
        NULL
    ),
    (
        31,
        11,
        'Historical Journey',
        'A private journey to a historical site',
        '2023-03-20',
        'private',
        FALSE,
        '2025-02-03 16:20:00',
        NULL
    ),
    (
        32,
        12,
        'Adventure Journey',
        'A private journey to an adventure site',
        '2023-04-20',
        'private',
        FALSE,
        '2025-02-08 09:35:00',
        NULL
    ),
    (
        33,
        13,
        'Nature Journey',
        'A private journey to a nature site',
        '2023-05-20',
        'private',
        FALSE,
        '2025-02-13 11:50:00',
        NULL
    ),
    (
        34,
        20,
        'New York Trip',
        'A journey to New York',
        '2025-05-21',
        'published',
        FALSE,
        '2025-05-28 11:50:00',
        'journey_photo_6.jpg'
    ),
    (
        35,
        22,
        'Botanic Garden',
        'A day at botanic garden',
        '2025-05-27',
        'private',
        FALSE,
        '2025-05-27 11:50:00',
        NULL
    );

-- Insert locations
INSERT INTO
    `locations` (`location_id`, `location_name`)
VALUES
    (1, 'Central Park, New York'),
    (2, 'Golden Gate Bridge, San Francisco'),
    (3, 'Space Needle, Seattle'),
    (4, 'Mount Bonnell, Austin'),
    (5, 'Rocky Mountain National Park, Denver'),
    (6, 'Freedom Trail, Boston'),
    (7, 'South Beach, Miami'),
    (8, 'Disney World, Orlando'),
    (9, 'Sky Tower, Auckland'),
    (10, 'Te Papa Museum, Wellington'),
    (11, 'Christchurch Botanic Gardens, Christchurch'),
    (12, 'Sydney Opera House, Sydney'),
    (13, 'Great Barrier Reef, Queensland'),
    (14, 'Shibuya Crossing, Tokyo'),
    (15, 'Eiffel Tower, Paris'),
    (16, 'Tower of London, London'),
    (17, 'Colosseum, Rome'),
    (18, 'Berlin Wall Memorial, Berlin'),
    (19, 'Blue Ridge Mountains, Asheville'),
    (20, 'Waikiki Beach, Honolulu'),
    (21, 'Grand Canyon, Arizona'),
    (22, 'Yellowstone National Park, Wyoming'),
    (23, 'Banff National Park, Canada'),
    (24, 'Santorini, Greece'),
    (25, 'Machu Picchu, Peru'),
    (26, 'Botanic Garden, Wellington');

-- Insert events
INSERT INTO
    `events` (
        `event_id`,
        `journey_id`,
        `title`,
        `description`,
        `start_datetime`,
        `end_datetime`,
        `location_id`,
        `comments_count`,
        `created_at`
    )
VALUES
    (
        1,
        1,
        'Central Park Walk',
        'A walk through Central Park',
        '2023-01-01 10:00:00',
        '2023-01-01 12:00:00',
        1,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        2,
        1,
        'Times Square Visit',
        'Exploring the vibrant Times Square',
        '2025-01-06 10:00:00',
        '2025-01-06 12:00:00',
        1,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        3,
        1,
        'Brooklyn Bridge Walk',
        'A scenic walk across Brooklyn Bridge',
        '2025-01-07 14:00:00',
        '2025-01-07 16:00:00',
        1,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        4,
        2,
        'Golden Gate Sunset',
        'Watching the sunset at Golden Gate Bridge',
        '2025-01-11 17:00:00',
        '2025-01-11 19:00:00',
        2,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        5,
        2,
        'Alcatraz Island Tour',
        'A tour of the historic Alcatraz Island',
        '2025-01-12 10:00:00',
        '2025-01-12 13:00:00',
        2,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        6,
        3,
        'Space Needle Visit',
        'Enjoying the view from the Space Needle',
        '2025-01-16 11:00:00',
        '2025-01-16 13:00:00',
        3,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        7,
        3,
        'Pike Place Market',
        'Exploring the famous Pike Place Market',
        '2025-01-17 14:00:00',
        '2025-01-17 16:00:00',
        3,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        8,
        4,
        'Mount Bonnell Hike',
        'Hiking to the top of Mount Bonnell',
        '2025-01-21 09:00:00',
        '2025-01-21 11:00:00',
        4,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        9,
        4,
        'Austin Live Music',
        'Enjoying live music in Austin',
        '2025-01-22 19:00:00',
        '2025-01-22 21:00:00',
        4,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        10,
        5,
        'Rocky Mountain Hike',
        'Exploring the trails in Rocky Mountain National Park',
        '2025-01-26 08:00:00',
        '2025-01-26 12:00:00',
        5,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        11,
        5,
        'Denver Art Museum',
        'Visiting the Denver Art Museum',
        '2025-01-27 14:00:00',
        '2025-01-27 16:00:00',
        5,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        12,
        6,
        'Freedom Trail Walk',
        'Walking the historic Freedom Trail',
        '2025-02-11 10:00:00',
        '2025-02-11 12:00:00',
        6,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        13,
        6,
        'Boston Tea Party Museum',
        'Learning history at the Boston Tea Party Museum',
        '2025-02-12 14:00:00',
        '2025-02-12 16:00:00',
        6,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        14,
        7,
        'South Beach Relaxation',
        'Relaxing on the beautiful South Beach',
        '2025-02-16 09:00:00',
        '2025-02-16 12:00:00',
        7,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        15,
        7,
        'Miami Art Deco Tour',
        'Exploring the Art Deco District in Miami',
        '2025-02-17 14:00:00',
        '2025-02-17 16:00:00',
        7,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        16,
        8,
        'Disney World Adventure',
        'A fun day at Disney World',
        '2025-02-21 10:00:00',
        '2025-02-21 18:00:00',
        8,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        17,
        8,
        'Orlando Science Center',
        'Exploring the Orlando Science Center',
        '2025-02-22 11:00:00',
        '2025-02-22 14:00:00',
        8,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        18,
        9,
        'Sky Tower Observation',
        'Enjoying the view from Sky Tower',
        '2025-02-26 10:00:00',
        '2025-02-26 12:00:00',
        9,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        19,
        9,
        'Auckland Zoo Visit',
        'Exploring the Auckland Zoo',
        '2025-02-27 14:00:00',
        '2025-02-27 16:00:00',
        9,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        20,
        10,
        'Te Papa Museum Tour',
        'Discovering the exhibits at Te Papa Museum',
        '2025-03-02 10:00:00',
        '2025-03-02 12:00:00',
        10,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        21,
        10,
        'Wellington Cable Car',
        'Riding the Wellington Cable Car',
        '2025-03-03 14:00:00',
        '2025-03-03 16:00:00',
        10,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        22,
        1,
        'Empire State Building Tour',
        'A visit to the iconic Empire State Building',
        '2025-01-08 10:00:00',
        '2025-01-08 12:00:00',
        1,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        23,
        1,
        'Statue of Liberty Visit',
        'Exploring the Statue of Liberty',
        '2025-01-09 14:00:00',
        '2025-01-09 16:00:00',
        1,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        24,
        1,
        'Broadway Show',
        'Watching a Broadway show',
        '2025-01-10 19:00:00',
        '2025-01-10 22:00:00',
        1,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        25,
        2,
        'Yosemite National Park',
        'Exploring Yosemite National Park',
        '2025-01-13 09:00:00',
        '2025-01-13 17:00:00',
        2,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        26,
        2,
        'Hollywood Walk of Fame',
        'Walking along the Hollywood Walk of Fame',
        '2025-01-14 10:00:00',
        '2025-01-14 12:00:00',
        2,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        27,
        2,
        'Santa Monica Pier',
        'Relaxing at Santa Monica Pier',
        '2025-01-15 15:00:00',
        '2025-01-15 18:00:00',
        2,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        28,
        3,
        'Millennium Park',
        'Exploring Millennium Park',
        '2025-01-18 10:00:00',
        '2025-01-18 12:00:00',
        3,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        29,
        3,
        'Willis Tower Skydeck',
        'Enjoying the view from Willis Tower Skydeck',
        '2025-01-19 14:00:00',
        '2025-01-19 16:00:00',
        3,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        30,
        3,
        'Navy Pier',
        'Walking along Navy Pier',
        '2025-01-20 17:00:00',
        '2025-01-20 19:00:00',
        3,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        31,
        4,
        'Lombard Street',
        'Visiting the famous Lombard Street',
        '2025-01-23 10:00:00',
        '2025-01-23 12:00:00',
        4,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        32,
        4,
        'Fisherman\'s Wharf',
        'Exploring Fisherman\'s Wharf',
        '2025-01-24 14:00:00',
        '2025-01-24 16:00:00',
        4,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        33,
        4,
        'Chinatown',
        'Walking through Chinatown',
        '2025-01-25 17:00:00',
        '2025-01-25 19:00:00',
        4,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        34,
        5,
        'Kerry Park',
        'Enjoying the view from Kerry Park',
        '2025-01-28 10:00:00',
        '2025-01-28 12:00:00',
        5,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        35,
        5,
        'Museum of Pop Culture',
        'Exploring the Museum of Pop Culture',
        '2025-01-29 14:00:00',
        '2025-01-29 16:00:00',
        5,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        36,
        5,
        'Seattle Aquarium',
        'Visiting the Seattle Aquarium',
        '2025-01-30 17:00:00',
        '2025-01-30 19:00:00',
        5,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        37,
        6,
        'Zilker Park',
        'Relaxing at Zilker Park',
        '2025-02-02 10:00:00',
        '2025-02-02 12:00:00',
        6,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        38,
        6,
        '6th Street Music',
        'Enjoying live music on 6th Street',
        '2025-02-03 19:00:00',
        '2025-02-03 22:00:00',
        6,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        39,
        6,
        'Barton Springs Pool',
        'Swimming at Barton Springs Pool',
        '2025-02-04 14:00:00',
        '2025-02-04 16:00:00',
        6,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        40,
        7,
        'Red Rocks Amphitheatre',
        'Exploring Red Rocks Amphitheatre',
        '2025-02-07 10:00:00',
        '2025-02-07 12:00:00',
        7,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        41,
        7,
        'Denver Botanic Gardens',
        'Walking through Denver Botanic Gardens',
        '2025-02-08 14:00:00',
        '2025-02-08 16:00:00',
        7,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        42,
        7,
        'Coors Brewery Tour',
        'Touring the Coors Brewery',
        '2025-02-09 17:00:00',
        '2025-02-09 19:00:00',
        7,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        43,
        8,
        'Boston Common',
        'Relaxing at Boston Common',
        '2025-02-12 10:00:00',
        '2025-02-12 12:00:00',
        8,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        44,
        8,
        'Harvard University Tour',
        'Exploring Harvard University',
        '2025-02-13 14:00:00',
        '2025-02-13 16:00:00',
        8,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        45,
        8,
        'Fenway Park',
        'Visiting Fenway Park',
        '2025-02-14 17:00:00',
        '2025-02-14 19:00:00',
        8,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        46,
        9,
        'Ocean Drive Walk',
        'A scenic walk along Ocean Drive',
        '2025-02-18 10:00:00',
        '2025-02-18 12:00:00',
        7,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        47,
        9,
        'Beach Volleyball',
        'Playing volleyball on South Beach',
        '2025-02-19 14:00:00',
        '2025-02-19 16:00:00',
        7,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        48,
        9,
        'Sunset Cruise',
        'Enjoying a sunset cruise in Miami',
        '2025-02-20 17:00:00',
        '2025-02-20 19:00:00',
        7,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        49,
        9,
        'Art Deco District Tour',
        'Exploring the Art Deco District',
        '2025-02-21 10:00:00',
        '2025-02-21 12:00:00',
        7,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        50,
        9,
        'Snorkeling Adventure',
        'Snorkeling in the clear waters of Miami',
        '2025-02-22 14:00:00',
        '2025-02-22 16:00:00',
        7,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        51,
        10,
        'Magic Kingdom Visit',
        'Exploring the Magic Kingdom at Disney World',
        '2025-02-23 10:00:00',
        '2025-02-23 18:00:00',
        8,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        52,
        10,
        'Universal Studios Adventure',
        'Enjoying rides at Universal Studios',
        '2025-02-24 10:00:00',
        '2025-02-24 18:00:00',
        8,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        53,
        10,
        'Epcot Exploration',
        'Exploring the attractions at Epcot',
        '2025-02-25 10:00:00',
        '2025-02-25 18:00:00',
        8,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        54,
        10,
        'Animal Kingdom Safari',
        'Going on a safari at Animal Kingdom',
        '2025-02-26 10:00:00',
        '2025-02-26 18:00:00',
        8,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        55,
        10,
        'SeaWorld Adventure',
        'Enjoying marine life at SeaWorld',
        '2025-02-27 10:00:00',
        '2025-02-27 18:00:00',
        8,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        56,
        11,
        'Auckland Museum Visit',
        'Exploring the Auckland Museum',
        '2025-03-01 10:00:00',
        '2025-03-01 12:00:00',
        9,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        57,
        11,
        'Viaduct Harbour Walk',
        'Walking along Viaduct Harbour',
        '2025-03-02 14:00:00',
        '2025-03-02 16:00:00',
        9,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        58,
        11,
        'Mount Eden Hike',
        'Hiking up Mount Eden for city views',
        '2025-03-03 09:00:00',
        '2025-03-03 11:00:00',
        9,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        59,
        11,
        'Waiheke Island Tour',
        'Exploring Waiheke Island',
        '2025-03-04 10:00:00',
        '2025-03-04 17:00:00',
        9,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        60,
        11,
        'Auckland Art Gallery',
        'Visiting the Auckland Art Gallery',
        '2025-03-05 13:00:00',
        '2025-03-05 15:00:00',
        9,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        61,
        12,
        'Cable Car Ride',
        'Riding the Wellington Cable Car',
        '2025-03-06 10:00:00',
        '2025-03-06 11:00:00',
        10,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        62,
        12,
        'Zealandia Sanctuary Tour',
        'Exploring Zealandia Ecosanctuary',
        '2025-03-07 14:00:00',
        '2025-03-07 16:00:00',
        10,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        63,
        12,
        'Wellington Waterfront Walk',
        'Walking along the Wellington Waterfront',
        '2025-03-08 09:00:00',
        '2025-03-08 11:00:00',
        10,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        64,
        12,
        'Te Papa Museum Visit',
        'Discovering exhibits at Te Papa Museum',
        '2025-03-09 10:00:00',
        '2025-03-09 12:00:00',
        10,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        65,
        12,
        'Mount Victoria Lookout',
        'Enjoying views from Mount Victoria',
        '2025-03-10 15:00:00',
        '2025-03-10 17:00:00',
        10,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        66,
        13,
        'Botanic Gardens Walk',
        'Exploring the Christchurch Botanic Gardens',
        '2025-03-11 10:00:00',
        '2025-03-11 12:00:00',
        11,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        67,
        13,
        'Avon River Punting',
        'Enjoying a punt ride on the Avon River',
        '2025-03-12 14:00:00',
        '2025-03-12 16:00:00',
        11,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        68,
        13,
        'Canterbury Museum Visit',
        'Learning history at the Canterbury Museum',
        '2025-03-13 10:00:00',
        '2025-03-13 12:00:00',
        11,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        69,
        13,
        'Port Hills Hike',
        'Hiking the scenic Port Hills',
        '2025-03-14 09:00:00',
        '2025-03-14 12:00:00',
        11,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        70,
        13,
        'Cardboard Cathedral Tour',
        'Visiting the unique Cardboard Cathedral',
        '2025-03-15 13:00:00',
        '2025-03-15 15:00:00',
        11,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        71,
        14,
        'Sydney Opera House Tour',
        'Exploring the iconic Sydney Opera House',
        '2025-03-16 10:00:00',
        '2025-03-16 12:00:00',
        12,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        72,
        14,
        'Harbour Bridge Climb',
        'Climbing the Sydney Harbour Bridge',
        '2025-03-17 14:00:00',
        '2025-03-17 16:00:00',
        12,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        73,
        14,
        'Darling Harbour Walk',
        'Walking along Darling Harbour',
        '2025-03-18 09:00:00',
        '2025-03-18 11:00:00',
        12,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        74,
        14,
        'Manly Beach Visit',
        'Relaxing at Manly Beach',
        '2025-03-19 13:00:00',
        '2025-03-19 15:00:00',
        12,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        75,
        14,
        'Taronga Zoo Visit',
        'Exploring the Taronga Zoo',
        '2025-03-20 10:00:00',
        '2025-03-20 13:00:00',
        12,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        76,
        15,
        'Snorkeling Adventure',
        'Snorkeling in the Great Barrier Reef',
        '2025-03-21 09:00:00',
        '2025-03-21 12:00:00',
        13,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        77,
        15,
        'Glass-Bottom Boat Tour',
        'Exploring the reef on a glass-bottom boat',
        '2025-03-22 14:00:00',
        '2025-03-22 16:00:00',
        13,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        78,
        15,
        'Scuba Diving Experience',
        'Scuba diving in the Great Barrier Reef',
        '2025-03-23 10:00:00',
        '2025-03-23 13:00:00',
        13,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        79,
        15,
        'Reef Island Visit',
        'Visiting a nearby reef island',
        '2025-03-24 11:00:00',
        '2025-03-24 15:00:00',
        13,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        80,
        15,
        'Marine Life Presentation',
        'Learning about marine life at the reef',
        '2025-03-25 16:00:00',
        '2025-03-25 18:00:00',
        13,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        81,
        16,
        'Shibuya Crossing Walk',
        'Experiencing the bustling Shibuya Crossing',
        '2025-03-26 10:00:00',
        '2025-03-26 12:00:00',
        14,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        82,
        16,
        'Tokyo Tower Visit',
        'Enjoying the view from Tokyo Tower',
        '2025-03-27 14:00:00',
        '2025-03-27 16:00:00',
        14,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        83,
        16,
        'Akihabara Tour',
        'Exploring the electronics district of Akihabara',
        '2025-03-28 10:00:00',
        '2025-03-28 13:00:00',
        14,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        84,
        16,
        'Asakusa Temple Visit',
        'Visiting the historic Asakusa Temple',
        '2025-03-29 09:00:00',
        '2025-03-29 11:00:00',
        14,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        85,
        16,
        'Odaiba Night Lights',
        'Enjoying the night lights of Odaiba',
        '2025-03-30 18:00:00',
        '2025-03-30 20:00:00',
        14,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        86,
        17,
        'Eiffel Tower Visit',
        'Exploring the iconic Eiffel Tower',
        '2025-03-31 10:00:00',
        '2025-03-31 12:00:00',
        15,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        87,
        17,
        'Louvre Museum Tour',
        'Discovering art at the Louvre Museum',
        '2025-04-01 14:00:00',
        '2025-04-01 16:00:00',
        15,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        88,
        17,
        'Notre Dame Cathedral Visit',
        'Visiting the historic Notre Dame Cathedral',
        '2025-04-02 10:00:00',
        '2025-04-02 12:00:00',
        15,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        89,
        17,
        'Montmartre Walk',
        'Exploring the artistic Montmartre district',
        '2025-04-03 09:00:00',
        '2025-04-03 11:00:00',
        15,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        90,
        17,
        'Seine River Cruise',
        'Enjoying a cruise on the Seine River',
        '2025-04-04 18:00:00',
        '2025-04-04 20:00:00',
        15,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        91,
        18,
        'Tower of London Tour',
        'Exploring the historic Tower of London',
        '2025-04-05 10:00:00',
        '2025-04-05 12:00:00',
        16,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        92,
        18,
        'Buckingham Palace Visit',
        'Watching the Changing of the Guard at Buckingham Palace',
        '2025-04-06 14:00:00',
        '2025-04-06 16:00:00',
        16,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        93,
        18,
        'Westminster Abbey Tour',
        'Visiting the historic Westminster Abbey',
        '2025-04-07 10:00:00',
        '2025-04-07 12:00:00',
        16,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        94,
        18,
        'British Museum Visit',
        'Exploring the exhibits at the British Museum',
        '2025-04-08 09:00:00',
        '2025-04-08 11:00:00',
        16,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        95,
        18,
        'London Eye Ride',
        'Enjoying the view from the London Eye',
        '2025-04-09 18:00:00',
        '2025-04-09 20:00:00',
        16,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        96,
        19,
        'Colosseum Tour',
        'Exploring the ancient Colosseum',
        '2025-04-10 10:00:00',
        '2025-04-10 12:00:00',
        17,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        97,
        19,
        'Roman Forum Walk',
        'Walking through the Roman Forum',
        '2025-04-11 14:00:00',
        '2025-04-11 16:00:00',
        17,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        98,
        19,
        'Pantheon Visit',
        'Visiting the historic Pantheon',
        '2025-04-12 10:00:00',
        '2025-04-12 12:00:00',
        17,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        99,
        19,
        'Trevi Fountain Stop',
        'Throwing a coin in the Trevi Fountain',
        '2025-04-13 09:00:00',
        '2025-04-13 11:00:00',
        17,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        100,
        19,
        'Vatican City Tour',
        'Exploring Vatican City and St. Peter\'s Basilica',
        '2025-04-14 18:00:00',
        '2025-04-14 20:00:00',
        17,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        101,
        20,
        'Berlin Wall Memorial Visit',
        'Learning history at the Berlin Wall Memorial',
        '2025-04-15 10:00:00',
        '2025-04-15 12:00:00',
        18,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        102,
        20,
        'Checkpoint Charlie Tour',
        'Exploring the historic Checkpoint Charlie',
        '2025-04-16 14:00:00',
        '2025-04-16 16:00:00',
        18,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        103,
        20,
        'Brandenburg Gate Visit',
        'Visiting the iconic Brandenburg Gate',
        '2025-04-17 10:00:00',
        '2025-04-17 12:00:00',
        18,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        104,
        20,
        'Reichstag Building Tour',
        'Exploring the Reichstag Building',
        '2025-04-18 09:00:00',
        '2025-04-18 11:00:00',
        18,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        105,
        20,
        'Museum Island Walk',
        'Discovering museums on Museum Island',
        '2025-04-19 18:00:00',
        '2025-04-19 20:00:00',
        18,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        106,
        21,
        'Mountain Cabin Stay',
        'Relaxing in a cozy mountain cabin',
        '2025-04-20 10:00:00',
        '2025-04-20 12:00:00',
        19,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        107,
        21,
        'Hiking Adventure',
        'Exploring mountain trails',
        '2025-04-21 09:00:00',
        '2025-04-21 12:00:00',
        19,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        108,
        21,
        'Campfire Night',
        'Enjoying a campfire under the stars',
        '2025-04-21 19:00:00',
        '2025-04-21 21:00:00',
        19,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        109,
        21,
        'Wildlife Watching',
        'Observing wildlife in the mountains',
        '2025-04-22 08:00:00',
        '2025-04-22 10:00:00',
        19,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        110,
        21,
        'Mountain Photography',
        'Capturing scenic mountain views',
        '2025-04-22 14:00:00',
        '2025-04-22 16:00:00',
        19,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        111,
        22,
        'Beachfront Relaxation',
        'Relaxing on the sandy beach',
        '2025-04-23 10:00:00',
        '2025-04-23 12:00:00',
        20,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        112,
        22,
        'Snorkeling Adventure',
        'Exploring underwater marine life',
        '2025-04-23 14:00:00',
        '2025-04-23 16:00:00',
        20,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        113,
        22,
        'Sunset Walk',
        'Walking along the beach at sunset',
        '2025-04-23 18:00:00',
        '2025-04-23 19:00:00',
        20,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        114,
        22,
        'Beach Yoga',
        'Practicing yoga on the beach',
        '2025-04-24 07:00:00',
        '2025-04-24 08:00:00',
        20,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        115,
        22,
        'Seafood Dinner',
        'Enjoying fresh seafood by the beach',
        '2025-04-24 19:00:00',
        '2025-04-24 21:00:00',
        20,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        116,
        23,
        'Hidden Trail Hike',
        'Exploring a secluded hiking trail',
        '2025-04-25 09:00:00',
        '2025-04-25 12:00:00',
        21,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        117,
        23,
        'Secluded Waterfall Visit',
        'Discovering a hidden waterfall',
        '2025-04-25 14:00:00',
        '2025-04-25 16:00:00',
        21,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        118,
        23,
        'Private Picnic',
        'Enjoying a private picnic in nature',
        '2025-04-26 11:00:00',
        '2025-04-26 13:00:00',
        21,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        119,
        23,
        'Stargazing Night',
        'Watching the stars in a remote location',
        '2025-04-26 20:00:00',
        '2025-04-26 22:00:00',
        21,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        120,
        23,
        'Nature Photography',
        'Capturing the beauty of the hidden location',
        '2025-04-27 10:00:00',
        '2025-04-27 12:00:00',
        21,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        121,
        24,
        'Mysterious Cave Exploration',
        'Exploring a hidden cave',
        '2025-04-28 09:00:00',
        '2025-04-28 12:00:00',
        22,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        122,
        24,
        'Forest Trek',
        'Trekking through a dense forest',
        '2025-04-28 14:00:00',
        '2025-04-28 17:00:00',
        22,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        123,
        24,
        'River Rafting',
        'Rafting down a secluded river',
        '2025-04-29 10:00:00',
        '2025-04-29 13:00:00',
        22,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        124,
        24,
        'Campfire Tales',
        'Sharing stories around a campfire',
        '2025-04-29 19:00:00',
        '2025-04-29 21:00:00',
        22,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        125,
        24,
        'Sunrise Viewpoint',
        'Watching the sunrise from a hidden viewpoint',
        '2025-04-30 05:30:00',
        '2025-04-30 07:00:00',
        22,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        126,
        25,
        'Countryside Walk',
        'Exploring the peaceful countryside',
        '2025-03-25 10:00:00',
        '2025-03-25 12:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        127,
        25,
        'Farm Visit',
        'Learning about life on a farm',
        '2025-03-25 14:00:00',
        '2025-03-25 16:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        128,
        25,
        'Picnic by the Lake',
        'Enjoying a picnic by the lake',
        '2025-03-26 11:00:00',
        '2025-03-26 13:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        129,
        25,
        'Bird Watching',
        'Observing birds in their natural habitat',
        '2025-03-26 15:00:00',
        '2025-03-26 17:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        130,
        25,
        'Sunset Photography',
        'Capturing the sunset over the fields',
        '2025-03-27 18:00:00',
        '2025-03-27 19:30:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        131,
        26,
        'City Walking Tour',
        'Exploring the city\'s landmarks',
        '2025-03-28 10:00:00',
        '2025-03-28 12:00:00',
        24,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        132,
        26,
        'Museum Visit',
        'Learning history at the city museum',
        '2025-03-28 14:00:00',
        '2025-03-28 16:00:00',
        24,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        133,
        26,
        'Street Food Tasting',
        'Trying local street food',
        '2025-03-29 12:00:00',
        '2025-03-29 14:00:00',
        24,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        134,
        26,
        'Art Gallery Tour',
        'Exploring the city\'s art galleries',
        '2025-03-29 15:00:00',
        '2025-03-29 17:00:00',
        24,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        135,
        26,
        'Night Market Visit',
        'Enjoying the vibrant night market',
        '2025-03-30 19:00:00',
        '2025-03-30 21:00:00',
        24,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        136,
        27,
        'Desert Safari',
        'Exploring the desert on a safari',
        '2025-03-25 09:00:00',
        '2025-03-25 12:00:00',
        25,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        137,
        27,
        'Camel Ride',
        'Riding a camel through the desert',
        '2025-03-25 14:00:00',
        '2025-03-25 16:00:00',
        25,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        138,
        27,
        'Sandboarding',
        'Sliding down sand dunes',
        '2025-03-26 10:00:00',
        '2025-03-26 12:00:00',
        25,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        139,
        27,
        'Desert Campfire',
        'Relaxing by a campfire in the desert',
        '2025-03-26 19:00:00',
        '2025-03-26 21:00:00',
        25,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        140,
        27,
        'Stargazing',
        'Observing the stars in the clear desert sky',
        '2025-03-27 20:00:00',
        '2025-03-27 22:00:00',
        25,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        141,
        28,
        'Forest Hike',
        'Hiking through the lush forest',
        '2025-03-28 09:00:00',
        '2025-03-28 12:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        142,
        28,
        'Wildlife Spotting',
        'Spotting wildlife in the forest',
        '2025-03-28 14:00:00',
        '2025-03-28 16:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        143,
        28,
        'Treehouse Visit',
        'Exploring a treehouse in the forest',
        '2025-03-29 10:00:00',
        '2025-03-29 12:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        144,
        28,
        'River Kayaking',
        'Kayaking down a forest river',
        '2025-03-29 14:00:00',
        '2025-03-29 16:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        145,
        28,
        'Forest Photography',
        'Capturing the beauty of the forest',
        '2025-03-30 11:00:00',
        '2025-03-30 13:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        146,
        29,
        'Beachfront Relaxation',
        'Relaxing on the pristine island beach',
        '2025-03-25 10:00:00',
        '2025-03-25 12:00:00',
        20,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        147,
        29,
        'Snorkeling Adventure',
        'Exploring coral reefs around the island',
        '2025-03-25 14:00:00',
        '2025-03-25 16:00:00',
        20,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        148,
        29,
        'Island Hiking Trail',
        'Hiking through the island\'s lush trails',
        '2025-03-26 09:00:00',
        '2025-03-26 11:00:00',
        24,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        149,
        29,
        'Sunset Cruise',
        'Enjoying a sunset cruise around the island',
        '2025-03-26 17:00:00',
        '2025-03-26 19:00:00',
        24,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        150,
        29,
        'Island Cultural Tour',
        'Learning about the island\'s culture and history',
        '2025-03-27 10:00:00',
        '2025-03-27 12:00:00',
        24,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        151,
        30,
        'Museum Tour',
        'Exploring the cultural artifacts in the museum',
        '2025-03-28 10:00:00',
        '2025-03-28 12:00:00',
        25,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        152,
        30,
        'Cultural Dance Show',
        'Watching a traditional cultural dance performance',
        '2025-03-28 14:00:00',
        '2025-03-28 16:00:00',
        25,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        153,
        30,
        'Local Cuisine Tasting',
        'Tasting traditional dishes from the region',
        '2025-03-29 12:00:00',
        '2025-03-29 14:00:00',
        25,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        154,
        30,
        'Historical Site Visit',
        'Visiting a famous historical site',
        '2025-03-29 15:00:00',
        '2025-03-29 17:00:00',
        25,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        155,
        30,
        'Cultural Workshop',
        'Participating in a cultural workshop',
        '2025-03-30 10:00:00',
        '2025-03-30 12:00:00',
        25,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        156,
        31,
        'Ancient Ruins Tour',
        'Exploring ancient ruins in the area',
        '2025-03-25 09:00:00',
        '2025-03-25 11:00:00',
        17,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        157,
        31,
        'Historical Museum Visit',
        'Learning about the history of the region',
        '2025-03-25 14:00:00',
        '2025-03-25 16:00:00',
        17,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        158,
        31,
        'Guided History Walk',
        'Walking through historical landmarks',
        '2025-03-26 10:00:00',
        '2025-03-26 12:00:00',
        17,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        159,
        31,
        'Historical Reenactment',
        'Watching a reenactment of historical events',
        '2025-03-26 15:00:00',
        '2025-03-26 17:00:00',
        17,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        160,
        31,
        'Historical Lecture',
        'Attending a lecture on the region\'s history',
        '2025-03-27 11:00:00',
        '2025-03-27 13:00:00',
        17,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        161,
        32,
        'Rock Climbing',
        'Climbing a challenging rock face',
        '2025-03-28 09:00:00',
        '2025-03-28 12:00:00',
        22,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        162,
        32,
        'Whitewater Rafting',
        'Rafting down a fast-moving river',
        '2025-03-28 14:00:00',
        '2025-03-28 16:00:00',
        22,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        163,
        32,
        'Ziplining',
        'Soaring through the treetops on a zipline',
        '2025-03-29 10:00:00',
        '2025-03-29 12:00:00',
        22,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        164,
        32,
        'Mountain Biking',
        'Biking through rugged mountain trails',
        '2025-03-29 14:00:00',
        '2025-03-29 16:00:00',
        22,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        165,
        32,
        'Camping Adventure',
        'Camping overnight in the wilderness',
        '2025-03-30 18:00:00',
        '2025-03-31 08:00:00',
        22,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        166,
        33,
        'Nature Walk',
        'Walking through a serene nature reserve',
        '2025-03-25 10:00:00',
        '2025-03-25 12:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        167,
        33,
        'Bird Watching',
        'Observing exotic birds in their habitat',
        '2025-03-25 14:00:00',
        '2025-03-25 16:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        168,
        33,
        'Nature Photography Workshop',
        'Learning photography techniques in nature',
        '2025-03-26 09:00:00',
        '2025-03-26 11:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        169,
        33,
        'Botanical Garden Tour',
        'Exploring a beautiful botanical garden',
        '2025-03-26 13:00:00',
        '2025-03-26 15:00:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        170,
        33,
        'Sunset Viewpoint',
        'Watching the sunset from a scenic viewpoint',
        '2025-03-27 18:00:00',
        '2025-03-27 19:30:00',
        23,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        171,
        34,
        'New York City Walk',
        'A day in New York city',
        '2025-05-22 09:00:00',
        '2025-05-22 10:30:00',
        1,
        0,
        CURRENT_TIMESTAMP
    ),
    (
        172,
        35,
        'Rose Garden',
        'A beautiful tour at rose garden',
        '2025-05-27 09:00:00',
        '2025-05-27 10:30:00',
        26,
        0,
        CURRENT_TIMESTAMP
    )
    ;

-- Insert announcements
INSERT INTO
    `announcements` (
        `announcement_id`,
        `user_id`,
        `title`,
        `content`,
        `created_at`
    )
VALUES
    (
        1,
        1,
        'System Maintenance',
        'The system will be down for maintenance on 2023-01-10 from 00:00 to 02:00 UTC.',
        CURRENT_TIMESTAMP
    ),
    (
        2,
        2,
        'New Features Released',
        'We have released new features including enhanced security and user interface improvements.',
        CURRENT_TIMESTAMP
    ),
    (
        3,
        3,
        'Welcome New Users',
        'We are excited to welcome new users to our platform. Enjoy your journey!',
        CURRENT_TIMESTAMP
    ),
    (
        4,
        4,
        'Travel Tips',
        'Check out our latest travel tips to make the most of your journeys.',
        CURRENT_TIMESTAMP
    ),
    (
        5,
        5,
        'Event Updates',
        'Stay tuned for updates on upcoming events and activities.',
        CURRENT_TIMESTAMP
    );

-- Insert subscription_types
INSERT INTO
    `subscription_types` (
        `subscription_type_id`,
        `type`,
        `duration`,
        `price`
    )
VALUES
    (1, 'paid', 30, 5.22),
    (2, 'paid', 90, 14.09),
    (3, 'paid', 365, 46.96),
    (4, 'free_trial', 30, 0),
    (5, 'admin_granted', 30, 0),
    (6, 'admin_granted', 90, 0),
    (7, 'admin_granted', 365, 0);

-- Insert event_photos
INSERT INTO
    `event_photos` (`event_id`, `photo_path`)
VALUES
    (1, 'event_photo_1.jpg'),
    (2, 'event_photo_2.jpg'),
    (3, 'event_photo_3.jpg'),
    (4, 'event_photo_4.jpg'),
    (5, 'event_photo_5.jpg'),
    (6, 'event_photo_6.jpg'),
    (7, 'event_photo_7.jpg'),
    (8, 'event_photo_8.jpg'),
    (9, 'event_photo_9.jpg'),
    (10, 'event_photo_10.jpg'),
    (11, 'event_photo_11.jpg'),
    (12, 'event_photo_12.jpg'),
    (13, 'event_photo_13.jpg'),
    (14, 'event_photo_14.jpg'),
    (15, 'event_photo_15.jpg'),
    (16, 'event_photo_16.jpg'),
    (17, 'event_photo_17.jpg'),
    (18, 'event_photo_18.jpg'),
    (19, 'event_photo_19.jpg'),
    (20, 'event_photo_20.jpg'),
    (21, 'event_photo_21.jpg'),
    (22, 'event_photo_22.jpg'),
    (23, 'event_photo_23.jpg'),
    (24, 'event_photo_24.jpg'),
    (25, 'event_photo_25.jpg'),
    (26, 'event_photo_26.jpg'),
    (27, 'event_photo_27.jpg'),
    (28, 'event_photo_28.jpg'),
    (29, 'event_photo_29.jpg'),
    (30, 'event_photo_30.jpg'),
    (31, 'event_photo_31.jpg'),
    (32, 'event_photo_32.jpg'),
    (33, 'event_photo_33.jpg'),
    (34, 'event_photo_34.jpg'),
    (35, 'event_photo_35.jpg'),
    (36, 'event_photo_36.jpg'),
    (37, 'event_photo_37.jpg'),
    (38, 'event_photo_38.jpg'),
    (39, 'event_photo_39.jpg'),
    (40, 'event_photo_40.jpg'),
    (41, 'event_photo_41.jpg'),
    (42, 'event_photo_42.jpg'),
    (43, 'event_photo_43.jpg'),
    (44, 'event_photo_44.jpg'),
    (45, 'event_photo_45.jpg'),
    (46, 'event_photo_46.jpg'),
    (47, 'event_photo_47.jpg'),
    (48, 'event_photo_48.jpg'),
    (49, 'event_photo_49.jpg'),
    (50, 'event_photo_50.jpg'),
    (51, 'event_photo_51.jpg'),
    (171, 'event_photo_52.jpg'),
    (171, 'event_photo_53.jpg'),
    (172, 'event_photo_54.jpg');

-- Insert subscriptions
INSERT INTO
    `subscriptions` (
        `user_id`,
        `subscription_type_id`,
        `start_datetime`,
        `end_datetime`,
        `payment_amount`,
        `gst`,
        `billing_address`
    )
VALUES
    (
        12,
        1,
        '2025-05-12 10:00:00',
        '2025-06-12 10:00:00',
        5.22,
        0,
        '008 Schuppe Shoal'
    ),
    (
        13,
        2,
        '2025-05-12 10:00:00',
        '2025-08-12 10:00:00',
        14.09,
        0,
        '13226 Zieme Underpass'
    ),
    (
        14,
        3,
        '2025-05-12 10:00:00',
        '2026-05-12 10:00:00',
        46.96,
        0,
        '504 Christelle Fall'
    ),
    (
        15,
        4,
        '2025-05-12 10:00:00',
        '2025-06-12 10:00:00',
        0,
        0,
        ''
    ),
    (
        16,
        5,
        '2025-05-12 10:00:00',
        '2025-06-12 10:00:00',
        0,
        0,
        ''
    ),
    (
        17,
        6,
        '2025-05-12 10:00:00',
        '2025-08-12 10:00:00',
        0,
        0,
        ''
    ),
    (
        18,
        7,
        '2025-05-12 10:00:00',
        '2026-05-12 10:00:00',
        0,
        0,
        ''
    ),
    (
        19,
        1,
        '2025-05-15 10:00:00',
        '2025-06-15 10:00:00',
        6.00,
        1,
        '189 Yost Harbor'
    ),
    (
        20,
        2,
        '2025-05-12 10:00:00',
        '2025-08-12 10:00:00',
        16.20,
        1,
        '4504 Ernser Oval'
    ),
    (
        21,
        3,
        '2025-05-12 10:00:00',
        '2026-05-12 10:00:00',
        54.00,
        1,
        '6113 Wilber Flat'
    );

-- Insert comments
INSERT INTO
    comments (
        `comment_id`,
        `event_id`,
        `user_id`,
        `content`,
        `is_hidden`,
        `escalated`
    )
VALUES
    (
        1,
        61,
        1,
        'Tenetur reprehenderit repellendus esse deleniti maxime.',
        FALSE,
        FALSE
    ),
    (
        2,
        61,
        2,
        'Fuga eius tempora nulla earum explicabo.',
        FALSE,
        FALSE
    ),
    (
        3,
        61,
        3,
        'Quam blanditiis corrupti odit iusto hic.',
        FALSE,
        FALSE
    ),
    (
        4,
        61,
        4,
        'Praesentium nulla unde totam doloribus veniam assumenda.',
        FALSE,
        FALSE
    ),
    (
        5,
        61,
        4,
        'Unde inventore voluptates fugit velit quia impedit.',
        FALSE,
        FALSE
    ),
    (
        6,
        61,
        4,
        'Facere nisi voluptatum quibusdam dicta.',
        FALSE,
        FALSE
    ),
    (
        7,
        62,
        4,
        'Ipsam excepturi et culpa occaecati fugiat.',
        FALSE,
        FALSE
    ),
    (
        8,
        62,
        4,
        'Id quisquam veniam illo voluptatum fugiat repellendus corporis.',
        FALSE,
        FALSE
    ),
    (
        9,
        62,
        4,
        'Commodi fugit alias aspernatur facilis asperiores repellat.',
        FALSE,
        FALSE
    ),
    (
        10,
        62,
        4,
        'Natus deleniti dicta quis eaque perspiciatis mollitia praesentium natus.',
        FALSE,
        FALSE
    ),
    (
        11,
        62,
        4,
        'Voluptate consequatur sunt eius.',
        FALSE,
        FALSE
    ),
    (
        12,
        63,
        4,
        'Adipisci natus quibusdam inventore molestiae vitae.',
        FALSE,
        FALSE
    ),
    (
        13,
        63,
        4,
        'Sint similique iure temporibus eligendi error eaque repellendus fugit quo.',
        FALSE,
        FALSE
    ),
    (
        14,
        63,
        4,
        'Molestiae officia sit recusandae explicabo autem.',
        FALSE,
        FALSE
    ),
    (
        15,
        63,
        4,
        'Necessitatibus voluptate corporis officiis culpa et fugiat error.',
        FALSE,
        FALSE
    ),
    (
        16,
        63,
        4,
        'Velit quas earum quaerat inventore modi unde deleniti qui nulla.',
        TRUE,
        FALSE
    ),
    (
        17,
        56,
        4,
        'Id non alias itaque magnam qui.',
        0,
        0
    ),
    (
        18,
        56,
        4,
        'Amet repellendus consequuntur quam.',
        TRUE,
        FALSE
    ),
    (
        19,
        56,
        4,
        'Pariatur similique ipsum animi commodi quod alias recusandae.',
        FALSE,
        TRUE
    ),
    (
        20,
        56,
        4,
        'Occaecati iure blanditiis illo.',
        0,
        0
    ),
    (
        21,
        56,
        4,
        'Natus maiores repellat sed recusandae.',
        FALSE,
        TRUE
    );

UPDATE events
SET
    comments_count = (
        SELECT
            COUNT(*)
        FROM
            comments
        WHERE
            comments.event_id = events.event_id
    )
WHERE
    EXISTS (
        SELECT
            1
        FROM
            comments
        WHERE
            comments.event_id = events.event_id
    );

-- Insert reports
INSERT INTO
    reports (`comment_id`, `user_id`, `reason`)
VALUES
    (1, 30, 'abusive'),
    (2, 31, 'abusive'),
    (3, 32, 'offensive'),
    (4, 33, 'offensive'),
    (5, 34, 'spam');

-- Insert reactions
INSERT INTO
    reactions (`user_id`, `event_id`, `reaction_type`, `is_like`)
VALUES
    (21, 61, 'event', TRUE),
    (22, 62, 'event', TRUE),
    (23, 63, 'event', TRUE),
    (24, 64, 'event', TRUE),
    (25, 65, 'event', TRUE);

UPDATE events
SET
    like_count = 1
WHERE
    event_id IN (61, 62, 63, 64, 65);

INSERT INTO
    reactions (
        `user_id`,
        `comment_id`,
        `reaction_type`,
        `is_like`
    )
VALUES
    (21, 1, 'comment', TRUE),
    (22, 2, 'comment', FALSE),
    (23, 3, 'comment', TRUE),
    (24, 4, 'comment', FALSE),
    (25, 5, 'comment', TRUE);

UPDATE comments
SET
    like_count = 1
WHERE
    comment_id IN (1, 3, 5);

UPDATE comments
SET
    dislike_count = 1
WHERE
    comment_id IN (2, 4);

-- Insert private messages
INSERT INTO
    `messages` (`from`, `to`, `content`, `status`)
VALUES
    (
        1,
        12,
        'Just read your trip to Iceland — amazing photos!',
        1
    ),
    (
        2,
        7,
        'Do you have tips for backpacking in Nepal?',
        0
    ),
    (
        3,
        19,
        'Your journal about the Sahara desert was inspiring.',
        1
    ),
    (
        4,
        25,
        'Loved your entry on the food markets in Bangkok!',
        0
    ),
    (
        5,
        3,
        'How did you get around Kyoto? Any recommendations?',
        1
    ),
    (
        6,
        18,
        'Great shots from Patagonia. Mind sharing your route?',
        0
    ),
    (
        7,
        21,
        'Your write-up on Amsterdam was super helpful.',
        1
    ),
    (
        8,
        30,
        'Just followed you after seeing your Italy post.',
        0
    ),
    (
        9,
        14,
        'Where did you stay in Cape Town? Looks great.',
        1
    ),
    (
        10,
        6,
        'Loved your hiking stories from the Alps!',
        1
    ),
    (11, 17, 'Your Egypt photos blew me away!', 0),
    (
        12,
        4,
        'Thanks for the travel checklist you posted!',
        1
    ),
    (
        13,
        2,
        'Planning a trip to Bali — your journal helped a lot.',
        0
    ),
    (
        14,
        35,
        'Your drone shots over Norway were insane.',
        1
    ),
    (
        15,
        8,
        'Mind if I use your Japan itinerary as a reference?',
        0
    ),
    (
        16,
        9,
        'Such good insights on traveling during off-season.',
        1
    ),
    (
        17,
        5,
        'Your recent post inspired me to visit Peru!',
        0
    ),
    (
        18,
        22,
        'Are you planning to post more from your Iceland trip?',
        1
    ),
    (19, 1, 'Love your minimalist travel style!', 1),
    (20, 31, 'That volcano trek story was intense!', 0),
    (
        21,
        10,
        'Where did you get that cool travel gear?',
        1
    ),
    (
        22,
        26,
        'Your blog helped me plan my Eurotrip.',
        0
    ),
    (
        23,
        13,
        'Following you after that stunning Thailand post!',
        1
    ),
    (
        24,
        15,
        'Your journal entries are so well-written.',
        0
    ),
    (
        25,
        11,
        'Can you share more about that local guide in Kenya?',
        1
    ),
    (
        26,
        23,
        'Really enjoyed your reflections on slow travel.',
        1
    ),
    (
        27,
        34,
        'How do you manage connectivity when traveling?',
        0
    ),
    (28, 29, 'Big fan of your photography tips!', 1),
    (
        29,
        24,
        'Your article on sustainable travel was eye-opening.',
        0
    ),
    (
        30,
        16,
        'Inspired me to go hiking in New Zealand!',
        1
    ),
    (
        31,
        20,
        'Where do you find those quiet beach spots?',
        0
    ),
    (32, 28, 'Your budget travel hacks are gold.', 1),
    (
        33,
        27,
        'I wish I could write like you about travel.',
        0
    ),
    (
        34,
        33,
        'Do you recommend any travel communities to join?',
        1
    ),
    (
        35,
        32,
        'Your story about losing your passport had me laughing!',
        0
    );

INSERT INTO
    issues (
        title,
        category,
        content,
        status,
        user_id,
        assigned_to,
        created_at
    )
VALUES
    (
        'Cannot Add New Journey',
        'issue',
        'I tried adding a new journey, but the form crashes after submitting.',
        'New',
        12,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Request to Edit Past Event',
        'request',
        'Can you allow editing for past events? I made a mistake in one of mine.',
        'Open',
        14,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Profile Picture Not Updating',
        'issue',
        'Uploaded new profile picture, but it keeps showing the old one.',
        'Stalled',
        12,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Add Option to Tag Friends in Photos',
        'request',
        'It would be great if we could tag friends in uploaded trip photos.',
        'New',
        14,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Journey Description Lost',
        'issue',
        'I wrote a detailed journey description, but it disappeared after saving.',
        'Open',
        12,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Request to Export Trip Data',
        'request',
        'I would like to export all my trip logs into a PDF or CSV file.',
        'Resolved',
        14,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Event Reminder Not Working',
        'issue',
        'The reminders for upcoming events aren’t sending notifications.',
        'New',
        12,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Change Username Feature',
        'request',
        'Please allow users to change their username once per year.',
        'Open',
        14,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Photo Upload Stuck at 99%',
        'issue',
        'Tried uploading trip photos, but the progress bar gets stuck.',
        'Stalled',
        12,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Request More Profile Customization',
        'request',
        'Can you add options to customize profile themes or cover images?',
        'New',
        14,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Journey Map Not Displaying Correctly',
        'issue',
        'The map for my latest journey is not showing the correct route.',
        'Open',
        22,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Request to Add More Travel Categories',
        'request',
        'Can we have more categories for travel types, like adventure or cultural?',
        'Resolved',
        23,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Event photo Not Working',
        'issue',
        'I can’t upload photos to events; the button is unresponsive.',
        'New',
        24,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Request for Dark Mode',
        'request',
        'Please add a dark mode option for better night-time reading.',
        'Open',
        25,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Journey Sharing Permissions',
        'issue',
        'I can’t share my journey with friends; the share button is missing.',
        'Stalled',
        26,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Request to Add More Languages',
        'request',
        'Can we have more language options for the app interface?',
        'New',
        27,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Request for Offline Mode',
        'request',
        'It would be great to have an offline mode for viewing journeys without internet.',
        'New',
        29,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Request for More Travel Tips',
        'request',
        'Can you add a section for travel tips and hacks from the community?',
        'Open',
        31,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Request to Add More Travel Destinations',
        'request',
        'Please add more travel destinations to explore in the app.',
        'Resolved',
        32,
        NULL,
        CURRENT_TIMESTAMP
    ),
    (
        'Request for More Photo Filters',
        'request',
        'Can we have more photo filters for trip photos?',
        'Open',
        34,
        NULL,
        CURRENT_TIMESTAMP
    );

INSERT INTO
    follows (follower_id, followable_type, followable_id)
VALUES
    (3, 'user', 17),
    (12, 'journey', 8),
    (25, 'user', 9),
    (6, 'location', 1),
    (15, 'user', 21),
    (29, 'journey', 1),
    (18, 'user', 34),
    (11, 'location', 2),
    (19, 'user', 13),
    (10, 'user', 4),
    (8, 'journey', 2),
    (30, 'user', 35),
    (5, 'location', 3),
    (14, 'user', 6),
    (21, 'journey', 19),
    (33, 'user', 12),
    (7, 'user', 11),
    (2, 'location', 2),
    (34, 'user', 14),
    (24, 'journey', 28),
    (13, 'user', 33),
    (16, 'journey', 18),
    (27, 'user', 5),
    (1, 'location', 5),
    (1, 'user', 5),
    (1, 'user', 8),
    (1, 'user', 9),
    (1, 'journey', 5),
    (17, 'user', 10),
    (9, 'user', 16),
    (23, 'journey', 26),
    (22, 'location', 12),
    (35, 'user', 3),
    (20, 'user', 25),
    (28, 'user', 15),
    (4, 'journey', 24),
    (26, 'user', 23),
    (31, 'location', 5),
    (32, 'user', 29),
    (19, 'journey', 3),
    (12, 'location', 1);

-- Insert achievement_types
INSERT INTO
    `achievement_types` (`achievement_type_id`, `type`, `is_premium`, `goal`, `description`)
VALUES
    (
        1,
        'five_journeys_with_cover_image',
        TRUE,
        5,
        "Add cover images to 5 journeys"
    ),
    (
        2,
        'first_viewer',
        FALSE,
        1,
        "Be the first viewer of a shared journey"
    ),
    (
        3,
        'seven_days_journey',
        FALSE,
        1,
        "Create a journey lasting 7 days"
    ),
    (4, 'first_event', FALSE, 1, "Create first event"),
    (5, 'first_journey', FALSE, 1, "Create first journey"),
    (
        6,
        'first_published_journey',
        TRUE,
        1,
        "Publish first journey"
    ),
    (
        7,
        'five_comments_for_event',
        FALSE,
        5,
        "Receive 5 comments on an event"
    ),
    (
        8,
        'ten_comments_for_event',
        FALSE,
        10,
        "Receive 10 comments on an event"
    ),
    (
        9,
        'twenty_comments_for_event',
        FALSE,
        20,
        "Receive 20 comments on an event"
    ),
    (
        10,
        '20_event_likes',
        FALSE,
        20,
        "Receive 20 likes on an event"
    ),
    (
        11,
        '40_event_likes',
        FALSE,
        40,
        "Receive 40 likes on an event"
    ),
    (
        12,
        '60_event_likes',
        FALSE,
        60,
        "Receive 60 likes on an event"
    ),
    (
        13,
        'first_public_journey',
        FALSE,
        1,
        "Share first public journey"
    ),
    (
        14,
        'five_locations',
        FALSE,
        5,
        "Visit 5 different locations"
    );

-- Insert achievements
INSERT INTO
    `achievements` (
        `achievement_type_id`,
        `user_id`,
        `progress`,
        `created_at`,
        `updated_at`
    )
VALUES
    -- first journey
    (
        5,
        13,
        1,
        '2025-01-03 09:00:00',
        '2025-01-03 09:00:00'
    ),
    (
        5,
        5,
        1,
        '2025-01-04 11:50:00',
        '2025-01-04 11:50:00'
    ),
    (
        5,
        1,
        1,
        '2025-01-05 10:15:00',
        '2025-01-05 10:15:00'
    ),
    (
        5,
        14,
        1,
        '2025-01-08 11:30:00',
        '2025-01-08 11:30:00'
    ),
    (
        5,
        6,
        1,
        '2025-01-09 14:05:00',
        '2025-01-09 14:05:00'
    ),
    (
        5,
        2,
        1,
        '2025-01-10 14:30:00',
        '2025-01-10 14:30:00'
    ),
    (
        5,
        15,
        1,
        '2025-01-13 14:00:00',
        '2025-01-13 14:00:00'
    ),
    (
        5,
        7,
        1,
        '2025-01-14 16:20:00',
        '2025-01-14 16:20:00'
    ),
    (
        5,
        3,
        1,
        '2025-01-15 09:45:00',
        '2025-01-15 09:45:00'
    ),
    (
        5,
        16,
        1,
        '2025-01-18 16:45:00',
        '2025-01-18 16:45:00'
    ),
    (
        5,
        8,
        1,
        '2025-01-19 09:35:00',
        '2025-01-19 09:35:00'
    ),
    (
        5,
        4,
        1,
        '2025-01-20 11:00:00',
        '2025-01-20 11:00:00'
    ),
    (
        5,
        17,
        1,
        '2025-01-23 09:15:00',
        '2025-01-23 09:15:00'
    ),
    (
        5,
        9,
        1,
        '2025-01-24 11:50:00',
        '2025-01-24 11:50:00'
    ),
    (
        5,
        18,
        1,
        '2025-01-28 12:30:00',
        '2025-01-28 12:30:00'
    ),
    (
        5,
        10,
        1,
        '2025-01-29 14:05:00',
        '2025-01-29 14:05:00'
    ),
    (
        5,
        11,
        1,
        '2025-02-03 16:20:00',
        '2025-02-03 16:20:00'
    ),
    (
        5,
        12,
        1,
        '2025-02-08 09:35:00',
        '2025-02-08 09:35:00'
    ),
    (
        5,
        22,
        1,
        '2025-05-27 11:50:00',
        '2025-05-27 11:50:00'
    ),
    (
        5,
        20,
        1,
        '2025-05-28 11:50:00',
        '2025-05-28 11:50:00'
    ),
    -- first event
    (
        4,
        20,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        22,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        1,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        2,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        3,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        4,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        5,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        6,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        7,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        8,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        9,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        10,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        11,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        12,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        13,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        14,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        15,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        16,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        17,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        4,
        18,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    -- first public journey
    (
        13,
        13,
        1,
        '2025-01-03 09:00:00',
        '2025-01-03 09:00:00'
    ),
    (
        13,
        14,
        1,
        '2025-01-08 11:30:00',
        '2025-01-08 11:30:00'
    ),
    (
        13,
        15,
        1,
        '2025-01-13 14:00:00',
        '2025-01-13 14:00:00'
    ),
    (
        13,
        16,
        1,
        '2025-01-18 16:45:00',
        '2025-01-18 16:45:00'
    ),
    (
        13,
        4,
        1,
        '2025-01-20 11:00:00',
        '2025-01-20 11:00:00'
    ),
    (
        13,
        17,
        1,
        '2025-01-23 09:15:00',
        '2025-01-23 09:15:00'
    ),
    (
        13,
        5,
        1,
        '2025-01-25 16:20:00',
        '2025-01-25 16:20:00'
    ),
    (
        13,
        18,
        1,
        '2025-01-28 12:30:00',
        '2025-01-28 12:30:00'
    ),
    (
        13,
        6,
        1,
        '2025-01-30 08:10:00',
        '2025-01-30 08:10:00'
    ),
    (
        13,
        1,
        1,
        '2025-02-02 15:00:00',
        '2025-02-02 15:00:00'
    ),
    (
        13,
        7,
        1,
        '2025-02-05 13:35:00',
        '2025-02-05 13:35:00'
    ),
    (
        13,
        2,
        1,
        '2025-02-07 17:20:00',
        '2025-02-07 17:20:00'
    ),
    (
        13,
        8,
        1,
        '2025-02-10 17:50:00',
        '2025-02-10 17:50:00'
    ),
    (
        13,
        9,
        1,
        '2025-02-15 12:25:00',
        '2025-02-15 12:25:00'
    ),
    (
        13,
        10,
        1,
        '2025-02-20 15:40:00',
        '2025-02-20 15:40:00'
    ),
    (
        13,
        11,
        1,
        '2025-02-25 10:05:00',
        '2025-02-25 10:05:00'
    ),
    (
        13,
        12,
        1,
        '2025-03-01 14:50:00',
        '2025-03-01 14:50:00'
    ),
    -- visited 5 locations
    (
        14,
        22,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        20,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        1,
        3,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        2,
        3,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        3,
        2,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        4,
        2,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        5,
        2,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        6,
        2,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        7,
        2,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        8,
        2,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        9,
        4,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        10,
        3,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        11,
        2,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        12,
        4,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        13,
        2,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        14,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        15,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        16,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        17,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        14,
        18,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    -- journey last 7 days
    (
        3,
        1,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        2,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        3,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        4,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        5,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        6,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        7,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        8,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        9,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        10,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        11,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        12,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        13,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        14,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        15,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        16,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        17,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    (
        3,
        18,
        1,
        '2025-06-01 11:42:13',
        '2025-06-01 11:42:13'
    ),
    -- first published journey
    (
        6,
        1,
        1,
        '2025-01-05 10:15:00',
        '2025-01-05 10:15:00'
    ),
    (
        6,
        2,
        1,
        '2025-01-10 14:30:00',
        '2025-01-10 14:30:00'
    ),
    (
        6,
        3,
        1,
        '2025-01-15 09:45:00',
        '2025-01-15 09:45:00'
    ),
    (
        6,
        20,
        1,
        '2025-05-28 11:50:00',
        '2025-05-28 11:50:00'
    ),
    -- 5 journey cover images
    (
        1,
        20,
        1,
        '2025-05-28 11:50:00',
        '2025-05-28 11:50:00'
    ),
    (
        1,
        12,
        1,
        '2025-03-01 14:50:00',
        '2025-03-01 14:50:00'
    ),
	(
        1,
        13,
        1,
        '2025-01-03 09:00:00',
        '2025-01-03 09:00:00'
	),
    (
		1, 
        14, 
        1, 
        '2025-01-08 11:30:00', 
        '2025-01-08 11:30:00'
	),
	(
		1,
        15, 
        1, 
        '2025-01-13 14:00:00', 
        '2025-01-13 14:00:00'
	),
	(
		1, 
        16, 
        1, 
        '2025-01-18 16:45:00', 
        '2025-01-18 16:45:00'
	),
	-- received likes
    (
		10, 
        12, 
        5, 
        '2025-06-08 22:01:18', 
        '2025-06-08 22:01:18'
	),
    -- received comments
    (
		7, 
        12, 
        4, 
        '2025-06-08 22:01:18', 
        '2025-06-08 22:01:18'
	),    
    (
		7, 
        11, 
        5, 
        '2025-06-08 22:01:18', 
        '2025-06-08 22:01:18'
	),
    -- first viewer
	(
		2, 
        22, 
        1, 
        '2025-06-08 22:01:18', 
        '2025-06-08 22:01:18'
	),
    (
		2, 
        4, 
        1, 
        '2025-06-08 22:01:18', 
        '2025-06-08 22:01:18'
	)
        ;
UPDATE journeys
SET first_viewer_id = 22
WHERE journey_id = 12;

UPDATE journeys
SET first_viewer_id = 4
WHERE journey_id = 11;


