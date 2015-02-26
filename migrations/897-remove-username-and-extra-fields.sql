-- username does not exist anymore.
ALTER TABLE `users` CHANGE `username` `fxa_uid`  varchar(255);
-- We no longer log login attempts, since they fail at FxA level, before our code.
ALTER TABLE `users` DROP COLUMN `last_login_attempt`;
ALTER TABLE `users` DROP COLUMN `last_login_attempt_ip`;
ALTER TABLE `users` DROP COLUMN `failed_login_attempts`;
-- We no longer need the password field, but keep it for now because it's
-- easier. This migration reverts it to its default length.
ALTER TABLE `users` MODIFY `password` varchar(128);
