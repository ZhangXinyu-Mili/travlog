-- CREATE SCHEMA otj;
USE otj;

-- Create the table for the users
CREATE TABLE `users` (
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(20) NOT NULL,
    `password_hash` CHAR(60) BINARY NOT NULL COMMENT 'Bcrypt Password Hash and Salt (60 bytes)',
    `email` VARCHAR(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321 section 4.5.3.1 is 320 characters (64 for local-part, 1 for at sign, 255 for domain)',
    `email_public` BOOLEAN DEFAULT True,
    `first_name` VARCHAR(50),
    `last_name` VARCHAR(50),
    `name_public` BOOLEAN DEFAULT True,
    `location` VARCHAR(50),
    `description` VARCHAR(500),
    `profile_image` VARCHAR(255),
    `role` ENUM ('traveller', 'moderator', 'editor', 'admin', 'supporttech') NOT NULL,
    `status` ENUM ('active', 'blocked', 'banned') NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `profile_public` BOOLEAN DEFAULT True,
    `places_public` BOOLEAN DEFAULT True,
    `likes_public` BOOLEAN DEFAULT True,
    `comments_public` BOOLEAN DEFAULT True,
    `achievement_count` INT NOT NULL DEFAULT 0 COMMENT 'Count of completed achievements (where progress >= goal)',
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `username` (`username`)
);

-- Create the table for journeys
CREATE TABLE `journeys` (
    `journey_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `title` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `start_date` DATE NOT NULL,
    `status` ENUM ('private', 'public', 'published') DEFAULT 'private',
    `is_hidden` BOOLEAN DEFAULT FALSE COMMENT 'Only visible to editors and admins',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `photo` VARCHAR(255),
    `first_viewer_id` INT DEFAULT NULL,
    PRIMARY KEY (`journey_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
);

-- Create the table for locations
CREATE TABLE `locations` (
    `location_id` INT NOT NULL AUTO_INCREMENT,
    `location_name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`location_id`),
    UNIQUE KEY `location_name` (`location_name`)
);

-- Create the table for events
CREATE TABLE `events` (
    `event_id` INT NOT NULL AUTO_INCREMENT,
    `journey_id` INT NOT NULL,
    `title` VARCHAR(100) NOT NULL,
    `description` TEXT,
    `start_datetime` DATETIME NOT NULL,
    `end_datetime` DATETIME,
    `location_id` INT,
    `like_count` INT NOT NULL DEFAULT 0,
    `comments_count` INT NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`event_id`),
    FOREIGN KEY (`journey_id`) REFERENCES `journeys` (`journey_id`),
    FOREIGN KEY (`location_id`) REFERENCES `locations` (`location_id`)
);

-- Create the table for event photos
CREATE TABLE `event_photos` (
    `photo_id` INT NOT NULL AUTO_INCREMENT,
    `event_id` INT NOT NULL,
    `photo_path` VARCHAR(255) NOT NULL,
    `uploaded_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`photo_id`),
    FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON DELETE CASCADE
);

-- Create the table for announcements
CREATE TABLE `announcements` (
    `announcement_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `title` VARCHAR(100) NOT NULL,
    `content` TEXT NOT NULL,
    `is_new` BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Indicates if the announcement is new',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`announcement_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
);

-- Create the table for sbuscription type
CREATE TABLE `subscription_types` (
    `subscription_type_id` INT NOT NULL AUTO_INCREMENT,
    `type` ENUM ('paid', 'free_trial', 'admin_granted') NOT NULL,
    `duration` INT NOT NULL COMMENT 'unit days',
    `price` DOUBLE(5, 2) NOT NULL,
    PRIMARY KEY (`subscription_type_id`)
);

-- Create the table for subscription
CREATE TABLE `subscriptions` (
    `subscription_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `subscription_type_id` int NOT NULL,
    `start_datetime` DATETIME,
    `end_datetime` DATETIME,
    `payment_amount` DOUBLE(5, 2) NOT NULL,
    `gst` BOOL NOT NULL,
    `billing_address` TEXT,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`subscription_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
    FOREIGN KEY (`subscription_type_id`) REFERENCES `subscription_types` (`subscription_type_id`)
);

-- Create the table for comments
CREATE TABLE `comments` (
    `comment_id` INT NOT NULL AUTO_INCREMENT,
    `event_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `content` TEXT NOT NULL,
    `is_hidden` BOOLEAN DEFAULT FALSE,
    `escalated` BOOLEAN DEFAULT FALSE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME ON UPDATE CURRENT_TIMESTAMP,
    `like_count` INT NOT NULL DEFAULT 0,
    `dislike_count` INT NOT NULL DEFAULT 0,
    PRIMARY KEY (`comment_id`),
    FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
);

-- Create the table for reports
CREATE TABLE `reports` (
    `report_id` INT NOT NULL AUTO_INCREMENT,
    `comment_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `reason` ENUM ('abusive', 'offensive', 'spam') NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`report_id`),
    FOREIGN KEY (`comment_id`) REFERENCES `comments` (`comment_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
    CONSTRAINT user_id_comment_id UNIQUE (user_id, comment_id)
);

-- Create the table for events and comments reaction
CREATE TABLE `reactions` (
    `reaction_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `event_id` INT,
    `comment_id` INT,
    `reaction_type` ENUM ('event', 'comment') NOT NULL,
    `is_like` BOOLEAN NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`reaction_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
    FOREIGN KEY (`comment_id`) REFERENCES `comments` (`comment_id`) ON DELETE CASCADE,
    FOREIGN KEY (`event_id`) REFERENCES `events` (`event_id`) ON DELETE CASCADE
);

-- Create the table for messages
CREATE TABLE `messages` (
    `message_id` INT NOT NULL AUTO_INCREMENT,
    `from` INT NOT NULL,
    `to` INT NOT NULL,
    `content` TEXT NOT NULL,
    `status` BOOLEAN NOT NULL COMMENT '1 non-read, 0 read',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`message_id`),
    FOREIGN KEY (`from`) REFERENCES `users` (`user_id`),
    FOREIGN KEY (`to`) REFERENCES `users` (`user_id`)
);

-- Create the table for follows
CREATE TABLE `follows` (
    `follow_id` INT NOT NULL AUTO_INCREMENT,
    `follower_id` INT NOT NULL,
    `followable_type` ENUM ('user', 'journey', 'location') NOT NULL,
    `followable_id` INT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`follow_id`),
    FOREIGN KEY (`follower_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
    CONSTRAINT follower_followable UNIQUE (follower_id, followable_type, followable_id)
);


-- Create the table for issues
CREATE TABLE
    `issues` (
        `issue_id` INT NOT NULL AUTO_INCREMENT,
        `title` VARCHAR(255) NOT NULL,
        `category` ENUM ('request', 'issue') NOT NULL,
        `content` TEXT NOT NULL,
        `status` ENUM ('New', 'Open', 'Stalled', 'Resolved', 'Delete') NOT NULL,
        `user_id` INT NOT NULL,
        `assigned_to` INT NULL,
        `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`issue_id`),
        FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
        FOREIGN KEY (`assigned_to`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
);

-- Create the table for comments of issues
CREATE TABLE
    `issue_comments` (
        `issue_comment_id` INT NOT NULL AUTO_INCREMENT,
        `issue_id` INT NOT NULL,
        `user_id` INT NOT NULL,
        `content` TEXT NOT NULL,
        `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`issue_comment_id`),
        FOREIGN KEY (`issue_id`) REFERENCES `issues` (`issue_id`) ON DELETE CASCADE,
        FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
);

-- Create the table for archievements
CREATE TABLE
    `achievement_types` (
        `achievement_type_id` INT NOT NULL AUTO_INCREMENT,

        `type` ENUM ('first_journey', 'first_event', 'first_public_journey', 'five_locations', 
        'seven_days_journey', 'first_published_journey', 'five_journeys_with_cover_image', 'five_comments_for_event',
        'ten_comments_for_event', 'twenty_comments_for_event', 'first_viewer', '20_event_likes', '40_event_likes', '60_event_likes') NOT NULL,
        `is_premium` BOOL NOT NULL DEFAULT FALSE,
        `goal` INT NOT NULL DEFAULT 1,
        `description` TEXT NOT NULL,
        PRIMARY KEY (`achievement_type_id`)
);

CREATE TABLE
    `achievements` (
        `achievement_id` INT NOT NULL AUTO_INCREMENT,
        `achievement_type_id` INT NOT NULL,
        `user_id` INT NOT NULL,
        `progress` INT NOT NULL,
        `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`achievement_id`),
        FOREIGN KEY (`achievement_type_id`) REFERENCES `achievement_types` (`achievement_type_id`) ON DELETE CASCADE,
        FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
        CONSTRAINT achievement_type_id_user_id UNIQUE (achievement_type_id, user_id)
);
