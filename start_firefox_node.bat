@echo off

java -jar selenium-server-4.44.0.jar node ^
--hub http://localhost:4444 ^

--config firefox-config.toml

pause