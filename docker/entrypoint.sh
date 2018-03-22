#!/bin/bash
mongod --dbpath /server_booking_system/db --fork --logpath=/server_booking_system/db/log --rest
/bin/bash